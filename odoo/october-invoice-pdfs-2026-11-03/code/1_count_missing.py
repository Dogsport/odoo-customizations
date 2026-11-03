# Read-only. Paste into: odoo-bin shell (Odoo.sh, production branch)
allm = env['account.move'].search([
    ('move_type', 'in', ('out_invoice', 'out_refund')),
    ('state', '=', 'posted'),
    ('invoice_date', '>=', '2026-10-01'),
    ('invoice_date', '<=', '2026-10-31'),
])
pdf_ids = set(env['ir.attachment'].search([
    ('res_model', '=', 'account.move'),
    ('res_id', 'in', allm.ids),
    ('mimetype', '=', 'application/pdf'),
]).mapped('res_id'))
# invoice_pdf_report_id is not stored -> filter in Python, not in the domain
todo = allm.filtered(lambda m: m.amount_total != 0
                     and m.id not in pdf_ids
                     and not m.invoice_pdf_report_id)
print(len(allm), 'October total')
print(len(todo), 'to generate:', todo.mapped('name'))
