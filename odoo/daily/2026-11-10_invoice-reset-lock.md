# Odoo change documentation – 10.11.2026

**Author:** Hamza Mohsin
**Asana:** [Posted invoices: rights and lock date](https://app.asana.com/0/0/1220208895306733/f), project "ToDo IT Hamza"
**Systems:** Odoo 19 production (`iq-dogsport.odoo.com`) and Odoo.sh staging (`iq-dogsport-staging-41221989.dev.odoo.com`)

---

## 1. Why

Elena reset five posted customer invoices that had already gone to the tax office (RE/2026/03477, 03817, 04640, 04679, 00566). The tax advisor said on 06.11. that changing posted invoices must not be possible.

**Root cause:** Elena did not have Accounting Administrator directly. The group **Shopify / Manager** (from the Emipro connector) automatically includes Sales Administrator, **Accounting Administrator**, Inventory Administrator and Shopify User.

**Decision (agreed with Florian, 10.11.):**

| Invoice status | Who can use "Reset to Draft" |
|---|---|
| Posted, **not yet sent** to the customer | everyone with invoicing rights |
| Posted and **sent** to the customer | only **Florian and Patricia** |

Posting new invoices and credit notes is **not** restricted.

---

## 2. What was changed, and where

### 2.1 User rights (production)

| User | Where | Before | After |
|---|---|---|---|
| Elena Kistritz | Settings → Users → Elena → Access Rights | Shopify: **Manager** (→ Accounting: Administrator, implied) | Shopify: **User** → Accounting: **Invoicing** (implied by Shopify/User) |
| Office (office@iq-dogsport.de) | Settings → Groups → Accounting / Administrator → Users | member of Accounting / Administrator | removed → Accounting: **No** (login is only used for picking/packing) |

- The **Shopify / Manager** group itself was **not** changed (it comes from the connector and affects all 5 members).
- Tested: Office can still edit normal customer addresses. Editing contacts linked to internal users (employees) is blocked for non-admins, which is standard Odoo and unrelated to this change.

### 2.2 Group "Invoice Posting Allowed"

- **Where:** Settings → Users & Companies → Groups
- **Privilege:** empty
- **Members:** Dr. Florian Knabl, Patricia Knabl

| | Production | Staging |
|---|---|---|
| Group ID | **151** | **152** (151 was deleted by mistake during testing) |

To give someone else the right to reset sent invoices, add the user to this group.

### 2.3 External identifier

- **Where:** Settings → Technical → Sequences & Identifiers → External Identifiers
- **Module:** `custom` · **External Identifier:** `group_invoice_posting` → full name `custom.group_invoice_posting`
- **Model:** `res.groups` · **Record ID:** 151 (production) / 152 (staging)
- **Non Updatable:** ticked

The view and the automation rule refer to the group by this name. **If the group is ever deleted and recreated, update the Record ID here.**

### 2.4 Inherited form view (button visibility)

- **Where:** Settings → Technical → User Interface → Views
- **View Name:** `account.move.form.reset.draft.sent`
- **View Type:** Form · **Model:** Journal Entry (`account.move`)
- **Inherited View:** `account.move.form` (External ID `account.view_move_form`)
- **View inheritance mode:** Extension View · **Sequence:** 16 · **Active:** yes
- **Architecture:**

```xml
<data>
    <!-- normal button: only when the invoice is NOT sent yet -->
    <xpath expr="//button[@name='button_draft']" position="attributes">
        <attribute name="invisible">not show_reset_to_draft_button or is_move_sent</attribute>
    </xpath>
    <!-- admin button: only when the invoice IS sent, only for the group -->
    <xpath expr="//button[@name='button_draft']" position="after">
        <button name="button_draft" string="Reset to Draft" type="object"
                groups="custom.group_invoice_posting"
                invisible="not show_reset_to_draft_button or not is_move_sent"/>
    </xpath>
    <xpath expr="//sheet" position="inside">
        <field name="is_move_sent" invisible="1"/>
    </xpath>
</data>
```

**Why two buttons:** Odoo can hide a button either by user group (`groups`) or by record data (`invisible`), but not both combined on one button. Both buttons call the same method (`button_draft`), and a user never sees both at once.

### 2.5 Automation rule (the real lock)

- **Where:** Settings → Technical → Automation → Automation Rules
- **Name:** Block post/reset/cancel invoices for unauthorized users
- **Model:** Journal Entry
- **Trigger:** On create and edit
- **When updating:** Status (only)
- **Before Update Domain:** empty
- **Apply on:**
  ```python
  [("move_type", "in", ["out_invoice", "out_refund", "in_invoice", "in_refund"])]
  ```
- **Action:** Execute Code

```python
allowed = (
    env.uid == 1                      # OdooBot / automatic jobs
    or env.user.share                 # public user (Shopify webhooks)
    or env.user.has_group('custom.group_invoice_posting')
)
if not allowed:
    for rec in records:
        if rec.posted_before and rec.is_move_sent and rec.state in ('draft', 'cancel'):
            raise UserError(
                "This invoice was already sent to the customer. "
                "Only Admins can reset it to draft. "
                "Please create a credit note or write a note in the chatter."
            )
```

This blocks resetting or cancelling a **sent** invoice for everyone outside the group, even if they don't use the button (for example via import or the API).

### 2.6 Studio (staging only, reverted)

During testing, Studio changes were made to the standard **Reset to Draft** button (Allow/Forbid visibility to groups). They were **reverted** in staging. Final state: Allow = Accounting / Invoicing, Forbid = empty. **Nothing was changed in Studio in production.**

---

## 3. How "sent" is detected

The standard field **`is_move_sent`** ("Sent") is set when an invoice goes out from Odoo: the **Send** button or the automatic invoice email (checked on Shopify invoice RE/2026/05530: `is_move_sent = true`).

**Limitation:** if a PDF is only printed or downloaded and given to the customer outside Odoo, `is_move_sent` stays false and the normal Reset to Draft button stays visible.

---

## 4. Tests

**Staging, before the change (as Elena with Invoicing rights):** create ✅, post ✅, reset to draft ✅, cancel ✅. This showed rights alone were not enough.

**Production, after the change:**

| User | Invoice | Result |
|---|---|---|
| Hamza | RE/2026/05730 (sent by email) | no Reset to Draft ✅ |
| Florian | RE/2026/05730 (sent) | Reset to Draft visible ✅ |
| Hamza / Elena | posted, not sent | Reset to Draft visible ✅ |

---

## 5. How to undo (if needed)

1. **View:** Settings → Technical → Views → `account.move.form.reset.draft.sent` → untick **Active**.
2. **Rule:** Automation Rules → "Block post/reset/cancel…" → archive it (untick Active).
3. **Elena:** Shopify back to **Manager** (gives Accounting Administrator again).
4. **Office:** add back to Accounting / Administrator.

Keep the group and the external identifier unless you remove both the view and the rule.

---

## 6. Still open

- **Lock date up to 31.10.2026:** Accounting → Configuration → Settings → Lock Dates. Set it only after Patricia confirms the opening stock bookings are done. Exception only for the terminal/API user. **Never set the Hard Lock Date** (it can't be undone).
- **Terminal/API user:** which user it is, so it can get the lock date exception (and, if needed, membership in the group).
- **Group members:** Patricia's task names Anastasiia, Patricia and Hamza; Florian decided Florian and Patricia. Waiting for Patricia's confirmation.
- **Florian** still has full Accounting Administrator rights.
- **Office** still has "Bank: Validate bank account".

---

## 7. Other changes on 10.11.2026

### Product category: Top-Matic / Jolly Pets → "Trainingszubehör" (production)
- 8 products moved from **Bekleidung** to **Trainingszubehör** (Top-Matic: Bite Roll 20x16cm, Fun Ball, Fun Ball orange, Profi Set; Multi Power Clip and MAXI Power Clip were already correct. Jolly Pets: Soccer Ball 6", Soccer Ball 8").
- No valuation entries: both categories have identical settings (FIFO, Perpetual (at invoicing), accounts 840000 / 340000 / 398000).
- Open: "Bekleidung" has 166 products incl. non-clothing items (e.g. IQ Magnetizer); a category with no name exists.

### Supplier merge: "McPet" → "Mc-Pet" (production)
- Merged McPet (ID 53595) into **Mc-Pet (ID 114)**. Mc-Pet was kept because name, address (Gewerbestrasse 4, 87752 Schwaighausen) and contact person (Markus Schwendinger) match the invoices.
- Result: 12 vendor bills, 26,668.09 €, all reconciled, balance 0.
- Bank account Deutsche Bank **DE20 6507 0024 0311 1937 00** (matches invoice IBAN) moved to Mc-Pet; still marked **Untrusted**.
- VAT ID **DE261263682** checked in EU VIES (valid, 10.11.2026) and added; Odoo set Intra-Community Valid = Yes.
- Open: other McPet-related contacts ("Mc Pet - Dein Heimtierspezialist", "Mc Pet Futtermittel-Großhandel, Lilo Heinzle" ×2, "Lilo Heinzle").

### Task 2: Holfelder P00053 (MFJ 4.0)
- Receipt already booked. 10 pieces still open on the order; these are the defective ones. Waiting for Patricia's decision on how to handle them.
