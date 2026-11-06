# IQ Goods Receipts – staging fix 05.11.2026 (3): 'Report rejected delivery'
# Adds menu Goods Receipts -> Report rejected delivery (new model x_iq_rejection_report).
# Run once: Scheduled Action (Model: Contact, Active = off) -> Save -> Run Manually -> Cmd+R.
# Safe to run again. If a popup appears, nothing was changed - send the text.

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


Stage = env['x_wareneingang_stage'].sudo().with_context(lang='en_US')
REJ = Stage.search([('x_name', 'in', ['Rejected', 'Abgelehnt'])], limit=1).id
if not REJ:
    raise UserError('Stage Rejected not found')
def ids(code):
    return code.replace('__REJ__', str(REJ))
we_act = Act.search([('res_model', '=', MODEL)], limit=1)
root = Menu.with_context(active_test=False).search([('action', '=', 'ir.actions.act_window,' + str(we_act.id))], limit=1).parent_id
if not root:
    raise UserError('Goods Receipts menu not found')
if not env['ir.model'].sudo().search([('model', '=', 'quality.reason')], limit=1):
    raise UserError('Model quality.reason not found (Quality app)')

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

log('IQ fix 05.11. (3): Report rejected delivery installed, menu %d' % rej_act.id)
