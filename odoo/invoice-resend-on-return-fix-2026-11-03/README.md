# Invoice re-sent on returns / exchanges – send only once, on the first delivery

**Status: Live in production (03.11.2026)** · tested in staging first · done by Hamza Mohsin

**Automation rule (production):** [IQ – Send invoice on first delivery](https://iq-dogsport.odoo.com/odoo/automations/52?debug=1) (id 52)

## In one sentence
When someone validated a **return** (or an exchange / second delivery), Odoo emailed the customer **all invoices of the order again**.
Now the invoice goes out automatically **only once – with the first delivery**. After that only by hand (**Send** button).

## Problem
- 02.11.2026: a warehouse user only validated a return (stock back in). The customer got the invoice email again, under that user's name.
- Nobody clicked "Send" – the email was created automatically during **Validate**.
- Production log: `stock.picking/web_save` (validate) → invoice PDF rendered → email message posted on the invoice, all in the same second.

## Cause
Third-party module **Automatic Invoice And Post** (Cybrosys, technical name `automatic_invoice_and_post`, version 19.0.1.0.0, AGPL-3) – installed from the Odoo.sh repo `src/user/`.

| What | Name |
|---|---|
| Setting | Settings → Accounting → **Auto Invoice Post** → **Auto Send Invoice** (system parameter `automatic_invoice_and_post.is_auto_send_invoice` = True) |
| Model | `stock.picking` (transfers) |
| Method | `button_validate()` → `_send_invoice_email()` |
| File / lines | `automatic_invoice_and_post/models/stock_picking.py`, lines 83–84 |

```python
if auto_send_invoice and self.sale_id.invoice_ids.partner_id.mapped('email'):
    self._send_invoice_email(self.sale_id.invoice_ids)   # ALL invoices, on EVERY validation
```
Missing checks: outgoing delivery or return? first delivery? invoice already sent (`is_move_sent`)? customer invoice or credit note?

Full original code (not changed): [code/cybrosys_stock_picking_ORIGINAL.py](code/cybrosys_stock_picking_ORIGINAL.py)

### How we found it
1. Production logs (Odoo.sh, times in **UTC**) – validate of the return, then invoice PDF + email in the same request.
2. Automation rules / server actions checked – only notes, nothing that sends invoices.
3. Staging shell, read-only search over custom modules:
   ```bash
   grep -rn --include=*.py -E "_generate_and_send|account\.move\.send|action_invoice_sent|account_invoices" ~/src/user | grep -v /tests/
   # → only result: automatic_invoice_and_post/models/stock_picking.py
   ```
4. Settings → Technical → System Parameters → `automatic_invoice_and_post` → `is_auto_send_invoice = True`.

## Solution (no change to the module code)
Options considered:

| Option | Result | Chosen |
|---|---|---|
| A – untick "Auto Send Invoice" only | no re-sends, but also **no first email** | ❌ |
| B – edit the Cybrosys Python file | works, but a module update overwrites it; needs Git/deploy | ❌ (too risky) |
| **C – untick "Auto Send Invoice" + own automation rule** | first delivery sends once, returns/exchanges never; no module change; off with one click | ✅ |

### 1. Setting
Settings → Accounting → **Auto Invoice Post** → **Auto Send Invoice = off** (Auto Post invoice was already off).

### 2. Automation rule
| Field | Value |
|---|---|
| Name | `IQ – Send invoice on first delivery` |
| Link | https://iq-dogsport.odoo.com/odoo/automations/52?debug=1 |
| Model | Transfer (`stock.picking`) |
| Trigger | **State is set to → Done** |
| Apply on | Status = Done · Type of Operation = Delivery · Return of is not set · Sales Order is set |
| Action | Execute Code – [code/automation_send_invoice_first_delivery.py](code/automation_send_invoice_first_delivery.py) |

Domain (code editor):
```python
[("state", "=", "done"), ("picking_type_code", "=", "outgoing"), ("return_id", "=", False), ("sale_id", "!=", False)]
```
Code:
```python
for picking in records:
    order = picking.sale_id
    if order.picking_ids.filtered(lambda p: p.id != picking.id and p.picking_type_code == 'outgoing' and p.state == 'done'):
        continue
    invoices = order.invoice_ids.filtered(lambda m: m.move_type == 'out_invoice' and m.state == 'posted' and not m.is_move_sent and m.partner_id.email)
    if invoices:
        picking._send_invoice_email(invoices)
```
It reuses the module's own `_send_invoice_email()` → same email template, PDF and customer language as before.

> When choosing the trigger "State is set to → Done", Odoo **resets** the Apply on domain – set the domain **after** the trigger.

## Behaviour now
| Situation | Automatic email | Manual "Send" |
|---|---|---|
| First delivery of the order (invoice posted, not sent yet) | ✅ once | ✅ |
| Return | ❌ | ✅ |
| Exchange / second delivery / backorder | ❌ | ✅ |
| Invoice already sent with the **Send** button before shipping | ❌ (marked as sent) | ✅ |
| Invoice sent as chatter "Send message" with PDF / outside Odoo | ⚠️ sent again (not marked as sent) | ✅ |
| Credit note | ❌ never automatically | ✅ |
| Customer without email | ❌ | – |
| Shopify POS order (no delivery, direct stock move) | handled by the POS scheduled action (below) | ✅ |

**Team rule:** to send an invoice before shipping, always use the **Send** button on the invoice – never "Send message" with the PDF.

**Backorders:** an invoice created for a second (partial) delivery is **not** sent automatically → send by hand.

## Shopify POS orders (not changed – existing jobs)
Shopify POS orders are imported by Emipro as sales orders **without a delivery** (direct stock move), so the rule above never runs for them. They are covered by existing scheduled actions (Settings → Technical → Scheduled Actions):

| Scheduled action | Interval | What it does |
|---|---|---|
| Create delayed POS invoices (Sales Order) | 5 min | creates the invoice for POS orders later |
| **Send Shopify POS Invoice (Cash)** (Journal Entry) | 2 min | emails paid **cash** POS invoices to customers with an email, once (Studio field "Shopify POS Invoice Sent") – [code](code/pos_cash_invoice_scheduled_action_REFERENCE.py) |
| Archive anonymous POS invoices (POS Customer) | 30 min | archives invoices of the generic "POS Customer" |

Unticking the Cybrosys setting does **not** affect these (they use Odoo's standard `account.move.send`).
The old automation rule "Send Shopify POS Invoice" (Journal Entry) is archived – the scheduled action replaced it.

## Test results (staging, 03.11.2026)
| # | Test | Expected | Result |
|---|---|---|---|
| 1 | Test order S00486, invoice RE/2026/05088 posted, delivery WH1/OUT/06892 validated | one email with PDF | ✅ |
| 2 | Return WH1/RET/00518 validated | no new email | ✅ |
| 3 | Exchange | no email | ⏳ not tested (rule only runs on deliveries; watch first real exchange) |
| 4 | Manual Send | works | ⏳ standard Odoo, not affected |

Then created in production (03.11.2026, 08:39) and unticked "Auto Send Invoice".

## Rollback (1 minute)
1. [Automation rule 52](https://iq-dogsport.odoo.com/odoo/automations/52?debug=1) → ⚙ → **Archive**.
2. Settings → Accounting → Auto Invoice Post → tick **Auto Send Invoice** → Save.
→ back to the old behaviour (including the re-sends).

## Open
- [ ] Check the first real delivery (one email) and the first real return / exchange (no email) in production
- [ ] Settings → Technical → Emails: nothing stuck in "Delivery Failed" (SMTP "Connection reset by peer" seen on 02.11.)
- [ ] Florian: should POS customers paying **by card** also get the invoice email? (POS job is cash only)
- [ ] Check that the contact "POS Customer (IQ Dogsport Shopify)" has **no** email
- [ ] Optional: report the bug to Cybrosys (odoo@cybrosys.com)
- [ ] If the Cybrosys module is updated / "Auto Send Invoice" ticked again → re-sends come back (and the first email is sent twice)
