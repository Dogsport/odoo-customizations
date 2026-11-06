# IQ Goods Receipts – fix 05.11.2026
# 1) Newest cards on top (kanban + list)
# 2) Upcoming deliveries opens in the calendar again (list still one click away)
# Run once: Scheduled Action (Model: Contact, Active = off) -> Run Manually -> reload browser.

View = env['ir.ui.view'].sudo().with_context(lang='en_US')
Act = env['ir.actions.act_window'].sudo()
done = []

# 1) newest first
for vname, tag in [('IQ Wareneingang Kanban', '<kanban '), ('IQ Wareneingang List', '<list')]:
    v = View.search([('name', '=', vname), ('model', '=', 'x_wareneingang')], limit=1)
    if not v:
        done.append(vname + ': NOT FOUND')
        continue
    arch = v.arch_db
    if 'default_order=' in arch.split('>', 1)[0]:
        done.append(vname + ': already sorted')
        continue
    arch = arch.replace(tag, tag + (' ' if tag == '<list' else '') + 'default_order="id desc" ', 1)
    v.write({'arch_db': arch})
    done.append(vname + ': newest first')

# 2) calendar first in Upcoming deliveries
cal = View.search([('model', '=', 'x_wareneingang_line'), ('type', '=', 'calendar')], limit=1)
act = Act.search([('res_model', '=', 'x_wareneingang_line')], limit=1)
if cal and act:
    act.view_ids.unlink()
    act.write({'view_mode': 'calendar,list,form', 'view_id': cal.id})
    done.append('Upcoming deliveries: opens in calendar')
else:
    done.append('Upcoming deliveries: calendar view or action NOT FOUND')

log('IQ fix 05.11.: ' + ' | '.join(done))
