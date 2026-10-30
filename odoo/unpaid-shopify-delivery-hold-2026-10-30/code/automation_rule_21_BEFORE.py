# Automation rule 21 "Change status of Transfer (For Business Partners EU and Abroad)"
# Server action 1602 (Execute Code) - ORIGINAL code before 2026-10-30
# Model: Transfer | Trigger: On create and edit
# Before Update: [("state", "!=", "assigned")]
# Apply on: [ "&","&","&", ("picking_type_code","=","outgoing"), ("state","=","assigned"),
#             ("x_studio_auto_unreserved","=",False),
#             "|", ("sale_id.fiscal_position_id","in",[6,5]), ("sale_id.shopify_payment_gateway_id","in",[21]) ]
# When updating: sale_id, state, picking_type_code, x_studio_auto_unreserved
# Fiscal positions 5/6 = Business partner EU (with VAT ID) / Business partner abroad (non-EU); gateway 21 = Bank Deposit

for picking in records:

    # Only outgoing deliveries
    if picking.picking_type_code != 'outgoing':
        continue

    # Only when in Ready state
    if picking.state != 'assigned':
        continue

    # Prevent re-running
    if picking.x_studio_auto_unreserved:
        continue

    # STEP 1: Set done/reserved qty = 0 (unreserve)
    for move in picking.move_ids:
        for line in move.move_line_ids:
            line.write({
                'quantity': 0
            })

    # STEP 2: Remove reservation layer completely
    if picking.move_line_ids:
        picking.move_line_ids.unlink()

    # STEP 3: Force moves back to WAITING
    for move in picking.move_ids:
        if move.state not in ('done', 'cancel'):
            move.write({
                'state': 'confirmed'
            })

    # STEP 4: Force picking state to WAITING
    picking.write({
        'state': 'confirmed',
        'x_studio_auto_unreserved': True
    })
