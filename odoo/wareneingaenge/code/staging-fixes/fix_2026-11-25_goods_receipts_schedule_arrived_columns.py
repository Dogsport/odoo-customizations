# IQ Goods Receipts – update 25.11.2026: Delivery schedule shows what ARRIVED per delivery (Lieferschein + counted)
#  Approved by Hamza 25.11.2026: 2 NEW FIELDS on the schedule line (x_wareneingang_line):
#     x_qty_ls       "Delivery note"  (pieces according to the Lieferschein / packing list)
#     x_qty_counted  "Counted"        (pieces counted by the warehouse)
#  - New automation "IQ Wareneingang: Meldung in Lieferplan": every time goods are reported as arrived
#    ("Ware angekommen" in the calendar, or a later added delivery like the October packing list),
#    the matching planned line gets Delivery note + Counted and is switched to Arrived.
#    Matching planned line = the line chosen in the calendar, otherwise the planned line dated up to 30 days before /
#    7 days after the report. If there is none (October on P00061), a NEW line "Angekommen" is added (Qty = counted).
#  - A correction (same receipt, same day or same Lieferschein no.) updates the same line – nothing is counted twice.
#  - Tab "Delivery schedule": new columns "Delivery note" and "Counted" (red when they differ, green when equal), with totals.
#  - One-time fill for all reports that already exist (P00061 October 160, P00062 October 160, November reports …).
#  Running it again is harmless. Nothing is booked, nothing is deleted.
# Install: Settings -> Technical -> Scheduled Actions -> New -> Model "Scheduled Actions" -> paste -> Save -> Run Manually.
#          STAGING first. Afterwards: Settings -> Technical -> Logging, search "IQ goods receipts 25.11 schedule arrived".

