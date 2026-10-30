# Automation rule 21 (suggested new name: "Unbezahlte Shopify-Lieferung zurück auf Wartend")
# Server action 1602 (Execute Code) - NEW code from 2026-10-30
# Model: Transfer | Trigger: On create and edit
# Before Update: [("state", "!=", "assigned")]          (unchanged)
# Apply on:      [("picking_type_code", "=", "outgoing"), ("state", "=", "assigned")]
# When updating: picking_type_code, state

allowed_logins = [
    'anastasiia.derkach@iq-dogsport.de',
    'florian.knabl@iq-dogsport.de',
    'elena.kistritz@iq-dogsport.de',
    'hamza.mohsin@iq-dogsport.de',
]

for picking in records:

    # Only outgoing deliveries in Ready state
    if picking.picking_type_code != 'outgoing' or picking.state != 'assigned':
        continue

    so = picking.sale_id

    # Rule 1: staff-created order (not Shopify) -> never blocked
    if not so or not so.shopify_instance_id:
        continue

    # Rule 2: Shopify order already paid -> may stay Ready
    posted = so.invoice_ids.filtered(lambda m: m.state == 'posted')
    if posted.filtered(lambda m: m.payment_state in ('paid', 'in_payment', 'reversed')):
        continue

    # Rule 3: allowed user clicked Check Availability on THIS order
    # (not stock coming in from validating a return/receipt)
    side_effect = bool(env.context.get('button_validate_picking_ids'))
    if env.user.login in allowed_logins and not side_effect:
        picking.message_post(body='Unbezahlte Shopify-Lieferung manuell freigegeben durch %s.' % env.user.name)
        continue

    # Otherwise: unpaid Shopify order -> back to Waiting
    for move in picking.move_ids:
        for line in move.move_line_ids:
            line.write({'quantity': 0})
    if picking.move_line_ids:
        picking.move_line_ids.unlink()
    for move in picking.move_ids:
        if move.state not in ('done', 'cancel'):
            move.write({'state': 'confirmed'})
    picking.write({'state': 'confirmed'})
    picking.message_post(body='Shopify-Bestellung nicht bezahlt – automatisch zurück auf Wartend.')
