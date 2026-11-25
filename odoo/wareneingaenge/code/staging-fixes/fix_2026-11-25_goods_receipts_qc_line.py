# IQ Goods Receipts – update 25.11.2026: QC line on every card (kanban)
#  - Cards with quality checks get one extra line under "Booked":  "QC  132 checked · 17 defect · 1,357 open"
#    plus a small bar (green = OK, red = defect, grey = not checked yet).
#  - "open" = booked pieces − checked pieces (only shown once something is booked).
#  - Uses the EXISTING computed fields x_quality_check_ids and x_qc_fail_count. No new fields.
#  - Changes only the kanban card design (view "IQ Wareneingang Kanban"). Running it twice is harmless.
# Install: Settings -> Technical -> Scheduled Actions -> New -> Model "Scheduled Actions" (ir.cron), Python code = this file,
#          Save -> "Run Manually". Run it on STAGING first.
# Afterwards check Settings -> Technical -> Logging, search "IQ goods receipts 25.11".

MODEL = 'x_wareneingang'
View = env['ir.ui.view'].sudo()
v = View.search([('name', '=', 'IQ Wareneingang Kanban'), ('model', '=', MODEL)], limit=1)
if not v:
    raise UserError('View "IQ Wareneingang Kanban" not found – nothing changed.')
arch = v.with_context(lang='en_US').arch_db
state = 'already installed'
if 't-set="qcn"' not in arch:
    QCLINE = (
        '<t t-set="qcrv" t-value="record.x_quality_check_ids.raw_value"/>'
        '<t t-set="qcn" t-value="(qcrv and qcrv.count) or (qcrv and qcrv.length) or 0"/>'
        '<t t-set="qcf" t-value="record.x_qc_fail_count.raw_value or 0"/>'
        '<t t-set="qcbase" t-value="(booked gt qcn) ? booked : qcn"/>'
        '<div t-if="qcn" class="mt-2 small">'
        '<div class="d-flex justify-content-between">'
        '<span class="text-muted"><i class="fa fa-check-square-o me-1"/>QC</span>'
        '<span><strong t-esc="qcn"/> <span>checked</span> · <span class="text-danger"><t t-esc="qcf"/> <span>defect</span></span>'
        '<t t-if="booked gt qcn"> · <span class="fw-bold" style="color:#b45309;"><t t-esc="Math.round(booked - qcn)"/> <span>open</span></span></t></span>'
        '</div>'
        '<div class="progress mt-1" style="height:6px;background:#e5e7eb;">'
        '<div class="progress-bar bg-success" t-attf-style="width: {{ qcbase ? Math.min(100, (qcn - qcf) * 100 / qcbase) : 0 }}%;"/>'
        '<div class="progress-bar bg-danger" t-attf-style="width: {{ qcbase ? Math.min(100, qcf * 100 / qcbase) : 0 }}%;"/>'
        '</div></div>\n                ')
    pairs = [
        ('<field name="x_studio_rejection_reason"/>',
         '<field name="x_studio_rejection_reason"/><field name="x_quality_check_ids"/><field name="x_qc_fail_count"/>'),
        ('<div t-if="rejected and record.x_studio_rejection_reason.raw_value"',
         QCLINE + '<div t-if="rejected and record.x_studio_rejection_reason.raw_value"'),
    ]
    miss = [a[:60] for a, b in pairs if arch.count(a) != 1]
    if miss:
        raise UserError('Kanban view looks different than expected – nothing changed. Not found: ' + ' | '.join(miss))
    for a, b in pairs:
        arch = arch.replace(a, b)
    v.with_context(lang='en_US').write({'arch': arch})
    state = 'installed'
try:
    v.update_field_translations('arch_db', {'de_DE': {'checked': 'geprüft', 'defect': 'defekt', 'open': 'offen'}})
except Exception:
    pass
log('IQ goods receipts 25.11 QC line ' + state, level='info')
