# Daily report – 10.11.2026

**Prepared by:** Hamza Mohsin · **Status:** 2 topics done, 2 waiting for a decision

| # | Topic | Status |
|---|---|---|
| 1 | MFJ 4.0 Unisex grey received and booked (P00053, WH1/IN/00086) | ✅ Done |
| 2 | Quality reports for Holfelder (Unisex new, Women finalised) | ✅ Done |
| 3 | Defective jackets: not received in Odoo, Holfelder collects them | ⏳ Waiting for Holfelder (2× Unisex S, 1× L) |
| 4 | Two credit notes for one refund (#IQD-96451) – root cause found | ⏳ Decision Patricia |
| 5 | Posted invoices may not be changed + lock date 31.10.2026 | ⏳ Decision Patricia (Option 1/2) + her OK for the lock date |

---

## 1. MFJ 4.0 Unisex grey – received and booked

Holfelder delivery note **2026-344819** (05.11.2026), item SP1007176 ("Herren" at Holfelder = **MFJ 4.0 Unisex grau** in Odoo, `IQD-EKL-MFJ4.GR.*`).

| | S | M | L | XL | 2XL | 3XL | 4XL | Total |
|---|---|---|---|---|---|---|---|---|
| Ordered (P00053) | 40 | 100 | 135 | 125 | 50 | 30 | 20 | 500 |
| Delivery note = counted | 40 | 100 | 134 | 125 | 50 | 30 | 20 | **499** |
| Checked (QC) | 5 | 7 | 8 | 6 | 4 | 3 | 2 | **35** |
| Defective | 2 | – | – | – | – | – | – | **2** |
| **Booked into stock (WH1/IN/00086)** | **38** | **100** | **134** | **125** | **50** | **30** | **20** | **497** |

- Checked in Odoo: Unisex jacket **On hand 497** ✅.
- Quality checks on WH1/IN/00086: **Quantity Tested** = number checked per size, then **Pass**.
- New backorder **WH1/IN/00089** = only the 10 defective jackets (2× Unisex S + 8× Women).
- Also received: **704 zipper puller sets** (not part of the jacket QC).

**How the booking was done**
1. WH1/IN/00086 → S line Quantity **38** (not 40), all other sizes as delivered, Women lines 0.
2. Quality checks: Quantity Tested, then **Pass** for all sizes.
3. **Validate → Create Backorder.**

**Learned about the Quality "Fail" button** (control point "QC Wareneingang", type quantity):
- Fail opens a window **Quantity Failed** (pre-filled with the whole line) + **Failure Location** (`Wareneingang-Beanstandung`).
- Failed pieces are still **received** – only into the complaint location. They count as received on the PO and as stock value.
- So Fail is **not** used for jackets the supplier takes back or removes from the invoice (see 3).

**Seen in Shopify (no action yet)**
- The Unisex product is still **Draft** in Shopify (Odoo: "Unpublished"): 497 in stock, but not for sale yet.
- The Women product has **16 variants** – correct: grey 8 sizes + black 8 sizes (merged product).

## 2. Quality reports for Holfelder

All in IQ brand, English and German, stored in [P00053 files](../p00053-holfelder-mfj4-receipt-2026-10-31/files/):

| Report | Delivery note | Content |
|---|---|---|
| MFJ 4.0 Women (DE/EN) | 2026-344396 | 1,000 received, 112 checked, **8 not acceptable for sale** (grey M 1, XL 2; black XS, M, L, 3XL, 4XL 1 each); photos of each defect next to its tag; 7 photos of workmanship issues that are going into sale |
| MFJ 4.0 Unisex grey (DE/EN) | 2026-344819 | 499 received, 35 checked, **2 not acceptable for sale** (S: left sleeve seams; S: small hole at the pocket flap corner), photos |

Changes to the Women report on 06.11.: only real defect photos, no photo used twice, black jackets with the new printed tags, black L added (lower pockets have no lining pocket bags).

## 3. Defective jackets – not received in Odoo

**Holfelder's answer:** the 8 Women jackets were **removed from the delivery**, with a new order confirmation and invoice for the quantity actually delivered. Holfelder collects the complained jackets (UPS or in person) after our Unisex QC, all together, and may repair some.

**Decision:** jackets the supplier takes back and does not invoice are **not received** in Odoo.

| Way | Effect | Used |
|---|---|---|
| Fail → Wareneingang-Beanstandung / Defektlager | counted as received on P00053 and as stock value → does not match the corrected invoice | ❌ |
| **Remove the lines on the backorder** (no receipt) | P00053 shows them as not received = matches Holfelder's invoice; stock value stays correct | ✅ |

**Steps (WH1/IN/00089)**
1. Do **not** change the destination to Defektlager.
2. Remove the 8 Women lines (bin icon) → Save.
3. Unisex S (2): leave open until Holfelder answers (replacement → receive normally; credit note → remove the line).
4. Document the rejection in the Goods Receipts app (**Report rejected delivery**) with the QC reports and photos.
5. The 10 jackets stay set aside in the warehouse for collection.

**Sent / to send to Holfelder:** the Unisex QC report + 1× L delivered less (134 of 135) → please also take these out of the invoice.

## 4. Two credit notes for one refund – order #IQD-96451

**What we found** (production, read-only checks in the Odoo shell):

| Credit note | Created | By | Reference | Status |
|---|---|---|---|---|
| RRE/2026/00955 | 04.11. 08:58 | office user, by hand (support ticket 867) | "Kundendienstticket Nr. 867" | posted, in payment (PSP1/2026/02059, 129.90 €) |
| RRE/2026/00990 | 09.11. 13:47 | **scheduled action 102 "Import Shopify Payout Report"** (runs as user Hamza Mohsin) | "Partially Refunded from shopify" | posted, not paid |

Shopify timeline: on 04.11. 09:04 the item was refunded **in Shopify** (108.90 € to Klarna + 21.00 € to the gift card = 129.90 €), six minutes after the manual credit note in Odoo. The Shopify webhook for that refund **failed** (queue line 84984, ODQ017431). On 09.11. the payout import found the refund in the payout, found **no credit note linked to this Shopify refund**, and created one. Connector log 37455: *"refund amount does not match"* (129.90 € credit note vs 108.90 € payout line; the 21.00 € went to the gift card).

**Root cause:** the refund was recorded twice – in Shopify **and** by hand in Odoo. The connector links credit notes to the **Shopify refund ID**; a manual credit note has no such link, so it cannot know they are the same.

**Proposal (decision Patricia, November not yet reported):**
- Keep one credit note, cancel the other – if RRE/2026/00990 was not sent to the customer, cancel it with a chatter note.
- Reconcile the payout line −108.90 € (statement line 16345, not reconciled) and the 21.00 € gift card part; the 129.90 € payment does not match the money movement.
- **Team rule:** refund in **Shopify only** – the connector creates the Odoo credit note itself.
- Optional: scheduled actions 102 and 117 run as user Hamza Mohsin, so everything they create shows that name.

**Read-only checks used**
```python
[print(x.name, x.create_date, x.create_uid.name, x.state, x.payment_state, x.ref) for x in env['account.move'].search([('name', 'in', ['RRE/2026/00955', 'RRE/2026/00990'])])]
[print(l.id, l.create_date, l.create_uid.name, l.write_date, l.write_uid.name, l.state, getattr(l.shopify_order_data_queue_id, 'created_by', '?'), l.shopify_order_data_queue_id.name) for l in env['shopify.order.data.queue.line.ept'].search([('name', 'ilike', '96451')])]
[print(c.id, c.name, '|', c.user_id.name, '|', c.lastcall, '| active:', c.active) for c in env['ir.cron'].search([('name', 'ilike', 'shopify')])]
[print(l.id, l.create_date, l.create_uid.name, (l.message or '')[:200]) for l in env['common.log.lines.ept'].search([('create_date', '>=', '2026-11-09 12:40:00'), ('create_date', '<=', '2026-11-09 12:55:00')])]
[print(p.name, p.date, p.amount, p.journal_id.name, p.state) for p in env['account.move'].search([('name', '=', 'RRE/2026/00955')]).matched_payment_ids]
[print(l.id, l.date, l.amount, l.journal_id.name, l.is_reconciled, l.payment_ref) for l in env['account.bank.statement.line'].search([('payment_ref', 'ilike', '96451')])]
```
(Times in the database are UTC; Berlin = +1 h.)

**Check for other orders with the same problem** (read-only):
```python
d = {}; [d.setdefault(m.reversed_entry_id.name or m.invoice_origin, []).append((m.name, str(m.create_date)[:16], m.create_uid.name, m.amount_total, m.payment_state)) for m in env['account.move'].search([('move_type', '=', 'out_refund'), ('state', '=', 'posted'), ('create_date', '>=', '2026-10-01')])]; [print(k, v) for k, v in d.items() if len(v) > 1]
```

## 5. Posted invoices may not be changed + lock date

**Why** (from Patricia, after the tax advisor meeting on 06.11.): posted entries must be unalterable – § 146 (4) AO / § 239 (3) HGB ("no eraser"), GoBD (lock posted entries, corrections only as new entries), §§ 14, 14c UStG and § 31 (5) UStDV (a sent invoice is a tax document; corrections only by credit note + new invoice). Example: a posted invoice was reset and re-posted after it had been reported (109.75 → 113.54 €), so Odoo no longer matched the tax office and the customer showed 3.79 € open.

**What Patricia wants**
1. Only Anastasiia, Patricia and Hamza may **post, reset to draft or cancel** invoices.
2. **Lock Everything = 31.10.2026** (Accounting → Accounting → Lock Dates). **Never set the Hard Lock date** – it cannot be undone. Exceptions only briefly "for me", with a reason.
3. Set the lock date only after Patricia confirms the opening stock bookings are done.
4. After every monthly package to the tax office, move the lock date to the end of that month.

**Status**
- Done in production earlier: one office user changed from "Shopify Manager" to "Shopify User" (no more accounting administrator rights); the Office user has no accounting rights.
- Automation rule built and tested in **staging**: only the 3 allowed users can post/reset/cancel; others get a message to write a chatter note. Shopify connector invoices are not affected. In staging this currently means office users can only **save drafts** (= Option 2).
- **Waiting for Patricia:** Option 1 (office can post, but never reset/cancel) or Option 2 (office drafts only) · Florian's rights · terminal/API user · OK for the lock date.
- Nothing changed in production for this today.

---

## Open
- [ ] WH1/IN/00089: remove the 8 Women lines; Unisex S (2) open until Holfelder answers
- [ ] Email Holfelder: Unisex QC report + 1× L missing → adjust invoice; collection of all 10 jackets
- [ ] Unisex QC report: confirm checked S = 4 or 5 (report says 35 in total)
- [ ] Goods Receipts app: Report rejected delivery for the 8 Women + 2 Unisex S
- [ ] Unisex product: publish in Shopify when it should go on sale
- [ ] #IQD-96451: Patricia decides which credit note stays; reconcile 108.90 € payout + 21.00 € gift card – before November is locked
- [ ] Tell the office team: refunds only in Shopify
- [ ] Posted-invoice restriction: Patricia's choice Option 1/2 → production + test with the office
- [ ] Lock Everything 31.10.2026 after Patricia's OK (no Hard Lock)
