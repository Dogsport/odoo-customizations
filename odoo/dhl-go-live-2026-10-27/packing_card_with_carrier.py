eu_country_codes = [
    'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR',
    'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL',
    'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE'
]

lang = env.user.lang or 'en_US'
is_de = lang.startswith('de')

if is_de:
    txt_order = 'Bestellung'
    txt_customer = 'Kunde'
    txt_address = 'Lieferadresse'
    txt_products = 'Produkte'
    txt_total_qty = 'Gesamtmenge'
    txt_articles = 'Artikel'
    txt_units = 'Stk.'
    txt_customs = 'Zolldokumente erforderlich'
    txt_no_products = 'Keine Produktzeilen gefunden.'
    txt_shipping_date = 'Versanddatum'
    txt_country_missing = 'Land fehlt - Adresse prüfen'
    txt_note = 'Bestellnotiz'
    txt_picking_note = 'Packhinweis'
    txt_paid = 'BEZAHLT'
    txt_unpaid = 'NICHT BEZAHLT'
    txt_partial = 'TEILZAHLUNG'
else:
    txt_order = 'Order'
    txt_customer = 'Customer'
    txt_address = 'Delivery address'
    txt_products = 'Products'
    txt_total_qty = 'Total quantity'
    txt_articles = 'Articles'
    txt_units = 'Units'
    txt_customs = 'Customs papers required'
    txt_no_products = 'No product lines found.'
    txt_shipping_date = 'Shipping date'
    txt_country_missing = 'Country missing - check address'
    txt_note = 'Order note'
    txt_picking_note = 'Packing note'
    txt_paid = 'PAID'
    txt_unpaid = 'NOT PAID'
    txt_partial = 'PARTIAL'


# ---------------------------------------------------------
# CUSTOMER / COUNTRY
# ---------------------------------------------------------

partner = record.partner_id

country = partner.country_id.name if partner.country_id else ''
country_code = partner.country_id.code if partner.country_id else ''

country_missing = not bool(country_code)

is_eu = False

if country_code:
    is_eu = country_code in eu_country_codes


# ---------------------------------------------------------
# COLORS / EU STATUS
# ---------------------------------------------------------

alert_color = '#d00000'
green_color = '#087f5b'
orange_color = '#f0ad4e'

if country_missing:
    border_color = orange_color
    order_color = orange_color
    badge_text = 'CHECK'

elif is_eu:
    border_color = '#dddddd'
    order_color = green_color
    badge_text = 'EU'

else:
    border_color = alert_color
    order_color = alert_color
    badge_text = 'NON-EU'


# ---------------------------------------------------------
# SHIPPING DATE
# ---------------------------------------------------------

ship_date = ''

ship_dt = record.date_done or record.scheduled_date

if ship_dt:
    ship_date = (
        ship_dt.strftime('%d.%m.%Y %H:%M:%S')
        if is_de
        else ship_dt.strftime('%Y-%m-%d %H:%M:%S')
    )


shipping_html = ''

if ship_date:
    shipping_html = """
        <div style="flex:0.7;min-width:0;">
            <div style="
                font-size:11px;
                font-weight:800;
                color:#666666;
                text-transform:uppercase;
            ">
                %s
            </div>

            <div style="
                font-size:15px;
                line-height:1.35;
                font-weight:900;
                margin-top:3px;
                color:%s;
            ">
                %s
            </div>
        </div>
    """ % (
        txt_shipping_date,
        order_color,
        ship_date
    )


# ---------------------------------------------------------
# SALE ORDER
# ---------------------------------------------------------

# ---------------------------------------------------------
# SALES ORDER / SHOPIFY CUSTOMER NOTE
# ---------------------------------------------------------

so = record.sale_id

order_note = ''

if so and so.note:
    note_txt = so.note.strip()

    if note_txt:
        order_note = note_txt


note_html = ''

if order_note:
    note_html = """
        <div style="
            margin:8px 0 4px 0;
            padding:9px 12px;
            border:1px solid #f2dfae;
            border-left:4px solid #f0ad4e;
            border-radius:8px;
            background:#fffdf5;
        ">
            <span style="
                font-size:10px;
                font-weight:800;
                color:#b07d00;
                text-transform:uppercase;
                letter-spacing:0.8px;
                margin-right:8px;
            ">
                %s
            </span>

            <span style="
                font-size:13.5px;
                line-height:1.4;
                font-weight:700;
                color:#222222;
                overflow-wrap:anywhere;
            ">
                %s
            </span>
        </div>
    """ % (
        txt_note,
        order_note
    )


