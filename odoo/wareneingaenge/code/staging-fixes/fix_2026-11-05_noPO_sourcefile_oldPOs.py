# IQ Goods Receipts – fix 05.11.2026 (2)
# A) Excel import attaches the source file to every card it creates or updates (+ chatter note)
# B) Card: badge "No PO yet"   C) Form: yellow banner when there is no purchase order
# D) Cards for ALL confirmed purchase orders, incl. completed ones (status + arrival date filled)
# Run once: Scheduled Action (Model: Contact, Active = off) -> Save -> Run Manually -> reload browser.
# Result line: Settings -> Technical -> Logging, search "IQ fix".

View = env['ir.ui.view'].sudo().with_context(lang='en_US')
done = []

# ---------------------------------------------------------------- A) import code
PROCESS = r'''
Line = env['x_wareneingang_line'].sudo()
WE = env['x_wareneingang'].sudo()
PO = env['purchase.order'].sudo()
DE = (env.lang or 'en_US').startswith('de')

def target(h):
    t = (h or '').strip().lower()
    if 'customer style' in t or 'description' in t or 'bezeichnung' in t or 'product' in t or 'artikel' in t:
        return 'x_product_text'
    if 'reference' in t or t.startswith('ref') or 'order' in t or 'auftrag' in t or 'bestell' in t:
        return 'x_supplier_ref'
    if t in ('no', 'no.', 'nr', 'nr.', 'item no.', 'art.-nr.', 'art. nr.') or t.startswith('style'):
        return 'x_style_no'
    if 'shipment' in t or 'versand' in t or 'transport' in t:
        return 'x_shipment'
    if 'qty' in t or 'quantity' in t or 'menge' in t:
        return 'x_qty'
    if 'date' in t or 'datum' in t or 'termin' in t:
        return 'x_date'
    if 'amount' in t or 'betrag' in t or 'wert' in t or 'value' in t:
        return 'x_amount'
    if 'valuta' in t or 'currency' in t or 'währung' in t:
        return 'x_currency'
    return False

def attach_src(we, up, raw, fname, attached, de):
    if not we or we.id in attached:
        return
    attached.append(we.id)
    Att = env['ir.attachment'].sudo()
    if Att.search_count([('res_model', '=', 'x_wareneingang'), ('res_id', '=', we.id), ('name', '=', fname), ('file_size', '=', len(raw))]):
        return
    att = Att.create({'name': fname, 'datas': up.x_file, 'res_model': 'x_wareneingang', 'res_id': we.id})
    we.message_post(body=('Quelle: Lieferübersicht ' if de else 'Source: delivery overview ') + fname + ' (' + (up.x_name or '') + ')', attachment_ids=[att.id])

for up in records:
    if not up.x_file or not up.x_supplier_id:
        raise UserError('Bitte Lieferant wählen und Excel-Datei hochladen.' if DE else 'Please choose a supplier and upload an Excel file.')
    if (up.x_file_name or '').lower().endswith('.pdf'):
        raise UserError('PDF-Dateien werden nicht unterstützt. Bitte Excel (.xlsx/.xls) oder CSV hochladen.' if DE else 'PDF files are not supported. Please upload Excel (.xlsx/.xls) or CSV.')
    sup = up.x_supplier_id
    if not up.x_name:
        up.write({'x_name': sup.name + ' – ' + datetime.date.today().strftime('%d.%m.%Y')})
    fname = up.x_file_name or 'upload.xlsx'
    ftype = 'text/csv' if fname.lower().endswith('.csv') else ('application/vnd.ms-excel' if fname.lower().endswith('.xls') else 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    imp = env['base_import.import'].sudo().create({'res_model': 'x_wareneingang_line', 'file': b64decode(up.x_file),
                                                   'file_name': fname, 'file_type': ftype})
    options = {'has_headers': True, 'advanced': False, 'keep_matches': False, 'name_create_enabled_fields': {},
               'import_set_empty_fields': [], 'import_skip_records': [], 'fallback_values': {}, 'skip': 0, 'limit': 5000,
               'encoding': '', 'separator': '', 'quoting': '"', 'date_format': '', 'datetime_format': '',
               'float_thousand_separator': ',', 'float_decimal_separator': '.'}
    prev = imp.parse_preview(options)
    if prev.get('error'):
        up.write({'x_result': '<div class="alert alert-danger">' + str(prev.get('error')) + '</div>'})
        continue
    options = prev.get('options') or options
    headers = prev.get('headers') or []
    used = []
    fields = []
    for h in headers:
        f = target(h)
        if f and f not in used:
            used.append(f)
            fields.append(f)
        else:
            fields.append(False)
    if 'x_supplier_ref' not in used or 'x_date' not in used:
        up.write({'x_result': '<div class="alert alert-danger">' + ('Spalten für Bestellnummer und Lieferdatum nicht gefunden. Gefundene Spalten: ' if DE else 'Columns for order no. and delivery date not found. Columns found: ') + ', '.join([str(h) for h in headers]) + '</div>'})
        continue
    res = imp.with_context(default_x_partner_id=sup.id).execute_import(fields, headers, options)
    errors = [m for m in (res.get('messages') or []) if m.get('type') == 'error']
    if errors or not res.get('ids'):
        up.write({'x_result': '<div class="alert alert-danger">' + '<br/>'.join([str(m.get('message')) for m in errors]) + '</div>'})
        continue
    new = Line.browse(res['ids'])
    new.write({'x_partner_id': sup.id})
    raw = b64decode(up.x_file)
    attached = []
    created = []
    linked = []
    changed = []
    same = 0
    added = 0
    for l in new:
        ref = (l.x_supplier_ref or '').strip()
        old = Line.search([('id', 'not in', new.ids), ('x_partner_id', '=', sup.id), ('x_supplier_ref', '=', ref),
                           ('x_style_no', '=', l.x_style_no), ('x_shipment', '=', l.x_shipment)], limit=1)
        if old:
            msgs = []
            if old.x_date != l.x_date:
                msgs.append(('Liefertermin ' if DE else 'Delivery date ') + (old.x_date.strftime('%d.%m.%Y') if old.x_date else '–') + ' → ' + (l.x_date.strftime('%d.%m.%Y') if l.x_date else '–'))
            if old.x_qty != l.x_qty:
                msgs.append(('Menge ' if DE else 'Qty ') + str(int(old.x_qty)) + ' → ' + str(int(l.x_qty)))
            if msgs:
                old.write({'x_date': l.x_date, 'x_qty': l.x_qty, 'x_amount': l.x_amount})
                txt = (old.x_product_text or '') + ' ' + (old.x_shipment or '') + ': ' + ', '.join(msgs)
                if old.x_wareneingang_id:
                    old.x_wareneingang_id.message_post(body=('Lieferübersicht aktualisiert – ' if DE else 'Delivery overview updated – ') + txt)
                changed.append(ref + ' – ' + txt)
            else:
                same += 1
            attach_src(old.x_wareneingang_id, up, raw, fname, attached, DE)
            l.unlink()
            continue
        we = WE.search([('x_supplier_ref', '=', ref), '|', ('x_studio_supplier', '=', sup.id),
                        ('x_studio_purchase_order.partner_id', 'child_of', sup.commercial_partner_id.id)], limit=1) if ref else WE
        if not we:
            po = PO.search([('partner_ref', '=', ref), ('partner_id', 'child_of', sup.commercial_partner_id.id)], limit=1) if ref else PO
            if po:
                we = WE.search([('x_studio_purchase_order', '=', po.id)], limit=1)
                if not we:
                    we = WE.create({'x_name': po.name, 'x_studio_purchase_order': po.id, 'x_studio_supplier': po.partner_id.id})
                we.write({'x_supplier_ref': ref})
                linked.append(ref + ' → ' + po.name)
            else:
                we = WE.create({'x_name': ref + ' – ' + (l.x_product_text or ''), 'x_studio_supplier': sup.id, 'x_supplier_ref': ref})
                created.append(we.x_name)
        l.write({'x_wareneingang_id': we.id, 'x_name': ' · '.join([x for x in [ref, l.x_product_text, l.x_shipment] if x])})
        attach_src(we, up, raw, fname, attached, DE)
        added += 1
    h = ['<div class="alert alert-success mb-2">' + ('Datei verarbeitet.' if DE else 'File processed.') + '</div><ul>']
    h.append('<li>' + ('Neue Lieferungen (ohne Bestellung): ' if DE else 'New deliveries (no PO): ') + str(len(created)) + '</li>')
    for c in created:
        h.append('<li class="ms-3">' + c + '</li>')
    h.append('<li>' + ('Mit Bestellung verknüpft: ' if DE else 'Linked to purchase orders: ') + str(len(linked)) + '</li>')
    for c in linked:
        h.append('<li class="ms-3">' + c + '</li>')
    h.append('<li>' + ('Neue Lieferpositionen: ' if DE else 'New shipment lines: ') + str(added) + '</li>')
    h.append('<li>' + ('Geändert: ' if DE else 'Changed: ') + str(len(changed)) + '</li>')
    for c in changed:
        h.append('<li class="ms-3 text-warning">' + c + '</li>')
    h.append('<li>' + ('Unverändert: ' if DE else 'Unchanged: ') + str(same) + '</li>')
    h.append('<li>' + ('Datei an Karten angehängt: ' if DE else 'File attached to cards: ') + str(len(attached)) + '</li></ul>')
    up.write({'x_result': ''.join(h)})
'''
sa = env['ir.actions.server'].sudo().search([('name', '=', 'IQ Lieferübersicht verarbeiten')], limit=1)
if sa:
    sa.write({'code': PROCESS})
    done.append('A import: source file attach ON')
