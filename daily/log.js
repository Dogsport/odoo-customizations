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
  {
    date: "2026-10-29",
    area: "Odoo · Returns",
    title: "DHL return label + reclamation form by email – one button",
    summary: "Automation sets DHL Parcel DE + deu on German returns; server action 'Send return label' (prod id 1777) creates the DHL label via print_return_label and opens DE/EN email with label + Retourenschein, posted in the ticket when the return comes from one. Fixes: trigger on create+edit, receiver set in same write, template attachments copied, no unlink, prod id, .sudo() for ir.model.fields. Limit: only for deliveries shipped with DHL.",
    status: "Live",
    link: "odoo/dhl-return-label-email-2026-10-29/"
  },
  {
    date: "2026-11-02",
    area: "Shopify",
    title: "Product merge: Patches K9 black + blue → one product",
    summary: "Duplicate + option Farbe, 11 variants (SKUs PAS/PAB unchanged), Odoo import 11/11, stock 1,684, price 12,00, redirects, service-ID upload field (Mini: Image Upload) only for Polizei/Zoll/Justiz/Police, EN translations.",
    status: "Live",
    link: "shopify/product-merge/#merges-patches-k9-readme"
  },
  {
    date: "2026-11-02",
    area: "Odoo",
    title: "Invoice tax-free notes § 4 Nr. 1a / 1b – only where they apply",
    summary: "Emipro view commercial_invoice_ept.report_invoice_document printed 1b + 1a on every 0-VAT invoice. New extension view 'IQ – Steuerfrei-Hinweise korrigiert' (seq 20): 1b = EU company with VAT ID, 1a = non-EU, none for DE. Tested in staging, live.",
    status: "Live",
    link: "odoo/invoice-tax-free-notes-2026-11-02/"
  },
  {
    date: "2026-11-03",
    area: "Odoo",
    title: "Invoice re-sent on returns – send only on the first delivery",
    summary: "Cybrosys automatic_invoice_and_post (stock.picking.button_validate) emailed all invoices of the order on every validated transfer, incl. returns. 'Auto Send Invoice' unticked + automation rule 52 'IQ – Send invoice on first delivery' (Transfer, State → Done, delivery, not a return): sends unsent posted invoices once. POS cash job unchanged. Tested in staging, live.",
    status: "Live",
    link: "odoo/invoice-resend-on-return-fix-2026-11-03/"
  },
  {
    date: "2026-11-03",
    area: "Odoo",
    title: "P00053 – MFJ 4.0 Damen grau fully booked (WH1/IN/00080)",
    summary: "Grey QC done (56 checked, 8 defective). Booked 345 in WH1/IN/00080 (XS 17, S 67, M 103, L 86, XL 44, 2XL 21, 3XL 3, 4XL 4), demand reduced for the 8 defective (claim Holfelder). 146 + 345 + 8 = 499. Backorder WH1/IN/00081 = 861 open: black 353 (QC running) + unisex 500 + 8 defective grey (claim).",
    status: "Done",
    link: "odoo/p00053-holfelder-mfj4-receipt-2026-10-31/"
  },
  {
    date: "2026-11-03",
    area: "Odoo · Shipping",
    title: "Exchange deliveries from tickets without carrier – fallback rule",
    summary: "WH1/OUT/07574 (ticket #00889) had no carrier: ticket Replace creates the delivery directly, no Propagation of carrier, rules 8/45 only on quotations, Auto Set Carrier archived since 27.10. New staging rule 'IQ – Delivery: carrier when empty' (DE → DHL Parcel DE, else GLS Germany, never overwrites). Edit trigger only on Carrier/Contact/Operation Type/Status.",
    status: "Staging",
    link: "odoo/carrier-fallback-ticket-deliveries-2026-11-03/"
  },
];

window.IQ_LOG = (window.IQ_LOG || []).concat([
  { date: "2026-11-04", area: "Odoo", status: "In progress",
    title: "Goods Receipts app – built in staging",
    summary: "One card per supplier delivery: numbers, receipts, quality checks and all files read live from the PO. Automations for PO confirmation and receipt booking, Excel delivery-overview import, Upcoming deliveries calendar, kit parts.",
    link: "odoo/wareneingaenge/" },
  { date: "2026-11-04", area: "Microsoft 365", status: "Waiting on decision",
    title: "Vacation mail coverage – out-of-office and backup",
    summary: "Exchange Administrator role assigned. Team guide published in Odoo Knowledge (article 172). Florian: each employee sets their own auto-reply and forwarding; Patricia and Florian decide the backups; not to mail@." },
  { date: "2026-11-04", area: "Outlook / Asana", status: "Done",
    title: "CD Company delivery dates in Outlook and Asana",
    summary: "4 delivery dates as milestones in Asana project Produktion CD and in the shared Outlook calendar CD Lieferungen (shared with Patricia, Florian, Elena, Anastasiia)." },
  { date: "2026-11-05", area: "Odoo", status: "Done in staging",
    title: "Goods Receipts app – tests, rejected deliveries, public calendar",
    summary: "Status logic tested (receipt, QC fail, inventory adjustment). Added: last-changed sorting, cards for all old POs, No PO yet badge, Excel attached to cards, Report rejected delivery, public delivery calendar without login. All in one install script.",
    link: "odoo/wareneingaenge/" },
  { date: "2026-11-06", area: "Odoo", status: "Live",
    title: "Goods Receipts app live in production",
    summary: "Install script reviewed for side effects, production backup taken, script run once. App live with cards for all POs, icon set in Studio. Docs page with code section published.",
    link: "odoo/wareneingaenge/" }
]);

