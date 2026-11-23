# IQ Goods Receipts – update 23.11.2026 (c, v2 for Odoo 19): only Settings admins can drag cards to another column
#  Odoo 19 does not allow a "groups" setting on an extra (inherited) view any more - that was the error of v1.
#  v2 changes only the board view "IQ Wareneingang Kanban" itself:
#   <field name="x_studio_stage_id" readonly="1" groups="!base.group_system"/>  -> normal users: column is read-only = no drag
#   <field name="x_studio_stage_id" groups="base.group_system"/>                -> Settings admins: drag as usual
#  - cards still move by themselves (goods reported = "Ware angekommen", booking = "Partly booked" / "Done")
#  - the stage lock (fix_2026-11-23_goods_receipts_stage_guard.py) stays as safety net
#  No new fields, no automation changed. Running it twice is harmless.
# Install: Settings -> Technical -> Scheduled Actions -> New -> Model "Scheduled Actions" (ir.cron),
#          Python code = ONLY the content of this file, Save -> "Run Manually" -> reload the browser (Cmd+Shift+R).
#          Run it on STAGING first.
# Afterwards check Settings -> Technical -> Logging, search "IQ goods receipts 23.11c".

MODEL = 'x_wareneingang'
View = env['ir.ui.view'].sudo().with_context(lang='en_US')
base_v = View.search([('name', '=', 'IQ Wareneingang Kanban'), ('model', '=', MODEL), ('inherit_id', '=', False)], limit=1)
if not base_v:
    raise UserError('View "IQ Wareneingang Kanban" not found – nothing changed.')

OLD = '<field name="x_studio_stage_id"/>'
NEW = ('<field name="x_studio_stage_id" readonly="1" groups="!base.group_system"/>'
       '<field name="x_studio_stage_id" groups="base.group_system"/>')
arch = base_v.arch_db
# clean up a possible earlier try (records_draggable="0" on the board)
arch2 = arch.replace(' records_draggable="0"', '')
if NEW in arch2:
    what = 'already done'
elif arch2.count(OLD) >= 1:
    arch2 = arch2.replace(OLD, NEW, 1)
    what = 'drag only for admins'
else:
    raise UserError('Stage field not found in the board view – nothing changed.')
if arch2 != arch:
    base_v.write({'arch': arch2})

# remove the extra view of v1 if it exists anywhere
old_v = View.search([('name', '=', 'IQ Wareneingang Kanban – Admin drag'), ('model', '=', MODEL)])
if old_v:
    old_v.unlink()

log('IQ goods receipts 23.11c admin drag v2 | ' + what, level='info')
