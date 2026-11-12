-- Read only: psql -c "<query>"

-- 1. Is a transfer a "real" return (return_id) or created from a ticket (empty)?
SELECT sp.name, sp.return_id, sp.carrier_tracking_ref, sp.sale_id, sp.dhl_return_receiver_id FROM stock_picking sp WHERE sp.name = 'WH1/RET/00701';

-- 2. Carrier technical name (must be dhl_parcel_de) and Returns operation type link
SELECT id, name, delivery_type FROM delivery_carrier WHERE name ILIKE '%DHL%';
SELECT id, name->>'en_US' AS name, return_picking_type_id FROM stock_picking_type WHERE code = 'outgoing' AND active;

-- 3. Return labels created without outbound DHL shipment (chatter note)
SELECT m.date, sp.name, left(regexp_replace(m.body,'<[^>]+>','','g'),140) AS note FROM mail_message m JOIN stock_picking sp ON sp.id = m.res_id AND m.model = 'stock.picking' WHERE m.body LIKE '%created without outbound DHL shipment%' ORDER BY m.date DESC LIMIT 30;

-- Source lookup in the BrowseInfo connector (read only):
-- cd ~/src/user/bi_delivery_dhl_de_connector && grep -rn "no validated outbound DHL shipment" .
--   models/stock_picking.py   action_open_return_receiver_wizard  (button "Get Receivers")
--   models/delivery_carrier.py dhl_parcel_de_get_return_label     (Print Return Label)
--   models/dhl_request.py:753 create_return_shipment(carrier, picking)  -> no check, used by our action
