# Product merge: colour products → one product with variants

How we merge several Shopify products (one per colour) into **one product**
with the options **Farbe** and **Größe**, without breaking the Odoo stock sync,
the reviews or the old URLs.

Owner: Hamza Mohsin · First done: MFJ 3.0 Unisex (October 2026)

## How it works in one picture

```
ODOO (stays as it is)                  SHOPIFY
3 products, e.g.                        1 new product "IQ Multifunktionsjacke 3.0 Damen"
  Women Black   MJD3.BK.XS…4XL  ──┐      Farbe × Größe = 24 variants
  Women Blue    MJD3.BL.XS…4XL  ──┼──►   linked per variant by SKU
  Women Olive   MJD3.OL.XS…4XL  ──┘      (Emipro connector)

Old Shopify products (Schwarz, Olive, Blau) → Draft, never deleted
  - keep their reviews (Judge.me product group)
  - their URLs redirect to the new product
```

**Key rule:** Odoo is the source of truth for stock. The connector matches
Shopify variants to Odoo variants **by SKU (Internal Reference)**. That's why
the new product keeps **exactly the same SKUs** as the old ones, and nothing
is merged in Odoo.

## Steps (in this order)

| # | Step | File |
|---|---|---|
| 1 | Check Odoo: every SKU exists once | [steps/01-odoo-check.md](steps/01-odoo-check.md) |
| 2 | Build and import the new Shopify product (Draft) | [steps/02-shopify-new-product.md](steps/02-shopify-new-product.md) |
| 3 | Link the new product in Odoo and sync stock | [steps/03-odoo-connector.md](steps/03-odoo-connector.md) |
| 4 | Reviews: Judge.me product group | [steps/04-judgeme-reviews.md](steps/04-judgeme-reviews.md) |
| 5 | Go live: handles, status, redirects | [steps/05-go-live.md](steps/05-go-live.md) |
| 6 | After go-live: collections, checks, clean-up | [steps/06-after-go-live.md](steps/06-after-go-live.md) |
| – | Problems we hit and how we fixed them | [troubleshooting.md](troubleshooting.md) |

## Merges done

| Merge | Status | Notes |
|---|---|---|
| MFJ 3.0 Unisex | Live | [merges/mfj-3-0-unisex](merges/mfj-3-0-unisex/README.md) |
| MFJ 3.0 Damen | Built as Draft, go-live pending | [merges/mfj-3-0-damen](merges/mfj-3-0-damen/README.md) |

## Never do this
- Never **delete** the old products: their reviews disappear from the group.
- Never change **SKUs** of merged variants.
- In Odoo, never use **"Update/Export product"** or **"Unpublish"** on a merged product. Only **Export stock**.
- Never leave old and new products **Active at the same time** (duplicate listings).
