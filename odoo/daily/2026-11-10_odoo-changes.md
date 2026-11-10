# Odoo work log – 10.11.2026 (Hamza Mohsin)

Entries for `CHANGELOG.md` and `WORK-LOG.md` (~/Documents/odoo-customizations/).

---

## CHANGELOG.md entries

### 2026-11-10 – Product category: Top-Matic / Jolly Pets moved to "Trainingszubehör"
- **Status:** ✅ Done (production)
- **Requested by:** Manager (data clean-up task)
- **What changed:** 8 products moved from category **Bekleidung** to **Trainingszubehör**
  - Top-Matic (6): Bite Roll 20x16cm, Fun Ball, Fun Ball orange, Profi Set, Multi Power Clip, MAXI Power Clip (the 2 Power Clips were already correct)
  - Jolly Pets (2): Soccer Ball 6", Soccer Ball 8"
- **Valuation check before the change:** both categories have identical settings (FIFO, Perpetual (at invoicing), Income 840000, Expense 340000, Stock 398000), so **no stock valuation entries were created** and the stock value stayed on account 398000.
- **Open / reported to manager:**
  - "Bekleidung" contains 166 products, incl. non-clothing items (e.g. IQ Magnetizer, 138 pcs). "Trainingszubehör" has only 5. Asked whether to review and move them.
  - There is a product category with no name.

### 2026-11-10 – Supplier merge: "McPet" merged into "Mc-Pet"
- **Status:** ✅ Done (production)
- **Requested by:** Patricia
- **Findings before merge:**
  - Both partners were used on vendor bills: Mc-Pet 5 bills (−9,104.32 €), McPet 7 bills (−17,563.77 €)
  - All 12 bills were paid via bank reconciliation (journal BNK4), balance 0.00 on both, nothing open
  - Invoice numbers run in one series (RG43437–RG44288), so it's the same supplier
  - Only McPet had a bank account: Deutsche Bank, **DE20 6507 0024 0311 1937 00**, BIC DEUTDEDB650. It matches the IBAN printed on McPet's invoices.
  - Neither partner had a VAT ID. DATEV Vendor = 0 on both.
- **What changed:**
  - Merged McPet (ID 53595) into **Mc-Pet (ID 114)**. Mc-Pet was kept because its name, address (Gewerbestrasse 4, 87752 Schwaighausen), email and contact person (Markus Schwendinger) match the invoices.
  - Result: 12 vendor bills, total 26,668.09 €, bank account moved to Mc-Pet.
  - VAT ID **DE261263682** (from the invoices) checked in EU VIES on 10.11.2026 (valid) and added to Mc-Pet. The Peppol Endpoint is set to the same value, and Odoo set "Intra-Community Valid = Yes" automatically.
- **Open / reported to Patricia:**
  - The IBAN is still marked **Untrusted**. Should accounting verify it?
  - Other McPet-related contacts exist ("Mc Pet - Dein Heimtierspezialist", "Mc Pet Futtermittel-Großhandel, Lilo Heinzle" ×2, "Lilo Heinzle"). Clean up?

