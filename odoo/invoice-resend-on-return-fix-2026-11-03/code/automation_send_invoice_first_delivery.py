# Automation rule "IQ – Send invoice on first delivery"
# Production: https://iq-dogsport.odoo.com/odoo/automations/52?debug=1
# Model: Transfer (stock.picking) · Trigger: State is set to → Done
# Apply on: [("state", "=", "done"), ("picking_type_code", "=", "outgoing"), ("return_id", "=", False), ("sale_id", "!=", False)]
# Action: Execute Code
#
# [Hamza 2026-11-03] send invoice only on the FIRST delivery of the order, only invoices not sent yet
# replaces Cybrosys "Auto Send Invoice" (unticked) - it re-sent invoices on returns/exchanges
for picking in records:
    order = picking.sale_id
    if order.picking_ids.filtered(lambda p: p.id != picking.id and p.picking_type_code == 'outgoing' and p.state == 'done'):
        continue
    invoices = order.invoice_ids.filtered(lambda m: m.move_type == 'out_invoice' and m.state == 'posted' and not m.is_move_sent and m.partner_id.email)
    if invoices:
        picking._send_invoice_email(invoices)
