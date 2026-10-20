# Defekt- & Reparaturfälle – Scrap Orders Integration

**20 October 2026 · Production: iq-dogsport.odoo.com (live) · Staging: iq-dogsport-staging-38965432.dev.odoo.com**
**Prepared for Hamza Mohsin, IQ Dogsport GmbH**

## 1. Summary

Extended the existing Defekt- & Reparaturfälle (Defect & Repair Case) tracking system to also cover Odoo's native Scrap Orders feature. Goal: when defective stock is scrapped into the Defektlager location, a claim case is automatically created so the Production Partner can be billed for the loss, using the exact same Payer / Claim Status / Production Partner / Cost mechanics already in place for Returns and Repairs — no parallel system, no duplicated logic.

Built and tested in staging first (test records SP/00001–00011 on "IQ Performance Leggings," several size variants), then rolled out to production (live claims SP/00001–00003 against Holfelder GmbH, Defektlager).

## 2. New fields

### 2.1 Scrap Orders (`stock.scrap`)

| Field name | Label | Type | Note |
|---|---|---|---|
| `x_studio_payer` | Payer | selection | Production Partner / IQ Dogsport / Customer — chosen by staff on the Scrap Order itself |
| (related) | Available Stock | related: Product → Quantity On Hand | Live stock check while picking a product to scrap |

### 2.2 Case model (`x_iq_service_case`)

| Field name | Label | Type | Note |
|---|---|---|---|
| `x_studio_source_scrap_order` | Source Scrap Order | many2one → stock.scrap | Links the case back to the originating Scrap Order |
| `x_studio_scrap_reason` | Scrap Reason | char | Copied from the Scrap Order's Scrap Reason tags |
| (related) | Scrapped Quantity | related: Source Scrap Order → Quantity (`scrap_qty`) | Shows how many units were disposed, without opening the Scrap Order |

## 3. Automation rule — "IQ – Scrap zu Fall"

- **Model:** Scrap
- **Trigger:** On create and edit
- **Apply on:** Status = Done
- **Before Update Domain:** Match all records
- **When updating:** Status

```python
try:
    DEFECT_LOCATIONS = ['Defektlager', 'Defektlager - Kunde']
    PAYER_MAP = {
        'Production Partner': 'supplier',
        'IQ Dogsport': 'iq',
        'Customer': 'customer',
    }

    if record.state == 'done' and record.scrap_location_id.name in DEFECT_LOCATIONS:
        Case = env['x_iq_service_case']
        company = env.company
        product = record.product_id

        # Same vendor-detection logic as the production 'guess_supplier' function
        suppliers = env['res.partner']
        for seller in product.seller_ids:
            if seller.company_id and seller.company_id != company:
                continue
            if seller.product_id and seller.product_id != product:
                continue
            partner = seller.partner_id.commercial_partner_id
            if partner == company.partner_id:
                continue
            suppliers |= partner
        production_partner = suppliers if len(suppliers) == 1 else env['res.partner']

        amount = 0.0
        if production_partner:
            seller = product._select_seller(partner_id=production_partner, quantity=record.scrap_qty)
            if seller:
                amount = seller.price * record.scrap_qty

        vals = {
            'x_studio_source_scrap_order': record.id,
            'x_product_id': product.id,
            'x_customer_id': False,
            'x_supplier_id': production_partner.id or False,
            'x_payer': PAYER_MAP.get(record.x_studio_payer, False),
            'x_cost_total': amount,
            'x_studio_scrap_reason': ', '.join(record.scrap_reason_tag_ids.mapped('name')),
            'x_company_id': company.id,
            'x_claim_status': 'not_submitted',
        }

        existing = Case.search([('x_studio_source_scrap_order', '=', record.id)], limit=1)
        if existing:
            existing.write(vals)
            case = existing
        else:
            case = Case.create(vals)

        already = env['ir.attachment'].search([
            ('res_model', '=', 'x_iq_service_case'), ('res_id', '=', case.id),
        ]).mapped('name')
        for att in env['ir.attachment'].search([
            ('res_model', '=', 'stock.scrap'), ('res_id', '=', record.id),
        ]):
            if att.name not in already:
                env['ir.attachment'].create({
                    'name': att.name, 'type': att.type, 'datas': att.datas,
                    'res_model': 'x_iq_service_case', 'res_id': case.id, 'mimetype': att.mimetype,
                })
except Exception as e:
    record.message_post(body="Scrap-to-Case automation error: %s" % str(e))
```

