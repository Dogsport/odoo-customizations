# Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Shopify shows "Ausverkauft" although Odoo has stock | Shopify variant linked to a duplicate Odoo product with the same SKU (0 stock) | Step 1: rename duplicate to `-ALT` + archive; delete wrong variant lines in the Odoo Shopify record; re-import the Shopify product by ID |
| Odoo log `INVALID_INVENTORY_ITEM` | A link points to a Shopify variant that was deleted | Delete that variant line (🗑) in the Odoo Shopify product record |
| Odoo queue "SKU missing" | Variant created in Shopify before the SKU existed in Odoo | Create the variant/SKU in Odoo first, then import again |
| New product stock lower than old products | Not all variants linked yet / export ran too early | Check Variants tab (one line per variant), run Export stock again |
| Small difference Shopify vs Odoo On Hand | Shopify gets on hand − reserved (open orders) | Normal |
| New product not found in Judge.me | Not published to a sales channel, or filter "In store: Yes" | Publish (Draft is fine), remove the filter, wait; else ask Judge.me support |
| New product shows 0 reviews in the group list | The list counts own reviews only | Check the product page in Preview |
| "Handle already in use" | Old product still has the handle | Rename old handle to `-alt` first |
| "Target can't redirect to another redirect" | Redirect exists from the target URL | Delete that redirect first |
| Extra variant after adding an option (e.g. Diensthundeführer / dunkelblau) | Shopify creates all combinations | Delete the combination that doesn't exist in Odoo |
| Odoo shows a different price after import (12,10 instead of 12,00) | Import copies the Shopify price into Odoo's Shopify pricelist | Fix the price in Shopify, then Import products by ID again |
| Shopify record in Odoo shows only one "Product Template" | The field holds one product only | Check the Variants tab; each line is linked by SKU |
| Redirect doesn't work | The old product is still Active at that URL | Set the old product to Draft; test in a private window |
| New product at the end of a collection | Collection sorted manually | Drag it up in each collection |

## Example: IQ Mini keychain (16.10.2026)
4 Odoo variants for 2 SKUs: the connector had created duplicates
("IQ Mini-Apportierholz Schlüsselanhänger" without attribute). Fixed by renaming
them to `IQD-APH-HETZ-ALT` / `IQD-APH-LIGHT-ALT`, deleting the 3 wrong lines and
re-importing Shopify product 12141783613704.