CODE = r'''
Line = env['x_wareneingang_line'].sudo()
ATT = env['ir.attachment'].sudo()
WE = env['x_wareneingang'].sudo()
cids = []
for a0 in records:
    if a0.res_model == 'x_wareneingang' and a0.res_id and a0.res_id not in cids:
        cids.append(a0.res_id)
for cid in cids:
    card = WE.browse(cid).exists()
    if not card:
        continue
    po = card.x_studio_purchase_order
    reps = {}
    for a in ATT.with_context(bin_size=False).search([('res_model', '=', 'x_wareneingang'), ('res_id', '=', cid), ('name', '=like', 'Wareneingang-Meldung %')], order='id'):
        body = (a.raw or b'').decode('utf-8', 'ignore').split(chr(10))
        if not body or not body[0].startswith('IQ-ARRIVAL|'):
            continue
        hd = body[0].split('|')
        pid_ = int(hd[3]) if len(hd) > 3 and hd[3].isdigit() else 0
        ts_ = int(hd[1]) if len(hd) > 1 and hd[1].isdigit() else 0
        day_ = (ts_ + 3600) // 86400
        lsn_ = (hd[6].strip().upper().replace('LS', '').replace(' ', '') if len(hd) > 6 else '')
        inh = []
        for k_ in list(reps.keys()):
            if reps[k_]['pid'] == pid_ and (reps[k_]['day'] == day_ or (lsn_ and reps[k_]['lsn'] == lsn_)):
                inh += reps[k_]['inh'] + [reps[k_]['att']]
                reps.pop(k_)
        reps[a.id] = {'att': a, 'hd': hd, 'body': body, 'day': day_, 'lsn': lsn_, 'pid': pid_, 'ts': ts_, 'inh': inh}
    eff = sorted(reps.values(), key=lambda r: (r['ts'], r['att'].id))
    used = []
    for r in eff:
        r['ds'] = datetime.date(1970, 1, 1) + datetime.timedelta(days=r['day'])
        r['rows'] = []
        for ln_ in r['body'][1:]:
            if ' · laut Lieferschein ' not in ln_ or ' · gezählt ' not in ln_:
                continue
            nm_ = ln_.split(': laut Lieferschein ', 1)[0] if ': laut Lieferschein ' in ln_ else ln_.rsplit(': offen ', 1)[0]
            v1 = ln_.split(' · laut Lieferschein ', 1)[1].split(' · ', 1)[0].strip() if ' · laut Lieferschein ' in ln_ else ln_.split(': laut Lieferschein ', 1)[1].split(' · ', 1)[0].strip()
            v2 = ln_.split(' · gezählt ', 1)[1].strip()
            lq = int(v1) if v1.isdigit() else -1
            cq = int(v2) if v2.isdigit() else -1
            r['rows'].append([nm_.strip(), lq, cq])
        # line already linked to this report (or to a report it corrected)?
        r['line'] = Line
        for aa in [r['att']] + r['inh']:
            dsc = aa.description or ''
            if dsc.startswith('IQ-SCHED:') and dsc[9:].strip().isdigit():
                l0 = Line.browse(int(dsc[9:].strip())).exists()
                if l0 and l0.x_wareneingang_id.id == cid and l0.id not in used:
                    r['line'] = l0
                    break
        if r['line']:
            used.append(r['line'].id)
    for r in eff:
        a = r['att']
        hd = r['hd']
        ds = r['ds']
        if not po:
            # goods without purchase order: the lines were created with the report – fill per product
            for rw in r['rows']:
                l1 = Line.search([('x_wareneingang_id', '=', cid), ('x_product_text', '=', rw[0][:120]), ('x_date', '=', ds), ('id', 'not in', used)], limit=1)
                if l1:
                    used.append(l1.id)
                    l1.write({'x_qty_ls': max(rw[1], 0), 'x_qty_counted': rw[2] if rw[2] >= 0 else max(rw[1], 0), 'x_done': True})
            continue
        ls_ok = [x[1] for x in r['rows'] if x[1] >= 0]
        cn_ok = [(x[2] if x[2] >= 0 else x[1]) for x in r['rows'] if x[2] >= 0 or x[1] >= 0]
        if not cn_ok:
            continue
        lsq = sum(ls_ok)
        cnt = sum(cn_ok)
        ln = r['line']
        if not ln and len(hd) > 4 and hd[4].isdigit() and int(hd[4]):
            l2 = Line.browse(int(hd[4])).exists()
            if l2 and l2.x_wareneingang_id.id == cid and l2.id not in used and not (l2.x_shipment or '').startswith('Geliefert'):
                ln = l2
        if not ln:
            cand = Line.search([('x_wareneingang_id', '=', cid), ('id', 'not in', used), ('x_date', '!=', False),
                                ('x_date', '>=', ds - datetime.timedelta(days=30)), ('x_date', '<=', ds + datetime.timedelta(days=7))], order='x_date desc, id')
            cand = cand.filtered(lambda c: not c.x_qty_counted and not (c.x_shipment or '').startswith('Geliefert'))
            if cand:
                ln = cand[0]
        vals = {'x_qty_ls': lsq, 'x_qty_counted': cnt, 'x_done': True}
        if not ln:
            lsno = (hd[6].strip() if len(hd) > 6 else '')
            prod = (hd[10].strip() if len(hd) > 10 else '') or po.name
            vals.update({'x_wareneingang_id': cid, 'x_partner_id': po.partner_id.id, 'x_supplier_ref': card.x_supplier_ref or po.partner_ref or po.name,
                         'x_product_text': prod[:120], 'x_shipment': 'Angekommen' + ((' · LS ' + lsno) if lsno else ''),
                         'x_qty': cnt, 'x_date': ds, 'x_name': '↓ ' + str(int(cnt)) + ' · ' + prod[:60] + ' · ' + po.name})
            ln = Line.create(vals)
        else:
            ln.write(vals)
        used.append(ln.id)
        if (a.description or '') != 'IQ-SCHED:' + str(ln.id):
            a.write({'description': 'IQ-SCHED:' + str(ln.id)})
'''

IrModel = env['ir.model'].sudo()
Fields = env['ir.model.fields'].sudo()
Auto = env['base.automation'].sudo()
LM = IrModel.search([('model', '=', 'x_wareneingang_line')], limit=1)
AM = IrModel.search([('model', '=', 'ir.attachment')], limit=1)
if not LM or not AM:
    raise UserError('Model x_wareneingang_line or ir.attachment not found – nothing changed.')

