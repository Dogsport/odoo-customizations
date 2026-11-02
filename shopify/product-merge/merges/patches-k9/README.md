# Patches K9 merge – black + blue patches → one product

Status: **live** (2 November 2026) · done by Hamza Mohsin · method: **duplicate + add option** (no CSV import)

| | |
|---|---|
| New product | **Patches für K9 Jacke & Hundeführerweste**, Shopify ID **12411509899528** |
| URL DE | `/products/patches-k9-jacke-weste-schwarz` |
| URL EN | `/en/products/k9-jacket-vest-patches-black-1` |
| Options | **Druck** (6 values) × **Farbe** (`Schwarz`, `dunkelblau`) |
| Variants | **11** = Schwarz 6 + dunkelblau 5 (Diensthundeführer exists only in black) |
| SKUs | `IQD-EKL-PAS.*` (black), `IQD-EKL-PAB.*` (blue) – unchanged |
| Price | 12,00 € all variants |
| Odoo | 2 products, **unchanged**: *Patches K9 Jacket / Vest Black* (6) + *Patches dog handler vest blue* (5) |
| Stock at go-live | 1,684 (326 black + 1,358 blue) – identical in Shopify after Export stock |
| Reviews | old products had 0 reviews → no Judge.me group needed |
| Service ID | upload + confirmation required for Polizei, Zoll, Justiz, Police (app *Mini: Image Upload*) |

## Why
Two Shopify products ("Patches K9 Jacke / Weste schwarz" and "Patches Hundeführerweste blau") for the
same item in two colours. Merged so the customer picks print and colour on one page, like the MFJ jackets.

## How it fits together

```
ODOO (unchanged)                                 SHOPIFY
Patches K9 Jacket / Vest Black  PAS.* (6) ──┐
                                            ├──► Patches für K9 Jacke & Hundeführerweste
Patches dog handler vest blue   PAB.* (5) ──┘     Druck × Farbe = 11 variants, linked by SKU
Old Shopify products → Draft + URL redirects to the new product
```

## Variants and SKUs

| Druck | Schwarz | dunkelblau |
|---|---|---|
| Leerer Patch | `IQD-EKL-PAS.Leer` | `IQD-EKL-PAB.Leer` |
| Diensthundeführer | `IQD-EKL-PAS.DHF` | – (does not exist) |
| Polizei (nur mit Dienstausweis) | `IQD-EKL-PAS.Poz` | `IQD-EKL-PAB.Poz` |
| Zoll (nur mit Dienstausweis) | `IQD-EKL-PAS.Zoll` | `IQD-EKL-PAB.Zoll` |
| Justiz (nur mit Dienstausweis) | `IQD-EKL-PAS.Jus` | `IQD-EKL-PAB.Jus` |
| Police (nur mit Dienstausweis) | `IQD-EKL-PAS.Poc` | `IQD-EKL-PAB.Poc` |

Barcode = SKU on all variants (same as in Odoo).

---

## Step 1 – Odoo check (nothing changed)
- Product Variants → search Internal Reference `IQD-EKL-PA` → **11 variants, each SKU once**.
- 6 × `PAS` on *Patches K9 Jacket / Vest Black*, 5 × `PAB` on *Patches dog handler vest blue*.
- Saved the search `IQD-EKL-PA` as a favourite = "one list" of all 11 variants in Odoo.
- In *Sales → Products* Odoo still shows **2 products** – correct, Odoo is not merged.

![Odoo: the two patch products](images/01-odoo-two-products.jpg)

## Step 2 – Shopify: build the new product (Draft)

**2.1 Duplicate the old black product** (More actions → Duplicate): Media ✓, SKUs ✓, Barcodes ✓,
Translations ✓, **Inventory quantities ✗** (stock only from Odoo), status **Draft**.

![Duplicate dialog](images/02-duplicate-product.jpg)

**2.2 Add option `Farbe`** with `Schwarz`, `dunkelblau` – the existing 6 variants became Schwarz.

![Farbe option added](images/03-add-option-farbe.jpg)

**2.3 Delete the combination that doesn't exist:** Shopify created 12 combinations →
deleted *Diensthundeführer / dunkelblau* → **11 variants** (Diensthundeführer = 1 variant).

