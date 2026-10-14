# DHL Parcel DE — Odoo automation documentation

**Updated:** 14 October 2026  
**Environment:** Odoo 19 Staging, IQ Dogsport GmbH  
**Deployment:** Documentation only; GitHub is not connected to an Odoo deployment pipeline.

## Current status: three active automations

The previous split domestic/international assignment has been consolidated. Fresh German and international sales orders and their returns were tested successfully in Staging on 14 October 2026.

| Status | Automation | Model | Purpose |
|---|---|---|---|
| **Active** | Combined DHL Shipping Method (**new ID to verify**) | `sale.order` | Default DHL Domestic for DE, DHL International for eligible non-DE test orders, provided no method is selected |
| **Active** | [ID 66 — Sync DHL Carrier to Delivery](https://iq-dogsport-staging-38965432.dev.odoo.com/odoo/automations/66) | `stock.picking` | Make the outgoing transfer use the selected sales order carrier |
| **Active** | [ID 64 — DHL – Automatic Return Receiver](https://iq-dogsport-staging-38965432.dev.odoo.com/odoo/automations/64) | `stock.picking` | Auto-set German return Receiver ID `deu`, preserving manual receiver changes |
| Active view (not automation) | IQ DHL – Conditional Receiver Buttons, view **6113** | `stock.picking` | Toggle Get Receivers / Change Receiver button based on receiver and tracking |
| **Archived** | [ID 8 — Shipping add](https://iq-dogsport-staging-38965432.dev.odoo.com/odoo/automations/8) | `sale.order` | Old Germany-only fixed assignment; replaced by combined rule |
| **Archived** | [ID 65 — Shipping add – DHL International](https://iq-dogsport-staging-38965432.dev.odoo.com/odoo/automations/65) | `sale.order` | Old non-DE fixed assignment; replaced by combined rule |
| **Archived** | ID 7 — Auto Set Carrier | `stock.picking` | Obsolete fixed-carrier action; previously caused delivery carrier to disagree with sales order |

**Important:** The new combined automation ID and actual saved source code have not been exported to this documentation yet. All reference code below is clearly labeled and must be verified against Odoo before any Production implementation.

## 1. Combined Sales Order automation

The combined automation replaced IDs 8 and 65 to simplify the carrier selection logic.

- Model: `sale.order`
- Trigger: `On create`
- Domain: Delivery Method empty, Delivery Address country set
- If country `DE`: choose `DHL Parcel DE`, product `V01PAK`
- Otherwise in Staging: choose `DHL Parcel DE – International`, product `V53WPAK`
- Do **not** overwrite an explicitly selected delivery method.

### Reference example (not exported final code)

```python
orders = records or record or env['sale.order']
for order in orders:
    if order.carrier_id:
        continue
    country = order.partner_shipping_id.country_id
    if not country:
        continue
    carrier_name = (
        'DHL Parcel DE' if country.code == 'DE'
        else 'DHL Parcel DE – International'
    )
    carriers = env['delivery.carrier'].search([
        ('name', '=', carrier_name),
        ('delivery_type', '=', 'dhl_parcel_de'),
    ])
    if len(carriers) != 1:
        log('DHL carrier not unique: %s' % carrier_name, level='warning')
        continue
    order.write({'carrier_id': carriers.id})
```

**Production safeguard:** A country-based default is not the same as the customer's shipping selection. A Shopify-imported order with an empty carrier field may still represent a customer who selected GLS. Preserve the customer's real selected service; restrict the rule to supported shipping destinations and business rules. The UK direct-shipping policy also needs consideration.

## 2. Automation 66 — outgoing transfer carrier synchronization

Original failure: for Austrian Sales Order `S00462`, `sale.order.carrier_id` was DHL International, but transfer `WH1/OUT/06242` had GLS Germany. Odoo stock rule carrier propagation was enabled, and the general default carrier was empty. The old fixed-carrier transfer automation (ID 7) was archived.

Automation 66 synchronizes the DHL method selected on a sales order with the outgoing transfer and leaves GLS orders untouched.

### Previously discussed reference code (not the verified saved code)

```python
pickings = records or record or env['stock.picking']
for picking in pickings:
    if picking.picking_type_id.code != 'outgoing':
        continue
    if picking.state in ('done', 'cancel'):
        continue
    if picking.carrier_tracking_ref:
        continue
    so = picking.sale_id
    if not so or not so.carrier_id:
        continue
    if so.carrier_id.delivery_type != 'dhl_parcel_de':
        continue
    if picking.carrier_id.id != so.carrier_id.id:
        picking.write({'carrier_id': so.carrier_id.id})
        log('Carrier synchronized: %s -> %s' %
            (picking.name, so.carrier_id.name), level='info')
```

This example must be compared with the saved action because the full final implementation was not independently exported.

## 3. Automation 64 — German DHL Return Receiver

- Model: `stock.picking`
- Trigger: `On create and edit`
- When updating: Carrier, Contact, Operation Type
- Action: Execute Code
- For an incoming German DHL return with no receiver selected, assign `deu`.
- Preserve any manually selected Receiver ID; skip completed/cancelled returns and transfers with other carriers.

### Documented implementation (confirm exact saved version)

```python
pickings = records or record or env['stock.picking']
for picking in pickings:
    if not picking.is_dhl_return:
        continue
    if picking.picking_type_id.code != 'incoming':
        continue
    if picking.carrier_id.delivery_type != 'dhl_parcel_de':
        continue
    if picking.state in ('done', 'cancel'):
        continue
    if picking.dhl_return_receiver_id:
        continue
    if picking.partner_id.country_id.code == 'DE':
        picking.write({'dhl_return_receiver_id': 'deu'})
        log('DHL receiver deu assigned to %s' %
            picking.name, level='info')
```

`is_dhl_return` is a non-stored computed field and is checked in Python, not in the automation domain. The guard for an existing receiver ID is essential for manual overrides.

## 4. Receiver buttons — inherited view 6113

The view is **not another automation**. It extends BrowseInfo's `stock.picking.form.inherit.dhl` (parent view 6081 in Staging) using extension mode, no website binding. Both Get Receivers and Change Receiver call `action_open_return_receiver_wizard`.

Keep the following `invisible` attribute expressions on a **single line** inside the saved XML view:

```python
# Get Receivers button
not is_dhl_return or state in ('done', 'cancel') or carrier_tracking_ref or dhl_return_receiver_id

# Change Receiver button
not is_dhl_return or state in ('done', 'cancel') or carrier_tracking_ref or not dhl_return_receiver_id
```

## 5. Verified Staging tests

| Test | Evidence | Result |
|---|---|---|
| Italy outbound | `S00456` / `WH1/OUT/06236` | International `V53WPAK` label generated after carrier correction |
| Austria outbound | `S00464` / `WH1/OUT/06244` | DHL International label generated, 13 October |
| Germany outbound | `S00465` / `WH1/OUT/06245` | DHL domestic label generated, 13 October |
| Combined rule, 14 October | New German and international test orders | Both automatically selected correct carrier on sales order and transfer |
| German return | Test return in Staging | Receiver `deu` automatically populated; return processed without manual receiver change |
| International return | Test return in Staging | Odoo requested manual Receiver ID; user selected a receiver and tested return successfully |
| Manual German override | `WH1/RET/00529` | Manually changed `deu` to `deu_ggp`; it persisted |

Sandbox label PDFs stamped **MUSTER** are test results, not live postage. International return testing does not prove that IQ Dogsport has corresponding international return receivers in its live DHL agreement.

## 6. DHL Business Customer Portal — 14 October

Under **Receiver DHL Retoure Online**, the business account currently displays **one receiver only**:

- Germany: `deu`
- IQ Dogsport GmbH, Langenwiesen 2, 85276 Pfaffenhofen

Under **Receiver DHL Retoure Selbstzahler**, there is a separate German receiver:

- Germany: `deu_SZ`
- The old Baar-Ebenhausen address was corrected to Langenwiesen 2, 85276 Pfaffenhofen.

No additional country-specific international Retoure Online receivers were shown in the portal screenshot.

**Business policy:** The **customer pays return shipping**, not IQ Dogsport. Do not assume a DHL label created with IQ Dogsport's business account bills the customer directly. Management will decide later whether IQ Dogsport wants to offer a customer-paid international label workflow, after DHL confirms how it would be charged.

## 7. Export the saved action code to finish the technical archive

Run this in the read-only Staging Odoo Shell and paste the output into this documentation. Note: the combined automation's ID must still be identified.

```python
for aid in [64, 66]:
    a = env['base.automation'].sudo().browse(aid)
    print(a.id, a.name, 'active:', a.active, 'trigger:', a.trigger)
    for action in a.action_server_ids:
        print('ACTION:', action.name, 'TYPE:', action.state)
        if action.state == 'code':
            print(action.code)

# Find the newly combined sale.order automation ID by its visible name.
for a in env['base.automation'].sudo().search([
    ('model_id.model', '=', 'sale.order'), ('active', '=', True)
]):
    print(a.id, a.name, a.trigger)
```

## 8. Production and Shopify safeguards

Production has not been configured simply by testing Staging. Before live deployment, verify contracts, credentials, billing numbers, eligible destinations, Shopify carrier mapping, return cost responsibility, Receiver IDs and the exact saved automation code. Old automation IDs may be different in Production. Keep archived rules for rollback and perform authorized DE, international, GLS and return tests before rollout.

---

**Documentation source:** IQ Dogsport Odoo screenshots and Staging tests, 13–14 October 2026.  
**Companion PDF:** `IQ_Dogsport_DHL_Automations_Updated_2026-10-14.pdf`
