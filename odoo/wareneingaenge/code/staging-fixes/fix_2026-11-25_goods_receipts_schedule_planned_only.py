# IQ Goods Receipts – update 25.11.2026: tab "Delivery schedule" shows only PLANNED / expected deliveries
#  - The lines "Geliefert (WH1/IN/…)" (written by the automation "IQ Wareneingang: gelieferte Ware in Kalender" when a receipt
#    is validated) are no longer shown in this tab. They are NOT deleted: the warehouse calendar still shows them as delivered.
#  - Booked goods are visible in the tabs Overview (Booked / size table) and Receipts.
#  - The total at the bottom of the tab = planned deliveries only.
#  - Technically: filter (domain) on the existing field x_schedule_ids. No new field, no data deleted.
#    Undo: run this file again with UNDO = True.
# Install: Settings -> Technical -> Scheduled Actions -> New -> Model "Scheduled Actions" -> paste -> Save -> Run Manually.
#          STAGING first. Afterwards: Settings -> Technical -> Logging, search "IQ goods receipts 25.11 schedule".

UNDO = False
DOM = "['|', ('x_shipment', '=', False), '!', ('x_shipment', '=like', 'Geliefert%')]"

F = env['ir.model.fields'].sudo().search([('model', '=', 'x_wareneingang'), ('name', '=', 'x_schedule_ids')], limit=1)
if not F or F.ttype != 'one2many':
    raise UserError('Field x_schedule_ids (one2many) on x_wareneingang not found – nothing changed.')
new = '[]' if UNDO else DOM
state = 'unchanged'
if (F.domain or '[]') != new:
    F.write({'domain': new})
    state = 'undone' if UNDO else 'filter set'
# check on one card
card = env['x_wareneingang'].sudo().search([('x_schedule_ids', '!=', False)], limit=1)
hidden = env['x_wareneingang_line'].sudo().search_count([('x_shipment', '=like', 'Geliefert%')])
log('IQ goods receipts 25.11 schedule planned only: ' + state + ' | delivered lines kept in data (hidden in tab): ' + str(hidden), level='info')