![Diensthundeführer only Schwarz](images/04-delete-variant.jpg)

**2.4 SKUs, barcodes, weight, price** (select all → ⋯):
- Edit SKU: the 5 `IQD-EKL-PAB.*` (copied from Odoo, exact case)
- Edit barcodes: dunkelblau = SKU
- Edit weight: as on the old products (EU shipping rates are weight-based)
- Edit price: 12,00 €

![All 11 SKUs](images/05-edit-skus.jpg)
![Barcodes – dunkelblau still empty at this point](images/06-edit-barcodes.jpg)

**2.5 Content:** images for every variant (blue patches uploaded), description for both colours,
SEO title/description, published to all channels (still Draft).

![Search engine listing](images/14-seo-listing.jpg)

## Step 3 – Odoo: link and sync
1. Shopify → Operations → **Import products** → ID `12411509899528` → queue **PDQ007027** Done.

![Import queue done](images/07-odoo-import-queue.jpg)

2. Shopify product record: **Total Variants 11 / Total Synced Variants 11**.
   "Product Template" shows only one product – that is only a label.

![Odoo Shopify record 11/11](images/08-odoo-shopify-record.jpg)

3. Variants tab: every line → the right Odoo variant by SKU.

![11 variant links](images/09-odoo-variant-links.jpg)

4. **Export stock** → Shopify = Odoo (e.g. Polizei 774 = 41 + 733, total 1,684).

![Stock in Shopify after Export stock](images/10-shopify-stock.jpg)

5. Price: the first import wrote 12,10 € into Odoo's Shopify pricelist → price fixed in Shopify → **Import products** again → 12,00 €.

![Odoo pricelist 12,00](images/11-odoo-price-12.jpg)

