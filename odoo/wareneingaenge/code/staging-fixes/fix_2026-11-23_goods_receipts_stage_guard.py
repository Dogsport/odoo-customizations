# IQ Goods Receipts – update 23.11.2026 (b): columns "Partly booked" and "Done" only through booking
#  New automation "IQ Wareneingang: Status nur durch Buchung" (Goods Receipts, runs when the column of a card changes):
#  - "Partly booked": only if the card has a purchase order AND something of it is booked in Odoo
#  - "Done": only if the card has a purchase order, something is booked AND everything is booked
#    (or no open receipt is left, e.g. the rest was cancelled)
#  - Settings admins may move every card anywhere (e.g. samples without a purchase order)
#  - "Expected", "Ware angekommen" and "Rejected" stay free for everybody
#  If not allowed, the card jumps back and a message explains why. The existing automation
#  "IQ Wareneingang: Status bei Buchung" keeps working (it only sets these columns after a booking).
#  No new fields, no change to existing automations.
# Install: Settings -> Technical -> Scheduled Actions -> New -> Model "Scheduled Actions" (ir.cron), Python code = this file,
#          Save -> "Run Manually". Run it on STAGING first. Running it twice is harmless (updates the code).
# Afterwards check Settings -> Technical -> Logging, search "IQ goods receipts 23.11b".

MODEL = 'x_wareneingang'
NAME = 'IQ Wareneingang: Status nur durch Buchung'
IrModel = env['ir.model'].sudo()
Fields = env['ir.model.fields'].sudo()
Auto = env['base.automation'].sudo()

GUARD = r'''
Stage = env['x_wareneingang_stage'].sudo().with_context(lang='en_US')
part = Stage.search([('x_name', 'in', ['Partly booked', 'Teilweise gebucht'])], limit=1)
done = Stage.search([('x_name', 'in', ['Done', 'Fertig'])], limit=1)
admin = env.uid == 1 or env.user.has_group('base.group_system')
if not admin:
    for we in records:
        st = we.x_studio_stage_id
        if not st or st.id not in (part.id, done.id):
            continue
        po = we.x_studio_purchase_order
        if not po:
            raise UserError('„' + (we.x_name or '') + '“: Ohne Bestellung kann die Karte nicht auf „' + st.x_name + '“ gesetzt werden – das darf nur ein Admin (z. B. Muster).\n'
                            'Without a purchase order this card cannot be moved to "' + st.x_name + '" – only an admin can do that (e.g. samples).')
        lines = po.order_line.filtered(lambda l: l.product_qty > 0 and l.product_id and l.product_id.type != 'service')
        booked = sum(lines.mapped('qty_received'))
        if booked <= 0:
            raise UserError('„' + (we.x_name or '') + '“: Noch nichts gebucht – bitte zuerst den Wareneingang in Odoo buchen. Dann wechselt die Karte von selbst.\n'
                            'Nothing booked yet – please book the receipt in Odoo first. The card then moves by itself.')
        if st.id == done.id:
            all_in = lines and not lines.filtered(lambda l: l.qty_received < l.product_qty)
            open_rc = env['stock.picking'].sudo().search_count([('purchase_id', '=', po.id), ('picking_type_code', '=', 'incoming'), ('state', 'not in', ['done', 'cancel'])])
            if not all_in and open_rc:
                raise UserError('„' + (we.x_name or '') + '“: Noch nicht alles gebucht (' + str(int(booked)) + ' von ' + str(int(sum(lines.mapped('product_qty')))) + ' Stk.) – die Karte bleibt bei „Teilweise gebucht“.\n'
                                'Not everything is booked yet – the card stays in "Partly booked". If the rest will not come, cancel the open receipt first.')
'''

m = IrModel.search([('model', '=', MODEL)], limit=1)
trig = Fields.search([('model', '=', MODEL), ('name', '=', 'x_studio_stage_id')], limit=1)
if not m or not trig:
    raise UserError('Goods Receipts model or its stage field not found – nothing changed.')
a = Auto.search([('name', '=', NAME)], limit=1)
if a:
    a.action_server_ids.write({'code': GUARD})
    a.write({'trigger': 'on_create_or_write', 'trigger_field_ids': [(6, 0, trig.ids)], 'active': True})
    what = 'updated'
else:
    Auto.create({'name': NAME, 'model_id': m.id, 'trigger': 'on_create_or_write', 'trigger_field_ids': [(6, 0, trig.ids)],
                 'action_server_ids': [(0, 0, {'name': NAME, 'model_id': m.id, 'state': 'code', 'usage': 'base_automation', 'code': GUARD})]})
    what = 'created'

log('IQ goods receipts 23.11b stage guard ' + what, level='info')
