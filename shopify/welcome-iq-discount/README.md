# Welcome-IQ discount – only IQ products (21.10.2026)

**Status 21.10.2026: live and tested.** Asana: *Welcome-IQ Rabatt: Banner, Popup und Willkommensmail anpassen* (ToDo IT Hamza) · requested by Patricia Knabl.

## 1. Why

The newsletter code **Welcome-IQ** gave 10 % on **every product**: no end date, no total limit, one use per customer (262 uses until 21.10.2026). That included:

- other brands with thin margins (Top-Matic, Nikwax, Jolly Pets, Kynovital)
- new products on their launch day (e.g. the new winter coats)

Goal: 10 % only on **IQ Dogsport's own products**, new products can be excluded, and every text in the shop says so.

## 2. How it works now

| Step | What Shopify checks | Result |
|---|---|---|
| 1 | Customer enters `Welcome-IQ` at checkout | – |
| 2 | Is the product in the collection **Welcome-Rabatt**? | yes → 10 % on this product |
| 3 | Product not in the collection (other brand, or tag `no-discount`) | no discount on this product |

The collection updates itself. A new IQ product gets the 10 % automatically. A product with the tag `no-discount` drops out automatically.

### Collection "Welcome-Rabatt"

| Setting | Value |
|---|---|
| Type | Automated, match **all** conditions |
| Condition 1 | Vendor **is equal to** `IQ Dogsport` OR `IQ Dogsport GmbH` (both spellings exist) |
| Condition 2 | Tag **does not include** `no-discount` |
| Sales channels | **0** (hidden – customers don't see it as a category) |
| Products | 151 → **149** after tagging the two winter coats |

### Discount "Welcome-IQ" (new)

| Setting | Value |
|---|---|
| Type | **Amount off products** (product discount) |
| Code | `Welcome-IQ` |
| Value | 10 % |
| Applies to | Specific collections → **Welcome-Rabatt** |
| Eligibility | All customers · Online Store |
| Minimum | none |
| Max. uses | one use per customer |
| Combinations | none |
| Active | from 21.10.2026, no end date |

### Old discount → "Welcome-IQ-ALT"

- Type **Amount off order** (whole cart). This type **cannot be limited to a collection**, so it had to be replaced, not edited.
- Renamed to `Welcome-IQ-ALT` and **deactivated** (Jan 6 – Oct 21, 262 uses). Kept for the history and reports.
- Note: "one use per customer" counts per discount, so a customer who used the old code can use the new one once.

### Excluded products (tag `no-discount`)

- IQ Winterparka Unisex
- IQ Zip-off-Wintermantel Damen

**To exclude another product:** Products → product → Tags → add `no-discount` → Save.

## 3. Texts updated

| Where | Change |
|---|---|
| Home page → section **IQ Insider Anmeldung** (live theme) | New line under "10 % zum Start." – DE: *Auf Deine erste Bestellung. Gültig für IQ Produkte, ausgenommen Neuheiten.* · EN: *On your first order. Valid on IQ products, excluding new arrivals.* |
| Flow **10% Rabatt für Newsletter-Anmeldung** → Send marketing email | "Gültig für deine erste Bestellung." → *Gültig für deine erste Bestellung auf IQ Produkte, ausgenommen Neuheiten.* |

### Section code

File in this folder: `iq-insider-anmeldung.liquid` (the full section file as it is live). Three additions to the previous version:

1. CSS class `.iq-insider__note` (small grey line, 14 px, `#52524F`)
2. The note line under the offer heading, DE/EN by `request.locale`
3. Two new settings in block **Inhalt 2**: `text_36` *Hinweis EN*, `text_37` *Hinweis DE*. Empty → the default text above is shown.

To change the text later without code: Customize → IQ Insider box → block **Inhalt 2** → *Hinweis DE / Hinweis EN*.

Gotcha: Shopify rejects a section setting **label longer than 70 characters** (`FileSaveError … label is too long`).

The Flow email contains the code as **plain text** (`WELCOME-IQ`), so it works with the new discount without relinking.

## 4. Test (21.10.2026, incognito)

| Cart | Price | Result |
|---|---|---|
| Nikwax Tech Wash | 11,90 € | no discount ✅ |
| IQ Summer Vest 3.0 | 129,90 € → **116,91 €** | 10 % ✅ |
| IQ Zip-off-Wintermantel Damen | 349,00 € | no discount ✅ |
| **Total discount** | **12,99 €** | = 10 % of the vest only ✅ |

## 5. Good to know

- **New arrivals:** the Flow *Tag 'new' für neue Produkte (60 Tage)* tags new products `new`, but the collection only excludes `no-discount`. A new IQ product gets the 10 % unless it is tagged `no-discount`.
- **Draft themes:** the section change is only in the live theme. If a draft theme (e.g. *ENTWURF IQ Outlet*) is published, copy `iq-insider-anmeldung.liquid` into it first.
- **Hidden sections** on the home page (*Newsletter Banner*, a second *Newsletter*) may still have the old 10 % text. Check them before turning them on.
- **Open:** deadline for the code (Patricia). Then add one sentence to the welcome email.

## 6. Rollback

1. Discounts → `Welcome-IQ` (new) → rename to e.g. `Welcome-IQ-NEU` → deactivate.
2. `Welcome-IQ-ALT` → rename back to `Welcome-IQ` → reactivate.
3. Section: Edit code → section file → *Older versions*.