## Step 4 – Storefront check
- Colour switch changes the image; dunkelblau shows the blue patches.
- Diensthundeführer + dunkelblau → crossed out / *Nicht verfügbar* (combination doesn't exist).

![dunkelblau selected](images/12-storefront-dunkelblau.jpg)
![Diensthundeführer not available in dunkelblau](images/13-storefront-unavailable.jpg)

## Step 5 – Go live and redirects
1. Old black product: handle `patches-hundefuhrerweste-schwarz` → `…-schwarz-alt` (no redirect), **Draft**.
2. New product: handle `patches-k9-jacke-weste-schwarz` (was `…-copy`), **Active**.
3. Old blue product (`patch-hundefuhrerweste-blau`) → **Draft**.
4. Online Store → Navigation → **URL redirects**:

| From | To |
|---|---|
| `/products/patches-hundefuhrerweste-schwarz` | `/products/patches-k9-jacke-weste-schwarz` |
| `/products/patches-hundefuhrerweste-schwarz-alt` | `/products/patches-k9-jacke-weste-schwarz` |
| `/products/patch-hundefuhrerweste-blau` | `/products/patches-k9-jacke-weste-schwarz?variant=59324793946376` (opens *Leerer Patch / dunkelblau*) |

A redirect only works when no **active** product uses the old URL → old products must be Draft.
Test in a private window (not logged in, no theme preview).

![Create redirect](images/15-create-redirect.jpg)
![Redirect list](images/16-redirect-list.jpg)

## Step 6 – Service ID upload (app *Mini: Image Upload*)
The official prints may only be sold with a service ID.

- The app block **Image Upload** sits in the *Default product* template (all products);
  the app decides per **field** where it shows. Theme code unchanged.
- Existing field **"Polizeiweste blau"** (jacket / vests) left unchanged.

![App block in the theme](images/17-theme-image-upload-block.jpg)

**New field "New Field – 2" (patches):**

| Step | Setting |
|---|---|
| Setup | Visibility **Specific variants** → the **8** variants Polizei, Zoll, Justiz, Police × Schwarz/dunkelblau (not Leerer Patch, not Diensthundeführer) · cart label `Datei` |
| Appearance | Subtitle `Dienstausweis hochladen` · description `Datei hochladen als JPG, PNG, oder PDF bis zu 10 MB.` |
| Upload rules | Allowed file types **Images + Documents (PDF)** · max **10 MB** · **Required upload** · German error texts |
| Additional fields | **Checkbox** header `Berechtigung`, option `Ich bestätige, dass ich zum Tragen dieses behördlichen Patches berechtigt bin.` – **required**, warning `Bitte bestätige deine Berechtigung zum Tragen des Patches.` |

![Setup – visibility](images/18-app-field-setup.jpg)
![Select the 8 variants](images/19-app-select-variants.jpg)
![Appearance](images/20-app-appearance.jpg)
![Upload rules](images/21-app-upload-rules.jpg)
![Checkbox field](images/22-app-checkbox.jpg)

The app's language dropdown ("English ⌄") only changes the **app interface**, not the shop texts.

## Step 7 – English translations (Translate & Adapt)
Duplicating copied the **old black product's English texts**; option values were auto-translated wrongly
("Pressure", Polizei → "Police" twice).

**Product** (Translate & Adapt → English → Products → the product):

| Field | English |
|---|---|
| Title | `Patches for K9 Jacket & Dog Handler Vest` |
| Product type | `Dog handler equipment` |
| Meta title | `Velcro Patches Black & Dark Blue for K9 Jacket & Vest \| IQ Dogsport` |
| Description / meta description | both colours, see the German text |
| Option Druck | `Print` |
| Option Farbe | `Color` |
| Leerer Patch | `Blank patch` |
| Diensthundeführer | `Diensthundeführer` |
| Polizei / Zoll / Justiz / Police (nur mit Dienstausweis) | `Polizei / Zoll / Justiz / Police (only with official ID)` – **print names stay German** (text on the patch) |

![Translate & Adapt – product](images/23-translate-product.jpg)

**Colour values** are not on the product page: Farbe is linked to Shopify's colour **metaobjects** →
Translate & Adapt → dropdown **Metaobjects** → `Schwarz` → `Black`, `dunkelblau` → `Dark blue`.
Always click the black **Save** (top right) before switching entries.

![Translate & Adapt – colour metaobject](images/24-translate-color.jpg)
![English product page](images/25-storefront-english.jpg)
![English page with upload field](images/26-storefront-upload-en.jpg)

---

## Checks done
- [x] 11 SKUs = Odoo, no duplicates
- [x] Odoo 11/11 synced, stock 1,684 = Odoo
- [x] Price 12,00 € in Shopify and Odoo
- [x] Barcodes and weight on all variants
- [x] Product page DE: colour switch, images, Diensthundeführer unavailable for dunkelblau
- [x] Upload field + checkbox only on the 4 official prints

## Open
- [ ] EN option values saved correctly (Polizei/Zoll/Justiz as above, no double "Police")
- [ ] EN colour labels Black / Dark blue saved; **dunkelblau swatch white on the EN page** → check the colour (hex) of the `dunkelblau` metaobject in Content → Metaobjects
- [ ] EN texts of the upload field and checkbox (Translate & Adapt or app support)
- [ ] Produktdetails metafield still "schwarz" only (DE + EN); Google colour metafield `Schwarz` on the 5 blue variants → `Dunkelblau`
- [ ] Test all redirects in a private window (DE + `/en/`); delete wrong redirect `/products/patches-k9-jacke-weste-schwarz-alt`
- [ ] Rename app field "New Field – 2" → `Patches – Dienstausweis`
- [ ] Xboost Bundle offers with the old patch products → new product
- [ ] Collections: Bestseller / K9 Ausrüstung position; tag `NEW` / Neuheiten keep or remove
- [ ] Optional: option order Farbe before Druck
- [ ] After a few days (with Florian): Odoo → each old Shopify patch record → Variants tab → 🗑 lines (link only)

## Lessons for the playbook
- For products with few variants, **duplicate + add option** is faster than the CSV import.
- Untick **Inventory quantities** when duplicating – stock only comes from Odoo.
- Adding an option creates **all combinations** → delete those that don't exist in Odoo.
- The first Odoo import copies the Shopify price into Odoo's Shopify pricelist → set prices **before** importing.
- Odoo's "Product Template" on the Shopify record shows one product only; the real links are the variant lines.
- A redirect only works when the old URL has no active product.
- Duplicating copies the old English translations → check Translate & Adapt; colour values are translated under **Metaobjects**.
- Duplicating also copies variant metafields (e.g. Google colour) → check them for the new colour.
- Upload apps: create a **separate field per product type** with *Specific variants* instead of changing a shared field.
