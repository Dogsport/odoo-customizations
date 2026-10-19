# Step 3: Link the new product in Odoo and sync stock

## How the connector works
The connector keeps a **link row per Shopify variant**, each pointing to one
Odoo variant (matched by SKU). Before the old links are removed, one Odoo
variant has **two** links:

```
Odoo variant MJD3.OL.M (stock)
  ├─ link → OLD Shopify product "Damen Olive", variant M
  └─ link → NEW Shopify product "Damen", variant Olive / M
```

**Export stock** sends each Odoo variant's free stock (on hand − reserved)
to **all** its links. So old and new products show the same numbers during
the changeover.

## Do
1. Copy the new product's ID from the Shopify admin URL (`…/products/1234567890`).
2. Odoo → **Shopify → Operations → Import products** → Product IDs = that ID → Execute.
   If needed: Queues → Product Data Queue → **Process**.
3. Odoo → **Shopify → Products** → search the Shopify Template Id → **Variants** tab:
   - one line per variant (e.g. 24)
   - each line → the right Odoo variant with the same SKU
4. **Operations → Export stock**. Check **Logs** for errors.
5. Shopify: the new product's total stock = the old products' total.

## Notes
- "Product Template" on the record shows only one Odoo product name. It's just a label.
- Line titles may still show old product names. That's cosmetic, don't "fix" it with an export.
- Shopify shows **on hand − reserved**, so small differences to Odoo "On Hand" are normal.
