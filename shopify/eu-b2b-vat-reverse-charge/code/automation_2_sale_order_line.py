# Odoo 19 - Automation Rule (PRODUCTION since 28.10.2026)
# Name:     IQ - EU VAT: 0% tax on reverse-charge lines
# Model:    Sales Order Line (sale.order.line)
# Trigger:  On create
# Apply on: [("order_id.shopify_instance_id", "!=", False), ("order_id.fiscal_position_id.vat_required", "=", True)]
# Action:   Execute Code
#
# Safety net: Emipro creates order lines WITHOUT tax when Shopify sends no tax lines
# (reverse charge). Such a line gets the product tax mapped through the order's
# fiscal position (-> 0% EU D). Lines that already have a tax are never touched.

tax_field = "tax_ids" if env["ir.model.fields"].search_count([("model", "=", "sale.order.line"), ("name", "=", "tax_ids")]) else "tax_id"
for line in records:
    try:
        order = line.order_id
        fp = order.fiscal_position_id
        if not fp or not fp.vat_required or line[tax_field] or not line.product_id:
            continue
        taxes = line.product_id.taxes_id.filtered(lambda t: t.company_id == order.company_id)
        mapped = fp.map_tax(taxes)
        if mapped:
            line.write({tax_field: [(6, 0, mapped.ids)]})
            order.message_post(body="IQ VAT: line '%s' -> tax %s (fiscal position %s)." % (line.product_id.display_name, ", ".join(mapped.mapped("name")), fp.display_name))
    except Exception as e:
        line.order_id.message_post(body="IQ VAT: tax on line skipped because of an error: %s" % e)