else:
    done.append('A import: server action NOT FOUND')

# ---------------------------------------------------------------- B) kanban badge
kb = View.search([('name', '=', 'IQ Wareneingang Kanban'), ('model', '=', 'x_wareneingang')], limit=1)
BADGE = '<span t-if="!record.x_studio_purchase_order.raw_value" class="badge rounded-pill text-bg-light border border-warning text-warning"><i class="fa fa-file-o me-1"/><span>No PO yet</span></span>\n                        '
ANCHOR = '<span t-if="record.x_qty_defect.raw_value'
if not kb:
    done.append('B kanban NOT FOUND')
elif 'No PO yet' in kb.arch_db:
    done.append('B badge already there')
elif ANCHOR in kb.arch_db:
    kb.write({'arch_db': kb.arch_db.replace(ANCHOR, BADGE + ANCHOR, 1)})
    kb.update_field_translations('arch_db', {'de_DE': {'No PO yet': 'Noch keine Bestellung'}})
    done.append('B badge added')
else:
    done.append('B anchor NOT FOUND')

# ---------------------------------------------------------------- C) form banner
fm = View.search([('name', '=', 'IQ Wareneingang Form'), ('model', '=', 'x_wareneingang'), ('inherit_id', '=', False)], limit=1)
T1 = 'No purchase order yet.'
T2 = "Planned from the supplier's delivery overview or entered by hand. The source file is in the Files tab and in the chatter. As soon as a purchase order with this supplier order no. as Vendor Reference is confirmed, it is linked here automatically."
BANNER = ('<div class="alert alert-warning" role="alert" invisible="x_studio_purchase_order">'
          '<i class="fa fa-info-circle me-1"/><strong>' + T1 + '</strong> <span>' + T2 + '</span></div>\n        ')
