-- Read only: PGOPTIONS='-c default_transaction_read_only=on' psql -P pager=off -c "<query>"

-- 1. Outgoing operation types (find the id of "Delivery Orders", WH1)
SELECT t.id, t.code, to_jsonb(t)->'name'->>'en_US' AS name, w.code AS wh FROM stock_picking_type t LEFT JOIN stock_warehouse w ON w.id=t.warehouse_id WHERE t.code='outgoing' AND t.active ORDER BY t.id;

-- 2. Open deliveries without carrier (check BEFORE activating / before the one-off fill)
SELECT sp.name, sp.origin, sp.state, c.code AS country FROM stock_picking sp JOIN stock_picking_type t ON t.id=sp.picking_type_id LEFT JOIN res_partner p ON p.id=sp.partner_id LEFT JOIN res_country c ON c.id=p.country_id WHERE t.code='outgoing' AND sp.carrier_id IS NULL AND sp.state NOT IN ('done','cancel') ORDER BY sp.id;

-- 3. Deliveries filled by the rule (chatter note)
SELECT m.date, sp.name, left(regexp_replace(m.body,'<[^>]+>','','g'),120) AS note FROM mail_message m JOIN stock_picking sp ON sp.id=m.res_id AND m.model='stock.picking' WHERE m.body LIKE '%IQ: carrier set to%' ORDER BY m.date DESC LIMIT 30;