Production Partner detection mirrors the existing `guess_supplier()` function already used by "IQ - Push Claim Total to Case" (filters by company, by exact product variant, collapses to `commercial_partner_id`, requires exactly one match) — no new vendor-detection logic was invented.

## 4. Modified existing compute fields

Both fields below already existed and are used across Repair- and Return-based cases. Each was extended with one additional branch so Scrap-originated cases are treated consistently — nothing changed for existing Repair/Return cases.

### 4.1 `x_decision` ("Decision After Review")

Dependencies: `x_repair_id, x_return_id, x_return_id.x_studio_entscheidung_nach_prufung, x_studio_source_scrap_order`

```python
for record in self:
    if record.x_repair_id:
        record['x_decision'] = 'Reparatur'
    elif record.x_return_id.x_studio_entscheidung_nach_prufung == 'Defektlager':
        record['x_decision'] = 'Defektlager'
    elif record.x_studio_source_scrap_order:
        record['x_decision'] = 'Defektlager'
    else:
        record['x_decision'] = False
```

### 4.2 `x_lager_id` ("Lager")

Was a simple Related Field mirroring `x_return_id.location_dest_id`. Converted to a custom compute so it also works for Scrap-originated cases, while preserving identical behavior for Return-based cases.

Dependencies: `x_return_id, x_return_id.location_dest_id, x_studio_source_scrap_order, x_studio_source_scrap_order.scrap_location_id`

```python
for record in self:
    if record.x_return_id:
        record['x_lager_id'] = record.x_return_id.location_dest_id.id
    elif record.x_studio_source_scrap_order:
        record['x_lager_id'] = record.x_studio_source_scrap_order.scrap_location_id.id
    else:
        record['x_lager_id'] = False
```

## 5. How it works end to end

1. Staff scraps a defective product via Inventory → Operations → Scrap Orders, picking Scrap Location = "Defektlager" or "Defektlager - Kunde," and selecting a Payer.
2. On Validate (Draft → Done), the automation fires, identifies the Production Partner from the product's vendor pricelist, computes cost as unit price × scrapped quantity, and creates (or updates) a case.
3. The case appears in Defekt- & Reparaturfälle with Claim Status = Not Submitted, ready to be worked the same way as any Return- or Repair-based claim (submit, mark Accepted/Rejected, etc.).
4. Decision and Lager columns automatically show "Defektlager," and Scrapped Quantity shows the disposed unit count — all without a parallel display system.

## 6. Known limitations / open items

- A single Scrap Order can only hold one product variant. A defect spanning multiple sizes/variants requires one Scrap Order (and resulting case) per variant — there is currently no mechanism to group several Scrap Orders under one combined claim.
- Scrap-originated cases never populate `x_repair_id` / `x_return_id`, so Decision is always either "Defektlager" or blank (never "Reparatur") for this path — expected, since scrapped goods aren't repaired.
- Old test records in both staging and production (SP/00001–00011 staging; SP/00001–00003 production) should be reviewed and either kept as real claims or cleaned up, depending on which were genuine defects vs. pure tests.

## 7. Test results

**Staging:** SP/00001–00011 (IQ Performance Leggings, multiple size variants) — Production Partner, cost, Claim Status, Decision, Lager, and Scrapped Quantity all confirmed correct end to end.

**Production:** SP/00001–00003 (live, Holfelder GmbH, Defektlager) — 606 units, €12,152.70 total claim value, correctly grouped and visible in the "1. To submit" favourite alongside existing Return/Repair claims.