window.IQ_LOG = (window.IQ_LOG || []).concat([
  { date: "2026-11-06", area: "Shopify / Brevo", status: "Ready to send",
    title: "MagDock voucher – eligibility check and voucher email",
    summary: "72 offer buyers found in the order export (47 MFJ 4.0, 24 winter coat). Code MAGDOCK-INSIDER tested: only works for tagged customers. Brevo list MagDock Insider 2026 (50 recipients) plus personal Outlook email for 14 non-subscribers. Email in newsletter design ready, waiting for Patricia's OK.",
    link: "shopify/magdock-voucher-2026/" },
  { date: "2026-11-06", area: "Customer service", status: "Done",
    title: "Return note for an order shipped abroad (GLS)",
    summary: "Package insert on letterhead: the return service is not available for returns from abroad; customers write to mail@iq-dogsport.de and we arrange the return." }
]);

window.IQ_LOG = (window.IQ_LOG || []).concat([
  { date: "2026-11-06", area: "Odoo", status: "Live",
    title: "Goods Receipts app installed in production",
    summary: "Install script run once in production after a backup. Cards for all purchase orders, status from receipts, files, rejection form, upcoming deliveries.",
    link: "odoo/wareneingaenge/" },
  { date: "2026-11-06", area: "Odoo", status: "Live",
    title: "Warehouse & team calendar – password, absences, new layout",
    summary: "Calendar page for staff without Odoo login: one password for deliveries and absences, approved absences of the whole month (no leave type), IQ logo, summary tiles, phone list view. Menu renamed to Warehouse & team calendar; key and password changed.",
    link: "odoo/wareneingaenge/" },
  { date: "2026-11-06", area: "Odoo", status: "Live",
    title: "PDF delivery notes in Import delivery overview",
    summary: "Supplier delivery note PDF is linked to the existing purchase order card (no new card or delivery) and added to the calendar per article. Tested with Holfelder 2026-344819 on P00053: 499 jackets + 704 zipper-puller sets.",
    link: "odoo/wareneingaenge/" },
  { date: "2026-11-06", area: "Odoo / Shopify", status: "Done",
    title: "P00053 receipt booked and Shopify stock fixed",
    summary: "Damen black + grey booked without the defective pieces from the QC report; rest on backorder. Holfelder invoice checked against the receipt. Black jacket stock did not sync – fixed with a manual stock export (reported to Emipro)." }
]);

window.IQ_LOG = (window.IQ_LOG || []).concat([
  { date: "2026-11-09", area: "Odoo", status: "Live",
    title: "Calendar: My hours & vacation (employee PIN)",
    summary: "Employees log in on the warehouse calendar with their attendance PIN and see their overtime balance, how it is made up, vacation left and all their requests with status. Open requests are shown in orange on the shared calendar.",
    link: "odoo/wareneingaenge/" },
  { date: "2026-11-09", area: "Odoo", status: "Live",
    title: "Calendar: Team overview for managers",
    summary: "Shared manager PIN opens one page with open requests to approve, overtime and vacation per employee, sick days and absences for the next 30 days. Every number links to the Odoo record.",
    link: "odoo/wareneingaenge/" },
  { date: "2026-11-09", area: "Odoo", status: "Done",
    title: "Maintenance guide for the Goods Receipts app",
    summary: "Guide with where each part lives in Odoo, the safe way to change it, troubleshooting and the full code. Master install script brought in line with live." }
]);

window.IQ_LOG = (window.IQ_LOG || []).concat([
  { date: "2026-11-09", area: "Odoo", status: "Live",
    title: "Calendar: My hours & vacation (employee PIN)",
    summary: "Employees log in on the warehouse calendar with their attendance PIN and see their overtime balance, how it is made up, vacation left and all their requests with status. Open requests are shown in orange on the shared calendar.",
    link: "odoo/wareneingaenge/" },
  { date: "2026-11-09", area: "Odoo", status: "Live",
    title: "Calendar: Team overview for managers",
    summary: "Shared manager PIN opens one page with open requests to approve, overtime and vacation per employee, sick days and absences for the next 30 days. Every number links to the Odoo record.",
    link: "odoo/wareneingaenge/" },
  { date: "2026-11-09", area: "Odoo", status: "Done",
    title: "Maintenance guide for the Goods Receipts app",
    summary: "Guide with where each part lives in Odoo, the safe way to change it, troubleshooting and the full code. Master install script brought in line with live." }
]);
