# Goods Receipts / Wareneingänge – Production rollout

Everything lives in the database (manual models, views, automations), not in git, so a merge or
push to main does **not** carry it over. You install it in production by running
`install_wareneingang.py` **once** in a Scheduled Action. It builds the final state from staging.

## What the script installs (state of 05.11.2026)
| Part | Content |
| --- | --- |
| App + menus | Goods Receipt · Upcoming deliveries · Import delivery overview · Report rejected delivery · Configuration → Stages |
| Models | `x_wareneingang` (card), `x_wareneingang_stage`, `x_wareneingang_line` (delivery schedule), `x_iq_delivery_upload` (Excel import), `x_iq_rejection_report` (rejected deliveries) |
| Stages | Expected · Partly booked · Done · Rejected (EN/DE) |
| Cards | Kanban sorted "last changed first", badges (Overdue, This week, defective, No PO yet), progress, kit parts, files |
| Form | KPI tiles, size table, Delivery schedule, Files (upload + preview), Defects, Notes and rejection, Order lines, Receipts, Quality; banner when there is no PO |
| Upcoming deliveries | Opens in calendar; list grouped by month |
| Excel import | Creates/updates planned lines and cards, links POs by vendor reference, attaches the Excel to every card |
| Report rejected delivery | Supplier/PO, reason (Quality root causes), note, files → card in Rejected with files |
| Automations | Card on PO confirmation · Status on receipt booking · Vendor ref sync · Manual delivery → card |
| Public calendar | `/website/action/iq-delivery-calendar?key=…` – no login, read-only, no prices. New key for production (see log line) |
| One-time data | Cards for **all** confirmed POs (open and completed) with status and arrival date |

**Not carried over:** staging test data (planned lines from the Excel, test POs, the rejected
test card). After go-live, re-upload the current delivery overview Excel in production.
**Not included:** Warehouse overview, staging experiments, diagnostic scripts, PDF reading (undecided).

## Steps
1. **Backup production:** Odoo.sh → Production → Backups → *Create backup*.
2. **Dry run (recommended):** rebuild a staging branch from production (fresh copy, no app yet),
   run steps 3–5 there and check. Then repeat on production.
3. **Run the script:**
   - Developer mode (`?debug=1`) → Settings → Technical → Automation → Scheduled Actions → New.
   - Name `IQ Install Goods Receipts`, Model **Contact**, **Active = off**.
   - Paste the **whole** `install_wareneingang.py` → Save → **Run Manually** (once). It can take a minute.
   - No popup = success. A popup = nothing was changed; send the text.
4. **Reload** (Cmd+R). The Goods Receipts app appears.
5. **Check:**
   - Settings → Technical → Logging, search `IQ` → "installed: N cards" and the **public calendar link**.
   - Cards in the right columns; open a card (tiles, size table, files).
   - Confirm a test PO → card appears; validate a receipt → card moves.
   - Upcoming deliveries opens in the calendar; Import delivery overview with the current Excel.
   - Report rejected delivery → test, then archive the test card.
   - Open the public link in a private window.
   - Switch user language DE ↔ EN.
6. **Document:** CHANGELOG entry + Knowledge article for the team; give the public link to the warehouse.
7. Set the scheduled action to stay **inactive** (or delete it).

## Running again
Safe: it updates views, calculations and automations to the script's version and never deletes
records. It overwrites manual Studio edits to the views named "IQ …". The public calendar key
is only set the first time (change it in System Parameters → `iq.delivery_calendar_key`).

## If something goes wrong
- Popup while running → whole run rolled back, nothing saved.
- Problem after running → restore the backup, or archive the four "IQ …" automations to stop them.
