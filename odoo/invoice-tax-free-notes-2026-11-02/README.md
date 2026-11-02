# Invoice tax-free notes (§ 4 Nr. 1a / 1b UStG) – only where they apply

**Status: Live in production (02.11.2026)** · tested in staging first · done by Hamza Mohsin

## In one sentence
Invoices without VAT printed **both** tax-free notes ("EU business sale" **and** "export outside the EU"),
even for EU customers and German gift card orders. Now each invoice shows **only the note that is true** – or none.

## What the two notes mean
| Note | Simple meaning | Example |
|---|---|---|
| **§ 4 Nr. 1b UStG** – steuerfreie innergemeinschaftliche Lieferung | No German VAT because the buyer is a **company in another EU country** with an EU VAT ID (pays VAT in its own country, reverse charge) | Company in Spain with VAT ID |
| **§ 4 Nr. 1a UStG** – steuerfreie Ausfuhrlieferung | No German VAT because the goods go **outside the EU** (buyer pays import tax there) | Customer in Switzerland |

When VAT **is** charged (Germany 19 %, EU private customers via OSS e.g. 21 % ES IVA), no note is printed –
the VAT on the invoice says everything.

## Problem
- Invoice for a German customer (gift card, 0 % VAT): showed **1b and 1a** – both wrong.
- Invoice for a Spanish company with VAT ID: showed **1b and 1a** – 1a ("export") wrong.
- Affected: **every** customer invoice with 0 € VAT.

## Cause
The text is not a tax setting – it comes from the invoice template of the Emipro module
**`commercial_invoice_ept`**, view `commercial_invoice_ept.report_invoice_document`
(inherits `account.report_invoice_document`), block `<div id="no_tax_note">`:

| Line | Condition in the module | Problem |
|---|---|---|
| whole block | invoice type out_invoice **and** VAT amount = 0 | ok |
| § 4 Nr. 1b | customer country is in country group **EU** | Germany is also in the EU; VAT ID not checked |
| § 4 Nr. 1a | **none** | printed on every 0-VAT invoice |

Original block: [code/commercial_invoice_ept_ORIGINAL_block.xml](code/commercial_invoice_ept_ORIGINAL_block.xml)

## How we found it
1. Settings → Technical → Reporting → **Reports** → "Invoice PDF" = `account.report_invoice_with_payments`
   (uses `account.report_invoice_document`).
2. Settings → Technical → User Interface → **Views** → search `report_invoice_document` → 10 views.
3. Opened the non-standard ones: `commercial_invoice_ept.report_invoice_document_custom` = only the info block
   top right; **`commercial_invoice_ept.report_invoice_document`** = contains the § 4 text.

## Solution
**No change to the Emipro module** (a module update would overwrite it). Instead one **new extension view**
that replaces only the `no_tax_note` block with the correct rules. Theme, taxes, accounting and data unchanged,
no new fields.

| Field | Value |
|---|---|
| View Name | `IQ – Steuerfrei-Hinweise korrigiert` |
| View Type | QWeb |
| Inherited View | `account.report_invoice_document` (row with empty "Inherited" column) |
| Inheritance mode | Extension View |
| Sequence | **20** (after the module's 16) |
| Architecture | [code/iq_steuerfrei_hinweise_view.xml](code/iq_steuerfrei_hinweise_view.xml) |

### New rule (checked live when a PDF is generated)
```
VAT on the invoice > 0                     → nothing
VAT = 0 and delivery country Germany       → nothing
VAT = 0, EU country and customer VAT ID    → § 4 Nr. 1b only
VAT = 0, country outside the EU            → § 4 Nr. 1a only
VAT = 0, EU country without VAT ID         → nothing (and the tax setting of that order is wrong)
```
- Country = **delivery address** (falls back to the customer); VAT ID = company of the customer.
- Works for manual and **automatic** (Shopify / Emipro workflow) invoices – the rule runs whenever the PDF is generated.
- PDFs already generated/sent before the change keep the old text.

## Test results (staging, 02.11.2026)
| # | Case | Invoice | Expected | Result |
|---|---|---|---|---|
| 1 | Spanish company with VAT ID – order from Shopify **test store**, invoice created automatically | RE/2026/05084 | only 1b | ✅ |
| 2 | Switzerland, private, manual order (fiscal position non-EU, 0 %) | RE/2026/05085 | only 1a | ✅ |
| 3 | Spain, private, no VAT ID → 21 % ES IVA | RE/2026/05087 | nothing | ✅ |
| 4 | Germany + gift card (0 %) | – | nothing | rule-wise covered (country DE) |

Then created the same view in **production**.

## Rollback
Settings → Technical → Views → `IQ – Steuerfrei-Hinweise korrigiert` → **Active off** → save.
Invoices look exactly like before.

## Open
- [ ] Invoices already sent with the wrong notes (filter: Customer invoices, posted, Tax = 0) – Florian / tax advisor decide whether to correct them
- [ ] Check that **Verify VAT Numbers (VIES)** is on in Invoicing settings
- [ ] Optional: tell Emipro that § 4 Nr. 1a is printed without a condition
- [ ] Side note: shipping line on the Spanish B2B invoice had no tax – check shipping tax on German orders

## Notes
- Wording of legal notes: agreed with Florian; ideally confirmed by the tax advisor.
- Test customers in staging: TEST ES B2B, TEST CH Privat, TEST ES Privat, TEST DE Privat (fictional data).
