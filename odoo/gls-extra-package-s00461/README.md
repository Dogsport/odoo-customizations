# GLS: 3 labels instead of 4 – order S00461 (21.10.2026)

**Status 21.10.2026: solved outside Odoo.** Delivery WH1/OUT/06806 · B2B order to Finland · carrier GLS Germany.

Customer address and tracking numbers are intentionally **not** stored here.

## 1. Problem

The order was packed in **3 packages** (PACK0000059–61), validated, and GLS created **3 labels**. It should have been **4 boxes / 4 labels**.

The delivery was already **Done**, so Odoo locks the packages and does not create new labels.

## 2. What we tried in Odoo (does not work)

| # | Try | Result |
|---|---|---|
| 1 | Clear *Tracking Reference* (Additional Info) | **Send to Shipper** button appears again |
| 2 | *Details* on a done line → set *Destination Package* to a new PACK0000062 | Saved on the line ("The done move line has been corrected"), but the **Packages** list still shows only 3 packages |
| 3 | *Unpack* on PACK0000061 | Package content empty (computed 0 kg). Delivery lines unchanged. **No stock impact** (goods are already at *Customers*) |

**Finding:** on a finished delivery in Odoo 19, the package records of the delivery do not update when you change the destination package on done lines. *Send to Shipper* would then send mixed data. **Don't use this route.**

Clean-up after the tries:

- Tracking Reference set back to the 3 original GLS numbers (this also hides *Send to Shipper* again)
- Changed lines (WMD.S, WPU.S) set back to their original packages
- PACK0000062 left empty (harmless)

## 3. Fix (outside Odoo)

1. Repack the goods physically into 4 boxes. Keep the 3 existing labels.
2. Create **one extra label** in the GLS portal (shipping section, not the tracking overview).
3. **Log note** on the delivery: 4th tracking number + what is in the 4th box.
4. Send the customer the 4th tracking number.

### GLS portal: why there is no "Cancel"

- Labels created by Odoo appear in the GLS **tracking overview** (status *Preadvice* = data sent, parcel not scanned yet). That view only offers *Export*, *Proof of delivery*, *Start inquiry*.
- *Start inquiry* on a preadvice parcel gave the error *"Beim Laden der Klärungsfälle zum Paket kam es zu einem Fehler"*. Inquiries are for parcels GLS has already handled.
- To cancel a label: GLS customer service (`versand-service@gls-germany.com`), only before it is scanned.
- An unscanned label is normally not charged on a business account, but this depends on the GLS contract. A label that is cancelled must never go on a box.

## 4. Next time

Before clicking **Validate**: **Put in Pack** once per physical box. Odoo creates one package and one GLS label per box.

If the delivery is already Done and a box is missing → go straight to step 3 (extra label in the GLS portal + log note). Don't edit the done delivery.
