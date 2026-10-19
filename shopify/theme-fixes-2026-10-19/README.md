# Shopify theme fixes – 19.10.2026

Small storefront fixes on iq-dogsport.de (FoxTheme). Every code change is marked with `[Hamza 2026-10-19]`.

| # | Fix | Where | File in this folder |
|---|---|---|---|
| 1 | Judge.me "Mehr anzeigen" button looks like the add-to-cart button (black pill, no border, slide hover) | Theme settings → Custom CSS | `judgeme-load-more-button.css` |
| 2 | Unit price (€/kg) small and grey in one line after the price – product page only | Theme settings → Custom CSS | `product-unit-price.css` |
| 3 | "Fit & Sizing" tab hidden when `custom.grosentabelle` is empty (≈80 products) | `snippets/product-information-blocks.liquid` | `product-information-blocks.collapsible-tab.liquid` |
| 4 | English shop showed German option names (Farbe, Größe, Schwarz …) on the merged MFJ 3.0 products | Translate & Adapt (no code) | – |

## 1. Judge.me "Mehr anzeigen" button
- **Problem:** the review "load more" button had Judge.me's own style and no visible hover.
- **Why the first hover didn't work:** the theme button doesn't change colour on hover. It slides two layers (`::before`, `::after`) in from the left (`translate(-100%)` → `translate(0)`, `.3s cubic-bezier(.75,0,.125,1)`, `::after` delayed `.175s`). Changing `#151515` → `#333` was barely visible.
- **Fix:** the same `::before`/`::after` slide on `.jm-load-more-pagination .jm-button--primary`, using the theme variables `--color-button-before`, `--color-button-hover-background`, `--color-button-hover-text` (with fallbacks). Border removed.
- **Key detail:** `position:relative; overflow:hidden; isolation:isolate` on the button keeps the layers inside the pill and behind the text.

## 2. Unit price on the product page
- **Problem:** "€39,50/KG" showed on its own line, large and uppercase.
- **Fix:** CSS scoped with `[id^="price-template--"][id$="__main"]` – only the price block of the main product section has this id, so collection cards, sticky add-to-cart bar, recently viewed and cart keep their style.
- Variant: one line below instead of inline → change `display: flex` to `display: block`.

## 3. "Fit & Sizing" tab only when a size chart is linked
- **Request:** Florian Knabl, 19.10.2026.
- **Problem:** the collapsible tab "Fit & Sizing" shows the page linked in metafield `custom.grosentabelle`. Without a linked page the tab still showed its heading with nothing underneath (books, treats, clickers, several T-shirts).
- **Fix:** in `snippets/product-information-blocks.liquid`, directly after `{%- when 'collapsible_tab' -%}`: build the tab content (`content` + `custom_liquid` + `page.content`); if it has no text **and** no `<img>`, `<iframe>`, `<video>` or Judge.me widget (`jdgm`) → `continue` (block skipped).
- The `jdgm` exception keeps the **Bewertungen** tab, which only contains the Judge.me widget (filled by JavaScript, so no text in Liquid).
- Generic: any collapsible tab that is completely empty is hidden; tabs with content are unchanged. Applies to DE and EN (same template).

**Test (DE + EN):**
- [ ] `/products/iq-unisex-t-shirt-slogan-schwarz` → no "Fit & Sizing", Bewertungen still there
- [ ] `/products/iq-dogsport-hose-unisex` → "Fit & Sizing" opens with the size chart
- [ ] `/en/…` for both
- [ ] One book + one treat product → no empty tab

## 4. English option names on merged products
- **Cause:** the merged products were created by CSV import. Option names and values (Farbe, Größe, Schwarz, Graublau, Olive) have no English translation, so `/en/` shows German.
- **Fix:** Translate & Adapt → English → Products → product → *Product options*: Farbe → Color, Größe → Size, Schwarz → Black, Graublau → Blue-grey, Olive → Olive. Sizes unchanged.
- Products: IQ Multifunktionsjacke 3.0 Damen, IQ Multifunktionsjacke 3.0 Unisex (+ every future merged product → added to the merge checklist).
- Safe: translations are display only – SKUs, Odoo sync and Judge.me are not affected. The colour-image code recognises `Color` as well.

## Rollback
- CSS: delete the block from Theme settings → Custom CSS.
- Liquid: remove the lines marked `[Hamza 2026-10-19]` from `snippets/product-information-blocks.liquid` (or restore the duplicated theme).
