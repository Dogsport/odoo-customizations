# Rückgabegründe column only on returns

**Date:** 31.10.2026 · **Author:** Hamza Mohsin · **System:** Odoo 19 (Inventory) · **Status:** Staging ✅ · Production ✅

## Problem
The column **Rückgabegründe (Wareneingang)** (`x_studio_ruckgabegrunde_wareneingang`, stock.move, many2many → `x_ruckgabegrund`) showed in the Operations list of **every** transfer (receipts, deliveries), e.g. on WH1/IN/00058. The cells were empty, but the column header was always visible.

## Cause
In view **5643** "Odoo Studio: stock.picking.form customization" the field had `invisible="picking_type_id not in [116]"` (116 = Returns operation type). In a list, `invisible` only hides the **cells**, not the column.

## Find the view
```bash
psql -c "select id, name::text from ir_ui_view where arch_db::text ilike '%x_studio_ruckgabegrunde_wareneingang%';"
psql -At -c "select arch_db->>'en_US' from ir_ui_view where id = 5643;" | grep -n "ruckgabegrunde_wareneingang"
```
Same ID (5643) and same line 32 in staging and production.

## Change
Before:
```xml
<field widget="many2many_tags" optional="show" name="x_studio_ruckgabegrunde_wareneingang" options="{&quot;color_field&quot;:&quot;x_studio_color&quot;}" invisible="picking_type_id not in [116]"/>
```
After:
```xml
<field widget="many2many_tags" optional="show" name="x_studio_ruckgabegrunde_wareneingang" options="{&quot;color_field&quot;:&quot;x_studio_color&quot;}" column_invisible="parent.picking_type_id not in [116]"/>
```
Edited via Settings → Technical → Views → 5643 → Architecture (backup copied first).

## Check
- Receipt / delivery: column gone ✅
- Return (WH1/RET/…): column still visible ✅

**Rollback:** paste the backup XML back.
**Note:** module views (e.g. shopify_ept) must not be edited directly – changes would be overwritten on update.
