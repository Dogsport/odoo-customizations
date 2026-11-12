# Odoo 19 - Server Action (PRODUCTION id 1777, staging id 1774)
# Name:  Send return label   - v2, live since 12.11.2026 (v1: 29.10.2026)
# Model: Transfer (stock.picking), Type: Execute Code, "Create Contextual Action" done
# Used by the buttons "Retourenlabel senden" / "Retourenlabel erneut senden" (view "IQ – Send return label button").
#
# 1. uses the existing LabelReturn PDF, or creates it:
#    a) return HAS an outbound DHL shipment (tracking ref) -> BrowseInfo connector as before (print_return_label)
#    b) NO outbound DHL shipment (returns from Helpdesk tickets, old/GLS orders)
#       -> calls the connector's DHL request directly: env["dhl.request"].create_return_shipment(carrier, picking)
#          (the "no validated outbound DHL shipment" check is only in the connector's buttons, not in this method)
#          and saves the PDF exactly like the connector (name LabelReturn-..., description, chatter note)
#    "Return" = created with the Return button (is_return_picking) OR operation type is a Returns type
# 2. picks template (DE) or (EN) by the customer's language
# 3. opens the email composer on the HELPDESK TICKET if the return belongs to one, otherwise on the return
# 4. attaches the DHL label + the reclamation form (Retourenschein) from the template

picking = record

def find_label(p):
    return env["ir.attachment"].search([
        ("res_model", "=", "stock.picking"), ("res_id", "=", p.id),
        ("mimetype", "=", "application/pdf"), ("name", "ilike", "LabelReturn")], order="id desc", limit=1)

def dhl_source_picking(p):
    # same lookup as the BrowseInfo connector uses for its check
    src = env["stock.picking"]
    for move in p.move_ids:
        if move.origin_returned_move_id and move.origin_returned_move_id.picking_id:
            src = move.origin_returned_move_id.picking_id
            break
    if not src and p.origin:
        name = p.origin.replace("Return of", "").strip()
        src = env["stock.picking"].search([("name", "=", name)], limit=1)
    return src if (src and src.carrier_tracking_ref) else env["stock.picking"]

label = find_label(picking)
if not label:
    # return = created with the Return button OR operation type is a Returns type (e.g. returns from tickets)
    is_return_type = picking.is_return_picking or env["stock.picking.type"].search_count([("return_picking_type_id", "=", picking.picking_type_id.id)])
    if not is_return_type or picking.picking_type_code != "incoming" or picking.state == "done":
        raise UserError("%s is not an open return - no return label can be created." % picking.name)
    carrier = picking.carrier_id
    if not carrier:
        raise UserError("No carrier on %s - please set DHL Parcel DE first." % picking.name)

    if dhl_source_picking(picking):
        # a) normal case - unchanged
        picking.print_return_label()
    else:
        # b) no outbound DHL shipment -> create the return label directly
        if carrier.delivery_type != "dhl_parcel_de":
            raise UserError("%s has no outbound DHL shipment and the carrier is '%s'. Please set carrier DHL Parcel DE." % (picking.name, carrier.name))
        partner = picking.partner_id
        if not partner:
            raise UserError("No customer (Receive From) on %s." % picking.name)
        if not picking.dhl_return_receiver_id:
            country = partner.country_id or partner.commercial_partner_id.country_id
            if country and country.code == "DE":
                picking.write({"dhl_return_receiver_id": "deu"})
            else:
                raise UserError("No DHL return receiver for %s (country %s). DHL returns are currently only set up for Germany - please create the label manually." % (picking.name, country.name if country else "-"))
        result = env["dhl.request"].create_return_shipment(carrier, picking)
        if not result or not result.get("label_b64"):
            raise UserError("DHL did not return a label for %s. Please check the customer address." % picking.name)
        tracking_no = result.get("tracking_number")
        att = env["ir.attachment"].create({
            "name": "%s-%s.pdf" % (carrier.get_return_label_prefix(), tracking_no),
            "type": "binary",
            "datas": result.get("label_b64"),
            "res_model": "stock.picking",
            "res_id": picking.id,
            "mimetype": "application/pdf",
            "description": "System generated DHL Return Label",
        })
        picking.write({"carrier_tracking_ref": tracking_no})
        picking.message_post(
            body="DHL Return shipping label attached. Tracking Number: %s (IQ: created without outbound DHL shipment)" % tracking_no,
            attachment_ids=[att.id])

    label = find_label(picking)
    if not label:
        raise UserError("The return label was created, but no 'LabelReturn' PDF was found on %s. Please check the chatter." % picking.name)

lang = (picking.partner_id.lang or "").lower()
key = "(DE)" if lang.startswith("de") else "(EN)"
template = env["mail.template"].search([("model", "=", "stock.picking"), ("name", "ilike", "Return label for customer " + key)], limit=1)
if not template:
    raise UserError("Email template 'IQ – Return label for customer %s' not found." % key)
tmp = env["mail.compose.message"].create({
    "model": "stock.picking", "res_ids": str([picking.id]),
    "composition_mode": "comment", "template_id": template.id})
subject, body = tmp.subject, tmp.body

ticket = env["helpdesk.ticket"]
# .sudo(): ir.model.fields is readable for administrators only (access error for Elena on 29.10.)
if env["ir.model.fields"].sudo().search_count([("model", "=", "helpdesk.ticket"), ("name", "=", "picking_ids")]):
    ticket = env["helpdesk.ticket"].search([("picking_ids", "in", picking.ids)], order="id desc", limit=1)
model, res_id = ("helpdesk.ticket", ticket.id) if ticket else ("stock.picking", picking.id)

composer = env["mail.compose.message"].create({
    "model": model, "res_ids": str([res_id]), "composition_mode": "comment",
    "subject": subject, "body": body,
    "partner_ids": [(6, 0, [picking.partner_id.id])]})
# template attachments are not copied when the composer is created from code -> copy them
form_ids = [a.copy({"res_model": "mail.compose.message", "res_id": composer.id}).id for a in template.attachment_ids]
composer.write({"attachment_ids": [(4, label.id)] + [(4, i) for i in form_ids]})
# no tmp.unlink(): server actions may not delete mail.compose.message (access error); Odoo cleans it up

action = {
    "type": "ir.actions.act_window",
    "name": "Send return label" + (" – Ticket %s" % ticket.display_name if ticket else ""),
    "res_model": "mail.compose.message", "res_id": composer.id,
    "view_mode": "form", "views": [[False, "form"]], "target": "new"}
