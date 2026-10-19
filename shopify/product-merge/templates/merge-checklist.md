# Merge checklist – <product name>

Copy this file to `merges/<product>/README.md` for each new merge.

| | |
|---|---|
| New product | |
| Shopify ID | |
| Final URL | |
| Variants | |
| SKU pattern | |
| Odoo products | |
| Judge.me group | |

## Old products
| Product | Shopify ID | Handle | Reviews |
|---|---|---|---|
| | | | |

## Steps
- [ ] 1 Odoo: each SKU exists once (Archived filter on)
- [ ] 2 Shopify: import CSV built (same SKUs, stock empty, Draft)
- [ ] 2 Imported; category, vendor, description, channels, Variant Galerie
- [ ] 3 Odoo: imported by Shopify ID, one line per variant, Export stock, totals match
- [ ] 4 Judge.me group created, reviews visible in Preview
- [ ] 5 Old main handle → `-alt` (no redirect), new handle set, new Active, old Draft
- [ ] 5 Redirects created and tested (DE + EN)
- [ ] 6 Collections re-sorted
- [ ] 6 After a few days: old links removed in Odoo (with Florian)
