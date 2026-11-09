# =====================================================================================
#  IQ Dogsport – "Goods Receipts / Wareneingänge" app – complete install / update script
#  Odoo 19 · run as a Scheduled Action (Model: any, e.g. "Contact"), Active = OFF,
#  then "Run Manually". Safe to run again: creates what is missing, sets views and
#  calculations to the final state, never deletes data.
#  Requires apps: Purchase, Inventory, Quality.
# =====================================================================================

IrModel = env['ir.model'].sudo()
Fields = env['ir.model.fields'].sudo()
View = env['ir.ui.view'].sudo().with_context(lang='en_US')
Act = env['ir.actions.act_window'].sudo()
Menu = env['ir.ui.menu'].sudo()
SA = env['ir.actions.server'].sudo()
Auto = env['base.automation'].sudo()
Acc = env['ir.model.access'].sudo()
Default = env['ir.default'].sudo()
MODEL = 'x_wareneingang'
G_USER = env.ref('base.group_user')
G_SYS = env.ref('base.group_system')

# ---------------------------------------------------------------- helpers
def addf(model, vals):
    f = Fields.search([('model_id', '=', model.id), ('name', '=', vals['name'])], limit=1)
    if f:
        upd = {}
        for k in ['compute', 'depends', 'store', 'readonly', 'sanitize', 'tracking', 'group_expand']:
            if k in vals:
                upd[k] = vals[k]
        if upd:
            f.write(upd)
        return f
    vals.update({'model_id': model.id, 'state': 'manual'})
    return Fields.create(vals)

def label(model_name, fname, en, de_):
    f = Fields.search([('model', '=', model_name), ('name', '=', fname)], limit=1)
    if f:
        f.update_field_translations('field_description', {'en_US': en, 'de_DE': de_})

