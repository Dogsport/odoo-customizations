# Odoo 19 - Server Action (read only report, changes nothing)
# Name:  IQ - VAT dry run (read only)
# Model: Sales Order, Type: Execute Code, then "Create Contextual Action".
# Use:   select orders > Action > IQ - VAT dry run (read only) -> popup report.

MARK = "A valid VAT number:"
QUERY = "query($id: ID!) { order(id: $id) { totalTaxSet { shopMoney { amount } } events(first: 50) { nodes { message } } } }"
out = []
for order in records:
    try:
        code = order.partner_shipping_id.country_id.code or ""
        if not order.shopify_order_id or not order.shopify_instance_id:
            out.append("%s: not a Shopify order - skip" % order.name)
            continue
        res = order.shopify_instance_id.get_graphql_client().execute(QUERY, {"id": "gid://shopify/Order/%s" % order.shopify_order_id})
        if not isinstance(res, dict):
            res = res.to_dict()
        so = (res.get("data", res) or {}).get("order") or {}
        tax = float(((so.get("totalTaxSet") or {}).get("shopMoney") or {}).get("amount") or 0)
        vat = False
        for ev in ((so.get("events") or {}).get("nodes") or []):
            msg = ev.get("message") or ""
            if "Reverse charge was applied" in msg and MARK in msg:
                vat = msg.split(MARK)[1].strip().split(" ")[0].strip()
        out.append("%s: %s | Shopify tax %.2f | reverse-charge VAT: %s | Odoo fiscal position: %s | Odoo tax %.2f"
                   % (order.name, code, tax, vat or "-", order.fiscal_position_id.display_name or "-", order.amount_tax))
    except Exception as e:
        out.append("%s: error %s" % (order.name, e))
raise UserError("\n".join(out))
