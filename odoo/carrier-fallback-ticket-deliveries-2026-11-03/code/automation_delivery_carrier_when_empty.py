# Odoo 19 - Automation Rule
# Name:          IQ - Delivery: carrier when empty (DE -> DHL, else GLS)
# Model:         Transfer (stock.picking)
# Trigger:       On create and edit
# Apply on:      Operation Type = "IQ Dogsport Main Warehouse: Delivery Orders"
#                AND Carrier is not set AND Status not in Done/Cancelled
#                code: [("picking_type_id", "=", <Delivery Orders id>), ("carrier_id", "=", False), ("state", "not in", ["done", "cancel"])]
# When updating: Carrier, Contact, Operation Type, Status
# Action:        Execute Code (below)
#
# Fallback for deliveries that are NOT created by a sales order (Helpdesk Replace/exchange,
# manual deliveries). Never overwrites an existing carrier. Skips POS transfers.

dhl = env["delivery.carrier"].search([("name", "=", "DHL Parcel DE")], limit=1)
gls = env["delivery.carrier"].search([("name", "=", "GLS Germany")], limit=1)
has_pos = "pos_order_id" in env["stock.picking"]._fields
for picking in records:
    if picking.carrier_id or picking.picking_type_code != "outgoing":
        continue
    if has_pos and picking.pos_order_id:
        continue
    partner = picking.partner_id
    country = partner.country_id or partner.commercial_partner_id.country_id
    if not country:
        continue
    carrier = dhl if country.code == "DE" else gls
    if not carrier:
        continue
    picking.write({"carrier_id": carrier.id})
    picking.message_post(body="IQ: carrier set to %s (delivery country %s, delivery not created from a sales order)." % (carrier.name, country.code))