def access(model, unlink_user=True):
    if not Acc.search([('model_id', '=', model.id)], limit=1):
        Acc.create({'name': model.model + ' user', 'model_id': model.id, 'group_id': G_USER.id,
                    'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': unlink_user})
        Acc.create({'name': model.model + ' admin', 'model_id': model.id, 'group_id': G_SYS.id,
                    'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True})

def view(name, model, vtype, arch, de=None, priority=1):
    v = View.search([('name', '=', name), ('model', '=', model)], limit=1)
    vals = {'name': name, 'model': model, 'type': vtype, 'arch': arch, 'priority': priority}
    if v:
        v.write(vals)
    else:
        v = View.create(vals)
    if de:
        v.update_field_translations('arch_db', {'de_DE': de})
    return v

def action(name_en, name_de, model, mode, extra=None):
    a = Act.search([('res_model', '=', model)], limit=1)
    vals = {'name': name_en, 'res_model': model, 'view_mode': mode}
    if extra:
        vals.update(extra)
    if a:
        a.write(vals)
    else:
        a = Act.create(vals)
    a.update_field_translations('name', {'en_US': name_en, 'de_DE': name_de})
    return a

def menu(name_en, name_de, parent, act, seq, icon=False):
    ref = ('ir.actions.act_window,' + str(act.id)) if act else False
    if act:
        m = Menu.with_context(active_test=False).search([('action', '=', ref)], limit=1)
    else:
        m = Menu.with_context(active_test=False).search([('name', 'in', [name_en, name_de]), ('parent_id', '=', parent.id if parent else False)], limit=1)
    vals = {'name': name_en, 'parent_id': parent.id if parent else False, 'sequence': seq, 'active': True}
    if ref:
        vals['action'] = ref
    if icon:
        vals['web_icon'] = icon
    if m:
        m.write(vals)
    else:
        m = Menu.create(vals)
    m.update_field_translations('name', {'en_US': name_en, 'de_DE': name_de})
    return m

def automation(name, model_name, trigger, code, trigger_fields=None, domain=False):
    m = IrModel.search([('model', '=', model_name)], limit=1)
    a = Auto.search([('name', '=', name)], limit=1)
    if a:
        a.action_server_ids.write({'code': code})
        return a
    vals = {'name': name, 'model_id': m.id, 'trigger': trigger,
            'action_server_ids': [(0, 0, {'name': name, 'model_id': m.id, 'state': 'code',
                                          'usage': 'base_automation', 'code': code})]}
    if trigger_fields:
        vals['trigger_field_ids'] = [(6, 0, Fields.search([('model', '=', model_name), ('name', 'in', trigger_fields)]).ids)]
    if domain:
        vals['filter_domain'] = domain
    return Auto.create(vals)

# German active
de_lang = env['res.lang'].sudo().with_context(active_test=False).search([('code', '=', 'de_DE')], limit=1)
if not de_lang or not de_lang.active:
    raise UserError('German (de_DE) is not active in this database – nothing was changed.')
TRANSLATE = 'standard' if Fields.fields_get(['translate'])['translate']['type'] == 'selection' else True

# =====================================================================================
# 1. Stage model + stages
# =====================================================================================
StM = IrModel.search([('model', '=', 'x_wareneingang_stage')], limit=1)
if not StM:
    StM = IrModel.create({'name': 'Goods Receipt Stages', 'model': 'x_wareneingang_stage', 'state': 'manual',
                          'field_id': [(0, 0, {'name': 'x_name', 'field_description': 'Stage Name', 'ttype': 'char',
                                               'required': True, 'translate': TRANSLATE})]})
addf(StM, {'name': 'x_studio_sequence', 'field_description': 'Sequence', 'ttype': 'integer'})
StM.write({'order': 'x_studio_sequence asc, id asc'})
access(StM, unlink_user=False)
Stage = env['x_wareneingang_stage'].sudo()
S = {}
for key, de_n, en_n, seq in [('exp', 'Erwartet', 'Expected', 10), ('part', 'Teilweise gebucht', 'Partly booked', 20),
                              ('done', 'Fertig', 'Done', 30), ('rej', 'Abgelehnt', 'Rejected', 40)]:
    s = Stage.search(['|', ('x_name', '=', de_n), ('x_name', '=', en_n)], limit=1)
    if not s:
        s = Stage.create({'x_name': en_n, 'x_studio_sequence': seq})
    s.write({'x_studio_sequence': seq})
    if Fields.search([('model', '=', 'x_wareneingang_stage'), ('name', '=', 'x_name')], limit=1).translate:
        s.update_field_translations('x_name', {'en_US': en_n, 'de_DE': de_n})
    S[key] = s.id
EXP, PART, DONE, REJ = S['exp'], S['part'], S['done'], S['rej']

def ids(code):
    return (code.replace('__EXP__', str(EXP)).replace('__PART__', str(PART))
                .replace('__DONE__', str(DONE)).replace('__REJ__', str(REJ)))

# =====================================================================================
# 2. Main model x_wareneingang + stored fields
# =====================================================================================
WE_M = IrModel.search([('model', '=', MODEL)], limit=1)
if not WE_M:
    WE_M = IrModel.create({'name': 'Goods Receipt', 'model': MODEL, 'state': 'manual',
                           'is_mail_thread': True, 'is_mail_activity': True,
                           'field_id': [(0, 0, {'name': 'x_name', 'field_description': 'Delivery', 'ttype': 'char', 'required': True})]})
access(WE_M, unlink_user=False)
addf(WE_M, {'name': 'x_active', 'field_description': 'Active', 'ttype': 'boolean'})
addf(WE_M, {'name': 'x_color', 'field_description': 'Color', 'ttype': 'integer'})
addf(WE_M, {'name': 'x_studio_stage_id', 'field_description': 'Status', 'ttype': 'many2one', 'relation': 'x_wareneingang_stage',
            'on_delete': 'restrict', 'required': True, 'group_expand': True, 'tracking': 1})
addf(WE_M, {'name': 'x_studio_date', 'field_description': 'Expected', 'ttype': 'date', 'tracking': 100})
addf(WE_M, {'name': 'x_studio_notes', 'field_description': 'Notes', 'ttype': 'html'})
addf(WE_M, {'name': 'x_studio_purchase_order', 'field_description': 'Purchase Order', 'ttype': 'many2one',
            'relation': 'purchase.order', 'on_delete': 'set null'})
addf(WE_M, {'name': 'x_studio_supplier', 'field_description': 'Supplier', 'ttype': 'many2one', 'relation': 'res.partner',
            'on_delete': 'set null', 'tracking': 100})
addf(WE_M, {'name': 'x_studio_product', 'field_description': 'Product', 'ttype': 'many2one', 'relation': 'product.template',
            'on_delete': 'set null'})
addf(WE_M, {'name': 'x_studio_arrival_date', 'field_description': 'Arrived', 'ttype': 'date'})
addf(WE_M, {'name': 'x_studio_rejection_reason', 'field_description': 'Rejection reason', 'ttype': 'text'})
addf(WE_M, {'name': 'x_supplier_ref', 'field_description': 'Supplier order no.', 'ttype': 'char'})
addf(WE_M, {'name': 'x_upload_ids', 'field_description': 'New files', 'ttype': 'many2many', 'relation': 'ir.attachment',
            'relation_table': 'x_we_upload_rel', 'column1': 'we_id', 'column2': 'attachment_id'})
if not Default.search([('field_id.model', '=', MODEL), ('field_id.name', '=', 'x_active')], limit=1):
    Default.set(MODEL, 'x_active', True)
Default.set(MODEL, 'x_studio_stage_id', EXP)

# =====================================================================================
# 3. Delivery schedule line + upload models
# =====================================================================================
LineM = IrModel.search([('model', '=', 'x_wareneingang_line')], limit=1)
if not LineM:
    LineM = IrModel.create({'name': 'Delivery schedule line', 'model': 'x_wareneingang_line', 'state': 'manual',
                            'field_id': [(0, 0, {'name': 'x_name', 'field_description': 'Delivery', 'ttype': 'char'})]})
access(LineM)
addf(LineM, {'name': 'x_wareneingang_id', 'field_description': 'Goods receipt', 'ttype': 'many2one', 'relation': MODEL, 'on_delete': 'cascade'})
addf(LineM, {'name': 'x_partner_id', 'field_description': 'Supplier', 'ttype': 'many2one', 'relation': 'res.partner', 'on_delete': 'set null'})
for fn, lab, tt in [('x_supplier_ref', 'Order no.', 'char'), ('x_style_no', 'Style no.', 'char'), ('x_product_text', 'Product', 'char'),
                    ('x_shipment', 'Shipment', 'char'), ('x_qty', 'Qty', 'float'), ('x_date', 'Delivery date', 'date'),
                    ('x_amount', 'Amount', 'float'), ('x_currency', 'Currency', 'char'), ('x_done', 'Arrived', 'boolean')]:
    addf(LineM, {'name': fn, 'field_description': lab, 'ttype': tt})

UpM = IrModel.search([('model', '=', 'x_iq_delivery_upload')], limit=1)
if not UpM:
    UpM = IrModel.create({'name': 'Delivery overview upload', 'model': 'x_iq_delivery_upload', 'state': 'manual',
                          'field_id': [(0, 0, {'name': 'x_name', 'field_description': 'Description', 'ttype': 'char'})]})
access(UpM)
addf(UpM, {'name': 'x_supplier_id', 'field_description': 'Supplier', 'ttype': 'many2one', 'relation': 'res.partner', 'on_delete': 'set null'})
addf(UpM, {'name': 'x_file', 'field_description': 'Excel file', 'ttype': 'binary'})
addf(UpM, {'name': 'x_file_name', 'field_description': 'File name', 'ttype': 'char'})
addf(UpM, {'name': 'x_result', 'field_description': 'Result', 'ttype': 'html'})

addf(WE_M, {'name': 'x_schedule_ids', 'field_description': 'Delivery schedule', 'ttype': 'one2many',
            'relation': 'x_wareneingang_line', 'relation_field': 'x_wareneingang_id'})

# =====================================================================================
# 4. Calculated fields (all read live from PO / receipts / quality)
# =====================================================================================
GOODS = "lambda l: l.product_qty > 0 and l.product_id and l.product_id.type != 'service'"
DEP = 'x_studio_purchase_order'

def calc(name, label_, ttype, code, depends=DEP, extra=None):
    vals = {'name': name, 'field_description': label_, 'ttype': ttype, 'store': False, 'readonly': True,
            'depends': depends, 'compute': code}
    if extra:
        vals.update(extra)
    return addf(WE_M, vals)

calc('x_po_line_ids', 'Order lines', 'many2many',
     "for rec in self:\n    rec['x_po_line_ids'] = rec.x_studio_purchase_order.order_line.filtered(" + GOODS + ")\n",
     extra={'relation': 'purchase.order.line', 'relation_table': 'x_we_po_line_rel', 'column1': 'we_id', 'column2': 'line_id'})
calc('x_receipt_ids', 'Receipts', 'many2many',
     "for rec in self:\n    rec['x_receipt_ids'] = rec.x_studio_purchase_order.picking_ids\n",
     extra={'relation': 'stock.picking', 'relation_table': 'x_we_receipt_rel', 'column1': 'we_id', 'column2': 'picking_id'})
calc('x_quality_check_ids', 'Quality checks', 'many2many',
     "for rec in self:\n"
     "    pickings = rec.x_studio_purchase_order.picking_ids\n"
     "    rec['x_quality_check_ids'] = self.env['quality.check'].search([('picking_id', 'in', pickings.ids)]) if pickings else self.env['quality.check']\n",
     extra={'relation': 'quality.check', 'relation_table': 'x_we_qc_rel', 'column1': 'we_id', 'column2': 'check_id'})
calc('x_quality_alert_ids', 'Quality alerts', 'many2many',
     "for rec in self:\n"
     "    pickings = rec.x_studio_purchase_order.picking_ids\n"
     "    rec['x_quality_alert_ids'] = self.env['quality.alert'].search([('picking_id', 'in', pickings.ids)]) if pickings else self.env['quality.alert']\n",
     extra={'relation': 'quality.alert', 'relation_table': 'x_we_alert_rel', 'column1': 'we_id', 'column2': 'alert_id'})
calc('x_all_attachment_ids', 'Files', 'many2many', r"""
for rec in self:
    po = rec.x_studio_purchase_order
    pickings = po.picking_ids
    checks = self.env['quality.check'].search([('picking_id', 'in', pickings.ids)]) if pickings else self.env['quality.check']
    atts = self.env['ir.attachment'].search([
        '|', '|', '|',
        '&', ('res_model', '=', 'purchase.order'), ('res_id', 'in', po.ids),
        '&', ('res_model', '=', 'stock.picking'), ('res_id', 'in', pickings.ids),
        '&', ('res_model', '=', 'quality.check'), ('res_id', 'in', checks.ids),
        '&', ('res_model', '=', 'x_wareneingang'), ('res_id', 'in', rec.ids),
    ]).sorted(lambda a: a.create_date, reverse=True)
    seen = []
    keep = self.env['ir.attachment']
    for a in atts:
        key = a.checksum or ((a.name or '') + str(a.file_size))
        if key in seen:
            continue
        seen.append(key)
        keep |= a
    rec['x_all_attachment_ids'] = keep
""", extra={'relation': 'ir.attachment', 'relation_table': 'x_we_attachment_rel', 'column1': 'we_id', 'column2': 'attachment_id'})
calc('x_file_count', 'Files', 'integer', "for rec in self:\n    rec['x_file_count'] = len(rec.x_all_attachment_ids)\n")
calc('x_qty_ordered', 'Ordered', 'float',
     "for rec in self:\n"
     "    po = rec.x_studio_purchase_order\n"
     "    rec['x_qty_ordered'] = sum(po.order_line.filtered(" + GOODS + ").mapped('product_qty')) if po else sum(rec.x_schedule_ids.mapped('x_qty'))\n",
     depends='x_studio_purchase_order,x_schedule_ids')
calc('x_qty_booked', 'Booked', 'float',
     "for rec in self:\n"
     "    rec['x_qty_booked'] = sum(rec.x_studio_purchase_order.order_line.filtered(" + GOODS + ").mapped('qty_received'))\n")
calc('x_qty_defect', 'Defective', 'float', r"""
QC = self.env['quality.check']
has_qty = 'qty_failed' in QC.fields_get(['qty_failed'])
for rec in self:
    pickings = rec.x_studio_purchase_order.picking_ids
    fails = QC.search([('picking_id', 'in', pickings.ids), ('quality_state', '=', 'fail')]) if pickings else QC
    rec['x_qty_defect'] = sum([((c.qty_failed or 1) if has_qty else 1) for c in fails])
""")
calc('x_qc_fail_count', 'Failed checks', 'integer',
     "for rec in self:\n    rec['x_qc_fail_count'] = len(rec.x_quality_check_ids.filtered(lambda c: c.quality_state == 'fail'))\n")
calc('x_qty_open', 'Open', 'float', r"""
QC = self.env['quality.check']
has_qty = 'qty_failed' in QC.fields_get(['qty_failed'])
for rec in self:
    po = rec.x_studio_purchase_order
    if not po:
        rec['x_qty_open'] = sum(rec.x_schedule_ids.filtered(lambda l: not l.x_done).mapped('x_qty'))
        continue
    fails = QC.search([('picking_id', 'in', po.picking_ids.ids), ('quality_state', '=', 'fail')]) if po.picking_ids else QC
    dmap = {}
    for c in fails:
        dmap[c.product_id.id] = dmap.get(c.product_id.id, 0) + ((c.qty_failed or 1) if has_qty else 1)
    total = 0
    for l in po.order_line.filtered(lambda l: l.product_qty > 0 and l.product_id and l.product_id.type != 'service'):
        d = dmap.pop(l.product_id.id, 0)
        total += max(l.product_qty - l.qty_received - d, 0)
    rec['x_qty_open'] = total
""", depends='x_studio_purchase_order,x_schedule_ids')
calc('x_product_summary', 'Products', 'char', r"""
SIZES = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', '2XL', '3XL', '4XL', '5XL']
for rec in self:
    lines = rec.x_studio_purchase_order.order_line.filtered(lambda l: l.product_qty > 0 and l.product_id and l.product_id.type != 'service')
    if not lines:
        rec['x_product_summary'] = rec.x_studio_product.display_name or ' · '.join(list(dict.fromkeys([t for t in rec.x_schedule_ids.mapped('x_product_text') if t])))
        continue
    groups = {}
    order = []
    for l in lines:
        t = l.product_id.product_tmpl_id
        if t.id not in groups:
            groups[t.id] = [(t.name or '').split(' – ')[0], []]
            order.append(t.id)
        for v in l.product_id.product_template_attribute_value_ids:
            an = (v.attribute_id.name or '').lower()
            is_size = (v.name or '').upper() in SIZES or 'size' in an or 'größe' in an or 'grösse' in an or 'groesse' in an
            if not is_size and v.name not in groups[t.id][1]:
                groups[t.id][1].append(v.name)
    parts = []
    for k in order:
        cols = groups[k][1]
        parts.append(groups[k][0] + (' (' + ', '.join(cols) + ')' if cols else ''))
    rec['x_product_summary'] = ' · '.join(parts)
""", depends='x_studio_purchase_order,x_studio_product,x_schedule_ids')
calc('x_po_vendor', 'Supplier', 'many2one',
     "for rec in self:\n    rec['x_po_vendor'] = rec.x_studio_purchase_order.partner_id or rec.x_studio_supplier\n",
     depends='x_studio_purchase_order,x_studio_supplier', extra={'relation': 'res.partner'})
calc('x_po_expected', 'Expected', 'date',
     "for rec in self:\n"
     "    po = rec.x_studio_purchase_order\n"
     "    rec['x_po_expected'] = po.date_planned.date() if po and po.date_planned else rec.x_studio_date\n",
     depends='x_studio_purchase_order,x_studio_date')
addf(WE_M, {'name': 'x_next_date', 'field_description': 'Next delivery', 'ttype': 'date', 'store': True, 'readonly': True,
            'depends': 'x_schedule_ids,x_schedule_ids.x_date,x_schedule_ids.x_done,x_studio_purchase_order,x_studio_purchase_order.date_planned,x_studio_date',
            'compute': r"""
for rec in self:
    open_lines = rec.x_schedule_ids.filtered(lambda l: not l.x_done and l.x_date)
    if open_lines:
        rec['x_next_date'] = min(open_lines.mapped('x_date'))
    elif rec.x_studio_purchase_order and rec.x_studio_purchase_order.date_planned:
        rec['x_next_date'] = rec.x_studio_purchase_order.date_planned.date()
    else:
        rec['x_next_date'] = rec.x_studio_date
"""})
calc('x_due_state', 'Due state', 'char', ids(r"""
today = datetime.date.today()
for rec in self:
    d = rec.x_next_date
    if not d or rec.x_studio_stage_id.id in (__DONE__, __REJ__):
        rec['x_due_state'] = ''
    elif d < today:
        rec['x_due_state'] = 'overdue'
    elif (d - today).days <= 7:
        rec['x_due_state'] = 'soon'
    else:
        rec['x_due_state'] = ''
"""), depends='x_next_date,x_studio_stage_id')
calc('x_next_info', 'Next shipment', 'char', r"""
de = (self.env.lang or 'en_US').startswith('de')
for rec in self:
    lines = rec.x_schedule_ids.filtered(lambda l: not l.x_done and l.x_date).sorted(lambda l: l.x_date)
    if not lines:
        rec['x_next_info'] = ''
        continue
    f = lines[0]
    s = f.x_date.strftime('%d.%m.%Y')
    if f.x_shipment:
        s += ' · ' + f.x_shipment
    s += ' · ' + str(int(f.x_qty)) + (' Stk.' if de else ' pcs.')
    if len(lines) > 1:
        s += (' · +%d weitere' if de else ' · +%d more') % (len(lines) - 1)
    rec['x_next_info'] = s
""", depends='x_schedule_ids')
calc('x_parts_info', 'Kit parts', 'char', r"""
de = (self.env.lang or 'en_US').startswith('de')
for rec in self:
    po = rec.x_studio_purchase_order
    txt = ''
    if po:
        mv = self.env['stock.move'].search([('purchase_line_id', 'in', po.order_line.ids), ('state', '!=', 'cancel')])
        parts = mv.filtered(lambda m: m.product_id != m.purchase_line_id.product_id)
        if parts:
            done = sum(parts.filtered(lambda m: m.state == 'done').mapped('quantity'))
            total = sum(parts.mapped('product_uom_qty'))
            txt = ('Teile ' if de else 'Parts ') + str(int(done)) + ' / ' + str(int(total))
    rec['x_parts_info'] = txt
""")
calc('x_product_matrix_html', 'Size table', 'html', r"""
SIZES = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', '2XL', '3XL', '4XL', '5XL']
de = (self.env.lang or 'en_US').startswith('de')
T = {
    'nopo': 'Noch keine Bestellung – Mengen siehe Tab Lieferplan.' if de else 'No purchase order yet – see the Delivery schedule tab.',
    'nolines': 'Keine Positionen in der Bestellung.' if de else 'No lines on the purchase order.',
    'product': 'Produkt' if de else 'Product',
    'colour': 'Farbe' if de else 'Colour',
    'total': 'Gesamt' if de else 'Total',
    'foot': 'Gesamt gebucht / bestellt' if de else 'Total booked / ordered',
    'defect': 'defekt' if de else 'defective',
    'parts': 'Teile ' if de else 'parts ',
    'open_product': 'Produkt öffnen' if de else 'Open product',
    'show': 'Buchungen anzeigen' if de else 'Show bookings',
    'legend': ('Gebucht / Bestellt · grün = vollständig · orange = teilweise · grau = noch nichts gebucht · rot = defekt · Klick auf ein Feld zeigt die Buchungen'
               if de else 'Booked / Ordered · green = complete · orange = partly · grey = nothing booked yet · red = defective · click a box to see the bookings'),
}
esc = lambda s: (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
css = lambda o, b: 'table-success' if b >= o else ('table-warning' if b > 0 else 'text-muted')
QC = self.env['quality.check']
has_qty = 'qty_failed' in QC.fields_get(['qty_failed'])
act = self.env['ir.actions.act_window'].search([('res_model', '=', 'stock.move'), ('domain', '=', "[('purchase_line_id', '=', active_id)]")], limit=1)
for rec in self:
    po = rec.x_studio_purchase_order
    if not po:
        rec['x_product_matrix_html'] = '<div class="alert alert-warning mb-0">' + T['nopo'] + '</div>'
        continue
    lines = po.order_line.filtered(lambda l: l.product_qty > 0 and l.product_id and l.product_id.type != 'service')
    if not lines:
        rec['x_product_matrix_html'] = '<div class="text-muted">' + T['nolines'] + '</div>'
        continue
    fails = QC.search([('picking_id', 'in', po.picking_ids.ids), ('quality_state', '=', 'fail')]) if po.picking_ids else QC
    dmap = {}
    for c in fails:
        dmap[c.product_id.id] = dmap.get(c.product_id.id, 0) + ((c.qty_failed or 1) if has_qty else 1)
    mv = self.env['stock.move'].search([('purchase_line_id', 'in', lines.ids), ('state', '!=', 'cancel')])
    kit = {}
    for m in mv:
        if m.product_id != m.purchase_line_id.product_id:
            k = kit.get(m.purchase_line_id.id, [0, 0])
            kit[m.purchase_line_id.id] = [k[0] + m.product_uom_qty, k[1] + (m.quantity if m.state == 'done' else 0)]
    rows = {}
    order = []
    sizes = []
    for l in lines:
        size = '–'
        cols = []
        for v in l.product_id.product_template_attribute_value_ids:
            an = (v.attribute_id.name or '').lower()
            if (v.name or '').upper() in SIZES or 'size' in an or 'größe' in an or 'grösse' in an or 'groesse' in an:
                size = v.name
            else:
                cols.append(v.name)
        tmpl = l.product_id.product_tmpl_id
        key = str(tmpl.id) + '|' + ', '.join(cols)
        if key not in rows:
            rows[key] = {'name': (tmpl.name or '').split(' – ')[0], 'tmpl': tmpl.id, 'colour': ', '.join(cols), 'cells': {}}
            order.append(key)
        if size not in sizes:
            sizes.append(size)
        kp = kit.get(l.id, [0, 0])
        cell = rows[key]['cells'].get(size, [0, 0, l.id, 0, 0, 0])
        rows[key]['cells'][size] = [cell[0] + l.product_qty, cell[1] + l.qty_received, cell[2], cell[3] + dmap.pop(l.product_id.id, 0), cell[4] + kp[0], cell[5] + kp[1]]
    sizes = sorted(sizes, key=lambda s: SIZES.index(s.upper()) if s.upper() in SIZES else 99)
    h = ['<div class="table-responsive"><table style="min-width:760px;" class="table table-sm table-bordered align-middle text-center mb-0 small">']
    h.append('<thead class="table-light"><tr><th class="text-start">' + T['product'] + '</th><th class="text-start">' + T['colour'] + '</th>')
    for s in sizes:
        h.append('<th>' + esc(s) + '</th>')
    h.append('<th>' + T['total'] + '</th></tr></thead><tbody>')
    tot_o = 0
    tot_b = 0
    tot_d = 0
    for k in order:
        r = rows[k]
        ro = 0
        rb = 0
        rd = 0
        purl = '/web#model=product.template&id=' + str(r['tmpl']) + '&view_type=form'
        h.append('<tr><td class="text-start fw-bold"><a href="' + purl + '" target="_blank" class="text-reset" title="' + T['open_product'] + '">' + esc(r['name']) + '</a></td><td class="text-start">' + esc(r['colour']) + '</td>')
        for s in sizes:
            c = r['cells'].get(s)
            if c:
                ro += c[0]
                rb += c[1]
                rd += c[3]
                dhtml = ('<div class="text-danger fw-bold" style="font-size:11px;">' + str(int(c[3])) + ' ' + T['defect'] + '</div>') if c[3] else ''
                phtml = ('<div class="text-muted" style="font-size:11px;">' + T['parts'] + str(int(c[5])) + ' / ' + str(int(c[4])) + '</div>') if c[4] else ''
                inner = str(int(c[1])) + ' / ' + str(int(c[0])) + phtml + dhtml
                cls = 'table-warning' if (c[5] and c[1] < c[0]) else css(c[0], c[1])
                if act:
                    url = '/web#action=' + str(act.id) + '&active_id=' + str(c[2]) + '&view_type=list'
                    h.append('<td class="p-0 ' + cls + '"><a href="' + url + '" target="_blank" title="' + T['show'] + '" class="d-block py-2 text-reset text-decoration-none" style="cursor:pointer;">' + inner + '</a></td>')
                else:
                    h.append('<td class="' + cls + '">' + inner + '</td>')
            else:
                h.append('<td class="text-muted">·</td>')
        tot_o += ro
        tot_b += rb
        tot_d += rd
        dtot = ('<div class="text-danger" style="font-size:11px;">' + str(int(rd)) + ' ' + T['defect'] + '</div>') if rd else ''
        h.append('<td class="fw-bold ' + css(ro, rb) + '">' + str(int(rb)) + ' / ' + str(int(ro)) + dtot + '</td></tr>')
    dfoot = (' · <span class="text-danger">' + str(int(tot_d)) + ' ' + T['defect'] + '</span>') if tot_d else ''
    h.append('</tbody><tfoot><tr class="fw-bold"><td class="text-start" colspan="' + str(len(sizes) + 2) + '">' + T['foot'] + '</td><td>' + str(int(tot_b)) + ' / ' + str(int(tot_o)) + dfoot + '</td></tr></tfoot></table></div>')
    h.append('<div class="small text-muted mt-1">' + T['legend'] + '</div>')
    rec['x_product_matrix_html'] = ''.join(h)
""", extra={'sanitize': False})
calc('x_files_gallery_html', 'Preview', 'html', r"""
de = (self.env.lang or 'en_US').startswith('de')
esc = lambda s: (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
SRC = {'purchase.order': 'Bestellung' if de else 'Purchase order',
       'stock.picking': 'Wareneingang' if de else 'Receipt',
       'quality.check': 'QC',
       'x_wareneingang': 'Hier hochgeladen' if de else 'Uploaded here'}
L_OPEN = 'Öffnen' if de else 'Open'
L_DL = 'Herunterladen' if de else 'Download'
for rec in self:
    atts = rec.x_all_attachment_ids.sorted(lambda a: a.create_date, reverse=True)
    if not atts:
        rec['x_files_gallery_html'] = '<div class="text-muted">' + ('Noch keine Dateien.' if de else 'No files yet.') + '</div>'
        continue
    cards = []
    for a in atts:
        name = esc(a.name)
        url = '/web/content/' + str(a.id)
        mt = a.mimetype or ''
        if mt.startswith('image/'):
            prev = '<a href="' + url + '" target="_blank"><img src="/web/image/' + str(a.id) + '/600x450" class="rounded border" style="width:100%;height:220px;object-fit:cover;" loading="lazy"/></a>'
        elif mt == 'application/pdf':
            prev = '<iframe src="' + url + '#view=FitH" style="width:100%;height:220px;border:1px solid #dee2e6;border-radius:6px;" loading="lazy"></iframe>'
        else:
            prev = '<div class="d-flex align-items-center justify-content-center bg-light rounded border" style="height:220px;"><i class="fa fa-file-o fa-3x text-muted"></i></div>'
        cards.append(
            '<div class="col-12 col-md-6 col-xl-4"><div class="border rounded p-2 h-100">' + prev +
            '<div class="small mt-2 text-truncate fw-bold" title="' + name + '">' + name + '</div>' +
            '<div class="d-flex justify-content-between align-items-center small mt-1">' +
            '<span class="badge text-bg-light border">' + SRC.get(a.res_model, '') + '</span>' +
            '<span class="text-nowrap"><a href="' + url + '" target="_blank">' + L_OPEN + '</a> · <a href="' + url + '?download=true">' + L_DL + '</a></span>' +
            '</div></div></div>')
    rec['x_files_gallery_html'] = '<div class="row g-3">' + ''.join(cards) + '</div>'
""", extra={'sanitize': False})

# =====================================================================================
# 5. Bookings action (opened from the size table)
# =====================================================================================
bk = Act.search([('res_model', '=', 'stock.move'), ('domain', '=', "[('purchase_line_id', '=', active_id)]")], limit=1)
if not bk:
    bk = Act.create({'name': 'Bookings', 'res_model': 'stock.move', 'view_mode': 'list,form',
                     'domain': "[('purchase_line_id', '=', active_id)]", 'context': "{'create': False}"})
bk.update_field_translations('name', {'en_US': 'Bookings', 'de_DE': 'Buchungen'})

# =====================================================================================
# 6. Views – goods receipt
# =====================================================================================
FORM_DE = {
    'Goods Receipt': 'Wareneingang', 'Goods receipt': 'Wareneingang',
    'e.g. P00053 – MFJ 4.0 Women grey': 'z.B. P00053 – MFJ 4.0 Damen grau',
    'Ordered': 'Bestellt', 'Booked': 'Gebucht', 'Open': 'Offen', 'Defective': 'Defekt', 'Files': 'Dateien',
    'Rejected:': 'Abgelehnt:', 'Delivery': 'Lieferung', 'Dates': 'Termine',
    'Purchase Order': 'Bestellung', 'Supplier': 'Lieferant', 'Product': 'Produkt', 'Supplier order no.': 'Lieferanten-Bestell-Nr.',
    'Expected': 'Erwartet', 'Arrived': 'Angekommen', 'Next delivery': 'Nächste Lieferung',
    'Overview': 'Übersicht', 'Sizes and quantities': 'Größen und Mengen', 'Delivery schedule': 'Lieferplan',
    'Delivery date': 'Liefertermin', 'Order no.': 'Bestell-Nr.', 'Style no.': 'Artikel-Nr.', 'Shipment': 'Versand',
    'Qty': 'Menge', 'Amount': 'Betrag', 'Currency': 'Währung', 'Total': 'Summe',
    'Upload delivery note, photos, count sheet or QC report. They appear in the preview after saving.':
        'Lieferschein, Fotos, Zählliste oder QC-Bericht hochladen. Erscheinen nach dem Speichern in der Vorschau.',
    'Defects': 'Defekte',
    'Defective pieces come from failed quality checks (button Fail on the check). For photos and the reason use Create Alert on the check.':
        'Defekte Stück kommen aus fehlgeschlagenen Qualitätsprüfungen (Button Fail in der Prüfung). Für Fotos und Grund: Create Alert in der Prüfung.',
    'Reference': 'Referenz', 'Title': 'Titel', 'Reason': 'Grund', 'Created on': 'Erstellt am', 'Status': 'Status',
    'Notes and rejection': 'Notizen und Ablehnung', 'Rejection reason': 'Ablehnungsgrund',
    'Reason, if the delivery was rejected': 'Grund, falls die Lieferung abgelehnt wurde',
    'Notes, e.g. quantities for deliveries without a purchase order': 'Notizen, z.B. Mengen bei Lieferungen ohne Bestellung',
    'Order lines': 'Bestellpositionen', 'Receipts': 'Wareneingänge', 'Planned': 'Geplant', 'Booked on': 'Gebucht am',
    'No purchase order yet.': 'Noch keine Bestellung.',
    "Planned from the supplier's delivery overview or entered by hand. The source file is in the Files tab and in the chatter. As soon as a purchase order with this supplier order no. as Vendor Reference is confirmed, it is linked here automatically.":
        'Geplant aus der Lieferübersicht des Lieferanten oder von Hand eingetragen. Die Quelldatei ist im Tab Dateien und im Chatter. Sobald eine Bestellung mit dieser Lieferanten-Bestell-Nr. als Lieferantenreferenz bestätigt wird, wird sie hier automatisch verknüpft.',
    'Quality': 'Qualität', 'Check': 'Prüfung', 'Receipt': 'Wareneingang', 'Checked on': 'Geprüft am', 'Checked by': 'Geprüft von',
}
# remove helper inherit views from staging builds (final form contains everything)
View.search([('model', '=', MODEL), ('inherit_id', '!=', False), ('name', 'like', 'IQ Wareneingang Form')]).unlink()
we_form = view('IQ Wareneingang Form', MODEL, 'form', r'''
<form string="Goods Receipt">
    <header>
        <field name="x_studio_stage_id" widget="statusbar" options="{'clickable': '1'}"/>
    </header>
    <sheet>
        <div class="oe_title">
            <div class="text-muted text-uppercase small">Goods receipt</div>
            <h1><field name="x_name" placeholder="e.g. P00053 – MFJ 4.0 Women grey"/></h1>
            <div class="text-muted" invisible="not x_product_summary">
                <i class="fa fa-cube me-1"/><field name="x_product_summary" readonly="1"/>
            </div>
        </div>
        <div class="row row-cols-2 row-cols-md-5 g-2 my-3">
            <div class="col"><div class="border rounded p-2 text-center h-100">
                <div class="text-muted small">Ordered</div>
                <div class="fs-4 fw-bold"><field name="x_qty_ordered" digits="[16,0]"/></div>
            </div></div>
            <div class="col"><div class="border rounded p-2 text-center h-100">
                <div class="text-muted small">Booked</div>
                <div class="fs-4 fw-bold text-success"><field name="x_qty_booked" digits="[16,0]"/></div>
            </div></div>
            <div class="col"><div class="border rounded p-2 text-center h-100">
                <div class="text-muted small">Open</div>
                <div class="fs-4 fw-bold text-warning"><field name="x_qty_open" digits="[16,0]"/></div>
            </div></div>
            <div class="col"><div class="border rounded p-2 text-center h-100">
                <div class="text-muted small">Defective</div>
                <div class="fs-4 fw-bold text-danger"><field name="x_qty_defect" digits="[16,0]"/></div>
            </div></div>
            <div class="col"><div class="border rounded p-2 text-center h-100">
                <div class="text-muted small">Files</div>
                <div class="fs-4 fw-bold"><field name="x_file_count"/></div>
            </div></div>
        </div>
        <div class="alert alert-warning" role="alert" invisible="x_studio_purchase_order">
            <i class="fa fa-info-circle me-1"/><strong>No purchase order yet.</strong>
            <span>Planned from the supplier's delivery overview or entered by hand. The source file is in the Files tab and in the chatter. As soon as a purchase order with this supplier order no. as Vendor Reference is confirmed, it is linked here automatically.</span>
        </div>
        <div class="alert alert-danger" role="alert" invisible="not x_studio_rejection_reason">
            <strong>Rejected:</strong> <field name="x_studio_rejection_reason" readonly="1" nolabel="1"/>
        </div>
        <group>
            <group string="Delivery">
                <field name="x_studio_purchase_order" string="Purchase Order"/>
                <field name="x_supplier_ref" string="Supplier order no."/>
                <field name="x_po_vendor" string="Supplier" invisible="not x_studio_purchase_order"/>
                <field name="x_studio_supplier" string="Supplier" invisible="x_studio_purchase_order"/>
                <field name="x_studio_product" string="Product" invisible="x_studio_purchase_order"/>
            </group>
            <group string="Dates">
                <field name="x_po_expected" string="Expected" invisible="not x_studio_purchase_order"/>
                <field name="x_studio_date" string="Expected" invisible="x_studio_purchase_order"/>
                <field name="x_studio_arrival_date" string="Arrived"/>
                <field name="x_next_date" string="Next delivery"/>
            </group>
        </group>
        <notebook>
            <page string="Overview" name="overview">
                <h5 class="mt-2 mb-2">Sizes and quantities</h5>
                <field name="x_product_matrix_html" nolabel="1" readonly="1"/>
            </page>
            <page string="Delivery schedule" name="schedule">
                <field name="x_schedule_ids" nolabel="1">
                    <list editable="bottom" decoration-danger="not x_done and x_date and x_date &lt; current_date" decoration-muted="x_done">
                        <field name="x_date" string="Delivery date"/>
                        <field name="x_supplier_ref" string="Order no."/>
                        <field name="x_style_no" string="Style no."/>
                        <field name="x_product_text" string="Product"/>
                        <field name="x_shipment" string="Shipment"/>
                        <field name="x_qty" string="Qty" digits="[16,0]" sum="Total"/>
                        <field name="x_done" string="Arrived" widget="boolean_toggle"/>
                    </list>
                </field>
            </page>
            <page string="Files" name="files">
                <div class="d-flex flex-wrap align-items-center gap-3 mt-2 mb-3">
                    <field name="x_upload_ids" widget="many2many_binary" nolabel="1"/>
                    <span class="text-muted small">Upload delivery note, photos, count sheet or QC report. They appear in the preview after saving.</span>
                </div>
                <field name="x_files_gallery_html" nolabel="1" readonly="1"/>
            </page>
            <page string="Defects" name="defects">
                <div class="text-muted small mt-2 mb-2">Defective pieces come from failed quality checks (button Fail on the check). For photos and the reason use Create Alert on the check.</div>
                <field name="x_quality_alert_ids" nolabel="1" readonly="1">
                    <list create="0" delete="0">
                        <field name="name" string="Reference"/>
                        <field name="title" string="Title"/>
                        <field name="product_id" string="Product"/>
                        <field name="reason_id" string="Reason"/>
                        <field name="create_date" string="Created on"/>
                        <field name="stage_id" string="Status"/>
                    </list>
                </field>
            </page>
            <page string="Notes and rejection" name="notes">
                <group>
                    <field name="x_studio_rejection_reason" string="Rejection reason" placeholder="Reason, if the delivery was rejected"/>
                </group>
                <field name="x_studio_notes" placeholder="Notes, e.g. quantities for deliveries without a purchase order"/>
            </page>
            <page string="Order lines" name="products">
                <field name="x_po_line_ids" nolabel="1" readonly="1">
                    <list create="0" delete="0" limit="200"
                          decoration-success="qty_received &gt;= product_qty"
                          decoration-warning="qty_received &gt; 0 and qty_received &lt; product_qty"
                          decoration-muted="qty_received == 0">
                        <field name="product_id" string="Product"/>
                        <field name="product_qty" string="Ordered" digits="[16,0]"/>
                        <field name="qty_received" string="Booked" digits="[16,0]"/>
                    </list>
                </field>
            </page>
            <page string="Receipts" name="receipts">
                <field name="x_receipt_ids" nolabel="1" readonly="1">
                    <list create="0" delete="0">
                        <field name="name" string="Reference"/>
                        <field name="scheduled_date" string="Planned"/>
                        <field name="date_done" string="Booked on"/>
                        <field name="state" widget="badge"
                               decoration-success="state == 'done'"
                               decoration-info="state == 'assigned'"
                               decoration-muted="state == 'cancel'"/>
                    </list>
                </field>
            </page>
            <page string="Quality" name="quality">
                <field name="x_quality_check_ids" nolabel="1" readonly="1">
                    <list create="0" delete="0" limit="200">
                        <field name="name" string="Check"/>
                        <field name="product_id" string="Product"/>
                        <field name="picking_id" string="Receipt"/>
                        <field name="control_date" string="Checked on"/>
                        <field name="user_id" string="Checked by"/>
                        <field name="quality_state" widget="badge"
                               decoration-success="quality_state == 'pass'"
                               decoration-danger="quality_state == 'fail'"/>
                    </list>
                </field>
            </page>
        </notebook>
    </sheet>
    <chatter/>
</form>''', FORM_DE)

we_kanban = view('IQ Wareneingang Kanban', MODEL, 'kanban', ids(r'''
<kanban default_group_by="x_studio_stage_id" default_order="write_date desc, id desc" quick_create="false">
    <field name="x_name"/><field name="x_studio_stage_id"/><field name="x_po_vendor"/>
    <field name="x_product_summary"/><field name="x_studio_purchase_order"/>
    <field name="x_next_date"/><field name="x_studio_arrival_date"/>
    <field name="x_qty_ordered"/><field name="x_qty_booked"/><field name="x_qty_open"/><field name="x_qty_defect"/>
    <field name="x_due_state"/><field name="x_next_info"/><field name="x_parts_info"/>
    <field name="x_file_count"/><field name="x_studio_rejection_reason"/>
    <templates>
        <t t-name="card">
            <t t-set="ordered" t-value="record.x_qty_ordered.raw_value or 0"/>
            <t t-set="booked" t-value="record.x_qty_booked.raw_value or 0"/>
            <t t-set="pct" t-value="ordered ? (booked gte ordered ? 100 : booked * 100 / ordered) : 0"/>
            <t t-set="rejected" t-value="record.x_studio_stage_id.raw_value == __REJ__"/>
            <div t-attf-style="border-left: 4px solid {{ (rejected || record.x_due_state.raw_value == 'overdue') ? '#dc3545' : (pct == 100 ? '#198754' : (record.x_due_state.raw_value == 'soon' ? '#fd7e14' : '#0d6efd')) }}; padding-left: 10px; margin-left: -4px;">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="overflow-hidden">
                        <div class="text-muted text-uppercase" style="font-size:11px; letter-spacing:.05em;">Order</div>
                        <field name="x_name" class="fw-bold fs-5"/>
                        <div class="text-muted small"><field name="x_po_vendor"/></div>
                    </div>
                    <div class="d-flex flex-column align-items-end gap-1">
                        <span t-if="rejected" class="badge rounded-pill text-bg-danger">Rejected</span>
                        <span t-elif="pct == 100" class="badge rounded-pill text-bg-success">Fully booked</span>
                        <span t-elif="booked gt 0" class="badge rounded-pill text-bg-warning">Partly booked</span>
                        <span t-else="" class="badge rounded-pill text-bg-secondary">Expected</span>
                        <span t-if="record.x_due_state.raw_value == 'overdue'" class="badge rounded-pill text-bg-danger"><i class="fa fa-clock-o me-1"/><span>Overdue</span></span>
                        <span t-if="record.x_due_state.raw_value == 'soon'" class="badge rounded-pill text-bg-warning"><i class="fa fa-clock-o me-1"/><span>This week</span></span>
                        <span t-if="!record.x_studio_purchase_order.raw_value" class="badge rounded-pill text-bg-light border border-warning text-warning"><i class="fa fa-file-o me-1"/><span>No PO yet</span></span>
                        <span t-if="record.x_qty_defect.raw_value gt 0" class="badge rounded-pill text-bg-danger">
                            <i class="fa fa-exclamation-triangle me-1"/><t t-esc="Math.round(record.x_qty_defect.raw_value)"/> <span>defective</span>
                        </span>
                    </div>
                </div>
                <div t-if="record.x_product_summary.raw_value" class="mt-2 small text-truncate" t-att-title="record.x_product_summary.raw_value">
                    <i class="fa fa-cube me-1 text-muted"/><t t-esc="record.x_product_summary.raw_value"/>
                </div>
                <div t-if="record.x_next_info.raw_value" class="small mt-1"><i class="fa fa-truck me-1 text-muted"/><t t-esc="record.x_next_info.raw_value"/></div>
                <div class="row mt-2 small">
                    <div class="col-6">
                        <div class="text-muted text-uppercase" style="font-size:11px;">Next delivery</div>
                        <field name="x_next_date"/>
                    </div>
                    <div class="col-6">
                        <div class="text-muted text-uppercase" style="font-size:11px;">Arrived</div>
                        <field name="x_studio_arrival_date"/>
                        <span t-if="!record.x_studio_arrival_date.raw_value" class="text-muted">–</span>
                    </div>
                </div>
                <div t-if="ordered" class="mt-3">
                    <div class="d-flex justify-content-between small">
                        <span class="text-muted">Booked</span>
                        <span><strong t-esc="Math.round(booked)"/> / <t t-esc="Math.round(ordered)"/> <span>pcs.</span> (<t t-esc="pct.toFixed(0)"/>%)</span>
                    </div>
                    <div class="progress mt-1" style="height:6px;">
                        <div t-attf-class="progress-bar {{ pct == 100 ? 'bg-success' : 'bg-primary' }}" t-attf-style="width: {{ pct }}%;"/>
                    </div>
                    <div t-if="record.x_parts_info.raw_value" class="small text-muted mt-1"><i class="fa fa-puzzle-piece me-1"/><t t-esc="record.x_parts_info.raw_value"/></div>
                    <div t-if="record.x_qty_open.raw_value gt 0" class="small text-warning mt-1">
                        <span>Open:</span> <t t-esc="Math.round(record.x_qty_open.raw_value)"/> <span>pcs.</span>
                    </div>
                </div>
                <div t-if="rejected and record.x_studio_rejection_reason.raw_value" class="alert alert-danger py-1 px-2 mt-2 mb-0 small">
                    <strong>Reason:</strong> <t t-esc="record.x_studio_rejection_reason.raw_value"/>
                </div>
                <div class="d-flex justify-content-between align-items-center mt-3 pt-2 border-top small text-muted">
                    <span><i class="fa fa-paperclip me-1"/><t t-esc="record.x_file_count.raw_value"/> <span>Files</span></span>
                    <span t-if="record.x_studio_purchase_order.raw_value"><i class="fa fa-file-text-o me-1"/><field name="x_studio_purchase_order"/></span>
                    <span t-else="" class="text-warning">Without PO</span>
                </div>
            </div>
        </t>
    </templates>
</kanban>'''), {
    'Order': 'Bestellung', 'Rejected': 'Abgelehnt', 'Fully booked': 'Vollständig gebucht',
    'Partly booked': 'Teilweise gebucht', 'Expected': 'Erwartet', 'defective': 'defekt',
    'Arrived': 'Angekommen', 'Booked': 'Gebucht', 'pcs.': 'Stk.', 'Open:': 'Offen:',
    'Reason:': 'Grund:', 'Files': 'Dateien', 'Without PO': 'Ohne Bestellung',
    'Overdue': 'Überfällig', 'This week': 'Diese Woche', 'Next delivery': 'Nächste Lieferung',
    'No PO yet': 'Noch keine Bestellung'})

we_list = view('IQ Wareneingang List', MODEL, 'list', r'''
<list default_order="write_date desc, id desc">
    <field name="x_name" string="Delivery"/>
    <field name="x_studio_purchase_order" string="Purchase Order"/>
    <field name="x_po_vendor" string="Supplier"/>
    <field name="x_product_summary" string="Products"/>
    <field name="x_supplier_ref" string="Supplier order no."/>
    <field name="x_next_date" string="Next delivery"/>
    <field name="x_studio_arrival_date" string="Arrived"/>
    <field name="x_qty_ordered" string="Ordered" digits="[16,0]"/>
    <field name="x_qty_booked" string="Booked" digits="[16,0]"/>
    <field name="x_qty_open" string="Open" digits="[16,0]"/>
    <field name="x_qty_defect" string="Defective" digits="[16,0]"/>
    <field name="x_file_count" string="Files"/>
    <field name="x_studio_stage_id" string="Status" widget="badge"/>
</list>''', {
    'Delivery': 'Lieferung', 'Purchase Order': 'Bestellung', 'Supplier': 'Lieferant', 'Products': 'Produkte',
    'Supplier order no.': 'Lieferanten-Bestell-Nr.', 'Next delivery': 'Nächste Lieferung', 'Arrived': 'Angekommen',
    'Ordered': 'Bestellt', 'Booked': 'Gebucht', 'Open': 'Offen', 'Defective': 'Defekt', 'Files': 'Dateien', 'Status': 'Status'})

we_search = view('IQ Wareneingang Search', MODEL, 'search', ids(r'''
<search>
    <field name="x_name"/>
    <field name="x_studio_purchase_order"/>
    <field name="x_studio_supplier"/>
    <field name="x_studio_product"/>
    <field name="x_supplier_ref"/>
    <filter name="open" string="Open" domain="[('x_studio_stage_id', 'not in', [__DONE__, __REJ__])]"/>
    <filter name="overdue" string="Overdue" domain="[('x_next_date', '&lt;', context_today().strftime('%Y-%m-%d')), ('x_studio_stage_id', 'not in', [__DONE__, __REJ__])]"/>
    <filter name="this_week" string="This week" domain="[('x_next_date', '&gt;=', context_today().strftime('%Y-%m-%d')), ('x_next_date', '&lt;=', (context_today() + relativedelta(days=7)).strftime('%Y-%m-%d')), ('x_studio_stage_id', 'not in', [__DONE__, __REJ__])]"/>
    <filter name="rejected" string="Rejected" domain="[('x_studio_stage_id', '=', __REJ__)]"/>
    <filter name="no_po" string="Without PO" domain="[('x_studio_purchase_order', '=', False)]"/>
    <separator/>
    <filter name="g_supplier" string="Supplier" context="{'group_by': 'x_studio_supplier'}"/>
    <filter name="g_stage" string="Status" context="{'group_by': 'x_studio_stage_id'}"/>
</search>'''), {
    'Open': 'Offen', 'Overdue': 'Überfällig', 'This week': 'Diese Woche', 'Rejected': 'Abgelehnt',
    'Without PO': 'Ohne Bestellung', 'Supplier': 'Lieferant', 'Status': 'Status'})

we_cal = view('IQ Wareneingang Calendar', MODEL, 'calendar', r'''
<calendar string="Goods Receipts" date_start="x_next_date" color="x_studio_stage_id" mode="month" quick_create="0">
    <field name="x_po_vendor"/><field name="x_product_summary"/>
</calendar>''', {'Goods Receipts': 'Wareneingänge'})

# =====================================================================================
# 7. Views – delivery schedule lines + upload + stages
# =====================================================================================
LINE_DE = {'Delivery date': 'Liefertermin', 'Goods receipt': 'Wareneingang', 'Supplier': 'Lieferant', 'Order no.': 'Bestell-Nr.',
           'Style no.': 'Artikel-Nr.', 'Product': 'Produkt', 'Shipment': 'Versand', 'Qty': 'Menge', 'Arrived': 'Angekommen',
           'Total': 'Summe', 'Delivery calendar': 'Lieferkalender', 'Delivery': 'Lieferung',
           'e.g. Rail, Sea, Truck': 'z.B. Bahn, See, LKW',
           'Leave empty – it is assigned automatically': 'Leer lassen – wird automatisch zugeordnet',
           'Not arrived': 'Nicht angekommen', 'Overdue': 'Überfällig', 'Next 30 days': 'Nächste 30 Tage', 'Month': 'Monat'}
line_list = view('IQ Delivery Line List', 'x_wareneingang_line', 'list', r'''
<list editable="bottom" default_order="x_date asc" decoration-danger="not x_done and x_date and x_date &lt; current_date" decoration-muted="x_done">
    <field name="x_date" string="Delivery date"/>
    <field name="x_wareneingang_id" string="Goods receipt"/>
    <field name="x_partner_id" string="Supplier"/>
    <field name="x_supplier_ref" string="Order no."/>
    <field name="x_style_no" string="Style no."/>
    <field name="x_product_text" string="Product"/>
    <field name="x_shipment" string="Shipment"/>
    <field name="x_qty" string="Qty" digits="[16,0]" sum="Total"/>
    <field name="x_done" string="Arrived" widget="boolean_toggle"/>
</list>''', LINE_DE)
line_form = view('IQ Delivery Line Form', 'x_wareneingang_line', 'form', r'''
<form string="Delivery">
    <sheet>
        <group>
            <group>
                <field name="x_date" string="Delivery date" required="1"/>
                <field name="x_partner_id" string="Supplier" required="1"/>
                <field name="x_supplier_ref" string="Order no."/>
                <field name="x_shipment" string="Shipment" placeholder="e.g. Rail, Sea, Truck"/>
            </group>
            <group>
                <field name="x_product_text" string="Product" required="1"/>
                <field name="x_style_no" string="Style no."/>
                <field name="x_qty" string="Qty" digits="[16,0]" required="1"/>
                <field name="x_done" string="Arrived" widget="boolean_toggle"/>
            </group>
        </group>
        <group>
            <field name="x_wareneingang_id" string="Goods receipt" placeholder="Leave empty – it is assigned automatically"/>
        </group>
    </sheet>
</form>''', LINE_DE)
line_cal = view('IQ Delivery Line Calendar', 'x_wareneingang_line', 'calendar', r'''
<calendar string="Delivery calendar" date_start="x_date" color="x_partner_id" mode="month" quick_create="0" event_open_popup="1" form_view_id="%d">
    <field name="x_product_text"/><field name="x_shipment"/><field name="x_qty"/><field name="x_wareneingang_id"/>
</calendar>''' % line_form.id, LINE_DE)
line_search = view('IQ Delivery Line Search', 'x_wareneingang_line', 'search', r'''
<search>
    <field name="x_product_text" string="Product"/>
    <field name="x_supplier_ref" string="Order no."/>
    <field name="x_partner_id" string="Supplier"/>
    <filter name="upcoming" string="Not arrived" domain="[('x_done', '=', False)]"/>
    <filter name="overdue" string="Overdue" domain="[('x_done', '=', False), ('x_date', '&lt;', context_today().strftime('%Y-%m-%d'))]"/>
    <filter name="next30" string="Next 30 days" domain="[('x_done', '=', False), ('x_date', '&gt;=', context_today().strftime('%Y-%m-%d')), ('x_date', '&lt;=', (context_today() + relativedelta(days=30)).strftime('%Y-%m-%d'))]"/>
    <separator/>
    <filter name="g_month" string="Month" context="{'group_by': 'x_date:month'}"/>
    <filter name="g_supplier" string="Supplier" context="{'group_by': 'x_partner_id'}"/>
</search>''', LINE_DE)

stage_list = view('IQ Wareneingang Stage List', 'x_wareneingang_stage', 'list', r'''
<list editable="bottom">
    <field name="x_studio_sequence" widget="handle"/>
    <field name="x_name" string="Stage Name"/>
</list>''', {'Stage Name': 'Status'})

# =====================================================================================
# 8. Server action "Process file" (Excel import)
# =====================================================================================
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
        sup = up.x_supplier_id
        Att = env['ir.attachment'].sudo()
        fname = up.x_file_name
        att = Att.search([('res_model', '=', 'x_iq_delivery_upload'), ('res_id', '=', up.id), ('name', '=', fname)], limit=1)
        if not att:
            att = Att.create({'name': fname, 'datas': up.x_file, 'mimetype': 'application/pdf', 'res_model': 'x_iq_delivery_upload', 'res_id': up.id})
        txt = att.index_content or ''
        if len(txt.strip()) < 20:
            up.write({'x_result': '<div class="alert alert-danger">' + ('Der Text im PDF konnte nicht gelesen werden (eingescanntes PDF?). Bitte die Lieferung im Wareneingang manuell eintragen.' if DE else 'The PDF text could not be read (scanned PDF?). Please add the delivery manually.') + '</div>'})
            continue
        flat = ' '.join(txt.split())
        # ---- purchase order: PO number or vendor reference (e.g. AB 2026-232475) in the text
        cand = PO.search([('partner_id', 'child_of', sup.commercial_partner_id.id), ('state', 'in', ['purchase', 'done'])], order='id desc')
        cand = cand.filtered(lambda p: p.receipt_status != 'full') + cand.filtered(lambda p: p.receipt_status == 'full')
        po = PO
        for p in cand:
            refs = [p.name]
            r = (p.partner_ref or '').strip()
            if r:
                refs.append(r)
                core = r.split()[-1]
                if len(core) >= 6:
                    refs.append(core)
            if [x for x in refs if x and x in flat]:
                po = p
                break
        if not po:
            up.write({'x_result': '<div class="alert alert-warning">' + ('Keine passende Bestellung gefunden. Im PDF steht keine Bestellnummer (P0…) und keine Auftragsnummer, die bei einer Bestellung von ' if DE else 'No matching purchase order found. The PDF contains no PO number and no order number stored on a purchase order of ') + sup.name + ('. Bitte die Lieferanten-Auftragsnummer in der Bestellung (Feld Lieferantenreferenz) prüfen.' if DE else '. Please check the vendor reference on the purchase order.') + '</div>'})
            continue
        # ---- delivery note number
        dn = ''
        for kw in ['Lieferscheinnummer', 'Lieferschein-Nr', 'Lieferschein Nr', 'Lieferschein', 'Delivery note']:
            pos_ = flat.find(kw)
            if pos_ >= 0:
                for tok in flat[pos_ + len(kw):pos_ + len(kw) + 40].replace(':', ' ').split():
                    if [c for c in tok if c.isdigit()] and len(tok) >= 4:
                        dn = tok.strip('.,;')
                        break
            if dn:
                break
        if not dn:
            dn = fname.rsplit('.', 1)[0]
        # ---- date: delivery date in the PDF if it is in the future, otherwise today (goods arrived)
        def find_dates(t):
            out = []
            for k in range(len(t) - 9):
                c = t[k:k + 10]
                if c[2] == '.' and c[5] == '.' and c[:2].isdigit() and c[3:5].isdigit() and c[6:].isdigit():
                    try:
                        out.append((k, datetime.date(int(c[6:]), int(c[3:5]), int(c[:2]))))
                    except Exception:
                        pass
            return out
        today = datetime.date.today()
        ddate = today
        for kw in ['Liefertermin', 'Lieferdatum', 'Anlieferung']:
            pos_ = flat.find(kw)
            if pos_ >= 0:
                near = [d for k, d in find_dates(flat[pos_:pos_ + 60])]
                if near and near[0] > today:
                    ddate = near[0]
                break
        # ---- quantities per article from the PDF
        # Holfelder layout: "IQ DOGSPORT | Multifunktionsjacke 4.0, Herren, grau, S" ... "HBM-Cross-Docking-1 (40)"
        groups = []
        gqty = {}
        npos = 0
        cur = ''
        for ln in txt.splitlines():
            s = ln.strip()
            if ' | ' in s and not s.startswith(sup.name or '#') and 'Holfelder GmbH' not in s:
                art = s.split(' | ', 1)[1]
                cur = art.split(',')[0].strip()
                if cur.lower().startswith('porto') or cur.lower().startswith('spedition'):
                    cur = ''
                continue
            if cur and s.endswith(')') and '(' in s:
                n = s[s.rfind('(') + 1:-1].strip()
                if n.isdigit():
                    if cur not in gqty:
                        groups.append(cur)
                        gqty[cur] = 0
                    gqty[cur] += int(n)
                    npos += 1
                    cur = ''
        goods = po.order_line.filtered(lambda l: l.product_qty > 0 and l.product_id and l.product_id.type != 'service')
        if not groups:
            open_qty = sum([max(l.product_qty - l.qty_received, 0) for l in goods])
            names = []
            for l in goods.filtered(lambda l: l.qty_received < l.product_qty) or goods:
                n = (l.product_id.product_tmpl_id.name or '').split(' – ')[0]
                if n not in names:
                    names.append(n)
            g0 = (names[0] + (' +' + str(len(names) - 1) if len(names) > 1 else '')) if names else po.name
            groups = [g0]
            gqty[g0] = open_qty
        qty_note = (('aus PDF, ' + str(npos) + ' Positionen') if DE else ('read from PDF, ' + str(npos) + ' lines')) if npos else ('Artikel im PDF nicht erkannt – offene Menge der Bestellung' if DE else 'articles not recognised in PDF – open quantity of the purchase order')
        # ---- card of this PO (never a new delivery card if the PO already has one)
        we = WE.search([('x_studio_purchase_order', '=', po.id)], limit=1)
        new_card = False
        if not we:
            we = WE.create({'x_name': po.name, 'x_studio_purchase_order': po.id, 'x_studio_supplier': po.partner_id.id,
                            'x_supplier_ref': po.partner_ref or False})
            new_card = True
        shipment = ('Lieferschein ' if DE else 'Delivery note ') + dn
        # same delivery note uploaded again: replace its open calendar entries
        old = Line.search([('x_wareneingang_id', '=', we.id), ('x_shipment', '=', shipment), ('x_done', '=', False)])
        replaced = len(old)
        old.unlink()
        rows = ''
        total = 0
        for g in groups:
            Line.create({'x_wareneingang_id': we.id, 'x_partner_id': sup.id, 'x_supplier_ref': po.partner_ref or po.name,
                         'x_product_text': g, 'x_shipment': shipment, 'x_qty': gqty[g], 'x_date': ddate,
                         'x_name': ' · '.join([x for x in [po.partner_ref or po.name, g, shipment] if x])})
            total += gqty[g]
            rows += '<li>' + g + ': <b>' + str(int(gqty[g])) + (' Stk.' if DE else ' pcs') + '</b></li>'
        qty = total
        action_txt = (('ersetzt' if DE else 'replaced') if replaced else ('angelegt' if DE else 'created'))
        prod_txt = ', '.join(groups)
        # ---- attach the PDF to the card (once)
        raw = b64decode(up.x_file)
        if not Att.search_count([('res_model', '=', 'x_wareneingang'), ('res_id', '=', we.id), ('name', '=', fname), ('file_size', '=', len(raw))]):
            catt = Att.create({'name': fname, 'datas': up.x_file, 'mimetype': 'application/pdf', 'res_model': 'x_wareneingang', 'res_id': we.id})
            we.message_post(body=(('Lieferschein ' + dn + ' hochgeladen: ' + str(int(qty)) + ' Stk. am ' + ddate.strftime('%d.%m.%Y')) if DE else ('Delivery note ' + dn + ' uploaded: ' + str(int(qty)) + ' pcs on ' + ddate.strftime('%d.%m.%Y'))), attachment_ids=[catt.id])
        if not up.x_name:
            up.write({'x_name': sup.name + ' – ' + dn})
        up.write({'x_result': '<div class="alert alert-success mb-2">' + ('PDF verarbeitet.' if DE else 'PDF processed.') + '</div><ul>'
                  + '<li>' + ('Bestellung: ' if DE else 'Purchase order: ') + '<b>' + po.name + '</b>' + (' (' + po.partner_ref + ')' if po.partner_ref else '') + '</li>'
                  + '<li>' + ('Wareneingangs-Karte: ' if DE else 'Goods receipt card: ') + we.x_name + (' (neu)' if new_card and DE else (' (new)' if new_card else '')) + '</li>'
                  + '<li>' + ('Kalendereinträge ' if DE else 'Calendar entries ') + action_txt + ' (' + str(len(groups)) + (') am ' if DE else ') on ') + ddate.strftime('%d.%m.%Y') + ' · ' + qty_note + ':<ul>' + rows + '</ul></li>'
                  + '<li>' + ('PDF an die Karte angehängt.' if DE else 'PDF attached to the card.') + '</li>'
                  + '<li class="text-muted">' + ('Nach dem Buchen des Wareneingangs bitte in „Anstehende Lieferungen“ den Haken „Angekommen“ setzen.' if DE else 'After booking the receipt, tick "Arrived" in Upcoming deliveries.') + '</li></ul>'})
        continue
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
proc = SA.search([('name', '=', 'IQ Lieferübersicht verarbeiten')], limit=1)
if proc:
    proc.write({'code': PROCESS})
else:
    proc = SA.create({'name': 'IQ Lieferübersicht verarbeiten', 'model_id': UpM.id, 'state': 'code', 'code': PROCESS})

up_form = view('IQ Delivery Upload Form', 'x_iq_delivery_upload', 'form', r'''
<form string="Import delivery overview">
    <header>
        <button name="%d" type="action" string="Process file" class="btn-primary"/>
    </header>
    <sheet>
        <div class="text-muted mb-3">Choose the supplier and upload its delivery overview (Excel or CSV). Each order number becomes a goods receipt card. Existing ones are updated.</div>
        <group>
            <field name="x_name" string="Description" placeholder="e.g. CD delivery overview 04.11.2026"/>
            <field name="x_supplier_id" string="Supplier" required="1"/>
            <field name="x_file" string="Excel file" filename="x_file_name" required="1"/>
            <field name="x_file_name" invisible="1"/>
        </group>
        <field name="x_result" readonly="1" nolabel="1"/>
    </sheet>
</form>''' % proc.id, {
    'Import delivery overview': 'Lieferübersicht importieren', 'Process file': 'Datei verarbeiten',
    'Choose the supplier and upload its delivery overview (Excel or CSV). Each order number becomes a goods receipt card. Existing ones are updated.':
        'Lieferant wählen und dessen Lieferübersicht (Excel oder CSV) hochladen. Jede Bestellnummer wird zu einer Wareneingangs-Karte. Bestehende werden aktualisiert.',
    'Description': 'Beschreibung', 'e.g. CD delivery overview 04.11.2026': 'z.B. CD Lieferübersicht 04.11.2026',
    'Supplier': 'Lieferant', 'Excel file': 'Excel-Datei'})
up_list = view('IQ Delivery Upload List', 'x_iq_delivery_upload', 'list', r'''
<list><field name="create_date" string="Uploaded on"/><field name="x_name" string="Description"/><field name="x_supplier_id" string="Supplier"/><field name="x_file_name" string="File"/></list>''',
    {'Uploaded on': 'Hochgeladen am', 'Description': 'Beschreibung', 'Supplier': 'Lieferant', 'File': 'Datei'})

# =====================================================================================
# 9. Actions + menus
# =====================================================================================
we_act = action('Goods Receipts', 'Wareneingänge', MODEL, 'kanban,list,form,calendar',
                {'search_view_id': we_search.id, 'view_id': we_kanban.id})
line_act = action('Upcoming deliveries', 'Anstehende Lieferungen', 'x_wareneingang_line', 'calendar,list,form',
                  {'search_view_id': line_search.id, 'view_id': line_cal.id,
                   'context': "{'search_default_upcoming': 1, 'search_default_g_month': 1}"})
up_act = action('Import delivery overview', 'Lieferübersicht importieren', 'x_iq_delivery_upload', 'list,form', {'view_id': up_list.id})
st_act = action('Stages', 'Status', 'x_wareneingang_stage', 'list', {'view_id': stage_list.id})

old_menu = Menu.with_context(active_test=False).search([('action', '=', 'ir.actions.act_window,' + str(we_act.id))], limit=1)
root = old_menu.parent_id if old_menu and old_menu.parent_id else menu('Goods Receipts', 'Wareneingänge', False, False, 60,
                                                                       icon='stock,static/description/icon.png')
root.update_field_translations('name', {'en_US': 'Goods Receipts', 'de_DE': 'Wareneingänge'})
menu('Goods Receipt', 'Wareneingang', root, we_act, 1)
menu('Upcoming deliveries', 'Anstehende Lieferungen', root, line_act, 10)
menu('Import delivery overview', 'Lieferübersicht importieren', root, up_act, 20)
conf = menu('Configuration', 'Konfiguration', root, False, 90)
menu('Stages', 'Status', conf, st_act, 1)

# =====================================================================================
# 13. Report rejected delivery (model + form + button + menu)
# =====================================================================================
RejM = IrModel.search([('model', '=', 'x_iq_rejection_report')], limit=1)
if not RejM:
    RejM = IrModel.create({'name': 'Rejected delivery report', 'model': 'x_iq_rejection_report', 'state': 'manual',
                           'field_id': [(0, 0, {'name': 'x_name', 'field_description': 'Description', 'ttype': 'char'})]})
access(RejM)
addf(RejM, {'name': 'x_supplier_id', 'field_description': 'Supplier', 'ttype': 'many2one', 'relation': 'res.partner', 'on_delete': 'set null'})
addf(RejM, {'name': 'x_purchase_order_id', 'field_description': 'Purchase Order', 'ttype': 'many2one', 'relation': 'purchase.order', 'on_delete': 'set null'})
addf(RejM, {'name': 'x_product_id', 'field_description': 'Product', 'ttype': 'many2one', 'relation': 'product.template', 'on_delete': 'set null'})
addf(RejM, {'name': 'x_reason_id', 'field_description': 'Reason', 'ttype': 'many2one', 'relation': 'quality.reason', 'on_delete': 'set null'})
addf(RejM, {'name': 'x_note', 'field_description': 'Note', 'ttype': 'text'})
addf(RejM, {'name': 'x_file_ids', 'field_description': 'Files', 'ttype': 'many2many', 'relation': 'ir.attachment',
            'relation_table': 'x_rej_file_rel', 'column1': 'rej_id', 'column2': 'attachment_id'})
addf(RejM, {'name': 'x_wareneingang_id', 'field_description': 'Goods receipt card', 'ttype': 'many2one', 'relation': MODEL, 'on_delete': 'set null'})
for fname, en, de_ in [('x_name', 'Description', 'Beschreibung'), ('x_supplier_id', 'Supplier', 'Lieferant'),
                       ('x_purchase_order_id', 'Purchase Order', 'Bestellung'), ('x_product_id', 'Product', 'Produkt'),
                       ('x_reason_id', 'Reason', 'Grund'), ('x_note', 'Note', 'Notiz'), ('x_file_ids', 'Files', 'Dateien'),
                       ('x_wareneingang_id', 'Goods receipt card', 'Wareneingangs-Karte')]:
    label('x_iq_rejection_report', fname, en, de_)
RejM.update_field_translations('name', {'en_US': 'Rejected delivery report', 'de_DE': 'Abgelehnte Lieferung'})

REJECT_CODE = ids(r'''
WE = env['x_wareneingang'].sudo()
Att = env['ir.attachment'].sudo()
DE = (env.lang or 'en_US').startswith('de')
REJ = __REJ__
today = datetime.date.today()
we = WE
for r in records:
    if not r.x_supplier_id and not r.x_purchase_order_id:
        raise UserError('Bitte Lieferant oder Bestellung wählen.' if DE else 'Please choose a supplier or a purchase order.')
    if not r.x_reason_id and not r.x_note:
        raise UserError('Bitte Grund wählen oder Notiz eintragen.' if DE else 'Please choose a reason or write a note.')
    po = r.x_purchase_order_id
    sup = r.x_supplier_id or po.partner_id
    we = r.x_wareneingang_id
    if not we and po:
        we = WE.search([('x_studio_purchase_order', '=', po.id)], limit=1)
        if not we:
            we = WE.create({'x_name': po.name, 'x_studio_purchase_order': po.id, 'x_studio_supplier': po.partner_id.id,
                            'x_supplier_ref': po.partner_ref or False,
                            'x_studio_date': po.date_planned and po.date_planned.date() or False})
    if not we:
        we = WE.create({'x_name': (sup.name or '') + ' – ' + (r.x_product_id.name or r.x_name or ('Abgelehnte Lieferung' if DE else 'Rejected delivery')),
                        'x_studio_supplier': sup.id, 'x_studio_product': r.x_product_id.id or False})
    reason = ' – '.join([x for x in [r.x_reason_id.name, r.x_note] if x])
    vals = {'x_studio_stage_id': REJ, 'x_studio_rejection_reason': reason}
    if not we.x_studio_arrival_date:
        vals['x_studio_arrival_date'] = today
    we.write(vals)
    new_ids = []
    for a in r.x_file_ids:
        if a.checksum and Att.search_count([('res_model', '=', 'x_wareneingang'), ('res_id', '=', we.id), ('checksum', '=', a.checksum)]):
            continue
        new_ids.append(a.copy({'res_model': 'x_wareneingang', 'res_id': we.id}).id)
    we.message_post(body=('Lieferung abgelehnt: ' if DE else 'Delivery rejected: ') + reason + ' (' + env.user.name + ')', attachment_ids=new_ids)
    r.write({'x_wareneingang_id': we.id, 'x_name': r.x_name or we.x_name})
if we:
    action = {'type': 'ir.actions.act_window', 'res_model': 'x_wareneingang', 'res_id': we.id,
              'view_mode': 'form', 'views': [[False, 'form']], 'target': 'current'}
''')
rej_sa = SA.search([('name', '=', 'IQ Abgelehnte Lieferung melden')], limit=1)
if rej_sa:
    rej_sa.write({'code': REJECT_CODE})
else:
    rej_sa = SA.create({'name': 'IQ Abgelehnte Lieferung melden', 'model_id': RejM.id, 'state': 'code', 'code': REJECT_CODE})

REJ_DE = {'Report rejected delivery': 'Abgelehnte Lieferung melden', 'Create rejected card': 'Abgelehnte Karte erstellen',
          'Choose the supplier (or the purchase order), a reason and add the files, e.g. the measurement protocol or photos. The goods receipt card is moved to Rejected (or created if there is none) and all files are attached to it.':
              'Lieferant (oder Bestellung) und Grund wählen und Dateien hinzufügen, z.B. Messprotokoll oder Fotos. Die Wareneingangs-Karte wird nach Abgelehnt verschoben (oder neu angelegt) und alle Dateien werden angehängt.',
          'Description': 'Beschreibung', 'e.g. CD vests 167904 / 167924 – sizes out of tolerance': 'z.B. CD Westen 167904 / 167924 – Maße außerhalb Toleranz',
          'Supplier': 'Lieferant', 'Purchase Order': 'Bestellung', 'Product': 'Produkt', 'Reason': 'Grund', 'Note': 'Notiz',
          'What exactly is wrong?': 'Was genau ist falsch?', 'Files': 'Dateien',
          'Measurement protocol, photos, delivery note …': 'Messprotokoll, Fotos, Lieferschein …',
          'Goods receipt card': 'Wareneingangs-Karte', 'Reported on': 'Gemeldet am', 'Reported by': 'Gemeldet von'}
rej_form = view('IQ Rejection Report Form', 'x_iq_rejection_report', 'form', r'''
<form string="Report rejected delivery">
    <header>
        <button name="%d" type="action" string="Create rejected card" class="btn-primary"/>
    </header>
    <sheet>
        <div class="text-muted mb-3">Choose the supplier (or the purchase order), a reason and add the files, e.g. the measurement protocol or photos. The goods receipt card is moved to Rejected (or created if there is none) and all files are attached to it.</div>
        <group>
            <field name="x_name" string="Description" placeholder="e.g. CD vests 167904 / 167924 – sizes out of tolerance"/>
        </group>
        <group>
            <group>
                <field name="x_supplier_id" string="Supplier"/>
                <field name="x_purchase_order_id" string="Purchase Order" domain="[('state', 'in', ['purchase', 'done'])]"/>
                <field name="x_product_id" string="Product" invisible="x_purchase_order_id"/>
            </group>
            <group>
                <field name="x_reason_id" string="Reason"/>
                <field name="x_note" string="Note" placeholder="What exactly is wrong?"/>
            </group>
        </group>
        <group>
            <field name="x_file_ids" string="Files" widget="many2many_binary"/>
            <span class="text-muted small" colspan="2">Measurement protocol, photos, delivery note …</span>
            <field name="x_wareneingang_id" string="Goods receipt card" readonly="1" invisible="not x_wareneingang_id"/>
        </group>
    </sheet>
</form>''' % rej_sa.id, REJ_DE)
rej_list = view('IQ Rejection Report List', 'x_iq_rejection_report', 'list', r'''
<list>
    <field name="create_date" string="Reported on"/>
    <field name="create_uid" string="Reported by"/>
    <field name="x_name" string="Description"/>
    <field name="x_supplier_id" string="Supplier"/>
    <field name="x_purchase_order_id" string="Purchase Order"/>
    <field name="x_reason_id" string="Reason"/>
    <field name="x_wareneingang_id" string="Goods receipt card"/>
</list>''', REJ_DE)
rej_act = action('Report rejected delivery', 'Abgelehnte Lieferung melden', 'x_iq_rejection_report', 'list,form', {'view_id': rej_list.id})
menu('Report rejected delivery', 'Abgelehnte Lieferung melden', root, rej_act, 25)

# =====================================================================================
# 10. Automations
# =====================================================================================
GOODS_FILTER = "order_line.filtered(lambda l: l.product_qty > 0 and l.product_id and l.product_id.type != 'service')"
STAGE_CODE = ids('''
EXP, PART, DONE, REJ = __EXP__, __PART__, __DONE__, __REJ__
for we in wes:
    if we.x_studio_stage_id.id == REJ or not we.x_studio_purchase_order:
        continue
    lines = we.x_studio_purchase_order.''' + GOODS_FILTER + '''
    booked = sum(lines.mapped('qty_received'))
    if lines and not lines.filtered(lambda l: l.qty_received < l.product_qty):
        sid = DONE
    elif booked > 0:
        sid = PART
    else:
        sid = EXP
    if we.x_studio_stage_id.id != sid:
        we.write({'x_studio_stage_id': sid})
''')
automation('IQ Wareneingang: anlegen bei Bestellbestätigung', 'purchase.order', 'on_create_or_write', '''
WE = env['x_wareneingang'].sudo()
for po in records:
    if WE.search([('x_studio_purchase_order', '=', po.id)], limit=1):
        continue
    we = WE.search([('x_supplier_ref', '=', po.partner_ref), ('x_studio_purchase_order', '=', False)], limit=1) if po.partner_ref else WE
    if we:
        we.write({'x_studio_purchase_order': po.id, 'x_studio_supplier': po.partner_id.id})
        we.message_post(body='Bestellung ' + po.name + ' verknüpft / Purchase order linked')
    else:
        WE.create({
            'x_name': po.name,
            'x_studio_purchase_order': po.id,
            'x_studio_supplier': po.partner_id.id,
            'x_studio_date': po.date_planned and po.date_planned.date() or False,
            'x_supplier_ref': po.partner_ref or False,
        })
''', trigger_fields=['state'], domain="[('state', 'in', ['purchase', 'done'])]")
automation('IQ Wareneingang: Status bei Buchung', 'stock.picking', 'on_create_or_write',
           "wes = env['x_wareneingang'].sudo().search([('x_studio_purchase_order', 'in', records.mapped('purchase_id').ids)])\n" + STAGE_CODE,
           trigger_fields=['state'], domain="[('state', '=', 'done'), ('purchase_id', '!=', False)]")
automation('IQ Wareneingang: Lieferanten-Bestellnr. von Bestellung', 'purchase.order', 'on_create_or_write', '''
WE = env['x_wareneingang'].sudo()
for po in records:
    for we in WE.search([('x_studio_purchase_order', '=', po.id)]):
        if po.partner_ref and we.x_supplier_ref != po.partner_ref:
            we.write({'x_supplier_ref': po.partner_ref})
''', trigger_fields=['partner_ref'])
automation('IQ Lieferung manuell: Karte zuordnen', 'x_wareneingang_line', 'on_create', '''
if not env.context.get('import_file'):
    WE = env['x_wareneingang'].sudo()
    PO = env['purchase.order'].sudo()
    for l in records:
        if l.x_wareneingang_id:
            continue
        ref = (l.x_supplier_ref or '').strip()
        sup = l.x_partner_id
        we = WE
        if ref:
            we = WE.search([('x_supplier_ref', '=', ref)], limit=1)
            if not we and sup:
                po = PO.search([('partner_ref', '=', ref), ('partner_id', 'child_of', sup.commercial_partner_id.id)], limit=1)
                if po:
                    we = WE.search([('x_studio_purchase_order', '=', po.id)], limit=1)
                    if not we:
                        we = WE.create({'x_name': po.name, 'x_studio_purchase_order': po.id, 'x_studio_supplier': po.partner_id.id})
                    we.write({'x_supplier_ref': ref})
        if not we:
            we = WE.create({'x_name': (ref + ' – ' if ref else '') + (l.x_product_text or 'Lieferung'),
                            'x_studio_supplier': sup.id, 'x_supplier_ref': ref or False})
        l.write({'x_wareneingang_id': we.id,
                 'x_name': ' · '.join([x for x in [ref, l.x_product_text, l.x_shipment] if x])})
        we.message_post(body='Lieferung manuell hinzugefügt / delivery added manually: ' + (l.x_product_text or '') + ' · ' + str(int(l.x_qty or 0)) + ' · ' + (l.x_date.strftime('%d.%m.%Y') if l.x_date else ''))
''')

# =====================================================================================
# 11. Labels EN / DE
# =====================================================================================
for fname, en, de_ in [
        ('x_name', 'Delivery', 'Lieferung'), ('x_studio_date', 'Expected', 'Erwartet'), ('x_studio_arrival_date', 'Arrived', 'Angekommen'),
        ('x_studio_purchase_order', 'Purchase Order', 'Bestellung'), ('x_studio_supplier', 'Supplier', 'Lieferant'),
        ('x_studio_product', 'Product', 'Produkt'), ('x_studio_rejection_reason', 'Rejection reason', 'Ablehnungsgrund'),
        ('x_studio_notes', 'Notes', 'Notizen'), ('x_studio_stage_id', 'Status', 'Status'), ('x_product_summary', 'Products', 'Produkte'),
        ('x_po_line_ids', 'Order lines', 'Bestellpositionen'), ('x_receipt_ids', 'Receipts', 'Wareneingänge'),
        ('x_quality_check_ids', 'Quality checks', 'Qualitätsprüfungen'), ('x_quality_alert_ids', 'Quality alerts', 'Qualitätsmeldungen'),
        ('x_all_attachment_ids', 'Files', 'Dateien'), ('x_upload_ids', 'New files', 'Neue Dateien'),
        ('x_qty_ordered', 'Ordered', 'Bestellt'), ('x_qty_booked', 'Booked', 'Gebucht'), ('x_qty_open', 'Open', 'Offen'),
        ('x_qty_defect', 'Defective', 'Defekt'), ('x_file_count', 'Files', 'Dateien'),
        ('x_qc_fail_count', 'Failed checks', 'Fehlgeschlagene Prüfungen'), ('x_product_matrix_html', 'Size table', 'Größentabelle'),
        ('x_files_gallery_html', 'Preview', 'Vorschau'), ('x_po_vendor', 'Supplier', 'Lieferant'), ('x_po_expected', 'Expected', 'Erwartet'),
        ('x_supplier_ref', 'Supplier order no.', 'Lieferanten-Bestell-Nr.'), ('x_schedule_ids', 'Delivery schedule', 'Lieferplan'),
        ('x_next_date', 'Next delivery', 'Nächste Lieferung'), ('x_next_info', 'Next shipment', 'Nächster Versand'),
        ('x_due_state', 'Due state', 'Fälligkeit'), ('x_parts_info', 'Kit parts', 'Set-Teile')]:
    label(MODEL, fname, en, de_)
for fname, en, de_ in [('x_name', 'Delivery', 'Lieferung'), ('x_wareneingang_id', 'Goods receipt', 'Wareneingang'),
                       ('x_partner_id', 'Supplier', 'Lieferant'), ('x_supplier_ref', 'Order no.', 'Bestell-Nr.'),
                       ('x_style_no', 'Style no.', 'Artikel-Nr.'), ('x_product_text', 'Product', 'Produkt'),
                       ('x_shipment', 'Shipment', 'Versand'), ('x_qty', 'Qty', 'Menge'), ('x_date', 'Delivery date', 'Liefertermin'),
                       ('x_amount', 'Amount', 'Betrag'), ('x_currency', 'Currency', 'Währung'), ('x_done', 'Arrived', 'Angekommen')]:
    label('x_wareneingang_line', fname, en, de_)
for fname, en, de_ in [('x_name', 'Description', 'Beschreibung'), ('x_supplier_id', 'Supplier', 'Lieferant'),
                       ('x_file', 'Excel file', 'Excel-Datei'), ('x_file_name', 'File name', 'Dateiname'), ('x_result', 'Result', 'Ergebnis')]:
    label('x_iq_delivery_upload', fname, en, de_)
WE_M.update_field_translations('name', {'en_US': 'Goods Receipt', 'de_DE': 'Wareneingang'})
StM.update_field_translations('name', {'en_US': 'Goods Receipt Stages', 'de_DE': 'Wareneingang Status'})
LineM.update_field_translations('name', {'en_US': 'Delivery schedule line', 'de_DE': 'Lieferplan-Position'})
UpM.update_field_translations('name', {'en_US': 'Delivery overview upload', 'de_DE': 'Lieferübersicht-Upload'})

# =====================================================================================
# 12. One-time data: cards for open POs, vendor refs, status
# =====================================================================================
WE = env[MODEL].sudo().with_context(tracking_disable=True, mail_create_nolog=True, mail_create_nosubscribe=True)
for po in env['purchase.order'].sudo().search([('state', 'in', ['purchase', 'done'])], order='id asc'):
    if not WE.search([('x_studio_purchase_order', '=', po.id)], limit=1):
        dones = po.picking_ids.filtered(lambda p: p.state == 'done' and p.date_done)
        WE.create({'x_name': po.name, 'x_studio_purchase_order': po.id, 'x_studio_supplier': po.partner_id.id,
                   'x_studio_date': po.date_planned and po.date_planned.date() or False,
                   'x_studio_arrival_date': max(dones.mapped('date_done')).date() if dones else False,
                   'x_supplier_ref': po.partner_ref or False, 'x_studio_stage_id': EXP, 'x_active': True})
wes = WE.search([('x_studio_purchase_order', '!=', False)])
for we in wes:
    po = we.x_studio_purchase_order
    vals = {}
    if po.partner_ref and we.x_supplier_ref != po.partner_ref:
        vals['x_supplier_ref'] = po.partner_ref
    if not we.x_studio_supplier:
        vals['x_studio_supplier'] = po.partner_id.id
    if vals:
        we.write(vals)
for we in wes:
    if we.x_studio_stage_id.id == REJ:
        continue
    lines = we.x_studio_purchase_order.order_line.filtered(lambda l: l.product_qty > 0 and l.product_id and l.product_id.type != 'service')
    booked = sum(lines.mapped('qty_received'))
    if lines and not lines.filtered(lambda l: l.qty_received < l.product_qty):
        sid = DONE
    elif booked > 0:
        sid = PART
    else:
        sid = EXP
    if we.x_studio_stage_id.id != sid:
        we.write({'x_studio_stage_id': sid})


# =====================================================================================
# 14. Warehouse & team calendar page (no Odoo login: link key + page password)
# =====================================================================================
CAL_KEY = '<KEY-REMOVED>'        # only used if the parameter is empty
CAL_PASSWORD = '<PASSWORD-REMOVED>'         # only used if the parameter is empty
PAGE = r'''
P = env['ir.config_parameter'].sudo()
KEY = P.get_param('iq.delivery_calendar_key') or ''
PW = P.get_param('iq.delivery_calendar_password') or ''
params = request.params if request else {}
de = params.get('lang', 'de') != 'en'
LOGO = 'https://iq-dogsport.de/cdn/shop/files/iq-dogogsport-logo-sw-White.png?v=1761656363&width=240'
h = 2166136261
for ch in (PW + '|' + KEY):
    h = ((h ^ ord(ch)) * 16777619) % 4294967296
h2 = 2166136261
for ch in (KEY + '#' + PW):
    h2 = ((h2 ^ ord(ch)) * 16777619) % 4294967296
TOKEN = '%08x%08x' % (h, h2)
authed = bool(PW) and request.httprequest.cookies.get('iq_cal') == TOKEN
base = '?key=' + KEY + ('' if de else '&lang=en')
TITLE = 'Lager- &amp; Teamkalender' if de else 'Warehouse &amp; team calendar'
CSS = """
:root{--bg:#f4f4f2;--card:#fff;--fg:#151515;--mut:#6b7280;--line:#e5e5e2;--red:#a51d1b;--soft:#fdecea}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}
a{color:inherit}
.top{background:#151515;color:#fff;border-bottom:4px solid var(--red)}
.top .in{max-width:1400px;margin:0 auto;padding:14px 18px;display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:space-between}
.brand{display:flex;align-items:center;gap:14px}.brand img{height:38px;width:auto;display:block}
.brand h1{font:800 20px/1.1 Arial,sans-serif;margin:0;letter-spacing:.2px}.brand p{margin:2px 0 0;color:#bdbdbd;font-size:12.5px}
nav{display:flex;gap:6px;align-items:center;flex-wrap:wrap}
nav a{padding:7px 12px;border:1px solid #3a3a3a;border-radius:6px;text-decoration:none;color:#fff;background:#222}
nav a:hover{border-color:#fff}nav b{font-size:16px;margin:0 6px;min-width:140px;text-align:center}
wrap,.wrap{display:block;max-width:1400px;margin:0 auto;padding:16px 18px}
.kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-bottom:14px}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 14px}
.kpi small{display:block;color:var(--mut);font:700 11px Arial;letter-spacing:1.2px;text-transform:uppercase}
.kpi b{display:block;font:800 22px/1.2 Arial;margin-top:4px}.kpi span{color:var(--mut);font-size:12.5px}
.kpi.red{border-color:#f3b4b0;background:var(--soft)}.kpi.red b{color:var(--red)}
main{display:grid;grid-template-columns:1fr 330px;gap:16px}
.grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr)) repeat(2,minmax(0,.55fr));background:var(--line);gap:1px;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.dh{background:#ecece9;padding:7px;text-align:center;font:700 11px Arial;letter-spacing:1px;text-transform:uppercase;color:var(--mut)}
.day{background:var(--card);min-height:112px;padding:5px}.day.we{background:#fafaf8}.day.out{background:#f7f7f5}.day.out .dn{color:#c4c4c0}
.dn{font:700 12px Arial;margin-bottom:4px;display:inline-block;min-width:22px;height:22px;line-height:22px;text-align:center}
.today{box-shadow:inset 0 0 0 2px var(--red)}.today .dn{background:var(--red);color:#fff;border-radius:50%}
.ev{border-left:4px solid;background:#f4f4f2;border-radius:4px;padding:4px 6px;margin-bottom:4px;font-size:12px}
.ev b{font-size:13px}.ev span{display:block;color:var(--mut);font-size:11px}.ev.od{background:var(--soft)}
.ab{display:flex;align-items:center;gap:5px;font-size:11.5px;color:#374151;margin-bottom:3px}
.av{display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:50%;color:#fff;font:700 9px Arial;flex:none}
aside{display:flex;flex-direction:column;gap:12px}
.box{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 14px}
.box h3{margin:0 0 8px;font:800 12px Arial;letter-spacing:1.2px;text-transform:uppercase}
.box.red{border-color:#f3b4b0;background:var(--soft)}.box.red h3{color:var(--red)}
.row{display:flex;justify-content:space-between;align-items:flex-start;gap:8px;padding:6px 0;border-top:1px solid var(--line)}.row:first-of-type{border-top:0}
.row span{min-width:0}.row small{display:block;color:var(--mut)}.row b{white-space:nowrap}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px}
.row.total{border-top:2px solid var(--fg);font-weight:700}.mut{color:var(--mut)}.now{font-weight:700}
.tag{display:inline-block;font:700 10px Arial;letter-spacing:.8px;text-transform:uppercase;background:var(--red);color:#fff;border-radius:3px;padding:1px 5px;margin-left:6px;vertical-align:middle}
.agenda{display:none}
footer{max-width:1400px;margin:0 auto;padding:0 18px 20px;color:var(--mut);font-size:12px;display:flex;justify-content:space-between}
@media(max-width:980px){main{grid-template-columns:1fr}.kpis{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:700px){.grid{display:none}.agenda{display:block}.brand img{height:30px}.brand h1{font-size:17px}nav b{min-width:0}}
.agenda .d{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin-bottom:8px}
.agenda .d h4{margin:0 0 6px;font:800 13px Arial}.agenda .d.today{box-shadow:inset 0 0 0 2px var(--red)}
"""

def page_head(t):
    return ('<!doctype html><html lang="' + ('de' if de else 'en') + '"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<meta name="robots" content="noindex"><title>' + t + ' – IQ Dogsport</title><style>' + CSS + '</style>')

if not KEY or params.get('key') != KEY or not PW:
    response = request.make_response('Not found', headers=[('Content-Type', 'text/plain; charset=utf-8')], status=404)
elif params.get('logout'):
    response = request.make_response('', headers=[('Location', base)], status=303)
    response.delete_cookie('iq_cal')
elif request.httprequest.method == 'POST' and params.get('pw') == PW:
    response = request.make_response('', headers=[('Location', base + ('&m=' + params.get('m') if params.get('m') else ''))], status=303)
    response.set_cookie('iq_cal', TOKEN, max_age=2592000, httponly=True, secure=True, samesite='Lax')
elif not authed:
    err = request.httprequest.method == 'POST'
    lp = (page_head(TITLE) + '<style>.lg{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:16px}'
          '.lg form{background:#fff;border:1px solid var(--line);border-radius:10px;width:340px;max-width:100%;overflow:hidden}'
          '.lg .hd{background:#151515;border-bottom:4px solid var(--red);padding:18px;text-align:center}.lg .hd img{height:44px}'
          '.lg .bd{padding:22px}.lg h2{margin:0 0 4px;font:800 18px Arial}.lg p{margin:0 0 14px;color:var(--mut)}'
          '.lg input{width:100%;padding:11px;border:1px solid #d1d5db;border-radius:6px;font-size:15px;margin-bottom:10px}'
          '.lg button{width:100%;padding:11px;border:0;border-radius:6px;background:var(--red);color:#fff;font:700 15px Arial;cursor:pointer}'
          '.lg .e{color:var(--red);margin:10px 0 0;font-weight:700}</style></head><body><div class="lg"><form method="post" action="">'
          '<div class="hd"><img src="' + LOGO + '" alt="IQ Dogsport"></div><div class="bd"><h2>' + TITLE + '</h2>'
          '<p>' + ('Nur für das IQ Dogsport Team. Bitte Passwort eingeben.' if de else 'IQ Dogsport team only. Please enter the password.') + '</p>'
          '<input type="hidden" name="csrf_token" value="' + request.csrf_token() + '"><input type="hidden" name="key" value="' + KEY + '">'
          + ('' if de else '<input type="hidden" name="lang" value="en">')
          + ('<input type="hidden" name="m" value="' + params.get('m') + '">' if params.get('m') else '')
          + '<input type="password" name="pw" placeholder="' + ('Passwort' if de else 'Password') + '" autofocus autocomplete="current-password">'
          + '<button>' + ('Anmelden' if de else 'Sign in') + '</button>'
          + ('<p class="e">' + ('Falsches Passwort.' if de else 'Wrong password.') + '</p>' if err else '') + '</div></form></div></body></html>')
    response = request.make_response(lp, headers=[('Content-Type', 'text/html; charset=utf-8'), ('X-Robots-Tag', 'noindex'), ('Cache-Control', 'no-store')])
else:
    L = {
        'sub': 'Lieferungen ins Lager und Abwesenheiten im Team' if de else 'Deliveries to the warehouse and team absences',
        'today': 'Heute' if de else 'Today', 'total': 'Gesamt' if de else 'Total',
        'deliv': 'Lieferungen' if de else 'deliveries', 'deliv1': 'Lieferung' if de else 'delivery', 'pcs': 'Stk.' if de else 'pcs.',
        'k_today': 'Heute erwartet' if de else 'Expected today', 'k_month': 'Diesen Monat' if de else 'This month',
        'k_od': 'Überfällig' if de else 'Overdue', 'k_abs': 'Heute abwesend' if de else 'Absent today',
        'nobody': 'niemand' if de else 'nobody', 'none_today': 'keine' if de else 'none',
        'overdue': 'Überfällig – noch nicht angekommen' if de else 'Overdue – not arrived yet',
        'month_list': 'Lieferungen im ' if de else 'Deliveries in ', 'by_sup': 'Stück pro Lieferant' if de else 'Pieces per supplier',
        'abs': 'Abwesend im ' if de else 'Absent in ', 'noabs': 'Niemand abwesend.' if de else 'Nobody absent.',
        'nodel': 'Keine Lieferungen.' if de else 'No deliveries.', 'po': 'Bestellung' if de else 'PO', 'plan': 'Geplant' if de else 'Planned',
        'away': 'abwesend' if de else 'absent', 'upd': 'Stand' if de else 'Updated', 'logout': 'Abmelden' if de else 'Sign out',
        'now': 'jetzt' if de else 'now',
    }
    MONTHS = (['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'] if de else
              ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    DAYS = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'] if de else ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    LDAYS = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag'] if de else ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    esc = lambda s: (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    num = lambda q: '{:,.0f}'.format(q or 0).replace(',', '.' if de else ',')
    today = datetime.date.today()
    y = today.year
    m = today.month
    mp = params.get('m') or ''
    if len(mp) == 7 and mp[:4].isdigit() and mp[5:].isdigit() and 1 <= int(mp[5:]) <= 12:
        y = int(mp[:4])
        m = int(mp[5:])
    first = datetime.date(y, m, 1)
    nxt = datetime.date(y + (1 if m == 12 else 0), 1 if m == 12 else m + 1, 1)
    prv = datetime.date(y - (1 if m == 1 else 0), 12 if m == 1 else m - 1, 1)
    last = nxt - datetime.timedelta(days=1)
    gstart = first - datetime.timedelta(days=first.weekday())
    gend = last + datetime.timedelta(days=6 - last.weekday())

    ev = []
    Line = env['x_wareneingang_line'].sudo()
    WE = env['x_wareneingang'].sudo()
    for l in Line.search([('x_done', '=', False), ('x_date', '!=', False)], order='x_date asc'):
        ev.append({'d': l.x_date, 'sup': l.x_partner_id.commercial_partner_id.name or '', 'prod': l.x_product_text or '',
                   'ship': l.x_shipment or '', 'qty': l.x_qty or 0, 'ref': l.x_supplier_ref or '', 'kind': 'plan'})
    picks = env['stock.picking'].sudo().search([('picking_type_code', '=', 'incoming'), ('purchase_id', '!=', False),
                                                ('state', 'not in', ['done', 'cancel', 'draft'])], order='scheduled_date asc')
    for p in picks:
        card = WE.search([('x_studio_purchase_order', '=', p.purchase_id.id)], limit=1)
        if card and card.x_schedule_ids.filtered(lambda x: not x.x_done):
            continue
        moves = p.move_ids.filtered(lambda mv: mv.state != 'cancel')
        names = []
        for mv in moves:
            n = (mv.product_id.product_tmpl_id.name or '').split(' – ')[0]
            if n not in names:
                names.append(n)
        prod = names[0] if names else ''
        if len(names) > 1:
            prod += ' +' + str(len(names) - 1)
        ev.append({'d': p.scheduled_date.date() if p.scheduled_date else today, 'sup': p.partner_id.commercial_partner_id.name or '',
                   'prod': prod, 'ship': '', 'qty': sum(moves.mapped('product_uom_qty')), 'ref': p.purchase_id.name, 'kind': 'po'})
    ev = sorted(ev, key=lambda e: e['d'])

    COLORS = ['#2563eb', '#db2777', '#059669', '#d97706', '#7c3aed', '#0891b2', '#dc2626', '#65a30d']
    sups = []
    for e in ev:
        if e['sup'] not in sups:
            sups.append(e['sup'])
    col = lambda s: COLORS[sups.index(s) % len(COLORS)] if s in sups else '#6b7280'

    absn = []
    people = []
    for lv in env['hr.leave'].sudo().search([('state', '=', 'validate'), ('request_date_from', '<=', max(gend, today)), ('request_date_to', '>=', min(gstart, today))], order='request_date_from asc'):
        parts = (lv.employee_id.name or '').split()
        nm = parts[0] + (' ' + parts[-1][0] + '.' if len(parts) > 1 else '') if parts else ''
        ini = (parts[0][0] + (parts[-1][0] if len(parts) > 1 else '')).upper() if parts else '?'
        if nm not in people:
            people.append(nm)
        absn.append({'n': nm, 'i': ini, 'a': lv.request_date_from, 'b': lv.request_date_to or lv.request_date_from})
    PCOL = ['#475569', '#7c3aed', '#0f766e', '#b45309', '#be185d', '#1d4ed8', '#4d7c0f', '#9f1239']
    pcol = lambda n: PCOL[people.index(n) % len(PCOL)] if n in people else '#475569'
    av = lambda a: '<i class="av" style="background:' + pcol(a['n']) + '">' + esc(a['i']) + '</i>'

    def link(d):
        return '?key=' + KEY + '&amp;m=' + d.strftime('%Y-%m') + ('' if de else '&amp;lang=en')

    def evhtml(e, d):
        od = ' od' if d < today else ''
        return ('<div class="ev' + od + '" style="border-left-color:' + col(e['sup']) + '" title="' + esc(e['sup'] + ' · ' + e['prod']) + '">'
                + '<b>' + num(e['qty']) + '</b> ' + esc(e['prod']) + '<span>' + esc(e['sup']) + (' · ' + esc(e['ship']) if e['ship'] else '')
                + (' · ' + esc(e['ref']) if e['ref'] else '') + '</span></div>')

    def abhtml(d):
        out = ''
        if d.weekday() < 5:
            for a in absn:
                if a['a'] <= d <= a['b']:
                    out += '<div class="ab">' + av(a) + esc(a['n']) + '</div>'
        return out

    # KPIs
    tday = [x for x in ev if x['d'] == today]
    mev = [x for x in ev if first <= x['d'] <= last]
    odl = [x for x in ev if x['d'] < today]
    absnow = [a for a in absn if a['a'] <= today <= a['b'] and today.weekday() < 5]
    k = ['<div class="kpis">',
         '<div class="kpi"><small>' + L['k_today'] + '</small><b>' + (num(sum(x['qty'] for x in tday)) + ' ' + L['pcs'] if tday else L['none_today']) + '</b><span>' + str(len(tday)) + ' ' + (L['deliv1'] if len(tday) == 1 else L['deliv']) + '</span></div>',
         '<div class="kpi"><small>' + L['k_month'] + ' · ' + MONTHS[m - 1] + '</small><b>' + num(sum(x['qty'] for x in mev)) + ' ' + L['pcs'] + '</b><span>' + str(len(mev)) + ' ' + (L['deliv1'] if len(mev) == 1 else L['deliv']) + '</span></div>',
         '<div class="kpi' + (' red' if odl else '') + '"><small>' + L['k_od'] + '</small><b>' + str(len(odl)) + '</b><span>' + num(sum(x['qty'] for x in odl)) + ' ' + L['pcs'] + '</span></div>',
         '<div class="kpi"><small>' + L['k_abs'] + '</small><b>' + str(len(absnow)) + '</b><span>' + (', '.join([esc(a['n']) for a in absnow]) or L['nobody']) + '</span></div>',
         '</div>']

    # grid
    g = ['<div class="grid">']
    for dn in DAYS:
        g.append('<div class="dh">' + dn + '</div>')
    d = gstart
    while d <= gend:
        cls = 'day' + (' we' if d.weekday() >= 5 else '') + (' out' if d.month != m else '') + (' today' if d == today else '')
        g.append('<div class="' + cls + '"><div class="dn">' + str(d.day) + '</div>' + abhtml(d))
        for e in [x for x in ev if x['d'] == d]:
            g.append(evhtml(e, d))
        g.append('</div>')
        d = d + datetime.timedelta(days=1)
    g.append('</div>')

    # agenda (phones)
    ag = ['<div class="agenda">']
    d = first
    anyday = False
    while d <= last:
        evs = [x for x in ev if x['d'] == d]
        abs_ = abhtml(d)
        if evs or abs_ or d == today:
            anyday = True
            ag.append('<div class="d' + (' today' if d == today else '') + '"><h4>' + LDAYS[d.weekday()] + ', ' + d.strftime('%d.%m.') + (' <span class="tag">' + L['today'] + '</span>' if d == today else '') + '</h4>'
                      + abs_ + ''.join([evhtml(e, d) for e in evs]) + ('' if (evs or abs_) else '<span class="mut">' + L['nodel'] + '</span>') + '</div>')
        d = d + datetime.timedelta(days=1)
    if not anyday:
        ag.append('<p class="mut">' + L['nodel'] + '</p>')
    ag.append('</div>')

    # side
    s = ['<aside>']
    cur = [a for a in absn if a['a'] <= last and a['b'] >= first]
    s.append('<div class="box"><h3>' + L['abs'] + MONTHS[m - 1] + '</h3>')
    if not cur:
        s.append('<p class="mut" style="margin:0">' + L['noabs'] + '</p>')
    for a in cur:
        isnow = a['a'] <= today <= a['b']
        s.append('<div class="row' + (' now' if isnow else '') + '"><span>' + av(a) + ' ' + esc(a['n']) + (' <span class="tag">' + L['now'] + '</span>' if isnow else '') + '</span><b>'
                 + a['a'].strftime('%d.%m.') + (' &ndash; ' + a['b'].strftime('%d.%m.') if a['b'] != a['a'] else '') + '</b></div>')
    s.append('</div>')
    if odl:
        s.append('<div class="box red"><h3>' + L['overdue'] + '</h3>')
        for e in odl:
            s.append('<div class="row"><span>' + e['d'].strftime('%d.%m.') + ' ' + esc(e['prod']) + '<small>' + esc(e['sup']) + (' · ' + esc(e['ref']) if e['ref'] else '') + '</small></span><b>' + num(e['qty']) + '</b></div>')
        s.append('</div>')
    s.append('<div class="box"><h3>' + L['month_list'] + MONTHS[m - 1] + '</h3>')
    if not mev:
        s.append('<p class="mut" style="margin:0">' + L['nodel'] + '</p>')
    for e in mev:
        tag = L['po'] if e['kind'] == 'po' else L['plan']
        s.append('<div class="row"><span><i class="dot" style="background:' + col(e['sup']) + '"></i>' + e['d'].strftime('%d.%m.') + ' ' + esc(e['prod'])
                 + '<small>' + esc(e['sup']) + (' · ' + esc(e['ship']) if e['ship'] else '') + ' · ' + tag + (' ' + esc(e['ref']) if e['ref'] else '') + '</small></span><b>' + num(e['qty']) + '</b></div>')
    s.append('</div>')
    if mev:
        tot = {}
        cnt = {}
        for e in mev:
            tot[e['sup']] = tot.get(e['sup'], 0) + e['qty']
            cnt[e['sup']] = cnt.get(e['sup'], 0) + 1
        s.append('<div class="box"><h3>' + L['by_sup'] + '</h3>')
        for kk in sorted(tot, key=lambda kk: -tot[kk]):
            s.append('<div class="row"><span><i class="dot" style="background:' + col(kk) + '"></i>' + esc(kk) + '<small>' + str(cnt[kk]) + ' ' + (L['deliv1'] if cnt[kk] == 1 else L['deliv']) + '</small></span><b>' + num(tot[kk]) + '</b></div>')
        s.append('<div class="row total"><span>' + L['total'] + '</span><b>' + num(sum(tot.values())) + ' ' + L['pcs'] + '</b></div></div>')
    s.append('</aside>')

    langlink = ('?key=' + KEY + '&amp;m=' + first.strftime('%Y-%m') + '&amp;lang=en') if de else ('?key=' + KEY + '&amp;m=' + first.strftime('%Y-%m'))
    html = (page_head(TITLE) + '<meta http-equiv="refresh" content="600"></head><body>'
            + '<div class="top"><div class="in"><div class="brand"><img src="' + LOGO + '" alt="IQ Dogsport"><div><h1>' + TITLE + '</h1><p>' + L['sub'] + '</p></div></div>'
            + '<nav><a href="' + link(prv) + '">&larr;</a><b>' + MONTHS[m - 1] + ' ' + str(y) + '</b><a href="' + link(nxt) + '">&rarr;</a>'
            + '<a href="' + link(today) + '">' + L['today'] + '</a><a href="' + langlink + '">' + ('EN' if de else 'DE') + '</a></nav></div></div>'
            + '<div class="wrap">' + ''.join(k) + '<main><div>' + ''.join(g) + ''.join(ag) + '</div>' + ''.join(s) + '</main></div>'
            + '<footer><span>' + L['upd'] + ': ' + datetime.datetime.now().strftime('%d.%m.%Y %H:%M') + ' UTC</span><a href="?key=' + KEY + '&amp;logout=1">' + L['logout'] + '</a></footer></body></html>')
    response = request.make_response(html, headers=[('Content-Type', 'text/html; charset=utf-8'), ('X-Robots-Tag', 'noindex'), ('Cache-Control', 'no-store')])
'''

CP = env['ir.config_parameter'].sudo()
if not CP.get_param('iq.delivery_calendar_key'):
    CP.set_param('iq.delivery_calendar_key', CAL_KEY)
if not CP.get_param('iq.delivery_calendar_password'):
    CP.set_param('iq.delivery_calendar_password', CAL_PASSWORD)
if 'website_published' in SA._fields:
    cal_sa = SA.search([('name', '=', 'IQ Public delivery calendar')], limit=1)
    gfield = 'group_ids' if 'group_ids' in SA._fields else 'groups_id'
    cvals = {'name': 'IQ Public delivery calendar', 'model_id': LineM.id, 'state': 'code', 'code': PAGE,
             'website_published': True, 'website_path': 'iq-delivery-calendar',
             gfield: [(6, 0, [env.ref('base.group_public').id, env.ref('base.group_user').id, env.ref('base.group_portal').id])]}
    if cal_sa:
        cal_sa.write(cvals)
    else:
        cal_sa = SA.create(cvals)
    log('IQ public calendar link: ' + (cal_sa.website_url or '') + '?key=' + CP.get_param('iq.delivery_calendar_key'))
    UrlAct = env['ir.actions.act_url'].sudo()
    cal_url = '/website/action/' + (cal_sa.website_path or str(cal_sa.id)) + '?key=' + CP.get_param('iq.delivery_calendar_key')
    ua = UrlAct.search([('name', 'in', ['Warehouse & team calendar', 'Lager- & Teamkalender', 'Public calendar', 'Öffentlicher Lieferkalender'])], limit=1)
    if ua:
        ua.write({'url': cal_url, 'target': 'new'})
    else:
        ua = UrlAct.create({'name': 'Warehouse & team calendar', 'url': cal_url, 'target': 'new'})
    ua.update_field_translations('name', {'en_US': 'Warehouse & team calendar', 'de_DE': 'Lager- & Teamkalender'})
    uref = 'ir.actions.act_url,' + str(ua.id)
    um = Menu.with_context(active_test=False).search([('action', '=', uref)], limit=1)
    uvals = {'name': 'Warehouse & team calendar', 'parent_id': root.id, 'action': uref, 'sequence': 12, 'active': True}
    if um:
        um.write(uvals)
    else:
        um = Menu.create(uvals)
    um.update_field_translations('name', {'en_US': 'Warehouse & team calendar', 'de_DE': 'Lager- & Teamkalender'})
else:
    log('IQ public calendar skipped: Website app not installed')

log('IQ Goods Receipts installed: %d cards' % WE.search_count([]))