### 2026-11-10 – Accounting rights: Elena and Office user restricted
- **Status:** ✅ Done (production)
- **Asana:** [Posted invoices: rights and lock date](https://app.asana.com/0/0/1220208895306733/f), project "ToDo IT Hamza"
- **Background:** Elena reset 5 posted customer invoices that had already gone to the tax office (RE/2026/03477, 03817, 04640, 04679, 00566). The tax advisor (06.11.) said changing posted invoices must not be possible.
- **Root cause:** Elena did not have Accounting Administrator directly. The group **Shopify / Manager** implies **Sales Administrator + Accounting Administrator + Inventory Administrator + Shopify User**.
- **What changed (production):**
  - **Elena Kistritz:** Shopify **Manager → User**, so Accounting is now **Invoicing** (implied by Shopify/User).
  - **Office user** (office@iq-dogsport.de): removed from Accounting / Administrator, so Accounting = **No**. The login is used for picking/packing. Tested: Office can still edit normal customer addresses. (Editing contacts of internal users, e.g. employees, is blocked for non-admins. That's standard Odoo, not related to this change.)
- **Not changed:** the Shopify / Manager group definition itself (it comes from the connector, and changing it would affect all 5 members).
- **Current Accounting Administrator / Shopify Manager members:** Florian, Hamza, Patricia (direct); Anastasiia (via Shopify Manager).
- **Open:** Should Florian keep Accounting Administrator? Should Office keep "Bank: Validate bank account"?

### 2026-11-10 – Block post / reset / cancel of invoices for unauthorized users
- **Status:** 🧪 Built and tested in **staging only**. **Not in production.** Waiting for Patricia's decision.
- **Asana:** [Posted invoices: rights and lock date](https://app.asana.com/0/0/1220208895306733/f)
- **Why:** with "Invoicing" rights, a user can still post, reset to draft and cancel invoices (tested as Elena in staging: create ✅, post ✅, reset ✅, cancel ✅). Standard Odoo rights can't separate "create" from "post/reset/cancel".
- **Staging setup:**
  1. **Group** `Invoice Posting Allowed` (res.groups, ID 151 in staging). Members: Hamza, Patricia, Anastasiia. (Terminal/API user still to be added.)
  2. **External identifier** `custom.group_invoice_posting` → res.groups, record ID 151 (non-updatable)
  3. **Automation rule** "Block post/reset/cancel invoices for unauthorized users"
     - Model: Journal Entry (account.move)
     - Trigger: On create and edit, when updating: **Status**
     - Before Update Domain: empty
     - Apply on: `[("move_type", "in", ["out_invoice", "out_refund", "in_invoice", "in_refund"])]`
     - Action: Execute Code (Option 2, current):

```python
allowed = (
    env.uid == 1                      # OdooBot / automatic jobs
    or env.user.share                 # public user (Shopify webhooks)
    or env.user.has_group('custom.group_invoice_posting')
)
if not allowed:
    for rec in records:
        # block: posting, cancelling, and resetting a previously posted invoice
        # allow: creating new drafts
        if rec.state in ('posted', 'cancel') or (rec.state == 'draft' and rec.posted_before):
            raise UserError(
                "Only Anastasiia, Patricia or Hamza can post, reset to draft or cancel invoices. "
                "Please write a note in the chatter and inform Anastasiia."
            )
```

- **Staging test results (as Elena, after the rule):** create draft ✅ allowed · Confirm/Post ❌ blocked with message · as Hamza (in the group): post/reset/cancel ✅ allowed.
- **Decision needed from Patricia (asked in Asana):**
  - **Option 1:** office staff may create **and post** new invoices/credit notes, but never reset or cancel after posting. Code change:
    ```python
    if rec.posted_before and rec.state in ('draft', 'cancel'):
        raise UserError("Posted invoices cannot be reset to draft or cancelled. ...")
    ```
  - **Option 2 (task wording, currently in staging):** office staff only create drafts; Anastasiia/Patricia/Hamza post everything (also the rule-3 current-month own corrections).
- **Still to test:** Credit Note → Reverse as Elena (is the credit note created as draft, or blocked?).
- **Before production:** add the terminal/API user to the group; repeat the group + external identifier + rule in production (the group ID will differ there, so check the ID); watch the first Shopify-connector invoices after go-live.

### 2026-11-10 – Lock date up to 31.10.2026
- **Status:** ⏳ Waiting for Patricia's signal (after the opening stock bookings)
- **Plan:** Accounting → Configuration → Settings → Lock Dates, set to **31.10.2026**, with an exception only for the terminal/API user. Late invoices for locked periods get an accounting date in the first open month, invoice date unchanged (to be verified in staging).
- **Warning:** never set the **Hard Lock Date** (it can't be undone).
- **Going forward:** after each monthly package to the tax office, move the lock date to the end of that month.

---

## WORK-LOG.md entry – 2026-11-10

- **Product category clean-up:** checked that Bekleidung and Trainingszubehör have the same valuation settings (no journal entries), then moved 8 Top-Matic/Jolly Pets products. Found 166 products in Bekleidung, incl. non-clothing. Reported to the manager.
- **McPet duplicate supplier:** checked bills, payments (Partner Ledger, all reconciled, balance 0), bank account vs. invoice IBAN, and the invoice number series. Merged McPet → Mc-Pet. Verified the VAT ID DE261263682 in VIES and added it. Reported to Patricia (untrusted IBAN, other McPet contacts).
- **Patricia's 6 priority tasks (tax-office errors):** order agreed: 1) rights + lock date, 3) Emipro ticket, 2) Holfelder P00053, 4) gift cards/discount lines, 5) B2B on company contact with VAT ID, 6) exchanges/refunds double invoice.
- **Task 1 (rights + lock date):**
  - Found that Elena's Accounting Administrator came from Shopify / Manager. Changed her to Shopify User → Accounting Invoicing (production).
  - Removed Office from Accounting Administrator (production). Customer editing still works.
  - Proved in staging that Invoicing users can still post/reset/cancel. Built a group + external identifier + automation rule in staging; tested that Elena is blocked and Hamza is allowed.
  - Sent Patricia the decision question (Option 1 vs 2, Florian, terminal user, lock date timing). Nothing from the block is in production yet.
- **Next:** wait for Patricia's answer → implement in production. Meanwhile: Task 2 Holfelder P00053 (MFJ 4.0, due 11.11.).
