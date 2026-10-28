// Daily work log – one entry per task, newest at the bottom.
// To add a day: copy one entry, change the fields, commit + push.
// date: YYYY-MM-DD · area: Shopify | Odoo | Odoo · DHL | Odoo · Shipping | Other
// status: Live | Done | In progress | Staging | Reference
// link: path from the site root (optional)
window.IQ_LOG = [
  {
    date: "2026-10-13",
    area: "Odoo · DHL",
    title: "DHL Receiver ID – knowledge page",
    summary: "How DHL return Receiver IDs work in Odoo.",
    status: "Reference",
    link: "DHL_Receiver_ID_Odoo_Knowledge.html"
  },
  {
    date: "2026-10-14",
    area: "Odoo · DHL",
    title: "DHL automations – updated configuration (PDF)",
    summary: "DHL configuration changes documented as a printable PDF.",
    status: "Staging",
    link: "IQ_Dogsport_DHL_Automations_Updated_2026-10-14.pdf"
  },
  {
    date: "2026-10-19",
    area: "Shopify",
    title: "Product merge MFJ 3.0 Unisex / Damen",
    summary: "Colour products merged into one product with variants: Odoo SKU check, import, connector, Judge.me groups, go-live.",
    status: "Done",
    link: "shopify/product-merge/"
  },
  {
    date: "2026-10-19",
    area: "Shopify",
    title: "Winter Insider Campaign 2026",
    summary: "Free MagDock voucher for winter-model buyers: Flow, segment, discount code, order email, newsletter.",
    status: "Live",
    link: "shopify/winter-insider-campaign-2026/"
  },
  {
    date: "2026-10-19",
    area: "Shopify",
    title: "Theme fixes",
    summary: "Judge.me button, unit price on product page and collection cards, Fit & Sizing tab only with size chart, English option names.",
    status: "Live",
    link: "shopify/theme-fixes-2026-10-19/"
  },
  {
    date: "2026-10-19",
    area: "Odoo · DHL",
    title: "DHL shipping & return automations page",
    summary: "Carrier selection, carrier sync to deliveries, return Receiver IDs (Odoo 19).",
    status: "Staging",
    link: "dhl-automations.html"
  },
  {
    date: "2026-10-20",
    area: "Odoo",
    title: "Scrap Orders integration",
    summary: "Scrap into Defektlager creates a claim case automatically, same logic as Returns/Repairs.",
    status: "Live",
    link: "odoo/scrap-integration/"
  },
  {
    date: "2026-10-20",
    area: "Odoo · DHL",
    title: "DHL production rollout – status",
    summary: "Carriers live in Production, receiver automation, findings on Shopify/GLS carrier flow, switch-day checklist.",
    status: "In progress",
    link: "odoo/dhl-production-rollout/"
  },
  {
    date: "2026-10-21",
    area: "Shopify",
    title: "Welcome-IQ discount – IQ products only",
    summary: "10 % newsletter code limited to IQ products via hidden collection Welcome-Rabatt; no-discount tag on winter coats; texts in newsletter box and Flow email. Tested in checkout.",
    status: "Live",
    link: "shopify/welcome-iq-discount/"
  },
  {
    date: "2026-10-21",
    area: "Odoo · Shipping",
    title: "GLS: 3 labels instead of 4 (S00461)",
    summary: "Missing box on a finished delivery: repacking a Done delivery doesn't work in Odoo 19; fix with an extra GLS label.",
    status: "Done",
    link: "odoo/gls-extra-package-s00461/"
    },
  {
    date: "2026-10-21",
    area: "Odoo · Shipping",
    title: "Deliveries: release only by authorised users",
    summary: "Group Check Availability erlaubt (5 users); Check Availability and Waiting-Validate hidden for others in Studio; automation blocks Waiting → Done outside the group, also in the Barcode app.",
    status: "Live",
    link: "odoo/delivery-validation-restrictions/"
  },
  {
  date: "2026-10-22",
  area: "Odoo",
  status: "In progress",
  title: "Overtime threshold notification: weekly check + month-end summary",
  summary: "Rewrote the overtime alert cron from a lifetime-balance check (never reset) to a rolling 7-day check scaled to each employee's own contracted hours, added a month-end total-hours summary for managers, and cleaned up 15 stale alerts the old logic had created.",
  link: "odoo/overtime-threshold-notification/index.html"
},
  {
    date: "2026-10-23",
    area: "Odoo",
    title: "Shopify instance archived by mistake – webhooks & schedulers restored",
    summary: "Production Shopify instance archived and reactivated by mistake: webhooks deleted, 2 schedulers off, orders stopped syncing. Diagnosed with read-only commands, schedulers 105/101 re-enabled, webhooks re-created one by one, missed orders imported, verified end to end.",
    status: "Done",
    link: "odoo/shopify-instance-archive-2026-10-23/"
  },
    {
    date: "2026-10-26",
    area: "Odoo · Attendances",
    title: "Overtime check: weekly on Mondays, always notify",
    summary: "Weekly overtime check now runs only on Mondays and looks at the previous week (Mon–Sun) instead of a rolling 7 days. A new to-do is created every week an employee is over the threshold, even if last week's to-do is still open. Week dates now shown in the to-do title. Month-end summary unchanged.",
    status: "Live",
    link: "odoo/overtime-threshold-notification/"
  },
  {
    date: "2026-10-26",
    area: "Odoo · Shipping",
    title: "Carrier assignment: Germany → DHL, international → GLS",
    summary: "Fixed Shipping add (condition never matched), new GLS rule, removed carrier actions from incoterm rules, archived Auto Set Carrier. Tested in staging with Odoo orders and Shopify test-store orders; production checklist ready.",
    status: "Staging",
    link: "odoo/dhl-gls-carrier-assignment/"
  },
  {
    date: "2026-10-26",
    area: "Odoo",
    title: "Shopify orders linked to archived products – duplicate mappings",
    summary: "Reactivating the instance on 23.10 re-activated old Shopify layer mappings: 27 wrong mappings, orders #IQD-99056/99075/99099 got archived or wrong products. Mappings 749 and 1169 archived and verified; 25 remaining, orders to correct.",
    status: "In progress",
    link: "odoo/shopify-duplicate-mappings/"
  },
  {
    date: "2026-10-26",
    area: "Shopify · Gift cards",
    title: "Gift cards – physical cards without code & custom amounts blocked",
    summary: "Customer complaint #IQD-95299: printed code never existed in Shopify; replacement 125 € card created with the same code. Root cause: Gift Card Hero physical-card auto assignment disabled; 9 more pre-21.09 orders without card. Custom amounts fail with 400 since ~20.10; support request sent to Syncube.",
    status: "Waiting for support",
    link: "odoo/gift-card-hero-2026-10-26/"
  },
  {
    date: "2026-10-27",
    area: "Odoo · Shipping",
    title: "DHL Parcel DE live in Production – Germany DHL, international GLS",
    summary: "DHL Parcel DE live: Germany → DHL Parcel DE, international → GLS Germany. Found on go-live: Shopify orders arrive with fixed price carriers (GLS Deutschland 15, auto-created DHL Paket 27, GLS EU 11, Standard 21…) set by a write after create; rules extended and Delivery Method added to When updating. Block Validate rule, packing card badge, DHL pickup booked for 28.10.",
    status: "Live",
    link: "odoo/dhl-go-live-2026-10-27/"
  },

  {
    date: "2026-10-27",
    area: "Odoo · Shopify",
    title: "Product data queues stuck – duplicate Shopify template links",
    summary: "Product data queues stuck since 23.10 (Expected singleton product.template(89, 178)). Duplicate template links re-activated by the instance reactivation. Archived 205, 199, 332, 333 with before/after checks; PDQ006762 completed. Open: 316 (PSD), 114, remaining queues.",
    status: "In progress",
    link: "odoo/shopify-template-duplicates-2026-10-27/"
  },

  {
    date: "2026-10-27",
    area: "Shopify · Tax",
    title: "EU business customers charged VAT – status",
    summary: "EU B2B customers with a valid VAT ID charged gross price. Investigation open: checklist of Shopify tax settings, Odoo query for affected orders since 01.04.2026, report to Patricia.",
    status: "Open",
    link: "shopify/eu-b2b-vat-reverse-charge/"
  },
  {
    date: "2026-10-28",
    area: "Shopify · Tax",
    title: "EU VAT ID – Odoo automations + Shopify Dynamic tax (live)",
    summary: "Root cause: Emipro does not import the checkout VAT ID (only in Shopify order events) and Shopify keeps the gross price with fixed tax display. Live: Odoo automations 'IQ – EU VAT from Shopify reverse charge' + '0% tax on reverse-charge lines', #IQD-99202 corrected, Shopify Dynamic tax-inclusive pricing on (decision Florian). Open: monitor first Dynamic orders, EU price adjustment, past refunds.",
    status: "Live",
    link: "shopify/eu-b2b-vat-reverse-charge/"
  },
];
