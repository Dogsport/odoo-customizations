# Odoo 19 - Automation Rule (PRODUCTION since 28.10.2026)
# Name:     IQ - EU VAT from Shopify reverse charge
# Model:    Sales Order (sale.order)
# Trigger:  On create
# Apply on: see domain_automation_1.txt
# Action:   Execute Code (paste everything below this header)
#
# What it does: when Shopify applied reverse charge ("Reverse charge was applied.
# A valid VAT number: XX..." in the Shopify order events), store the VAT ID on the
# customer (Odoo runs the VIES check), set the "VAT required" fiscal position
# (Business partner EU (with VAT ID)), update taxes (0% EU D) and post a note.
# Never changes prices. Skips dealers that already have VAT + B2B fiscal position.

MARK = "A valid VAT number:"
QUERY = "query($id: ID!) { order(id: $id) { events(first: 50) { nodes { message } } } }"
for order in records:
    try:
        if not order.shopify_order_id:
            continue
        partner = order.partner_invoice_id.commercial_partner_id
        # dealer with VAT already in Odoo and correct fiscal position -> nothing to do
        if partner.vat and order.fiscal_position_id.vat_required:
            continue
        country = order.partner_shipping_id.country_id
        code = country.code or ""
        res = order.shopify_instance_id.get_graphql_client().execute(QUERY, {"id": "gid://shopify/Order/%s" % order.shopify_order_id})
        if not isinstance(res, dict):
            res = res.to_dict()
        so = (res.get("data", res) or {}).get("order") or {}
        vat = False
        for ev in ((so.get("events") or {}).get("nodes") or []):
            msg = ev.get("message") or ""
            if "Reverse charge was applied" in msg and MARK in msg:
                vat = msg.split(MARK)[1].strip().split(" ")[0].strip()
        if not vat:
            continue
        prefix = "EL" if code == "GR" else code
        if not vat.startswith(prefix) or not vat.isalnum():
            order.message_post(body="IQ VAT: VAT %s does not match delivery country %s - nothing changed, please check." % (vat, code))
            continue
        # 1. store VAT ID on the customer (Odoo runs the VIES check)
        if not partner.vat:
            partner.write({"vat": vat})
            partner.message_post(body="VAT ID %s taken from Shopify order %s." % (vat, order.name))
        elif partner.vat.replace(" ", "").upper() != vat:
            order.message_post(body="IQ VAT: customer already has VAT %s, Shopify says %s - customer not changed, please check." % (partner.vat, vat))
            continue
        # 2. fiscal position + taxes, only if not already B2B
        if not order.fiscal_position_id.vat_required:
            fp = env["account.fiscal.position"].search([
                ("auto_apply", "=", True), ("vat_required", "=", True),
                ("country_group_id.country_ids", "in", country.id),
                ("company_id", "in", [order.company_id.id, False])], order="sequence", limit=1)
            if fp:
                order.write({"fiscal_position_id": fp.id})
                if order.order_line and order.invoice_status != "invoiced":
                    order.action_update_taxes()
        order.message_post(body="IQ VAT: This order contains VAT ID %s (Shopify reverse charge). Customer updated, fiscal position: %s." % (vat, order.fiscal_position_id.display_name))
    except Exception as e:
        order.message_post(body="IQ VAT: could not process VAT ID: %s" % e)
