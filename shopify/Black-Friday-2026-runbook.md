# IQ Dogsport | Black Friday 2026
Change record and rollback runbook — 27 November 2026

## Monday 30 November — priority checklist
- Confirm the automatic Black Friday discount is expired. Do not delete the discount record; retain it for reporting.
- Check an eligible product in the storefront and cart: MFJ 3.0 should return to EUR 279.90, Allround to EUR 127.90, Softshell 2.0 Damen to EUR 89.00, provided no unrelated changes occurred.
- Hide the homepage section named Black friday (Image with text overlay). Re-enable the original Hero section and preserve its previous slide visibility. Save and test desktop/mobile, DE/EN.
- Remove only temporary Black Friday tags (if present): `tag__sale_BLACK FRIDAY -15%`, `tag__sale_-15%`. Do not remove unrelated tags.
- Remove campaign navigation/announcement links if added. Hide the collection banner or remove its dedicated template assignment if the collection will remain accessible. Do not modify the default collection template.
- Verify the price and image badges have automatically reverted. If desired, remove the temporary Liquid/CSS via a targeted diff or restore the pre-campaign price snippet version after checking for unrelated edits.
- Test checkout with an eligible and excluded product; verify Odoo import, tax and totals. Check B2B and English storefront separately.

## 1. Campaign controls and direct links
- [Shopify collection admin](https://admin.shopify.com/store/iqdogsport/collections/595074318600) — ID 595074318600, manual collection, Black Friday – 15 % Rabatt, handle `black-friday-15-rabatt`.
- [German storefront collection](https://iq-dogsport.de/collections/black-friday-15-rabatt) / [English storefront collection](https://iq-dogsport.de/en/collections/black-friday-15-rabatt).
- [Discount admin](https://admin.shopify.com/store/iqdogsport/discounts/2190498398472) — ID from screenshot filename; [discount list](https://admin.shopify.com/store/iqdogsport/discounts).
- [Themes](https://admin.shopify.com/store/iqdogsport/themes) — active theme displayed as Arbeitskopie ab 25.11.2026 – Bewertungen. Confirm theme ID before editing; do not assume an older theme ID is current.
- [Homepage](https://iq-dogsport.de/) / [English homepage](https://iq-dogsport.de/en/).

Automatic amount-off-products discount: 15%, specific Black Friday collection, no minimum, no combinations with other product/order/shipping discounts, POS excluded, all customers selected. Start 27 Nov 00:00 CET; end 29 Nov 23:59 CET. Schedule restored after temporary early activation test on 26 Nov. Discount applies to eligible products in every collection, not only the campaign page. Existing sale prices receive an additional 15%. B2B exclusion was not confirmed.

## 2. Product scope and chronology
26 Nov: collection created, initially 18 products added, then MFJ 3.0 Damen and Unisex added. Initial list: Allround Damen/Unisex; Trainingsjacke 2.0 Damen/Unisex; Zip-In Shell Damen/Unisex; Softshell 2.0 Damen/Unisex; Hundesportweste 3.0; Sommerweste 3.0; Trainer Pants; three Train Hard hoodies; In Dog We Trust hoodie; Train Hard and Logo socks; Magnetizer; two MFJ 3.0 products. Magnetizer was questioned because the handwritten list was ambiguous. Later screenshot shows Zip-Hoodie Damen Grau and still 20 products. Exact final membership and whether Magnetizer was removed are not verified; export current collection if an authoritative inventory is needed. Do not bulk-remove products or change prices as part of rollback.

26 Nov: automatic discount created, tested early, then rescheduled. Cart screenshot confirmed MFJ 3.0 Damen Schwarz XS EUR 279.90 -> EUR 237.92. Collection and product pages originally retained regular price because automatic discounts do not change price/compare-at fields.

26–27 Nov: banner, price display, badge styling and text changed iteratively. On 27 Nov Florian requested visible -15% badges. Collection screenshots confirm red promotional prices and image badges; latest requested revision adds crossed-out prices and a detail-only savings badge, but its deployment is not confirmed.

## 3. Homepage banner
Location: theme editor > Home page > Black friday / Image with text overlay. Added separate section above Hero; original Hero hidden, not deleted in screenshot. Desktop and mobile images uploaded; removed default Subheading, Heading and Text blocks; retained Button linked via collection picker. Full width; desktop height changed toward Auto, mobile Auto, opacity 0%, parallax off, padding 0. Custom class `iq-black-friday-banner`.

Image files observed in HTML: `Black-Friday_-15_-Rabatt-auf-Hundesportbekleidung.jpg` (1920 x 640) and `Black-Friday-Hundessport-Angebot-2.jpg` (1173 x 1341). Earlier ZIP contained separate DE/EN hero assets; actual English image assignment not verified. Link picker intended to localize DE/EN paths. Transparent header overlap was observed; verify navigation remains clickable.

Section-specific CSS recommendation, based on inspected HTML (final save not independently verified):
```css
.image-with-text-ovelay__content {
  position: absolute !important; inset: 0; z-index: 5;
}
.image-with-text-ovelay__content-wrapper,
.rich-text, motion-element.block.is-animated {
  position: static !important; transform: none !important;
}
.btn--primary {
  position: absolute !important; inset: 0;
  width: 100%; height: 100%; opacity: 0;
  cursor: pointer; z-index: 6;
}
```
The misspelling `ovelay` matches inspected HTML. Earlier pseudo-element CSS was rejected by section CSS validator; absolute link was 80 x 0 px because of nested positioning/transform. Do not restore those failed attempts. Monday: hide the campaign section and re-enable Hero; no shared Liquid change required. If the section is retained hidden, its local CSS can remain for reuse.

## 4. Collection banner and template
Created `black-friday` collection template from Default collection; assigned to campaign collection (confirmed by admin screenshot). Template copied unrelated collection sections; hide those within campaign template only. Used IQ Collection Banner with desktop/mobile artwork. Title duplicated because shared section falls back to `collection.title`; image cropped due to 16:5 ratio, max-height 550px and object-fit cover. Recommended local CSS hid `.iqcb__copy` and `::before`, reset `.iqcb` aspect-ratio/max-height and `.iqcb__picture` positioning, set `.iqcb__image` width 100%, height auto, object-fit contain. Enable Desktop: gesamte Bildhöhe erhalten. Exact saved CSS not confirmed. Monday: hide campaign-specific banner or change this collection's template to Default collection if desired. Keep collection record for reuse; verify any public campaign claims removed. Do not change shared IQ Collection Banner Liquid or other collections.

## 5. Main code change: snippets/price.liquid
Location: Themes > Edit code > Snippets > price.liquid. The existing snippet chooses selected variant when `use_variant`, otherwise product; uses `price`, `compare_at_price`, money filters, volume pricing and unit pricing. Preserve those original branches. No actual Shopify prices were changed by this display code.

The temporary logic uses collection membership, availability and CET epoch timestamps. Latest supplied revision moves it into the opening Liquid block and adds `iq-bf-active` to the outer `f-price` class. Earlier revision inserted logic after `.f-price__sale`, before `.f-price__unit-wrapper`. Test override used `request.design_mode`; must be false in production.
```liquid
assign bf_test_mode = false
assign bf_active = false
assign bf_eligible = false
assign bf_now = 'now' | date: '%s' | plus: 0
assign bf_start = '2026-11-27 00:00:00 +0100' | date: '%s' | plus: 0
assign bf_end = '2026-11-29 23:59:00 +0100' | date: '%s' | plus: 0
assign bf_collections = product.collections | map: 'handle'
if bf_now >= bf_start and bf_now < bf_end
  assign bf_active = true
endif
if bf_test_mode and request.design_mode
  assign bf_active = true
endif
if bf_active and available
  if bf_collections contains 'black-friday-15-rabatt'
    assign bf_eligible = true
  endif
endif
if bf_eligible
  assign bf_price = price | times: 85 | divided_by: 100.0 | round
endif
```
This is storefront-only estimated pricing; it cannot read the actual discount eligibility. Verify cart rounding, variants, currency, B2B, other discounts and caching. The end condition is exclusive at 23:59, matching the configured end minute; verify expiration in Shopify.

Original price blocks are hidden only when `.iq-bf-active` is present. New `.iq-bf-price` block prints the calculated price. Latest proposed revision prints `.iq-bf-price-row`, `.iq-bf-discounted-price` and `.iq-bf-original-price` (current pre-BF selling price, crossed out), plus `.iq-bf-detail-badge` only on product page when `use_variant` is true. Older versions used `.f-price:has(> .iq-bf-price)` and included a small cart explanation; it was hidden first on collection cards then everywhere at user request. Recommend retain clear cart-discount explanation and verify legally required lowest 30-day reference price (not established by current price). Do not assume a compare-at price or current selling price meets that requirement.

Image badge styling is driven by the presence of `.iq-bf-price` inside the card:
```css
.product-card:has(.iq-bf-price) .product-card__image-wrapper {
  position: relative;
}
.product-card:has(.iq-bf-price) .product-card__badge .f-badge--sale {
  display: none !important;
}
.product-card:has(.iq-bf-price) .product-card__image-wrapper::after {
  content: "-15%"; position: absolute; top: 12px; left: 12px;
  z-index: 10; background: #f4a0a0; color: #000;
  padding: 4px 10px; border-radius: 5px; font-size: 13px;
  font-weight: 700; line-height: 1.3; pointer-events: none;
}
.product-card:has(.iq-bf-active.f-price--on-sale)
.product-card__image-wrapper::after { content: "Extra -15%"; }
```
Mobile variant uses 8px offsets and 12px font. Existing badges hidden only for eligible cards. Latest proposed detail badge uses Spare 15% / Save 15%, Extra -15% for existing sale products; separate detail badge snippet may still show old badge. Existing native badge rendering may be suppressed via `{% unless bf_eligible %}` around sale badge only, retaining sold-out badge. Do not edit auto-generated `foxify-product-card.liquid`.

## 6. Exact targeted code cleanup (if needed)
Preferred: compare price.liquid with the version immediately before the Black Friday edits on 26 Nov. Restore only this file if no unrelated edits would be lost. In GitHub, use a targeted revert/diff on a branch, not a reset of the whole theme. Shopify file history/Timeline availability must be checked.

Manual alternative: remove all `bf_*` assignments and eligibility conditions from opening Liquid block; remove conditional `iq-bf-active` class; remove temporary block from IQ BLACK FRIDAY comment through its closing endif before unit-price wrapper; remove its styles and any separate Black Friday-only CSS; restore original `show_sale_badge` logic by unwrapping `unless bf_eligible` or removing campaign-specific branch while preserving original `case sale_badge_type` and sold-out badge. If older version has code after sale block instead, remove that temporary block only. Search `iq-bf-`, `bf_`, `black-friday-15-rabatt`, `Extra -15%` for leftovers. If a separate product badges snippet was edited, restore only the original `{%- if on_sale and block.settings.show_sale_badge -%}` branch and remove BF-only assignments/branch. Separate edit was proposed, not confirmed. Verify syntax and preview before publishing. Do not revert the entire theme, since unrelated review and newsletter work occurred.

## 7. Newsletter work — unrelated, retain
Homepage `templates/index.json` contains `iq_home_newsletter`, type `iq-home-newsletter`, instance name IQ Insider – kompakt. Actual file `sections/iq-home-newsletter.liquid`, schema and preset name IQ Start · Newsletter. No enabled_on restriction. Add via search IQ Start; IQ Insider Anmeldung is a different section. New instance settings lack defaults; copy DE/EN settings from homepage. Form uses customer form with `contact[tags]` = `newsletter,homepage`; keep unless tracking change approved. Renaming schema/preset was optional, not confirmed applied. Default page template affects every page assigned to it; use dedicated newsletter template if needed. Do not roll this back with Black Friday.

## 8. Verification and evidence
Confirmed by conversation screenshots: 20-item collection and assigned template, scheduled discount with GMT+1, cart discount MFJ 3.0 EUR 237.92, red prices on product and collection pages, -15%/Extra -15% image badges. Latest dual-price/detail badge code provided but not independently verified saved. Banner full-click behavior and final English version require verification. No product price or inventory mutation was requested as part of display fix. Odoo and checkout beyond screenshot not independently tested.

Test matrix: eligible MFJ 3.0, already reduced Allround, Softshell Damen, socks, excluded MFJ 4.0 (verify membership), multiple sizes/colours, DE/EN, desktop/mobile, B2C/B2B, cart and checkout. After rollback verify original regular/sale badges, homepage Hero, newsletter, navigation, and no stale campaign claims. Keep order records intact.

## 9. GitHub handoff
Suggested repository path: `docs/shopify/black-friday-2026-runbook.md`. Suggested branch: `docs/black-friday-2026-runbook`. Commit message: `docs: record Black Friday 2026 Shopify changes and rollback`. Upload this Markdown file through GitHub Add file > Upload files, or use a documentation-only pull request. Do not deploy theme code from this runbook. Repository URL, branch and baseline commit are not known; GitHub is not connected in this session, so no repository write was performed. Add actual repository file/commit links once available. Sources: conversation 26–27 November, pasted Liquid/HTML and Shopify screenshots; this is a reconstructed change record, not a verified live code diff.
