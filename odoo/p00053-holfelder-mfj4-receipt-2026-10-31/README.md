# P00053 corrected + partial receipt WH1/IN/00058 (MFJ 4.0 Damen, Holfelder)

**Date:** 30./31.10.2026 · **Author:** Hamza Mohsin · **System:** Odoo 19 (Purchase / Inventory) + Shopify
**Status:** PO corrected ✅ (staging → production) · Partial receipt 294 pcs ✅ · Rest in backorder ⏳ (Monday with Florian)
**Asana:** _(add task link)_ · Task by Patricia: "P00053 does not match Holfelder order confirmation 2026-232475"

## Problem
Purchase order **P00053** did not match Holfelder's order confirmation **AB 2026-232475** (confirmed: 500 MFJ 4.0 Damen grau, 500 MFJ 4.0 Unisex grau, 500 MFJ 4.0 Damen schwarz, all 97.50 €, net 146,250.00 €):
- 500 black women's jackets were entered as the **old MFJ 3.0 Damen Schwarz** (IQD-EKL-MJD3.BK.*) at **88.70 €** – wrong product, wrong price.
- MFJ 4.0 Damen grau only **490**: 2XL/3XL/4XL had 24/3/3 (the black quantities, copied by mistake).
- Odoo net 140,875.00 € instead of 146,250.00 €.

## Documents
| Document | Content |
|---|---|
| AB 2026-232475 (share Buchhaltung/2026/05) | 3 × 500 at 97.50 €, net 146,250.00 € |
| Delivery note 2026-344396 (28.10.2026) | Pos 1–8 Damen grau 25/95/150/125/65/30/4/5 = **499** · Pos 9–16 Damen schwarz 14/85/196/99/77/24/3/3 = **501** · zippers Herren 21 / Damen 68 · "Teillieferung" (unisex not included) |
| Counting sheet (warehouse, "MZ") | GESAMT gezählt = delivery note on every line · "davon Kontrolle (QC)" = jackets taken out for QC |

## PO correction (staging first, then production)
1. 8 lines **IQD-EKL-MJD3.BK.\*** → quantity **0** (confirmed PO lines cannot be deleted: *"Cannot delete a purchase order line which is in state Purchase Order"*; 0-lines are not received or billed).
2. Added **IQD-EKL-MJD4.BK.\*** (variants already existed) at **97.50 €**: XS 14 / S 85 / M 196 / L 99 / XL 77 / 2XL 24 / 3XL 3 / 4XL 3 = **501**.
3. **IQD-EKL-MJD4.GR.2XL/3XL/4XL**: 24/3/3 → **30/4/5** (grey = 499).
4. Result: **Untaxed 146,250.00 €** = AB ✅ (1,000 women's jackets × 97.50 + 500 unisex × 97.50).
- Receipt WH1/IN/00058 updated automatically (MJD3 lines demand 0, MJD4.BK lines added). PO exceptions ("3.0 Units … instead of 30.0") closed with Mark Done.
- Note: AB split 500/500, delivery 499 grey / 501 black – same total.

## Partial receipt 31.10.2026 (approved by Patricia: "1/3 is good")
QC not finished (112 jackets taken for QC, 56 grey / 56 black, some defects) → book **1/3** for the weekend, rest in backorder.

| Size | XS | S | M | L | XL | 2XL | 3XL | 4XL | Total |
|---|---|---|---|---|---|---|---|---|---|
| Grau (MJD4.GR) booked | 7 | 28 | 44 | 37 | 19 | 9 | 1 | 1 | **146** |
| Schwarz (MJD4.BK) booked | 4 | 25 | 58 | 29 | 23 | 7 | 1 | 1 | **148** |

Steps: Quantity set per table, **Unisex grau (MFJ4.GR.\*) = 0** (not delivered), MJD3 = 0 → 16 quality checks **Pass** (note on 1/16) → **Validate → Create Backorder** (never "No Backorder").
- Destination: WH1/Stock/Picklager · Effective date 31.10.2026 07:36
- Product MFJ 4.0 Damen: On hand **294**, Forecasted **1,000**, Purchased **1,000**
- Shopify stock export queue: **16/16 done**, Shopify shows grey 146 / black 148, total 294, price 279.90 €

## Backorder (open)
- 706 women's jackets (incl. 112 QC jackets)
- 500 MFJ 4.0 Unisex grau (not delivered yet)

## Open – Monday with Florian
- Book the rest after QC: OK → WH1/Stock, defective → Defektlager **or** return/claim to Holfelder (decide with Patricia).
- Zippers (Herren 21 / Damen 68) on delivery note but not on PO – clarify.
- Customers who waited for MFJ 3.0 Damen Schwarz from this PO – forecast dropped, check orders.
- Counting sheet date (24.10.?) vs. delivery note 28.10 / arrival 30.10 – clarify.
- After booking: check "Zahlung ausstehend" deliveries that became Ready from the new stock.

## Lessons
- Check PO against AB **per size and product** before confirming (grey 2XL–4XL had black quantities, MFJ 3.0 instead of 4.0).
- Partial receipt = enter only the quantity to book now + **Create Backorder**.
- Inventory adjustment would double stock – always receive via the PO receipt.
