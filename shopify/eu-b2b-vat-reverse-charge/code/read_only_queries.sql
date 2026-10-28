-- All read only. Run on Odoo.sh shell with:
-- PGOPTIONS='-c default_transaction_read_only=on' psql -P pager=off -c "<query>"

-- 1. Emipro tax setting (decides whether Odoo or Shopify taxes are used on import)
SELECT id, name, apply_tax_in_order FROM shopify_instance_ept;

-- 2. VIES check switch per company
SELECT id, name, vat_check_vies FROM res_company;

-- 3. EU orders since 01.04 where the customer has a VAT ID but VAT was charged
SELECT so.name, so.date_order::date, c.code AS country, cp.vat, cp.vies_valid,
       fp.name->>'en_US' AS fiscal_position, so.amount_untaxed, so.amount_tax, so.amount_total
FROM sale_order so
JOIN res_partner p ON p.id = so.partner_invoice_id
JOIN res_partner cp ON cp.id = p.commercial_partner_id
LEFT JOIN res_partner sh ON sh.id = so.partner_shipping_id
LEFT JOIN res_country c ON c.id = sh.country_id
LEFT JOIN account_fiscal_position fp ON fp.id = so.fiscal_position_id
WHERE so.name LIKE '#IQD-%' AND so.date_order >= '2026-04-01' AND so.state <> 'cancel'
  AND coalesce(cp.vat,'') <> '' AND c.code <> 'DE'
ORDER BY so.amount_tax DESC, so.date_order;

-- 4. Orders touched by the new automations (chatter notes)
SELECT m.date, so.name, left(regexp_replace(m.body, '<[^>]+>', '', 'g'), 160) AS note
FROM mail_message m JOIN sale_order so ON so.id = m.res_id AND m.model = 'sale.order'
WHERE m.body LIKE '%IQ VAT:%' ORDER BY m.date DESC LIMIT 50;

-- 5. Shopify vs Odoo totals after the Dynamic switch (compare with Shopify admin)
SELECT so.name, so.date_order::date, c.code, fp.name->>'en_US' AS fiscal_position,
       so.amount_untaxed, so.amount_tax, so.amount_total
FROM sale_order so
LEFT JOIN res_partner sh ON sh.id = so.partner_shipping_id
LEFT JOIN res_country c ON c.id = sh.country_id
LEFT JOIN account_fiscal_position fp ON fp.id = so.fiscal_position_id
WHERE so.name LIKE '#IQD-%' AND so.date_order >= '2026-10-28 17:00'
ORDER BY so.date_order;