# ---------------------------------------------------------
# DELIVERY / PICKING NOTE
# This is the "Note" tab directly on the delivery.
# ---------------------------------------------------------

picking_note = (record.note or '').strip()

picking_note_html = ''

if picking_note:
    picking_note_html = """
        <div style="
            margin:8px 0 4px 0;
            padding:9px 12px;
            border:1px solid #f2dfae;
            border-left:4px solid #f0ad4e;
            border-radius:8px;
            background:#fffdf5;
        ">
            <span style="
                font-size:10px;
                font-weight:800;
                color:#b07d00;
                text-transform:uppercase;
                letter-spacing:0.8px;
                margin-right:8px;
            ">
                %s
            </span>

            <span style="
                font-size:13.5px;
                line-height:1.4;
                font-weight:700;
                color:#222222;
                overflow-wrap:anywhere;
            ">
                %s
            </span>
        </div>
    """ % (
        txt_picking_note,
        picking_note
    )


# ---------------------------------------------------------
# PAYMENT STATUS
# ---------------------------------------------------------

pay_badge = ''

if so:

    posted = so.invoice_ids.filtered(
        lambda m: m.state == 'posted'
    )

    if posted.filtered(
        lambda m: m.payment_state in (
            'paid',
            'in_payment',
            'reversed'
        )
    ):
        pay_text = txt_paid
        pay_color = green_color
        pay_font = '#ffffff'

    elif posted.filtered(
        lambda m: m.payment_state == 'partial'
    ):
        pay_text = txt_partial
        pay_color = orange_color
        pay_font = '#3d2b00'

    else:
        pay_text = txt_unpaid
        pay_color = alert_color
        pay_font = '#ffffff'


    pay_badge = """
        <div style="
            background:%s;
            border:2px solid %s;
            color:%s;
            padding:4px 14px;
            border-radius:999px;
            font-weight:900;
            font-size:13px;
            letter-spacing:0.3px;
            text-align:center;
            white-space:nowrap;
        ">
            %s
        </div>
    """ % (
        pay_color,
        pay_color,
        pay_font,
        pay_text
    )


# ---------------------------------------------------------
# CARRIER BADGE (DHL / GLS)
# Only real label carriers count. Price-only carriers
# (e.g. "DHL Paket", "GLS Deutschland", "GLS EU") or an
# empty carrier show an orange "check carrier" warning.
# ---------------------------------------------------------

carrier = record.carrier_id
carrier_type = carrier.delivery_type if carrier else ''

if carrier_type == 'dhl_parcel_de':
    carrier_text = 'DHL'
    carrier_bg = '#ffcc00'
    carrier_fg = '#d40511'
    carrier_border = '#d40511'

elif carrier_type == 'gls_germany':
    carrier_text = 'GLS'
    carrier_bg = '#061ab1'
    carrier_fg = '#ffffff'
    carrier_border = '#061ab1'

else:
    carrier_text = 'CARRIER PRÜFEN' if is_de else 'CHECK CARRIER'
    carrier_bg = '#fff3cd'
    carrier_fg = '#8a5a00'
    carrier_border = orange_color


carrier_badge = """
    <div style="
        background:%s;
        border:2px solid %s;
        color:%s;
        padding:4px 16px;
        border-radius:999px;
        font-weight:900;
        font-size:15px;
        letter-spacing:0.5px;
        text-align:center;
        white-space:nowrap;
    ">
        %s
    </div>
""" % (
    carrier_bg,
    carrier_border,
    carrier_fg,
    carrier_text
)


# ---------------------------------------------------------
# ADDRESS
# ---------------------------------------------------------

address_parts = []

for part in [
    partner.street,
    partner.street2
]:
    if part:
        address_parts.append(part)


city_line = " ".join(
    filter(
        None,
        [
            partner.zip or "",
            partner.city or ""
        ]
    )
)

if city_line:
    address_parts.append(city_line)

if country:
    address_parts.append(country)


address_html = '<br/>'.join(address_parts)


# ---------------------------------------------------------
# PRODUCTS
# ---------------------------------------------------------

product_lines = []

total_qty = 0
article_count = 0


