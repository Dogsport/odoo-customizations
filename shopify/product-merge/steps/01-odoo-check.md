# Step 1: Odoo check – every SKU exists once

**Why:** the Emipro connector links Shopify variants to Odoo variants by SKU.
If a SKU exists twice in Odoo, the connector may pick the wrong (empty) product,
and Shopify shows "Ausverkauft" (sold out).

## Do
1. Odoo → Sales (or Inventory) → Products → **Product Variants** (list view).
2. Search **Internal Reference** with the SKU prefix, e.g. `MJD3` or `MFJ3`.
3. Turn on the **Archived** filter too.
4. Count: the number of rows must equal the number of variants you will create
   (e.g. 3 colours × 8 sizes = 24). Each SKU exactly **once**.

## If a SKU exists twice
- Find the duplicate: usually 0 stock, no attribute values, created by the connector.
- Check its smart buttons (Sold, In/Out). Never delete; it may have history.
- Rename its Internal Reference to `…-ALT` and **archive** it.

## Don't
- Don't merge the Odoo products. 3 Odoo products behind 1 Shopify product is correct.
- Don't create new fields in Odoo for this.
