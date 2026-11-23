# IQ Goods Receipts – update 23.11.2026: new first column "Ware angekommen" / "Goods arrived"
#  - When the warehouse reports goods in the calendar ("Ware angekommen", with or without purchase order), the card jumps
#    into this column (amber), shows "Im Lager seit <date>" and, without PO, the counted pieces.
#  - The card also gets a To-Do activity (clock icon in the Odoo top bar).
#  - Cards that were already reported but are still in "Expected" are moved into the new column once.
#  - As soon as the receipt is booked, the existing automation moves the card to "Partly booked" / "Done" as before.
#  - No new fields. Changes: 1 stage + the kanban card design (view "IQ Wareneingang Kanban").
# Install: Settings -> Technical -> Scheduled Actions -> New -> Model "Scheduled Actions" (ir.cron), Python code = this file,
#          Save -> "Run Manually". Run it on STAGING first. Running it twice is harmless.
# Afterwards check Settings -> Technical -> Logging, search "IQ goods receipts 23.11".

MODEL = 'x_wareneingang'
Stage = env['x_wareneingang_stage'].sudo()
View = env['ir.ui.view'].sudo()

# ---------------------------------------------------------------- 1. stage (first column)
st = Stage.search([('x_name', 'in', ['Goods arrived', 'Ware angekommen', 'Arrived – to check', 'Angekommen – prüfen'])], limit=1)
if not st:
    st = Stage.create({'x_name': 'Goods arrived', 'x_studio_sequence': 5})
st.with_context(lang='en_US').write({'x_name': 'Goods arrived', 'x_studio_sequence': 5})
try:
    st.update_field_translations('x_name', {'en_US': 'Goods arrived', 'de_DE': 'Ware angekommen'})
except Exception:
    pass
ARR = st.id

# ---------------------------------------------------------------- 2. kanban card
v = View.search([('name', '=', 'IQ Wareneingang Kanban'), ('model', '=', MODEL)], limit=1)
if not v:
    raise UserError('View "IQ Wareneingang Kanban" not found – nothing changed except the new stage.')
arch = v.with_context(lang='en_US').arch_db
done_txt = 'already patched'
if 't-set="arrived"' not in arch:
    pairs = [
        ('<field name="x_file_count"/>',
         '<field name="x_file_count"/><field name="activity_ids"/><field name="activity_state"/>'),
        ('<t t-set="rejected" t-value="record.x_studio_stage_id.raw_value == ',
         '<t t-set="arrived" t-value="record.x_studio_stage_id.raw_value == ' + str(ARR) + '"/>\n            <t t-set="rejected" t-value="record.x_studio_stage_id.raw_value == '),
        ("border-left: 4px solid {{ (rejected",
         "border-left: 4px solid {{ arrived ? '#f59e0b' : (rejected"),
        ('<span t-if="rejected" class="badge rounded-pill text-bg-danger">',
         '<span t-if="arrived" class="badge rounded-pill" style="background:#f59e0b;color:#151515;"><i class="fa fa-truck me-1"/><span>Goods arrived</span></span>\n                        <span t-elif="rejected" class="badge rounded-pill text-bg-danger">'),
        ('<span t-if="record.x_due_state.raw_value == \'overdue\'"',
         '<span t-if="!arrived and record.x_due_state.raw_value == \'overdue\'"'),
        ('<span t-if="record.x_due_state.raw_value == \'soon\'"',
         '<span t-if="!arrived and record.x_due_state.raw_value == \'soon\'"'),
        ('<div t-if="ordered" class="mt-3">',
         '<div t-if="arrived" class="mt-2 px-2 py-1 small rounded" style="background:#fff7e6;border:1px solid #f59e0b;color:#7c4a03;">'
         '<i class="fa fa-home me-1"/><span>In the warehouse since</span> <strong><t t-esc="record.x_studio_arrival_date.value"/></strong>'
         '<div t-if="!record.x_studio_purchase_order.raw_value and ordered" class="fw-bold"><t t-esc="Math.round(ordered)"/> <span>pcs. counted</span></div></div>\n'
         '                <div t-if="ordered and !(arrived and !record.x_studio_purchase_order.raw_value)" class="mt-3">'),
        ('<span><i class="fa fa-paperclip me-1"/>',
         '<field name="activity_ids" widget="kanban_activity"/>\n                    <span><i class="fa fa-paperclip me-1"/>'),
    ]
    miss = [a[:60] for a, b in pairs if arch.count(a) != 1]
    if miss:
        raise UserError('Kanban view looks different than expected – nothing changed in the view. Not found: ' + ' | '.join(miss))
    for a, b in pairs:
        arch = arch.replace(a, b)
    v.with_context(lang='en_US').write({'arch': arch})
    done_txt = 'patched'
else:
    # first version of this file already ran -> only new wording
    for a, b in [('<i class="fa fa-bell me-1"/><span>Arrived – check</span>', '<i class="fa fa-truck me-1"/><span>Goods arrived</span>'),
                 ('<i class="fa fa-truck me-1"/><strong>Arrived</strong> <t t-esc="record.x_studio_arrival_date.value"/> – <span>please check and book</span>',
                  '<i class="fa fa-home me-1"/><span>In the warehouse since</span> <strong><t t-esc="record.x_studio_arrival_date.value"/></strong>')]:
        arch = arch.replace(a, b)
    v.with_context(lang='en_US').write({'arch': arch})
    done_txt = 'wording updated'
v.update_field_translations('arch_db', {'de_DE': {
    'Order': 'Bestellung', 'Rejected': 'Abgelehnt', 'Fully booked': 'Vollständig gebucht',
    'Partly booked': 'Teilweise gebucht', 'Expected': 'Erwartet', 'defective': 'defekt',
    'Arrived': 'Angekommen', 'Booked': 'Gebucht', 'pcs.': 'Stk.', 'Open:': 'Offen:',
    'Reason:': 'Grund:', 'Files': 'Dateien', 'Without PO': 'Ohne Bestellung',
    'Overdue': 'Überfällig', 'This week': 'Diese Woche', 'Next delivery': 'Nächste Lieferung',
    'No PO yet': 'Noch keine Bestellung',
    'Goods arrived': 'Ware angekommen', 'In the warehouse since': 'Im Lager seit', 'pcs. counted': 'Stk. gezählt'}})

# ---------------------------------------------------------------- 3. cards already reported but still "Expected" -> new column (once)
moved = 0
exp = Stage.search([('x_studio_sequence', '=', 10)], limit=1)
if exp:
    rep_ids = env['ir.attachment'].sudo().search([('res_model', '=', MODEL), ('name', '=like', 'Wareneingang-Meldung%')]).mapped('res_id')
    for card in env[MODEL].sudo().browse(list(set(rep_ids))).exists():
        if card.x_studio_stage_id.id == exp.id and not (card.x_qty_booked or 0):
            card.write({'x_studio_stage_id': ARR})
            moved += 1

log('IQ goods receipts 23.11 arrived column installed | stage id ' + str(ARR) + ' | kanban ' + done_txt + ' | cards moved ' + str(moved), level='info')