# 1. the two approved fields
newf = []
for fn, en, de in [('x_qty_ls', 'Delivery note', 'Lieferschein'), ('x_qty_counted', 'Counted', 'Gezählt')]:
    f = Fields.search([('model', '=', 'x_wareneingang_line'), ('name', '=', fn)], limit=1)
    if not f:
        f = Fields.create({'model_id': LM.id, 'name': fn, 'field_description': en, 'ttype': 'float', 'state': 'manual', 'copied': False})
        newf.append(fn)
    try:
        f.update_field_translations('field_description', {'de_DE': de})
    except Exception:
        pass

# 2. schedule list in the form: two new columns after Qty
View = env['ir.ui.view'].sudo()
OLD = '<field name="x_qty" string="Qty" digits="[16,0]" sum="Total"/>'
NEW = (OLD + '<field name="x_qty_ls" string="Delivery note" digits="[16,0]" sum="Total" optional="show" invisible="not x_qty_ls"/>'
       '<field name="x_qty_counted" string="Counted" digits="[16,0]" sum="Total" optional="show" invisible="not x_qty_counted"'
       ' decoration-danger="x_qty_ls and x_qty_counted != x_qty_ls" decoration-success="x_qty_ls and x_qty_counted == x_qty_ls"/>')
vstate = []
for v in View.search([('model', '=', 'x_wareneingang'), ('type', '=', 'form')]):
    arch = v.with_context(lang='en_US').arch_db or ''
    if 'name="x_qty_counted"' in arch:
        vstate.append((v.name or str(v.id)) + ' already ok')
    elif arch.count(OLD) == 1:
        v.with_context(lang='en_US').write({'arch': arch.replace(OLD, NEW)})
        try:
            v.update_field_translations('arch_db', {'de_DE': {'Delivery note': 'Lieferschein', 'Counted': 'Gezählt'}})
        except Exception:
            pass
        vstate.append((v.name or str(v.id)) + ' columns added')
if not vstate:
    raise UserError('Delivery schedule list (Qty column) not found in the Goods Receipt form – fields created, view NOT changed. Please send this message to Claude.')

# 3. automation on the arrival reports
NAME = 'IQ Wareneingang: Meldung in Lieferplan'
auto = Auto.search([('name', '=', NAME)], limit=1)
if auto:
    auto.action_server_ids.write({'code': CODE})
else:
    auto = Auto.create({
        'name': NAME, 'model_id': AM.id, 'trigger': 'on_create_or_write',
        'trigger_field_ids': [(6, 0, Fields.search([('model', '=', 'ir.attachment'), ('name', '=', 'name')]).ids)],
        'filter_domain': "[('res_model', '=', 'x_wareneingang'), ('name', '=like', 'Wareneingang-Meldung %')]",
        'action_server_ids': [(0, 0, {'name': NAME, 'model_id': AM.id, 'state': 'code', 'usage': 'base_automation', 'code': CODE})],
    })

# 4. one-time fill for all existing reports
reps = env['ir.attachment'].sudo().search([('res_model', '=', 'x_wareneingang'), ('name', '=like', 'Wareneingang-Meldung %')], order='id')
fill = 'no reports'
if reps:
    try:
        auto.action_server_ids[0].with_context(active_model='ir.attachment', active_ids=reps.ids, active_id=reps.ids[0]).run()
        fill = str(len(reps)) + ' reports on ' + str(len(set(reps.mapped('res_id')))) + ' cards'
    except Exception as e:
        fill = 'FAILED (' + str(e)[:200] + ') – fields are created now, please run this file once more'
chk = []
for pon in ('P00061', 'P00062'):
    c = env['x_wareneingang'].sudo().search([('x_studio_purchase_order.name', '=', pon)], limit=1)
    if c:
        ls_ = env['x_wareneingang_line'].sudo().search([('x_wareneingang_id', '=', c.id)], order='x_date').filtered(lambda l: l.x_qty_counted)
        chk.append(pon + ': ' + ', '.join([(l.x_date.strftime('%d.%m.') if l.x_date else '?') + ' ' + (l.x_shipment or '') + ' LS ' + str(int(l.x_qty_ls)) + ' / counted ' + str(int(l.x_qty_counted)) for l in ls_]))
log('IQ goods receipts 25.11 schedule arrived | new fields: ' + (', '.join(newf) or 'already there') + ' | view: ' + ', '.join(vstate)
    + ' | automation: ' + NAME + ' | fill: ' + fill + ' | check ' + ' ; '.join(chk), level='info')
