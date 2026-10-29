# Odoo 19 - Automation Rule (PRODUCTION since 29.10.2026)
# Name:          IQ - Return: DHL carrier for Germany
# Model:         Transfer (stock.picking)
# Trigger:       On create and edit
# Apply on:      [("picking_type_code", "=", "incoming"), ("return_id", "!=", False),
#                 ("carrier_id", "=", False), ("state", "not in", ["done", "cancel"])]
# When updating: Carrier, Contact, Type of Operation, Return of, Status
# Action:        Execute Code (below)
#
# Sets DHL Parcel DE + return receiver "deu" on open returns of German customers.
# "On create" alone did not work: Odoo fills "Return of"/state only after create.
# The receiver is set here as well because "DHL - Automatic Return Receiver" does not
# fire while the return is still being created.

carrier = env["delivery.carrier"].search([("name", "=", "DHL Parcel DE")], limit=1)
for picking in records:
    if picking.carrier_id or not carrier:
        continue
    partner = picking.partner_id
    country = partner.country_id or partner.commercial_partner_id.country_id
    if country.code != "DE":
        continue
    vals = {"carrier_id": carrier.id}
    if not picking.dhl_return_receiver_id:
        vals["dhl_return_receiver_id"] = "deu"
    picking.write(vals)
    picking.message_post(body="IQ Return: carrier set to %s, return receiver %s (customer in Germany)." % (carrier.name, picking.dhl_return_receiver_id or "-"))
