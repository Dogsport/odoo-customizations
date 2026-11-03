# All commands and results – 03.11.2026

The full raw shell output is in the other files in this folder. This page has every command in order, with its key result.

## A. UI attempts (no shell)
| Time | Action | Result |
|---|---|---|
| 16:35 | Custom filter `invoice_pdf_report_id = False` | "Domain is invalid" (field not stored) |
| 16:37 | Filter "Main Attachment is not set" | 44 found (unreliable measure) |
| 16:46 | Extra filter on SO delivery_status | 5 delivered / 36 not delivered |
| 16:51 | Posted + Oct filter → 1061; Print → Invoice PDF (80 per page) | Print went to the printer (direct printing) |
| 17:03 | Print 200 at once | wkhtmltopdf error -9 (too big) |
| 17:30 | Print with direct printing off | Only downloads; RE/2026/05097 still has no PDF |
| 17:35 | Bulk Send | "79 invoice(s) by Email", no checkbox → **cancelled** |
| 17:56 | Single Send → untick "by Email" → **Generate** | PDF stored on RE/2026/05097 and 05057 ✅ |

## B. Staging shell (iq-dogsport-staging-40297587)
```python
# 1) error: field not stored
env['account.move'].search([..., ('invoice_pdf_report_id', '=', False)])
# -> ValueError: Cannot convert account.move.invoice_pdf_report_id to SQL because it is not stored

# 2) count, filter in Python
moves = env['account.move'].search([
    ('move_type','in',('out_invoice','out_refund')), ('state','=','posted'),
    ('invoice_date','>=','2026-10-01'), ('invoice_date','<=','2026-10-31'), ('amount_total','!=',0)])
missing = moves.filtered(lambda m: not m.invoice_pdf_report_id)

# 3) wizard default
m = missing[0]   # RE/2026/05083
wiz = env['account.move.send.wizard'].with_context(active_model='account.move', active_ids=m.ids).create({'move_id': m.id})
print(wiz.sending_methods)          # -> ['email']
wiz.sending_methods = False         # -> False

# 4) generate + check
wiz.action_send_and_print(); env.cr.commit()
# PDF: ir.attachment(51560,)  new chatter entries: []  mails queued: 0
# RE_2026_05083.pdf application/pdf 113673 bytes  0 mails for this invoice

# 5) 5 more
# RE/2026/05082..05078 -> PDF each, 0 mails

# 6) side-effect checks
# sent flag: True   attachments: []   automations on account.move: ['Change Transfer state on Paid Invoice']
# trigger: on_create_or_write  fields: ['invoice_line_ids','move_type','payment_state','state'] -> not triggered
```

## C. Production shell (knabl-florian-iq-dogsport-main-25450466)
```python
# 1) count (invoice_pdf_report_id only)
# 1061 October total | 27 zero-amount | 898 "without PDF" -> WRONG measure, stopped

# 2) test 1 record
# RE/2026/05385 methods: False -> RE_2026_05385.pdf, 0 mails

# 3) count like Patricia (any PDF attachment)
# 162 without ANY PDF attachment (3 zero-amount)

# 4) final target: no attachment AND no invoice_pdf_report_id AND amount != 0
todo = no_pdf.filtered(lambda m: m.amount_total != 0 and not m.invoice_pdf_report_id)
# 35 to generate (all credit notes RRE/2026/00897-00936)

# 5) loop (code/2_generate_pdfs.py)
# 34 done | failed: RRE/2026/00931 (could not serialize access due to concurrent update) | 0 mails

# 6) retry RRE/2026/00931 -> RRE_2026_00931.pdf

# 7) verification (code/3_verify.py)
# 1061 October total
# 2 without PDF: [('RE/2026/05314', 0.0), ('RE/2026/04645', 0.0)]
# 0 mails queued/sent today for invoices
# 0 e-mail messages on October invoices today
```

## D. UI verification
RRE/2026/00936, 00931, 00920, 00904, 00897 opened: PDF stored, no "Message sent".
Note: remove the "Invoices or Receipts" filter when searching credit notes, otherwise the list is empty.
