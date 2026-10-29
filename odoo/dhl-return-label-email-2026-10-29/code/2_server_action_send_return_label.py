# Odoo 19 - Server Action (PRODUCTION id 1777, staging id 1774)
# Name:  Send return label
# Model: Transfer (stock.picking), Type: Execute Code, "Create Contextual Action" done
# Used by the buttons "Retourenlabel senden" / "Retourenlabel erneut senden" (view 3).
#
# 1. uses the existing LabelReturn PDF, or creates it via the DHL connector (print_return_label)
# 2. picks template (DE) or (EN) by the customer's language
# 3. opens the email composer on the HELPDESK TICKET if the return belongs to one
#    (customer replies come back into the ticket), otherwise on the return
# 4. attaches the DHL label + the reclamation form (Retourenschein) from the template

picking = record

def find_label(p):
    return env["ir.attachment"].search([
        ("res_model", "=", "stock.picking"), ("res_id", "=", p.id),
        ("mimetype", "=", "application/pdf"), ("name", "ilike", "LabelReturn")], order="id desc", limit=1)

label = find_label(picking)
if not label:
    if not picking.is_return_picking or picking.picking_type_code != "incoming" or picking.state == "done":
        raise UserError("%s is not an open return - no return label can be created." % picking.name)
    if not picking.carrier_id:
        raise UserError("No carrier on %s - please set DHL Parcel DE first." % picking.name)
    picking.print_return_label()
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
form_ids = [att.copy({"res_model": "mail.compose.message", "res_id": composer.id}).id for att in template.attachment_ids]
composer.write({"attachment_ids": [(4, label.id)] + [(4, i) for i in form_ids]})
# no tmp.unlink(): server actions may not delete mail.compose.message (access error); Odoo cleans it up

action = {
    "type": "ir.actions.act_window",
    "name": "Send return label" + (" – Ticket %s" % ticket.display_name if ticket else ""),
    "res_model": "mail.compose.message", "res_id": composer.id,
    "view_mode": "form", "views": [[False, "form"]], "target": "new"}