for move in record.move_ids:

    product = move.product_id

    qty = move.product_uom_qty or 0


    if not product or qty <= 0:
        continue


    sku = product.default_code or ''


    # Do not show Shopify technical/custom product
    if sku == 'shopifycustomstorableproduct':
        continue


    total_qty += qty
    article_count += 1


    image_url = (
        "/web/image/product.product/%s/image_128"
        % product.id
    )


    qty_display = (
        int(qty)
        if qty == int(qty)
        else qty
    )


    # Quantity highlight when more than 1
    if qty > 1:

        qty_border = '#f0ad4e'
        qty_bg = '#fff3cd'
        qty_color = '#8a5a00'

    else:

        qty_border = '#dddddd'
        qty_bg = '#ffffff'
        qty_color = '#111111'


    # -----------------------------------------------------
    # IMPORTANT:
    # Product Internal Notes are intentionally NOT shown.
    #
    # OLD CODE REMOVED:
    #
    # product.product_tmpl_id.description
    #
    # -----------------------------------------------------


    product_lines.append("""
        <div style="
            display:flex;
            align-items:center;
            gap:12px;
            padding:10px 12px;
            margin-bottom:7px;
            border:1px solid #e0e0e0;
            border-radius:8px;
            background:#ffffff;
        ">

            <img src="%s"
                 style="
                    width:72px;
                    height:72px;
                    object-fit:cover;
                    border-radius:8px;
                    border:1px solid #dddddd;
                    background:#f8f8f8;
                    flex-shrink:0;
                 "/>


            <div style="
                flex:1;
                min-width:0;
                overflow-wrap:anywhere;
                word-break:break-word;
            ">

                <div style="
                    font-size:14px;
                    line-height:1.35;
                    font-weight:800;
                    color:#111111;
                ">
                    %s
                </div>


                <div style="
                    font-size:12px;
                    font-weight:600;
                    color:#666666;
                    margin-top:2px;
                ">
                    SKU: %s
                </div>

            </div>


            <div style="
                min-width:64px;
                text-align:center;
                border:2px solid %s;
                background:%s;
                border-radius:8px;
                padding:6px;
                flex-shrink:0;
            ">

                <div style="
                    font-size:24px;
                    font-weight:900;
                    line-height:1;
                    color:%s;
                ">
                    %s
                </div>

                <div style="
                    font-size:11px;
                    font-weight:700;
                    color:#333333;
                ">
                    %s
                </div>

            </div>

        </div>
    """ % (
        image_url,
        product.name or '',
        sku,
        qty_border,
        qty_bg,
        qty_color,
        qty_display,
        txt_units
    ))


# ---------------------------------------------------------
# NO PRODUCTS
# ---------------------------------------------------------

if not product_lines:

    product_lines.append("""
        <div style="
            padding:10px;
            border:1px solid #dddddd;
            border-radius:8px;
            color:#777777;
        ">
            %s
        </div>
    """ % txt_no_products)


# ---------------------------------------------------------
# ORDER NUMBER
# ---------------------------------------------------------

order_number = record.origin or record.name or ''


# ---------------------------------------------------------
# TOTAL QUANTITY
# ---------------------------------------------------------

total_qty_display = (
    int(total_qty)
    if total_qty == int(total_qty)
    else total_qty
)


# ---------------------------------------------------------
# CUSTOMS WARNING
# ---------------------------------------------------------

customs_note = ''


if country_missing:

    customs_note = """
        <div style="
            margin-top:10px;
            padding:8px 10px;
            border-radius:6px;
            background:#fff3cd;
            border:1px solid #f0ad4e;
            color:#8a5a00;
            font-size:13px;
            font-weight:800;
            text-align:center;
        ">
            %s
        </div>
    """ % txt_country_missing


elif not is_eu:

    customs_note = """
        <div style="
            margin-top:10px;
            padding:8px 10px;
            border-radius:6px;
            background:#fff5f5;
            border:1px solid #d00000;
            color:#d00000;
            font-size:13px;
            font-weight:800;
            text-align:center;
        ">
            %s
        </div>
    """ % txt_customs


# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

summary_section = """
    <div style="
        margin-top:12px;
        padding:14px 16px;
        border-radius:10px;
        background:#f8f8f8;
        border:1px solid #dddddd;
        display:flex;
        align-items:center;
        justify-content:space-between;
        gap:16px;
    ">

        <div style="flex:1;">

            <div style="
                font-size:12px;
                font-weight:800;
                color:#666666;
                text-transform:uppercase;
            ">
                %s
            </div>

            <div style="
                font-size:26px;
                font-weight:900;
                color:#111111;
                line-height:1.1;
            ">
                %s
            </div>

        </div>


        <div style="
            width:1px;
            height:46px;
            background:#cccccc;
        ">
        </div>


        <div style="
            flex:2;
            display:flex;
            align-items:center;
            justify-content:flex-end;
            gap:12px;
        ">

            <div style="
                font-size:16px;
                font-weight:800;
                color:#555555;
            ">
                %s
            </div>


            <div style="
                font-size:48px;
                line-height:1;
                font-weight:900;
                color:%s;
            ">
                %s
            </div>


            <div style="
                font-size:16px;
                font-weight:800;
                color:#333333;
            ">
                %s
            </div>

        </div>

    </div>
""" % (
    txt_articles,
    article_count,
    txt_total_qty,
    order_color,
    total_qty_display,
    txt_units
)


