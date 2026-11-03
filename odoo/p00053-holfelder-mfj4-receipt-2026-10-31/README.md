# P00053 corrected + receipts WH1/IN/00058 and WH1/IN/00080 (MFJ 4.0 Damen, Holfelder)

**Date:** 30./31.10.2026, update 03.11.2026 · **Author:** Hamza Mohsin · **System:** Odoo 19 (Purchase / Inventory) + Shopify
**Status:** PO corrected ✅ · Receipt 1/3 294 pcs ✅ (31.10.) · **All grey Damen booked ✅ (03.11., WH1/IN/00080, 345 pcs)** · Black Damen after QC ⏳ · Unisex grau not delivered ⏳
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
| Booking summary 03.11.2026 (PDF) | [files/P00053_MFJ4_Damen_grau_Booking_2026-11-03.pdf](files/P00053_MFJ4_Damen_grau_Booking_2026-11-03.pdf) – grey 499 delivered / 491 booked / 8 defective, backorder 861, photos |
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

## Backorder after 31.10. (WH1/IN/00080)
- 706 women's jackets (incl. 112 QC jackets)
- 500 MFJ 4.0 Unisex grau (not delivered yet)

## Receipt 03.11.2026 – all grey Damen booked (WH1/IN/00080)

📄 **Summary PDF (with defect photos):** [P00053_MFJ4_Damen_grau_Booking_2026-11-03.pdf](files/P00053_MFJ4_Damen_grau_Booking_2026-11-03.pdf)

QC grey finished on 02.11.: **56 checked (1 per carton), 8 defective** → book the rest of the grey women's jackets now.
Basis: counting comparison "Abgleich MFJ 4.0 Damen, LS 2026-344396, Stand 02.11." (delivery note = counted on every line, no difference).

| Grau (MJD4.GR) | XS | S | M | L | XL | 2XL | 3XL | 4XL | Total |
|---|---|---|---|---|---|---|---|---|---|
| Delivery note / counted | 25 | 95 | 150 | 125 | 65 | 30 | 4 | 5 | **499** |
| Booked 31.10. (WH1/IN/00058) | 7 | 28 | 44 | 37 | 19 | 9 | 1 | 1 | **146** |
| Defective (QC) – **not booked** | 1 | 0 | 3 | 2 | 2 | 0 | 0 | 0 | **8** |
| **Booked 03.11. (WH1/IN/00080)** | **17** | **67** | **103** | **86** | **44** | **21** | **3** | **4** | **345** |
| Check: 146 + 345 + 8 | 25 | 95 | 150 | 125 | 65 | 30 | 4 | 5 | **499 ✅** |

The 48 good QC jackets went back into stock and are included in the 345.

Steps in Odoo (production, 03.11.2026 08:26):
1. WH1/IN/00080 → grey lines: **Quantity** = booked numbers above (only the good pieces). For the 4 sizes with defects Odoo reduced the demand (XS 18→17, M 106→103, L 88→86, XL 46→44) and moved the defective pieces to the backorder.
2. Black Damen and Unisex grau: Quantity **0** (black QC still running, unisex not delivered).
3. **Validate → Create Backorder** → new backorder **WH1/IN/00081**. Destination WH1/Stock/Picklager.

Result – **all 499 grey women's jackets are accounted for: 491 in stock (146 + 345), 8 defective (open in the backorder, claim Holfelder).**

### Defective grey jackets (claim Holfelder, stored separately, not booked)
| # | Size | Defect |
|---|---|---|
| 1 | XS | R1.2 – seam lower hem + patch |
| 2 | M | inner pocket / small pocket broken |
| 3 | M | R1.3 – seams, patch |
| 4 | M | R1.5 – seams, logo |
| 5 | L | R1.4 – seams, patch, hem, front logo |
| 6 | L | R1.1 – seams, hem, hood + patch |
| 7 | XL | hole in the right inner pocket |
| 8 | XL | seam open / not clean |

Photos 30.10. and 02.11.2026, R-no. = note on the label. Photos + list go to Holfelder for the claim.

## Backorder now (WH1/IN/00081, open)
| Open | XS | S | M | L | XL | 2XL | 3XL | 4XL | Total |
|---|---|---|---|---|---|---|---|---|---|
| Damen schwarz (MJD4.BK) – QC running | 10 | 60 | 138 | 70 | 54 | 17 | 2 | 2 | **353** |
| Unisex grau (MFJ4.GR) – not delivered | – | 40 | 100 | 135 | 125 | 50 | 30 | 20 | **500** |
| Damen grau (MJD4.GR) – defective, claim | 1 | 0 | 3 | 2 | 2 | 0 | 0 | 0 | **8** |
| **Total open** | 11 | 100 | 241 | 207 | 181 | 67 | 32 | 22 | **861** |

Black: after QC book **353 minus defective** the same way (reduce demand of the defective sizes, Create Backorder).

> The 8 defective grey jackets are **still open in backorder WH1/IN/00081** (checked on the WH1/IN/00081 delivery slip, 03.11.). On P00053 the grey lines show 491 of 499 received.
> Decide with Patricia/Florian: replacements from Holfelder (receive them on these backorder lines) or credit note (then set these lines to 0 and validate without backorder for them).

## Open – Monday with Florian
- ~~Book grey rest after QC~~ ✅ 03.11. (345 booked, 8 defective not booked)
- Black Damen: book after QC (353 minus defective)
- Claim for the 8 defective grey jackets: replacement or credit note (Patricia / Florian)
- Zippers (Herren 21 / Damen 68) on delivery note but not on PO – clarify.
- Customers who waited for MFJ 3.0 Damen Schwarz from this PO – forecast dropped, check orders.
- Counting sheet date (24.10.?) vs. delivery note 28.10 / arrival 30.10 – clarify.
- After booking: check "Zahlung ausstehend" deliveries that became Ready from the new stock.

## Lessons
- Check PO against AB **per size and product** before confirming (grey 2XL–4XL had black quantities, MFJ 3.0 instead of 4.0).
- Partial receipt = enter only the quantity to book now + **Create Backorder**.
- Inventory adjustment would double stock – always receive via the PO receipt.
