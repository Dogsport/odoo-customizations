# DHL Parcel DE – Production rollout

**Status 20.10.2026: carriers live in Production, automations partly created, full switch GLS → DHL planned**
Odoo 19 Production (iq-dogsport.odoo.com) · BrowseInfo module `bi_delivery_dhl_de_connector` · Staging tests: see [DHL automations](../../dhl-automations.html)

> Credentials (passwords, client secret, tokens), bank details and full billing numbers are intentionally **not** stored here.

## 1. Decision
IQ Dogsport switches **completely from GLS to DHL**. Customers do not choose a carrier; DHL is set automatically:
- Germany → **DHL Parcel DE** (V01PAK)
- all other countries → **DHL Parcel DE – International** (V53WPAK)

## 2. Done today (20.10.2026)
| # | Item | Result |
|---|---|---|
| 1 | Module `bi_delivery_dhl_de_connector` committed to the Odoo.sh repo (`main`) and installed in Production | ✅ |
| 2 | Carrier **DHL Parcel DE**: Production environment, `api-eu.dhl.com`, portal user, client ID/secret, token, EKP, participation `01`, V01PAK, label thermal 103×199 (910-300-610) | ✅ |
| 3 | Carrier **DHL Parcel DE – International** (duplicate of DHL Parcel DE): same login/EKP, participation `01`, V53WPAK, label thermal 103×199 | ✅ |
| 4 | DHL developer app `Odoo_dhl_connect`: Shipping, Tracking **and Returns** enabled for Production | ✅ |
| 5 | View **IQ DHL – Conditional Receiver Buttons** (Get Receivers / Change Receiver) | ✅ |
| 6 | Automation **DHL – Automatic Return Receiver** (receiver `deu` on German DHL returns) | ✅ |
| 7 | DHL thermal labels 103×199 ordered in the DHL portal (500 pcs) | ✅ ordered, waiting for delivery |

### DHL contract (from the Business Customer Portal)
| Billing number (procedure) | Product | Used for |
|---|---|---|
| `…01 01` | DHL Paket | DHL Parcel DE |
| `…53 01` | DHL Paket International + Retoure International | DHL Parcel DE – International |
| `…07 01` | DHL Retoure Online | German returns (receiver `deu`) |
| `…08 01` | DHL Retoure with pickup | not used in Odoo |

Billing number = EKP (10 digits) + procedure (2) + participation (2). Booked products: Paket National, Paket International, Retoure National, Retoure Selbstzahler, Retoure International.

## 3. How carriers work today (GLS) – findings
Example: Shopify order `#IQD-98668` → delivery `WH1/OUT/06482`.

| Layer | Carrier | Set by |
|---|---|---|
| Shopify checkout | "GLS Deutschland" (only option) | customer |
| Odoo import (Emipro) | matches `shipping_lines.source` = `shopify` + `code` = `GLS Deutschland` with **Shopify Carrier Info** on the Odoo method "GLS Deutschland" (Fixed Price → only the price line) | Emipro |
| Sales order carrier | **GLS Germany** | automation **"Shipping add"** (Sales Order, on create, if carrier empty → GLS Germany) |
| Delivery | GLS Germany → label + tracking on **Validate**, tracking sent to Shopify with Tracking Company "GLS" | inherited from the order |

If Emipro finds no matching Source/Code, it creates a new *Fixed Price* method automatically (this is where "GLS EU", "GLS Welt Zone …" came from). A Fixed Price method cannot create labels.

## 4. Still to do
### 4.1 Automations (create with TEST GUARD = only orders of the test contact)
- [ ] **IQ Sync DHL Carrier to Delivery** – Transfer, on create and edit: outgoing delivery gets the order's DHL carrier (skips done/cancelled/with tracking).
- [ ] **Combined DHL Shipping Method** – Sales Order, on create and edit: empty or **GLS** carrier → DHL Parcel DE (DE) / DHL Parcel DE – International (other countries). Keeps non-GLS methods (e.g. Direct Sales) and orders with tracking.

### 4.2 Tests (after the labels arrive; own address, cancel every label the same day)
- [ ] DE order → DHL Parcel DE → label on 103×199 roll → tracking → Cancel Shipment → check *Shipment overview* in the DHL portal
- [ ] AT order → DHL International → label → cancel
- [ ] DE return → receiver `deu` automatic, *Change Receiver* keeps manual choice → return label → delete in *Returns overview*
- [ ] Token: does the module renew it automatically after expiry?
- [ ] Address without separate house number (e.g. "Street13") – does DHL accept it?

### 4.3 Switch day
- [ ] Back up Production (Odoo.sh)
- [ ] Remove the TEST GUARD lines from both automations
- [ ] Archive automation **"Shipping add"** (do not delete)
- [ ] Shopify → Shipping and delivery: rename "GLS Deutschland" → **DHL Paket**; all other zones → **DHL Paket International** (prices unchanged unless Florian decides otherwise)
- [ ] Odoo → both DHL carriers → *Shopify Carrier Info*: Source `shopify`, Code `DHL Paket` / `DHL Paket International`, Tracking Company = DHL (Germany)
- [ ] Test order through Shopify → order + delivery = DHL, label, tracking in Shopify
- [ ] Check the first 10–20 real orders; open GLS deliveries with labels stay GLS
- [ ] After 1–2 days: archive GLS carriers (keep for history)

### 4.4 Open decisions (Florian)
- Return costs: customer pays → Retoure Selbstzahler (`deu_SZ`) for normal returns, `deu` (paid by IQ) only for defects/warranty?
- International returns (billed to IQ via `…53 01`) – offer or not?
- Customer shipping prices per zone for DHL (DHL contract prices from the account manager).
- Non-EU shipping (CH, UK, NO …): customs data (HS code, country of origin) on products.

## 5. Security
- DHL portal password and client secret were visible in screenshots during setup → **change the portal password** after go-live and update both carriers.
- Never commit credentials, tokens, invoices or bank details to this repository (it is public).