# ---------------------------------------------------------
# COUNTRY BADGE BACKGROUND
# ---------------------------------------------------------

badge_bg = (
    '#fff3cd'
    if country_missing
    else (
        '#fff5f5'
        if not is_eu
        else '#f0fff4'
    )
)


# ---------------------------------------------------------
# FINAL PACKING CARD HTML
# ---------------------------------------------------------

html = """
<div style="
    background:#ffffff;
    border:2px solid %s;
    border-radius:10px;
    padding:14px;
    font-family:Arial, sans-serif;
">

    <!-- ORDER HEADER -->

    <div style="
        display:flex;
        justify-content:space-between;
        align-items:center;
        margin-bottom:10px;
        gap:10px;
    ">

        <div style="min-width:0;">

            <div style="
                font-size:11px;
                font-weight:800;
                color:#666666;
                text-transform:uppercase;
            ">
                %s
            </div>

            <div style="
                font-size:32px;
                line-height:1.05;
                font-weight:900;
                color:%s;
                overflow-wrap:anywhere;
            ">
                %s
            </div>

        </div>


        <div style="
            display:flex;
            align-items:center;
            gap:8px;
            flex-shrink:0;
        ">

            %s

            <div style="
                border:2px solid %s;
                color:%s;
                background:%s;
                padding:4px 14px;
                border-radius:999px;
                font-weight:900;
                font-size:13px;
                letter-spacing:0.3px;
                white-space:nowrap;
            ">
                %s
            </div>

            %s

        </div>

    </div>


    <div style="
        border-top:1px solid #e0e0e0;
        margin:10px 0 12px 0;
    ">
    </div>


    <!-- CUSTOMER / ADDRESS / SHIPPING -->

    <div style="
        display:flex;
        gap:14px;
        margin-bottom:12px;
    ">

        <div style="
            flex:0.8;
            min-width:0;
        ">

            <div style="
                font-size:11px;
                font-weight:800;
                color:#666666;
                text-transform:uppercase;
            ">
                %s
            </div>

            <div style="
                font-size:17px;
                font-weight:900;
                margin-top:3px;
                overflow-wrap:anywhere;
            ">
                %s
            </div>

        </div>


        <div style="
            flex:1.1;
            min-width:0;
        ">

            <div style="
                font-size:11px;
                font-weight:800;
                color:#666666;
                text-transform:uppercase;
            ">
                %s
            </div>

            <div style="
                font-size:14px;
                line-height:1.35;
                font-weight:700;
                margin-top:3px;
                overflow-wrap:anywhere;
            ">
                %s
            </div>

        </div>

        %s

    </div>


    <div style="
        border-top:1px solid #e0e0e0;
        margin:12px 0;
    ">
    </div>


    <!-- PRODUCTS -->

    <div style="
        font-size:15px;
        font-weight:900;
        margin-bottom:9px;
        color:#111111;
    ">
        %s
    </div>


    %s


    <!-- DELIVERY / PICKING NOTE -->

    %s


    <!-- SALE ORDER / SHOPIFY NOTE -->

    %s


    <!-- SUMMARY -->

    %s


    <!-- CUSTOMS -->

    %s

</div>
""" % (

    # Main card border
    border_color,

    # Order
    txt_order,
    order_color,
    order_number,

    # Carrier badge (DHL / GLS)
    carrier_badge,

    # EU / NON-EU badge
    order_color,
    order_color,
    badge_bg,
    badge_text,

    # Payment badge
    pay_badge,

    # Customer
    txt_customer,
    partner.name or '',

    # Address
    txt_address,
    address_html,

    # Shipping date
    shipping_html,

    # Products title
    txt_products,

    # Product cards
    ''.join(product_lines),

    # Delivery / Picking Note
    picking_note_html,

    # Sale Order / Shopify Note
    note_html,

    # Summary
    summary_section,

    # Customs
    customs_note
)


# ---------------------------------------------------------
# WRITE GENERATED HTML TO PACKING CARD FIELD
# ---------------------------------------------------------

record.write({
    'x_studio_packing_card': html,
})