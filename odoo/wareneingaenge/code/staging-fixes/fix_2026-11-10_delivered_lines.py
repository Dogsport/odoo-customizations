# IQ Goods Receipts – delivered goods in "Upcoming deliveries"   10.11.2026
# Run once: Scheduled Action (Model: Contact, Active = off) -> paste -> Save -> Run Manually -> reload.
# What it does (no new fields):
#  1. New automation "IQ Wareneingang: gelieferte Ware in Kalender" on receipts (stock.picking):
#     when a purchase receipt is validated -> one ARRIVED line per purchase order and day in Upcoming deliveries
#     ("✓ 90 · Farrado Sensitive Buffalo · P00073", date = booking date, pieces delivered, kits as sets),
#     sets the card's "Arrived" date if empty, and closes old planned lines once the order is fully received.
#  2. One-time fill for all receipts validated since 01.01.2026 (safe to run again – nothing is counted twice).
#  3. "Upcoming deliveries" opens without the default filter "Not arrived" (filter stays available).
# Afterwards check Settings -> Technical -> Logging, search "IQ delivered".

CODE = r'''
Line = env['x_wareneingang_line'].sudo()
WE = env['x_wareneingang'].sudo()
Move = env['stock.move'].sudo()
DE = (env.lang or 'de_DE').startswith('de')
TAG = 'Geliefert'
for p in records:
    if p.state != 'done' or not p.purchase_id or p.picking_type_code != 'incoming' or not p.date_done:
        continue
    po = p.purchase_id
    # products + delivered pieces (kit parts counted as sets)
    names = []
    qty = 0.0
    kit = {}
    for mv in p.move_ids:
        if mv.state != 'done':
            continue
        pl = mv.purchase_line_id
        tmpl = pl.product_id.product_tmpl_id if pl else mv.product_id.product_tmpl_id
        n = (tmpl.name or '').split(' – ')[0]
        if n and n not in names:
            names.append(n)
        if pl and mv.product_id != pl.product_id:
            kit[pl.id] = kit.get(pl.id, 0.0) + (mv.quantity or 0.0)
        else:
            qty += mv.quantity or 0.0
    for plid in kit:
        pl = env['purchase.order.line'].sudo().browse(plid)
        total = sum(Move.search([('purchase_line_id', '=', plid), ('state', '!=', 'cancel')]).mapped('product_uom_qty'))
        qty += round(kit[plid] / total * pl.product_qty) if total and pl.product_qty else 0
    if not qty:
        continue
    we = WE.search([('x_studio_purchase_order', '=', po.id)], limit=1)
    if not we:
        we = WE.create({'x_name': po.name, 'x_studio_purchase_order': po.id, 'x_studio_supplier': po.partner_id.id,
                        'x_supplier_ref': po.partner_ref or False})
    d = p.date_done.date()
    prod = (names[0] + (' +' + str(len(names) - 1) if len(names) > 1 else '')) if names else po.name
    line = Line.search([('x_wareneingang_id', '=', we.id), ('x_date', '=', d), ('x_shipment', '=like', TAG + '%')], limit=1)
    if line:
        if p.name in (line.x_shipment or ''):
            continue
        newq = (line.x_qty or 0) + qty
        ship = (line.x_shipment or '').rstrip(')') + ', ' + p.name + ')'
        line.write({'x_qty': newq, 'x_shipment': ship,
                    'x_name': '✓ ' + str(int(newq)) + ' · ' + (line.x_product_text or prod) + ' · ' + po.name})
    else:
        Line.create({'x_wareneingang_id': we.id, 'x_partner_id': po.partner_id.id, 'x_supplier_ref': po.partner_ref or po.name,
                     'x_product_text': prod, 'x_shipment': TAG + ' (' + p.name + ')', 'x_qty': qty, 'x_date': d, 'x_done': True,
                     'x_name': '✓ ' + str(int(qty)) + ' · ' + prod + ' · ' + po.name})
    if not we.x_studio_arrival_date:
        we.write({'x_studio_arrival_date': d})
    if po.receipt_status == 'full':
        Line.search([('x_wareneingang_id', '=', we.id), ('x_done', '=', False)]).write({'x_done': True})
'''

IrModel = env['ir.model'].sudo()
Fields = env['ir.model.fields'].sudo()
Auto = env['base.automation'].sudo()
SA = env['ir.actions.server'].sudo()
NAME = 'IQ Wareneingang: gelieferte Ware in Kalender'
pm = IrModel.search([('model', '=', 'stock.picking')], limit=1)
auto = Auto.search([('name', '=', NAME)], limit=1)
if auto:
    auto.action_server_ids.write({'code': CODE})
else:
    auto = Auto.create({
        'name': NAME, 'model_id': pm.id, 'trigger': 'on_create_or_write',
        'trigger_field_ids': [(6, 0, Fields.search([('model', '=', 'stock.picking'), ('name', '=', 'state')]).ids)],
        'filter_domain': "[('state', '=', 'done'), ('purchase_id', '!=', False), ('picking_type_code', '=', 'incoming')]",
        'action_server_ids': [(0, 0, {'name': NAME, 'model_id': pm.id, 'state': 'code', 'usage': 'base_automation', 'code': CODE})],
    })

# one-time fill: all purchase receipts validated since 01.01.2026 (oldest first)
picks = env['stock.picking'].sudo().search([('state', '=', 'done'), ('purchase_id', '!=', False), ('picking_type_code', '=', 'incoming'),
                                            ('date_done', '>=', datetime.datetime(2026, 1, 1))], order='date_done asc')
before = env['x_wareneingang_line'].sudo().search_count([('x_shipment', '=like', 'Geliefert%')])
if picks:
    auto.action_server_ids[0].with_context(active_model='stock.picking', active_ids=picks.ids, active_id=picks.ids[0]).run()
after = env['x_wareneingang_line'].sudo().search_count([('x_shipment', '=like', 'Geliefert%')])

# Upcoming deliveries: no default "Not arrived" filter (still available in the search)
act = env['ir.actions.act_window'].sudo().search([('res_model', '=', 'x_wareneingang_line')], limit=1)
if act:
    act.write({'context': "{'search_default_g_month': 1}"})

log('IQ delivered installed | automation: ' + NAME + ' | receipts since 01.01.2026: ' + str(len(picks))
    + ' | delivered lines before/after: ' + str(before) + ' / ' + str(after)
    + ' | Upcoming deliveries default filter removed: ' + ('yes' if act else 'action not found'))
