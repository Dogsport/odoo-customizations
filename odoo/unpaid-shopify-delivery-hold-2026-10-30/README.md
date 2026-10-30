# Unpaid Shopify deliveries jump from Waiting to Ready – fix of automation rule 21

**Date:** 30.10.2026 · **Author:** Hamza Mohsin · **System:** Odoo 19 (Inventory)
**Status:** Staging ✅ tested 30.10.2026 · Production ⏳ ______ (date)
**Asana:** _(add task link)_

## Problem
Unpaid Shopify delivery orders (tag "Zahlung ausstehend") sometimes changed from **Waiting** to **Ready** by themselves.
The chatter showed the change under the name of the user who was working at that moment (e.g. Elena), although she never opened that order.

Example (production): **WH1/OUT/07401** (#IQD-99211) – 29.10.2026 12:19 "Wartend → Bereit" (Elena Kistritz).
At exactly 12:19 Elena validated return **WH1/RET/00564** (same product IQD-EKL-MJD3.BK.XL back into WH1/Stock).
Same pattern: **WH1/OUT/06641** reserved at 28.10.2026 11:48 when **WH1/RET/00545** was validated.

## Root cause
1. Standard Odoo: when stock comes in (return, receipt), Odoo automatically reserves it for waiting deliveries → Ready.
2. Automation rule **21** ("Change status of Transfer (For Business Partners EU and Abroad)", server action 1602) pushed Ready deliveries back to Waiting – **but only once**:
   it set the field `x_studio_auto_unreserved = True` and both the "Apply on" domain and the code skipped every delivery that already had this flag.
3. So the first reservation was undone, every later one (return, receipt, scheduler) was not. The flag could not tell a **manual release** from an **automatic reservation**.
4. The rule also only covered fiscal positions 5/6 (Business partner EU / abroad) and gateway 21 (Bank Deposit), not all unpaid Shopify orders.

The defect & repair automations (IQ – …) were checked and are **not** involved (they never change transfer status).

## Investigation (staging shell, read-only)
- `grep -rn "Zahlung ausstehend" ~/src/user` → nothing (tag is set by hand).
- Automation rules on Transfer: 21 (this rule), 27 "Block delivery if not paid" (blocks Validate only), 42 "Waiting-Lieferung: nur berechtigte Benutzer" (blocks Waiting→Done for users without group).
- Shopify connector `shopify_ept/models/sale_order.py:773` only skips payment registration for pending orders – does not touch deliveries.
- `x_studio_auto_unreserved = true` on WH1/OUT/06641 and WH1/OUT/06820 confirmed the one-time flag.

## New logic (when a delivery becomes Ready)
| Order | Result |
|---|---|
| Created by staff in Odoo (no Shopify instance) | stays Ready – never blocked |
| Shopify, invoice paid / in payment / reversed | stays Ready |
| Shopify, unpaid, **allowed user clicks Check Availability** on it | stays Ready + chatter "Unbezahlte Shopify-Lieferung manuell freigegeben durch …" |
| Shopify, unpaid, anything else (return/receipt validated, scheduler, other user) | back to **Waiting** + chatter "Shopify-Bestellung nicht bezahlt – automatisch zurück auf Wartend." |

Allowed users (same as rule 27): Anastasiia Derkach, Florian Knabl, Elena Kistritz, Hamza Mohsin.
"Stock came in" is detected by Odoo's context key `button_validate_picking_ids` (present while another transfer is validated).

## Changes in rule 21
| Setting | Before | After |
|---|---|---|
| Before Update | state ≠ Ready | unchanged |
| Apply on | Delivery, Ready, `auto unreserved` not set, fiscal position 5/6 **or** gateway Bank Deposit | `[("picking_type_code","=","outgoing"), ("state","=","assigned")]` |
| When updating | Type of Operation, Sales Order, Status, auto unreserved | Type of Operation, Status |
| Code | see `code/automation_rule_21_BEFORE.py` | see `code/automation_rule_21_AFTER.py` |
| Name (optional) | Change status of Transfer (For Business Partners EU and Abroad) | Unbezahlte Shopify-Lieferung zurück auf Wartend |

Field `x_studio_auto_unreserved` is no longer used (not deleted). No new fields.

## Tests (staging, 30.10.2026, order WH1/OUT/06641 #IQD-98804, unpaid Shopify)
| # | Test | Result |
|---|---|---|
| 1 | Allowed user clicks Check Availability | ✅ Ready + "manuell freigegeben durch Hamza Mohsin" (09:59) |
| 2 | One line (Ball Pouch IQD-EKL-MTW) set to 0 → Waiting; receipt with that product validated → order complete | ✅ rule pushed it back: "Shopify-Bestellung nicht bezahlt – automatisch zurück auf Wartend." (10:01), all reservations released |
| 3 | Paid Shopify order (06820, Shopify Payments, invoice In Payment) – Check Availability | ⏳ |
| 4 | Staff-created order – Confirm | ⏳ |

Observation: a receipt/return only reserves the products that came in; an order stays Waiting until it is complete (shipping policy "all products ready").

## Production rollout
1. Backup: copy old code (= BEFORE file) + screenshot of Apply on / When updating.
2. Apply on, When updating, Code as above. Save.
3. Smoke test: unpaid Waiting Shopify order → Check Availability (as allowed user) → Ready + release note → Unreserve.
4. Do **not** run receipt/return tests in production.

**Rollback:** paste BEFORE code back, re-add `auto unreserved is not set` and the fiscal position / Bank Deposit block to Apply on.

## Known limits / follow-ups
- An **inventory adjustment** (Apply) by an allowed user has no "validate" marker → would count as a manual release (rare).
- Unpaid orders can still hold **part** of the stock while Waiting (partial reservation) – cannot ship, but blocks those items for paid orders.
- "In Payment" counts as paid (correct for Shopify Payments; for Bank Deposit only once a payment is registered). Rule 27 uses the same check.
- Tag "Zahlung ausstehend" is manual and can be outdated (e.g. 06820 is card-paid).
- Related, separate topics: Zoll orders are not held by any rule; Shipping Policy "When all products are ready" for partly available orders.

## Team message
> Ab heute werden unbezahlte Shopify-Bestellungen automatisch auf „Wartend" zurückgesetzt, sobald sie „Bereit" werden (z. B. nach dem Validieren einer Retoure). Der Chatter zeigt den Grund. Nur Anastasiia, Florian, Elena und Hamza können eine unbezahlte Bestellung mit „Check Availability" freigeben. Kartenzahlungen („In Payment") gelten als bezahlt.
