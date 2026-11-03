# Read-only verification
import datetime
env.invalidate_all()
allm = env['account.move'].search([
    ('move_type', 'in', ('out_invoice', 'out_refund')), ('state', '=', 'posted'),
    ('invoice_date', '>=', '2026-10-01'), ('invoice_date', '<=', '2026-10-31'),
])
pdf_ids = set(env['ir.attachment'].search([
    ('res_model', '=', 'account.move'), ('res_id', 'in', allm.ids),
    ('mimetype', '=', 'application/pdf'),
]).mapped('res_id'))
left = allm.filtered(lambda m: m.id not in pdf_ids and not m.invoice_pdf_report_id)
print(len(allm), 'October total')
print(len(left), 'without PDF:', [(m.name, m.amount_total) for m in left])
since = datetime.datetime(2026, 11, 3, 15, 0)   # UTC
print(env['mail.mail'].search_count([('model', '=', 'account.move'), ('create_date', '>=', since)]), 'mails')
print(env['mail.message'].search_count([('model', '=', 'account.move'), ('message_type', '=', 'email'),
      ('create_date', '>=', since), ('res_id', 'in', allm.ids)]), 'e-mail messages')