FANCHOR = '<div class="alert alert-danger" role="alert" invisible="not x_studio_rejection_reason">'
if not fm:
    done.append('C form NOT FOUND')
elif T1 in fm.arch_db:
    done.append('C banner already there')
elif FANCHOR in fm.arch_db:
    fm.write({'arch_db': fm.arch_db.replace(FANCHOR, BANNER + FANCHOR, 1)})
    fm.update_field_translations('arch_db', {'de_DE': {
        T1: 'Noch keine Bestellung.',
        T2: 'Geplant aus der Lieferübersicht des Lieferanten oder von Hand eingetragen. Die Quelldatei ist im Tab Dateien und im Chatter. Sobald eine Bestellung mit dieser Lieferanten-Bestell-Nr. als Lieferantenreferenz bestätigt wird, wird sie hier automatisch verknüpft.'}})
    done.append('C banner added')
else:
    done.append('C anchor NOT FOUND')

# ---------------------------------------------------------------- D) cards for all confirmed POs
Stage = env['x_wareneingang_stage'].sudo().with_context(lang='en_US')
def sid(names):
    s = Stage.search([('x_name', 'in', names)], limit=1)
    return s.id
EXP = sid(['Expected', 'Erwartet'])
PART = sid(['Partly booked', 'Teilweise gebucht'])
DONE = sid(['Done', 'Fertig'])
if not (EXP and PART and DONE):
    done.append('D stages NOT FOUND')
else:
    WE = env['x_wareneingang'].sudo()
    created = 0
    for po in env['purchase.order'].sudo().search([('state', 'in', ['purchase', 'done'])], order='id asc'):
        if WE.search_count([('x_studio_purchase_order', '=', po.id)]):
            continue
        lines = po.order_line.filtered(lambda l: l.product_qty > 0 and l.product_id and l.product_id.type != 'service')
        booked = sum(lines.mapped('qty_received'))
        if lines and not lines.filtered(lambda l: l.qty_received < l.product_qty):
            st = DONE
        elif booked > 0:
            st = PART
        else:
            st = EXP
        dones = po.picking_ids.filtered(lambda p: p.state == 'done' and p.date_done)
        WE.create({'x_name': po.name, 'x_studio_purchase_order': po.id, 'x_studio_supplier': po.partner_id.id,
                   'x_studio_date': po.date_planned and po.date_planned.date() or False,
                   'x_studio_arrival_date': max(dones.mapped('date_done')).date() if dones else False,
                   'x_supplier_ref': po.partner_ref or False, 'x_studio_stage_id': st, 'x_active': True})
        created += 1
    done.append('D cards created for old POs: %d' % created)

log('IQ fix 05.11. (2): ' + ' | '.join(done))
