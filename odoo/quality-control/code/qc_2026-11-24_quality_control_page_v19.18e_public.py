# IQ Quality control page (QC) - PUBLIC COPY of PRODUCTION 23.11.2026 (v19.18b supplier check in the normal QC)
# v19.18b: 'Lieferanten-Prüfung' (guest mode). A manager switches one phone to a supplier (QC Dashboard: 'Lieferant prüft selbst (Gastmodus)'
#         on a receipt card, or the 'Lieferanten-Prüfungen' card). The supplier uses the NORMAL check screen: scan -> OK / Defekt with
#         reason, place on the drawing, photo, label – only articles of his receipts (open or already booked). No dashboard, packing,
#         calendar, login, other suppliers. End with the manager PIN (letters + numbers) or automatically after 4–12 h. Pages always German.
#         Results go into the normal QC exactly like the IQ team's checks (dashboard, product cards, QC details, report, inspector table
#         as 'Holfelder-Prüfung · Name'); defect cards show 'Lieferantenprüfung'. Records marked '[Lieferantenprüfung <name> IQ-SUP:<id>]'.
#         Dashboard card 'Lieferanten-Prüfungen': per day / product checked, defects, pieces taken ('Mitgenommen', text file
#         iq_qc_sup_YYYY-MM-DD.txt on the supplier contact). No new fields.
# v19.18d: supplier packs his defects on the same phone ('Defekte verpacken' / 'Verpacken'): only his products, his defects and his own
#         boxes (marked S|<partner id>, label + list show 'Holfelder-Prüfung'); no reopening, no handover, no IQ boxes. Box numbers stay unique.
# v19.18e: Brother RAW labels (defect + box) for the DK-44205 roll (62 mm continuous, removable white, black only):
#         single-colour raster (ESC i z flags 0x8E, ESC i K 0x08, 'g' raster lines) – tested on the QL-820NWB on 24.11.2026.
#         System parameter iq.qc_brother_roll: empty / 'DK-44205' = black only (default); 'DK-22251' = red/black two-colour roll.
# v19.16.10: real line icons instead of emoji ('Wareneingang melden' box icon, 'Keine Zeichnung' warning icon).
# v19.16.9: QC start page: orange button '📦 Wareneingang melden' -> 'Ware angekommen' page of the warehouse calendar.
# v19.16.8: Inspector card: compact one line '✓ Prüfer: Name · ändern' once filled in (was unreadable – light text on green);
#          QC report: IQ Dogsport logo at the very top, above the interim banner.
# v19.16.7: Managers mark the quality check of a product as completed ('Prüfung abschließen' on the details page) – then the
#          QC report is the final report (no 'Zwischenstand' banner); 'Wieder öffnen' undoes it. IQ Dogsport logo on the report.
#          Edit: 'Änderungen speichern' without printer icon, label reprint only optional (tick box).
#          Inspector name: first card on the start and check page, red until filled in, scanning blocked without a name.
#          Scanning also works when the cursor is in a text field (fast scanner input is detected and removed from the field).
# v19.16.6: QC report: no links, no inspector names, no 'Hinweis – kein Defekt' entries, every photo shown complete,
#          print button only after all photos are loaded, banner 'ZWISCHENSTAND – NICHT FINAL' (managers: 'Als Endbericht (final)'),
#          browser header/footer with the page link removed when printing.
#          'Bearbeiten' on defect cards (managers): same screen as creating, pre-filled – reason, place, size, note, photos,
#          switch Defekt <-> Hinweis; every change is written into the chatter of the quality alert.
#          Team password: 5 wrong tries -> 15 min lock. Fix: inspectors can again cancel a just-saved defect in the photo step.
# v19.16.5: Defect cards: 'Löschen' and 'Foto hinzufügen' only for logged-in managers (hidden + server check).
#          Inspectors can still add photos during the check (up to 2 h after saving the defect).
# v19.16.4: 'Karton abgegeben' – a whole closed box can be marked as handed over (who + date, managers only, undo possible);
#          its pieces move from 'In Kartons' to 'Abgegeben' in the comparison. Product name shown above the comparison.
# v19.16.3: 'Defekte verpacken': 'Bereits abgegeben' – record defective pieces that already left (e.g. supplier took them), per size or
#          'Größe unbekannt'; counted in the comparison (column 'Abgegeben'). Managers only. Stored as attachments – no new fields.
# v19.16.2: 'Defekte verpacken': barcode scan works without Enter (TC22 scanner) and without tapping the field; English texts fixed.
# v19.16.1: fix 500 error on 'Defekte verpacken' product page (reversed() is not allowed in Odoo safe_eval).
# v19.16: Manager login on the QC page (button "Anmelden" top right, same manager PIN + same session as the
#         Lager- & Teamkalender, 30 minutes). Drawing status / "Zeichnungen einrichten" only for logged-in managers,
#         saving a drawing needs no PIN while logged in. Links "Kalender" + "Verpacken" in the top bar.
#         New page "Defekte verpacken": scan or tap sizes into numbered boxes, close box -> label (Brother RAW or PDF)
#         with sizes, article numbers, totals, DEFEKT; comparison Odoo defects <-> boxes per size;
#         "Fehlende in Odoo nachtragen" (managers only). Boxes stored as attachments – no new fields.
# v19.15: QC Dashboard: new section 'Zu prüfen – offene Wareneingänge' – every open receipt (expected / partly booked) with clothing
#         (products with sizes): checked / delivered, overdue flag, drawing status and 'Prüfen starten' with that delivery pre-selected.
#         Own drawing for IQ Hundesportweste 4.0 Unisex from CD tech pack 167904 (Mens Dog vest 3.0), only if no own drawing exists yet.
# v19.14: 'Zeichnungen einrichten' (own drawing per product), clearer label, Start button. v19.13 zipper button. v19.12 drawing by article no.
# v19.11: saved screen, tap reasons, label with drawing. v19.10 guided steps. v19.9 defect locations – no new fields.
# v19.8: selected-period inspector breakdown (no misleading new-day zero); compact reason picker and mobile sticky Print Label CTA;
#        require at least one server-verified defect photo before Done/next scan. Notes retain optional photos.
#        Preserve IQ QC v19.7 Brother DK-22251 RAW print, PDF fallback and QC/stock/receipt logic.
# IMPORTANT: Brother RAW requires a separate macOS CUPS RAW queue, not a new application.
# A normal Brother CUPS queue will be BLOCKED from automatic QC printing, not sent PDFs.
# Odoo.sh generates Brother binary raster bytes in safe_eval, then the existing Direct Print PRO
# client delivers those bytes through its qweb-text path. Physical RAW queue test still required.
# Branch: PRODUCTION (run only after the staging test is OK); original 19.6.2 QC functionality and downloadable PDF are preserved.
# Phone page for the inspectors + QC dashboard + product details + printable QC report.
# v19.6.2: Brother PDF jobs no longer override CUPS media with generic 62mm or force rotation.
#          Keep 62mm Black/Red DK-22251 media configured in the macOS CUPS queue; the PDF stays content-sized.
# v19.6.1: badge DEFEKT sits next to QA number with a safe inset, avoiding right-edge clipping. All other QC logic is unchanged.
# v19.6: Brother PrintNode jobs request 62mm continuous roll and disable scaling; v19.5 dynamic-length PDFs preserved.
# v19.5: labels on 62mm continuous Brother DK roll grow with every reason, article and product line. No text truncation for multiple reasons.
#        Separate reason blocks; preserve all QC, photo, mobile, inspector, printer and receipt logic.
# v19.4.1: use the exact Brother_QL_820NWB Direct Print name, enable PDF for Brother, and log the actual output mode.
#          All v19.4 QC workflow, inspector filters, photos, label PDFs, stock and imports remain unchanged.
# v19.4: QC details/report: period + inspector filters; mobile daily inspector table (checked, OK, defects).
#        Inspector source = existing quality.check.note, no new model/fields. Stock-booking overview never filtered.
# v19.3: QC label PDF now 62 mm wide with length selected from text (no fixed 30 mm waste). Direct PDF download in step 2 and on details, no printer needed.
#        Default LABEL_OUTPUT_MODE = download; later switch to print after connecting Brother via Direct Print/PrintNode.
#        Label downloads and Brother print jobs use exactly the same PDF bytes; no QC records/fields modified.
# v19.2: self-contained vector icons (no emoji), compact responsive TC22/mobile layout, touch-friendly actions; QC workflows unchanged.
# v19.1: correct legacy reason Sizenetikett -> Sizeetikett in the QC page and new entries; configurable Direct Print selection.
# v19: defect/note two-step flow: save + label first, then immediate individual photo uploads, retry, cancel, and photo-missing follow-up.
# v18: Holfelder import: receipt must contain the product, P00053 receipt pre-selected, any error is shown clearly and nothing is kept.
# v17: one-time "Holfelder-Import" (link at the bottom of the QC Dashboard): MFJ 4.0 Damen (LS 2026-344396, WH1/IN/00058) and Unisex grau (LS 2026-344819)
#      from the quality reports 05.11./10.11.: 137 OK checks, 10 defects (not booked), 8 notes, 25 photos (HF_photos.zip). Documentation only – no stock,
#      quantity or receipt changes; allowed on booked receipts. Marked IQ-QC-IMPORT-HF-2026-11-17, undo button on the same page.
# v16: phone fixes for products with colour + size (e.g. MFJ 4.0): size buttons grouped by colour, big display shows colour small + size big,
#      delivery bar and "last entry" row wrap correctly on small screens.
# v15: QC only for OPEN receipts (booked ones are hidden/blocked); standard "QC Wareneingang" checks from Quality Control Points are ignored;
#      "Hinweis – kein Defekt" button (photos + reason, counts as OK, no label, own section in details/report);
#      "Letzte Eingaben" list + big saved confirmation; booking overview per receipt (delivered / OK / note / defect / not checked);
#      NEW Odoo button on receipts (Action menu): "QC: OK-Mengen übernehmen" – sets quantity = OK count, does NOT validate (Inventory Administrators only).
# v14: phone layout for all pages: dashboard shows products first, QC reports as cards, max 5 newest defects;
#      details: compact defect rows (photo left, +n photos badge, tap = full screen), scrollable filters; smaller top bar.
# v13: if a product has only one open receipt it is chosen automatically; clear red hint + button when no delivery is chosen;
#      English texts fixed ("Size chosen", "Scanned"); "hide size buttons" link.
# v12: SAFEGUARDS: inspector name required before checking; same barcode again within 3 s = "scanned twice?", not counted;
#      progress per size vs. the receipt (checked / delivered, red when more checked than delivered, Auto-OK stops there);
#      "Letzter war Defekt" turns the last OK into a defect and opens the photo screen.
# v11: BARCODE SCANNING (TC22 scanner = keyboard input): scan the label -> beep + size shown big, choose quantity, OK / Defect.
#      Scanning another product switches product + its receipt automatically. Optional "Auto-OK: every scan = 1x OK".
#      Size buttons only behind "choose size manually". Barcode matched on variant Barcode, else Internal Reference.
#      Defect view: big photos, tap = full screen with swipe, filters by size and reason, clean text.
# v10: records marked [Größe unbekannt] (imported paper checks without size) are shown as size "?" in the size table,
#      on defect cards and labels, and are not counted on the size buttons.
# v10: one-time "Papier-Import" page (link at the bottom of the QC Dashboard): choose the 2 receipts, select the 78 photos,
#      click "Hochladen & importieren" -> creates the paper checks 11.–16.11.2026 (263 + 90 OK, 50 + 4 defects with photos).
#      Runs only once; the same page has "Import rückgängig machen" (undo).
# v9: label PDF is now 62 mm wide x 30 mm high (landscape) – v8 produced a turned 30 x 62 page, so the Brother stopped.
# v8: prints QC labels on the Brother QL-800 (DK-22251, 62 mm continuous) as a 62 x 30 mm PDF through Direct Print / PrintNode.
#     Zebra printers (name contains ZPL / ZD4 / Zebra / ZDesigner) still get ZPL. Same flow on the phone:
#     "Save & print label" -> label prints -> back to the checking screen ("Print again" if it failed).
# Creates 2 settings records once (no fields): paper format "IQ QC Label 62x30" and report entry "IQ QC Label 62x30"
#     (not shown in any print menu – only used to size the PDF).
# Printer: change the PRINTER_NAME below and rerun this installer in STAGING, or (without rerunning)
#     change Odoo Settings -> Technical -> System Parameters -> iq.qc_printnode_printer_id.
#     The ID is Odoo's internal printnode.printer database record ID (not PrintNode's cloud ID).
#     Use PRINTER_NAME = '' to preserve the existing system parameter on re-install.
#     Optional system parameter iq.qc_label_mode: pdf for Brother QL-800, zpl for Zebra ZD421.
#     Clear iq.qc_label_mode to let the QC page detect the mode from the printer's name.
# IMPORTANT: Renaming an existing quality tag in Odoo is required to fix its name in Odoo itself.

# EDIT HERE: Exact name of your Direct Print printer. Set '' to keep the existing selected printer.
# Examples: 'Brother_QL_800', 'Zebra ZD421' (use the actual name from Odoo Direct Print).
PRINTER_NAME = ''  # PRESERVE existing printer choice; set exact name only for initial setup

# 'download' = never send any job to the printer; show downloadable PDF on the TC22.
# 'print' = automatically send label to Direct Print/PrintNode (PDF download still available).
# Change this to 'print' ONLY when the Brother has been added to Odoo and tested.
LABEL_OUTPUT_MODE = 'print'
# Also adds the menu "QC Dashboard" in the Goods Receipts app (no separate menu file needed). After running: press F5.
# Run in PRODUCTION (after staging test): Scheduled Action (Model: Contact, Active = off) -> paste ALL -> Save -> Run Manually.
# Then: Settings -> Technical -> Logging, search "IQ QC": you should see 3 lines: "IQ QC page installed (v19.4)", "IQ QC menu added" and "IQ QC button added".

PAGE = r'''P = env['ir.config_parameter'].sudo()
KEY = P.get_param('iq.delivery_calendar_key') or ''
PW = P.get_param('iq.delivery_calendar_password') or ''
params = request.params if request else {}
h = 2166136261
for ch in (PW + '|' + KEY):
    h = ((h ^ ord(ch)) * 16777619) % 4294967296
h2 = 2166136261
for ch in (KEY + '#' + PW):
    h2 = ((h2 ^ ord(ch)) * 16777619) % 4294967296
TOKEN = '%08x%08x' % (h, h2)
authed = bool(PW) and request.httprequest.cookies.get('iq_cal') == TOKEN
LOGO = 'https://iq-dogsport.de/cdn/shop/files/iq-dogogsport-logo-sw-White.png?v=1761656363&width=240'
QB = '?key=' + KEY
QC = env['quality.check'].sudo()
QA = env['quality.alert'].sudo()
Tmpl = env['product.template'].sudo()
Prod = env['product.product'].sudo()
Pick = env['stock.picking'].sudo()
Att = env['ir.attachment'].sudo()
CF = QC.fields_get(['note', 'picking_id', 'quality_state', 'control_date', 'point_id'])
# standard Odoo checks created by a Quality Control Point ("QC Wareneingang") are not counted coats -> ignored on this page
AUTO = [('point_id', '=', False)] if 'point_id' in CF else []
NOTEMARK = '[HINWEIS]'
MISSING_HTML = '<p>Foto fehlt</p>'
AF = QA.fields_get(['title', 'tag_ids', 'check_id', 'description', 'picking_id', 'product_tmpl_id', 'product_id'])
PKF = Pick.fields_get(['purchase_id', 'return_id'])
# only supplier receipts: linked to a purchase order, no customer returns
SUPDOM = ([('purchase_id', '!=', False)] if 'purchase_id' in PKF else []) + ([('return_id', '=', False)] if 'return_id' in PKF else []) + [('name', 'not ilike', '/RET/')]
TAGMODEL = (AF.get('tag_ids') or {}).get('relation') or ''
TAG = env[TAGMODEL].sudo() if TAGMODEL and TAGMODEL in env else False
EN = request.httprequest.cookies.get('iq_qc_lang') == 'en'
now = datetime.datetime.now()
PN_ID = P.get_param('iq.qc_printnode_printer_id') or ''
PNP = env['printnode.printer'].sudo().browse(int(PN_ID)).exists() if PN_ID.isdigit() and 'printnode.printer' in env else False
LABEL_OUTPUT = P.get_param('iq.qc_label_output_mode') or 'download'
PRINT_ENABLED = LABEL_OUTPUT == 'print' and bool(PNP)
DPI = int(P.get_param('iq.qc_label_dpi') or (300 if PNP and '300' in (PNP.name or '') else 203))
PNU = (PNP.name or '').upper() if PNP else ''
MODE = ('brother-raw' if 'BROTHER' in PNU else (P.get_param('iq.qc_label_mode') or ('zpl' if [w for w in ['ZPL', 'ZD4', 'ZD2', 'ZEBRA', 'ZDESIGNER'] if w in PNU] else 'pdf')))
REP = env['ir.actions.report'].sudo().search([('report_name', '=', 'iq_qc.label_62x30')], limit=1)
today = now.date()
SIZES = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', '2XL', 'XXXL', '3XL', '4XL', '5XL', '6XL']
DEF_TAGS = ['Loch Brusttasche', 'Brusttasche defekt', 'Innentasche zugenäht', 'Naht offen', 'Lose Fäden', 'Fleck / Verschmutzung',
            'Reißverschluss defekt', 'Druckknopf defekt', 'Falsches Größenetikett', 'Stoff beschädigt', 'Nähfehler']

TAG_EN = {'Nähfehler': 'Sewing defect', 'Loch Brusttasche': 'Hole in chest pocket', 'Brusttasche defekt': 'Chest pocket defective', 'Innentasche zugenäht': 'Inner pocket sewn shut', 'Naht offen': 'Seam open', 'Lose Fäden': 'Loose threads', 'Fleck / Verschmutzung': 'Stain / dirt', 'Reißverschluss defekt': 'Zipper defective', 'Druckknopf defekt': 'Snap button defective', 'Falsches Größenetikett': 'Wrong size label', 'Stoff beschädigt': 'Fabric damaged'}
TR = [
    ('Lieferanten-Prüfungen', 'Supplier checks'), ('Prüfung durch den Lieferanten selbst – getrennt ausgewertet, nicht in den Zahlen oben.', 'Check done by the supplier – evaluated separately, not in the figures above.'),
    ('Lieferant wählen …', 'Choose supplier …'), ('Lieferanten-Prüfung auf diesem Gerät starten', 'Start supplier check on this device'),
    ('>Lieferant prüft selbst (Gastmodus)<', '>Supplier checks (guest mode)<'), ('>Mitgenommen<', '>Taken<'), ('>Datum<', '>Date<'), ('>Lieferant<', '>Supplier<'),
    ('Lieferantenprüfung', 'Supplier check'), ('>Produkt<', '>Product<'),
    ('Wareneingang melden<small>', 'Report arrived goods<small>'),
    ('Ware angekommen? Lieferschein + Menge erfassen', 'Goods arrived? Record delivery note + quantity'),
    ('Wer prüft? Bitte zuerst deinen Namen eingeben', 'Who is checking? Please enter your name first'),
    ('Dein Name – Pflichtfeld', 'Your name – required'),
    ('Der Name wird auf diesem Handy gemerkt.', 'The name is remembered on this phone.'),
    ('Bitte zuerst deinen Namen eingeben (oben)', 'Please enter your name first (top)'),
    ('Prüfer: ', 'Inspector: '),
    ('>ändern<', '>change<'),
    ('IQ Dogsport GmbH · Qualitätsprüfung Wareneingang', 'IQ Dogsport GmbH · Incoming goods quality inspection'),
    ('✓ Prüfung abgeschlossen', '✓ Quality check completed'),
    (' · Der QC-Bericht ist ein Endbericht.', ' · The QC report is a final report.'),
    ('Prüfung läuft', 'Check in progress'),
    (' · Der QC-Bericht ist ein Zwischenstand (nicht final).', ' · The QC report is an interim report (not final).'),
    ('Prüfung abschließen', 'Complete check'),
    ('Wieder öffnen', 'Reopen'),
    ('✓ Änderungen speichern', '✓ Save changes'),
    ('Danach Etikett neu drucken', 'Print a new label afterwards'),
    ('(optional – nur wenn ein neues Etikett gebraucht wird)', '(optional – only if a new label is needed)'),
    ('Nur die Änderungen werden gespeichert – es wird kein Etikett gedruckt (außer oben angehakt).', 'Only the changes are saved – no label is printed (unless ticked above).'),
    ('ZWISCHENSTAND – NICHT FINAL', 'INTERIM REPORT – NOT FINAL'),
    ('Die Qualitätsprüfung ist noch nicht abgeschlossen. Zahlen können sich bis zum Endbericht noch ändern.', 'The quality check is not completed yet. Numbers may still change until the final report.'),
    ('Der Druck-Knopf wird aktiv, sobald alle Fotos geladen sind.', 'The print button becomes active as soon as all photos are loaded.'),
    ('Fotos werden geladen …', 'Loading photos …'),
    (' – Endbericht', ' – final report'),
    (' – Zwischenstand', ' – interim'),
    ('Als Endbericht (final)', 'As final report'),
    ('Als Zwischenstand', 'As interim report'),
    ('Änderungen speichern', 'Save changes'),
    ('Vorhandene Fotos – zum Entfernen anhaken', 'Existing photos – tick to remove'),
    (' entfernen</span>', ' remove</span>'),
    ('>Bearbeiten<', '>Edit<'),
    ('Bearbeiten: ', 'Edit: '),
    ('Zu viele falsche Versuche', 'Too many wrong attempts'),
    (' (ganzer Karton)', ' (whole box)'),
    ('Karton(s) im Lager', 'box(es) in stock'),
    ('Karton(s) abgegeben', 'box(es) handed over'),
    ('>Karton abgegeben<', '>Box handed over<'),
    ('>Rückgängig<', '>Undo<'),
    ('Abgegeben: ', 'Handed over: '),
    ('In den Kartons (+ abgegeben) sind ', 'Boxes (+ handed over) contain '),
    (' Defekte mehr erfasst als verpackt oder abgegeben.', ' defects more than packed or handed over.'),
    ('Defekte Teile, die nicht mehr bei uns sind (z. B. vom Lieferanten mitgenommen). Sie zählen im Vergleich mit, kommen aber in keinen Karton.', 'Defective pieces that are no longer here (e.g. taken by the supplier). They count in the comparison but go into no box.'),
    ('Wer / wohin? z. B. Holfelder mitgenommen', 'Who / where? e.g. taken by Holfelder'),
    ('Bereits abgegeben', 'Already handed over'),
    ('Abgabe erfassen', 'Record handover'),
    ('Abgabe speichern', 'Save handover'),
    ('Nichts abgegeben.', 'Nothing handed over.'),
    ('Größe unbekannt', 'Size unknown'),
    ('>Abgegeben<', '>Handed over<'),
    ('>abgegeben<', '>handed over<'),
    (' abgegeben ·', ' handed over ·'),
    ('In den Kartons sind ', 'The boxes contain '),
    (' Teile mehr als in Odoo erfasst.', ' pieces more than recorded in Odoo.'),
    ('In Odoo sind ', 'Odoo has '),
    (' Defekte mehr erfasst als verpackt.', ' defects more than packed.'),
    ('Ohne Scanner: Größe antippen (+1).', 'No scanner: tap the size (+1).'),
    ('Noch leer – erstes Teil scannen.', 'Still empty – scan the first piece.'),
    ('Barcode scannen …', 'Scan barcode …'),
    ('Leeren Karton löschen', 'Delete empty box'),
    ('„? (ohne Größe)“ = Defekte aus dem Papier-Import ohne Größe – sie liegen in den Kartons unter ihrer echten Größe.', '“? (no size)” = defects from the paper import without size – in the boxes they are under their real size.'),
    ('? (ohne Größe)', '? (no size)'),
    ('Fehlende Defekte nachtragen: ', 'Add missing defects: '),
    ('als Führungskraft anmelden', 'log in as manager'),
    ('>Inhalt<', '>Contents<'),
    ('Stk. verpackt', 'pcs packed'),
    ('Odoo: ', 'Odoo: '),
    (' Defekte</small>', ' defects</small>'),
    (' beginnen</button>', ' – start</button>'),
    ('ohne Lieferung', 'no delivery'),
    ('>Öffnen<', '>Reopen<'),
    ('>Etikett<', '>Label<'),
    ('>offen<', '>open<'),
    ('>abgeschlossen<', '>closed<'),
    ('Noch keine Kartons.', 'No boxes yet.'),
    ('← Alle Produkte', '← All products'),
    ('Defekte verpacken', 'Pack defects'),
    ('Verpacken', 'Packing'),
    ('Kalender', 'Calendar'),
    ('Abmelden', 'Log out'),
    ('Anmelden – Führungskraft', 'Manager login'),
    ('Nur für Führungskräfte', 'Managers only'),
    ('Karton abschließen &amp; Etikett drucken', 'Close box &amp; print label'),
    ('Vergleich: Odoo ↔ Kartons', 'Comparison: Odoo ↔ boxes'),
    ('Fehlende in Odoo nachtragen', 'Add missing to Odoo'),
    ('Jetzt in Odoo nachtragen', 'Add to Odoo now'),
    ('Alle Kartons', 'All boxes'),
    ('Neuer Karton', 'New box'),
    ('Odoo Defekte', 'Odoo defects'),
    ('In Kartons', 'In boxes'),
    ('Differenz', 'Difference'),
    ('Karton(s)', 'box(es)'),
    ('Karton ', 'Box '),
    ('Bekleidung aus offenen Wareneingängen (Erwartet / Teilweise gebucht). „Prüfen starten“ öffnet die Prüfung mit dieser Lieferung.', 'Clothing from open goods receipts (expected / partly booked). “Start checking” opens the check with this delivery.'),
    ('Keine Zeichnung – <u>einrichten</u>', 'No drawing – <u>set up</u>'),
    ('Zu prüfen – offene Wareneingänge', 'To check – open goods receipts'),
    ('>Standard-Zeichnung<', '>Standard drawing<'),
    ('✓ Eigene Zeichnung', '✓ Own drawing'),
    ('Prüfen starten →', 'Start checking →'),
    ('>Überfällig<', '>Overdue<'),
    (' · erwartet ', ' · expected '),
    ('Eigene Zeichnung löschen (zurück zur Standard-Zeichnung)', 'Delete own drawing (back to the standard drawing)'),
    ('Noch kein Bild für diese Seite.', 'No picture for this side yet.'),
    ('Von anderem Produkt übernehmen', 'Copy from another product'),
    ('Bild dieser Seite entfernen', 'Remove picture of this side'),
    ('Zeichnungen einrichten', 'Set up drawings'),
    ('Teile auf dieser Seite', 'Parts on this side'),
    ('Zeichnung einrichten', 'Set up drawing'),
    ('Zeichnung speichern', 'Save drawing'),
    ('Bild hochladen', 'Upload picture'),
    ('>Start<', '>Start<'),
    ('</b> Grund <small>', '</b> Reason <small>'),
    ('</b> Was ist auffällig? <small>', '</b> What is noticeable? <small>'),
    ('Anderer Grund? Hier alle Gründe A–Z …', 'Other reason? All reasons A–Z here …'),
    ('aria-label="Weitere Gründe"', 'aria-label="More reasons"'),
    ('Abbrechen – Hinweis löschen', 'Cancel – delete note'),
    ('Abbrechen – Defekt löschen', 'Cancel – delete defect'),
    ('<small>– antippen</small>', '<small>– tap</small>'),
    ('Neuer Grund (eingeben) …', 'New reason (type) …'),
    ('Foto aufnehmen</button>', 'Take photo</button>'),
    ('Nächstes Teil scannen', 'Scan next item'),
    ('"✓ Gespeichert"', '"✓ Saved"'),
    ('>← Zurück<', '>← Back<'),
    ('Beim Klick werden alle Fehler und Fotos gespeichert und das Etikett-PDF erstellt.', 'This saves all defects and photos and creates the label PDF.'),
    ('Beim Drucken werden alle Fehler und Fotos gespeichert und ein Etikett gedruckt.', 'Printing saves all defects and photos and prints one label.'),
    ("'Zuerst auf der Zeichnung antippen, wo der Fehler ist (Schritt 2).'", "'First tap the drawing where the defect is (step 2).'"),
    ("'Bitte auf der Zeichnung antippen, wo der Fehler ist (Schritt 2).'", "'Please tap the drawing where the defect is (step 2).'"),
    ('Gespeichert – Etikett-PDF herunterladen und an die Jacke kleben', 'Saved – download the label PDF and stick it on the garment'),
    ("'Ohne Foto weiter? Nur wenn wirklich kein Foto möglich ist.'", "'Continue without a photo? Only if a photo is really not possible.'"),
    ("'Nächster Fehler: Grund wählen – oder Fehler-Liste drucken'", "'Next defect: choose a reason – or print the list'"),
    ("'Auf die Zeichnung tippen – Vorne / Hinten / Innen'", "'Tap the drawing – Front / Back / Inside'"),
    ('Vorne · Front-Reißverschluss / Leiste / Druckknöpfe', 'Front · front zip / placket / snaps'),
    ("'Bitte ein Foto vom Fehler aufnehmen (Schritt 3).'", "'Please take a photo of the defect (step 3).'"),
    ('Hinweis wird mit Fotos gespeichert. Kein Etikett.', 'Note is saved with its photos. No label.'),
    ("'Schritt 2: Ort auf der Zeichnung antippen'", "'Step 2: tap the place on the drawing'"),
    ('Hinten · Zip-off (Reißverschluss Unterteil)', 'Back · zip-off (lower part zip)'),
    ('Vorne · Zip-off (Reißverschluss Unterteil)', 'Front · zip-off (lower part zip)'),
    ('Gespeichert – Etikett an die Jacke kleben', 'Saved – stick the label on the garment'),
    ('Vorne · Brusttasche links (RV) / IQ-Logo', 'Front · left chest zip pocket / IQ logo'),
    ("'Zuerst den Grund wählen (Schritt 1).'", "'First choose the reason (step 1).'"),
    ('Zuerst Ort auf der Zeichnung wählen ②', 'First choose the place on the drawing ②'),
    ('Vorne · Schulter rechts / RV-Tasche', 'Front · right shoulder / zip pocket'),
    ('Vorne · Brusttasche links / IQ-Logo', 'Front · left chest pocket / IQ logo'),
    ('Grund eingeben, z. B. Kordel fehlt', 'Type the reason, e.g. cord missing'),
    ('+ Weiteren Hinweis an dieser Jacke', '+ Another note on this garment'),
    ('Vorne · Schulter links / RV-Tasche', 'Front · left shoulder / zip pocket'),
    ('+ Weiteren Fehler an dieser Jacke', '+ Another defect on this garment'),
    ('Vorne · Pattentasche unten rechts', 'Front · right lower flap pocket'),
    ('Vorne · Seitentasche rechts (RV)', 'Front · right side zip pocket'),
    ('Vorne · Pattentasche unten links', 'Front · left lower flap pocket'),
    ('Hinten · Klett-Patch Ärmel links', 'Back · left sleeve velcro patch'),
    ('Vorne · Seitentasche links (RV)', 'Front · left side zip pocket'),
    ('Vorne · Brusttasche rechts (RV)', 'Front · right chest zip pocket'),
    ('Vorne · Ärmeltasche rechts (RV)', 'Front · right sleeve zip pocket'),
    ('Vorne · Klett-Patch Ärmel links', 'Front · left sleeve velcro patch'),
    ('Innen · Magnetfach unten rechts', 'Inside · lower right magnet pocket'),
    ('Vorne · Reißverschluss / Leiste', 'Front · zip / placket'),
    ('Innen · Magnetfach oben rechts', 'Inside · right upper magnet pocket'),
    ('<h2 id="defno">Hinweis 1</h2>', '<h2 id="defno">Note 1</h2>'),
    ('Vorne · Brust links / IQ-Logo', 'Front · left chest / IQ logo'),
    ('Innen · Magnetfach oben links', 'Inside · left upper magnet pocket'),
    ('Vorne · Tasche / Seite rechts', 'Front · right pocket / side'),
    ('<h2 id="defno">Fehler 1</h2>', '<h2 id="defno">Defect 1</h2>'),
    ('Vorne · Bauch / Seite rechts', 'Front · right belly / side'),
    ('Vorne · Tasche / Seite links', 'Front · left pocket / side'),
    ("'Schritt 3: Foto aufnehmen'", "'Step 3: take a photo'"),
    ('Hinten · Gürtel / Schlaufen', 'Back · belt / loops'),
    ('Hinten · Große Rückentasche', 'Back · big back pocket'),
    ('Hinten · Saum / Druckknöpfe', 'Back · hem / snaps'),
    ('Vorne · Bauch / Seite links', 'Front · left belly / side'),
    ("'Schritt 1: Grund wählen.'", "'Step 1: choose a reason.'"),
    ('Anderer Grund (eingeben) …', 'Other reason (type) …'),
    ('Hinten · Patch Ärmel links', 'Back · left sleeve patch'),
    ('Innen · Ärmelfutter rechts', 'Inside · right sleeve lining'),
    ('Vorne · Brusttasche rechts', 'Front · right chest pocket'),
    ('Innen · Innentasche rechts', 'Inside · right inner pocket'),
    ("'Schritt 1: Grund wählen'", "'Step 1: choose a reason'"),
    ("'Foto wird vorbereitet …'", "'Preparing photo …'"),
    ('Vorne · Patch Ärmel links', 'Front · left sleeve patch'),
    ('Hinten · Unterteil rechts', 'Back · right lower part'),
    ('Innen · Innentasche links', 'Inside · left inner pocket'),
    ('Innen · Ärmelfutter links', 'Inside · left sleeve lining'),
    ('Vorne · Gürtel / Schnalle', 'Front · belt / buckle'),
    ('Hinweise an dieser Jacke', 'Notes on this garment'),
    ('Vorne · Unterteil rechts', 'Front · right lower part'),
    ('Hinten · Schulter rechts', 'Back · right shoulder'),
    ('Hinten · Unterteil links', 'Back · left lower part'),
    ('Hinten · Bündchen rechts', 'Back · right cuff'),
    ('Innen · Nacken / Etikett', 'Inside · neck / label'),
    ('Innen · Futter Unterteil', 'Inside · lower part lining'),
    ('Hinten · Kragen / Kapuze', 'Back · collar / hood'),
    ("?'Hinweis(e)':'Fehler')", "?'note(s)':'defect(s)')"),
    ('label="Alle Gründe A–Z"', 'label="All reasons A–Z"'),
    ('Vorne · Schulter rechts', 'Front · right shoulder'),
    ('Vorne · Unterteil links', 'Front · left lower part'),
    ('Vorne · Bündchen rechts', 'Front · right cuff'),
    ('Hinten · Schulter links', 'Back · left shoulder'),
    ('Hinten · Bündchen links', 'Back · left cuff'),
    ('Vorne · Kragen / Kapuze', 'Front · collar / hood'),
    ("'Ohne Foto (Ausnahme)'", "'No photo (exception)'"),
    ('Fehler an dieser Jacke', 'Defects on this garment'),
    ('Vorne · Schulter links', 'Front · left shoulder'),
    ('Vorne · Bündchen links', 'Front · left cuff'),
    ('Zuerst Grund wählen ①', 'First choose the reason ①'),
    ('Hinten · Rücken Mitte', 'Back · mid back'),
    ('Hinten · Ärmel rechts', 'Back · right sleeve'),
    ('Innen · Futter rechts', 'Inside · right lining'),
    ('Innen · Zip-off innen', 'Inside · zip-off inside'),
    ('Hinten · Rücken unten', 'Back · lower back'),
    ('Hinten · Seite rechts', 'Back · right side'),
    ("'Hinweis ':'Fehler '", "'Note ':'Defect '"),
    ('"Kein Defekt · Gr. "', '"No defect found · Size "'),
    ('Vorne · Brust rechts', 'Front · right chest'),
    ('Vorne · MagDock-Clip', 'Front · MagDock clip'),
    ('Vorne · Ärmel rechts', 'Front · right sleeve'),
    ('Hinten · Rücken oben', 'Back · upper back'),
    ('Hinten · Ärmel links', 'Back · left sleeve'),
    ('Innen · Futter links', 'Inside · left lining'),
    ('Hinten · Saum / Bund', 'Back · hem / waistband'),
    ('Hinten · Seite links', 'Back · left side'),
    ("'Speichert + lädt '", "'Saving + uploading '"),
    ('Vorne · Ärmel links', 'Front · left sleeve'),
    ('Hinten · Saum unten', 'Back · hem'),
    ('Vorne · Brust links', 'Front · left chest'),
    ('Vorne · Saum / Bund', 'Front · hem / waistband'),
    ('Foto nicht möglich', 'Photo not possible'),
    ('Wo ist der Fehler?', 'Where is the defect?'),
    ('Was ist auffällig?', 'What is noticeable?'),
    ('</b> Grund</label>', '</b> Reason</label>'),
    ('Vorne · Saum unten', 'Front · hem'),
    ("' · alles bereit'", "' · ready'"),
    ("'+ weiteres Foto'", "'+ another photo'"),
    ("' Foto(s) hoch …'", "' photo(s) …'"),
    ("confirm('Fehler '", "confirm('Remove defect '"),
    ("'Foto aufnehmen'", "'Take photo'"),
    ("'Foto entfernen'", "'Remove photo'"),
    ('– Grund wählen –', '– choose a reason –'),
    ('Notiz (optional)', 'Note (optional)'),
    ("+' entfernen?')", "+'?')"),
    ('Foto vom Fehler', 'Photo of the defect'),
    (':"Kein Defekt"}', ':"No defect found"}'),
    ('Hinten · Kapuze', 'Back · hood'),
    ('label="Häufig"', 'label="Most used"'),
    ('> Foto <small>', '> Photo <small>'),
    ('Vorne · Kapuze', 'Front · hood'),
    ('>Kein Defekt<', '>No defect found<'),
    ("'Hinweis(e)'", "'note(s)'"),
    ('> Grund</li>', '> Reason</li>'),
    ("'ohne Foto'", "'no photo'"),
    ('> Foto</li>', '> Photo</li>'),
    ("' Foto(s)'", "' photo(s)'"),
    ('Wo ist es?', 'Where is it?'),
    ('> Wo?</li>', '> Where?</li>'),
    ('Vorne · Ärmel links', 'Front · left sleeve'),
    ('Vorne · Saum / Bund', 'Front · hem / waistband'),
    ('Vorne · Seite links', 'Front · left side'),
    ('Innen · Futter links', 'Inside · left lining'),
    ('Hinten · Ärmel links', 'Back · left sleeve'),
    ('Hinten · Saum / Bund', 'Back · hem / waistband'),
    ('Hinten · Rücken oben', 'Back · upper back'),
    ('Vorne · Ärmel rechts', 'Front · right sleeve'),
    ('Vorne · Seite rechts', 'Front · right side'),
    ('Innen · Futter rechts', 'Inside · right lining'),
    ('Hinten · Ärmel rechts', 'Back · right sleeve'),
    ('Vorne · Zip-off-Linie', 'Front · zip-off line'),
    ('Hinten · Zip-off-Linie', 'Back · zip-off line'),
    ('Vorne · Bündchen links', 'Front · left cuff'),
    ('Vorne · Schulter links', 'Front · left shoulder'),
    ('Hinten · Bündchen links', 'Back · left cuff'),
    ('Hinten · Schulter links', 'Back · left shoulder'),
    ('Vorne · Bündchen rechts', 'Front · right cuff'),
    ('Vorne · Unterteil links', 'Front · left lower part'),
    ('Vorne · Schulter rechts', 'Front · right shoulder'),
    ('Vorne · Kragen / Kapuze', 'Front · collar / hood'),
    ('Hinten · Bündchen rechts', 'Back · right cuff'),
    ('Hinten · Unterteil links', 'Back · left lower part'),
    ('Hinten · Schulter rechts', 'Back · right shoulder'),
    ('Hinten · Kragen / Kapuze', 'Back · collar / hood'),
    ('Vorne · Unterteil rechts', 'Front · right lower part'),
    ('Innen · Ärmelfutter links', 'Inside · left sleeve lining'),
    ('Innen · Innentasche links', 'Inside · left inner pocket'),
    ('Hinten · Unterteil rechts', 'Back · right lower part'),
    ('Hinten · Seitennaht links', 'Back · left side seam'),
    ('Innen · Ärmelfutter rechts', 'Inside · right sleeve lining'),
    ('Innen · Innentasche rechts', 'Inside · right inner pocket'),
    ('Hinten · Seitennaht rechts', 'Back · right side seam'),
    ('Vorne · Tasche unten links', 'Front · left lower pocket'),
    ('Vorne · Tasche unten rechts', 'Front · right lower pocket'),
    ('Ganze Jacke / mehrere Stellen', 'Whole garment / several places'),
    ('Innen · Kragen innen / Etikett', 'Inside · inside collar / label'),
    ('Vorne · Brust / Brusttasche links', 'Front · left chest / chest pocket'),
    ('Vorne · Brust / Brusttasche rechts', 'Front · right chest / chest pocket'),
    ('Vorne · Reißverschluss / Leiste / Knöpfe', 'Front · front zip / placket / snaps'),
    ('Hinten · Rücken Mitte / Rückentasche / RV', 'Back · mid back / back pocket / back zip'),
    ('Fehler an dieser Jacke', 'Defects on this garment'),
    ('+ Fehler hinzufügen', '+ Add defect'),
    ('Noch kein Fehler hinzugefügt – Grund wählen, auf die Zeichnung tippen, dann „+ Fehler hinzufügen“ oder direkt drucken.', 'No defect added yet – choose a reason, tap the drawing, then "+ Add defect" or print directly.'),
    ('Wo ist der Fehler?', 'Where is the defect?'),
    ('Wo ist es?', 'Where is it?'),
    ('Rechts/links immer vom Träger aus gesehen.', 'Right/left always as seen by the wearer.'),
    ('Rechts/links vom Träger aus gesehen. Zahl = Anzahl Defekte an dieser Stelle.', 'Right/left as seen by the wearer. Number = defects at this place.'),
    ('Ort: noch nicht gewählt – auf die Zeichnung tippen', 'Place: not chosen yet – tap the drawing'),
    ('Wo sind die Defekte?', 'Where are the defects?'),
    ('Defekte mit Ort', 'defects with place'),
    ('Kein Foto – die Zeichnung zeigt die Stelle', 'No photo – the drawing shows the place'),
    ('Kein Foto (optional)', 'No photo (optional)'),
    ('Fotos sind optional.', 'Photos are optional.'),
    ('Weitere Fotos (optional)', 'More photos (optional)'),
    ('Foto zu Fehler', 'Photo for defect'),
    ('Fehlergrund + Ort', 'Defect reason + place'),
    ('Mantel / Parka', 'Coat / parka'),
    ('>Jacke<', '>Jacket<'),
    ('>Vorne<', '>Front<'),
    ('>Hinten<', '>Back<'),
    ('>Innen<', '>Inside<'),
    ('>Vorne (', '>Front ('),
    ('>Hinten (', '>Back ('),
    ('>Innen (', '>Inside ('),
    ('"Vorne"', '"Front"'),
    ('"Hinten"', '"Back"'),
    ('"Innen"', '"Inside"'),
    ('Alle Orte', 'All places'),
    ('>Ort<', '>Place<'),
    ('Ort: ', 'Place: '),
    ('ohne Ort', 'no place'),
    ('Nähfehler', 'Sewing defect'),
    ('Prüfungen heute nach Prüfer', 'Checks today by inspector'),
    ('Prüfungen nach Prüfer', 'Checks by inspector'),
    ('Keine Prüfungen im gewählten Zeitraum.', 'No checks in the selected period.'),
    ('Weitere Fehlergründe', 'More defect reasons'),
    ('Grund suchen', 'Search reasons'),
    ('Ausgewählt:', 'Selected:'),
    ('Foto erforderlich – mindestens ein Foto hochladen.', 'Photo required – upload at least one photo.'),
    ('Mindestens ein Foto ist Pflicht, bevor Sie fortfahren.', 'At least one photo is required before continuing.'),
    ('Prüfungen heute', 'Checks today'),
    ('Zeitraum auswählen', 'Select period'),
    ('Prüfer auswählen', 'Select inspector'),
    ('Alle Prüfer', 'All inspectors'),
    ('Prüfer nicht angegeben', 'Inspector not recorded'),
    ('Keine Prüfungen heute für dieses Produkt.', 'No checks today for this product.'),
    ('Heute: alle Prüfer', 'Today: all inspectors'),
    ('Tagesübersicht', 'Daily summary'),
    ('Zeitraum', 'Period'),
    ('Letzte 7 Tage', 'Last 7 days'),
    ('Letzte 30 Tage', 'Last 30 days'),
    ('Alle Zeiträume', 'All periods'),
    ('Anzeige filtern', 'Filter results'),
    ('Filter zurücksetzen', 'Reset filters'),
    ('Nur angezeigte Prüfungen und Defekte', 'Only matching checks and defects'),
    ('Keine Ergebnisse für diese Auswahl.', 'No results for this selection.'),
    ('Schritt 1 von 2', 'Step 1 of 2'),
    ('Schritt 2 von 2', 'Step 2 of 2'),
    ('Fertig – zurück zu den Details', 'Done – back to details'),
    ('Fotos · sofortiger Upload', 'Photos · instant upload'),
    ('Foto(s) hochgeladen', 'photo(s) uploaded'),
    ('Foto nicht hochgeladen', 'Photo not uploaded'),
    ('Foto leer oder größer als 12 MB', 'Photo empty or larger than 12 MB'),
    ('Nochmal drucken', 'Print again'),
    ('Zurück zu den Details', 'Back to details'),
    ('Etikett an die Jacke kleben, dann fotografieren', 'Stick the label on the jacket, then take photos'),
    ('Fertig – nächstes Teil scannen', 'Done – scan next item'),
    ('Hinweis speichern – weiter zu Fotos', 'Save note – continue to photos'),
    ('Druckauftrag an Brother gesendet', 'Print job sent to Brother'),
    ('Der Defekt wird jetzt gespeichert. Danach das PDF herunterladen, Etikett aufkleben und fotografieren.', 'The defect will be saved. Download the PDF, attach the label, then take photos.'),
    ('Etikett-PDF bereit. Herunterladen, aufkleben, dann fotografieren.', 'Label PDF ready. Download, attach, then photograph.'),
    ('Etikett-PDF herunterladen', 'Download label PDF'),
    ('Etikett-PDF erstellen', 'Create label PDF'),
    ('PDF bereit – noch kein Druckauftrag gesendet', 'PDF ready – no print job sent'),
    ('PDF herunterladen', 'Download PDF'),
    ('Hinweis gespeichert – jetzt fotografieren', 'Note saved – now take photos'),
    ('Etikett drucken – dann fotografieren', 'Print label – then take photos'),
    ('Foto wird hochgeladen …', 'Photo uploading …'),
    ('Foto hochgeladen', 'Photo uploaded'),
    ('Upload wiederholen', 'Retry upload'),
    ('Nochmal drucken', 'Print again'),
    ('Im Browser drucken', 'Print in browser'),
    ('Foto hinzufügen', 'Add photo'),
    ('Foto fehlt', 'Photo missing'),
    ('Fotos aufnehmen', 'Take photos'),
    ('Ohne Foto beenden?', 'Finish without a photo?'),
    ('Ohne Foto gespeichert', 'Saved without photo'),
    ('Abbrechen und Defekt löschen', 'Cancel and delete defect'),
    ('Abbrechen und Hinweis löschen', 'Cancel and delete note'),
    ('Zurück zu den Details', 'Back to details'),
    ('10 Defekte (nicht gebucht), 8 Hinweise', '10 defects (not booked), 8 notes'),
    ('Defekte, ', 'defects, '),
    (' Hinweise und ', ' notes and '),
    ('Hinweis – kein Defekt: das Teil ist in Ordnung und wird gebucht. Fotos als Nachweis für den Lieferanten. Kein Etikett.', 'Note – not a defect: the piece is OK and will be booked. Photos as proof for the supplier. No label.'),
    ('Auffällig, aber in Ordnung: diese Teile werden gebucht. Fotos zum Nachweis für den Lieferanten, im Auge behalten.', 'Unusual but acceptable: these pieces are booked. Photos as proof for the supplier – keep an eye on it.'),
    ('Kein offener Wareneingang für dieses Produkt. QC ist nur für offene (noch nicht gebuchte) Wareneingänge.', 'No open receipt for this product. QC is only for open (not yet booked) receipts.'),
    ('ist schon gebucht – QC nur für offene Wareneingänge. Bitte andere Lieferung wählen.', 'is already booked – QC only for open receipts. Please choose another delivery.'),
    ('Lieferung schon gebucht – QC nur für offene Wareneingänge. Nichts gespeichert.', 'Delivery already booked – QC only for open receipts. Nothing saved.'),
    ('Prüfungen ohne Größe (Papier-Import) sind hier nicht enthalten.', 'checks without size (paper import) are not included here.'),
    ('Gebucht wird nur „OK“: Button „QC: OK-Mengen übernehmen“ im Wareneingang (Aktionsmenü), danach Prüfen/Validieren in Odoo. Defekte und nicht geprüfte Teile werden nicht gebucht.', 'Only "OK" is booked: button "QC: OK-Mengen übernehmen" on the receipt (Action menu), then Validate in Odoo. Defective and unchecked pieces are not booked.'),
    ('gespeichert (kein Defekt, wird gebucht)', 'saved (not a defect, will be booked)'),
    ('Hinweise (kein Defekt)', 'notes (not a defect)'),
    ('! Hinweis – kein Defekt', '! Note – not a defect'),
    ('Hinweise – kein Defekt', 'Notes – not a defect'),
    ('Hinweis – kein Defekt', 'Note – not a defect'),
    ('Hinweis erfassen', 'Record note'),
    ('Hinweis speichern', 'Save note'),
    ('Was ist auffällig?', 'What is unusual?'),
    ('Buchungsübersicht', 'Booking overview'),
    ('OK – wird gebucht', 'OK – will be booked'),
    ('Defekt – nicht gebucht', 'Defect – not booked'),
    ('davon Hinweis', 'of which note'),
    ('Nicht geprüft', 'Not checked'),
    ('Geliefert', 'Delivered'),
    ('(schon gebucht)', '(already booked)'),
    ('(offen)', '(open)'),
    ('Letzte Eingaben', 'Last entries'),
    ('Noch nichts gespeichert.', 'Nothing saved yet.'),
    ('mehr als geliefert', 'more than delivered'),
    ('Summe', 'Total'),
    ('Größe gewählt', 'Size chosen'),
    ('Gescannt', 'Scanned'),
    ('Größenauswahl ausblenden', 'Hide size buttons'),
    ('Keine Lieferung gewählt – Zahlen gelten für alle Lieferungen.', 'No delivery chosen – numbers are for all deliveries.'),
    ('Lieferung wählen →', 'Choose delivery →'),
    ('alle Lieferungen', 'all deliveries'),
    ('Bitte zuerst Prüfer-Name eingeben (unten)', 'Please enter the inspector name first (below)'),
    ('Doppelt gescannt? Nicht gezählt', 'Scanned twice? Not counted'),
    ('Mehr als geliefert – bitte OK selbst tippen', 'More than delivered – please tap OK yourself'),
    ('mehr geprüft als geliefert', 'more checked than delivered'),
    ('alle geprüft', 'all checked'),
    ('Trotzdem speichern?', 'Save anyway?'),
    ('Fortschritt dieser Lieferung (geprüft / geliefert)', 'Progress of this delivery (checked / delivered)'),
    ('Letzter war Defekt', 'Last one was defective'),
    ('Etikett scannen – oder Größe unten manuell wählen', 'Scan the label – or choose the size manually below'),
    ('Nächstes Etikett scannen', 'Scan the next label'),
    ('Etikett scannen', 'Scan the label'),
    ('Größe manuell wählen (Etikett nicht lesbar)', 'Choose size manually (label not readable)'),
    ('Auto-OK: jeder Scan = 1× OK', 'Auto-OK: every scan = 1× OK'),
    ('Barcode eintippen', 'Type barcode'),
    ('Barcode nicht gefunden', 'Barcode not found'),
    ('Gewechselt zu', 'Switched to'),
    ('Bitte Lieferung für dieses Produkt wählen', 'Please choose the delivery for this product'),
    ('ohne Lieferung – kein offener Wareneingang gefunden', 'no delivery – no open receipt found'),
    ('Alle Größen', 'All sizes'),
    ('Alle Gründe', 'All reasons'),
    ('nachgetragen', 'added afterwards'),
    ('Kein Foto', 'No photo'),
    ('Gleiches Passwort wie der Lagerkalender. Einmal pro Handy, dann 30 Tage gemerkt.', 'Same password as the warehouse calendar. Once per phone, then remembered for 30 days.'),
    ('Rot = Defektquote ab 10 %, Gelb = ab 5 %, Grün = darunter. Klick auf ein Produkt zeigt Größen, Gründe und alle Fotos.', 'Red = defect rate 10 % or more, yellow = 5 % or more, green = below. Click a product to see sizes, reasons and all photos.'),
    ('Rückgängig nur bis 15 Minuten nach dem Speichern.', 'Undo is only possible up to 15 minutes after saving.'),
    ('Bitte einen Fehlergrund wählen oder eingeben.', 'Please choose or type a defect reason.'),
    ('Bitte einen Fehlergrund wählen.', 'Please choose a defect reason.'),
    ('Bitte mindestens ein Foto aufnehmen.', 'Please take at least one photo.'),
    ('Keine Verbindung – nicht gespeichert', 'No connection – not saved'),
    ('Keine Verbindung – bitte nochmal.', 'No connection – please try again.'),
    ('Nichts gefunden. Bitte oben suchen.', 'Nothing found. Please search above.'),
    ('Produkt suchen, z. B. Wintermantel', 'Search product, e.g. winter coat'),
    ('Produkt oder Grund suchen', 'Search product or reason'),
    ('z. B. Stelle, Größe des Lochs', 'e.g. position, size of the hole'),
    ('Speichern &amp; Etikett drucken', 'Save &amp; print label'),
    ('Speichern & Etikett drucken', 'Save & print label'),
    ('Anderer Grund (neu eingeben)', 'Other reason (type a new one)'),
    ('Drucken / als PDF speichern', 'Print / save as PDF'),
    ('Letzte Eingabe löschen?', 'Delete the last entry?'),
 (' wirklich löschen? Fotos und Prüfung werden mit gelöscht.', ' – really delete? Photos and the check are deleted too.'),
 (' gespeichert · Etikett gedruckt', ' saved · label printed'),
 (' gespeichert – Etikett NICHT gedruckt (', ' saved – label NOT printed ('),
 (' · Etikett gedruckt', ' · label printed'),
 ('Druck fehlgeschlagen: ', 'Printing failed: '),
 ('Defekt nicht gefunden', 'Defect not found'),
 ('Nochmal drucken', 'Print again'),
 ('Gedruckt', 'Printed'),
 ('>Löschen<', '>Delete<'),
 ('Wie viele OK-Teile in dieser Größe?', 'How many OK pieces in this size?'),
 ('Lieferung ändern', 'Change delivery'),
 ('Lieferung: ', 'Delivery: '),
 ('Wareneingang ', 'Receipt '),
 (' Stück', ' pcs'),
 ('>Anzahl<', '>Qty<'),
    ('Prüfer auf diesem Handy', 'Inspector on this phone'),
    ('2 · Zu welcher Lieferung?', '2 · Which delivery?'),
    ('Qualitätsprüfbericht', 'Quality inspection report'),
    ('Qualitätskontrolle', 'Quality control'),
    ('Letzte Prüfberichte', 'Latest QC reports'),
    ('Produkt / Lieferung', 'Product / delivery'),
 ('× ohne Lieferung', '× no delivery'),
 (' · zuletzt ', ' · last '),
    ('Produkt nicht gefunden', 'Product not found'),
    ('Etikett nicht gefunden', 'Label not found'),
    ('Ohne Lieferung prüfen', 'Check without delivery'),
    ('QC-Bericht erstellen', 'Create QC report'),
    ('Etikett neu drucken', 'Reprint label'),
    ('Etikett drucken', 'Print label'),
    ('Noch keine Prüfungen.', 'No checks yet.'),
    ('Rückgängig gemacht', 'Undone'),
    ('Name (wird gemerkt)', 'Name (remembered)'),
    ('Neueste Defekte', 'Latest defects'),
    ('Alle Lieferungen', 'All deliveries'),
    ('Alle Defekte', 'All defects'),
    ('1 · Produkt wählen', '1 · Choose product'),
    ('1 · Größe wählen', '1 · Choose size'),
    ('Lieferung wählen', 'Choose delivery'),
    ('2 · Fehlergrund', '2 · Defect reason'),
    ('3 · Notiz (optional)', '3 · Note (optional)'),
    ('Größen/Varianten', 'sizes/variants'),
    ('Defekt erfassen', 'Record defect'),
    ('OK gespeichert', 'OK saved'),
    ('Prüfen starten', 'Start checking'),
    ('Weiter prüfen', 'Continue checking'),
    ('Zuletzt geprüft', 'Recently checked'),
    ('ohne Lieferung', 'no delivery'),
    ('Keine Defekte', 'No defects'),
    ('Fehlergründe', 'Defect reasons'),
    ('Team-Passwort', 'Team password'),
    ('Falsches Passwort.', 'Wrong password.'),
    ('Suchergebnis', 'Search results'),
    ('Defektquote', 'Defect rate'),
    ('Nach Größe', 'By size'),
    ('ohne Grund', 'without reason'),
    ('Rückgängig', 'Undo'),
    ('Speichert …', 'Saving …'),
    ('Größe fehlt', 'Size missing'),
    ('<br>gebucht</small>', '<br>booked</small>'),
    ('<br>offen</small>', '<br>open</small>'),
    ('<b>+</b>Foto', '<b>+</b>Photo'),
    ('1 · Fotos', '1 · Photos'),
    ('Abbrechen', 'Cancel'),
    ('Anmelden', 'Sign in'),
    ('Gelöscht', 'Deleted'),
    ('Zuletzt: ', 'Last: '),
    ('Lieferung ', 'Delivery '),
    ('← Zurück', '← Back'),
    ('>Zurück<', '>Back<'),
    ('Geprüft', 'Checked'),
    ('Produkte', 'Products'),
    ('>Produkt<', '>Product<'),
    ('Bericht', 'Report'),
    ('Größe', 'Size'),
    ('Anzahl', 'Count'),
    ('Anteil', 'Share'),
    ('>Quote<', '>Rate<'),
    ('>Grund<', '>Reason<'),
    ('In Odoo öffnen', 'Open in Odoo'),
    ('Stand ', 'As of '),
    ('>Heute<', '>Today<'),
    ('7 Tage', '7 days'),
    ('30 Tage', '30 days'),
    ('>Gesamt<', '>All time<'),
    ('DEFEKT', 'DEFECT'),
    ('Defekt', 'Defect'),
    ('Defekt', 'Defect'),
    ('"Fehler"', '"Error"'),
    ('Prüfen', 'Check'),
    ('Gr. ', 'Size '),
 ('Art.-Nr. ', 'Art. no. '),
    (' Tage', ' days'),
    ('Hinweis', 'Note'),
]

CSS = """
:root{--bg:#f4f4f2;--card:#fff;--fg:#151515;--mut:#6b7280;--line:#e5e5e2;--red:#b91c1c;--redbg:#fdecea;--grn:#15803d;--grnbg:#e8f6ec}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}
a{color:inherit}.top{background:#151515;color:#fff;border-bottom:4px solid #a51d1b}
.top .in{max-width:1100px;margin:0 auto;padding:10px 14px;display:flex;gap:10px;align-items:center;justify-content:space-between}
.top img{height:28px}.top h1{font:800 17px Arial;margin:0;flex:1}.top a{color:#fff;text-decoration:none;border:1px solid #444;border-radius:6px;padding:6px 10px;font-size:13px}
.wrap{max-width:1100px;margin:0 auto;padding:12px 14px 40px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin-bottom:12px}
h2{font:800 13px Arial;letter-spacing:1px;text-transform:uppercase;margin:0 0 10px;color:var(--mut)}
.mut{color:var(--mut)}.r{text-align:right}
input[type=search],input[type=text],select,textarea{width:100%;padding:12px;border:1px solid #d1d5db;border-radius:8px;font-size:16px;background:#fff}
.list a{display:flex;justify-content:space-between;gap:8px;padding:13px 12px;border:1px solid var(--line);border-radius:10px;margin-bottom:8px;text-decoration:none;background:#fff}
.list a:active{background:#f3f4f6}.list small{color:var(--mut)}
.ctx{display:flex;justify-content:space-between;gap:8px;align-items:center;font-size:13px;color:var(--mut);margin-bottom:10px}
.ctx b{color:var(--fg);font-size:15px}
.sz{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:12px}
.sz button{padding:14px 0;border:1px solid #c9c9c4;border-radius:10px;background:#fff;font:700 16px Arial;color:var(--fg)}
.sz button.on{background:#151515;color:#fff;border-color:#151515}
.sz button small{display:block;font:400 11px Arial;color:inherit;opacity:.7}
.big{display:block;width:100%;border:0;border-radius:14px;padding:22px 10px;font:800 22px Arial;margin-bottom:10px;cursor:pointer}
.ok{background:var(--grn);color:#fff}.bad{background:var(--red);color:#fff}.blk{background:#151515;color:#fff}
.big:disabled{opacity:.35}
.pmsg{display:flex;justify-content:space-between;align-items:center;gap:10px;border-radius:12px;padding:16px;margin-bottom:12px;font:800 17px Arial}.pmsg.nt{background:#fef3c7;color:#92400e}
.hnt{background:#fef3c7;color:#92400e;font-size:17px!important;padding:14px 10px!important}
.le{display:grid;grid-template-columns:44px 92px 1fr;gap:6px;align-items:center;padding:8px 0;border-bottom:1px solid #f0f0ee;font-size:14px}.le span:first-child{color:var(--mut);font-size:12px}
.le.leo b{color:var(--grn)}.le.led b{color:var(--red)}.le.len b{color:#92400e}.le.fresh{animation:fr 2.5s ease-out}@keyframes fr{0%{background:#dcfce7}100%{background:transparent}}.pmsg.ok{background:var(--grnbg);color:var(--grn)}.pmsg.warn{background:#fff7e6;color:#92400e;border:1px solid #f6d28b}.pmsg button{background:#92400e;color:#fff;border:0;border-radius:8px;padding:9px 12px;font-weight:700}
.qty{display:flex;gap:5px;align-items:center;margin:0 0 10px}.qty span{font-size:13px;color:var(--mut);margin-right:4px}.qty button{flex:1;min-width:0;padding:9px 2px;border:1px solid #c9c9c4;border-radius:8px;background:#fff;font:700 15px Arial}.qty button.on{background:var(--grn);color:#fff;border-color:var(--grn)}
.cnt{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;text-align:center}
.cnt div{background:#f7f7f5;border-radius:10px;padding:8px}.cnt b{display:block;font:800 22px Arial}.cnt small{color:var(--mut);font-size:12px}
.cnt .g b{color:var(--grn)}.cnt .d b{color:var(--red)}
.last{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:6px;font-size:13px;color:var(--mut);margin-top:10px;min-height:22px}.last span:last-child{display:flex;gap:6px}
.last button{background:none;border:1px solid #c9c9c4;border-radius:6px;padding:5px 10px;font-size:13px}
.flash{position:fixed;left:0;right:0;top:0;padding:14px;text-align:center;font:800 18px Arial;color:#fff;transform:translateY(-100%);transition:transform .15s}
.flash.show{transform:none}
.ph{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:12px}
.ph img,.ph label{width:100%;aspect-ratio:1;object-fit:cover;border-radius:10px;border:1px solid var(--line)}
.ph label{display:flex;flex-direction:column;align-items:center;justify-content:center;border:2px dashed #c9c9c4;color:var(--mut);font-size:13px;text-align:center}
.ph label b{font-size:28px;line-height:1}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}
.chips button{border:1px solid #c9c9c4;background:#fff;border-radius:999px;padding:10px 14px;font-size:14px}
.chips button.on{background:var(--redbg);border-color:var(--red);color:var(--red);font-weight:700}
.photo-head{text-align:center;background:#fff;border:2px solid #e5e5e2;border-radius:13px;padding:18px;margin-bottom:12px}.photo-head .qa{font:900 36px Arial}.photo-head .detail{font:800 20px Arial;color:var(--red);overflow-wrap:anywhere}.photo-ok{display:flex;gap:7px;align-items:center;background:#f0fdf4;border:1px solid #a7f3d0;border-radius:10px;padding:7px;margin:6px 0;font-weight:700;color:#166534}.photo-ok img{width:76px;height:76px;object-fit:cover;border-radius:7px}.photo-missing{color:var(--red);font-weight:800}.dk .nopic.photo-missing{color:var(--red);font-weight:800}.smallaction{display:inline-block;margin:5px 5px 5px 0;border:1px solid #d1d5db;border-radius:8px;background:#fff;padding:10px 13px;font:700 14px Arial;color:#151515;text-decoration:none}.smallaction:disabled{opacity:.4}.photo-hint{font-weight:700;text-align:center;background:#fef3c7;border-radius:11px;padding:14px;margin-bottom:12px;font-size:18px}
.err{color:var(--red);font-weight:700;margin:6px 0 10px;display:none}
.kp{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-bottom:12px}
.kp div{background:#fff;border:1px solid var(--line);border-radius:10px;padding:12px}.kp small{display:block;color:var(--mut);font:700 11px Arial;letter-spacing:1px;text-transform:uppercase}
.kp b{display:block;font:800 26px Arial}.kp .d b{color:var(--red)}.kp .g b{color:var(--grn)}
.pc{display:block;text-decoration:none;background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px;margin-bottom:10px}
.pc.hi{border-left:6px solid var(--red)}.pc.mid{border-left:6px solid #d97706}.pc.lo{border-left:6px solid var(--grn)}
.pc h3{margin:0 0 6px;font-size:16px}.bar{height:8px;border-radius:4px;background:var(--grnbg);overflow:hidden;margin:8px 0}.bar i{display:block;height:100%;background:var(--red)}
table{width:100%;border-collapse:collapse;font-size:14px}th{font:700 11px Arial;letter-spacing:1px;text-transform:uppercase;color:var(--mut);text-align:left;padding:7px 6px;border-bottom:1px solid var(--line)}
td{padding:8px 6px;border-bottom:1px solid #f0f0ee;vertical-align:top}td.neg{color:var(--red);font-weight:700}
.dl{display:grid;grid-template-columns:110px 1fr;gap:12px;padding:12px 0;border-bottom:1px solid #f0f0ee}
.scan{border:2px dashed #c9c9c4;border-radius:14px;padding:14px;text-align:center;margin-bottom:12px;background:#fafaf8}
.scan.hit{border-style:solid;border-color:#151515;background:#fff}
.scan .sp{font:700 13px Arial;color:var(--mut);text-transform:uppercase;letter-spacing:.08em}
.scan .bs{font:800 64px/1 Arial;margin:6px 0 2px;color:var(--fg);word-break:break-word}.scan .bc{font:800 20px Arial;color:var(--fg);margin-top:6px}
.szh{font:700 12px Arial;color:var(--mut);text-transform:uppercase;letter-spacing:.06em;margin:4px 0 6px}
.scan .bn{font:700 15px Arial}
.scan .bp{font-size:13px;color:var(--mut);margin-top:2px}
.swb{background:#fef3c7;color:#92400e;border-radius:10px;padding:10px 12px;font-weight:700;margin-bottom:10px}
.mrow{display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:13px;margin:-4px 0 10px}
.mrow label{display:flex;align-items:center;gap:6px}
.mrow input{width:auto}
#manual{display:none}#manual.open{display:block}
.prg{display:grid;grid-template-columns:minmax(44px,auto) 1fr 74px;gap:6px 10px;align-items:center;font-size:14px}
.prg b{font:800 15px Arial}.prg .br{height:10px;background:#eee;border-radius:5px;overflow:hidden}.prg .br i{display:block;height:10px;background:#151515}
.prg .n{text-align:right;font-variant-numeric:tabular-nums}.prg .ov{color:var(--red);font-weight:700}.prg .ov i{background:var(--red)}.prg .dn{color:var(--grn);font-weight:700}.prg .dn i{background:var(--grn)}
.bprog{font:700 15px Arial;margin-top:4px}.bprog.ov{color:var(--red)}
.needname{border:2px solid var(--red)!important}
#lwd{background:#fde8e8;color:var(--red);border:0;border-radius:8px;padding:6px 10px;font:700 13px Arial;margin-left:6px}
.mcode{display:flex;gap:6px;margin-top:8px}.mcode input{flex:1}
.dk{border:1px solid #e7e7e3;border-radius:12px;overflow:hidden;background:#fff;display:flex;flex-direction:column}
.dk .pics{display:flex;gap:4px;overflow-x:auto;background:#151515;scroll-snap-type:x mandatory}
.dk .pics img{height:240px;width:auto;max-width:100%;object-fit:cover;flex:0 0 auto;scroll-snap-align:start;cursor:zoom-in}
.dk .pics.one img{width:100%;object-fit:cover}
.dk .nopic{height:80px;display:flex;align-items:center;justify-content:center;color:#9a9a95;background:#f3f3f0;font-size:13px}
.dk .bd{padding:10px 12px 12px}
.dk .hd{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.dk .szp{font:800 18px Arial;background:#151515;color:#fff;border-radius:8px;padding:3px 10px}
.dk .rs{font:700 14px Arial;color:var(--red);background:#fde8e8;border-radius:8px;padding:4px 9px}
.dk .meta{font-size:12px;color:var(--mut);margin-top:6px}
.dk .tx{margin-top:6px;font-size:14px}
.dk .rs.nt{color:#92400e;background:#fef3c7}.dk.nt{border-color:#f6d28b}
.dk .imp{font-size:11px;background:#eef2ff;color:#3730a3;border-radius:6px;padding:1px 6px}
.dk .ac{margin-top:8px;font-size:13px}
.dkg{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.flt{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px}
.flt button{border:1px solid #c9c9c4;background:#fff;border-radius:999px;padding:6px 12px;font:600 13px Arial;cursor:pointer}
.flt button.on{background:#151515;color:#fff;border-color:#151515}
.flt .lb{font:700 12px Arial;color:var(--mut);align-self:center;margin-right:4px}
.lbx{position:fixed;inset:0;background:rgba(0,0,0,.92);display:none;align-items:center;justify-content:center;z-index:99}
.lbx.show{display:flex}.lbx img{max-width:96vw;max-height:84vh;object-fit:contain}
.lbx button{position:absolute;background:rgba(255,255,255,.15);color:#fff;border:0;font:700 26px Arial;width:52px;height:52px;border-radius:50%;cursor:pointer}
.lbx .x{top:14px;right:14px}.lbx .pv{left:10px;top:50%}.lbx .nx{right:10px;top:50%}
.lbx .cap{position:absolute;bottom:14px;left:0;right:0;text-align:center;color:#fff;font:600 14px Arial}
@media(max-width:700px){
.top .in{padding:8px 10px;gap:6px}.top img{height:22px}.top h1{font-size:15px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}.top a{padding:5px 7px;font-size:12px;white-space:nowrap}
.wrap{padding-left:10px;padding-right:10px}.card{padding:12px}
.dg{display:flex;flex-direction:column}.dmain{order:1}.dside{order:2}
.dtop .big{font-size:19px;padding:13px!important}.dtop .fl{overflow-x:auto;flex-wrap:nowrap}
.nd .dl:nth-of-type(n+6){display:none}
table.rtab,table.rtab tbody{display:block}table.rtab tr:first-child{display:none}
table.rtab tr{display:grid;grid-template-columns:repeat(3,1fr) auto;gap:2px 8px;padding:10px 0;border-bottom:1px solid #eee}
table.rtab td{border:0;padding:0;text-align:left}table.rtab td.rn{grid-column:1/-1}table.rtab td.rc::before{content:attr(data-l);display:block;font:700 10px Arial;color:var(--mut);text-transform:uppercase;letter-spacing:.06em}
table.rtab td.rc{font:700 16px Arial}table.rtab td.rl{align-self:end;text-align:right;white-space:nowrap}table.rtab td.rl a{margin-left:8px}.dsk{display:none}
.flt{flex-wrap:nowrap;overflow-x:auto;padding-bottom:4px;-webkit-overflow-scrolling:touch}.flt button{white-space:nowrap;flex:0 0 auto}
.dkg{grid-template-columns:1fr;gap:8px}.dk{flex-direction:row;min-height:104px}
.dk .pics{flex:0 0 104px;width:104px;display:block;position:relative;overflow:hidden}.dk .pics img{display:none;width:104px;height:104px;object-fit:cover}.dk .pics img:first-child{display:block;height:100%;min-height:104px}
.dk .pics[data-n]::after{content:attr(data-n);position:absolute;right:4px;bottom:4px;background:rgba(0,0,0,.75);color:#fff;font:700 11px Arial;padding:1px 6px;border-radius:5px}
.dk .nopic{flex:0 0 104px;height:auto;font-size:11px}.dk .bd{padding:8px 10px;min-width:0}.dk .hd{gap:5px}.dk .szp{font-size:14px;padding:2px 8px}.dk .rs{font-size:12px;padding:2px 7px}
.dk .tx{font-size:13px;margin-top:4px;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}.dk .meta{font-size:11px;margin-top:4px}.dk .ac{font-size:12px;margin-top:4px}
.kp b{font-size:24px}.two{gap:10px}
.mrow{flex-direction:column;align-items:flex-start;gap:6px}.swb{flex-wrap:wrap}.swb .btn{width:100%;text-align:center}.sz button{padding:12px 0}.scan .bs{font-size:56px}.qty button{padding:10px 0}
}
@media print{.dk .pics img{height:170px}.flt,.lbx{display:none!important}.dk{break-inside:avoid}}
.dl img{width:110px;height:110px;object-fit:cover;border-radius:8px;display:block}.dl .ths{display:flex;gap:6px;flex-wrap:wrap;margin-top:6px}.dl .ths img{width:56px;height:56px}
.tag{display:inline-block;background:var(--redbg);color:var(--red);border-radius:999px;padding:2px 9px;font:700 12px Arial}
.btn{display:inline-block;background:#151515;color:#fff;text-decoration:none;border-radius:8px;padding:10px 14px;font:700 14px Arial;border:0}
.fl{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px}.fl a{padding:7px 12px;border-radius:999px;background:#e9e9e6;text-decoration:none;font-size:13px}.fl a.on{background:#151515;color:#fff}
@media(max-width:700px){.kp{grid-template-columns:repeat(2,minmax(0,1fr))}}
.wrap.wide{max-width:1500px}.top .in{max-width:1500px}
.dtop{display:grid;grid-template-columns:260px auto 1fr;gap:12px;align-items:center;margin-bottom:12px}
.dg{display:grid;grid-template-columns:minmax(0,1fr) 480px;gap:16px;align-items:start}.dside{grid-column:2;grid-row:1}.dmain{grid-column:1;grid-row:1}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:10px}.pgrid .pc{margin:0}
.two{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;align-items:start}.two .card{margin-bottom:12px}
.dlg{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));column-gap:20px}
@media(max-width:1000px){.dtop{grid-template-columns:1fr}.dg{grid-template-columns:1fr}.dside,.dmain{grid-column:auto;grid-row:auto}.two{grid-template-columns:1fr}.dlg{grid-template-columns:1fr}}
@media print{.dg,.two,.dlg{display:block}}
@media print{.top,.noprint{display:none!important}body{background:#fff}.card{border:0;padding:0}}

/* v19.4: inspector/date controls; mobile and print-safe */
.qcfilter{padding:12px 14px}
.qcfilter-row{display:flex;flex-wrap:wrap;gap:10px;align-items:end}
.qcfilter-item{display:block;flex:1 1 190px;min-width:0}
.qcfilter-item b{display:block;font:700 12px Arial;color:var(--mut);margin-bottom:5px}
.qcfilter select{display:block;width:100%;min-height:44px;padding:9px 10px;font:600 15px Arial;border:1px solid #d1d5db;background:#fff;border-radius:9px}
.qcfilter .reset{padding:11px 13px;border-radius:9px;border:1px solid #d1d5db;text-decoration:none;font:700 14px Arial;white-space:nowrap}
.qcfilter-note{margin:8px 0 0;font-size:12px;color:var(--mut)}
.today-head{display:flex;gap:9px;align-items:center;justify-content:space-between;flex-wrap:wrap;margin-bottom:6px}
.today-head h2{margin:0}
.today-pill{background:var(--grnbg);color:var(--grn);font:800 16px Arial;border-radius:9px;padding:6px 12px}
.today-table-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.today-table{min-width:0;table-layout:fixed;font-size:13px}
.today-table th{font-size:10px;letter-spacing:0;padding:7px 3px;white-space:nowrap}
.today-table td{padding:8px 3px}
.today-table th:first-child{width:46%}
.today-table th:not(:first-child){width:18%}
.today-table td:first-child{overflow-wrap:anywhere}
.today-table td:first-child,.today-table th:first-child{text-align:left}
.today-table td:not(:first-child),.today-table th:not(:first-child){text-align:right;font-variant-numeric:tabular-nums}
.today-table .warnrow td:first-child{color:#92400e}
@media(max-width:520px){.qcfilter{padding:12px}.qcfilter-row{display:grid;grid-template-columns:minmax(0,1fr);gap:10px}.qcfilter-item{min-width:0}.qcfilter .reset{text-align:center}.today-pill{font-size:14px}}
@media print{.qcfilter{display:none!important}.today-table-wrap{overflow:visible}.today-table{min-width:0}}

/* v19.2: locally embedded, monochrome vector icons (no emoji or external icon font) */
#take::before,#done::before,#ok::before,#bad::before,#hnt::before,
#save::before,#printer::before,#retry::before,#cancel::before,#pmr::before,
.photo-ok span::before,.photo-missing::before,.pmsg.ok::before,.pmsg.warn::before,.pmsg.nt::before,
.le.leo b::before,.le.len b::before,.le.led b::before,.big.start-check::before,
.nav-back::before,.nav-dash::before,.photo-hint::before,#print-status:not(:empty)::before,
[data-rp]::before,a[href*="photo_for"]::before{
  content:"";display:inline-block;width:1.08em;height:1.08em;flex:0 0 auto;
  vertical-align:-.16em;margin-right:.42em;background-color:currentColor;
  -webkit-mask-image:var(--qc-svg);mask-image:var(--qc-svg);
  -webkit-mask-size:contain;mask-size:contain;
  -webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;
  -webkit-mask-position:center;mask-position:center
}

#take{--qc-svg:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2224%22%20height%3D%2224%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Cpath%20d%3D%22M14.5%204h-5L7%207H4a2%202%200%200%200-2%202v9a2%202%200%200%200%202%202h16a2%202%200%200%200%202-2V9a2%202%200%200%200-2-2h-3z%22%2F%3E%3Ccircle%20cx%3D%2212%22%20cy%3D%2213.5%22%20r%3D%223.5%22%2F%3E%3C%2Fsvg%3E")}
#done,.photo-ok span,.pmsg.ok,.le.leo b,.big.start-check{--qc-svg:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2224%22%20height%3D%2224%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Ccircle%20cx%3D%2212%22%20cy%3D%2212%22%20r%3D%2210%22%2F%3E%3Cpath%20d%3D%22m8%2012%202.5%202.5L16%209%22%2F%3E%3C%2Fsvg%3E")}
#bad,.le.led b{--qc-svg:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2224%22%20height%3D%2224%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Ccircle%20cx%3D%2212%22%20cy%3D%2212%22%20r%3D%2210%22%2F%3E%3Cpath%20d%3D%22m15%209-6%206m0-6%206%206%22%2F%3E%3C%2Fsvg%3E")}
#download_pdf,#save.icon-download{--qc-svg:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2224%22%20height%3D%2224%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Cpath%20d%3D%22M12%203v12m-5-5%205%205%205-5%22%2F%3E%3Cpath%20d%3D%22M5%2017v3h14v-3%22%2F%3E%3C%2Fsvg%3E")}
#download_pdf{display:inline-flex;align-items:center;justify-content:center;gap:8px;text-align:center;min-height:45px;max-width:100%;white-space:normal}
#download_pdf.big{display:flex;width:100%;font-size:20px;margin:8px 0 2px;min-height:64px}
#download_pdf::before,#save.icon-download::before{content:'';display:inline-block;width:20px;height:20px;flex:0 0 20px;background:currentColor;mask:var(--qc-svg) center/contain no-repeat;-webkit-mask:var(--qc-svg) center/contain no-repeat}
#printer,#save.icon-printer,[data-rp]{--qc-svg:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2224%22%20height%3D%2224%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Cpath%20d%3D%22M6%209V2h12v7M6%2018H4a2%202%200%200%201-2-2v-5a2%202%200%200%201%202-2h16a2%202%200%200%201%202%202v5a2%202%200%200%201-2%202h-2%22%2F%3E%3Cpath%20d%3D%22M6%2014h12v8H6zM18%2012h.01%22%2F%3E%3C%2Fsvg%3E")}
#hnt,.le.len b,.photo-missing,.pmsg.warn{--qc-svg:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2224%22%20height%3D%2224%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Cpath%20d%3D%22m10.3%203.1-8.2%2014.3a2%202%200%200%200%201.7%203h16.4a2%202%200%200%200%201.7-3L13.7%203.1a2%202%200%200%200-3.4%200z%22%2F%3E%3Cpath%20d%3D%22M12%209v4m0%204h.01%22%2F%3E%3C%2Fsvg%3E")}
a[href*="photo_for"]{--qc-svg:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2224%22%20height%3D%2224%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Ccircle%20cx%3D%2212%22%20cy%3D%2212%22%20r%3D%2210%22%2F%3E%3Cpath%20d%3D%22M12%208v8m-4-4h8%22%2F%3E%3C%2Fsvg%3E")}
#retry,#pmr{--qc-svg:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2224%22%20height%3D%2224%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Cpath%20d%3D%22M3%2011a9%209%200%201%201%202.8%206.5M3%204v7h7%22%2F%3E%3C%2Fsvg%3E")}
#ok{--qc-svg:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2224%22%20height%3D%2224%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Cpath%20d%3D%22m20%206-11%2011-5-5%22%2F%3E%3C%2Fsvg%3E")}
.nav-back{--qc-svg:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2224%22%20height%3D%2224%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Cpath%20d%3D%22m12%2019-7-7%207-7M5%2012h14%22%2F%3E%3C%2Fsvg%3E")}
.nav-dash{--qc-svg:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2224%22%20height%3D%2224%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Crect%20x%3D%223%22%20y%3D%223%22%20width%3D%227%22%20height%3D%229%22%20rx%3D%221%22%2F%3E%3Crect%20x%3D%2214%22%20y%3D%223%22%20width%3D%227%22%20height%3D%225%22%20rx%3D%221%22%2F%3E%3Crect%20x%3D%2214%22%20y%3D%2212%22%20width%3D%227%22%20height%3D%229%22%20rx%3D%221%22%2F%3E%3Crect%20x%3D%223%22%20y%3D%2216%22%20width%3D%227%22%20height%3D%225%22%20rx%3D%221%22%2F%3E%3C%2Fsvg%3E")}
.photo-hint{--qc-svg:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2224%22%20height%3D%2224%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Crect%20x%3D%224%22%20y%3D%225%22%20width%3D%2216%22%20height%3D%2217%22%20rx%3D%222%22%2F%3E%3Cpath%20d%3D%22M9%203h6v4H9zM8%2014l3%203%205-5%22%2F%3E%3C%2Fsvg%3E")}
#save.icon-note,.pmsg.nt{--qc-svg:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2224%22%20height%3D%2224%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Cpath%20d%3D%22M14%202H6a2%202%200%200%200-2%202v16a2%202%200%200%200%202%202h12a2%202%200%200%200%202-2V8z%22%2F%3E%3Cpath%20d%3D%22M14%202v6h6M9%2016l4-4%202%202-4%204-3%201z%22%2F%3E%3C%2Fsvg%3E")}
#print-status{--qc-svg:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2224%22%20height%3D%2224%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Ccircle%20cx%3D%2212%22%20cy%3D%2212%22%20r%3D%2210%22%2F%3E%3Cpath%20d%3D%22M12%2011v6m0-10h.01%22%2F%3E%3C%2Fsvg%3E")}
#cancel{--qc-svg:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2224%22%20height%3D%2224%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Cpath%20d%3D%22M3%206h18m-2%200-1%2014a2%202%200%200%201-2%202H8a2%202%200%200%201-2-2L5%206m3%200V4a2%202%200%200%201%202-2h4a2%202%200%200%201%202%202v2M10%2011v6m4-6v6%22%2F%3E%3C%2Fsvg%3E")}

/* Consistent, minimum-size mobile touch targets, with normal browser zoom enabled */
.top .nav-back,.top .nav-dash{display:inline-flex;align-items:center;justify-content:center}
button,.btn,.smallaction,.fl a,.top a,.chips button,.sz button,.flt button{touch-action:manipulation}
button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible{outline:3px solid #2563eb;outline-offset:2px}
.photo-head .qa{font-size:clamp(30px,9vw,38px);line-height:1.1}
.photo-head .detail{font-size:clamp(16px,5vw,20px);line-height:1.35}
.photo-head .mut{overflow-wrap:anywhere}
.photo-ok{min-width:0;overflow-wrap:anywhere}.photo-ok span{min-width:0}
.photo-hint{line-height:1.35}.photo-hint::before{vertical-align:-.17em}
#take{min-height:74px;display:flex;justify-content:center;align-items:center;gap:0}
#take::before{width:1.28em;height:1.28em}
#done{min-height:62px}
.smallaction{min-height:44px;line-height:1.25}
#cancel{display:flex;align-items:center;justify-content:center;min-height:48px;gap:0}
.big.start-check{display:flex;align-items:center;justify-content:center}
#photo-status,#print-status,.ctx,.photo-head{overflow-wrap:anywhere}
#save:disabled,#printer:disabled,#retry:disabled,#done:disabled,#take:disabled{cursor:wait}
@media(max-width:560px){
 html{-webkit-text-size-adjust:100%;text-size-adjust:100%}
 body{font-size:15px}
 .wrap{padding:10px 10px calc(24px + env(safe-area-inset-bottom, 0px));width:100%;max-width:100%;overflow-x:clip}
 .top .in{display:flex;flex-wrap:wrap;gap:7px;padding:9px 10px}
 .top img{height:24px;flex:0 0 auto}
 .top h1{font-size:15px;flex:1 1 calc(100% - 74px);min-width:0}
 .top a{display:inline-flex;align-items:center;justify-content:center;flex:1 1 75px;min-height:39px;margin:0;font-size:13px}
 .top a.nav-back{flex:1.2 1 96px}.top a.nav-dash{flex:1.6 1 100px}
 .card{padding:12px;margin-bottom:10px;min-width:0}
 .photo-hint{font-size:16px;padding:12px;overflow-wrap:anywhere}
 .photo-head{padding:13px 10px;margin-bottom:10px}
 .photo-head .qa{margin:2px 0 4px}
 .photo-head .detail{font-size:17px}
 .photo-head .mut{line-height:1.35}
 .photo-ok img{width:64px;height:64px}.photo-ok{padding:7px}
 #take{font-size:20px;min-height:70px;border-radius:12px}
 #done{font-size:18px;padding:16px 10px;min-height:60px}
 #cancel{font-size:14px;padding:12px 9px}
 .big{font-size:19px;padding:16px 10px;border-radius:12px;line-height:1.25}
 .smallaction{font-size:14px;padding:11px 12px}
 .ctx{flex-wrap:wrap;align-items:flex-start}.ctx > span{min-width:0}
 .ctx > span:first-child{flex:1 1 55%;min-width:0}
 .ctx > span:last-child{flex:0 1 auto}
 .scan{padding:12px 9px}.scan .bs{font-size:clamp(40px,13vw,56px)}
 .scan .bc{font-size:17px;overflow-wrap:anywhere}
 .chips{gap:7px}.chips button{font-size:14px;padding:11px 12px;min-height:44px}
 .sz{grid-template-columns:repeat(4,minmax(0,1fr));gap:6px}
 .sz button{min-height:54px;padding:10px 2px;font-size:15px;overflow-wrap:anywhere}
 .qty{gap:4px}.qty span{font-size:12px}.qty button{min-height:43px;font-size:14px}
 .mcode input{min-width:0}.mcode .btn{min-width:48px;min-height:45px}
 .cnt{gap:5px}.cnt div{padding:7px 4px}.cnt b{font-size:20px}.cnt small{font-size:11px}
 .le{grid-template-columns:40px minmax(82px,auto) minmax(0,1fr);gap:5px;font-size:12px}
 .le b{font-size:12px;overflow-wrap:anywhere}.le span:last-child{overflow-wrap:anywhere;min-width:0}
 .last{gap:7px}.last button{min-height:38px;padding:8px}
 .pmsg{padding:12px;font-size:15px;flex-wrap:wrap;overflow-wrap:anywhere}
 .pmsg button{min-height:40px}
 .pgrid,.dkg{grid-template-columns:minmax(0,1fr)}
 .dk .bd{overflow-wrap:anywhere}
 .dl{grid-template-columns:88px minmax(0,1fr);gap:9px}
 .dl img{width:88px;height:88px}
 .fl a,.flt button{min-height:41px;display:inline-flex;align-items:center}
 .kp{gap:7px}.kp div{padding:9px}.kp b{font-size:22px}
 .prg{grid-template-columns:minmax(40px,auto) minmax(0,1fr) 64px}
 .swb{overflow-wrap:anywhere}.swb .btn{min-height:42px}
 table{font-size:13px}td,th{padding:7px 5px}
}
@media(max-width:350px){
 .top h1{font-size:14px}
 .sz{grid-template-columns:repeat(3,minmax(0,1fr))}
 .photo-head .detail{font-size:16px}
 .big{font-size:18px}
 .qty span{display:none}
 .le{grid-template-columns:36px 84px minmax(0,1fr)}
}
@media(prefers-reduced-motion:reduce){.le.fresh{animation:none}.flash{transition:none}}
/* v19.8: compact reasons, visibly selected reasons, and sticky label action. */
.reason-card .chips{gap:7px;margin-bottom:6px}
.reason-card .chips button{min-height:40px;padding:8px 12px;line-height:1.25}
.reason-card .chips button.on{box-shadow:inset 0 0 0 1px var(--red)}
.reason-more{border:1px solid #d1d5db;border-radius:9px;margin:8px 0 12px;background:#fafaf9}
.reason-more summary,.note-optional summary{cursor:pointer;font-weight:800;padding:12px 13px;list-style-position:inside}
.reason-more summary:focus-visible,.note-optional summary:focus-visible{outline:3px solid #2563eb}
.reason-more-body{padding:0 10px 12px}
.reason-more-body input{margin:1px 0 10px}
.reason-more .chips{max-height:250px;overflow-y:auto;margin-bottom:0}
.reason-selection{font-size:12px;line-height:1.4;color:var(--red);font-weight:700;padding:6px 1px 10px;overflow-wrap:anywhere}
.reason-selection[hidden]{display:none}
.note-optional{padding:3px 10px 10px}
.note-optional textarea{margin-top:5px}
.savebar{position:sticky;bottom:0;z-index:9;background:rgba(244,244,242,.98);border-top:1px solid #ddd;padding:9px 0 10px;box-shadow:0 -5px 18px rgba(0,0,0,.05)}
.savebar .big{margin:0;min-height:64px}
#photo-required{font-size:13px;color:var(--red);font-weight:800;padding:7px 0 2px}
#done:disabled{opacity:.45;filter:grayscale(.5);cursor:not-allowed}
@media(max-width:560px){
 .reason-card{padding:10px!important}
 .reason-card .chips-primary{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px}
 .reason-card .chips-primary button{min-height:44px;white-space:normal;overflow-wrap:anywhere;padding:8px 6px;font-size:12px}
 .reason-more summary{padding:11px;font-size:14px}
 .reason-card #newtag{padding:10px;font-size:14px}
 .savebar{bottom:0;padding-bottom:calc(9px + env(safe-area-inset-bottom, 0px));margin:0 -10px;padding-left:10px;padding-right:10px}
 .savebar .big{font-size:19px;min-height:62px}
 .note-optional summary{padding:9px 8px}
 .qcfilter{padding:9px 10px}
 .qcfilter .qcfilter-row{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:6px}
 .qcfilter .qcfilter-item{min-width:0}
 .qcfilter .qcfilter-item b{font-size:10px;margin-bottom:2px}
 .qcfilter select{min-height:38px;padding:7px 5px;font-size:13px}
 .qcfilter .reset{grid-column:1/-1;justify-self:end;min-height:30px;padding:6px 10px;font-size:12px}
 .qcfilter > .qcfilter-note{display:none}
}
@media print{.photo-hint,#take,#done,#cancel,#printer,#retry{display:none!important}}


/* v19.9: defect location drawings */
.lsvg{display:block;width:100%;height:auto;touch-action:manipulation}
.lsvg .lo{fill:#f6f6f3;stroke:#151515;stroke-width:2.2;stroke-linejoin:round}
.lsvg.vI .lo{fill:#eef2f6;stroke-dasharray:6 3}
.lsvg .lz{fill:rgba(255,255,255,.01);stroke:#b9b9b3;stroke-width:1;stroke-dasharray:3 2}
.lsvg.int .lz{cursor:pointer}
.lsvg.int .lz:hover{fill:rgba(220,38,38,.12)}
.lsvg .lz.on{fill:rgba(220,38,38,.6)!important;stroke:#b91c1c;stroke-width:2.2;stroke-dasharray:none}
.lsvg .lz.hz{stroke:#b91c1c;stroke-dasharray:none}
.lsvg .lc{font:800 15px Arial;fill:#fff;text-anchor:middle;dominant-baseline:central;paint-order:stroke;stroke:#7f1d1d;stroke-width:3px}
.lsvg .lsd{font:800 15px Arial;fill:#8a8a85;text-anchor:middle}
.lpick{display:grid;grid-template-columns:minmax(0,1fr);gap:8px}
.lseg{display:flex;gap:6px;flex-wrap:wrap;margin:4px 0 8px}
.lseg button{flex:1 1 0;min-height:42px;border:2px solid #d6d6d1;background:#fff;border-radius:10px;font:800 15px Arial;color:#151515;padding:6px 8px;position:relative}
.lseg button.on{border-color:#151515;background:#151515;color:#fff}
.lseg button[data-n]:not([data-n="0"])::after{content:attr(data-n);position:absolute;top:-8px;right:-6px;background:var(--red);color:#fff;border-radius:999px;font:800 12px Arial;padding:2px 7px}
.ldraw{max-width:290px;margin:0 auto;width:100%}
.ldraw[hidden]{display:none!important}
.lzall{display:block;width:100%;min-height:40px;border:2px dashed #c9c9c4;background:#fff;border-radius:10px;font:700 14px Arial;margin-top:6px}
.lzall.on{border-style:solid;border-color:var(--red);background:#fde8e8;color:#991b1b}
#zsel{font:700 14px Arial;margin:8px 0 2px;color:#151515}
#zsel.none{color:#8a8a85;font-weight:600}
.lhint{font-size:12px;color:var(--mut);margin:2px 0 0;text-align:center}
#addf{width:100%;margin-top:10px;min-height:48px;font:800 16px Arial}
.fi{display:flex;gap:10px;align-items:flex-start;border:2px solid #f1c4c4;background:#fff7f7;border-radius:12px;padding:9px 10px;margin-bottom:8px}
.fi b{display:block;font:800 16px Arial}
.fi span{display:block;font-size:13px;color:#444;margin-top:2px}
.fi .fx{margin-left:auto;border:0;background:#fff;border:1px solid #ddd;border-radius:8px;min-width:40px;min-height:40px;font:800 18px Arial;color:var(--red)}
.fi.nt{border-color:#f3d69b;background:#fffaf0}
#flist-empty{font-size:13px;color:var(--mut)}
.ldr-row{display:flex;gap:6px;flex-wrap:wrap;justify-content:center}
.ldr-row .lfig{margin:0;flex:0 1 110px;text-align:center}
.ldr-row figcaption{font:700 11px Arial;color:var(--mut);margin-top:2px}
.ldr-row.heat .lfig{flex:1 1 140px;max-width:220px}
.ldr-row.heat figcaption{font:800 14px Arial;color:#151515}
.fblk{border:2px solid #eee;border-radius:12px;padding:10px;margin-bottom:10px;background:#fff}
.fbh b{display:block;font:800 17px Arial}
.fbh span{display:block;font-size:13px;color:#444;margin:2px 0 6px}
.fblk .ldr-row .lfig{flex-basis:96px}
.fblk .fph:empty{display:none}
.fblk .fph{margin:6px 0}
.fblk button[data-f]{width:100%;margin-top:6px}
.dk .locpic{flex-direction:column;background:#fafaf8;color:#151515;padding:6px 4px;height:auto}
.dk .locpic .ldr-row{flex-wrap:nowrap;gap:2px}
.dk .locpic .lfig{flex:1 1 0;min-width:0;max-width:96px}
.dk .wo{font-size:13px;margin-top:4px;color:#222}
.dk .wo b{color:var(--red)}
.heatt td{font-size:13px}
@media print{.ldr-row.heat .lfig{max-width:220px}.dk .locpic .lfig{max-width:80px}}

/* v19.10: product drawings + guided defect steps */
.lsvg .lo2{fill:#e9e9e5;stroke:#151515;stroke-width:2}
.lsvg .ld{fill:none;stroke:#555;stroke-width:1.4}
.lsvg .ldk{fill:#d4d4cf;stroke:none}
.lsvg .llt{fill:#ffffff;stroke:#888;stroke-width:1}
.lsvg .lq{stroke:#c3c3bd;stroke-width:1;fill:none}
.lsvg .lzp{stroke:#151515;stroke-width:2;stroke-dasharray:2 1.5}
.lsvg .lzo{stroke:#151515;stroke-width:2.4;stroke-dasharray:4 2}
.lsvg .lbl{fill:#9a9a95;stroke:#555}
.lsvg .lbk{fill:#e0e0dc;stroke:#151515;stroke-width:1.5}
.lsvg .lmd{fill:#151515}
.lsvg .lmg{fill:none;stroke:#b91c1c;stroke-width:1.6}
.lsvg .lpt{fill:#fff;stroke:#151515;stroke-width:1.4}
.lsvg .llg{font:900 11px Arial;fill:#151515;text-anchor:middle}
.lsvg .lz{stroke:rgba(120,120,115,.25)}
.lsvg.int .lz{stroke:rgba(80,110,170,.35)}
.qsteps{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;list-style:none;padding:0;margin:0 0 10px}
.qsteps li{background:#fff;border:2px solid #e2e2de;border-radius:12px;padding:8px 6px;text-align:center;font:800 15px Arial;color:#9a9a95}
.qsteps li b{display:inline-block;width:22px;height:22px;line-height:22px;border-radius:50%;background:#e2e2de;color:#fff;margin-right:4px;font-size:13px}
.qsteps li.cur{border-color:var(--red);color:#151515;background:#fff5f5}.qsteps li.cur b{background:var(--red)}
.qsteps li.done{border-color:#16a34a;color:#166534;background:#f0fdf4}.qsteps li.done b{background:#16a34a}
.qsteps li small{font-weight:600;font-size:11px}
.qsec{margin-top:14px}.qsec:first-of-type{margin-top:4px}
.qlbl{display:block;font:800 17px Arial;margin-bottom:6px;color:#151515}
.qlbl b{display:inline-block;width:24px;height:24px;line-height:24px;text-align:center;border-radius:50%;background:#151515;color:#fff;font-size:14px;margin-right:6px}
.qlbl small{font-weight:600;color:var(--mut)}
.qsel{width:100%;min-height:54px;font:700 18px Arial;border:2px solid #151515;border-radius:12px;padding:8px 12px;background:#fff;color:#151515}
.qnew{width:100%;margin-top:8px;min-height:48px;font-size:17px}
.qwrap{position:relative}
.qlock{opacity:.3;filter:grayscale(1);pointer-events:none}
.qcover{position:absolute;left:0;right:0;top:34px;bottom:0;background:transparent;border:2px dashed #c9c9c4;border-radius:12px;font:800 16px Arial;color:#151515;cursor:pointer;display:flex;align-items:center;justify-content:center;padding:10px}
.qcover[hidden]{display:none}
.qflash{animation:qflash 1s ease 2}
@keyframes qflash{0%,100%{box-shadow:0 0 0 0 rgba(220,38,38,0)}50%{box-shadow:0 0 0 6px rgba(220,38,38,.45)}}
#zsel{min-height:20px}#zsel.zok{color:#166534}
.qths{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0}
.qth{position:relative;display:inline-block}
.qth img{width:72px;height:72px;object-fit:cover;border-radius:8px;border:1px solid #ddd;display:block}
.qth button{position:absolute;top:-6px;right:-6px;width:26px;height:26px;border-radius:50%;border:0;background:var(--red);color:#fff;font:800 13px Arial}
.fi .qths .qth img{width:52px;height:52px}
#fstate{font:800 15px Arial;min-height:20px}#fstate.fok{color:#166534}
.qnof{display:block;text-align:center;font-size:13px;color:var(--mut);margin-top:8px}
#addf{border:2px solid #151515}
#addf:disabled{opacity:.4;border-color:#ccc}
#savehint{margin:0 0 6px;text-align:center;font:700 14px Arial;color:#444}
#save:disabled{opacity:.35}
.dk .pics .pdraw{flex:0 0 auto;height:240px;background:#fafaf8;display:flex;align-items:center;padding:4px 6px;scroll-snap-align:start}
.dk .pics .pdraw .ldr-row{flex-wrap:nowrap;height:100%;align-items:center}
.dk .pics .pdraw .lfig{width:96px;flex:0 0 96px}
.dk .pics.hasd img{width:auto!important;max-width:62%}
.ndraw{width:64px;height:64px;border-radius:8px;background:#fafaf8;overflow:hidden;display:flex;justify-content:center}
.ndraw .lsvg{height:64px;width:auto}
@media(max-width:700px){
 .dk .pics{display:flex;flex-direction:column;background:#fafaf8}
 .dk .pics img:first-child{height:104px;min-height:104px;flex:0 0 104px}
 .dk .pics[data-n]::after{bottom:auto;top:80px}
 .dk .pics .pdraw{display:block;height:auto;padding:2px;width:104px}
 .dk .pics.hasd img{max-width:none;width:104px!important}
 .dk .pics .pdraw .ldr-row{flex-wrap:nowrap;gap:1px}
 .dk .pics .pdraw .lfig{flex:1 1 0;width:auto;min-width:0}
 .dk .pics .pdraw figcaption{font-size:9px}
}
@media print{.dk .pics .pdraw{height:170px}}

/* v19.11 */
.lsvg .lnc{fill:#151515}.lsvg .lnt{font:800 15px Arial;fill:#fff;text-anchor:middle;dominant-baseline:central}
#rchips{margin-bottom:8px}
#rchips button{min-height:52px;font-size:16px;font-weight:800}
#rchips button.on{background:var(--red);color:#fff;border-color:var(--red)}
.qsel2{min-height:48px;font-size:16px;border-width:1px;font-weight:600;color:#444}
.qlbl small{font-size:13px}
.qsrow{display:flex;gap:8px;align-items:stretch}
.qsrow .qback{flex:0 0 auto;display:flex;align-items:center;justify-content:center;padding:0 14px;border:2px solid #151515;border-radius:12px;background:#fff;color:#151515;font:800 16px Arial;text-decoration:none;min-height:64px}
.qsrow .big{flex:1 1 auto;margin:0}
.qov{position:fixed;inset:0;z-index:80;background:rgba(255,255,255,.9);display:flex;align-items:center;justify-content:center}
.qov[hidden]{display:none}
.qovb{display:flex;flex-direction:column;align-items:center;gap:10px;text-align:center;padding:24px}
.qovb b{font:900 28px Arial;color:#151515}.qovb span{font:800 22px Arial}.qovb small{display:none;font:700 16px Arial}
.qsp{width:54px;height:54px;border:6px solid #d4d4cf;border-top-color:#151515;border-radius:50%;animation:qspin .8s linear infinite}
@keyframes qspin{to{transform:rotate(360deg)}}
.qov.okd{background:rgba(21,128,61,.96)}.qov.okd .qsp{display:none}.qov.okd b,.qov.okd span,.qov.okd small{color:#fff}.qov.okd small{display:block}

/* v19.12: bigger drawing */
.ldraw{max-width:420px}
@media(min-width:900px){.ldraw{max-width:460px}}

/* v19.14: own drawings, editor, start button */
.cdr{position:relative;display:block;width:100%;line-height:0}
.cdr img{display:block;width:100%;height:auto}
.ldraw .cdr{max-width:340px;margin:0 auto}
.cdr svg.lsvg{position:absolute;left:0;top:0;width:100%;height:100%}
.lsvg.cdz .lz{fill:rgba(255,255,255,.04);stroke:rgba(255,255,255,.6);stroke-width:1.4;vector-effect:non-scaling-stroke;stroke-dasharray:4 3}
.lsvg.cdz .lz.on{fill:rgba(220,38,38,.72)!important;stroke:#fff;stroke-width:3;stroke-dasharray:none}
.lsvg.cdz .lz.hz{stroke:#fff;stroke-dasharray:none}
.lsvg.cdz .lc{stroke-width:4px}
.cdside{position:absolute;top:5px;font:800 15px Arial;color:#6b6b66;line-height:1;pointer-events:none}.cdside.l{left:7px}.cdside.r{right:7px}
.ndraw .cdr{width:64px;height:64px;overflow:hidden}.ndraw .cdr img{width:64px;height:auto}
.top .nav-logo{border:0;padding:0;display:flex;align-items:center}
.dstage{position:relative;max-width:560px;margin:10px auto;touch-action:none;user-select:none;-webkit-user-select:none;background:#f3f3f0;border-radius:10px;line-height:0}
.dstage img{display:block;width:100%;height:auto;border-radius:10px}
#dboxes{position:absolute;inset:0}
#dempty{min-height:220px;display:flex;align-items:center;justify-content:center;color:var(--mut);font:600 15px Arial;line-height:1.4}
.dbox{position:absolute;border:2px solid #ef4444;background:rgba(239,68,68,.2);box-sizing:border-box;pointer-events:none}
.dbox span{position:absolute;left:2px;top:2px;background:#ef4444;color:#fff;font:700 11px Arial;line-height:1.3;padding:1px 4px;border-radius:3px;white-space:nowrap;max-width:calc(100% - 4px);overflow:hidden;text-overflow:ellipsis}
.dbox.sel{border-color:#2563eb;background:rgba(37,99,235,.25)}.dbox.sel span{background:#2563eb}.dbox.ghost{border-style:dashed}
.dzr{display:flex;gap:6px;align-items:center;margin-bottom:6px}.dzr code{font-size:11px;color:var(--mut);min-width:46px}.dzr input{flex:1;min-width:0}
.dzr button{border:1px solid #ddd;background:#fff;border-radius:8px;min-width:40px;min-height:40px;color:var(--red);font:800 16px Arial}
.dzr.sel input{border-color:#2563eb;box-shadow:0 0 0 2px rgba(37,99,235,.2)}
.drow{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:8px}
.dup{cursor:pointer}.dsec{background:#fff!important;color:#151515!important;border:1px solid #ccc!important}
.dsteps{margin:6px 0 10px;padding-left:20px;font-size:14px}.dsteps li{margin-bottom:3px}

/* v19.15: open receipts to check */
.todo{border:2px solid #16a34a}
.tdg{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px}
.tdc{background:#fff;border:1px solid var(--line);border-left:6px solid #16a34a;border-radius:12px;padding:12px}
.tdc.od{border-left-color:var(--red)}
.tdh{display:flex;justify-content:space-between;gap:8px;align-items:flex-start}.tdh b{font-size:15px}
.tdod{background:var(--red);color:#fff;border-radius:6px;font:700 11px Arial;padding:2px 6px;white-space:nowrap}
.tdn{display:flex;justify-content:space-between;margin-top:8px;font-size:14px}
.tdbar{background:#e5e7eb}.tdbar i{background:#16a34a}
.tdf{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;margin-top:6px}
.tdl{text-decoration:none;font-size:12px}.tds{color:var(--mut)}.tds.tdsok{color:#166534;font-weight:700}.tds.tdswarn{color:#b45309;font-weight:700}
.tdgo{background:#16a34a!important;color:#fff!important;text-decoration:none;font-weight:800}

/* v19.16 login, calendar link, packing */
.top form.nav-out{margin:0;display:inline-flex}.top form.nav-out button{background:#a51d1b;color:#fff;border:1px solid #a51d1b;border-radius:6px;padding:6px 10px;font-size:13px;cursor:pointer;white-space:nowrap}
.top a.nav-in{border-color:#a51d1b}.top a.nav-cal,.top a.nav-pack{white-space:nowrap}
@media(max-width:560px){.top form.nav-out{flex:1 1 120px}.top form.nav-out button{width:100%;min-height:39px}}
.dbtns{display:grid;gap:8px}.dpack{background:#151515!important;color:#fff!important;text-align:center;text-decoration:none;padding:12px!important;margin:0!important;font-size:17px!important}
.pbox{border:2px solid #151515}.pbh{display:flex;justify-content:space-between;align-items:center}.pbh h2{margin:0}.pbh b{font:800 22px Arial}
.popen{background:#f59e0b;color:#fff;border-radius:6px;padding:2px 7px;font:700 11px Arial;letter-spacing:0;text-transform:none;vertical-align:2px}
.pcl{background:#16a34a;color:#fff;border-radius:6px;padding:2px 7px;font:700 11px Arial}
.pscan{width:100%;padding:16px;border:2px dashed #a51d1b;border-radius:10px;font-size:20px;margin-top:10px;background:#fff}
.pszg{display:flex;flex-wrap:wrap;gap:8px}.psz{min-width:64px;min-height:52px;font:800 17px Arial;border:1px solid #151515;background:#fff;border-radius:10px;cursor:pointer}
.prow{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid var(--line)}.pq{font:800 22px Arial;min-width:60px}
.ps{flex:1;display:flex;flex-direction:column}.ps small{color:var(--mut)}
.pbtn{width:46px;height:46px;font:800 22px Arial;border:1px solid #d1d5db;background:#fff;border-radius:10px;cursor:pointer}
.pdif{background:#dc2626;color:#fff;border-radius:6px;padding:3px 8px;font:800 13px Arial}
.pbad{color:#dc2626;font-weight:800}.ptr td{font-weight:800;border-top:2px solid #151515}
.pwarn{background:#fef3c7;border:1px solid #f59e0b;border-radius:8px;padding:10px;font-weight:700}
.pfix{margin-top:10px;border:1px solid var(--line);border-radius:10px;padding:10px}.pfix summary{font-weight:800;cursor:pointer}
.pok{display:none;background:#dcfce7;border:1px solid #16a34a;color:#166534;border-radius:8px;padding:8px 10px;font-weight:800;margin:8px 0 0}
.rnotfinal{border:2px solid #b45309;background:#fff7ed;color:#7c2d12;border-radius:10px;padding:12px 14px;margin:0 0 12px;font-size:14px}
.rbar{margin-bottom:10px}.rkg{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.rk{border:1px solid #e7e7e3;border-radius:10px;overflow:hidden;background:#fff;break-inside:avoid;page-break-inside:avoid}
.rk .rph{display:grid;grid-template-columns:1fr 1fr;gap:2px;background:#f4f4f2;border-bottom:1px solid #eee}.rk .rph.r1{grid-template-columns:1fr}
.rk .rimg{display:block;width:100%;height:260px;object-fit:contain;background:#f4f4f2}.rk .rph.r1 .rimg{height:340px}
.rep h2{break-after:avoid;page-break-after:avoid}
.rk .bd{padding:10px 12px 12px}.rk .hd{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.rk .szp{font:800 17px Arial;background:#151515;color:#fff;border-radius:8px;padding:3px 10px;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.rk .rs{font:700 13px Arial;color:var(--red);background:#fde8e8;border-radius:8px;padding:4px 9px;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.rk .wo{font-size:13px;margin-top:6px}.rk .tx{margin-top:6px;font-size:13px}.rk .meta{font-size:11px;color:var(--mut);margin-top:6px}.rk .rdraw{margin-top:6px}
.rk .rdraw .ldr-row{justify-content:flex-start}.rk .rdraw .lfig{max-width:90px}
.rep .hcol,.rep .hidep{display:none!important}
@media print{@page{size:A4;margin:0}.rep{padding:12mm 12mm!important}.rk .rimg{height:190px}.rk .rph.r1 .rimg{height:250px}.rkg{gap:8px}.rnotfinal{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
@media(max-width:700px){.rkg{grid-template-columns:1fr}}
.edbox{border:2px solid #151515}.edrow{display:flex;gap:8px}.edrow a{flex:1;text-align:center;padding:10px;border:1px solid #d1d5db;border-radius:8px;text-decoration:none;font-weight:800;color:inherit}.edrow a.on{background:#151515;color:#fff;border-color:#151515}
.ephs{display:flex;flex-wrap:wrap;gap:8px}.eph{display:flex;flex-direction:column;align-items:center;font-size:12px;gap:4px}.eph img{width:96px;height:96px;object-fit:cover;border-radius:8px}
.rhead{display:flex;align-items:center;gap:14px;margin:0 0 12px;padding-bottom:10px;border-bottom:2px solid #151515}.rhead img{height:38px;width:auto;filter:invert(1)}.rhead span{font:700 12px Arial;letter-spacing:.06em;text-transform:uppercase;color:#555}
.qdone{border-left:5px solid #f59e0b;display:flex;gap:10px;align-items:center;justify-content:space-between;flex-wrap:wrap}.qdone.on{border-left-color:#16a34a;background:#f0fdf4}
.erp{display:flex;gap:8px;align-items:center;margin-top:10px;font-weight:700;font-size:14px}.erp small{font-weight:400;color:var(--mut)}
.whoc{border:1px solid var(--line);background:#fff;padding:10px 14px}.whoc.wneed{border:3px solid #dc2626;background:#fef2f2;padding:14px}
.whoh{display:flex;align-items:center;gap:10px;font-size:16px;color:#151515}.whoh b{flex:1;color:#151515}
.whon{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;border-radius:50%;background:#dc2626;color:#fff;font:900 15px Arial;flex:0 0 26px}
.whoc.wok .whon{background:#16a34a}.whoe{font-size:13px;color:#555;display:none}.whoc.wok .whoe{display:inline}
.whob{margin-top:8px}.whoc.wok .whob{display:none}.whoc input{width:100%;font-size:18px;padding:12px}.whob small{display:block;color:#555;margin-top:4px}
.whoc.shake{animation:wsh .4s}@keyframes wsh{0%,100%{transform:translateX(0)}25%{transform:translateX(-8px)}75%{transform:translateX(8px)}}
.ic{width:1.15em;height:1.15em;vertical-align:-.2em;margin-right:.35em}
.arrbtn{display:block;background:#f59e0b;color:#151515;text-decoration:none;border-radius:12px;padding:14px 16px;margin-bottom:12px;font:800 18px Arial}.arrbtn small{display:block;font:400 13px Arial;margin-top:2px}
.pcmp{width:100%;border-collapse:collapse}.pcmp th,.pcmp td{padding:7px 5px;font-size:14px}.pcmp th{font-size:10px;letter-spacing:.3px}
@media(max-width:560px){.pcmp th,.pcmp td{padding:6px 3px;font-size:13px}.pcmp th{font-size:9px}}
.pprod{margin:-4px 0 10px;font-weight:800;font-size:15px}.pligone{opacity:.75}.pgn{font-size:13px;font-weight:700;color:#4b5563;margin-top:2px}
.pgone{background:#6b7280;color:#fff;border-radius:6px;padding:2px 7px;font:700 11px Arial}
.pgg{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:8px}.pgi{display:flex;flex-direction:column;font-weight:700;font-size:13px}.pgi input{padding:10px;font-size:17px;border:1px solid #d1d5db;border-radius:8px}
.pli{display:flex;justify-content:space-between;gap:10px;padding:10px 0;border-bottom:1px solid var(--line)}.pit{font-size:13px;margin-top:4px}
.pact{display:flex;gap:6px;align-items:center;flex-wrap:wrap;justify-content:flex-end}.pn{font:800 20px Arial;margin-right:4px}
"""


def head(t):
    return ('<!doctype html><html lang="' + ('en' if EN else 'de') + '"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
            '<meta name="robots" content="noindex"><title>' + t + ' – IQ Dogsport</title><style>' + CSS + '</style></head><body>')


def topbar(t, back):
    if GUEST:
        return ('<div style="background:#b45309;color:#fff;text-align:center;font:700 13px Arial;padding:6px">Lieferantenprüfung · ' + esc(GNAME) + '</div>'
                + '<div class="top"><div class="in"><a class="nav-logo" href="' + QB + '"><img src="' + LOGO + '" alt="IQ"></a><h1>' + t + '</h1>'
                + '<a class="nav-home" href="' + QB + '">Start</a><a class="nav-pack" href="' + QB + '&amp;view=pack">Verpacken</a><a id="gendb" href="' + QB + '&amp;gshow=1">Beenden</a></div></div>')
    return ('<div class="top"><div class="in"><a class="nav-logo" href="' + QB + '" title="QC Start"><img src="' + LOGO + '" alt="IQ"></a><h1>' + t + '</h1>'
            + (('<a class="nav-back" href="' + back + '">Zurück</a>') if back else '')
            + '<a class="nav-home" href="' + QB + '">Start</a>'
            + '<a class="nav-dash" href="' + QB + '&amp;view=dash">Dashboard</a>'
            + '<a class="nav-pack" href="' + QB + '&amp;view=pack">Verpacken</a>'
            + '<a class="nav-cal" href="' + CAL_URL + '" title="Lager- &amp; Teamkalender">Kalender</a>'
            + (('<form method="post" action="" class="nav-out"><input type="hidden" name="csrf_token" value="' + request.csrf_token() + '"><input type="hidden" name="key" value="' + KEY + '">'
                + '<input type="hidden" name="act" value="mlogout"><input type="hidden" name="next" value="' + esc(qself()) + '"><button type="submit" title="Führungskraft angemeldet">Abmelden (' + str(ADM_LEFT) + ' Min.)</button></form>')
               if ADM else ('<a class="nav-in" href="' + QB + '&amp;view=mlogin&amp;next=' + qself().replace('&', '%26') + '">Anmelden</a>'))
            + '<a href="#" onclick="document.cookie=\'iq_qc_lang=' + ('de' if EN else 'en') + ';path=/;max-age=31536000;SameSite=Lax\';location.reload();return false">' + ('DE' if EN else 'EN') + '</a></div></div>')


def qself():
    q = request.httprequest.query_string.decode('utf-8', 'ignore') if request else ''
    if not q.startswith('key=') or 'view=mlogin' in q:
        return QB + '&view=dash'
    return '?' + q


def esc(s):
    return (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def jsq(s):
    s = str(s or '')
    return '"' + s.replace(chr(92), chr(92) + chr(92)).replace('"', chr(92) + '"').replace(chr(13), chr(92) + 'r').replace(chr(10), chr(92) + 'n').replace('<', chr(92) + 'u003c').replace('>', chr(92) + 'u003e').replace('&', chr(92) + 'u0026').replace(chr(8232), chr(92) + 'u2028').replace(chr(8233), chr(92) + 'u2029') + '"'


def tr(s):
    if not EN:
        return s
    for a, b in TR:
        s = s.replace(a, b)
    return s


def resp(html):
    html = tr(html)
    return request.make_response(html, headers=[('Content-Type', 'text/html; charset=utf-8'), ('X-Robots-Tag', 'noindex'), ('Cache-Control', 'no-store')])


def txt(s):
    s = tr(s)
    return request.make_response(s, headers=[('Content-Type', 'text/plain; charset=utf-8'), ('Cache-Control', 'no-store')])


def size_of(p):
    vals = p.product_template_attribute_value_ids.mapped('name')
    return ' / '.join(vals) if vals else '–'


UNK = '[Größe unbekannt]'


def chk_size(c):
    if 'note' in CF and UNK in str(c.note or ''):
        return '?'
    return size_of(c.product_id)


def al_size(al):
    if 'description' in AF and UNK in str(al.description or ''):
        return '?'
    return size_of(al.product_id)


# ------------------------------------------------------------------ one-time paper import (11.–16.11.2026)
IMARK = 'IQ-QC-IMPORT-2026-11-16'
ICODES = {'WMD': 'IQD-EKL-WMD.', 'WPU': 'IQD-EKL-WPU.', 'MJD_GR': 'IQD-EKL-MJD4.GR.', 'MJD_BK': 'IQD-EKL-MJD4.BK.', 'MFJ_GR': 'IQD-EKL-MFJ4.GR.'}
HFMARK = 'IQ-QC-IMPORT-HF-2026-11-17'
ICOLOR = {'MJD_GR': 'grau', 'MJD_BK': 'schwarz', 'MFJ_GR': 'grau'}
IALIAS = [['2XL', 'XXL'], ['3XL', 'XXXL'], ['4XL', 'XXXXL']]


def imp_keys(v):
    ks = [str(x).upper().strip() for x in v.product_template_attribute_value_ids.mapped('name')]
    code = v.default_code or ''
    if '.' in code:
        ks.append(code.split('.')[-1].upper().strip())
    return ks


def imp_var(vs, size):
    w = [size.upper()]
    for grp in IALIAS:
        if size.upper() in grp:
            w = grp
    for v in vs:
        if [k for k in imp_keys(v) if k in w]:
            return v
    return False


def imp_vars(art):
    PA = Prod.with_context(active_test=False)
    vs = PA.search([('default_code', '=like', ICODES[art] + '%')])
    if not vs and art in ICOLOR:
        base = PA.search([('default_code', '=like', ICODES[art][:-3] + '%')], limit=1)
        if base:
            out = []
            for v in base.product_tmpl_id.with_context(active_test=False).product_variant_ids:
                if [x for x in v.product_template_attribute_value_ids.mapped('name') if ICOLOR[art] in str(x).lower()]:
                    out.append(v.id)
            vs = PA.browse(out)
    return vs


def hf_done():
    return QC.search_count([('note', 'ilike', HFMARK)]) if 'note' in CF else 0


def imp_done():
    return QC.search_count([('note', 'ilike', IMARK)]) if 'note' in CF else 0


def imp_picks(art):
    vs = imp_vars(art)
    if not vs:
        return Pick.browse([])
    return Pick.search([('picking_type_code', '=', 'incoming'), ('state', '!=', 'cancel'), ('move_ids.product_id', 'in', vs.ids)] + SUPDOM, order='id desc', limit=15)


SCANJS = ('var AC=null;function beep(k){try{AC=AC||new(window.AudioContext||window.webkitAudioContext)();if(AC.state==="suspended")AC.resume();'
          + 'var seq=k==="err"?[[220,.35]]:(k==="sw"?[[880,.09],[1320,.12]]:[[1500,.09]]),t=AC.currentTime;seq.forEach(function(q){var o=AC.createOscillator(),g=AC.createGain();o.type="square";o.frequency.value=q[0];'
          + 'g.gain.value=.12;o.connect(g);g.connect(AC.destination);o.start(t);o.stop(t+q[1]);t+=q[1]+.04})}catch(e){}if(navigator.vibrate)navigator.vibrate(k==="err"?[120,60,120]:40)}'
          + 'document.addEventListener("click",function(){try{AC=AC||new(window.AudioContext||window.webkitAudioContext)();AC.resume()}catch(e){}},{once:true});'
          + 'var SB="",ST=0,STO=null,SF=0,STG=null;function scanDone(){var c=SB.trim();SB="";SF=0;if(c.length>=4&&window.onScan)window.onScan(c)}'
          + 'function scanStrip(t){try{if(t&&t.value!==undefined&&SB&&t.value.slice(-SB.length)===SB)t.value=t.value.slice(0,-SB.length)}catch(x){}}'
          + 'document.addEventListener("keydown",function(e){var t=e.target,tag=(t&&t.tagName)||"";if(tag==="TEXTAREA"||(t&&(t.id==="mcode"||t.id==="pscan")))return;'
          + 'var inp=tag==="INPUT"&&/^(text|search|password|number|email|tel)$/.test(t.type||"text");'
          + 'var n=Date.now(),gap=n-ST;if(gap>120){SB="";SF=0}else if(gap<45)SF++;ST=n;clearTimeout(STO);STG=t;'
          + 'function fast(){return !inp||SF>=SB.length-2}'
          + 'if(e.key==="Enter"||e.key==="Tab"){if(SB.length>=4&&fast()){e.preventDefault();if(inp)scanStrip(t);scanDone()}return}'
          + 'if(e.key&&e.key.length===1){SB+=e.key;STO=setTimeout(function(){if(SB.length>=6&&fast()){if(inp)scanStrip(STG);scanDone()}},180)}},true);'
          + 'function scanPost(code,extra,cb){var fd=new FormData();fd.append("csrf_token",CSRF);fd.append("key",KEY);fd.append("act","scan");fd.append("code",code);for(var k in extra)fd.append(k,extra[k]);'
          + 'fetch(location.pathname,{method:"POST",body:fd,credentials:"same-origin"}).then(function(r){return r.text()}).then(function(t){cb(t.split("|"))}).catch(function(){cb(["ERR","Keine Verbindung – bitte nochmal."])})}'
          + 'function remPick(tm,v){try{if(v===undefined)return localStorage.getItem("iq_qc_pick_"+tm)||"";if(v)localStorage.setItem("iq_qc_pick_"+tm,v)}catch(e){return ""}}'
          + 'function goScan(a,auto){var url="?key="+KEY;if(a[7]==="M"&&remPick(a[2])){a[5]=remPick(a[2]);a[7]=""}if(a[7]==="M"){url+="&pt="+a[2]+"&sp="+a[1]}else{url+="&tmpl="+a[2]+(a[5]?"&pick="+a[5]:"")+"&sp="+a[1]+(a[7]==="N"?"&np=1":"")}'
          + 'try{sessionStorage.setItem("iq_qc_sw",a[4]);if(auto)sessionStorage.setItem("iq_qc_autook","1")}catch(e){}location.href=url}')


DEFECT_JS = r"""
(function(){
    // v19.10: one defect = (1) reason -> (2) place on the drawing -> (3) photo. Several defects per garment, one label.
    var btn=document.getElementById('save'),error=document.getElementById('err'),hint=document.getElementById('savehint');
    var EDM=(typeof EDIT!=='undefined'&&EDIT)?EDIT:'';
    var rid=String(Date.now())+'-'+Math.random().toString(36).slice(2);
    var ISN=KIND==='note',V0=(document.querySelector('#lview button')?document.querySelector('#lview button').getAttribute('data-v'):'V'),V=V0,LIST=[],cur=blank();
    var selR=document.getElementById('reason'),nt=document.getElementById('newtag'),cam=document.getElementById('fcam');
    function blank(){return {r:'',t:'',z:[],ph:[],nofoto:false}}
    function $(id){return document.getElementById(id)}
    function zlabel(c){var e=document.querySelector('[data-z="'+c+'"]');return e?e.getAttribute('data-l'):c}
    function placeOk(c){return ISN||c.z.length>0}
    function photoOk(c){return ISN||!!EDM||c.ph.length>0||c.nofoto}
    function complete(c){return !!c.r&&placeOk(c)&&photoOk(c)}
    function empty(c){return !c.r&&!c.z.length&&!c.ph.length}
    function flash(el){if(!el)return;el.classList.remove('qflash');void el.offsetWidth;el.classList.add('qflash');if(el.scrollIntoView)el.scrollIntoView({behavior:'smooth',block:'center'})}
    function msg(t){error.textContent=t;error.style.display=t?'block':'none'}

    // ---------- (1) reason
    function chipsOff(){document.querySelectorAll('#rchips button.on').forEach(function(x){x.classList.remove('on')})}
    document.querySelectorAll('#rchips button').forEach(function(b){b.onclick=function(){
      var was=b.classList.contains('on');chipsOff();selR.value='';nt.hidden=true;nt.value='';
      if(was){cur.r='';cur.t=''}else{b.classList.add('on');cur.r=b.getAttribute('data-n');cur.t=b.textContent.trim()}
      msg('');ui();
      if(cur.r&&!cur.z.length&&!ISN){var w=$('wo');if(w&&w.scrollIntoView)w.scrollIntoView({behavior:'smooth',block:'start'})}
    }});
    selR.onchange=function(){chipsOff();
      if(selR.value==='__new'){nt.hidden=false;nt.focus();cur.r=nt.value.trim();cur.t=cur.r}
      else{nt.hidden=true;cur.r=selR.value;cur.t=selR.value?selR.options[selR.selectedIndex].text:''}
      msg('');ui();
      if(cur.r&&!cur.z.length&&!ISN){var w=$('wo');if(w&&w.scrollIntoView)w.scrollIntoView({behavior:'smooth',block:'start'})}
    };
    nt.oninput=function(){cur.r=nt.value.trim();cur.t=cur.r;ui()};

    // ---------- (2) place
    document.querySelectorAll('[data-z]').forEach(function(z){z.addEventListener('click',function(){
      if(!cur.r){msg('Zuerst den Grund wählen (Schritt 1).');flash($('rbox'));return}
      var c=z.getAttribute('data-z'),i=cur.z.indexOf(c);
      if(i>=0)cur.z.splice(i,1);else{
        if(c==='X-ALL')cur.z=[];else{var j=cur.z.indexOf('X-ALL');if(j>=0)cur.z.splice(j,1);}
        cur.z.push(c);if(navigator.vibrate)try{navigator.vibrate(15)}catch(e){}
      }
      msg('');ui();
    })});
    document.querySelectorAll('#lview button').forEach(function(b){b.onclick=function(){V=b.getAttribute('data-v');ui()}});
    $('wo-lock').onclick=function(){msg('Zuerst den Grund wählen (Schritt 1).');flash($('rbox'))};
    $('ph-lock').onclick=function(){if(!cur.r){msg('Zuerst den Grund wählen (Schritt 1).');flash($('rbox'))}else{msg('Zuerst auf der Zeichnung antippen, wo der Fehler ist (Schritt 2).');flash($('wo'))}};

    // ---------- (3) photo
    function compress(file){return new Promise(function(resolve){
       var image=new Image(),url=URL.createObjectURL(file);
       image.onload=function(){try{var max=1600,scale=Math.min(1,max/Math.max(image.width,image.height)),c=document.createElement('canvas');
         c.width=Math.max(1,Math.round(image.width*scale));c.height=Math.max(1,Math.round(image.height*scale));
         c.getContext('2d').drawImage(image,0,0,c.width,c.height);URL.revokeObjectURL(url);
         c.toBlob(function(blob){resolve(blob||file)},'image/jpeg',0.82);
       }catch(e){URL.revokeObjectURL(url);resolve(file)}};
       image.onerror=function(){URL.revokeObjectURL(url);resolve(file)};image.src=url;
    })}
    $('fbtn').onclick=function(){if(!cur.r||!placeOk(cur)){$('ph-lock').onclick();return}cam.click()};
    cam.onchange=function(){var f=cam.files&&cam.files[0];if(!f)return;cam.value='';
      $('fbtn').disabled=true;$('fbtn').textContent='Foto wird vorbereitet …';
      compress(f).then(function(b){cur.ph.push({b:b,u:URL.createObjectURL(b)});cur.nofoto=false;ui()})
      .catch(function(){cur.ph.push({b:f,u:URL.createObjectURL(f)});ui()});
    };
    if($('nofoto'))$('nofoto').onclick=function(e){e.preventDefault();if(!cur.r||!placeOk(cur)){$('ph-lock').onclick();return}
      if(confirm('Ohne Foto weiter? Nur wenn wirklich kein Foto möglich ist.')){cur.nofoto=true;ui()}};
    function thumbs(box,c,removable){box.innerHTML='';c.ph.forEach(function(p,i){var w=document.createElement('span');w.className='qth';
      var im=document.createElement('img');im.src=p.u;im.alt='';w.appendChild(im);
      if(removable){var x=document.createElement('button');x.type='button';x.textContent='✕';x.setAttribute('aria-label','Foto entfernen');
        x.onclick=function(){c.ph.splice(i,1);ui()};w.appendChild(x);}
      box.appendChild(w)});}

    // ---------- list
    function addCur(){
      if(!cur.r){msg('Zuerst den Grund wählen (Schritt 1).');flash($('rbox'));return false}
      if(!placeOk(cur)){msg('Bitte auf der Zeichnung antippen, wo der Fehler ist (Schritt 2).');flash($('wo'));return false}
      if(!photoOk(cur)){msg('Bitte ein Foto vom Fehler aufnehmen (Schritt 3).');flash($('fotos'));return false}
      LIST.push(cur);cur=blank();V=V0;selR.value='';chipsOff();nt.value='';nt.hidden=true;msg('');ui();return true;
    }
    $('addf').onclick=function(){if(addCur()){var c=$('qcard');if(c&&c.scrollIntoView)c.scrollIntoView({behavior:'smooth',block:'start'})}};
    function render(){
      var box=$('flist');box.innerHTML='';
      LIST.forEach(function(it,i){
        var d=document.createElement('div');d.className='fi'+(ISN?' nt':'');
        var tx=document.createElement('div');var b=document.createElement('b');b.textContent=(i+1)+'. '+it.t;
        var sp=document.createElement('span');sp.textContent=it.z.length?it.z.map(zlabel).join(', '):'–';
        var th=document.createElement('div');th.className='qths';thumbs(th,it,false);
        if(!it.ph.length&&!ISN&&!it.ex){var nf=document.createElement('small');nf.className='photo-missing';nf.textContent='ohne Foto';th.appendChild(nf)}
        tx.appendChild(b);tx.appendChild(sp);tx.appendChild(th);d.appendChild(tx);
        var x=document.createElement('button');x.type='button';x.className='fx';x.textContent='✕';x.setAttribute('aria-label','Entfernen');
        x.onclick=function(){if(confirm('Fehler '+(i+1)+' entfernen?')){LIST.splice(i,1);ui()}};d.appendChild(x);box.appendChild(d);
      });
      $('fn').textContent=String(LIST.length);$('flist-card').hidden=!LIST.length;
    }

    // ---------- everything visible follows the state
    function ui(){
      var s1=!!cur.r,s2=s1&&placeOk(cur)&&(ISN||cur.z.length>0),s3=s2&&photoOk(cur);
      $('defno').textContent=(ISN?'Hinweis ':'Fehler ')+(LIST.length+1);
      [['st1',s1,true],['st2',s2,s1],['st3',s3,s2]].forEach(function(a){var e=$(a[0]);e.className=a[1]?'done':(a[2]?'cur':'')});
      $('wo').classList.toggle('qlock',!s1);$('wo-lock').hidden=s1;
      var phOpen=s1&&(ISN||cur.z.length>0);$('fotos').classList.toggle('qlock',!phOpen);$('ph-lock').hidden=phOpen;
      document.querySelectorAll('.ldraw').forEach(function(d){d.hidden=d.getAttribute('data-v')!==V});
      document.querySelectorAll('#lview button').forEach(function(b){var v=b.getAttribute('data-v');b.classList.toggle('on',v===V);
        b.setAttribute('data-n',String(cur.z.filter(function(z){return z.indexOf(v+'-')===0}).length))});
      document.querySelectorAll('[data-z]').forEach(function(z){var on=cur.z.indexOf(z.getAttribute('data-z'))>=0;
        if(z.classList)z.classList.toggle('on',on)});
      var zl=$('zsel');
      if(cur.z.length){zl.textContent='✓ '+cur.z.map(zlabel).join(', ');zl.className='zok'}
      else{zl.textContent=s1?'Auf die Zeichnung tippen – Vorne / Hinten / Innen':'';zl.className='none'}
      thumbs($('fthumbs'),cur,true);
      var fb=$('fbtn');fb.disabled=false;fb.textContent=cur.ph.length?'+ weiteres Foto':'Foto aufnehmen';
      $('fstate').textContent=cur.ph.length?('✓ '+cur.ph.length+' Foto(s)'):(cur.nofoto?'Ohne Foto (Ausnahme)':'');
      $('fstate').className=cur.ph.length||cur.nofoto?'fok':'';
      var ad=$('addf');ad.disabled=!complete(cur);
      render();
      var ready=(complete(cur)||(empty(cur)&&LIST.length>0));
      btn.disabled=!ready;btn.setAttribute('aria-disabled',String(!ready));
      hint.textContent=ready?((LIST.length+(complete(cur)?1:0))+' '+(ISN?'Hinweis(e)':'Fehler')+' · alles bereit'):
        (!cur.r?(LIST.length?'Nächster Fehler: Grund wählen – oder Fehler-Liste drucken':'Schritt 1: Grund wählen'):(!s2?'Schritt 2: Ort auf der Zeichnung antippen':'Schritt 3: Foto aufnehmen'));
      if(!cur.r&&LIST.length){btn.disabled=false;btn.setAttribute('aria-disabled','false')}
    }

    function fail(t){msg(t);btn.disabled=false;btn.textContent=SVT;}
    btn.onclick=function(){
        msg('');
        if(!empty(cur)){if(!complete(cur)){addCur();return}LIST.push(cur);cur=blank();ui()}
        if(!LIST.length){fail('Schritt 1: Grund wählen.');flash($('rbox'));return}
        var fd=new FormData();fd.append('csrf_token',CSRF);fd.append('key',KEY);fd.append('act',EDM?'defect_edit':'defect');fd.append('pid',(EDM&&document.getElementById('esize'))?document.getElementById('esize').value:PID);fd.append('pick',PICK);
        if(EDM){fd.append('aid',EDM);document.querySelectorAll('.ephx:checked').forEach(function(x){fd.append('delph',x.value)});var rpx=document.getElementById('ereprint');if(rpx&&rpx.checked)fd.append('reprint','1')}
        fd.append('reqid',rid);fd.append('tags',LIST.map(function(x){return x.r}).join('\n'));fd.append('newtag','');fd.append('kind',KIND);
        fd.append('garm',GARM);fd.append('defs',LIST.map(function(x){return x.r.replace(/[\t\n]/g,' ')+'\t'+x.z.join(',')}).join('\n'));
        var nph=0;LIST.forEach(function(x,i){x.ph.forEach(function(p){fd.append('photo_'+(i+1),p.b,'foto.jpg');nph++})});
        fd.append('note',document.getElementById('note').value);fd.append('who',who());
        btn.disabled=true;btn.textContent=nph?('Speichert + lädt '+nph+' Foto(s) hoch …'):'Speichert …';
        fetch(location.pathname,{method:'POST',body:fd,credentials:'same-origin'}).then(function(r){return r.text().then(function(t){if(!r.ok)throw new Error('Serverfehler '+r.status+': '+t.slice(0,180));return t})})
        .then(function(t){var a=t.split('|');if(a[0]!=='OK')throw new Error(a[1]||t);
            if(EDM){if(a[2]==='D')window.open('?key='+encodeURIComponent(KEY)+'&pdf_label='+encodeURIComponent(EDM),'_blank');location.replace(BACK);return}
            location.replace('?key='+encodeURIComponent(KEY)+'&photo_for='+encodeURIComponent(a[2])+'&stage=2&pr='+encodeURIComponent(a[4]||'')+'&pe='+encodeURIComponent(a[5]||'')+'&nph='+nph);
        }).catch(function(e){fail('Keine Verbindung oder Fehler – bitte erneut versuchen: '+e.message)});
    };
    function who(){try{return localStorage.getItem('iq_qc_who')||''}catch(e){return ''}}
    if(EDM){btn.textContent=SVT;LIST=EDEFS.map(function(d){return {r:d[0],t:d[1],z:d[2],ph:[],nofoto:true,ex:true}});var nn=document.getElementById('note');if(nn){nn.value=ENOTE||'';if(ENOTE&&nn.closest('details'))nn.closest('details').open=true}}
    ui();
})();
"""

EDIT_JS = r"""
(function(){
  // v19.14 drawing editor: one picture per side, boxes in fractions of the picture (0..1).
  var V='V',S={},cur=null;
  ['V','H','I'].forEach(function(v){var d=DV[v];S[v]={src:d.src,w:d.w,h:d.h,file:null,line:null,bits:null,cleared:false,
    z:d.z.map(function(z){return {c:z[0],l:z[1],x:d.w?z[2]/d.w:0,y:d.h?z[3]/d.h:0,w:d.w?z[4]/d.w:0,h:d.h?z[5]/d.h:0}})}});
  var stage=document.getElementById('dstage'),img=document.getElementById('dimgel'),boxes=document.getElementById('dboxes'),empty=document.getElementById('dempty');
  var zl=document.getElementById('dzl'),msg=document.getElementById('dmsg'),info=document.getElementById('dinfo');
  function $(id){return document.getElementById(id)}
  function say(t,bad){msg.textContent=t;msg.style.color=bad?'#b91c1c':'#15803d'}
  function newCode(v){var n=1,used={};S[v].z.forEach(function(z){used[z.c]=1});while(used[v+'-Z'+n])n++;return v+'-Z'+n}
  function render(){
    var s=S[V];
    document.querySelectorAll('#dv button').forEach(function(b){b.classList.toggle('on',b.getAttribute('data-v')===V);
      var n=S[b.getAttribute('data-v')].z.length;b.setAttribute('data-n',String(n))});
    if(s.src){img.src=s.src;img.style.display='block';empty.style.display='none'}else{img.removeAttribute('src');img.style.display='none';empty.style.display='flex'}
    info.textContent=s.src?(s.z.length+' Teil(e) markiert'+(s.file?' · neues Bild (noch nicht gespeichert)':'')):'Für diese Seite gibt es noch kein Bild.';
    boxes.innerHTML='';
    s.z.forEach(function(z,i){var b=document.createElement('div');b.className='dbox'+(cur===i?' sel':'');
      b.style.left=(z.x*100)+'%';b.style.top=(z.y*100)+'%';b.style.width=(z.w*100)+'%';b.style.height=(z.h*100)+'%';
      var t=document.createElement('span');t.textContent=z.l||'?';b.appendChild(t);
      boxes.appendChild(b)});
    zl.innerHTML='';
    if(!s.z.length){zl.innerHTML='<p class="mut" style="margin:0">Noch keine Teile markiert.</p>'}
    s.z.forEach(function(z,i){var r=document.createElement('div');r.className='dzr'+(cur===i?' sel':'');
      var c=document.createElement('code');c.textContent=z.c;
      var inp=document.createElement('input');inp.value=z.l;inp.setAttribute('list','dparts');inp.setAttribute('data-i',i);inp.placeholder='Name des Teils, z. B. Kapuze';
      inp.oninput=function(){z.l=inp.value;var bx=boxes.children[i];if(bx)bx.firstChild.textContent=z.l||'?'};
      inp.onfocus=function(){if(cur!==i){cur=i;var bx=boxes.children;for(var k=0;k<bx.length;k++)bx[k].classList.toggle('sel',k===i)}};
      var x=document.createElement('button');x.type='button';x.textContent='✕';x.title='Teil löschen';
      x.onclick=function(){s.z.splice(i,1);cur=null;render()};
      r.appendChild(c);r.appendChild(inp);r.appendChild(x);zl.appendChild(r)});
  }
  document.querySelectorAll('#dv button').forEach(function(b){b.onclick=function(){V=b.getAttribute('data-v');cur=null;render()}});
  // ---- drag a rectangle over the picture
  var drag=null,ghost=null;img.draggable=false;stage.addEventListener('dragstart',function(e){e.preventDefault()});
  stage.addEventListener('pointercancel',function(){drag=null;render()});
  function rel(e){var r=img.getBoundingClientRect();return {x:Math.min(1,Math.max(0,(e.clientX-r.left)/r.width)),y:Math.min(1,Math.max(0,(e.clientY-r.top)/r.height))}}
  stage.addEventListener('pointerdown',function(e){if(!S[V].src)return;e.preventDefault();drag=rel(e);ghost=document.createElement('div');ghost.className='dbox ghost';boxes.appendChild(ghost);
    try{stage.setPointerCapture(e.pointerId)}catch(x){}});
  stage.addEventListener('pointermove',function(e){if(!drag)return;var p=rel(e),x=Math.min(drag.x,p.x),y=Math.min(drag.y,p.y);
    ghost.style.left=(x*100)+'%';ghost.style.top=(y*100)+'%';ghost.style.width=(Math.abs(p.x-drag.x)*100)+'%';ghost.style.height=(Math.abs(p.y-drag.y)*100)+'%'});
  stage.addEventListener('pointerup',function(e){if(!drag)return;var p=rel(e),x=Math.min(drag.x,p.x),y=Math.min(drag.y,p.y),w=Math.abs(p.x-drag.x),h=Math.abs(p.y-drag.y);drag=null;
    if(w<0.02||h<0.02){render();return}
    S[V].z.push({c:newCode(V),l:'',x:x,y:y,w:w,h:h});cur=S[V].z.length-1;render();
    var inp=document.querySelector('#dzl input[data-i="'+cur+'"]');if(inp){inp.focus();if(inp.scrollIntoView)inp.scrollIntoView({block:'center'})}});
  // ---- upload: picture (JPEG) + black/white line version (PNG, for the label) + 1-bit raster (for the Brother RAW label)
  function lineCanvas(c){var w=c.width,h=c.height,src=c.getContext('2d').getImageData(0,0,w,h).data,g=new Float32Array(w*h);
    for(var i=0;i<w*h;i++)g[i]=0.299*src[i*4]+0.587*src[i*4+1]+0.114*src[i*4+2];
    var o=document.createElement('canvas');o.width=w;o.height=h;var ox=o.getContext('2d'),od=ox.createImageData(w,h),d=od.data;
    function G(x,y){x=x<0?0:(x>=w?w-1:x);y=y<0?0:(y>=h?h-1:y);return g[y*w+x]}
    for(var y=0;y<h;y++)for(var x=0;x<w;x++){
      var gx=(G(x+1,y-1)+2*G(x+1,y)+G(x+1,y+1))-(G(x-1,y-1)+2*G(x-1,y)+G(x-1,y+1));
      var gy=(G(x-1,y+1)+2*G(x,y+1)+G(x+1,y+1))-(G(x-1,y-1)+2*G(x,y-1)+G(x+1,y-1));
      var v=(Math.abs(gx)+Math.abs(gy))>48?0:255,k=(y*w+x)*4;d[k]=d[k+1]=d[k+2]=v;d[k+3]=255}
    ox.putImageData(od,0,0);return o}
  function bitsBlob(line){var bw=Math.min(400,line.width),bh=Math.round(line.height*bw/line.width),c=document.createElement('canvas');c.width=bw;c.height=bh;
    var x=c.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,bw,bh);x.drawImage(line,0,0,bw,bh);var d=x.getImageData(0,0,bw,bh).data,stride=Math.ceil(bw/8),buf=new Uint8Array(8+stride*bh);
    buf.set([73,81,66,49,bw>>8,bw&255,bh>>8,bh&255]);
    for(var yy=0;yy<bh;yy++)for(var xx=0;xx<bw;xx++){if(d[(yy*bw+xx)*4]<215)buf[8+yy*stride+(xx>>3)]|=(128>>(xx&7))}
    return new Blob([buf],{type:'application/octet-stream'})}
  $('dfile').onchange=function(){var f=this.files&&this.files[0];this.value='';if(!f)return;say('Bild wird vorbereitet …');
    var im=new Image(),url=URL.createObjectURL(f);
    im.onload=function(){var max=1100,sc=Math.min(1,max/Math.max(im.width,im.height)),c=document.createElement('canvas');
      c.width=Math.round(im.width*sc);c.height=Math.round(im.height*sc);var x=c.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,c.width,c.height);x.drawImage(im,0,0,c.width,c.height);URL.revokeObjectURL(url);
      var ln=lineCanvas(c),s=S[V];s.w=c.width;s.h=c.height;s.cleared=false;s.bits=bitsBlob(ln);
      c.toBlob(function(b){s.file=b;s.src=URL.createObjectURL(b);ln.toBlob(function(lb){s.line=lb;render();say('Bild geladen – jetzt Teile markieren und speichern.')},'image/png')},'image/jpeg',0.85)};
    im.onerror=function(){say('Bild konnte nicht gelesen werden.',true)};im.src=url};
  $('dclear').onclick=function(){var s=S[V];if(!s.src)return;if(!confirm('Bild und Kästen dieser Seite entfernen?'))return;s.src='';s.file=null;s.z=[];s.cleared=true;s.w=0;s.h=0;render()};
  function pin(){return '-'}
  function post(fd,done){fd.append('csrf_token',CSRF);fd.append('key',KEY);fd.append('tmpl',TMPL);
    fetch(location.pathname,{method:'POST',body:fd,credentials:'same-origin'}).then(function(r){return r.text()}).then(function(t){var a=t.split('|');if(a[0]==='OK')done();else say(a[1]||t,true)})
    .catch(function(){say('Keine Verbindung – bitte nochmal.',true)})}
  $('dsave').onclick=function(){var p=pin();if(!p)return;var fd=new FormData();fd.append('act','draw_save');fd.append('mpin',p);var miss='';
    ['V','H','I'].forEach(function(v){var s=S[v];if(s.cleared&&!s.src){fd.append('clear_'+v,'1');return}if(!s.src)return;
      if(s.file){fd.append('img_'+v,s.file,'bild.jpg');if(s.line)fd.append('line_'+v,s.line,'line.png');if(s.bits)fd.append('bits_'+v,s.bits,'bits.bin')}
      fd.append('w_'+v,String(s.w));fd.append('h_'+v,String(s.h));
      s.z.forEach(function(z){if(!(z.l||'').trim())miss=v});
      fd.append('zones_'+v,s.z.filter(function(z){return (z.l||'').trim()}).map(function(z){return [z.c,z.l.trim().replace(/[\t\n|]/g,' '),Math.round(z.x*s.w),Math.round(z.y*s.h),Math.max(1,Math.round(z.w*s.w)),Math.max(1,Math.round(z.h*s.h))].join('\t')}).join('\n'))});
    if(miss&&!confirm('Mindestens ein Kasten hat noch keinen Namen – Kästen ohne Namen werden nicht gespeichert. Trotzdem speichern?'))return;
    $('dsave').disabled=true;say('Speichert …');
    post(fd,function(){say('Gespeichert ✓');setTimeout(function(){location.reload()},700)});setTimeout(function(){$('dsave').disabled=false},2500)};
  if($('dcopy'))$('dcopy').onclick=function(){var p=pin();if(!p)return;if(!confirm('Zeichnung vom anderen Produkt übernehmen? Die aktuelle Zeichnung dieses Produkts wird ersetzt.'))return;
    var fd=new FormData();fd.append('act','draw_copy');fd.append('mpin',p);fd.append('from',$('dfrom').value);post(fd,function(){location.reload()})};
  if($('ddel'))$('ddel').onclick=function(){var p=pin();if(!p)return;if(!confirm('Eigene Zeichnung löschen? Danach wird wieder die Standard-Zeichnung benutzt.'))return;
    var fd=new FormData();fd.append('act','draw_del');fd.append('mpin',p);post(fd,function(){location.reload()})};
  render();
})();
"""

PHOTO_JS = r"""
(function(){
    var cam=document.getElementById('cam'),take=document.getElementById('take'),done=document.getElementById('done');
    var cancel=document.getElementById('cancel'),printer=document.getElementById('printer'),retry=document.getElementById('retry');
    var error=document.getElementById('err'),pics=document.getElementById('photos'),counter=document.getElementById('counter'),status=document.getElementById('photo-status');
    var uploaded=Number(counter.dataset.count||0),pending=0,failed=[];
    var photoRequired=document.getElementById('photo-required');
    function token(){return String(Date.now())+'-'+Math.random().toString(36).slice(2)}
    function feedback(t,isError){status.textContent=t;status.style.color=isError?'#b91c1c':'#15803d'}
    function errorText(t){error.style.display='block';error.textContent=t}
    var CURF='';
    function sync(){counter.textContent=uploaded?uploaded+' Foto(s) hochgeladen':NOPH;counter.className='mut';
      var needsPhoto=false;
      document.querySelectorAll('[data-f]').forEach(function(b){b.disabled=!!pending});
      done.disabled=!!pending||needsPhoto;done.setAttribute('aria-disabled',String(done.disabled));
      done.title=needsPhoto?'Foto erforderlich – mindestens ein Foto hochladen.':'';
      if(photoRequired){photoRequired.hidden=!needsPhoto;photoRequired.textContent=needsPhoto?'Mindestens ein Foto ist Pflicht, bevor Sie fortfahren.':'';}
      take.disabled=!!pending; if(cancel)cancel.disabled=!!pending;
      if(retry)retry.style.display=failed.length?'inline-block':'none';
    }
    function request(fd){return fetch(location.pathname,{method:'POST',body:fd,credentials:'same-origin'})
      .then(function(r){return r.text().then(function(t){var a=t.split('|');if(!r.ok||a[0]!=='OK')throw new Error(a[1]||('HTTP '+r.status));return a})})}
    function compress(file){return new Promise(function(resolve){
       var image=new Image(),url=URL.createObjectURL(file);
       image.onload=function(){try{var max=1600,scale=Math.min(1,max/Math.max(image.width,image.height)),c=document.createElement('canvas');
         c.width=Math.max(1,Math.round(image.width*scale));c.height=Math.max(1,Math.round(image.height*scale));
         c.getContext('2d').drawImage(image,0,0,c.width,c.height);URL.revokeObjectURL(url);
         c.toBlob(function(blob){resolve(blob||file)},'image/jpeg',0.82);
       }catch(e){URL.revokeObjectURL(url);resolve(file)}};
       image.onerror=function(){URL.revokeObjectURL(url);resolve(file)};image.src=url;
    })}
    function upload(blob,id,f){
       pending++;sync();feedback('Foto wird hochgeladen …',false);error.style.display='none';
       var fd=new FormData();fd.append('csrf_token',CSRF);fd.append('key',KEY);fd.append('act','photo_add');fd.append('aid',AID);fd.append('token',id);fd.append('fidx',f||'');fd.append('photo',blob,'foto.jpg');
       request(fd).then(function(a){
         uploaded=Number(a[2])||uploaded+1;var line=document.createElement('div');line.className='photo-ok';
         var image=document.createElement('img');image.src='?key='+encodeURIComponent(KEY)+'&img='+encodeURIComponent(a[1]);image.alt='';
         var title=document.createElement('span');title.textContent='Foto hochgeladen';line.appendChild(image);line.appendChild(title);(document.getElementById('ph-'+f)||pics).appendChild(line);
         feedback('Foto hochgeladen',false);
       }).catch(function(e){failed.push({blob:blob,id:id,f:f});feedback('Foto nicht hochgeladen',true);errorText('Upload fehlgeschlagen: '+e.message+' – Upload wiederholen.');
       }).finally(function(){pending--;sync()});
    }
    cam.onchange=function(){var f=cam.files&&cam.files[0],fx=CURF;if(!f)return;cam.value='';pending++;sync();
       compress(f).then(function(b){pending--;upload(b,token(),fx)}).catch(function(){pending--;upload(f,token(),fx)});
    };
    take.onclick=function(){CURF='';cam.click()};
    document.querySelectorAll('[data-f]').forEach(function(b){b.onclick=function(){if(pending)return;CURF=b.getAttribute('data-f');cam.click()}});
    if(retry)retry.onclick=function(){var q=failed.slice();failed=[];sync();q.forEach(function(x){upload(x.blob,x.id,x.f)})};
    done.onclick=function(){if(pending)return;
       if(failed.length&&!confirm('Mindestens ein Foto wurde NICHT hochgeladen. Trotzdem beenden?'))return;
       // Verify on the Odoo server that the photo really exists before navigating.
       done.disabled=true;var fd=new FormData();fd.append('csrf_token',CSRF);fd.append('key',KEY);fd.append('act','finish_photo');fd.append('aid',AID);
       request(fd).then(function(){
         try{if(STAGE2){sessionStorage.setItem('iq_qc_done',(ISNOTE?'Hinweis ':'Defekt ')+QA);
           if(CID&&CID!=='0')sessionStorage.setItem('iq_qc_last',CID+'|'+(ISNOTE?'Hinweis ':'Defekt ')+QA);
         }}catch(e){}
         location.href=RETURN_URL;
       }).catch(function(e){errorText('Abschluss nicht möglich: '+e.message);sync();});
    };
    if(cancel)cancel.onclick=function(){if(pending)return;
       if(!confirm((ISNOTE?'Hinweis ':'Defekt ')+QA+' vollständig löschen? Alle Fotos und die Prüfung werden gelöscht. Bereits gedrucktes Etikett entsorgen.'))return;
       cancel.disabled=true;var fd=new FormData();fd.append('csrf_token',CSRF);fd.append('key',KEY);fd.append('act','del');fd.append('aid',AID);
       request(fd).then(function(){location.href=SCAN_URL}).catch(function(e){cancel.disabled=false;errorText('Löschen fehlgeschlagen: '+e.message)});
    };
    if(printer)printer.onclick=function(){
       if(!HAS_PRINTER){location.href='?key='+encodeURIComponent(KEY)+'&pdf_label='+encodeURIComponent(AID);return}
       printer.disabled=true;var fd=new FormData();fd.append('csrf_token',CSRF);fd.append('key',KEY);fd.append('act','print');fd.append('aid',AID);
       request(fd).then(function(){feedback('Druckauftrag an Brother gesendet',false)}).catch(function(e){errorText('Druck fehlgeschlagen: '+e.message)}).finally(function(){printer.disabled=false});
    };
    sync();
})();
"""


def scan_prod(code):
    code = (code or '').strip()
    if len(code) < 3:
        return Prod.browse([])
    PA = Prod.with_context(active_test=False)
    p = PA.search([('barcode', '=', code)], limit=1)
    if not p:
        p = PA.search([('default_code', '=ilike', code)], limit=1)
    if not p and code.isdigit() and len(code) in (12, 13, 14):
        p = PA.search([('barcode', 'in', [code.lstrip('0'), code.zfill(13), code.zfill(14)])], limit=1)
    return p


def open_picks(tmpl):
    return Pick.search([('picking_type_code', '=', 'incoming'), ('state', 'not in', ['done', 'cancel']), ('move_ids.product_id.product_tmpl_id', '=', tmpl.id)] + SUPDOM,
                       order='scheduled_date desc', limit=15)


def choose_pick(p, cur, remembered):
    cands = open_picks(p.product_tmpl_id)
    for pid in [cur, remembered]:
        if pid and pid.isdigit() and int(pid) in cands.ids:
            return [Pick.browse(int(pid)), '']
    if len(cands) == 1:
        return [cands, '']
    if not cands:
        return [Pick.browse([]), 'N']
    exact = []
    for k in cands:
        if p.id in k.move_ids.mapped('product_id').ids:
            exact.append(k.id)
    if len(exact) == 1:
        return [Pick.browse(exact[0]), '']
    return [Pick.browse([]), 'M']



def sz_parts(label):
    parts = [x.strip() for x in (label or '').split(' / ')]
    zi = len(parts) - 1
    for i in range(len(parts)):
        if parts[i].upper() in SIZES:
            zi = i
    return [' / '.join([parts[i] for i in range(len(parts)) if i != zi]), parts[zi]]


def size_rank(s):
    u = (s or '').upper().split(' / ')[-1].strip()
    return SIZES.index(u) if u in SIZES else 50



def is_note(al):
    return 'description' in AF and NOTEMARK in str(al.description or '')


def photo_count(al):
    return Att.search_count([('res_model', '=', 'quality.alert'), ('res_id', '=', al.id), ('mimetype', '=like', 'image%')]) if al else 0


def pick_open(pk):
    return bool(pk) and pk.state not in ('done', 'cancel')


def reason_spelling(name):
    # Legacy quality tags can contain a typo; display/print the requested spelling.
    # This does not silently rename any existing Odoo quality.tag record.
    return (name or '').replace('Sizenetikett', 'Sizeetikett')


def tags_of(al):
    if TAG and al.tag_ids:
        return [reason_spelling(n) for n in al.tag_ids.mapped('name')]
    t = (al.title or '') if 'title' in AF else ''
    if ' · Gr. ' in t and ' @ ' in t:
        return [reason_spelling(x.split(' @ ')[0].replace('Hinweis: ', '').strip()) for x in t.split(' · Gr. ')[0].split('; ') if x.strip()]
    return [reason_spelling(x.strip()) for x in t.split(' · Gr. ')[0].split(',') if x.strip()] if ' · Gr. ' in t else []


def tl(n):
    return TAG_EN.get(n, n) if EN else n


def loc(dt):
    if not dt:
        return now
    m = dt.month
    return dt + datetime.timedelta(hours=2 if (4 <= m <= 9 or (m == 3 and dt.day >= 29) or (m == 10 and dt.day < 25)) else 1)


def checks_for(tmpl, pick, since):
    dom = [('product_id.product_tmpl_id', '=', tmpl.id), ('quality_state', 'in', ['pass', 'fail'])] + AUTO
    if pick:
        dom.append(('picking_id', '=', pick.id))
    if since:
        dom.append(('create_date', '>=', datetime.datetime.combine(since, datetime.time(0, 0))))
    return QC.search(dom)


def counts(tmpl, pick):
    cs = checks_for(tmpl, pick, False)
    ok = len([c for c in cs if c.quality_state == 'pass'])
    return str(len(cs)) + '|' + str(ok) + '|' + str(len(cs) - ok)


def get_pick():
    pk = str(params.get('pick') or '')
    return Pick.browse(int(pk)).exists() if pk.isdigit() else Pick.browse([])


def pick_short(pk):
    d = pk.date_done or pk.scheduled_date
    return (pk.origin or pk.name) + (' · ' + loc(d).strftime('%d.%m.') if d else '')


def pick_label(pk):
    d = pk.date_done or pk.scheduled_date
    return ((pk.origin + ' · ') if pk.origin else '') + (pk.partner_id.name or '') + (' · ' + loc(d).strftime('%d.%m.%Y') if d else '') + ' (' + pk.name + ')'


def ctx_q(tmpl, pick):
    return QB + '&amp;tmpl=' + str(tmpl.id) + ('&amp;pick=' + str(pick.id) if pick else '')


def who_of(al):
    d = str(al.description or '') if 'description' in AF else ''
    return d.split('Prüfer:')[1].split('<')[0].strip()[:30] if 'Prüfer:' in d else ''


def check_who(c):
    # Every interactive OK/defect/note saves this information in quality.check.note.
    d = str(c.note or '') if 'note' in CF else ''
    if 'Prüfer:' in d:
        nm = d.split('Prüfer:', 1)[1].split('<', 1)[0].split('\n', 1)[0].strip()
        nm = nm.split(' [IQ-QC-REQ:', 1)[0]
        nm = ' '.join(nm.split())[:80]
        if 'IQ-SUP:' in d:
            return sup_label(d, nm)
        if nm:
            return nm
    if 'IQ-SUP:' in d:
        return sup_label(d, '')
    return 'Prüfer nicht angegeben'


def inspector_key(s):
    return ' '.join(str(s or '').split()).lower()


def in_period(dt, period, local_today):
    if period == 'all':
        return True
    if not dt:
        return False
    delta = (local_today - loc(dt).date()).days
    if period == 'today':
        return delta == 0
    if period == '7':
        return 0 <= delta < 7
    if period == '30':
        return 0 <= delta < 30
    return True


def zclean(s):
    return (s or '').replace('^', ' ').replace('~', ' ').replace('\n', ' ')


def zfit(s, n):
    s = zclean(s)
    return s if len(s) <= n else s[:n - 2].rstrip() + '..'


def zwrap(s, n, maxl):
    words = zclean(s).split(' ')
    lines = ['']
    for w in words:
        if not w:
            continue
        if len(lines[-1]) + len(w) + (1 if lines[-1] else 0) <= n:
            lines[-1] = (lines[-1] + ' ' + w) if lines[-1] else w
        else:
            lines.append(w[:n])
    if len(lines) > maxl:
        lines = lines[:maxl]
        lines[-1] = zfit(lines[-1] + ' ..', n)
    return lines


def zd(x):
    return str(int(round(x * DPI / 203.0)))


# ------------------------------------------------------------------ v19.10 defect locations (where on the garment)
# One drawing set per product (front / back / inside), chosen automatically from the product:
#   wmd = Wintermantel Damen, wpu = Winter Parka Unisex, mfjd = Multifunktionsjacke 4.0 Damen,
#   mfjh = Multifunktionsjacke 4.0 Herren/Unisex, gen = any other product (simple jacket).
# Stored WITHOUT new fields in the quality.alert description, e.g.
#   <p>[ORT:wmd] Naht offen=V-SR,V-AR | Loch=H-RO</p>
# The title stays human readable: "Naht offen @ Vorne Schulter re., Vorne Ärmel re.; Loch @ Hinten Rücken oben · Gr. M".
# Left/right are ALWAYS seen from the wearer. Front and inside drawings show the wearer's right side
# on the viewer's LEFT; the back drawing shows it on the viewer's right.
LOCMARK = '[ORT:'
LOC_VIEWS = [['V', 'Vorne'], ['H', 'Hinten'], ['I', 'Innen']]
LOC_PROD = {'wmd': {'B': 300, 'out': 'M90 36 L56 44 L15 197 L45 204 L60 128 L56 300 L184 300 L180 128 L195 204 L225 197 L184 44 L150 36 Z', 'deco': {'V': '<path class="ld" d="M90 36 Q82 2 120 2 Q158 2 150 36"/><path class="ld" d="M99 36 Q101 14 120 13 Q139 14 141 36"/><line class="lq" x1="62" y1="70" x2="178" y2="70"/><line class="lq" x1="62" y1="98" x2="178" y2="98"/><line class="lq" x1="62" y1="126" x2="178" y2="126"/><line class="lq" x1="62" y1="154" x2="178" y2="154"/><line class="lq" x1="62" y1="182" x2="178" y2="182"/><line class="lq" x1="60" y1="222" x2="180" y2="222"/><line class="lq" x1="60" y1="248" x2="180" y2="248"/><line class="lq" x1="60" y1="274" x2="180" y2="274"/><line class="lzo" x1="60" y1="196" x2="180" y2="196"/><line class="lzp" x1="120" y1="36" x2="120" y2="300"/><line class="lq" x1="113" y1="36" x2="113" y2="300"/><path class="ld" d="M80 136 L84 176"/><path class="ld" d="M160 136 L156 176"/><rect class="lmd" x="90" y="180" width="10" height="9" rx="1"/><text class="llg" x="140" y="70">IQ</text><circle class="lpt" cx="200" cy="92" r="8"/>', 'H': '<path class="lo2" d="M86 42 Q78 0 120 0 Q162 0 154 42 Q120 56 86 42 Z"/><line class="lq" x1="62" y1="70" x2="178" y2="70"/><line class="lq" x1="62" y1="98" x2="178" y2="98"/><line class="lq" x1="62" y1="126" x2="178" y2="126"/><line class="lq" x1="62" y1="154" x2="178" y2="154"/><line class="lq" x1="62" y1="182" x2="178" y2="182"/><line class="lq" x1="60" y1="222" x2="180" y2="222"/><line class="lq" x1="60" y1="248" x2="180" y2="248"/><line class="lq" x1="60" y1="274" x2="180" y2="274"/><line class="lzo" x1="60" y1="196" x2="180" y2="196"/><circle class="lpt" cx="40" cy="92" r="8"/>', 'I': '<rect class="ld" x="104" y="38" width="32" height="14" rx="2"/><line class="lzo" x1="60" y1="196" x2="180" y2="196"/><rect class="ld" x="136" y="84" width="30" height="38" rx="2"/><line class="lq" x1="64" y1="110" x2="176" y2="110"/><line class="lq" x1="64" y1="150" x2="176" y2="150"/>'}, 'V': [['V-KA', 'p', '88,38 84,14 104,2 136,2 156,14 152,38'], ['V-SR', 'p', '58,43 90,34 104,36 104,62 63,62'], ['V-SL', 'p', '182,43 150,34 136,36 136,62 177,62'], ['V-BR', 'r', '62 64 50 42'], ['V-BL', 'r', '128 64 50 42'], ['V-TR', 'r', '62 108 50 64'], ['V-TL', 'r', '128 108 50 64'], ['V-MD', 'r', '82 173 26 14'], ['V-ZO', 'r', '58 188 124 16'], ['V-LR', 'r', '60 204 52 74'], ['V-LL', 'r', '128 204 52 74'], ['V-SA', 'r', '58 280 124 18'], ['V-RV', 'r', '112 36 16 262'], ['V-AR', 'p', '56,42 62,64 60,126 48,178 21,172'], ['V-AL', 'p', '184,42 178,64 180,126 192,178 219,172'], ['V-CR', 'p', '21,174 48,180 45,204 15,197'], ['V-CL', 'p', '219,174 192,180 195,204 225,197'], ['V-PL', 'r', '190 82 20 20']], 'H': [['H-KA', 'p', '86,42 80,12 100,0 140,0 160,12 154,42 120,54'], ['H-SL', 'p', '58,43 90,34 104,36 104,62 63,62'], ['H-SR', 'p', '182,43 150,34 136,36 136,62 177,62'], ['H-RO', 'r', '62 64 116 56'], ['H-RM', 'r', '62 122 116 64'], ['H-ZO', 'r', '58 188 124 16'], ['H-LL', 'r', '60 204 59 74'], ['H-LR', 'r', '121 204 59 74'], ['H-SA', 'r', '58 280 124 18'], ['H-AL', 'p', '56,42 62,64 60,126 48,178 21,172'], ['H-AR', 'p', '184,42 178,64 180,126 192,178 219,172'], ['H-CL', 'p', '21,174 48,180 45,204 15,197'], ['H-CR', 'p', '219,174 192,180 195,204 225,197'], ['H-PL', 'r', '30 82 20 20']], 'I': [['I-KR', 'r', '100 36 40 20'], ['I-FR', 'r', '62 58 50 128'], ['I-FL', 'r', '128 58 50 128'], ['I-IL', 'r', '132 80 38 46'], ['I-ZO', 'r', '58 188 124 16'], ['I-UF', 'r', '60 204 120 94'], ['I-AR', 'p', '56,42 62,64 60,126 45,204 15,197'], ['I-AL', 'p', '184,42 178,64 180,126 195,204 225,197']]}, 'wpu': {'B': 236, 'out': 'M90 36 L56 44 L15 197 L45 204 L60 128 L58 236 L182 236 L180 128 L195 204 L225 197 L184 44 L150 36 Z', 'deco': {'V': '<path class="ld" d="M90 36 Q82 2 120 2 Q158 2 150 36"/><path class="ld" d="M99 36 Q101 14 120 13 Q139 14 141 36"/><line class="lq" x1="62" y1="72" x2="178" y2="72"/><line class="lq" x1="62" y1="102" x2="178" y2="102"/><line class="lq" x1="62" y1="132" x2="178" y2="132"/><line class="lq" x1="62" y1="162" x2="178" y2="162"/><line class="lq" x1="62" y1="194" x2="178" y2="194"/><line class="lzp" x1="120" y1="36" x2="120" y2="236"/><line class="lq" x1="113" y1="36" x2="113" y2="236"/><path class="ld" d="M82 138 L86 184"/><path class="ld" d="M158 138 L154 184"/><rect class="lmd" x="94" y="196" width="10" height="9" rx="1"/><circle class="lpt" cx="200" cy="92" r="8"/><rect class="ld" x="18" y="186" width="14" height="6"/><rect class="ld" x="208" y="186" width="14" height="6"/>', 'H': '<path class="lo2" d="M86 42 Q78 0 120 0 Q162 0 154 42 Q120 56 86 42 Z"/><line class="lq" x1="62" y1="72" x2="178" y2="72"/><line class="lq" x1="62" y1="102" x2="178" y2="102"/><line class="lq" x1="62" y1="132" x2="178" y2="132"/><line class="lq" x1="62" y1="162" x2="178" y2="162"/><line class="lq" x1="62" y1="194" x2="178" y2="194"/><circle class="lpt" cx="40" cy="92" r="8"/>', 'I': '<rect class="ld" x="104" y="38" width="32" height="14" rx="2"/><line class="lq" x1="64" y1="100" x2="176" y2="100"/><line class="lq" x1="64" y1="150" x2="176" y2="150"/><line class="lq" x1="64" y1="200" x2="176" y2="200"/>'}, 'V': [['V-KA', 'p', '88,38 84,14 104,2 136,2 156,14 152,38'], ['V-SR', 'p', '58,43 90,34 104,36 104,62 63,62'], ['V-SL', 'p', '182,43 150,34 136,36 136,62 177,62'], ['V-BR', 'r', '62 64 50 54'], ['V-BL', 'r', '128 64 50 54'], ['V-TR', 'r', '62 120 50 70'], ['V-TL', 'r', '128 120 50 70'], ['V-MD', 'r', '88 192 22 16'], ['V-SA', 'r', '61 210 118 24'], ['V-RV', 'r', '112 36 16 198'], ['V-AR', 'p', '56,42 62,64 60,126 48,178 21,172'], ['V-AL', 'p', '184,42 178,64 180,126 192,178 219,172'], ['V-CR', 'p', '21,174 48,180 45,204 15,197'], ['V-CL', 'p', '219,174 192,180 195,204 225,197'], ['V-PL', 'r', '190 82 20 20']], 'H': [['H-KA', 'p', '86,42 80,12 100,0 140,0 160,12 154,42 120,54'], ['H-SL', 'p', '58,43 90,34 104,36 104,62 63,62'], ['H-SR', 'p', '182,43 150,34 136,36 136,62 177,62'], ['H-RO', 'r', '62 64 116 62'], ['H-RM', 'r', '62 128 116 80'], ['H-SA', 'r', '61 210 118 24'], ['H-AL', 'p', '56,42 62,64 60,126 48,178 21,172'], ['H-AR', 'p', '184,42 178,64 180,126 192,178 219,172'], ['H-CL', 'p', '21,174 48,180 45,204 15,197'], ['H-CR', 'p', '219,174 192,180 195,204 225,197'], ['H-PL', 'r', '30 82 20 20']], 'I': [['I-KR', 'r', '100 36 40 20'], ['I-FR', 'r', '62 58 50 176'], ['I-FL', 'r', '128 58 50 176'], ['I-IL', 'r', '132 80 38 46'], ['I-AR', 'p', '56,42 62,64 60,126 45,204 15,197'], ['I-AL', 'p', '184,42 178,64 180,126 195,204 225,197']]}, 'mfjd': {'B': 240, 'out': 'M90 36 L56 44 L15 197 L45 204 L60 128 L57 240 L183 240 L180 128 L195 204 L225 197 L184 44 L150 36 Z', 'deco': {'V': '<path class="ld" d="M90 36 Q82 2 120 2 Q158 2 150 36"/><path class="ld" d="M99 36 Q101 14 120 13 Q139 14 141 36"/><path class="ldk" d="M60 136 L60 240 L180 240 L180 136 Z"/><path class="ldk" d="M62 64 L74 64 L72 134 L62 134 Z"/><path class="ldk" d="M178 64 L166 64 L168 134 L178 134 Z"/><line class="lzp" x1="120" y1="36" x2="120" y2="240"/><line class="lq" x1="113" y1="36" x2="113" y2="240"/><line class="lzp" x1="90" y1="70" x2="90" y2="102"/><line class="lzp" x1="150" y1="70" x2="150" y2="102"/><text class="llg" x="160" y="74">IQ</text><rect class="lbl" x="58" y="124" width="124" height="12"/><rect class="lbk" x="112" y="122" width="16" height="16" rx="2"/><rect class="ld" x="66" y="146" width="44" height="58" rx="3"/><line class="ld" x1="66" y1="162" x2="110" y2="162"/><rect class="ld" x="130" y="146" width="44" height="58" rx="3"/><line class="ld" x1="130" y1="162" x2="174" y2="162"/><line class="lzp" x1="38" y1="80" x2="34" y2="106"/><rect class="lpt" x="197" y="84" width="13" height="17" rx="2"/><rect class="ld" x="16" y="184" width="16" height="7"/><rect class="ld" x="208" y="184" width="16" height="7"/>', 'H': '<path class="lo2" d="M86 42 Q78 0 120 0 Q162 0 154 42 Q120 56 86 42 Z"/><rect class="ld" x="114" y="34" width="12" height="16" rx="2"/><path class="ldk" d="M60 136 L60 240 L180 240 L180 136 Z"/><rect class="lbl" x="58" y="124" width="124" height="10"/><path class="ld" d="M76 140 L164 140 L160 218 L80 218 Z"/><circle class="ld" cx="108" cy="232" r="2"/><circle class="ld" cx="120" cy="232" r="2"/><circle class="ld" cx="132" cy="232" r="2"/><rect class="lpt" x="31" y="84" width="13" height="17" rx="2"/>', 'I': '<rect class="ld" x="104" y="38" width="32" height="14" rx="2"/><path class="lq" d="M64 70 L176 182 M64 110 L136 182 M64 150 L104 182 M100 58 L176 134 M140 58 L176 94 M176 70 L64 182 M176 110 L104 182 M176 150 L136 182 M140 58 L64 134 M100 58 L64 94"/><circle class="lmg" cx="88" cy="74" r="7"/><circle class="lmg" cx="152" cy="74" r="7"/><circle class="lmg" cx="80" cy="176" r="7"/>'}, 'V': [['V-KA', 'p', '88,38 84,14 104,2 136,2 156,14 152,38'], ['V-SR', 'p', '58,43 90,34 104,36 104,62 63,62'], ['V-SL', 'p', '182,43 150,34 136,36 136,62 177,62'], ['V-BR', 'r', '62 64 50 56'], ['V-BL', 'r', '128 64 50 56'], ['V-GU', 'r', '58 121 124 18'], ['V-TR', 'r', '62 141 50 68'], ['V-TL', 'r', '128 141 50 68'], ['V-SA', 'r', '59 212 122 26'], ['V-RV', 'r', '112 36 16 202'], ['V-AR', 'p', '56,42 62,64 60,126 48,178 21,172'], ['V-AL', 'p', '184,42 178,64 180,126 192,178 219,172'], ['V-CR', 'p', '21,174 48,180 45,204 15,197'], ['V-CL', 'p', '219,174 192,180 195,204 225,197'], ['V-AZ', 'r', '26 76 20 34'], ['V-PL', 'r', '193 80 20 24']], 'H': [['H-KA', 'p', '86,42 80,12 100,0 140,0 160,12 154,42 120,54'], ['H-SL', 'p', '58,43 90,34 104,36 104,62 63,62'], ['H-SR', 'p', '182,43 150,34 136,36 136,62 177,62'], ['H-RO', 'r', '62 64 116 58'], ['H-GU', 'r', '58 122 124 14'], ['H-NL', 'r', '62 138 14 80'], ['H-RT', 'r', '76 138 88 82'], ['H-NR', 'r', '164 138 14 80'], ['H-SA', 'r', '59 222 122 16'], ['H-AL', 'p', '56,42 62,64 60,126 48,178 21,172'], ['H-AR', 'p', '184,42 178,64 180,126 192,178 219,172'], ['H-CL', 'p', '21,174 48,180 45,204 15,197'], ['H-CR', 'p', '219,174 192,180 195,204 225,197'], ['H-PL', 'r', '27 80 20 24']], 'I': [['I-KR', 'r', '100 36 40 20'], ['I-FR', 'r', '62 58 50 178'], ['I-FL', 'r', '128 58 50 178'], ['I-MR', 'r', '76 62 26 26'], ['I-ML', 'r', '138 62 26 26'], ['I-MU', 'r', '66 162 28 28'], ['I-AR', 'p', '56,42 62,64 60,126 45,204 15,197'], ['I-AL', 'p', '184,42 178,64 180,126 195,204 225,197']]}, 'mfjh': {'B': 240, 'out': 'M90 36 L56 44 L15 197 L45 204 L60 128 L58 240 L182 240 L180 128 L195 204 L225 197 L184 44 L150 36 Z', 'deco': {'V': '<path class="ldk" d="M60 62 L60 240 L180 240 L180 62 Z"/><path class="llt" d="M56 44 L15 197 L30 200 L64 66 Z"/><path class="llt" d="M184 44 L225 197 L210 200 L176 66 Z"/><path class="llt" d="M90 36 L56 44 L52 60 L62 66 L178 66 L188 60 L184 44 L150 36 Z"/><path class="ld" d="M90 36 Q82 2 120 2 Q158 2 150 36"/><path class="ld" d="M99 36 Q101 14 120 13 Q139 14 141 36"/><line class="lzp" x1="120" y1="36" x2="120" y2="240"/><line class="lq" x1="113" y1="36" x2="113" y2="240"/><line class="lzp" x1="70" y1="58" x2="104" y2="58"/><line class="lzp" x1="136" y1="58" x2="170" y2="58"/><rect class="ld" x="68" y="70" width="40" height="40" rx="3"/><line class="ld" x1="68" y1="84" x2="108" y2="84"/><rect class="ld" x="132" y="70" width="40" height="40" rx="3"/><line class="ld" x1="132" y1="84" x2="172" y2="84"/><text class="llg" x="146" y="102">IQ</text><rect class="ld" x="66" y="150" width="44" height="58" rx="3"/><line class="ld" x1="66" y1="166" x2="110" y2="166"/><rect class="ld" x="130" y="150" width="44" height="58" rx="3"/><line class="ld" x1="130" y1="166" x2="174" y2="166"/><rect class="lpt" x="197" y="84" width="13" height="17" rx="2"/><rect class="ld" x="16" y="184" width="16" height="7"/><rect class="ld" x="208" y="184" width="16" height="7"/>', 'H': '<path class="ldk" d="M60 70 L60 240 L180 240 L180 70 Z"/><path class="llt" d="M56 44 L15 197 L30 200 L64 66 Z"/><path class="llt" d="M184 44 L225 197 L210 200 L176 66 Z"/><path class="llt" d="M90 36 L56 44 L52 60 L62 74 L178 74 L188 60 L184 44 L150 36 Z"/><path class="lo2" d="M86 42 Q78 0 120 0 Q162 0 154 42 Q120 56 86 42 Z"/><path class="ld" d="M76 134 L164 134 L160 218 L80 218 Z"/><line class="ld" x1="76" y1="134" x2="164" y2="134"/><circle class="ld" cx="108" cy="232" r="2"/><circle class="ld" cx="120" cy="232" r="2"/><circle class="ld" cx="132" cy="232" r="2"/><rect class="lpt" x="31" y="84" width="13" height="17" rx="2"/>', 'I': '<rect class="ld" x="104" y="38" width="32" height="14" rx="2"/><line class="lq" x1="64" y1="100" x2="176" y2="100"/><line class="lq" x1="64" y1="150" x2="176" y2="150"/><line class="lq" x1="64" y1="200" x2="176" y2="200"/><rect class="ld" x="74" y="84" width="30" height="38" rx="2"/><rect class="ld" x="136" y="84" width="30" height="38" rx="2"/>'}, 'V': [['V-KA', 'p', '88,38 84,14 104,2 136,2 156,14 152,38'], ['V-SR', 'p', '58,43 90,34 104,36 104,62 63,62'], ['V-SL', 'p', '182,43 150,34 136,36 136,62 177,62'], ['V-BR', 'r', '64 66 48 48'], ['V-BL', 'r', '128 66 48 48'], ['V-MR', 'r', '62 116 50 30'], ['V-ML', 'r', '128 116 50 30'], ['V-TR', 'r', '62 148 50 64'], ['V-TL', 'r', '128 148 50 64'], ['V-SA', 'r', '59 214 122 24'], ['V-RV', 'r', '112 36 16 202'], ['V-AR', 'p', '56,42 62,64 60,126 48,178 21,172'], ['V-AL', 'p', '184,42 178,64 180,126 192,178 219,172'], ['V-CR', 'p', '21,174 48,180 45,204 15,197'], ['V-CL', 'p', '219,174 192,180 195,204 225,197'], ['V-PL', 'r', '193 80 20 24']], 'H': [['H-KA', 'p', '86,42 80,12 100,0 140,0 160,12 154,42 120,54'], ['H-SL', 'p', '58,43 90,34 104,36 104,62 63,62'], ['H-SR', 'p', '182,43 150,34 136,36 136,62 177,62'], ['H-RO', 'r', '62 64 116 68'], ['H-NL', 'r', '62 134 14 84'], ['H-RT', 'r', '76 134 88 86'], ['H-NR', 'r', '164 134 14 84'], ['H-SA', 'r', '59 222 122 16'], ['H-AL', 'p', '56,42 62,64 60,126 48,178 21,172'], ['H-AR', 'p', '184,42 178,64 180,126 192,178 219,172'], ['H-CL', 'p', '21,174 48,180 45,204 15,197'], ['H-CR', 'p', '219,174 192,180 195,204 225,197'], ['H-PL', 'r', '27 80 20 24']], 'I': [['I-KR', 'r', '100 36 40 20'], ['I-FR', 'r', '62 58 50 178'], ['I-FL', 'r', '128 58 50 178'], ['I-IR', 'r', '72 80 34 46'], ['I-IL', 'r', '134 80 34 46'], ['I-AR', 'p', '56,42 62,64 60,126 45,204 15,197'], ['I-AL', 'p', '184,42 178,64 180,126 195,204 225,197']]}, 'gen': {'B': 230, 'out': 'M90 36 L56 44 L15 197 L45 204 L60 128 L60 230 L180 230 L180 128 L195 204 L225 197 L184 44 L150 36 Z', 'deco': {'V': '<line class="lzp" x1="120" y1="36" x2="120" y2="230"/>', 'H': '', 'I': ''}, 'V': [['V-KR', 'r', '92 12 56 24'], ['V-SR', 'p', '58,43 90,34 104,36 104,62 63,62'], ['V-SL', 'p', '182,43 150,34 136,36 136,62 177,62'], ['V-BR', 'r', '62 64 50 50'], ['V-BL', 'r', '128 64 50 50'], ['V-TR', 'r', '62 116 50 84'], ['V-TL', 'r', '128 116 50 84'], ['V-SA', 'r', '60 202 120 26'], ['V-RV', 'r', '112 36 16 192'], ['V-AR', 'p', '56,42 62,64 60,126 48,178 21,172'], ['V-AL', 'p', '184,42 178,64 180,126 192,178 219,172'], ['V-CR', 'p', '21,174 48,180 45,204 15,197'], ['V-CL', 'p', '219,174 192,180 195,204 225,197']], 'H': [['H-KR', 'r', '92 12 56 24'], ['H-SL', 'p', '58,43 90,34 104,36 104,62 63,62'], ['H-SR', 'p', '182,43 150,34 136,36 136,62 177,62'], ['H-RO', 'r', '62 64 116 66'], ['H-RM', 'r', '62 132 116 68'], ['H-SA', 'r', '60 202 120 26'], ['H-AL', 'p', '56,42 62,64 60,126 48,178 21,172'], ['H-AR', 'p', '184,42 178,64 180,126 192,178 219,172'], ['H-CL', 'p', '21,174 48,180 45,204 15,197'], ['H-CR', 'p', '219,174 192,180 195,204 225,197']], 'I': [['I-KR', 'r', '100 36 40 20'], ['I-FR', 'r', '62 58 50 170'], ['I-FL', 'r', '128 58 50 170'], ['I-IR', 'r', '72 80 34 46'], ['I-IL', 'r', '134 80 34 46'], ['I-AR', 'p', '56,42 62,64 60,126 45,204 15,197'], ['I-AL', 'p', '184,42 178,64 180,126 195,204 225,197']]}}
LOC_PLAB = {'wmd': {'V-KA': ['Vorne · Kapuze', 'Vorne Kapuze'], 'V-SR': ['Vorne · Schulter rechts', 'Vorne Schulter re.'], 'V-SL': ['Vorne · Schulter links', 'Vorne Schulter li.'], 'V-BR': ['Vorne · Brust rechts', 'Vorne Brust re.'], 'V-BL': ['Vorne · Brust links / IQ-Logo', 'Vorne Brust li.'], 'V-TR': ['Vorne · Seitentasche rechts (RV)', 'Vorne Seitentasche re.'], 'V-TL': ['Vorne · Seitentasche links (RV)', 'Vorne Seitentasche li.'], 'V-MD': ['Vorne · MagDock-Clip', 'Vorne MagDock-Clip'], 'V-ZO': ['Vorne · Zip-off (Reißverschluss Unterteil)', 'Vorne Zip-off'], 'V-LR': ['Vorne · Unterteil rechts', 'Vorne Unterteil re.'], 'V-LL': ['Vorne · Unterteil links', 'Vorne Unterteil li.'], 'V-SA': ['Vorne · Saum unten', 'Vorne Saum'], 'V-RV': ['Vorne · Front-Reißverschluss / Leiste / Druckknöpfe', 'Vorne Front-RV/Leiste'], 'V-AR': ['Vorne · Ärmel rechts', 'Vorne Ärmel re.'], 'V-AL': ['Vorne · Ärmel links', 'Vorne Ärmel li.'], 'V-CR': ['Vorne · Bündchen rechts', 'Vorne Bündchen re.'], 'V-CL': ['Vorne · Bündchen links', 'Vorne Bündchen li.'], 'V-PL': ['Vorne · Patch Ärmel links', 'Vorne Patch li.'], 'H-KA': ['Hinten · Kapuze', 'Hinten Kapuze'], 'H-SL': ['Hinten · Schulter links', 'Hinten Schulter li.'], 'H-SR': ['Hinten · Schulter rechts', 'Hinten Schulter re.'], 'H-RO': ['Hinten · Rücken oben', 'Hinten Rücken oben'], 'H-RM': ['Hinten · Rücken Mitte', 'Hinten Rücken Mitte'], 'H-ZO': ['Hinten · Zip-off (Reißverschluss Unterteil)', 'Hinten Zip-off'], 'H-LL': ['Hinten · Unterteil links', 'Hinten Unterteil li.'], 'H-LR': ['Hinten · Unterteil rechts', 'Hinten Unterteil re.'], 'H-SA': ['Hinten · Saum unten', 'Hinten Saum'], 'H-AL': ['Hinten · Ärmel links', 'Hinten Ärmel li.'], 'H-AR': ['Hinten · Ärmel rechts', 'Hinten Ärmel re.'], 'H-CL': ['Hinten · Bündchen links', 'Hinten Bündchen li.'], 'H-CR': ['Hinten · Bündchen rechts', 'Hinten Bündchen re.'], 'H-PL': ['Hinten · Patch Ärmel links', 'Hinten Patch li.'], 'I-KR': ['Innen · Nacken / Etikett', 'Innen Etikett'], 'I-FR': ['Innen · Futter rechts', 'Innen Futter re.'], 'I-FL': ['Innen · Futter links', 'Innen Futter li.'], 'I-IL': ['Innen · Innentasche links', 'Innen Innentasche li.'], 'I-ZO': ['Innen · Zip-off innen', 'Innen Zip-off innen'], 'I-UF': ['Innen · Futter Unterteil', 'Innen Futter Unterteil'], 'I-AR': ['Innen · Ärmelfutter rechts', 'Innen Ärmelfutter re.'], 'I-AL': ['Innen · Ärmelfutter links', 'Innen Ärmelfutter li.']}, 'wpu': {'V-KA': ['Vorne · Kapuze', 'Vorne Kapuze'], 'V-SR': ['Vorne · Schulter rechts', 'Vorne Schulter re.'], 'V-SL': ['Vorne · Schulter links', 'Vorne Schulter li.'], 'V-BR': ['Vorne · Brust rechts', 'Vorne Brust re.'], 'V-BL': ['Vorne · Brust links', 'Vorne Brust li.'], 'V-TR': ['Vorne · Seitentasche rechts (RV)', 'Vorne Seitentasche re.'], 'V-TL': ['Vorne · Seitentasche links (RV)', 'Vorne Seitentasche li.'], 'V-MD': ['Vorne · MagDock-Clip', 'Vorne MagDock-Clip'], 'V-SA': ['Vorne · Saum / Bund', 'Vorne Saum'], 'V-RV': ['Vorne · Front-Reißverschluss / Leiste / Druckknöpfe', 'Vorne Front-RV/Leiste'], 'V-AR': ['Vorne · Ärmel rechts', 'Vorne Ärmel re.'], 'V-AL': ['Vorne · Ärmel links', 'Vorne Ärmel li.'], 'V-CR': ['Vorne · Bündchen rechts', 'Vorne Bündchen re.'], 'V-CL': ['Vorne · Bündchen links', 'Vorne Bündchen li.'], 'V-PL': ['Vorne · Patch Ärmel links', 'Vorne Patch li.'], 'H-KA': ['Hinten · Kapuze', 'Hinten Kapuze'], 'H-SL': ['Hinten · Schulter links', 'Hinten Schulter li.'], 'H-SR': ['Hinten · Schulter rechts', 'Hinten Schulter re.'], 'H-RO': ['Hinten · Rücken oben', 'Hinten Rücken oben'], 'H-RM': ['Hinten · Rücken unten', 'Hinten Rücken unten'], 'H-SA': ['Hinten · Saum / Bund', 'Hinten Saum'], 'H-AL': ['Hinten · Ärmel links', 'Hinten Ärmel li.'], 'H-AR': ['Hinten · Ärmel rechts', 'Hinten Ärmel re.'], 'H-CL': ['Hinten · Bündchen links', 'Hinten Bündchen li.'], 'H-CR': ['Hinten · Bündchen rechts', 'Hinten Bündchen re.'], 'H-PL': ['Hinten · Patch Ärmel links', 'Hinten Patch li.'], 'I-KR': ['Innen · Nacken / Etikett', 'Innen Etikett'], 'I-FR': ['Innen · Futter rechts', 'Innen Futter re.'], 'I-FL': ['Innen · Futter links', 'Innen Futter li.'], 'I-IL': ['Innen · Innentasche links', 'Innen Innentasche li.'], 'I-AR': ['Innen · Ärmelfutter rechts', 'Innen Ärmelfutter re.'], 'I-AL': ['Innen · Ärmelfutter links', 'Innen Ärmelfutter li.']}, 'mfjd': {'V-KA': ['Vorne · Kapuze', 'Vorne Kapuze'], 'V-SR': ['Vorne · Schulter rechts', 'Vorne Schulter re.'], 'V-SL': ['Vorne · Schulter links', 'Vorne Schulter li.'], 'V-BR': ['Vorne · Brusttasche rechts (RV)', 'Vorne Brusttasche re.'], 'V-BL': ['Vorne · Brusttasche links (RV) / IQ-Logo', 'Vorne Brusttasche li.'], 'V-GU': ['Vorne · Gürtel / Schnalle', 'Vorne Gürtel'], 'V-TR': ['Vorne · Pattentasche unten rechts', 'Vorne Pattentasche re.'], 'V-TL': ['Vorne · Pattentasche unten links', 'Vorne Pattentasche li.'], 'V-SA': ['Vorne · Saum unten', 'Vorne Saum'], 'V-RV': ['Vorne · Front-Reißverschluss / Leiste / Druckknöpfe', 'Vorne Front-RV/Leiste'], 'V-AR': ['Vorne · Ärmel rechts', 'Vorne Ärmel re.'], 'V-AL': ['Vorne · Ärmel links', 'Vorne Ärmel li.'], 'V-CR': ['Vorne · Bündchen rechts', 'Vorne Bündchen re.'], 'V-CL': ['Vorne · Bündchen links', 'Vorne Bündchen li.'], 'V-AZ': ['Vorne · Ärmeltasche rechts (RV)', 'Vorne Ärmeltasche re.'], 'V-PL': ['Vorne · Klett-Patch Ärmel links', 'Vorne Klett-Patch li.'], 'H-KA': ['Hinten · Kapuze', 'Hinten Kapuze'], 'H-SL': ['Hinten · Schulter links', 'Hinten Schulter li.'], 'H-SR': ['Hinten · Schulter rechts', 'Hinten Schulter re.'], 'H-RO': ['Hinten · Rücken oben', 'Hinten Rücken oben'], 'H-GU': ['Hinten · Gürtel / Schlaufen', 'Hinten Gürtel'], 'H-NL': ['Hinten · Seite links', 'Hinten Seite li.'], 'H-RT': ['Hinten · Große Rückentasche', 'Hinten Rückentasche'], 'H-NR': ['Hinten · Seite rechts', 'Hinten Seite re.'], 'H-SA': ['Hinten · Saum / Druckknöpfe', 'Hinten Saum'], 'H-AL': ['Hinten · Ärmel links', 'Hinten Ärmel li.'], 'H-AR': ['Hinten · Ärmel rechts', 'Hinten Ärmel re.'], 'H-CL': ['Hinten · Bündchen links', 'Hinten Bündchen li.'], 'H-CR': ['Hinten · Bündchen rechts', 'Hinten Bündchen re.'], 'H-PL': ['Hinten · Klett-Patch Ärmel links', 'Hinten Klett-Patch li.'], 'I-KR': ['Innen · Nacken / Etikett', 'Innen Etikett'], 'I-FR': ['Innen · Futter rechts', 'Innen Futter re.'], 'I-FL': ['Innen · Futter links', 'Innen Futter li.'], 'I-MR': ['Innen · Magnetfach oben rechts', 'Innen Magnetfach re.'], 'I-ML': ['Innen · Magnetfach oben links', 'Innen Magnetfach li.'], 'I-MU': ['Innen · Magnetfach unten rechts', 'Innen Magnetfach unten'], 'I-AR': ['Innen · Ärmelfutter rechts', 'Innen Ärmelfutter re.'], 'I-AL': ['Innen · Ärmelfutter links', 'Innen Ärmelfutter li.']}, 'mfjh': {'V-KA': ['Vorne · Kapuze', 'Vorne Kapuze'], 'V-SR': ['Vorne · Schulter rechts / RV-Tasche', 'Vorne Schulter re.'], 'V-SL': ['Vorne · Schulter links / RV-Tasche', 'Vorne Schulter li.'], 'V-BR': ['Vorne · Brusttasche rechts', 'Vorne Brusttasche re.'], 'V-BL': ['Vorne · Brusttasche links / IQ-Logo', 'Vorne Brusttasche li.'], 'V-MR': ['Vorne · Bauch / Seite rechts', 'Vorne Seite re.'], 'V-ML': ['Vorne · Bauch / Seite links', 'Vorne Seite li.'], 'V-TR': ['Vorne · Pattentasche unten rechts', 'Vorne Pattentasche re.'], 'V-TL': ['Vorne · Pattentasche unten links', 'Vorne Pattentasche li.'], 'V-SA': ['Vorne · Saum unten', 'Vorne Saum'], 'V-RV': ['Vorne · Front-Reißverschluss / Leiste / Druckknöpfe', 'Vorne Front-RV/Leiste'], 'V-AR': ['Vorne · Ärmel rechts', 'Vorne Ärmel re.'], 'V-AL': ['Vorne · Ärmel links', 'Vorne Ärmel li.'], 'V-CR': ['Vorne · Bündchen rechts', 'Vorne Bündchen re.'], 'V-CL': ['Vorne · Bündchen links', 'Vorne Bündchen li.'], 'V-PL': ['Vorne · Klett-Patch Ärmel links', 'Vorne Klett-Patch li.'], 'H-KA': ['Hinten · Kapuze', 'Hinten Kapuze'], 'H-SL': ['Hinten · Schulter links', 'Hinten Schulter li.'], 'H-SR': ['Hinten · Schulter rechts', 'Hinten Schulter re.'], 'H-RO': ['Hinten · Rücken oben', 'Hinten Rücken oben'], 'H-NL': ['Hinten · Seite links', 'Hinten Seite li.'], 'H-RT': ['Hinten · Große Rückentasche', 'Hinten Rückentasche'], 'H-NR': ['Hinten · Seite rechts', 'Hinten Seite re.'], 'H-SA': ['Hinten · Saum / Druckknöpfe', 'Hinten Saum'], 'H-AL': ['Hinten · Ärmel links', 'Hinten Ärmel li.'], 'H-AR': ['Hinten · Ärmel rechts', 'Hinten Ärmel re.'], 'H-CL': ['Hinten · Bündchen links', 'Hinten Bündchen li.'], 'H-CR': ['Hinten · Bündchen rechts', 'Hinten Bündchen re.'], 'H-PL': ['Hinten · Klett-Patch Ärmel links', 'Hinten Klett-Patch li.'], 'I-KR': ['Innen · Nacken / Etikett', 'Innen Etikett'], 'I-FR': ['Innen · Futter rechts', 'Innen Futter re.'], 'I-FL': ['Innen · Futter links', 'Innen Futter li.'], 'I-IR': ['Innen · Innentasche rechts', 'Innen Innentasche re.'], 'I-IL': ['Innen · Innentasche links', 'Innen Innentasche li.'], 'I-AR': ['Innen · Ärmelfutter rechts', 'Innen Ärmelfutter re.'], 'I-AL': ['Innen · Ärmelfutter links', 'Innen Ärmelfutter li.']}, 'gen': {'V-KR': ['Vorne · Kragen / Kapuze', 'Vorne Kragen'], 'V-SR': ['Vorne · Schulter rechts', 'Vorne Schulter re.'], 'V-SL': ['Vorne · Schulter links', 'Vorne Schulter li.'], 'V-BR': ['Vorne · Brust rechts', 'Vorne Brust re.'], 'V-BL': ['Vorne · Brust links', 'Vorne Brust li.'], 'V-TR': ['Vorne · Tasche / Seite rechts', 'Vorne Tasche re.'], 'V-TL': ['Vorne · Tasche / Seite links', 'Vorne Tasche li.'], 'V-SA': ['Vorne · Saum / Bund', 'Vorne Saum'], 'V-RV': ['Vorne · Reißverschluss / Leiste', 'Vorne RV/Leiste'], 'V-AR': ['Vorne · Ärmel rechts', 'Vorne Ärmel re.'], 'V-AL': ['Vorne · Ärmel links', 'Vorne Ärmel li.'], 'V-CR': ['Vorne · Bündchen rechts', 'Vorne Bündchen re.'], 'V-CL': ['Vorne · Bündchen links', 'Vorne Bündchen li.'], 'H-KR': ['Hinten · Kragen / Kapuze', 'Hinten Kragen'], 'H-SL': ['Hinten · Schulter links', 'Hinten Schulter li.'], 'H-SR': ['Hinten · Schulter rechts', 'Hinten Schulter re.'], 'H-RO': ['Hinten · Rücken oben', 'Hinten Rücken oben'], 'H-RM': ['Hinten · Rücken unten', 'Hinten Rücken unten'], 'H-SA': ['Hinten · Saum / Bund', 'Hinten Saum'], 'H-AL': ['Hinten · Ärmel links', 'Hinten Ärmel li.'], 'H-AR': ['Hinten · Ärmel rechts', 'Hinten Ärmel re.'], 'H-CL': ['Hinten · Bündchen links', 'Hinten Bündchen li.'], 'H-CR': ['Hinten · Bündchen rechts', 'Hinten Bündchen re.'], 'I-KR': ['Innen · Nacken / Etikett', 'Innen Etikett'], 'I-FR': ['Innen · Futter rechts', 'Innen Futter re.'], 'I-FL': ['Innen · Futter links', 'Innen Futter li.'], 'I-IR': ['Innen · Innentasche rechts', 'Innen Innentasche re.'], 'I-IL': ['Innen · Innentasche links', 'Innen Innentasche li.'], 'I-AR': ['Innen · Ärmelfutter rechts', 'Innen Ärmelfutter re.'], 'I-AL': ['Innen · Ärmelfutter links', 'Innen Ärmelfutter li.']}}
LOC_LABEL = {'V-KA': ['Vorne · Kapuze', 'Vorne Kapuze'], 'V-SR': ['Vorne · Schulter rechts', 'Vorne Schulter re.'], 'V-SL': ['Vorne · Schulter links', 'Vorne Schulter li.'], 'V-BR': ['Vorne · Brust rechts', 'Vorne Brust re.'], 'V-BL': ['Vorne · Brust links / IQ-Logo', 'Vorne Brust li.'], 'V-TR': ['Vorne · Seitentasche rechts (RV)', 'Vorne Seitentasche re.'], 'V-TL': ['Vorne · Seitentasche links (RV)', 'Vorne Seitentasche li.'], 'V-MD': ['Vorne · MagDock-Clip', 'Vorne MagDock-Clip'], 'V-ZO': ['Vorne · Zip-off (Reißverschluss Unterteil)', 'Vorne Zip-off'], 'V-LR': ['Vorne · Unterteil rechts', 'Vorne Unterteil re.'], 'V-LL': ['Vorne · Unterteil links', 'Vorne Unterteil li.'], 'V-SA': ['Vorne · Saum unten', 'Vorne Saum'], 'V-RV': ['Vorne · Front-Reißverschluss / Leiste / Druckknöpfe', 'Vorne Front-RV/Leiste'], 'V-AR': ['Vorne · Ärmel rechts', 'Vorne Ärmel re.'], 'V-AL': ['Vorne · Ärmel links', 'Vorne Ärmel li.'], 'V-CR': ['Vorne · Bündchen rechts', 'Vorne Bündchen re.'], 'V-CL': ['Vorne · Bündchen links', 'Vorne Bündchen li.'], 'V-PL': ['Vorne · Patch Ärmel links', 'Vorne Patch li.'], 'H-KA': ['Hinten · Kapuze', 'Hinten Kapuze'], 'H-SL': ['Hinten · Schulter links', 'Hinten Schulter li.'], 'H-SR': ['Hinten · Schulter rechts', 'Hinten Schulter re.'], 'H-RO': ['Hinten · Rücken oben', 'Hinten Rücken oben'], 'H-RM': ['Hinten · Rücken Mitte', 'Hinten Rücken Mitte'], 'H-ZO': ['Hinten · Zip-off (Reißverschluss Unterteil)', 'Hinten Zip-off'], 'H-LL': ['Hinten · Unterteil links', 'Hinten Unterteil li.'], 'H-LR': ['Hinten · Unterteil rechts', 'Hinten Unterteil re.'], 'H-SA': ['Hinten · Saum unten', 'Hinten Saum'], 'H-AL': ['Hinten · Ärmel links', 'Hinten Ärmel li.'], 'H-AR': ['Hinten · Ärmel rechts', 'Hinten Ärmel re.'], 'H-CL': ['Hinten · Bündchen links', 'Hinten Bündchen li.'], 'H-CR': ['Hinten · Bündchen rechts', 'Hinten Bündchen re.'], 'H-PL': ['Hinten · Patch Ärmel links', 'Hinten Patch li.'], 'I-KR': ['Innen · Nacken / Etikett', 'Innen Etikett'], 'I-FR': ['Innen · Futter rechts', 'Innen Futter re.'], 'I-FL': ['Innen · Futter links', 'Innen Futter li.'], 'I-IL': ['Innen · Innentasche links', 'Innen Innentasche li.'], 'I-ZO': ['Innen · Zip-off innen', 'Innen Zip-off innen'], 'I-UF': ['Innen · Futter Unterteil', 'Innen Futter Unterteil'], 'I-AR': ['Innen · Ärmelfutter rechts', 'Innen Ärmelfutter re.'], 'I-AL': ['Innen · Ärmelfutter links', 'Innen Ärmelfutter li.'], 'V-GU': ['Vorne · Gürtel / Schnalle', 'Vorne Gürtel'], 'V-AZ': ['Vorne · Ärmeltasche rechts (RV)', 'Vorne Ärmeltasche re.'], 'H-GU': ['Hinten · Gürtel / Schlaufen', 'Hinten Gürtel'], 'H-NL': ['Hinten · Seite links', 'Hinten Seite li.'], 'H-RT': ['Hinten · Große Rückentasche', 'Hinten Rückentasche'], 'H-NR': ['Hinten · Seite rechts', 'Hinten Seite re.'], 'I-MR': ['Innen · Magnetfach oben rechts', 'Innen Magnetfach re.'], 'I-ML': ['Innen · Magnetfach oben links', 'Innen Magnetfach li.'], 'I-MU': ['Innen · Magnetfach unten rechts', 'Innen Magnetfach unten'], 'V-MR': ['Vorne · Bauch / Seite rechts', 'Vorne Seite re.'], 'V-ML': ['Vorne · Bauch / Seite links', 'Vorne Seite li.'], 'I-IR': ['Innen · Innentasche rechts', 'Innen Innentasche re.'], 'V-KR': ['Vorne · Kragen / Kapuze', 'Vorne Kragen'], 'H-KR': ['Hinten · Kragen / Kapuze', 'Hinten Kragen'], 'X-ALL': ['Ganze Jacke / mehrere Stellen', 'ganze Jacke']}
LOC_SIDE = {'V': ['R', 'L'], 'H': ['L', 'R'], 'I': ['R', 'L']}
LOC_OLD = {'c': 'wmd', 'j': 'gen'}
def clean_reason(n):
    n = reason_spelling(str(n or '').strip())
    for pre in ['Hinweis: ', 'Note: ', 'Hinweis:', 'Note:']:
        if n.startswith(pre):
            n = n[len(pre):].strip()
    return n


def reason_hidden(n):
    t = str(n or '').strip().lower()
    return (not t) or t in HIDE_TAGS or t.startswith('lorem ipsum')


PIN_TAGS = ['Reißverschluss defekt']
HIDE_TAGS = ['andre reason', 'andere reason', 'andre grund', 'andere', 'anderer grund', 'other reason', 'andre']


def garm_of(tmpl):
    if tmpl and cdraw(tmpl.id):
        return 'T' + str(tmpl.id)
    # 1) article number of the template or its first variant (most reliable), 2) product name (German or English)
    if not tmpl:
        return 'gen'
    codes = (tmpl.default_code or '')
    for v in tmpl.product_variant_ids[:3]:
        codes += ' ' + (v.default_code or '')
    c = codes.upper()
    if '-WMD' in c:
        return 'wmd'
    if '-WPU' in c:
        return 'wpu'
    if 'MJD4' in c:
        return 'mfjd'
    if 'MFJ4' in c:
        return 'mfjh'
    n = (tmpl.name or '').lower()
    if 'multifunktion' in n or 'multifunction' in n or 'mfj' in n:
        if 'damen' in n or 'women' in n or 'woman' in n or 'ladies' in n:
            return 'mfjd'
        return 'mfjh'
    if 'wintermantel' in n or 'zip-off' in n or 'zip off' in n or (('coat' in n or 'mantel' in n) and ('women' in n or 'damen' in n)):
        return 'wmd'
    if 'parka' in n:
        return 'wpu'
    return 'gen'


def loc_label(code, g=''):
    cl = custom_label(code, g)
    if cl:
        return dict(LOC_VIEWS).get(code[:1], '') + ' · ' + cl
    pl = LOC_PLAB.get(g or '', {})
    if code in pl:
        return pl[code][0]
    return LOC_LABEL[code][0] if code in LOC_LABEL else code


def loc_short(code, g=''):
    cl = custom_label(code, g)
    if cl:
        return dict(LOC_VIEWS).get(code[:1], '') + ' ' + cl
    pl = LOC_PLAB.get(g or '', {})
    if code in pl:
        return pl[code][1]
    return LOC_LABEL[code][1] if code in LOC_LABEL else code


def loc_clean(s):
    return str(s or '').replace('|', '/').replace('=', '-').replace(chr(9), ' ').replace('<', '').replace('>', '').replace('&', '+').replace('"', '').strip()


def locs_of(al):
    # -> [product key, [[reason, [codes]], ...]]; empty list for older records without location.
    d = str(al.description or '') if al and 'description' in AF else ''
    if LOCMARK not in d:
        return ['', []]
    s = d.split(LOCMARK, 1)[1].split('</p>', 1)[0]
    g = s.split(']', 1)[0].strip() if ']' in s else 'gen'
    g = LOC_OLD.get(g, g)
    if g not in LOC_PROD and not is_custom(g):
        g = 'gen'
    body = s.split(']', 1)[1].strip() if ']' in s else ''
    out = []
    for part in body.split(' | '):
        if '=' not in part:
            continue
        pr = part.rsplit('=', 1)
        zs = []
        for z in pr[1].split(','):
            z = z.strip()
            if loc_code_ok(z) and z not in zs:
                zs.append(z)
        if pr[0].strip():
            out.append([pr[0].strip().replace('&amp;', '+'), zs])
    return [g, out]


def loc_codes(al):
    out = []
    for it in locs_of(al)[1]:
        for z in it[1]:
            if z not in out:
                out.append(z)
    return out


def loc_text(al):
    lg = locs_of(al)
    parts = []
    for it in lg[1]:
        names = []
        for z in it[1]:
            names.append(loc_short(z, lg[0]))
        if names:
            parts.append(', '.join(names))
    return '; '.join(parts)


def loc_svg(g, view, marks, counts, inter, cls, tags=None):
    if is_custom(g):
        return cdraw_html(g, view, marks, counts, inter, cls, tags)
    pr = LOC_PROD.get(g) or LOC_PROD['gen']
    geo = pr.get(view, [])
    hh = pr['B'] + 6
    mxn = 1
    if counts:
        for k in counts:
            if counts[k] > mxn:
                mxn = counts[k]
    out = ('<svg class="lsvg v' + view + ' ' + cls + '" viewBox="0 0 240 ' + str(hh) + '" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="' + dict(LOC_VIEWS).get(view, '') + '">'
           + '<path class="lo" d="' + pr['out'] + '"/>' + pr['deco'].get(view, ''))
    nums = ''
    for z in geo:
        code = z[0]
        n = counts.get(code, 0) if counts else 0
        attr = ' class="lz' + (' on' if code in marks else '') + (' hz' if n else '') + '"'
        if inter:
            attr += ' data-z="' + code + '" data-l="' + esc(loc_label(code, g)) + '"'
        if n:
            attr += ' style="fill:rgba(220,38,38,' + ('%.2f' % (0.18 + 0.72 * n / mxn)) + ')"'
        if z[1] == 'r':
            q = [int(x) for x in z[2].split(' ')]
            out += '<rect x="' + str(q[0]) + '" y="' + str(q[1]) + '" width="' + str(q[2]) + '" height="' + str(q[3]) + '"' + attr + '><title>' + esc(loc_label(code, g)) + '</title></rect>'
            cx = q[0] + q[2] / 2.0
            cy = q[1] + q[3] / 2.0
            bb = [q[0], q[1], q[0] + q[2], q[1] + q[3]]
        else:
            out += '<polygon points="' + z[2] + '"' + attr + '><title>' + esc(loc_label(code, g)) + '</title></polygon>'
            xs = [int(p.split(',')[0]) for p in z[2].split(' ')]
            ys = [int(p.split(',')[1]) for p in z[2].split(' ')]
            cx = sum(xs) / float(len(xs))
            cy = sum(ys) / float(len(ys))
            bb = [min(xs), min(ys), max(xs), max(ys)]
        if n:
            nums += '<text class="lc" x="' + ('%.0f' % cx) + '" y="' + ('%.0f' % cy) + '">' + str(n) + '</text>'
        if tags and code in tags:
            rr = 17 + 6 * (len(tags[code]) - 1)
            mp = marker_pos(bb[0], bb[1], bb[2], bb[3], 240, hh, rr)
            nums += ('<circle class="lnc" cx="' + ('%.0f' % mp[0]) + '" cy="' + ('%.0f' % mp[1]) + '" r="' + str(rr) + '"/>'
                     + '<text class="lnt" x="' + ('%.0f' % mp[0]) + '" y="' + ('%.0f' % mp[1]) + '" style="font-size:' + str(int(rr * 1.3)) + 'px">' + tags[code] + '</text>')
    sd = LOC_SIDE.get(view, ['R', 'L'])
    out += nums + '<text class="lsd" x="14" y="22">' + sd[0] + '</text><text class="lsd" x="226" y="22">' + sd[1] + '</text></svg>'
    return out


def loc_draws(g, marks, cls):
    # Small drawings (only the views that contain a marked place) with captions.
    out = ''
    for v in LOC_VIEWS:
        hit = False
        for z in marks:
            if z.startswith(v[0] + '-'):
                hit = True
        if hit:
            out += '<figure class="lfig">' + loc_svg(g or 'gen', v[0], marks, {}, False, cls) + '<figcaption>' + v[1] + '</figcaption></figure>'
    return ('<div class="ldr-row">' + out + '</div>') if out else ''


def zpl_label(al):
    p = al.product_id
    art = p.default_code or p.product_tmpl_id.default_code or '-'
    reason = ', '.join(tags_of(al)) or ((al.title or '') if 'title' in AF else '')
    who = who_of(al)
    return ('^XA^CI28^PW' + zd(400) + '^LL' + zd(240) + '^LH0,0'
            + '^FO' + zd(16) + ',' + zd(12) + '^A0N,' + zd(38) + ',' + zd(38) + '^FD' + zclean(al.name) + '^FS'
            + '^FO' + zd(268) + ',' + zd(10) + '^GB' + zd(116) + ',' + zd(40) + ',' + zd(3) + '^FS'
            + '^FO' + zd(268) + ',' + zd(19) + '^FB' + zd(116) + ',1,0,C,0^A0N,' + zd(26) + ',' + zd(26) + '^FDDEFEKT^FS'
            + '^FO' + zd(16) + ',' + zd(60) + '^A0N,' + zd(28) + ',' + zd(28) + '^FD' + zfit('Gr. ' + al_size(al) + ' · ' + art, 26) + '^FS'
            + ''.join(['^FO' + zd(16) + ',' + zd(98 + 34 * i) + '^A0N,' + zd(30) + ',' + zd(30) + '^FD' + ln + '^FS' for i, ln in enumerate(zwrap(reason, 21, 2))])
            + '^FO' + zd(16) + ',' + zd(172) + '^A0N,' + zd(20) + ',' + zd(20) + '^FD' + zfit(p.product_tmpl_id.name, 34) + '^FS'
            + '^FO' + zd(16) + ',' + zd(200) + '^A0N,' + zd(20) + ',' + zd(20) + '^FD' + zfit(loc(al.create_date).strftime('%d.%m.%Y') + ((' - ' + who) if who else ''), 34) + '^FS'
            + '^PQ1^XZ')


# Adaptive 62mm continuous DK-roll labels. Both the downloaded PDF and the Brother
# PrintNode job use exactly this layout. The 62mm width NEVER changes. The cut
# length is calculated from ALL defect reasons and the remaining information.
# We use Odoo paper formats to define actual PDF page dimensions; @page alone
# cannot override an ir.actions.report paperformat in wkhtmltopdf.
# Each preset must also appear in the installer loop near the end of the file.
LABEL_LENGTHS = [26, 30, 34, 38, 42, 46, 50, 54, 58, 62, 66, 70, 74, 78, 82, 86,
                 90, 94, 98, 110, 130, 160, 200, 240, 280, 320, 400, 500, 650, 800, 1000]


def label_glyph_width(ch):
    # Conservative Arial-bold estimates, in units of approximately one em.
    # This deliberately leaves space at the right edge on Brother 62mm media.
    if ch in 'MW@%ÄÖÜ':
        return 0.98
    if ch in "iljrtfI.,:;!| '()":
        return 0.39
    if ch in '-_[]/':
        return 0.52
    if ch.isupper():
        return 0.77
    return 0.64


def label_wrap_text(value, max_units):
    # Word wrap; if a *single* long word is too wide, split it rather than lose it.
    # Return only complete, visible text; do not crop or abbreviate.
    words = str(value or '').replace(chr(10), ' ').split()
    lines = []
    line = ''
    width = 0.0
    for word in words:
        ww = sum([label_glyph_width(ch) for ch in word])
        if line and width + label_glyph_width(' ') + ww > max_units:
            lines.append(line)
            line, width = '', 0.0
        if ww <= max_units:
            if line:
                line += ' '
                width += label_glyph_width(' ')
            line += word
            width += ww
        else:
            for ch in word:
                cw = label_glyph_width(ch)
                if line and width + cw > max_units:
                    lines.append(line)
                    line, width = '', 0.0
                line += ch
                width += cw
    if line:
        lines.append(line)
    return lines or ['-']


# ------------------------------------------------------------------ v19.14 own drawings per product (page "Zeichnungen einrichten")
# Stored as attachments on the product template (no new fields):
#   iq_qc_draw_V.jpg / _H.jpg / _I.jpg   picture shown on the TC22 (e.g. a screenshot of the supplier's tech sketch)
#   iq_qc_draw_V_line.png ...            black/white line version for the PDF label
#   iq_qc_draw_V.bits ...                1-bit raster for the Brother RAW label (header IQB1 + width + height)
#   iq_qc_draw.txt                       sizes + boxes: "SIZE|V|w|h" and "Z|V-SR|Schulter rechts|x|y|w|h" (pixels of the picture)
# A product with its own drawing gets the drawing key "T<template id>"; everything else keeps the built-in drawings.
CDRAW = {}


def is_custom(g):
    g = str(g or '')
    return g[:1] == 'T' and g[1:].isdigit()


def cdraw(tid):
    tid = int(tid or 0)
    if tid in CDRAW:
        return CDRAW[tid]
    out = {}
    if tid:
        atts = Att.search([('res_model', '=', 'product.template'), ('res_id', '=', tid), ('name', '=like', 'iq_qc_draw%')], order='id')
        cfg = ''
        files = {}
        for a in atts:
            if a.name == 'iq_qc_draw.txt':
                cfg = (a.raw or b'').decode('utf-8', 'ignore')
            else:
                files[a.name] = a
        rows = [ln.strip().split('|') for ln in cfg.split(chr(10))]
        for pr in rows:
            if len(pr) == 4 and pr[0] == 'SIZE' and pr[1] in ('V', 'H', 'I') and pr[2].isdigit() and pr[3].isdigit():
                img = files.get('iq_qc_draw_' + pr[1] + '.jpg')
                if img and int(pr[2]) > 0 and int(pr[3]) > 0:
                    out[pr[1]] = {'w': int(pr[2]), 'h': int(pr[3]), 'z': [], 'img': img.id,
                                  'line': files.get('iq_qc_draw_' + pr[1] + '_line.png'), 'bits': files.get('iq_qc_draw_' + pr[1] + '.bits')}
        for pr in rows:
            if len(pr) == 7 and pr[0] == 'Z' and pr[1][:1] in out:
                ok = True
                for v in pr[3:]:
                    if not v.lstrip('-').isdigit():
                        ok = False
                if ok:
                    out[pr[1][:1]]['z'].append([pr[1], pr[2], int(pr[3]), int(pr[4]), int(pr[5]), int(pr[6])])
    for v in out:
        out[v]['z'] = sorted(out[v]['z'], key=lambda z: -(z[4] * z[5]))
    CDRAW[tid] = out
    return out


def loc_code_ok(z):
    z = str(z or '')
    return z in LOC_LABEL or (3 <= len(z) <= 8 and z[:1] in ('V', 'H', 'I') and z[1:2] == '-' and z[2:].isalnum())


def loc_views(g):
    if is_custom(g):
        c = cdraw(g[1:])
        out = []
        for v in LOC_VIEWS:
            if v[0] in c:
                out.append(v)
        return out
    return LOC_VIEWS


def custom_label(code, g):
    c = cdraw(g[1:]).get(code[:1]) if is_custom(g) else None
    if c:
        for z in c['z']:
            if z[0] == code:
                return z[1]
    return ''


def draw_ratio(g, view):
    if is_custom(g):
        c = cdraw(g[1:]).get(view)
        return (c['h'] / float(c['w'])) if c else 1.2
    pr = LOC_PROD.get(g) or LOC_PROD['gen']
    return (pr['B'] + 6) / 240.0


def marker_pos(x0, y0, x1, y1, W, H, r):
    # Big area: number in the middle. Small area (cuff, patch, pocket …): number next to it, so the place stays visible.
    cx = (x0 + x1) / 2.0
    cy = (y0 + y1) / 2.0
    if (x1 - x0) * (y1 - y0) >= W * H * 0.02 and (x1 - x0) > 2.4 * r and (y1 - y0) > 2.4 * r:
        return [cx, cy]
    if cx < W / 2.0:
        nx = x0 - r - 3
        if nx < r:
            nx = x1 + r + 3
    else:
        nx = x1 + r + 3
        if nx > W - r:
            nx = x0 - r - 3
    return [min(max(nx, r), W - r), min(max(cy, r), H - r)]


def cdraw_html(g, view, marks, counts, inter, cls, tags=None):
    c = cdraw(g[1:]).get(view)
    if not c:
        return ''
    w = c['w']
    h = c['h']
    mxn = 1
    if counts:
        for k in counts:
            if counts[k] > mxn:
                mxn = counts[k]
    fs = max(14, int(w / 14))
    out = ('<div class="cdr v' + view + ' ' + cls + '"><img src="' + QB + '&amp;dimg=' + str(c['img']) + '" alt="" loading="lazy">'
           + '<svg class="lsvg cdz' + (' int' if inter else '') + '" viewBox="0 0 ' + str(w) + ' ' + str(h) + '" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">')
    nums = ''
    for z in c['z']:
        code = z[0]
        n = counts.get(code, 0) if counts else 0
        attr = ' class="lz' + (' on' if code in marks else '') + (' hz' if n else '') + '"'
        if inter:
            attr += ' data-z="' + code + '" data-l="' + esc(loc_label(code, g)) + '"'
        if n:
            attr += ' style="fill:rgba(220,38,38,' + ('%.2f' % (0.25 + 0.65 * n / mxn)) + ')"'
        out += ('<rect x="' + str(z[2]) + '" y="' + str(z[3]) + '" width="' + str(z[4]) + '" height="' + str(z[5]) + '"' + attr + '><title>' + esc(z[1]) + '</title></rect>')
        if n:
            nums += '<text class="lc" x="' + str(int(z[2] + z[4] / 2)) + '" y="' + str(int(z[3] + z[5] / 2)) + '" style="font-size:' + str(fs) + 'px">' + str(n) + '</text>'
        if tags and code in tags:
            r = int(w * 0.07)
            mp = marker_pos(z[2], z[3], z[2] + z[4], z[3] + z[5], w, h, r)
            nums += ('<circle class="lnc" cx="' + str(int(mp[0])) + '" cy="' + str(int(mp[1])) + '" r="' + str(r) + '"/><text class="lnt" x="' + str(int(mp[0])) + '" y="' + str(int(mp[1]))
                     + '" style="font-size:' + str(int(r * 1.3)) + 'px">' + tags[code] + '</text>')
    sd = LOC_SIDE.get(view, ['R', 'L'])
    out += nums + '</svg><span class="cdside l">' + sd[0] + '</span><span class="cdside r">' + sd[1] + '</span></div>'
    return out


def label_place(code, g):
    # "Vorne · Ärmel links" -> "Vorne: Ärmel links" (full words on the label, no abbreviations)
    return loc_label(code, g).replace(' · ', ': ', 1)


def label_draw_plan(al):
    # -> [drawing key, [[view, marks, {code: 'n,n'}], ...]] for the views that contain a marked place
    lg = locs_of(al)
    nums = {}
    for index, item in enumerate(lg[1]):
        for z in item[1]:
            if z == 'X-ALL':
                continue
            nums[z] = (nums[z] + ',' if z in nums else '') + str(index + 1)
    views = []
    g = lg[0] or 'gen'
    for v in loc_views(g):
        marks = []
        for z in nums:
            if z.startswith(v[0] + '-'):
                marks.append(z)
        if marks:
            views.append([v[0], marks, nums])
    return [g, views]


def label_reason_groups(al):
    # Each defect: "1. Reason" (printed white on black, big) + "» Vorne: Ärmel links" lines; numbers match the drawing.
    lgx = locs_of(al)
    lc = lgx[1]
    if lc:
        groups = []
        for index, item in enumerate(lc):
            lines = label_wrap_text(str(index + 1) + '. ' + reason_spelling(item[0]), 13.5)
            for z in item[1]:
                pl = label_wrap_text('» ' + label_place(z, lgx[0]), 18.0)
                lines = lines + [pl[0]] + ['   ' + x for x in pl[1:]]
            groups.append(lines)
        return groups
    reasons = tags_of(al) or [((al.title or '') if 'title' in AF else 'Defekt')]
    groups = []
    for index, reason in enumerate(reasons):
        reason = reason_spelling(str(reason or '').strip())
        if not reason:
            continue
        prefix = str(index + 1) + '. ' if len(reasons) > 1 else ''
        groups.append(label_wrap_text(prefix + reason, 12.5))
    return groups or [['Defekt']]


def label_reason_lines(al):
    # Kept as a helper for compatibility with any older external references.
    return [line for group in label_reason_groups(al) for line in group]


def label_draw_mm(al):
    # [width of one drawing in mm, height of the drawing block in mm]
    plan = label_draw_plan(al)
    nv = len(plan[1])
    if not nv:
        return [0, 0]
    w = min(40.0, 56.0 / nv - 1.0)
    rmax = 0.5
    for vv in plan[1]:
        rmax = max(rmax, draw_ratio(plan[0], vv[0]))
    if w * rmax > 46.0:
        w = 46.0 / rmax
    return [w, w * rmax + 3.2]


def label_layout(al):
    p = al.product_id
    art = p.default_code or p.product_tmpl_id.default_code or '-'
    sku = label_wrap_text('Gr. ' + al_size(al) + ' - Art.-Nr. ' + art, 19.0)
    reasons = label_reason_groups(al)
    product = label_wrap_text(p.product_tmpl_id.name or '-', 20.0)
    stamp = loc(al.create_date).strftime('%d.%m.%Y')
    who = who_of(al)
    if who:
        stamp += ' - ' + who
    foot = label_wrap_text(stamp, 21.0)
    n_reason = 0
    n_place = 0
    for group in reasons:
        for line in group:
            if line.startswith('» ') or line.startswith('   '):
                n_place += 1
            else:
                n_reason += 1
    dm = label_draw_mm(al)
    # mm allocated: padding, QA header, SKU, reasons (big black bars) + places, drawing, product, date/inspector, safety.
    need = (2.8 + 5.7 + 3.6 * len(sku) + 0.25
            + 5.0 * n_reason + 3.9 * n_place + 0.8 * len(reasons) + 0.35
            + (dm[1] + 1.2 if dm[1] else 0)
            + 3.0 * len(product) + 0.25 + 2.8 * len(foot) + 1.3)
    mm = False
    for candidate in LABEL_LENGTHS:
        if candidate >= need:
            mm = candidate
            break
    # Never silently truncate if someone enters an exceptionally long list.
    if not mm:
        raise ValueError('Etikett zu lang (mehr als 1000 mm); bitte Gründe aufteilen')
    return {'mm': mm, 'sku': sku, 'reasons': reasons, 'product': product, 'foot': foot, 'draw': dm}


LABEL_SVG_CSS = ('.lo{fill:#fff;stroke:#000;stroke-width:2.6;stroke-linejoin:round}.lo2{fill:#fff;stroke:#000;stroke-width:2}'
                 '.ld,.lpt,.lbk{fill:none;stroke:#555;stroke-width:1.3}.ldk,.llt,.lbl{fill:none;stroke:#888;stroke-width:1}'
                 '.lq,.lmg{display:none}.lzp,.lzo{stroke:#000;stroke-width:1.6;stroke-dasharray:3 2}.lmd{fill:#555}.llg{display:none}'
                 '.lz{fill:none;stroke:none}.lz.on{fill:#000;fill-opacity:.5;stroke:#000;stroke-width:3}'
                 '.lsd{font:bold 18px Arial;fill:#000;text-anchor:middle}.lnc{fill:#000;stroke:#fff;stroke-width:2}.lnt{font-family:Arial;font-weight:bold;fill:#fff;text-anchor:middle;dominant-baseline:central}')


def label_svg_img(g, view, marks, nums):
    if is_custom(g):
        c = cdraw(g[1:]).get(view)
        if not c:
            return ''
        w = c['w']
        h = c['h']
        line = c['line']
        r = int(w * 0.07)
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="' + str(w) + '" height="' + str(h) + '" viewBox="0 0 ' + str(w) + ' ' + str(h) + '">'
               + '<style>' + LABEL_SVG_CSS + '</style>'
               + (('<image x="0" y="0" width="' + str(w) + '" height="' + str(h) + '" xlink:href="data:image/png;base64,' + line.datas.decode() + '"/>') if line else '<rect x="1" y="1" width="' + str(w - 2) + '" height="' + str(h - 2) + '" fill="none" stroke="#000"/>'))
        mk = ''
        for z in c['z']:
            if z[0] in marks:
                svg += '<rect class="lz on" x="' + str(z[2]) + '" y="' + str(z[3]) + '" width="' + str(z[4]) + '" height="' + str(z[5]) + '"/>'
                if z[0] in nums:
                    mp = marker_pos(z[2], z[3], z[2] + z[4], z[3] + z[5], w, h, r)
                    mk += ('<circle class="lnc" cx="' + str(int(mp[0])) + '" cy="' + str(int(mp[1])) + '" r="' + str(r) + '"/><text class="lnt" x="' + str(int(mp[0])) + '" y="' + str(int(mp[1]))
                           + '" style="font-size:' + str(int(r * 1.35)) + 'px">' + nums[z[0]] + '</text>')
        sd = LOC_SIDE.get(view, ['R', 'L'])
        fs = int(w * 0.07)
        svg += mk + ('<text x="' + str(fs // 2 + 2) + '" y="' + str(fs + 2) + '" style="font:bold ' + str(fs) + 'px Arial">' + sd[0] + '</text>'
                     + '<text x="' + str(w - fs) + '" y="' + str(fs + 2) + '" style="font:bold ' + str(fs) + 'px Arial">' + sd[1] + '</text></svg>')
    else:
        svg = loc_svg(g, view, marks, {}, False, '', nums)
        svg = svg.replace('role="img"', 'width="240" height="' + str((LOC_PROD.get(g) or LOC_PROD['gen'])['B'] + 6) + '"', 1)
        svg = svg.replace('"><path class="lo"', '"><style>' + LABEL_SVG_CSS + '</style><path class="lo"', 1)
    return 'data:image/svg+xml;base64,' + b64encode(svg.encode('utf-8')).decode()


def label_draw_html(al, dm):
    plan = label_draw_plan(al)
    if not plan[1]:
        return ''
    out = ''
    for vv in plan[1]:
        src = label_svg_img(plan[0], vv[0], vv[1], vv[2])
        if src:
            out += ('<div class="dv" style="width:' + ('%.1f' % dm[0]) + 'mm"><img src="' + src
                    + '" style="width:' + ('%.1f' % dm[0]) + 'mm"><div class="dc">' + dict(LOC_VIEWS).get(vv[0], '') + '</div></div>')
    return '<div class="dr">' + out + '</div>'


def label_length_mm(al):
    return label_layout(al)['mm']


def pdf_label_html(al):
    layout = label_layout(al)
    mm = layout['mm']
    # Every row is explicitly calculated before rendering, so multiple
    # selected reasons cannot run below the printable area.
    reason_html = ''
    for group in layout['reasons']:
        reason_html += '<div class="reason-group">'
        for line in group:
            reason_html += ('<div class="rp">' if (line.startswith('» ') or line.startswith('   ')) else '<div class="rh">') + esc(line.strip() if line.startswith('   ') else line).replace('   ', '') + '</div>'
        reason_html += '</div>'
    return ('<!DOCTYPE html><html><head><meta charset="utf-8"><style>'
            '@page{size:62mm ' + str(mm) + 'mm;margin:0}'
            'html,body{margin:0;padding:0;width:62mm;height:' + str(mm) + 'mm;'
            'font-family:Arial,Helvetica,sans-serif;color:#000}'
            '.lb{box-sizing:border-box;width:62mm;height:' + str(mm) + 'mm;'
            'padding:1.4mm 2.4mm;page-break-inside:avoid}'
            '.h{height:5.7mm;line-height:5.7mm;white-space:nowrap}'
            '.h span{display:inline-block;vertical-align:middle}'
            '.n{font-weight:bold;font-size:13pt;white-space:nowrap}'
            '.x{margin-left:3mm;line-height:normal}.x b{border:1.2pt solid #000;padding:0 1.1mm;font-size:8pt}'
            '.a{font-weight:bold;font-size:8.0pt;line-height:3.6mm;margin-top:.25mm}'
            '.a div{white-space:nowrap}'
            '.d{font-weight:bold;font-size:9.2pt;line-height:4.0mm;margin-top:.25mm}'
            '.reason-group{margin-top:.8mm}.rh{background:#000;color:#fff;font-size:10.5pt;line-height:4.8mm;padding:0 1.2mm;white-space:nowrap}'
            '.rp{font-size:8.6pt;line-height:3.8mm;padding-left:1mm;white-space:nowrap}'
            '.reason-line{white-space:nowrap}'
            '.p{font-size:7pt;line-height:3.0mm;margin-top:.35mm}'
            '.p div{white-space:nowrap}'
            '.f{font-size:7pt;line-height:2.8mm;margin-top:.25mm}'
            '.f div{white-space:nowrap}'
            '.dr{margin-top:1.2mm;white-space:nowrap}.dv{display:inline-block;vertical-align:top;margin-right:1mm;text-align:center}'
            '.dv img{display:block}.dc{font-size:6.5pt;font-weight:bold;line-height:2.6mm}'
            '</style></head><body><div class="lb"><div class="h"><span class="n">'
            + esc(al.name) + '</span><span class="x"><b>DEFEKT</b></span></div>'
            '<div class="a">' + ''.join(['<div>' + esc(line) + '</div>' for line in layout['sku']]) + '</div>'
            '<div class="d">' + reason_html + '</div>' + label_draw_html(al, layout['draw']) +
            '<div class="p">' + ''.join(['<div>' + esc(line) + '</div>' for line in layout['product']]) + '</div>'
            '<div class="f">' + ''.join(['<div>' + esc(line) + '</div>' for line in layout['foot']]) + '</div>'
            '</div></body></html>')


def render_label_pdf(al):
    try:
        mm = label_length_mm(al)
        rep = env['ir.actions.report'].sudo().search([('report_name', '=', 'iq_qc.label_62x' + str(mm))], limit=1)
        if not rep:
            return [False, 'PDF format 62x' + str(mm) + 'mm fehlt - QC v19.5 Installer erneut ausführen']
        pdf = env['ir.actions.report'].sudo()._run_wkhtmltopdf([pdf_label_html(al)], report_ref=rep)
        if not pdf or not pdf.startswith(b'%PDF'):
            return [False, 'PDF wurde nicht korrekt erzeugt']
        return [pdf, '']
    except Exception as e:
        return [False, 'PDF: ' + str(e).replace('|', '/')[:200]]



# -------- v19.18b hotfix: DK-44205 mono / DK-22251 black-red RAW raster; no Odoo PIL/subprocess needed.
# The data format below matches the validated brother_ql v0.9.4 --red network test.
# 62mm tape: 696 printable dots, centred in a 720-dot-wide two-colour raster.
# Mac PrintNode must deliver RAW bytes unchanged using a RAW CUPS queue.
BR_RAW_NAME = 'Brother_QL_820NWB_RAW'
BR_RAW_DOTS_PER_MM = 300.0 / 25.4
BR_RAW_WHITE_ROW = bytes(90)
# Roll format: DK-44205 = monochrome removable white; DK-22251 = black/red.
# Set Odoo System Parameter iq.qc_brother_roll to switch without reinstalling.
BR_ROLL = (P.get_param('iq.qc_brother_roll') or 'DK-44205').strip().upper()
BR_TWO_COLOR = BR_ROLL == 'DK-22251'


# Brother raster font pixels pre-rendered at build time (no Odoo Python imports).
BR_FONT_HEIGHTS = {'h': 71, 'a': 49, 'd': 55, 'p': 43}
BR_FONT_GLYPHS = {
    'h': {
        32: '18:20:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        33: '23:25:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000000fe000000fe000000fe000000fe000000fe000000fe000000fe00000000000000000000000000000000000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        34: '26:28:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007e0f80007e0f80007e0f80007e0f80007e0f80007e0f80007e0f80007e0f80007e0f80007e0f80007e0f80007e0f80007e0f80007e0f80007e0f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        35: '42:44:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007c07c00000007c07c0000000fc0fc0000000fc0fc0000000f80f80000000f80f80000001f81f80000001f81f80000001f81f00000001f01f000003fffffffe0003fffffffe0003fffffffe0003fffffffe0003fffffffe0003fffffffe000007e07e00000007c07c00000007c07c0000000fc0fc0000000fc0fc0000000f80f80000000f80f80000000f80f800001ffffffff0001ffffffff0001ffffffff0001ffffffff0001ffffffff0001ffffffff000003f03f00000003e03e00000003e03e00000007e07e00000007e07e00000007c07c00000007c07c0000000fc0fc0000000fc0fc0000000fc0f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        36: '35:37:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f000000000f000000000f000000000f000000000f000000000f000000000f00000001fff8000007ffff80001fffff80003fffff80007fffff80007fffff80007fcf0f8000ff0f018000ff0f000000ff0f000000ff0f000000ff0f000000ff8f000000ffff0000007fffe000007ffffc00003fffff00003fffff80000fffffc00007ffffc00000ffffe000000fffe000000f3fe000000f1ff000000f0ff000000f0ff000000f0ff000c00f0fe000f80f1fe000ff8f7fe000ffffffc000ffffffc000ffffff8000ffffff00001ffffc000001ffe00000000f000000000f000000000f000000000f000000000f000000000f000000000f000000000f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        37: '50:52:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003800003e000001ff00007e000007ffc0007c00000fffe000fc00001fffe000f800001fc7f001f800003f83f001f000003f03f803f000003f01f803e000003f01f807e000003f01f807c000003f01f80f8000003f01f81f8000003f01f81f0000003f01f83f0000003f01f83e0000003f83f07e0000001fc7f07c0000001ffff0fc0000000fffe0f800000007ffc1f800000003ff01f01ff000007803f07ff800000007e0fffc00000007c1fffe0000000fc3fcff0000000f83f83f0000001f83f03f0000001f07f03f8000003f07f01f8000003e07e01f8000007e07e01f8000007c07e01f800000fc07e01f800000f807f03f800001f003f03f000003f003f03f000003e003f87f000007e001fffe000007c000fffe00000fc0007ffc00000f80003ff000001f80000fc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        38: '44:46:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003c0000000003fff00000000ffffc0000001ffffc0000003ffffc0000003ffffc0000007ffffc0000007fe07c0000007fc01c0000007f8004000000ff80000000007fc0000000007fc0000000007fe0000000007fe0000000003ff0000000003ff8000000007ffc00000000fffe00ff0001fffe00ff0003ffff00ff0007ffff80ff0007fdffc0fe000ff8ffe0fe000ff07ff1fe001ff03ff1fe001ff01ffbfc001ff01ffffc001ff00ffffc001ff007fff8001ff003fff0001ff001fff0001ff800ffe0000ffc00ffe0000ffe01fff0000fff87fff80007fffffff80003fffffffc0003fffffffe0000fffff7ff00007fffe3ff80001fff81ff800003f8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        39: '15:17:00000000000000000000000000000000000000000000000000000000000000000007e00007e00007e00007e00007e00007e00007e00007e00007e00007e00007e00007e00007e00007e00007e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        40: '23:25:000000000000000000000000000000000000000000000000000000000000000000000000000fe000001fe000001fc000003fc000003f8000007f8000007f000000ff000000ff000001fe000001fe000001fe000003fc000003fc000003fc000003fc000007fc000007f8000007f8000007f8000007f8000007f800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff8000007f8000007f8000007f8000007f8000007fc000003fc000003fc000003fc000003fc000001fe000001fe000001fe000000ff000000ff0000007f0000007f8000003f8000003fc000001fc000001fe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        41: '23:25:0000000000000000000000000000000000000000000000000000000000000000000000000fe000000ff0000007f0000007f8000003f8000003fc000001fc000001fe000001fe000000ff000000ff000000ff0000007f8000007f8000007f8000007f8000007fc000003fc000003fc000003fc000003fc000003fc000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fc000003fc000003fc000003fc000003fc000007fc000007f8000007f8000007f8000007f800000ff000000ff000000ff000001fe000001fe000001fc000003fc000003f8000007f8000007f000000ff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        42: '26:28:00000000000000000000000000000000000000000000000000000000000000000000000000000000001e0000001e0000001e0000001e0000001e0000101e03003c1e07003e1e1f807f9e7f803ffeff000ffffc0003fff80000ffe000007f800001ffe00003fff8000ffffc003fdeff007f9e3f803e1e1f80381e0700101e0100001e0000001e0000001e0000001e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        43: '42:44:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000007fffffff80007fffffff80007fffffff80007fffffff80007fffffff80007fffffff80007fffffff80000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        44: '19:21:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007f8000ff0000ff0000fe0000fe0000fc0001f80001f80001f0000000000000000000000000000000000000000000000000000000000000000000000',
        45: '21:23:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001fffc01fffc01fffc01fffc01fffc01fffc01fffc01fffc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        46: '19:21:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        47: '18:20:0000000000000000000000000000000000000000000000000000000000000000000007c00007c0000fc0000f80000f80001f80001f80001f00001f00003f00003f00003e00007e00007e00007c00007c0000fc0000fc0000f80001f80001f80001f00001f00003f00003f00003e00003e00007e00007c00007c0000fc0000fc0000f80000f80001f80001f00001f00003f00003f00003e00003e00007e00007c00007c0000fc0000fc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        48: '35:37:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e00000000ffe0000003fff8000007fffe00000fffff00001fffff00003fffff80007fffffc0007fe0ffc000ffc07fe000ff803fe000ff803fe001ff803ff001ff001ff001ff001ff001ff001ff001ff001ff001ff001ff003ff001ff803ff001ff803ff001ff803ff001ff803ff001ff803ff001ff803ff001ff801ff001ff001ff001ff001ff001ff001ff001ff001ff001ff001ff803ff000ff803fe000ff803fe000ffc07fe0007fe07fc0007ff1ffc0003fffff80003fffff80001fffff00000ffffe000003fff8000001fff00000003f80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        49: '35:37:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007fe000000fffe000003fffe000003fffe000003fffe000003fffe000003fffe000003fffe00000383fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe000003ffffff0003ffffff0003ffffff0003ffffff0003ffffff0003ffffff0003ffffff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        50: '35:37:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001e0000000fffe000007ffff80000fffffe0000ffffff0000ffffff0000ffffff8000ffffffc000fc03ffc000f001ffc000c000ffc0008000ffc00000007fc00000007fc00000007fc00000007fc0000000ffc0000000ffc0000000ff80000001ff80000003ff00000007fe0000000ffc0000001ff80000003ff80000007fe0000000ffe0000001ff80000003ff00000007fe0000000ffc0000001ff80000003ff00000007fe0000000ffffffe000ffffffe000ffffffe000ffffffe000ffffffe000ffffffe000ffffffe000ffffffe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        51: '35:37:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003c0000001ffff000007ffffc00007ffffe00007fffff00007fffff80007fffff80007fffffc0007003ffc0004000ffc0000000ffc00000007fc00000007fc00000007fc0000000ffc0000000ff80000001ff8000001fff000003fffe000003fff8000003fff8000003fffe000003ffff000003ffff8000000fffc0000001ffc0000000ffe00000007fe00000007fe00000003fe00000003fe00000007fe00000007fe0018000ffe001e001ffc001ff0fffc001ffffffc001ffffff8001ffffff0001fffffe0001fffffc00003fffe0000003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        52: '35:37:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007ff0000000fff0000000fff0000001fff0000003fff0000003fff0000007fff0000007fff000000ffff000001fdff000001fdff000003f9ff000003f1ff000007f1ff00000fe1ff00000fe1ff00001fc1ff00003f81ff00003f81ff00007f01ff00007e01ff0000fe01ff0001fc01ff0001fc01ff0003f801ff0003f001ff0003fffffff803fffffff803fffffff803fffffff803fffffff803fffffff803fffffff803fffffff8000001ff00000001ff00000001ff00000001ff00000001ff00000001ff00000001ff0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        53: '35:37:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007fffff80007fffff80007fffff80007fffff80007fffff80007fffff80007fffff80007fffff80007f800000007f800000007f800000007f800000007f800000007f800000007fffe000007ffffc00007ffffe00007fffff00007fffff80007fffffc0007fffffc0007c03ffe0006000ffe00000007fe00000007fe00000003fe00000003ff00000003ff00000003ff00000003fe00000003fe00080007fe000e000ffe000f801ffe000ff8fffc000ffffffc000ffffff8000ffffff0000fffffe00007ffffc00000ffff0000000ff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        54: '35:37:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001c00000003fff000000ffffc00001ffffc00007ffffc0000fffffc0000fffffc0001fff1fc0003ff801c0003fe00040007fc00000007fc0000000ff80000000ff80000000ff80000000ff0ff00000ff3ffc0001ffffff0001ffffff8001ffffffc001ffffffc001ffffffe001fff07fe001ffe03ff001ffc03ff001ffc01ff001ff801ff001ff801ff000ff801ff000ff801ff000ff801ff000ff801ff0007fc01ff0007fc03ff0007fe03fe0003ff07fe0003fffffc0001fffffc0000fffff800007ffff000003fffc000000fff80000001f80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        55: '35:37:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001ffffffe001ffffffe001ffffffe001ffffffe001ffffffe001ffffffe001ffffffe001ffffffe00000007fc0000000ffc0000000ff80000000ff80000001ff00000001ff00000003ff00000003fe00000003fe00000007fc00000007fc0000000ffc0000000ff80000001ff80000001ff00000001ff00000003ff00000003fe00000007fe00000007fc00000007fc0000000ff80000000ff80000001ff80000001ff00000001ff00000003fe00000003fe00000007fe00000007fc00000007fc0000000ff80000000ff8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        56: '35:37:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f00000003fff800000ffffe00001fffff00003fffff80007fffffc0007fffffc000ffe0ffe000ffc07fe000ff803fe000ff803fe000ff803fe000ff803fe000ff803fe000ff803fe0007fc07fc0007fe0ffc0003fffff80001fffff000007fffc000003fff800000ffffe00003fffff80007fffffc0007fc07fc000ff803fe000ff803fe001ff001ff001ff001ff001ff001ff001ff001ff001ff001ff001ff001ff001ff803ff001ff803fe000ffe0ffe000ffffffe0007fffffc0007fffff80003fffff80000ffffe000003fff80000007fc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        57: '35:37:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c00000001ffc0000007fff000001ffffc00003ffffe00003fffff00007fffff0000ffe1ff8000ff80ff8001ff807fc001ff007fc001ff007fe001ff003fe001ff003fe001ff003fe001ff003fe001ff003ff001ff007ff001ff007ff001ff807ff001ffc0fff000fffffff000fffffff0007ffffff0003ffffff0001ffffff0000fff9fe00003ff1fe00000003fe00000003fe00000003fe00000007fc00000007fc0000000ff80006001ff80007c07ff00007fffff00007ffffe00007ffffc00007ffff800007fffe000003fff80000003fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        58: '20:22:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003fe0003fe0003fe0003fe0003fe0003fe0003fe0003fe0003fe0003fe0003fe0000000000000000000000000000000000000000000000000000000003fe0003fe0003fe0003fe0003fe0003fe0003fe0003fe0003fe0003fe0003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        59: '20:22:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003fe0003fe0003fe0003fe0003fe0003fe0003fe0003fe0003fe0003fe0003fe0000000000000000000000000000000000000000000000000000000003fe0003fe0003fe0003fe0003fe0003fe0003fe0003fe0003fe0007fc0007f80007f80007f0000ff0000fe0000fc0000fc0000f80001f8000000000000000000000000000000000000000000000000000000000000000000000',
        60: '42:44:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000180000000000f80000000003f8000000001ff8000000007ff800000003fff80000000ffff80000007fffc0000001fffe0000000ffff80000003fffc0000001ffff00000007fff800000007ffc000000007ff0000000007f80000000007ff0000000007ffe000000007fff800000001ffff000000003fffc00000000ffff800000001ffff000000007fffc00000000ffff800000003fff8000000007ff8000000001ff80000000003f80000000000f800000000001800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        61: '42:44:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007fffffff80007fffffff80007fffffff80007fffffff80007fffffff80007fffffff80000000000000000000000000000000000000000000000000000000000000000000000000007fffffff80007fffffff80007fffffff80007fffffff80007fffffff80007fffffff80007fffffff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        62: '42:44:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007000000000007c00000000007f80000000007fe0000000007ffc000000007fff000000003fffe00000000ffff800000001ffff000000007fffc00000000ffff800000001fffe000000007fff800000000fff8000000001ff80000000007f8000000003ff800000000fff800000007fff80000003fffe0000000ffff00000007fffc0000001fffe0000000ffff80000007fffc00000007fff000000007ff8000000007fe0000000007f00000000007c000000000060000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        63: '29:31:00000000000000000000000000000000000000000000000000000000000000000000000000000000000f000001fff0000ffffc001ffffe001fffff001fffff801fffff801fffffc01f00ffc01c007fc018007fc000007fc000007fc000007fc00000ffc00000ff800001ff800003ff000007fe00000ffe00001ffc00003ff800003ff000007fe000007fc000007fc000007f8000007f800000000000000000000000000000000000007f8000007f8000007f8000007f8000007f8000007f8000007f8000007f8000007f8000007f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        64: '50:52:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000fff00000000007fffe000000001fffff800000007fffffc0000000ffffffe0000001ff801ff0000003fc0007f8000007f00001fc00000fe00000fe00000fc000007f00001f8000003f00003f0000001f80003e007e000f80007e01ff9f0fc0007c03ffdf07c0007c07ffdf07c000f807ffff03c000f80fe1ff03e000f80fc0ff03e000f01f807f03e000f01f807f03e001f01f803f03e001f01f803f03e001f01f003f03e001f01f003f03e001f01f803f03c001f01f803f07c001f01f803f07c000f01f807f0f8000f80fc07f1f8000f80fe0ff3f8000f80fffffff00007c07fffffe00007c03ffdffc00007c01ff9ff000003e00ff1fe000003f00181c0000001f8000000000001f8000000000000fe0000080000007f00001c0000003f80007e0000003fe001fe0000000fff1ffe00000007fffffc00000003fffff800000000ffffe0000000003fff800000000003f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        65: '39:41:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003ff8000000007ffc000000007ffc000000007ffc00000000fffe00000000fffe00000000fffe00000001ffff00000001ffff00000001ffff00000003feff80000003feff80000003feff80000007fc7fc0000007fc7fc0000007fc7fc000000ff83fe000000ff83fe000000ff83fe000001ff81ff000001ff01ff000001ff01ff000003ff01ff800003fe00ff800003fe00ff800007fe00ffc00007ffffffc00007ffffffc0000fffffffe0000fffffffe0000fffffffe0001ffffffff0001ffffffff0001ffffffff0003ff0001ff8003ff0000ff8003fe0000ff8007fe0000ffc007fe0000ffc007fc00007fc00ffc00007fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        66: '38:40:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007ffff000007fffff00007fffffc0007fffffe0007ffffff0007ffffff0007ffffff8007fc07ff8007fc01ff8007fc01ff8007fc00ff8007fc00ff8007fc00ff8007fc00ff8007fc01ff8007fc03ff0007ffffff0007fffffe0007fffffc0007fffff80007fffffe0007ffffff0007ffffff8007fc03ffc007fc00ffc007fc007fc007fc007fe007fc007fe007fc007fe007fc007fe007fc007fe007fc007fe007fc00ffe007fc03ffc007ffffffc007ffffff8007ffffff8007ffffff0007fffffe0007fffff80007ffffc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        67: '37:39:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f00000001fff8000007ffff00001fffffc0003fffffc0007fffffc000ffffffc001ffffffc003fff01fc007ffc003c007ff0000c00ffe0000400ffe0000000ffc0000001ffc0000001ff80000001ff80000001ff80000001ff00000001ff00000001ff00000001ff00000001ff00000001ff00000001ff00000001ff80000001ff80000001ff80000001ff80000000ffc0000000ffc0000000ffe00004007ff0000c007ff8003c003ffe00fc001ffffffc001ffffffc000ffffffc0007fffffc0001fffffc0000fffff000003fffc0000003fc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        68: '42:44:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007fffc00000007ffffe0000007fffffc000007fffffe000007ffffff800007ffffffc00007ffffffe00007ffffffe00007fc07fff00007fc00fff80007fc007ff80007fc001ffc0007fc001ffc0007fc000ffc0007fc000ffe0007fc0007fe0007fc0007fe0007fc0007fe0007fc0007fe0007fc0007fe0007fc0007fe0007fc0007fe0007fc0007fe0007fc0007fe0007fc0007fe0007fc0007fe0007fc000ffe0007fc000ffc0007fc001ffc0007fc001ffc0007fc003ff80007fc00fff80007fc03fff00007ffffffe00007ffffffe00007ffffffc00007ffffff800007fffffe000007fffffc000007ffffe0000007fffe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        69: '34:36:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fffff80007fffff80007fffff80007fffff80007fffff80007fffff80007fffff80007fffff80007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fffffe0007fffffe0007fffffe0007fffffe0007fffffe0007fffffe0007fffffe0007fffffe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        70: '34:36:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fffff80007fffff80007fffff80007fffff80007fffff80007fffff80007fffff80007fffff80007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        71: '41:43:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000078000000001fffe00000007ffffc000001ffffff000003ffffff000007ffffff00000fffffff00001fffffff00003fff00ff00007ffc001f00007ff800030000ffe000000000ffe000000000ffc000000001ffc000000001ff8000000001ff8000000001ff8000000001ff8000000001ff001fffc001ff001fffc001ff001fffc001ff001fffc001ff001fffc001ff001fffc001ff801fffc001ff80007fc001ff80007fc001ff80007fc000ffc0007fc000ffc0007fc000ffe0007fc0007ff0007fc0007ff8007fc0003ffe00ffc0001fffffffc0001fffffffc0000fffffffc00007ffffffc00001ffffff800000fffffc0000003fffe000000003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        72: '42:44:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fffffffc0007fffffffc0007fffffffc0007fffffffc0007fffffffc0007fffffffc0007fffffffc0007fffffffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc0007fc000ffc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        73: '19:21:00000000000000000000000000000000000000000000000000000000000000000007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        74: '19:21:00000000000000000000000000000000000000000000000000000000000000000007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc000ffc000ffc000ffc001ffc003ff800fff800fff000fff000ffe000ffc000ff8000ff0000f80000000000000000000000000000000000000000000000000000',
        75: '39:41:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007fc001ffc0007fc001ffc0007fc003ff80007fc007ff00007fc00ffe00007fc01ffc00007fc03ff800007fc07ff000007fc0ffe000007fc1ffc000007fc3ff8000007fc7ff0000007fcffe0000007fcffe0000007fdffc0000007ffff80000007ffff00000007fffe00000007fffc00000007fff800000007fffc00000007fffe00000007ffff00000007ffff80000007ffffc0000007fdffe0000007fcffe0000007fcfff0000007fc7ff8000007fc3ffc000007fc1ffe000007fc0fff000007fc07ff800007fc03ffc00007fc01ffe00007fc00fff00007fc007ff80007fc003ff80007fc003ffc0007fc001ffe0007fc000fff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        76: '32:34:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fffffe0007fffffe0007fffffe0007fffffe0007fffffe0007fffffe0007fffffe0007fffffe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        77: '50:52:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007ff80007ffc0007ff80007ffc0007ffc0007ffc0007ffc000fffc0007ffc000fffc0007ffe001fffc0007ffe001fffc0007ffe001fffc0007fff003fffc0007fff003fffc0007fff807fffc0007fff807f7fc0007fff807f7fc0007fdfc0ff7fc0007fdfc0fe7fc0007fdfe0fe7fc0007fcfe1fc7fc0007fcfe1fc7fc0007fcff3fc7fc0007fc7f3f87fc0007fc7f3f87fc0007fc3fff87fc0007fc3fff07fc0007fc3fff07fc0007fc1ffe07fc0007fc1ffe07fc0007fc0ffe07fc0007fc0ffc07fc0007fc0ffc07fc0007fc07f807fc0007fc07f807fc0007fc07f807fc0007fc03f007fc0007fc000007fc0007fc000007fc0007fc000007fc0007fc000007fc0007fc000007fc0007fc000007fc0007fc000007fc0007fc000007fc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        78: '42:44:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007fe0007fc0007ff0007fc0007ff0007fc0007ff8007fc0007ff8007fc0007ffc007fc0007ffc007fc0007ffe007fc0007ffe007fc0007fff007fc0007fff007fc0007fff807fc0007fff807fc0007fffc07fc0007fffc07fc0007fdfe07fc0007fdfe07fc0007fcfe07fc0007fcff07fc0007fc7f07fc0007fc7f87fc0007fc3f87fc0007fc3fc7fc0007fc1fc7fc0007fc1fe7fc0007fc0fe7fc0007fc0ff7fc0007fc07f7fc0007fc07fffc0007fc07fffc0007fc03fffc0007fc03fffc0007fc01fffc0007fc01fffc0007fc00fffc0007fc00fffc0007fc007ffc0007fc007ffc0007fc003ffc0007fc003ffc0007fc001ffc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        79: '43:45:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e0000000003fff00000000ffffe0000003fffff0000007fffffc00000ffffffe00001fffffff00003fffffff00003ffe0fff80007ff803ffc0007ff001ffc000ffe000ffe000ffc0007fe000ffc0007fe001ff80007ff001ff80003ff001ff80003ff001ff80003ff001ff00003ff001ff00003ff001ff00001ff001ff00001ff001ff00001ff001ff00003ff001ff00003ff001ff80003ff001ff80003ff001ff80003ff001ff80003ff001ffc0007fe000ffc0007fe000ffe000ffe0007fe001ffc0007ff003ffc0003ffc07ff80003fffffff80001fffffff00000ffffffe000007fffffc000003fffff8000000ffffe00000003fff8000000007f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        80: '37:39:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007ffff000007fffff00007fffffc0007fffffe0007ffffff0007ffffff8007ffffff8007ffffffc007fc03ffc007fc00ffc007fc00ffe007fc007fe007fc007fe007fc007fe007fc007fe007fc007fe007fc00ffe007fc00ffc007fc03ffc007ffffffc007ffffff8007ffffff8007ffffff0007fffffe0007fffffc0007fffff00007ffff000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        81: '43:45:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e0000000003fff80000000ffffe0000003fffff8000007fffffc00000ffffffe00001fffffff00003fffffff80003ffe0fff80007ff803ffc0007ff001ffc000ffe000ffe000ffc0007fe000ffc0007fe001ff80007ff001ff80003ff001ff80003ff001ff80003ff001ff00003ff001ff00003ff001ff00001ff001ff00001ff001ff00001ff001ff00003ff001ff00003ff001ff80003ff001ff80003ff001ff80003ff001ff80003ff001ffc0007fe000ffc0007fe000ffe000ffe0007fe001ffc0007ff003ffc0003ffc07ff80003fffffff00001fffffff00000ffffffe000007fffffc000003fffff0000000ffffe00000003fffc000000003ffe0000000001ff0000000000ff80000000007fc0000000007fe0000000003fe0000000001ff0000000000ff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        82: '39:41:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007ffff00000007ffffe0000007fffff8000007fffffc000007fffffe000007ffffff000007ffffff000007ffffff800007fc03ff800007fc01ff800007fc01ff800007fc01ff800007fc00ff800007fc00ff800007fc00ff800007fc01ff800007fc01ff000007fc03ff000007fffffe000007fffffc000007fffff8000007ffffe0000007fffff0000007fffff8000007fffffc000007fffffe000007fc0ffe000007fc07ff000007fc03ff000007fc01ff800007fc01ff800007fc00ffc00007fc00ffc00007fc00ffc00007fc007fe00007fc007fe00007fc003ff00007fc003ff00007fc001ff80007fc001ff80007fc001ffc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        83: '36:38:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f00000001fffc000007ffffc0001fffffc0003fffffc0003fffffc0007fffffc0007fffffc000ffe01fc000ff8003c000ff80004000ff00000000ff00000000ff00000000ff80000000ffc0000000fffc000000ffffc000007ffff800007ffffe00003fffff80001fffffc0000fffffe00003ffffe00000fffff000000ffff0000000fff00000003ff00000001ff80000001ff80000001ff80080001ff000e0001ff000f8003ff000ff007ff000fffffff000ffffffe000ffffffe000ffffffc000ffffff80003fffff000007fffc0000007fc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        84: '34:36:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ffffffffc0ffffffffc0ffffffffc0ffffffffc0ffffffffc0ffffffffc0ffffffffc0ffffffffc0000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc0000000ffc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        85: '41:43:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fe003ff00007fe003ff00007fe003ff00003ff007fe00003ffc1ffe00003ffffffc00001ffffffc00000ffffff800000ffffff0000007ffffe0000001ffffc00000007fff000000000ff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        86: '39:41:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ffc00007fe007fc00007fc007fe0000ffc007fe0000ffc003fe0000ff8003fe0000ff8003ff0001ff8001ff0001ff0001ff0001ff0001ff8003ff0000ff8003fe0000ff8003fe0000ffc007fe00007fc007fc00007fc007fc00007fe00ffc00003fe00ff800003fe00ff800003ff01ff800001ff01ff000001ff01ff000001ff83ff000000ff83fe000000ff83fe000000ffc7fe0000007fc7fc0000007fc7fc0000007feffc0000003feff80000003feff80000003ffff80000001ffff00000001ffff00000001ffff00000000fffe00000000fffe00000000fffe000000007ffc000000007ffc000000007ffc000000003ff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        87: '56:58:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003fe001ff0007fc003fe001ff8007fc003fe001ff8007fc003fe001ff800ff8003ff003ff800ff8001ff003ffc00ff8001ff003ffc00ff8001ff003ffc01ff0001ff007ffc01ff0001ff807ffc01ff0000ff807ffe01ff0000ff807efe01ff0000ff807efe03fe0000ff80fe7e03fe00007fc0fe7e03fe00007fc0fe7f03fe00007fc0fc7f03fe00007fc0fc7f07fc00007fc1fc3f07fc00003fe1fc3f07fc00003fe1fc3f87fc00003fe1f83f8ffc00003fe3f83f8ff800003ff3f81f8ff800001ff3f81fcff800001ff3f01fcff800001ff3f01fdff000001ff7f00fdff000000ffff00fdff000000ffff00ffff000000fffe00ffff000000fffe00fffe000000fffe007ffe0000007ffe007ffe0000007ffe007ffe0000007ffc007ffe0000007ffc007ffc0000007ffc003ffc0000003ffc003ffc0000003ffc003ffc0000003ff8003ff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        88: '39:41:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003ff0001ff8003ff0001ff8001ff8003ff0001ff8007fe0000ffc007fe00007fe00ffc00007fe00ff800003ff01ff800001ff03ff000001ff83ff000000ffc7fe000000ffcffc0000007feffc0000003ffff80000003ffff80000001ffff00000001fffe00000000fffe000000007ffc000000007ffc000000007ff8000000007ffc00000000fffe00000000fffe00000001ffff00000003ffff00000003ffff80000007feffc0000007feffc000000ffc7fe000001ff83fe000001ff83ff000003ff01ff800003fe01ff800007fe00ffc0000ffc007fc0000ffc007fe0001ff8003ff0003ff0003ff0003ff0001ff8007fe0000ffc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        89: '36:38:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ffc0003ff8ffe0003ff07fe0007ff07ff0007fe03ff000ffc01ff800ffc01ffc01ff800ffc03ff800ffe03ff0007fe07fe0003ff07fe0003ff0ffc0001ff9ffc0001ffdff80000fffff800007ffff000007fffe000003fffe000003fffc000001fffc000000fff8000000fff00000007ff00000007fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        90: '37:39:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001fffffffc01fffffffc01fffffffc01fffffffc01fffffffc01fffffffc01fffffffc01fffffff80000003ff00000007ff0000000ffe0000001ffc0000001ff80000003ff80000007ff0000000ffe0000000ffc0000001ffc0000003ff80000003ff00000007fe0000000ffe0000001ffc0000001ff80000003ff00000007ff0000000ffe0000000ffc0000001ff80000003ff80000007ff00000007fe0000000ffc0000001fffffffc03fffffffc03fffffffc03fffffffc03fffffffc03fffffffc03fffffffc03fffffffc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        91: '23:25:0000000000000000000000000000000000000000000000000000000000000000000000000ffff0000ffff0000ffff0000ffff0000ffff0000ffff0000ffff0000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ffff0000ffff0000ffff0000ffff0000ffff0000ffff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        92: '18:20:000000000000000000000000000000000000000000000000000000000000000000fc0000fc00007c00007c00007e00007e00003e00003f00003f00001f00001f00001f80001f80000f80000f80000fc00007c00007c00007e00007e00003e00003e00003f00001f00001f00001f80001f80000f80000f80000fc00007c00007c00007e00007e00003e00003e00003f00003f00001f00001f80001f80000f80000f80000fc0000fc00007c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        93: '23:25:0000000000000000000000000000000000000000000000000000000000000000000000001fffe0001fffe0001fffe0001fffe0001fffe0001fffe0001fffe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe000003fe0001fffe0001fffe0001fffe0001fffe0001fffe0001fffe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        94: '42:44:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003f00000000007f8000000000ffc000000001ffe000000003fff000000003fff800000007fffc0000000ffffc0000001ff1fe0000003fc0ff0000007f807f800000ff003fc00000fe000fe00001f80007f00003f00003f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        95: '25:27:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ffffff80ffffff80ffffff80ffffff80ffffff80000000000000000000000000000000000000000000000000',
        96: '25:27:000000000000000000000000000000000000000000000000000000001f8000001fc000000fe0000007f0000003f0000001f8000000fc0000007c0000003e0000001f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        97: '34:36:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001fffe000007ffff800007ffffc00007ffffe00007fffff00007fffff80007e03ff80006000ff800000007fc00000007fc00000007fc000007fffc0000fffffc0003fffffc0007fffffc000ffffffc001ffffffc001ffc07fc001ff007fc003fe007fc003fe007fc003fe007fc003fe00ffc003ff01ffc003ff83ffc001ffffffc001ffffffc000ffff7fc000ffff7fc0007ffe7fc0001ff87fc00007e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        98: '36:38:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff83fc0000ff8fff0000ff9fff8000ffbfffc000ffffffe000ffffffe000fffffff000fff03ff000ffe01ff800ffc01ff800ffc00ff800ffc00ff800ff800ffc00ff8007fc00ff8007fc00ff8007fc00ff8007fc00ff8007fc00ff8007fc00ff800ffc00ffc00ff800ffc00ff800ffe01ff800fff03ff800fff8fff000fffffff000ffffffe000ffbfffc000ff9fffc000ff8fff0000ff87fe00000000f8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        99: '30:32:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000fff00003fffe000ffffe001ffffe003ffffe007ffffe00fffffe00ffe01e01ffc00601ff800001ff000001ff000003ff000003fe000003fe000003fe000003fe000003fe000003ff000003ff000001ff000001ff800001ff800200ffe00e00fff83e007ffffe007ffffe003ffffe001ffffe0007fffe0001fffc00003fc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        100: '36:38:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001ff00000001ff00000001ff00000001ff00000001ff00000001ff00000001ff00000001ff00000001ff00000001ff00000001ff00000001ff00003fc1ff0000fff1ff0001fff9ff0003fffdff0007ffffff0007ffffff000fffffff000ffc0fff001ff807ff001ff803ff001ff003ff001ff001ff003ff001ff003fe001ff003fe001ff003fe001ff003fe001ff003fe001ff003ff001ff003ff001ff001ff003ff001ff003ff001ff807ff001ffc07ff000fff1fff000fffffff0007ffffff0003fffdff0003fff9ff0000fff1ff00007fe1ff00001f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        101: '34:36:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ffe0000007fff800000ffffc00001ffffe00003fffff00007fffff8000ffe1ffc000ffc07fc001ff803fe001ff003fe001ff003fe001fe001fe003fffffff003fffffff003fffffff003fffffff003fffffff003fffffff003fe00000003fe00000001ff00000001ff00000001ff00004000ff8001c000ffe00fc0007fffffc0007fffffc0003fffffc0001fffffc00007ffffc00001fffe0000003fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        102: '22:24:0000000000000000000000000000000000000000000000000000000003fc003ffc00fffc01fffc01fffc03fffc03fffc03fe0007fc0007fc0007fc0007fc007ffffc7ffffc7ffffc7ffffc7ffffc7ffffc7ffffc07fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        103: '36:38:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003fc1ff0000fff1ff0001fff9ff0003fffdff0007ffffff0007ffffff000fffffff000ffc0fff001ff807ff001ff803ff001ff003ff001ff001ff003ff001ff003fe001ff003fe001ff003fe001ff003fe001ff003ff001ff003ff001ff001ff003ff001ff003ff001ff803ff001ffc07ff000ffe1fff000fffffff0007ffffff0007fffdff0003fffdff0001fff9ff00007fe1ff00001f81ff00000001ff00000003fe00000003fe00020007fe0003800ffc0003f8fffc0003fffff80003fffff00003ffffe00003ffffc00003ffff0000003ff8000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        104: '36:38:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff83fe0000ff8fff0000ff9fff8000ffbfffc000ffffffc000ffffffe000ffffffe000fff87fe000ffe03ff000ffe01ff000ffc01ff000ffc01ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        105: '17:19:0000000000000000000000000000000000000000000000000000000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000000000000000000000000000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        106: '17:19:0000000000000000000000000000000000000000000000000000000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000000000000000000000000000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8001ff0007ff000fff000ffe000ffe000ffc000ff8000fe0000000000000000000000000000000000000000000000',
        107: '34:36:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff801ff800ff803ff000ff807fe000ff80ffc000ff81ff8000ff81ff8000ff83ff0000ff87fe0000ff8ffc0000ff9ff80000ffbff00000ffffe00000ffffc00000ffff800000ffff000000ffff800000ffffc00000ffffe00000fffff00000ffbff00000ff9ff80000ff8ffc0000ff87fe0000ff87ff0000ff83ff8000ff81ffc000ff80ffe000ff807fe000ff803ff000ff801ff800ff801ffc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        108: '17:19:0000000000000000000000000000000000000000000000000000000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        109: '52:54:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ff83f801fe0000ff8ffe07ff8000ff9fff0fffc000ffbfff9fffc000ffffffbfffe000ffffffffffe000fffffffffff000fff0fffc3ff000ffe07ff81ff000ffc07ff01ff000ffc03ff00ff000ffc03fe00ff800ff803fe00ff800ff803fe00ff800ff803fe00ff800ff803fe00ff800ff803fe00ff800ff803fe00ff800ff803fe00ff800ff803fe00ff800ff803fe00ff800ff803fe00ff800ff803fe00ff800ff803fe00ff800ff803fe00ff800ff803fe00ff800ff803fe00ff800ff803fe00ff800ff803fe00ff800ff803fe00ff800ff803fe00ff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        110: '36:38:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ff83fe0000ff8fff0000ff9fff8000ffbfffc000ffffffc000ffffffe000ffffffe000fff87fe000ffe03ff000ffe01ff000ffc01ff000ffc01ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        111: '35:37:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ffe0000007fff800000ffffe00001fffff00003fffff80007fffffc000ffffffc000ffc0ffe001ff807fe001ff803ff001ff003ff001ff001ff003ff001ff003fe001ff003fe001ff003fe001ff003fe001ff003fe001ff003ff001ff003ff001ff001ff001ff001ff003ff001ff803fe000ffc07fe000ffe1ffe0007fffffc0007fffff80003fffff00001ffffe000007fffc000003fff00000003f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        112: '36:38:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ff83fc0000ff8fff0000ff9fff8000ffbfffc000ffffffe000ffffffe000fffffff000fff03ff000ffe01ff800ffc01ff800ffc00ff800ffc00ff800ff800ffc00ff8007fc00ff8007fc00ff8007fc00ff8007fc00ff8007fc00ff8007fc00ff800ffc00ffc00ff800ffc00ff800ffe01ff800fff03ff800fff8fff000fffffff000ffffffe000ffbfffc000ff9fffc000ff8fff0000ff87fe0000ff80f80000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        113: '36:38:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003fc1ff0000fff1ff0001fff9ff0003fffdff0007ffffff0007ffffff000fffffff000ffc0fff001ff807ff001ff803ff001ff003ff001ff001ff003ff001ff003fe001ff003fe001ff003fe001ff003fe001ff003fe001ff003ff001ff003ff001ff001ff003ff001ff003ff001ff807ff001ffc07ff000fff1fff000fffffff0007ffffff0003fffdff0003fff9ff0000fff1ff00007fe1ff00001f81ff00000001ff00000001ff00000001ff00000001ff00000001ff00000001ff00000001ff00000001ff00000001ff00000001ff00000001ff0000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        114: '25:27:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ff83f800ff8ff800ff9ff800ffbff800ffbff800fffff800fffff800fffff800fff80800ffe00000ffc00000ffc00000ffc00000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        115: '30:32:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007ffc0003ffffc007ffffc00fffffc00fffffc01fffffc01ff81fc01fe001c01fc000401fc000001fe000001ff800001fffe0001ffffe000fffff800fffffc003ffffc001ffffe0001fffe00000ffe000001ff000001ff000001ff018001ff01f003fe01fffffe01fffffe01fffffc01fffff801fffff0007fffc00003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        116: '24:26:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007fc000007fc000007fc000007fc000007fc000007fc000007fc000007fc00007ffffe007ffffe007ffffe007ffffe007ffffe007ffffe007ffffe0007fc000007fc000007fc000007fc000007fc000007fc000007fc000007fc000007fc000007fc000007fc000007fc000007fc000007fc000007fc000007fc000007fe000007fffc0003fffc0003fffc0003fffc0001fffc0000fffc00003ffc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        117: '36:38:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff803ff000ff803ff000ff803ff000ffc07ff000ffc0fff0007ffffff0007ffffff0007ffffff0003fffdff0003fff9ff0001fff1ff00007fe1ff00001f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        118: '33:35:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007fc001ff007fc001ff003fc001fe003fe003fe003fe003fe001fe003fc001ff007fc001ff007fc000ff007f8000ff80ff8000ff80ff80007f80ff00007fc1ff00007fc1fe00003fc1fe00003fc3fe00003fe3fc00001fe3fc00001fe7fc00000ff7f800000ff7f800000ffff8000007fff0000007fff0000007fff0000003ffe0000003ffe0000003ffe0000001ffc0000001ffc0000001ff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        119: '47:49:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003fc00fe00ff8003fe01fe00ff8003fe01fe00ff0001fe01ff00ff0001fe01ff01ff0001fe03ff01ff0001ff03ff01fe0001ff03ff81fe0000ff03ff83fe0000ff03ff83fe0000ff87ff83fc0000ff87ef83fc00007f87efc3fc00007f87efc7fc00007f8fcfc7f800007fcfc7c7f800003fcfc7e7f800003fcfc7eff800003fcf87eff800003fff87eff000001fff83eff000001fff83fff000001fff83fff000001fff03ffe000001fff01ffe000000fff01ffe000000fff01ffe000000ffe01ffc000000ffe01ffc0000007fe00ffc0000007fe00ffc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        120: '32:34:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007fe003fe003fe007fe001ff007fc001ff80ff8000ff81ff80007fc1ff00007fc3fe00003fe7fe00001ff7fc00001ffff800000ffff8000007fff0000007ffe0000003ffe0000001ffc0000001ff80000003ffc0000003ffe0000007ffe000000ffff000000ffff800001ffff800003fe7fc00003fe3fe00007fc3fe0000ffc1ff0000ff80ff8001ff00ff8003ff007fc003fe007fe007fc003fe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        121: '33:35:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007f8001ff007fc001ff007fc003fe003fe003fe003fe003fe001fe003fc001ff007fc001ff007f8000ff007f8000ff80ff80007f80ff00007f80ff00007fc1ff00003fc1fe00003fc1fe00003fe1fe00001fe3fc00001ff3fc00000ff3fc00000ff7f800000ffff8000007fff8000007fff0000003fff0000003fff0000003ffe0000001ffe0000001ffe0000001ffc0000000ffc0000000ffc00000007f800000007f800000007f00000000ff00000001ff00000003fe0000007ffe0000007ffc0000007ffc0000007ff80000007ff00000007fc0000000000000000000000000000000000000000000000000000000000000000000000000000',
        122: '29:31:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001fffffe01fffffe01fffffe01fffffe01fffffe01fffffe01fffffe000007fe00000ffc00001ff800003ff000007fe00000ffc00001ffc00001ff800003ff000007fe00000ffc00001ff800003ff000007fe000007fe00000ffc00001ff800003fffffe03fffffe03fffffe03fffffe03fffffe03fffffe03fffffe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        123: '36:38:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001fc0000003ffc0000007ffc000000fffc000001fffc000001fffc000003fffc000003ff00000003fe00000003fe00000003fc00000003fc00000003fc00000003fc00000003fc00000003fc00000003fc00000003fc00000003fc00000003fc00000007fc00000007fc0000000ffc000003fff8000003fff8000003ffe0000003ffc0000003fff0000003fff8000000fff80000000ffc00000007fc00000007fc00000003fc00000003fc00000003fc00000003fc00000003fc00000003fc00000003fc00000003fc00000003fc00000003fe00000003fe00000003fe00000003ff00000001fffc000001fffc000001fffc000000fffc0000007ffc0000001ffc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        124: '18:20:00000000000000000000000000000000000000000000000000000003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f000000000000000000000000000000000000000',
        125: '36:38:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003f800000003ff80000003ffe0000003fff0000003fff8000003fff8000003fff80000000ffc00000007fc00000007fc00000007fc00000007fc00000003fc00000003fc00000003fc00000003fc00000003fc00000003fc00000003fc00000003fc00000003fe00000003fe00000003ff00000001fffc000001fffc0000007ffc0000003ffc000000fffc000001fffc000003ffe0000003ff00000003fe00000003fc00000003fc00000003fc00000003fc00000003fc00000003fc00000003fc00000003fc00000003fc00000007fc00000007fc00000007fc00000007fc0000001ffc000003fff8000003fff8000003fff0000003fff0000003ffc0000003ff8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        126: '42:44:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000700000800003ff000180000fffc00780001ffff81f80007fffffff80007fffffff80007fffffff80007e03ffff00007800fffc000060001ff0000040000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        160: '18:20:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        161: '23:25:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff00000000000000000000000000000000000000fe000000fe000000fe000000fe000000fe000000fe000000fe000001fe000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff000001ff0000000000000000000000000000000000000000000000000000000000000000000000000000',
        162: '35:37:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000078000000007800000000780000000078000000007800000000780000000078000000007800000003ffc000001ffff800003ffff800007ffff80000fffff80001fffff80003fffff80003fff8780007ff78180007fe78000007fe78000007fc7800000ffc7800000ffc7800000ff87800000ff87800000ff87800000ffc7800000ffc78000007fc78000007fc78000007fe78000007ff78080003fff8180003fff8f80001fffff80000fffff80000fffff800003ffff800001ffff8000007ffe0000000ff00000000780000000078000000007800000000780000000078000000007800000000780000000078000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        163: '35:37:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f00000001fff8000007fffe00000ffffe00001ffffe00001ffffe00003ffffe00003ffffe00007ff00e00007fe00200007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc000000fffffe0000fffffe0000fffffe0000fffffe0000fffffe0000fffffe0000fffffe000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc000001ffffffe001ffffffe001ffffffe001ffffffe001ffffffe001ffffffe001ffffffe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        164: '32:34:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004000020000e000070001f0000f8003f8001fc003fcff3fc001ffffff8000ffffff00007ffffe00003ffffc00001ffff800001f81fc00003f00fc00003e007c00003e007c00003e007e00003e007e00003e007e00003e007c00003e007c00003f00fc00003f81fc00001ffff800003ffffc00007ffffe0000ffffff0001ffffff8003fcff3fc003f8001fc001f0000f8000e0000700004000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        165: '35:37:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007fe000ffc07fe000ffc03ff001ff803ff001ff801ff803ff000ff803ff000ffc07fe0007fe07fc0007fe0ffc0003ff1ff80003ff1ff80001ffbff00000ffbff00000ffffe000007fffc0003fffffff803fffffff803fffffff803fffffff803fffffff80000ffe0000000ffe00000007fc00000007fc00003fffffff803fffffff803fffffff803fffffff803fffffff803fffffff800007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        166: '18:20:00000000000000000000000000000000000000000000000000000000000000000000000003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00000000000000000000000000000000000000000000003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f00003f000000000000000000000000000000000000000000000000000000000000000',
        167: '25:27:00000000000000000000000000000000000000000000000000000000000000000000000000000000001e000001fff00007fffc000ffffc000ffffc001ffffc001ff07c003fe00c003fc000003fe000001fe000001ff800001ffe00000fff800007ffe00007fff0000ffffc001ffffe003ffffe007f87ff007f01ff007f00ff80fe007f80fe003f80ff003f80ff003f807fc03f807fe07f007ff8ff003ffffe001ffffc000ffff80007fff00001fff800007ffc00001ffc000007fe000003fe000001fe000001fe001c01fe001feffe001ffffc001ffffc001ffff8001ffff00007ff80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        168: '25:27:000000000000000000000000000000000000000000000000000000000000000007e1f00007e1f00007e1f00007e1f00007e1f00007e1f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        169: '50:52:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001e000000000001ffe00000000007fff8000000001ffffe000000003fffff000000007f003f80000000fc000fc0000001f80007e0000001f00001f0000003e01fc0f0000007c0fff8f800000781fff87800000f83fff83c00000f07fff83c00000f0ff8781e00000e0fe0081e00001e1fc0001e00001e1fc0001e00001e1f80000e00001e1f80000e00001e1f80000e00001e1f80000e00001e1f80000e00001e1fc0000e00001e1fc0001e00001e0fe0081e00000f0ff0181e00000f0ffff83c00000f07fff83c00000783fff87c000007c1fff878000003c07ff0f8000003e00001f0000001f00003e0000000fc0007e00000007e001fc00000003fc0ff800000001ffffe000000000ffffc0000000003fff000000000007f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        170: '28:30:00000000000000000000000000000000000000000000000000000000000000000000000000000000000f000001fff00003fffc0003fffe0003fffe000380ff0000003f0000003f0000003f8000ffff8003ffff8007ffff8007fc3f800fe03f800fc03f800fc03f800fc07f800fe0ff800ffbff8007ffdf8007ff9f8003ff1f8000fc00000000000000000000000000000fffff000fffff000fffff000fffff000fffff000fffff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        171: '33:35:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100100000030030000007007000000f00f000001f03f000007f07f00000ff0ff00001fe1fe00003fc3fc00007f8ff00000fe0fe00000fc0fc00000f80f800000fc0fc00000fe0fe00000ff0ff000007f87f800001fe3fc00000ff0ff000007f07f000003f03f000000f01f000000700f00000030030000001001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        172: '42:44:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007fffffff80007fffffff80007fffffff80007fffffff80007fffffff80007fffffff80007fffffff80000000001f80000000001f80000000001f80000000001f80000000001f80000000001f80000000001f80000000001f80000000001f80000000001f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        173: '1:3:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        174: '50:52:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001e000000000001ffe00000000007fff8000000001ffffe000000003fffff000000007f003f80000000fc000fc0000001f80007e0000001f00001f0000003e3ff80f0000007c3ffe0f800000783fff07800000f83fff83c00000f03e1f83c00000f03e0f81e00000e03e0f81e00001e03e1f81e00001e03e1f81e00001e03fff80e00001e03fff00e00001e03ffe00e00001e03ff800e00001e03efc00e00001e03e7e00e00001e03e3e01e00001e03e3f01e00000f03e1f01e00000f03e1f83c00000f03e1f83c00000783e0fc7c000007c3e0fc78000003c3e07cf8000003e00001f0000001f00003e0000000fc0007e00000007e001fc00000003fc0ff800000001ffffe000000000ffffc0000000003fff000000000007f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        175: '25:27:00000000000000000000000000000000000000000000000000000000000000000000000007fff00007fff00007fff00007fff00007fff00007fff0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        176: '25:27:00000000000000000000000000000000000000000000000000000000000000000000000000000000003e000000ff800001ffc00003ffe00007fff00007c1f0000780f0000f8078000f0078000f0078000f8078000780f80007c0f00007e3f00003ffe00001ffe00000ff8000007f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        177: '42:44:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000007fffffff80007fffffff80007fffffff80007fffffff80007fffffff80007fffffff80000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000003f00000000000000000000000000000007fffffff80007fffffff80007fffffff80007fffffff80007fffffff80007fffffff80007fffffff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        178: '22:24:0000000000000000000000000000000000000000000000000000000000000070000fff001fff801fffc01fbfe01c0fe01007e00007e00007e00007e0000fc0001fc0003f80007f0000fe0001fc0003f80007f0000fe0001fffe01fffe01fffe01fffe01fffe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        179: '22:24:00000000000000000000000000000000000000000000000000000000000000f0001fff001fff801fffc01f7fe0100fe00007e00007e0000fc0003fc003ff8003fe0003ff80003fc0000fe00007e00007e00007e02007e0380fe03fffe03fffc03fff800ffc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        180: '25:27:000000000000000000000000000000000000000000000000000000000000fe000001fc000003f8000003f0000007e000000fc000000f8000001f0000003f0000007e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        181: '37:39:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ffc01ff000ffc03ff000ffe07ff000ffffffff00ffffffff00ffffffff00ffffffff00fffff7ff00fffff3ff00ffbfc1ff00ff8f807800ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000000000000000000000000000000000000000000000000000000000000000000000000',
        182: '32:34:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ffff000007ffff00001fffff00003fffff00007ffc1f00007ffc1f0000fffc1f0000fffc1f0000fffc1f0001fffc1f0001fffc1f0001fffc1f0001fffc1f0001fffc1f0001fffc1f0000fffc1f0000fffc1f0000fffc1f00007ffc1f00003ffc1f00001ffc1f00000ffc1f000003fc1f0000003c1f0000003c1f0000003c1f0000003c1f0000003c1f0000003c1f0000003c1f0000003c1f0000003c1f0000003c1f0000003c1f0000003c1f0000003c1f0000003c1f0000003c1f0000003c1f0000003c1f0000003c1f0000003c1f0000003c1f0000003c1f0000003c1f0000003c1f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        183: '19:21:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        184: '25:27:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e0000000f00000007800000078000000380000007c000030fc00003ff800003ff800003ff000001fe00000000000000000000000000000000000000000000000000000000000000000000',
        185: '22:24:00000000000000000000000000000000000000000000000000000000000003fc001ffc001ffc001ffc001e7c00007c00007c00007c00007c00007c00007c00007c00007c00007c00007c00007c00007c00007c001fffe01fffe01fffe01fffe01fffe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        186: '28:30:0000000000000000000000000000000000000000000000000000000000000000000000000000000000070000007ff00001fff80003fffe0007fffe000ff0ff000fe07f801fe03f801fc03f801fc03f801fc03fc01fc03fc01fc03fc01fc03f801fc03f801fe03f800fe07f800ff07f0007ffff0003fffe0001fffc0000fff000001fc0000000000000000000000000000fffff000fffff000fffff000fffff000fffff000fffff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        187: '33:35:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000040080000006004000000700700000078078000007c07c000007e07e000007f87f000003fc3fc00001fe1fe00000ff0ff000007f87f800001f83f800000f80f800001f81f800003f87f80000ff0ff00001fe1fe00003fc3fc00007f87f800007f07e000007c07c00000780780000070070000006006000000400800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        188: '52:54:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f800007f800001f80003ff800001f00003ff800003f00003ff800003e00003cf800007e000000f800007c000000f80000fc000000f80000f8000000f80001f8000000f80003f0000000f80003e0000000f80007e0000000f80007c0000000f8000fc0000000f8000f80000000f8001f80000000f8001f00000000f8003f0000003fffc03e03f8003fffc07e07f8003fffc07c07f8003fffc0f80ff8003fffc1f81ff800000001f01ff800000003f03df800000003e07df800000007e079f800000007c0f1f80000000fc1f1f80000000f81e1f80000001f83c1f80000001f07c1f80000003f07ffff0000007e07ffff0000007c07ffff000000fc07ffff000000f80001f8000001f80001f8000001f00001f8000003f00001f8000003e00001f8000007e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        189: '52:54:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f800007f800001f80003ff800001f00003ff800003f00003ff800003e00003cf800007e000000f800007c000000f80000fc000000f80000f8000000f80001f8000000f80003f0000000f80003e0000000f80007e0000000f80007c0000000f8000fc0000000f8000f80000000f8001f80000000f8001f00000000f8003f01c0003fffc03e3ffc003fffc07e7ffe003fffc07c7fff003fffc0f87eff803fffc1f8703f80000001f0401f80000003f0001f80000003e0001f80000007e0001f80000007c0003f0000000fc0007f0000000f8000fe0000001f8001fc0000001f0003f80000003f0007f00000007e000fe00000007c001fc0000000fc003f80000000f8007fff800001f8007fff800001f0007fff800003f0007fff800003e0007fff800007e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        190: '52:54:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f000000f80001fff00001f80001fff80001f00001fffc0003f00001f7fe0003e0000100fe0007e00000007e0007c00000007e000fc0000000fc000f80000003fc001f8000003ff8003f0000003fe0003e0000003ff8007e00000003fc007c00000000fe00fc000000007e00f8000000007e01f8000000007e01f0000002007e03f000000380fe03e03f8003fffe07e07f8003fffc07c07f8003fff80f80ff8000ffc01f81ff800000001f01ff800000003f03df800000003e07df800000007e079f800000007c0f1f80000000fc1f1f80000000f81e1f80000001f83c1f80000001f07c1f80000003f07ffff0000007e07ffff0000007c07ffff000000fc07ffff000000f80001f8000001f80001f8000001f00001f8000003f00001f8000003e00001f8000007e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        191: '29:31:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff800000ff80000000000000000000000000000000000000ff800000ff800000ff800000ff800001ff000003ff000007fe00000ffe00001ffc00003ff800003ff000007fe00000ffc00000ff800000ff800000ff800001ff000001ff000001ff800c00ff803c00ffe1fc00fffffc00fffffc007ffffc003ffffc001ffffc000ffff00001ff0000000000000000000000000000000000000000000000000000000000000000000',
        192: '39:41:001fc0000000000fe00000000007f00000000003f00000000001f80000000000fc00000000007c0000000000020000000000000000000000000000000000000000000003ff8000000007ffc000000007ffc000000007ffc00000000fffe00000000fffe00000000fffe00000001ffff00000001ffff00000001ffff00000003feff80000003feff80000003feff80000007fc7fc0000007fc7fc0000007fc7fc000000ff83fe000000ff83fe000000ff83fe000001ff81ff000001ff01ff000001ff01ff000003ff01ff800003fe00ff800003fe00ff800007fe00ffc00007ffffffc00007ffffffc0000fffffffe0000fffffffe0000fffffffe0001ffffffff0001ffffffff0001ffffffff0003ff0001ff8003ff0000ff8003fe0000ff8007fe0000ffc007fe0000ffc007fc00007fc00ffc00007fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        193: '39:41:00000fe0000000000fc0000000001f80000000003f00000000003f00000000007e0000000000fc0000000000000000000000000000000000000000000000000000000003ff8000000007ffc000000007ffc000000007ffc00000000fffe00000000fffe00000000fffe00000001ffff00000001ffff00000001ffff00000003feff80000003feff80000003feff80000007fc7fc0000007fc7fc0000007fc7fc000000ff83fe000000ff83fe000000ff83fe000001ff81ff000001ff01ff000001ff01ff000003ff01ff800003fe00ff800003fe00ff800007fe00ffc00007ffffffc00007ffffffc0000fffffffe0000fffffffe0000fffffffe0001ffffffff0001ffffffff0001ffffffff0003ff0001ff8003ff0000ff8003fe0000ff8007fe0000ffc007fe0000ffc007fc00007fc00ffc00007fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        194: '39:41:0001fe0000000001ff0000000003ff8000000007efc00000000fc7c00000000f83e00000001f01f000000000000000000000000000000000000000000000000000000003ff8000000007ffc000000007ffc000000007ffc00000000fffe00000000fffe00000000fffe00000001ffff00000001ffff00000001ffff00000003feff80000003feff80000003feff80000007fc7fc0000007fc7fc0000007fc7fc000000ff83fe000000ff83fe000000ff83fe000001ff81ff000001ff01ff000001ff01ff000003ff01ff800003fe00ff800003fe00ff800007fe00ffc00007ffffffc00007ffffffc0000fffffffe0000fffffffe0000fffffffe0001ffffffff0001ffffffff0001ffffffff0003ff0001ff8003ff0000ff8003fe0000ff8007fe0000ffc007fe0000ffc007fc00007fc00ffc00007fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        195: '39:41:0003807000000007e0f00000000ff8f00000001ffff00000001e7fe00000001e3fe00000001c0fc000000000000000000000000000000000000000000000000000000003ff8000000007ffc000000007ffc000000007ffc00000000fffe00000000fffe00000000fffe00000001ffff00000001ffff00000001ffff00000003feff80000003feff80000003feff80000007fc7fc0000007fc7fc0000007fc7fc000000ff83fe000000ff83fe000000ff83fe000001ff81ff000001ff01ff000001ff01ff000003ff01ff800003fe00ff800003fe00ff800007fe00ffc00007ffffffc00007ffffffc0000fffffffe0000fffffffe0000fffffffe0001ffffffff0001ffffffff0001ffffffff0003ff0001ff8003ff0000ff8003fe0000ff8007fe0000ffc007fe0000ffc007fc00007fc00ffc00007fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        196: '39:41:000f87e00000000f87e00000000f87e00000000f87e00000000f87e00000000f87e00000000f87e000000000000000000000000000000000000000000000000000000003ff8000000007ffc000000007ffc000000007ffc00000000fffe00000000fffe00000000fffe00000001ffff00000001ffff00000001ffff00000003feff80000003feff80000003feff80000007fc7fc0000007fc7fc0000007fc7fc000000ff83fe000000ff83fe000000ff83fe000001ff81ff000001ff01ff000001ff01ff000003ff01ff800003fe00ff800003fe00ff800007fe00ffc00007ffffffc00007ffffffc0000fffffffe0000fffffffe0000fffffffe0001ffffffff0001ffffffff0001ffffffff0003ff0001ff8003ff0000ff8003fe0000ff8007fe0000ffc007fe0000ffc007fc00007fc00ffc00007fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        197: '39:41:00007c0000000001ff0000000003ff8000000003ff8000000007c7c00000000783c00000000781c00000000f01e00000000701c00000000783c00000000783c000000007ffc000000007ffc000000007ffc000000007ffc00000000fffe00000000fffe00000000fffe00000001ffff00000001ffff00000001ffff00000003feff80000003feff80000003feff80000007fc7fc0000007fc7fc0000007fc7fc000000ff83fe000000ff83fe000000ff83fe000001ff81ff000001ff01ff000001ff01ff000003ff01ff800003fe00ff800003fe00ff800007fe00ffc00007ffffffc00007ffffffc0000fffffffe0000fffffffe0000fffffffe0001ffffffff0001ffffffff0001ffffffff0003ff0001ff8003ff0000ff8003fe0000ff8007fe0000ffc007fe0000ffc007fc00007fc00ffc00007fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        198: '55:57:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001ffffffffc0000001ffffffffc0000003ffffffffc0000003ffffffffc0000003ffffffffc0000007ffffffffc0000007ffffffffc0000007fc7fffffc000000ff87fc0000000000ff87fc0000000001ff87fc0000000001ff07fc0000000001ff07fc0000000003ff07fc0000000003fe07fc0000000003fe07fc0000000007fc07fffffc000007fc07fffffc00000ffc07fffffc00000ff807fffffc00000ff807fffffc00001ff807fffffc00001ff007fffffc00001ff007fffffc00003ffffffc000000003ffffffc000000007ffffffc000000007ffffffc000000007ffffffc00000000fffffffc00000000fffffffc00000000ff8007fc00000001ff0007fc00000001ff0007fffffe0003ff0007fffffe0003fe0007fffffe0003fe0007fffffe0007fc0007fffffe0007fc0007fffffe0007fc0007fffffe000ff80007fffffe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        199: '37:39:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f00000001fff8000007ffff00001fffffc0003fffffc0007fffffc000ffffffc001ffffffc003fff01fc007ffc003c007ff0000c00ffe0000400ffe0000000ffc0000001ffc0000001ff80000001ff80000001ff80000001ff00000001ff00000001ff00000001ff00000001ff00000001ff00000001ff00000001ff80000001ff80000001ff80000001ff80000000ffc0000000ffc0000000ffe00004007ff0000c007ff8003c003ffe00fc001ffffffc001ffffffc000ffffffc0007fffffc0001fffffc0000fffff000003fffc0000003fc0000000078000000003c000000003c000000001c000000003e000000187e0000001ffc0000001ffc0000001ff80000000ff000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        200: '34:36:007f000000003f800000001fc00000000fc000000007e000000003f000000001f00000000008000000000000000000000000000000000007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fffff80007fffff80007fffff80007fffff80007fffff80007fffff80007fffff80007fffff80007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fffffe0007fffffe0007fffffe0007fffffe0007fffffe0007fffffe0007fffffe0007fffffe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        201: '34:36:00003f800000003f000000007e00000000fc00000000fc00000001f800000003f00000000000000000000000000000000000000000000007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fffff80007fffff80007fffff80007fffff80007fffff80007fffff80007fffff80007fffff80007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fffffe0007fffffe0007fffffe0007fffffe0007fffffe0007fffffe0007fffffe0007fffffe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        202: '34:36:0007f800000007fc0000000ffe0000001fbf0000003f1f0000003e0f8000007c07c000000000000000000000000000000000000000000007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fffff80007fffff80007fffff80007fffff80007fffff80007fffff80007fffff80007fffff80007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fffffe0007fffffe0007fffffe0007fffffe0007fffffe0007fffffe0007fffffe0007fffffe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        203: '34:36:003e1f8000003e1f8000003e1f8000003e1f8000003e1f8000003e1f8000003e1f8000000000000000000000000000000000000000000007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fffffc0007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fffff80007fffff80007fffff80007fffff80007fffff80007fffff80007fffff80007fffff80007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fffffe0007fffffe0007fffffe0007fffffe0007fffffe0007fffffe0007fffffe0007fffffe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        204: '19:21:fe00007f00003f80001f80000fc00007e00003e00000100000000000000000000007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        205: '19:21:007f00007e0000fc0001f80001f80003f00007e00000000000000000000000000007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        206: '19:21:07f80007fc000ffe001fbf003f1f003e0f807c07c000000000000000000000000007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        207: '19:21:3e1f803e1f803e1f803e1f803e1f803e1f803e1f8000000000000000000000000007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc0007fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        208: '42:44:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007fffc00000007fffff0000007fffffc000007ffffff000007ffffff800007ffffffc00007ffffffe00007fffffff00007fe03fff80007fe00fff80007fe003ffc0007fe001ffc0007fe000ffc0007fe000ffe0007fe0007fe0007fe0007fe0007fe0007fe007ffff003fe007ffff003ff007ffff003ff007ffff003ff007ffff003ff007ffff003ff007ffff003fe0007fe0007fe0007fe0007fe0007fe0007fe0007fe000ffe0007fe000ffc0007fe001ffc0007fe003ffc0007fe007ff80007fe03fff80007fffffff00007ffffffe00007ffffffc00007ffffff800007ffffff000007fffffc000007fffff0000007fffe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        209: '42:44:0001c03800000003f07800000007fc780000000ffff80000000f3ff00000000f1ff00000000e07e0000000000000000000000000000000000000000000000000000007fe0007fc0007ff0007fc0007ff0007fc0007ff8007fc0007ff8007fc0007ffc007fc0007ffc007fc0007ffe007fc0007ffe007fc0007fff007fc0007fff007fc0007fff807fc0007fff807fc0007fffc07fc0007fffc07fc0007fdfe07fc0007fdfe07fc0007fcfe07fc0007fcff07fc0007fc7f07fc0007fc7f87fc0007fc3f87fc0007fc3fc7fc0007fc1fc7fc0007fc1fe7fc0007fc0fe7fc0007fc0ff7fc0007fc07f7fc0007fc07fffc0007fc07fffc0007fc03fffc0007fc03fffc0007fc01fffc0007fc01fffc0007fc00fffc0007fc00fffc0007fc007ffc0007fc007ffc0007fc003ffc0007fc003ffc0007fc001ffc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        210: '43:45:000fe00000000007f00000000003f80000000001f80000000000fc00000000007e00000000003e00000000000100000000000000000000000000000000000e0000000003fff00000000ffffe0000003fffff0000007fffffc00000ffffffe00001fffffff00003fffffff00003ffe0fff80007ff803ffc0007ff001ffc000ffe000ffe000ffc0007fe000ffc0007fe001ff80007ff001ff80003ff001ff80003ff001ff80003ff001ff00003ff001ff00003ff001ff00001ff001ff00001ff001ff00001ff001ff00003ff001ff00003ff001ff80003ff001ff80003ff001ff80003ff001ff80003ff001ffc0007fe000ffc0007fe000ffe000ffe0007fe001ffc0007ff003ffc0003ffc07ff80003fffffff80001fffffff00000ffffffe000007fffffc000003fffff8000000ffffe00000003fff8000000007f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        211: '43:45:000007f00000000007e0000000000fc0000000001f80000000001f80000000003f00000000007e00000000000000000000000000000000000000000000000e0000000003fff00000000ffffe0000003fffff0000007fffffc00000ffffffe00001fffffff00003fffffff00003ffe0fff80007ff803ffc0007ff001ffc000ffe000ffe000ffc0007fe000ffc0007fe001ff80007ff001ff80003ff001ff80003ff001ff80003ff001ff00003ff001ff00003ff001ff00001ff001ff00001ff001ff00001ff001ff00003ff001ff00003ff001ff80003ff001ff80003ff001ff80003ff001ff80003ff001ffc0007fe000ffc0007fe000ffe000ffe0007fe001ffc0007ff003ffc0003ffc07ff80003fffffff80001fffffff00000ffffffe000007fffffc000003fffff8000000ffffe00000003fff8000000007f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        212: '43:45:0000ff0000000000ff8000000001ffc000000003f7e000000007e3e000000007c1f00000000f80f8000000000000000000000000000000000000000000000e0000000003fff00000000ffffe0000003fffff0000007fffffc00000ffffffe00001fffffff00003fffffff00003ffe0fff80007ff803ffc0007ff001ffc000ffe000ffe000ffc0007fe000ffc0007fe001ff80007ff001ff80003ff001ff80003ff001ff80003ff001ff00003ff001ff00003ff001ff00001ff001ff00001ff001ff00001ff001ff00003ff001ff00003ff001ff80003ff001ff80003ff001ff80003ff001ff80003ff001ffc0007fe000ffc0007fe000ffe000ffe0007fe001ffc0007ff003ffc0003ffc07ff80003fffffff80001fffffff00000ffffffe000007fffffc000003fffff8000000ffffe00000003fff8000000007f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        213: '43:45:0000e01c00000001f83c00000003fe3c00000007fffc000000079ff8000000078ff80000000703f0000000000000000000000000000000000000000000000e0000000003fff00000000ffffe0000003fffff0000007fffffc00000ffffffe00001fffffff00003fffffff00003ffe0fff80007ff803ffc0007ff001ffc000ffe000ffe000ffc0007fe000ffc0007fe001ff80007ff001ff80003ff001ff80003ff001ff80003ff001ff00003ff001ff00003ff001ff00001ff001ff00001ff001ff00001ff001ff00003ff001ff00003ff001ff80003ff001ff80003ff001ff80003ff001ff80003ff001ffc0007fe000ffc0007fe000ffe000ffe0007fe001ffc0007ff003ffc0003ffc07ff80003fffffff80001fffffff00000ffffffe000007fffffc000003fffff8000000ffffe00000003fff8000000007f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        214: '43:45:0003e1f800000003e1f800000003e1f800000003e1f800000003e1f800000003e1f800000003e1f8000000000000000000000000000000000000000000000e0000000003fff00000000ffffe0000003fffff0000007fffffc00000ffffffe00001fffffff00003fffffff00003ffe0fff80007ff803ffc0007ff001ffc000ffe000ffe000ffc0007fe000ffc0007fe001ff80007ff001ff80003ff001ff80003ff001ff80003ff001ff00003ff001ff00003ff001ff00001ff001ff00001ff001ff00001ff001ff00003ff001ff00003ff001ff80003ff001ff80003ff001ff80003ff001ff80003ff001ffc0007fe000ffc0007fe000ffe000ffe0007fe001ffc0007ff003ffc0003ffc07ff80003fffffff80001fffffff00000ffffffe000007fffffc000003fffff8000000ffffe00000003fff8000000007f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        215: '42:44:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200001000000700003800000f80003c00001fc0007e00003fc000ff00001fe001fe00000ff003fc000007f807f8000003fc0ff0000001fe1ff0000000ff3fe0000000ffffc00000007fff800000003fff000000001ffe000000000ffc0000000007f8000000000ffc000000001ffe000000003fff000000007fff80000000ffffc0000000ff3fe0000001fe1ff0000003fc0ff8000007f807f800000ff003fc00001fe001fe00003fc000ff00001fc0007e00000f80003c000007000018000002000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        216: '43:45:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000e0007000003fff00780000ffffe0f80003fffff1f00007ffffffe0000fffffffe0001fffffffc0003fffffff80003ffe0fff80007ff803ffc0007ff001ffc000ffe000ffe000ffc001ffe000ffc003ffe001ff8007fff001ff800ffff001ff801fbff001ff803f3ff001ff007e3ff001ff00fc3ff001ff01f81ff001ff01f01ff001ff03e01ff001ff07c03ff001ff0f803ff001ff9f803ff001ffbf003ff001fffe003ff001fffc003ff001fff8007fe000fff0007fe000ffe000ffe0007fe001ffc0007ff003ffc0003ffc07ff80003fffffff80007fffffff0000fffffffe0001fffffffc0003f3fffff80007e0ffffe00003c03fff8000038003f800000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        217: '41:43:001fc0000000000fe00000000007f00000000003f00000000001f80000000000fc00000000007c00000000000200000000000000000000000000000000000000000007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fe003ff00007fe003ff00007fe003ff00003ff007fe00003ffc1ffe00003ffffffc00001ffffffc00000ffffff800000ffffff0000007ffffe0000001ffffc00000007fff000000000ff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        218: '41:43:00000fe0000000000fc0000000001f80000000003f00000000003f00000000007e0000000000fc00000000000000000000000000000000000000000000000000000007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fe003ff00007fe003ff00007fe003ff00003ff007fe00003ffc1ffe00003ffffffc00001ffffffc00000ffffff800000ffffff0000007ffffe0000001ffffc00000007fff000000000ff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        219: '41:43:0000ff0000000000ff8000000001ffc000000003f7e000000007e3e000000007c1f00000000f80f8000000000000000000000000000000000000000000000000000007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fe003ff00007fe003ff00007fe003ff00003ff007fe00003ffc1ffe00003ffffffc00001ffffffc00000ffffff800000ffffff0000007ffffe0000001ffffc00000007fff000000000ff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        220: '41:43:0007c3f000000007c3f000000007c3f000000007c3f000000007c3f000000007c3f000000007c3f0000000000000000000000000000000000000000000000000000007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fc001ff00007fe003ff00007fe003ff00007fe003ff00003ff007fe00003ffc1ffe00003ffffffc00001ffffffc00000ffffff800000ffffff0000007ffffe0000001ffffc00000007fff000000000ff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        221: '36:38:00003f800000003f000000007e00000000fc00000000fc00000001f800000003f000000000000000000000000000000000000000000000ffc0003ff8ffe0003ff07fe0007ff07ff0007fe03ff000ffc01ff800ffc01ffc01ff800ffc03ff800ffe03ff0007fe07fe0003ff07fe0003ff0ffc0001ff9ffc0001ffdff80000fffff800007ffff000007fffe000003fffe000003fffc000001fffc000000fff8000000fff00000007ff00000007fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        222: '37:39:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007ffff000007fffff00007fffffc0007fffffe0007ffffff0007ffffff8007ffffff8007ffffffc007fc03ffc007fc00ffc007fc00ffe007fc007fe007fc007fe007fc007fe007fc007fe007fc007fe007fc007fe007fc00ffc007fc01ffc007ffffffc007ffffff8007ffffff8007ffffff0007fffffe0007fffffc0007fffff00007ffff800007fc00000007fc00000007fc00000007fc00000007fc00000007fc00000007fc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        223: '36:38:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e00000001fff0000007fffc00000ffffe00001fffff00003fffff80007fffff80007ff07fc0007fc03fc000ffc03fc000ff801fe000ff801fe000ff807fe000ff81ffe000ff83ffe000ff87fc0000ff87f00000ff8ff00000ff8fe00000ff8fe00000ff8ff00000ff8ff80000ff8ffc0000ff8fff0000ff8fff8000ff87ffe000ff83fff000ff81fff000ff807ff800ff803ff800ff800ffc00ff8007fc00ff8007fc00ff8007fc00ff8007fc00ff8007fc00ff8c0ffc00ff8ffffc00ff8ffff800ff8ffff800ff8ffff000ff8fffe000ff8fff80000000fc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        224: '34:36:000000000000000000000000000000000000000000000000000000000000000000000000fc00000000fe000000007f000000003f800000001f800000000fc000000007e000000003e000000001f000000000f80000000000000000000000000000000000000000000001fffe000007ffff800007ffffc00007ffffe00007fffff00007fffff80007e03ff80006000ff800000007fc00000007fc00000007fc000007fffc0000fffffc0003fffffc0007fffffc000ffffffc001ffffffc001ffc07fc001ff007fc003fe007fc003fe007fc003fe007fc003fe00ffc003ff01ffc003ff83ffc001ffffffc001ffffffc000ffff7fc000ffff7fc0007ffe7fc0001ff87fc00007e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        225: '34:36:0000000000000000000000000000000000000000000000000000000000000000000000000007f00000000fe00000001fc00000001f800000003f000000007e000000007c00000000f800000001f800000001f00000000200000000000000000000000000000000000001fffe000007ffff800007ffffc00007ffffe00007fffff00007fffff80007e03ff80006000ff800000007fc00000007fc00000007fc000007fffc0000fffffc0003fffffc0007fffffc000ffffffc001ffffffc001ffc07fc001ff007fc003fe007fc003fe007fc003fe007fc003fe00ffc003ff01ffc003ff83ffc001ffffffc001ffffffc000ffff7fc000ffff7fc0007ffe7fc0001ff87fc00007e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        226: '34:36:00000000000000000000000000000000000000000000000000000000000000000000000003f800000003f800000007fc00000007fe0000000ffe0000001f9f0000001f1f0000003e0f8000003c07c000007c03c000000000000000000000000000000000000000000001fffe000007ffff800007ffffc00007ffffe00007fffff00007fffff80007e03ff80006000ff800000007fc00000007fc00000007fc000007fffc0000fffffc0003fffffc0007fffffc000ffffffc001ffffffc001ffc07fc001ff007fc003fe007fc003fe007fc003fe007fc003fe00ffc003ff01ffc003ff83ffc001ffffffc001ffffffc000ffff7fc000ffff7fc0007ffe7fc0001ff87fc00007e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        227: '34:36:00000000000000000000000000000000000000000000000000000000000000000000000000000000000601c000001f81c000003fc1c000003ff3c000007fffc0000078ff800000787f800000701f00000000000000000000000000000000000000000000000000000001fffe000007ffff800007ffffc00007ffffe00007fffff00007fffff80007e03ff80006000ff800000007fc00000007fc00000007fc000007fffc0000fffffc0003fffffc0007fffffc000ffffffc001ffffffc001ffc07fc001ff007fc003fe007fc003fe007fc003fe007fc003fe00ffc003ff01ffc003ff83ffc001ffffffc001ffffffc000ffff7fc000ffff7fc0007ffe7fc0001ff87fc00007e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        228: '34:36:00000000000000000000000000000000000000000000000000000000000000000000000000000000003f0f8000003f0f8000003f0f8000003f0f8000003f0f8000003f0f800000000000000000000000000000000000000000000000000000000000000001fffe000007ffff800007ffffc00007ffffe00007fffff00007fffff80007e03ff80006000ff800000007fc00000007fc00000007fc000007fffc0000fffffc0003fffffc0007fffffc000ffffffc001ffffffc001ffc07fc001ff007fc003fe007fc003fe007fc003fe007fc003fe00ffc003ff01ffc003ff83ffc001ffffffc001ffffffc000ffff7fc000ffff7fc0007ffe7fc0001ff87fc00007e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        229: '34:36:000000000000000000000000e000000003f800000007fe0000000ffe0000001fbf0000001e0f0000001e0f0000001c078000001c078000001e070000001e0f0000001fbf0000000ffe00000007fe00000003fc00000001f0000000000000000000000000000000000001fffe000007ffff800007ffffc00007ffffe00007fffff00007fffff80007e03ff80006000ff800000007fc00000007fc00000007fc000007fffc0000fffffc0003fffffc0007fffffc000ffffffc001ffffffc001ffc07fc001ff007fc003fe007fc003fe007fc003fe007fc003fe00ffc003ff01ffc003ff83ffc001ffffffc001ffffffc000ffff7fc000ffff7fc0007ffe7fc0001ff87fc00007e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        230: '53:55:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001fff801ff800007fffe07ffe00007ffff8ffff80007ffffdffffc0007fffffffffe0007ffffffffff0007e03fffc3ff0006000fff01ff80000007fe00ff80000007fe007fc0000007fc007fc00007fffc007fc000ffffffffffc003ffffffffffc007ffffffffffc00fffffffffffc01fffffffffffc01ffc07ffffffc01ff007fc0000003fe007fc0000003fe007fc0000003fe007fe0000003fe00ffe0001803ff01fff0007803ff83fff801f801fffffffffff801fffffffffff800ffffe7fffff800ffffc3fffff8007fff01fffff0001ffc007fff800007e00007f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        231: '30:32:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000fff00003fffe000ffffe001ffffe003ffffe007ffffe00fffffe00ffe01e01ffc00601ff800001ff000001ff000003ff000003fe000003fe000003fe000003fe000003fe000003ff000003ff000001ff000001ff800001ff800200ffe00e00fff83e007ffffe007ffffe003ffffe001ffffe0007fffe0001fffc00003fc000000780000003c0000003c0000001c0000003e0000187e00001ffc00001ffc00001ff800000ff000000000000000000000000000000000000000000000000000000000000000000000000000',
        232: '34:36:000000000000000000000000000000000000000000000000000000000000000000000000fc00000000fe000000007f000000003f800000001f800000000fc000000007e000000003e000000001f000000000f800000000000000000000000000000000000000000000000ffe0000007fff800000ffffc00001ffffe00003fffff00007fffff8000ffe1ffc000ffc07fc001ff803fe001ff003fe001ff003fe001fe001fe003fffffff003fffffff003fffffff003fffffff003fffffff003fffffff003fe00000003fe00000001ff00000001ff00000001ff00004000ff8001c000ffe00fc0007fffffc0007fffffc0003fffffc0001fffffc00007ffffc00001fffe0000003fc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        233: '34:36:0000000000000000000000000000000000000000000000000000000000000000000000000007f00000000fe00000001fc00000001f800000003f000000007e000000007c00000000f800000001f800000001f000000002000000000000000000000000000000000000000ffe0000007fff800000ffffc00001ffffe00003fffff00007fffff8000ffe1ffc000ffc07fc001ff803fe001ff003fe001ff003fe001fe001fe003fffffff003fffffff003fffffff003fffffff003fffffff003fffffff003fe00000003fe00000001ff00000001ff00000001ff00004000ff8001c000ffe00fc0007fffffc0007fffffc0003fffffc0001fffffc00007ffffc00001fffe0000003fc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        234: '34:36:00000000000000000000000000000000000000000000000000000000000000000000000003f800000003f800000007fc00000007fe0000000ffe0000001f9f0000001f1f0000003e0f8000003c07c000007c03c0000000000000000000000000000000000000000000000ffe0000007fff800000ffffc00001ffffe00003fffff00007fffff8000ffe1ffc000ffc07fc001ff803fe001ff003fe001ff003fe001fe001fe003fffffff003fffffff003fffffff003fffffff003fffffff003fffffff003fe00000003fe00000001ff00000001ff00000001ff00004000ff8001c000ffe00fc0007fffffc0007fffffc0003fffffc0001fffffc00007ffffc00001fffe0000003fc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        235: '34:36:00000000000000000000000000000000000000000000000000000000000000000000000000000000003f0f8000003f0f8000003f0f8000003f0f8000003f0f8000003f0f8000000000000000000000000000000000000000000000000000000000000000000ffe0000007fff800000ffffc00001ffffe00003fffff00007fffff8000ffe1ffc000ffc07fc001ff803fe001ff003fe001ff003fe001fe001fe003fffffff003fffffff003fffffff003fffffff003fffffff003fffffff003fe00000003fe00000001ff00000001ff00000001ff00004000ff8001c000ffe00fc0007fffffc0007fffffc0003fffffc0001fffffc00007ffffc00001fffe0000003fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        236: '17:19:000000000000000000000000000000000000000000fc0000fe00007f00003f80001f80000fc00007e00003e00001f00000f8000000000000000000000000000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        237: '17:19:0000000000000000000000000000000000000000000007e0000fe0001fc0001f80003f00007e00007c0000f80001f80001f0000200000000000000000000000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        238: '17:19:00000000000000000000000000000000000000000007f00007f0000ff8000ffc001ffc003f3e003e3e007c1f00780f80f807800000000000000000000000000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        239: '17:19:0000000000000000000000000000000000000000000000007e1f007e1f007e1f007e1f007e1f007e1f000000000000000000000000000000000000000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff8000ff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        240: '35:37:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ff800000007fc03800003fe1f800001feffc00000ffff000000fff8000001ffc000000fffe000003fffe000007fcff000003e07f800003007fc00000003fe00000001fe000000feff000007ffff80001fffff80003fffffc0007fffffc000ffffffe000ffffffe001ffe0fff001ff803ff001ff801ff003ff001ff003ff001ff003fe001ff003fe001ff003fe001ff003fe001ff003fe001ff003ff001ff001ff001ff001ff003ff001ff803fe000ffc07fe000fff1ffe0007fffffc0007fffff80003fffff00001ffffe000007fffc000003fff00000003f80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        241: '36:38:00000000000000000000000000000000000000000000000000000000000000000000000000000000000300e000000fc0e000001fe0e000001ff9e000003fffe000003c7fc000003c3fc00000380f8000000000000000000000000000000000000000000000000000000ff83fe0000ff8fff0000ff9fff8000ffbfffc000ffffffc000ffffffe000ffffffe000fff87fe000ffe03ff000ffe01ff000ffc01ff000ffc01ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        242: '35:37:000000000000000000000000000000000000000000000000000000000000000000000000fc00000000fe000000007f000000003f800000001f800000000fc000000007e000000003e000000001f000000000f800000000000000000000000000000000000000000000000ffe0000007fff800000ffffe00001fffff00003fffff80007fffffc000ffffffc000ffc0ffe001ff807fe001ff803ff001ff003ff001ff001ff003ff001ff003fe001ff003fe001ff003fe001ff003fe001ff003fe001ff003ff001ff003ff001ff001ff001ff001ff003ff001ff803fe000ffc07fe000ffe1ffe0007fffffc0007fffff80003fffff00001ffffe000007fffc000003fff00000003f80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        243: '35:37:0000000000000000000000000000000000000000000000000000000000000000000000000007f00000000fe00000001fc00000001f800000003f000000007e000000007c00000000f800000001f800000001f000000002000000000000000000000000000000000000000ffe0000007fff800000ffffe00001fffff00003fffff80007fffffc000ffffffc000ffc0ffe001ff807fe001ff803ff001ff003ff001ff001ff003ff001ff003fe001ff003fe001ff003fe001ff003fe001ff003fe001ff003ff001ff003ff001ff001ff001ff001ff003ff001ff803fe000ffc07fe000ffe1ffe0007fffffc0007fffff80003fffff00001ffffe000007fffc000003fff00000003f80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        244: '35:37:00000000000000000000000000000000000000000000000000000000000000000000000003f800000003f800000007fc00000007fe0000000ffe0000001f9f0000001f1f0000003e0f8000003c07c000007c03c0000000000000000000000000000000000000000000000ffe0000007fff800000ffffe00001fffff00003fffff80007fffffc000ffffffc000ffc0ffe001ff807fe001ff803ff001ff003ff001ff001ff003ff001ff003fe001ff003fe001ff003fe001ff003fe001ff003fe001ff003ff001ff003ff001ff001ff001ff001ff003ff001ff803fe000ffc07fe000ffe1ffe0007fffffc0007fffff80003fffff00001ffffe000007fffc000003fff00000003f80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        245: '35:37:00000000000000000000000000000000000000000000000000000000000000000000000000000000000601c000001f81c000003fc1c000003ff3c000007fffc0000078ff800000787f800000701f000000000000000000000000000000000000000000000000000000000ffe0000007fff800000ffffe00001fffff00003fffff80007fffffc000ffffffc000ffc0ffe001ff807fe001ff803ff001ff003ff001ff001ff003ff001ff003fe001ff003fe001ff003fe001ff003fe001ff003fe001ff003ff001ff003ff001ff001ff001ff001ff003ff001ff803fe000ffc07fe000ffe1ffe0007fffffc0007fffff80003fffff00001ffffe000007fffc000003fff00000003f80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        246: '35:37:00000000000000000000000000000000000000000000000000000000000000000000000000000000003f0f8000003f0f8000003f0f8000003f0f8000003f0f8000003f0f8000000000000000000000000000000000000000000000000000000000000000000ffe0000007fff800000ffffe00001fffff00003fffff80007fffffc000ffffffc000ffc0ffe001ff807fe001ff803ff001ff003ff001ff001ff003ff001ff003fe001ff003fe001ff003fe001ff003fe001ff003fe001ff003ff001ff003ff001ff001ff001ff001ff003ff001ff803fe000ffc07fe000ffe1ffe0007fffffc0007fffff80003fffff00001ffffe000007fffc000003fff00000003f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        247: '42:44:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007f80000000007f80000000007f80000000007f80000000007f80000000007f80000000007f80000000007f80000000007f80000000000000000000000000000000000000000007fffffff80007fffffff80007fffffff80007fffffff80007fffffff80007fffffff80007fffffff80000000000000000000000000000000000000000007f80000000007f80000000007f80000000007f80000000007f80000000007f80000000007f80000000007f80000000007f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        248: '35:37:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006000000000f00000ffe1f80007fff9f0000fffffe0001fffffc0003fffff80007fffffc000ffffffc000ffc0ffe001ff807fe001ff80fff001ff01fff001ff03fff003ff07dff003fe07dff003fe0f9ff003fe1f1ff003fe3e1ff003fe7c1ff003fff81ff003fff81ff001fff01ff001ffe03ff001ffc03fe000ffc07fe000fff1ffe0007fffffc0007fffff80007fffff0000fffffe0001f7fffc0003e3fff00003c03f800000c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        249: '36:38:0000000000000000000000000000000000000000000000000000000000000000000000007e000000007f000000003f800000001fc00000000fc000000007e000000003f000000001f000000000f8000000007c000000000000000000000000000000000000000000000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff803ff000ff803ff000ff803ff000ffc07ff000ffc0fff0007ffffff0007ffffff0007ffffff0003fffdff0003fff9ff0001fff1ff00007fe1ff00001f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        250: '36:38:0000000000000000000000000000000000000000000000000000000000000000000000000003f800000007f00000000fe00000000fc00000001f800000003f000000003e000000007c00000000fc00000000f8000000010000000000000000000000000000000000000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff803ff000ff803ff000ff803ff000ffc07ff000ffc0fff0007ffffff0007ffffff0007ffffff0003fffdff0003fff9ff0001fff1ff00007fe1ff00001f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        251: '36:38:00000000000000000000000000000000000000000000000000000000000000000000000003f800000003f800000007fc00000007fe0000000ffe0000001f9f0000001f1f0000003e0f8000003c07c000007c03c00000000000000000000000000000000000000000000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff803ff000ff803ff000ff803ff000ffc07ff000ffc0fff0007ffffff0007ffffff0007ffffff0003fffdff0003fff9ff0001fff1ff00007fe1ff00001f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        252: '36:38:00000000000000000000000000000000000000000000000000000000000000000000000000000000003f0f8000003f0f8000003f0f8000003f0f8000003f0f8000003f0f80000000000000000000000000000000000000000000000000000000000000000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff801ff000ff803ff000ff803ff000ff803ff000ffc07ff000ffc0fff0007ffffff0007ffffff0007ffffff0003fffdff0003fff9ff0001fff1ff00007fe1ff00001f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        253: '33:35:000000000000000000000000000000000000000000000000000000000000000000000000000fe00000001fc00000003f800000003f000000007e00000000fc00000000f800000001f000000003f000000003e0000000040000000000000000000000000000000000007f8001ff007fc001ff007fc003fe003fe003fe003fe003fe001fe003fc001ff007fc001ff007f8000ff007f8000ff80ff80007f80ff00007f80ff00007fc1ff00003fc1fe00003fc1fe00003fe1fe00001fe3fc00001ff3fc00000ff3fc00000ff7f800000ffff8000007fff8000007fff0000003fff0000003fff0000003ffe0000001ffe0000001ffe0000001ffc0000000ffc0000000ffc00000007f800000007f800000007f00000000ff00000001ff00000003fe0000007ffe0000007ffc0000007ffc0000007ff80000007ff00000007fc0000000000000000000000000000000000000000000000000000000000000000000000000000',
        254: '36:38:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff83fc0000ff8fff0000ff9fff8000ffbfffc000ffffffe000ffffffe000fffffff000fff03ff000ffe01ff800ffc01ff800ffc00ff800ffc00ff800ff800ffc00ff8007fc00ff8007fc00ff8007fc00ff8007fc00ff8007fc00ff8007fc00ff800ffc00ffc00ff800ffc00ff800ffe01ff800fff03ff800fff8fff000fffffff000ffffffe000ffbfffc000ff9fffc000ff8fff0000ff87fe0000ff80f80000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000ff80000000000000000000000000000000000000000000000000000000000000000000000000000',
        255: '33:35:00000000000000000000000000000000000000000000000000000000000000000000000000000000007e1f0000007e1f0000007e1f0000007e1f0000007e1f0000007e1f00000000000000000000000000000000000000000000000000000000000000007f8001ff007fc001ff007fc003fe003fe003fe003fe003fe001fe003fc001ff007fc001ff007f8000ff007f8000ff80ff80007f80ff00007f80ff00007fc1ff00003fc1fe00003fc1fe00003fe1fe00001fe3fc00001ff3fc00000ff3fc00000ff7f800000ffff8000007fff8000007fff0000003fff0000003fff0000003ffe0000001ffe0000001ffe0000001ffc0000000ffc0000000ffc00000007f800000007f800000007f00000000ff00000001ff00000003fe0000007ffe0000007ffc0000007ffc0000007ff80000007ff00000007fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8364: '35:37:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e00000001fff0000007fffc00001fffff00003fffff00007fffff0000ffffff0001ffffff0001ffe01f0003ff80070003ff00030007fe00010007fe00000007fc0000007fffffe0007fffffe000ffffffc000ffffffc000ffffffc000ffffff80000ff80000000ff80000000ff80000000ff80000007ffffe0000fffffe0000fffffc0000fffffc0000fffffc000007fc00000007fe00000007fe00010003ff00030003ff80070001ffc01f0001fff8ff0000ffffff00007fffff00003fffff00001fffff00000ffffc000003fff00000003f8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8211: '25:27:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001ffffe001ffffe001ffffe001ffffe001ffffe001ffffe001ffffe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8212: '50:52:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001fffffffffff001fffffffffff001fffffffffff001fffffffffff001fffffffffff001fffffffffff001fffffffffff0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8222: '33:35:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003fc1fe00003fc1fe00003fc1fe00003fc1fe00003fc1fe00003fc1fe00003fc1fe00003fc1fe00003fc3fe00003fc3fc00007f83fc00007f83f800007f07f000007e07f00000fe07e00000fc07e00000fc0fc00000f80fc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8220: '33:35:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001f01f000003f03f000007e03f000007e07f00000fe07e00000fe0fe00001fc0fe00001fc1fe00003fc3fc00007fc3fc00007fc3fc00007fc3fc00007fc3fc00007fc3fc00007fc3fc00007fc3fc00007fc3fc00007fc3fc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8221: '33:35:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001fe0ff00001fe0ff00001fe0ff00001fe0ff00001fe0ff00001fe0ff00001fe0ff00001fe0ff00001fe1ff00001fe1fe00003fc1fe00003f81fc00003f83f800003f03f800007f03f000007e03f000007e07e000007c07c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8217: '19:21:00000000000000000000000000000000000000000000000000000000000000000003fc0003fc0003fc0003fc0003fc0003fc0003fc0003fc0007fc0007f80007f80007f0000fe0000fe0000fc0000fc0001f80001f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8226: '32:34:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001c00000000ff00000001ffc0000003ffe0000007ffe000000ffff000000ffff000000ffff800001ffff800001ffff800001ffff800001ffff800001ffff800000ffff000000ffff0000007fff0000007ffe0000003ffc0000001ff800000007e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        338: '59:61:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ffffffffe000001fffffffffe000007fffffffffe00001ffffffffffe00007ffffffffffe0000fffffffffffe0001fffffffffffe0003fffffffffffe0003fffc07fe00000007ffe007fe00000007ff8007fe0000000ffe0007fe0000000ffe0007fe0000001ffc0007fe0000001ff80007fe0000001ff80007fe0000001ff80007fffffc001ff80007fffffc001ff00007fffffc001ff00007fffffc001ff00007fffffc001ff00007fffffc001ff00007fffffc001ff80007fffffc001ff80007fe0000001ff80007fe0000001ff80007fe0000001ffc0007fe0000000ffe0007fe0000000ffe0007fe0000000fff8007fe00000007ffc007fe00000003fff807fe00000003fffffffffffe0001fffffffffffe0000fffffffffffe00007ffffffffffe00001ffffffffffe00000ffffffffffe000001fffffffffe0000003ffffffffe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        339: '55:57:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ffe007ff00000007fff81fffc000000ffffc7fffe000001ffffefffff000003ffffffffff800007ffffffffffc0000ffffffff0ffe0000ffc0fffe03fe0001ff807ffc01ff0001ff803ff801ff0001ff003ff801ff0001ff001ff000ff0003ff001fffffff8003fe001fffffff8003fe001fffffff8003fe001fffffff8003fe001fffffff8003fe001fffffff8003ff001ff000000003ff001ff000000001ff001ff800000001ff003ff800000001ff803ff800020000ffc07ffc000e0000ffe1ffff007e00007ffffffffffe00007ffffffffffe00003ffffffffffe00001ffffc7ffffe000007fff83ffffc000003ffe00ffff00000003f0001fe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        352: '36:38:00f803c000007c07c000003e0f8000001f1f0000001fbe0000000ffe00000007fc00000000000000000000000000000000000000f00000001fffc000007ffffc0001fffffc0003fffffc0003fffffc0007fffffc0007fffffc000ffe01fc000ff8003c000ff80004000ff00000000ff00000000ff00000000ff80000000ffc0000000fffc000000ffffc000007ffff800007ffffe00003fffff80001fffffc0000fffffe00003ffffe00000fffff000000ffff0000000fff00000003ff00000001ff80000001ff80000001ff80080001ff000e0001ff000f8003ff000ff007ff000fffffff000ffffffe000ffffffe000ffffffc000ffffff80003fffff000007fffc0000007fc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        353: '30:32:0000000000000000000000000000000000000000000000000000000003c01f0003e03e0001f03c0001f07c0000f8f800007df800007ff000003fe000003fe000001fc00000000000000000000000000000000000007ffc0003ffffc007ffffc00fffffc00fffffc01fffffc01ff81fc01fe001c01fc000401fc000001fe000001ff800001fffe0001ffffe000fffff800fffffc003ffffc001ffffe0001fffe00000ffe000001ff000001ff000001ff018001ff01f003fe01fffffe01fffffe01fffffc01fffff801fffff0007fffc00003fe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        381: '37:39:00f803c000007c07c000003e0f8000001f1f0000001fbe0000000ffe00000007fc000000000000000000000000000000000000000000001fffffffc01fffffffc01fffffffc01fffffffc01fffffffc01fffffffc01fffffffc01fffffff80000003ff00000007ff0000000ffe0000001ffc0000001ff80000003ff80000007ff0000000ffe0000000ffc0000001ffc0000003ff80000003ff00000007fe0000000ffe0000001ffc0000001ff80000003ff00000007ff0000000ffe0000000ffc0000001ff80000003ff80000007ff00000007fe0000000ffc0000001fffffffc03fffffffc03fffffffc03fffffffc03fffffffc03fffffffc03fffffffc03fffffffc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        382: '29:31:0000000000000000000000000000000000000000000000000000000003c01f0003e03e0001f03c0001f07c0000f8f800007df800007ff000003fe000003fe000001fc000000000000000000000000000000000001fffffe01fffffe01fffffe01fffffe01fffffe01fffffe01fffffe000007fe00000ffc00001ff800003ff000007fe00000ffc00001ffc00001ff800003ff000007fe00000ffc00001ff800003ff000007fe000007fe00000ffc00001ff800003fffffe03fffffe03fffffe03fffffe03fffffe03fffffe03fffffe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
    },
    'a': {
        32: '11:13:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        33: '14:16:00000000000000000000000000000fc00fc00fc00fc00fc00fc00fc00fc00fc00fc00fc00f8007800780078007800780000000000fc00fc00fc00fc00fc00fc000000000000000000000000000000000000000000000000000000000000000000000',
        34: '16:18:0000000000000000000000000000000000000000001c78001c78001c78001c78001c78001c78001c78001c78001c7800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        35: '26:28:00000000000000000000000000000000000000000000000000000000003878000038700000387000007870000078f0000070f0000fffff000fffff000fffff000fffff0000e1c00000e1c00001e1c00001c3c0003ffffc003ffffc003ffffc003ffffc0003878000038700000387000007870000070f0000070f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        36: '21:23:00000000000000000000000000000000000000700000700000700000700001ff0007ffc00fffc01fffc01f70c03e70003e70003f70001ff0001fff000fff8007ffc001ffe0007fe00073e00073e02073e03c73e03fffe03fffc03fff8003fe00007000007000007000007000007000000000000000000000000000000000000000000000000000000000000000000000000000',
        37: '31:33:0000000000000000000000000000000000000000000000000000000000000fc00f00001fe00e00003ff01e000078701c00007878380000787838000078787000007878f000007878e000007871e000003ff1c000001fe3c000000fc387c00000078ff00000071ff800000e3c7800000e3c3800001c3c3c00003c383c0000383c3c0000783c3c0000703c780000f03ef80000e01ff00001e00fe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        38: '27:29:00000000000000000000000000000000000000000000000000ff800001ffc00003ffc00003ffc00007e0c00007e0000007e0000007e0000003f0000003f8000007fc0f000ffc0f001ffe1f001f3f1f003e3f9f003e1ffe003e0ffe003e07fc003e03fc003f01f8003f83fc001ffffe000ffffe0007ffbf0003fe1f80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        39: '9:11:00000000000000000000000000001c001c001c001c001c001c001c001c001c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        40: '14:16:00000000000000000000000001e003e003c007c007c007800f800f800f001f001f001f001f001f001f001f001f001f001f001f001f001f000f800f800f80078007c003c003e001e00000000000000000000000000000000000000000000000000000',
        41: '14:16:0000000000000000000000001e001f001f000f800f80078007c007c007c003e003e003e003e003e003e003e003e003e003e003e003e003e007c007c007c00f800f800f001f001e000000000000000000000000000000000000000000000000000000',
        42: '16:18:000000000000000000000000000000000000018000018000018000718600799e003ffc000ff00007e0000ff0003ffc007dbe00718e00018000018000018000018000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        43: '26:28:00000000000000000000000000000000000000000000000000000000000000000000000000000000001e0000001e0000001e0000001e0000001e0000001e0000001e0000001e00001ffffc001ffffc001ffffc001ffffc00001e0000001e0000001e0000001e0000001e0000001e0000001e0000001e0000001e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        44: '12:14:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001f801f801f801f801f801f001e003e003c003c0038000000000000000000000000000000000000000000000000000000',
        45: '13:15:00000000000000000000000000000000000000000000000000000000000000000000000000003fe03fe03fe03fe03fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        46: '12:14:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001f801f801f801f801f801f80000000000000000000000000000000000000000000000000000000000000000000000000',
        47: '11:13:000000000000000000000000000000e001e001e001c001c003c00380038003800780070007000f000e000e000e001e001c001c003c00380038003800780070007000f000e00000000000000000000000000000000000000000000000000000000000',
        48: '21:23:00000000000000000000000000000000000001fc0007ff000fff800fffc01f8fc01f07e03f07e03f03e03e03f03e03f03e03f07e03f07e03f07e03f03e03f03e03f03e03f03f03e03f03e03f07e01f8fc01fffc00fff8007ff0003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        49: '21:23:00000000000000000000000000000000000000000001fc001ffc001ffc001ffc001ffc00187c00007c00007c00007c00007c00007c00007c00007c00007c00007c00007c00007c00007c00007c00007c00007c000fffe00fffe00fffe00fffe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        50: '21:23:00000000000000000000000000000000000007fc003fff003fff803fffc03e1fc0300fc0200fc00007c00007c0000fc0000fc0001f80003f00007f0000fe0001fc0003f80007f0000fe0001fc0003fffe03fffe03fffe03fffe03fffe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        51: '21:23:0000000000000000000000000000000000000ffe001fff001fff801fffc01c1fc0000fc0000fc00007c0000fc0001f8003ff0003fe0003ff0003ff80003fc0000fe00007e00007e00007e00007e0381fc03fffc03fff803fff001ffe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        52: '21:23:000000000000000000000000000000000000000000003f80003f80007f8000ff8000ff8001ff8003ff8003df80079f80079f800f1f801f1f801e1f803c1f803c1f80781f807ffff07ffff07ffff07ffff0001f80001f80001f80001f80001f80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        53: '21:23:0000000000000000000000000000000000000000001fffc01fffc01fffc01fffc01fffc01f00001f00001f00001f78001ffe001fff801fffc01fffc0180fe00007e00007e00007e00007e00007e03007e03c1fe03fffc03fff803fff000ffe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        54: '21:23:00000000000000000000000000000000000000ff8001ffc007ffc007ffc00fe0c01f80001f00001f00003f00003eff003fff803fffc03fffe03f87e03f03e03f03f03f03f03f03f01f03f01f03e01f87e00fffc00fffc007ff8001fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        55: '21:23:0000000000000000000000000000000000000000003fffe03fffe03fffe03fffe03fffe00007c0000fc0000f80001f80001f80003f00003f00003e00007e00007c0000fc0000fc0000f80001f80001f00003f00003f00003e00007e00007c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        56: '21:23:00000000000000000000000000000000000003fe000fff801fffc01fffc01f87e03f07e03f07e03f07e01f07e01f8fc00fff8003ff0007ff000fffc01f87e03f07e03e03e03e03e03e03e03f03e03f07e03fffe01fffc00fff8007ff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        57: '21:23:00000000000000000000000000000000000003fc0007fe000fff001fff803f0fc03f07c03e07e03e07e03e07e03e07e03e07e03f0fe03fffe01fffe00fffe007fbe001e3e00007e00007c0000fc0101fc01fff801fff001ffe001ffc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        58: '12:14:00000000000000000000000000000000000000000000000000001f801f801f801f801f801f801f800000000000000000000000001f801f801f801f801f801f8000000000000000000000000000000000000000000000000000000000000000000000',
        59: '12:14:00000000000000000000000000000000000000000000000000001f801f801f801f801f801f801f800000000000000000000000001f801f801f801f801f801f001f001e003e003c003800000000000000000000000000000000000000000000000000',
        60: '26:28:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c0000003c000001fc000007fc00003ff80000ffc00007fe00001ff800001fc000001f0000001fe000000ffc000003ff0000007fe000001ffc000003fc000000fc0000001c000000040000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        61: '26:28:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001ffffc001ffffc001ffffc001ffffc000000000000000000000000001ffffc001ffffc001ffffc001ffffc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        62: '26:28:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000180000001f0000001fc000001ff8000007fe000000ffc000003ff0000007fc000001fc0000007c000001fc00000ffc00007fe00001ff80000ffc00001ff000001f8000001e0000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        63: '18:20:0000000000000000000000000000000000000ff0003ffc003ffe003ffe003c7f00203f00003f00003f00003e00007e0000fc0001fc0003f80003f00007e00007e00007e00000000000000007e00007e00007e00007e00007e00007e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        64: '31:33:00000000000000000000000000000000000000000000000000000000000000000000000000000000000fe00000003ffc000000fffe000001f83f000003e0078000078003c0000f0001e0000e0000e0001c0f9c70001c1fdc70001c3ffc700038387c700038783c300038783c300038703c300038703c700038783c700038783c700038787ce0001c3fffe0001c1fdfc0001e0fdf00000e031800000f00000000078002000003c00e000001f83f000000fffe0000003ff80000000fe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        65: '24:26:0000000000000000000000000000000000000000000000000000000000fe000000ff000000ff000001ff000001ff800001ff800003ff800003efc00003e7c00007e7c00007c7e00007c3e0000fc3e0000fc3f0000f83f0001f81f0001ffff8001ffff8003ffff8003ffffc003e00fc007e007c007e007e007c007e00fc003e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        66: '23:25:000000000000000000000000000000000000000000000000000000001ffe00001fffc0001fffe0001ffff0001ffff0001f83f0001f83f0001f81f0001f83f0001f87f0001fffe0001fffc0001fffe0001ffff0001f83f0001f81f8001f81f8001f81f8001f81f8001f81f8001f87f8001ffff0001ffff0001fffe0001fff80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        67: '22:24:000000000000000000000000000000000000007fc001fff003fff807fff80ff9f81fc0381f80083f80003f00003f00003f00003e00003e00003e00003f00003f00003f00003f00001f80001fc0180ff0780ffff807fff803fff800ffe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        68: '25:27:000000000000000000000000000000000000000000000000000000001ffc00001fffc0001fffe0001ffff0001ffff8001f83fc001f81fe001f80fe001f807e001f807f001f803f001f803f001f803f001f803f001f803f001f807f001f807e001f807e001f80fe001f83fc001ffffc001ffff8001ffff0001fffc0001ffe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        69: '21:23:0000000000000000000000000000000000000000001fffc01fffc01fffc01fffc01fffc01f80001f80001f80001f80001f80001fffc01fffc01fffc01fffc01f80001f80001f80001f80001f80001f80001fffe01fffe01fffe01fffe01fffe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        70: '21:23:0000000000000000000000000000000000000000001fffc01fffc01fffc01fffc01fffc01f80001f80001f80001f80001f80001fffc01fffc01fffc01fffc01f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        71: '25:27:000000000000000000000000000000000000000000000000007fe00001fffc0003fffc0007fffc000ff8fc001fc00c001f8000003f8000003f0000003f0000003f0000003e03fe003e03fe003e03fe003f03fe003f03fe003f007e003f007e001f807e001fc07e000ff07e000ffffe0007fffe0003fffc0000fff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        72: '26:28:000000000000000000000000000000000000000000000000000000001f807e001f807e001f807e001f807e001f807e001f807e001f807e001f807e001f807e001f807e001ffffe001ffffe001ffffe001ffffe001f807e001f807e001f807e001f807e001f807e001f807e001f807e001f807e001f807e001f807e001f807e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        73: '11:13:00000000000000000000000000001f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f8000000000000000000000000000000000000000000000000000000000000000000000',
        74: '11:13:00000000000000000000000000001f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f003f007f00ff00fe00fc00f800c0000000000000000000000000000000000000000000',
        75: '24:26:000000000000000000000000000000000000000000000000000000001f807e001f80fc001f81f8001f83f8001f87f0001f8fe0001f9fc0001fbf80001fff00001ffe00001ffc00001ff800001ff800001ffc00001ffe00001fff00001fbf80001f9fc0001f8fe0001f8ff0001f87f8001f83f8001f81fc001f80fe001f807f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        76: '19:21:0000000000000000000000000000000000000000001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001fffe01fffe01fffe01fffe01fffe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        77: '30:32:000000000000000000000000000000000000000000000000000000001fc00ff01fe00ff01fe01ff01fe01ff01ff01ff01ff03ff01ff83ff01ff87ff01f787ff01f7c7bf01f3cfbf01f3cf3f01f3ef3f01f1ff3f01f1fe3f01f0fe3f01f0fc3f01f0fc3f01f07c3f01f0783f01f0003f01f0003f01f0003f01f0003f01f0003f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        78: '26:28:000000000000000000000000000000000000000000000000000000001f807e001fc07e001fc07e001fe07e001fe07e001ff07e001ff07e001ff87e001ff87e001f7c7e001f7c7e001f3e7e001f3e7e001f1f7e001f1f7e001f0ffe001f0ffe001f07fe001f07fe001f03fe001f03fe001f01fe001f01fe001f00fe001f00fe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        79: '26:28:00000000000000000000000000000000000000000000000000ffc00001ffe00007fff8000ffffc000ff3fc001fc0fe001f807e003f003f003f003f003f003f003f003f003e003f003e001f003e001f003f003f003f003f003f003f003f003f003f807f001fc0fe001fe1fe000ffffc0007fff80003fff00000ffc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        80: '22:24:0000000000000000000000000000000000000000001ffe001fffc01fffe01ffff01ffff01f83f81f81f81f81f81f81f81f81f81f81f81f87f81ffff01ffff01fffe01fff801f80001f80001f80001f80001f80001f80001f80001f80001f8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        81: '26:28:00000000000000000000000000000000000000000000000000ffc00001fff00007fff8000ffffc000ff3fc001fc0fe001f807e003f003f003f003f003f003f003f003f003e003f003e001f003e001f003f003f003f003f003f003f003f003f003f807e001fc0fe001fe1fc000ffffc0007fff80003fff00000ffc0000003e0000003f0000001f8000000fc0000007c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        82: '24:26:000000000000000000000000000000000000000000000000000000001ffe00001fffc0001fffe0001fffe0001ffff0001f87f0001f83f0001f83f0001f83f0001f83f0001f87e0001fffe0001fffc0001fff00001fffc0001fffe0001f87e0001f87f0001f83f0001f83f8001f81f8001f81f8001f80fc001f80fc001f807e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        83: '22:24:00000000000000000000000000000000000003ff8007ffc00fffc01fffc01fc7c03f00403e00003e00003f00003fe0001ffe001fff800fffc007ffe000ffe0000ff00003f00003f02003f03803f03f07e03fffe03fffc03fffc007ff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        84: '21:23:000000000000000000000000000000000000000000fffff8fffff8fffff8fffff8fffff800f80000f80000f80000f80000f80000f80000f80000f80000f80000f80000f80000f80000f80000f80000f80000f80000f80000f80000f80000f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        85: '25:27:000000000000000000000000000000000000000000000000000000001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001fc1f8000fe3f8000ffff80007fff00003ffe00001ff80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        86: '24:26:00000000000000000000000000000000000000000000000000000000fc003e007c007e007e007e007e007c003e00fc003f00fc003f00f8001f01f8001f81f8001f81f0000f83f0000fc3f0000fc3e00007c7e00007e7e00007e7c00003efc00003ffc00003ff800001ff800001ff800001ff000000ff000000ff000000fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        87: '34:36:00000000000000000000000000000000000000000000000000000000000000000000007c03f01f807e03f01f807e03f01f003e07f01f003e07f83f003f07f83f003f07f83e003f07f83e001f0f783e001f0f3c7e001f8f3c7e001f8f3c7c000f9f3c7c000f9e3cfc000f9e1efc000fde1efc000fde1ef80007fc1ef80007fc0ff80007fc0ff80007fc0ff80007fc0ff00003f80ff00003f807f00003f807f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        88: '24:26:000000000000000000000000000000000000000000000000000000007e00fe003f00fc003f01f8001f81f8001fc3f0000fc7e00007e7e00007efc00003ffc00001ff800001ff000000ff000000fe000000ff000001ff800003ff800003ffc00007efc00007e7e0000fc3f0001f83f0001f81f8003f01f8007f00fc007e007e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        89: '22:24:000000000000000000000000000000000000000000f801f8fc03f8fc03f07e07f07e07e03f0fc03f8fc01f9f800fff800fff0007fe0007fe0003fc0001fc0001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        90: '22:24:0000000000000000000000000000000000000000003ffff03ffff03ffff03ffff03ffff00007e0000fe0000fc0001f80003f00007f00007e0000fc0001f80003f80003f00007e0000fe0001fc0001f80003ffff87ffff87ffff87ffff87ffff8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        91: '14:16:0000000000000000000000001ff01ff01ff01ff01f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001ff01ff01ff00000000000000000000000000000000000000000000000000000',
        92: '11:13:0000000000000000000000000000e000f0007000700078007800380038003c001c001c001c001e000e000e000f0007000700070007800380038003c001c001c001c001e000e000000000000000000000000000000000000000000000000000000000',
        93: '14:16:0000000000000000000000003fe03fe03fe03fe003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e03fe03fe03fe00000000000000000000000000000000000000000000000000000',
        94: '26:28:00000000000000000000000000000000000000000000000000000000001e0000003f0000007f800000ff800001ffc00003f3e00003c1f000078078000f003c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        95: '15:17:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000fffe00fffe00fffe00000000000000000000000000000000000000000000000000000000',
        96: '15:17:0000000000000000000000003c00001e00000e0000070000038000038000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        97: '21:23:0000000000000000000000000000000000000000000000000000000000000000000000000ffc001fff001fff801fff80180fc00007c00007c003ffc01fffc03fffc03fffc03e07c07e07c07e0fc07e0fc03fbfc03fffc01ff7c00fe7c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        98: '22:24:0000000000000000000000000000000000001f00001f00001f00001f00001f00001f00001f00001f1f001f7f801fffc01fffe01fc7f01f83f01f01f01f01f01f01f01f01f81f01f81f01f01f01f01f83f01fc7f01fffe01fffe01f7fc01f3f80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        99: '18:20:00000000000000000000000000000000000000000000000000000000000000000000000001fe0007ff000fff001fff003fc3003f00003f00007e00007e00007e00007e00007e00003e00003f00003f81001fff001fff000fff0003ff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        100: '22:24:0000000000000000000000000000000000000003e00003e00003e00003e00003e00003e00003e003e3e00ffbe01fffe01fffe03f8fe03f07e03e07e03e03e07e03e07e03e07e03e07e03e03e03e03f07e03f0fe01fffe01fffe00ffbe007f3e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        101: '21:23:00000000000000000000000000000000000000000000000000000000000000000000000001fc0007ff000fff801fffc03f0fc03f07e03e03e07e03e07fffe07fffe07fffe07e00003e00003e00003f00c01fefc01fffc00fffc003ff80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        102: '13:15:00000000000000000000000001fc07fc0ffc0ffc1f801f801f807ff87ff87ff87ff87ff81f801f801f801f801f801f801f801f801f801f801f801f801f801f8000000000000000000000000000000000000000000000000000000000000000000000',
        103: '22:24:00000000000000000000000000000000000000000000000000000000000000000000000003e3e00ffbe01ffbe01fffe03f8fe03f07e03e07e07e03e07e03e07e03e07e03e07e03e03e07e03f07e03f8fe01fffe01fffe00ffbe003e3e00003e00007e0180fe01fffc01fff801fff000ffc00000000000000000000000000000000000000000000000000000000000000000000',
        104: '22:24:0000000000000000000000000000000000001f00001f00001f00001f00001f00001f00001f00001f1f001f7fc01fffc01fffe01fefe01f87e01f83e01f03e01f03e01f03e01f03e01f03e01f03e01f03e01f03e01f03e01f03e01f03e01f03e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        105: '10:12:0000000000000000000000001f001f001f001f001f00000000001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f0000000000000000000000000000000000000000000000000000000000000000000000',
        106: '10:12:0000000000000000000000003e003e003e003e003e00000000003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e007e007e00fc00fc00f800f0000000000000000000000000000000000000000000',
        107: '20:22:0000000000000000000000000000000000001f00001f00001f00001f00001f00001f00001f00001f03f01f07e01f0fc01f1f801f3f001f7e001f7c001ffc001ff8001ff8001ffc001ffc001f7e001f3f001f1f801f1fc01f0fe01f07f01f03f8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        108: '10:12:0000000000000000000000001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f0000000000000000000000000000000000000000000000000000000000000000000000',
        109: '32:34:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001f1e07c0001f7f8ff0001fffdff0001ffffff8001fcffbf8001f87f0f8001f07e0f8001f07e0f8001f07e0f8001f07e0f8001f07e0f8001f07e0f8001f07e0f8001f07e0f8001f07e0f8001f07e0f8001f07e0f8001f07e0f8001f07e0f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        110: '22:24:0000000000000000000000000000000000000000000000000000000000000000000000001f1f001f7fc01fffc01fffe01fefe01f87e01f83e01f03e01f03e01f03e01f03e01f03e01f03e01f03e01f03e01f03e01f03e01f03e01f03e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        111: '21:23:00000000000000000000000000000000000000000000000000000000000000000000000001fc0007ff000fff801fffc03f8fe03f07e03e03e07e03f07e03f07e03f07e03f07e03f03e03e03f07e03f07e01fffc01fffc00fff8003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        112: '22:24:0000000000000000000000000000000000000000000000000000000000000000000000001f1f001f7f801fffc01fffe01fc7f01f83f01f01f01f01f01f01f01f01f81f01f81f01f01f01f01f83f01fc7f01fffe01fffe01f7fc01f3f801f00001f00001f00001f00001f00001f00001f0000000000000000000000000000000000000000000000000000000000000000000000',
        113: '22:24:00000000000000000000000000000000000000000000000000000000000000000000000003e3e00ffbe00ffbe01fffe03f8fe03f07e03e07e03e03e07e03e07e03e07e03e07e03e03e03e03f07e03f0fe01fffe01fffe00ffbe007f3e00003e00003e00003e00003e00003e00003e00003e0000000000000000000000000000000000000000000000000000000000000000000',
        114: '15:17:0000000000000000000000000000000000000000000000000000000000000000000000001f1e001f7e001f7e001ffe001ffe001fc0001f80001f00001f00001f00001f00001f00001f00001f00001f00001f00001f00001f00001f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        115: '18:20:00000000000000000000000000000000000000000000000000000000000000000000000007fc001fff003fff003fff003e07003c00003e00003fc0003ffc001ffe000fff0001ff80001f80000f80201f803f7f003fff003ffe003ffc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        116: '15:17:0000000000000000000000000000000000000000000000001f00001f00001f00001f00001f0000fffc00fffc00fffc00fffc00fffc001f00001f00001f00001f00001f00001f00001f00001f00001f80001f80001ff8000ff8000ff80003f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        117: '22:24:0000000000000000000000000000000000000000000000000000000000000000000000000000003f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f07e03f07e01f8fe01fffe01fffe00ffbe007f3e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        118: '20:22:000000000000000000000000000000000000000000000000000000000000000000000000000000fc03e07c03e07c07e03e07c03e07c03e0fc01f0f801f0f801f0f800f9f000f9f000f9f0007fe0007fe0007fe0003fc0003fc0001f80001f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        119: '28:30:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007c0f03e07e0f83e03e1f83e03e1f87c03e1f87c03e1fc7c01f1fc7c01f3fcfc01f3dcf801f39cf801f39ef800ff9ef800ff8ff000ff8ff000ff0ff0007f0ff0007f0fe0007f07e0007e07e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        120: '20:22:0000000000000000000000000000000000000000000000000000000000000000000000000000007c07e07e07c03f0fc01f1f801f9f000fff0007fe0007fc0003fc0001f80003fc0007fc0007fe000fff001f9f001f1f803f0fc07e07c07c07e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        121: '20:22:000000000000000000000000000000000000000000000000000000000000000000000000000000fc03e07c03e07c07e03e07c03e07c03f0fc01f0f801f0f801f8f800f9f000f9f0007df0007fe0007fe0003fe0003fc0001fc0001fc0001f80000f80000f00001f0001ff0001fe0001fc0001f8000000000000000000000000000000000000000000000000000000000000000',
        122: '18:20:0000000000000000000000000000000000000000000000000000000000000000000000000000003fff003fff003fff003fff003fff00007f00007e0000fc0001f80003f00007e0000fc0001f80001f80003f00007fff007fff007fff007fff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        123: '22:24:000000000000000000000000000000000000000fc0003fc0007fc0007fc0007c0000fc0000fc0000fc0000fc0000fc0000fc0000fc0000f80001f8000ff8000fe0000ff0000ff80001f80000f80000fc0000fc0000fc0000fc0000fc0000fc0000fc00007e00007fc0007fc0003fc00007c0000000000000000000000000000000000000000000000000000000000000000000',
        124: '11:13:0000000000000000000000000e000e000e000e000e000e000e000e000e000e000e000e000e000e000e000e000e000e000e000e000e000e000e000e000e000e000e000e000e000e000e000e000e000e00000000000000000000000000000000000000',
        125: '22:24:0000000000000000000000000000000000000fc0000ff0000ff8000ff80001f80000f80000f80000f80000f80000f80000f80000f80000fc00007e00007fc0003fc0003fc0007fc000fc0000fc0000f80000f80000f80000f80000f80000f80000f80001f8000ff8000ff0000fe0000f0000000000000000000000000000000000000000000000000000000000000000000000',
        126: '26:28:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001e0040007f80c000fffbc001ffffc001e1ffc001807f0001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        160: '11:13:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        161: '14:16:00000000000000000000000000000000000000000000000000000fc00fc00fc00fc00fc00fc0000000000000078007800780078007800fc00fc00fc00fc00fc00fc00fc00fc00fc00fc00fc000000000000000000000000000000000000000000000',
        162: '21:23:00000000000000000000000000000000000000000000000000380000380000380000380000380000ff0003ff8007ff800fff800ff9801ff8001fb8001f38001f38001f38001f38001f38001fb8001fb8000ff8800fff8007ff8003ff8001ff80003800003800003800003800003800000000000000000000000000000000000000000000000000000000000000000000000000',
        163: '21:23:000000000000000000000000000000000000007fc001ffe001ffe003ffe003f06007e00007e00007e00007e00007e00007e0003fff003fff003fff003fff0007e00007e00007e00007e00007e00007e0003fffe03fffe03fffe03fffe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        164: '19:21:0000000000000000000000000000000000000000000000000000000000000000001001803801c07ce3c03fff801fff000fff000f0f000e07001e07001c07001e07000e0f000f1e000fff001fff803fffc07c03c0380180100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        165: '21:23:0000000000000000000000000000000000000000007e01f87e03f03f03f03f07e01f87e01f8fc00fdf800fdf8007ff007ffff07ffff07ffff001fc0000fc0000fc007ffff07ffff07ffff000fc0000fc0000fc0000fc0000fc0000fc0000fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        166: '11:13:000000000000000000000000000000000e000e000e000e000e000e000e000e000e000e000e000e000e0000000000000000000e000e000e000e000e000e000e000e000e000e000e000e000e0000000000000000000000000000000000000000000000',
        167: '15:17:0000000000000000000000000000000000000ff8001ff8003ff8003e38007c00007e00003f00003fc0001ff0003ff8007ffc0078fe00f83e00f01e00f81e00fc1e007e3e007ffc003ff8000ff00003f80000fc00007c00007c0038fc003ff8003ff8003fe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        168: '15:17:0000000000000000000000000000001c70001c70001c70001c7000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        169: '31:33:00000000000000000000000000000000000000000000000000000000000000000000000007800000001ff00000007ffc000000f03e000001e00f00000380070000030ff38000071ff18000063ff1c000063c10c0000e7800c0000e7800c0000c7800c0000e7800c0000e7800c0000e7c00c000063e31c000071ff18000070ff380000383c3800001c007000000f01e0000007ffc0000003ff80000000fc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        170: '17:19:0000000000000000000000000000000000000ff0001ffc001ffc00101e00001e0007fe001ffe001e1e003c1e003c3e003e7e001ffe000fde000000000000001ffe001ffe001ffe001ffe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        171: '20:22:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c08001c38003c78007cf800f1f003e3c003c38003c38003e3c001f1e0007cf8003c78001c38000c180004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        172: '26:28:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001ffffc001ffffc001ffffc001ffffc0000001c0000001c0000001c0000001c0000001c0000001c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        173: '1:3:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        174: '31:33:00000000000000000000000000000000000000000000000000000000000000000000000007800000001ff00000007ffc000000f03e000001e00f00000380070000031fe38000071ff18000061cf1c000061c70c0000e1cf0c0000e1ff0c0000c1fe0c0000e1fc0c0000e1de0c0000e1ce0c000061cf1c000071c718000071c7b8000038003800001c007000000f01e0000007ffc0000003ff80000000fc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        175: '15:17:0000000000000000000000000000000000001ff0001ff0001ff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        176: '15:17:00000000000000000000000000000000000007c0000fe0001e70001c30001838001838001830001c70000ff00007e000018000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        177: '26:28:00000000000000000000000000000000000000000000000000000000000000000000000000000000001e0000001e0000001e0000001e0000001e0000001e00001ffffc001ffffc001ffffc00001e0000001e0000001e0000001e0000001e0000001e000000000000000000001ffffc001ffffc001ffffc001ffffc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        178: '13:15:0000000000000000000000003fc03fe031e000f000f000e001e003c007800f001e003ff03ff03ff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        179: '13:15:0000000000000000000000003fc03fe031e000e000e00fe00f800fe000f000f000f071e07fe03fc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        180: '15:17:00000000000000000000000000780000700000f00001e00003c000038000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        181: '23:25:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001f03e0001f03e0001f03e0001f03e0001f03e0001f03e0001f03e0001f03e0001f03e0001f03e0001f03e0001f03e0001f03e0001f03e0001f87f0001ffffc001ffffc001ffffc001ffcfc001f0000001f0000001f0000001f0000001f0000001f0000001f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        182: '19:21:00000000000000000000000000000000000000000001ff8007ff800fff801fe3803fe3803fe3803fe3803fe3803fe3803fe3801fe3801fe3800fe38003e38000e38000e38000e38000e38000e38000e38000e38000e38000e38000e38000e38000e38000e38000e380000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        183: '12:14:00000000000000000000000000000000000000000000000000000000000000001f801f801f801f801f801f80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        184: '15:17:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001800000c00000e00000e0000fe0000fc000078000000000000000000000000000000000000000000000000000000000000000',
        185: '13:15:00000000000000000000000000001f803f803f80078007800780078007800780078007803ff03ff03ff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        186: '17:19:00000000000000000000000000000000000007f0000ffc001ffc003e3e003c1e003c1e003c1f003c1e003c1e003e1e001f7c001ffc0007f0000000000000003ffe003ffe003ffe003ffe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        187: '20:22:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001020001838001e3c001f3e000f9f0007c78001c38001c38007c7800f9f001f3e001e3c001c3800103000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        188: '32:34:0000000000000000000000000000000000000000000000000000000000001f800780003f800700003f800f000007800e000007801e000007801c000007803c00000780380000078070000007807000000780e000003ff1e1e0003ff1c3e0003ff3c3e000000387e00000078ee00000070ce000000f1ce000000e38e000001e30e000001c3ff80000383ff800003800e000007000e00000f000e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        189: '32:34:0000000000000000000000000000000000000000000000000000000000001f800780003f800700003f800f000007800e000007801e000007801c000007803c00000780380000078070000007807000000780e000003ff1e7f8003ff1c7fc003ff3c63c000003801e000007801e000007001c00000f003c00000e007800001e00f000001c01e000003803c000003807fe00007007fe0000f007fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        190: '32:34:0000000000000000000000000000000000000000000000000000000000003fc00780003fe007000031e00f000000e00e000000e01e00000fe01c00000f803c00000fe038000000f070000000f070000000f0e0000071e1e1e0007fe1c3e0003fc3c3e000000387e00000078ee00000070ce000000f1ce000000e38e000001e30e000001c3ff80000383ff800003800e000007000e00000f000e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        191: '18:20:00000000000000000000000000000000000000000000000000000000000000000000000000000001f80001f80001f80001f80001f80001f80000000000000000000001f80001f80001f00003f00007e0000fc0001f80001f00003f00003f00003f01003f07003fff001fff001fff0007fe0001e000000000000000000000000000000000000000000000000000000000000000',
        192: '24:26:01e0000000f000000078000000380000000000000000000000fe000000ff000000ff000001ff000001ff800001ff800003ff800003efc00003e7c00007e7c00007c7e00007c3e0000fc3e0000fc3f0000f83f0001f81f0001ffff8001ffff8003ffff8003ffffc003e00fc007e007c007e007e007c007e00fc003e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        193: '24:26:000f0000001e0000003c000000380000000000000000000000fe000000ff000000ff000001ff000001ff800001ff800003ff800003efc00003e7c00007e7c00007c7e00007c3e0000fc3e0000fc3f0000f83f0001f81f0001ffff8001ffff8003ffff8003ffffc003e00fc007e007c007e007e007c007e00fc003e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        194: '24:26:00fc000000fe000001c7000003838000000000000000000000fe000000ff000000ff000001ff000001ff800001ff800003ff800003efc00003e7c00007e7c00007c7e00007c3e0000fc3e0000fc3f0000f83f0001f81f0001ffff8001ffff8003ffff8003ffffc003e00fc007e007c007e007e007c007e00fc003e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        195: '24:26:01e3800001fb000003bf0000030e0000000000000000000000fe000000ff000000ff000001ff000001ff800001ff800003ff800003efc00003e7c00007e7c00007c7e00007c3e0000fc3e0000fc3f0000f83f0001f81f0001ffff8001ffff8003ffff8003ffffc003e00fc007e007c007e007e007c007e00fc003e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        196: '24:26:01c7000001c7000001c7000001c70000000000000000000000fe000000ff000000ff000001ff000001ff800001ff800003ff800003efc00003e7c00007e7c00007c7e00007c3e0000fc3e0000fc3f0000f83f0001f81f0001ffff8001ffff8003ffff8003ffffc003e00fc007e007c007e007e007c007e00fc003e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        197: '24:26:00180000007e000000fe000000e7000000c3000000c3000000c7000000ff000000ff000000ff000001ff000001ff800001ff800003ff800003efc00003e7c00007e7c00007c7e00007c3e0000fc3e0000fc3f0000f83f0001f81f0001ffff8001ffff8003ffff8003ffffc003e00fc007e007c007e007e007c007e00fc003e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        198: '33:35:0000000000000000000000000000000000000000000000000000000000000000000000007ffffe00007ffffe0000fffffe0000fffffe0000f9fffe0001f9f8000001f9f8000001f1f8000003f1f8000003e1f8000007e1fffc0007e1fffc0007c1fffc000fc1fffc000fc1f800000ffff800001ffff800001ffff800003ffff800003f01f800003e01fffe007e01fffe007e01fffe007c01fffe00fc01fffe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        199: '22:24:000000000000000000000000000000000000007fc001fff003fff807fff80ff9f81fc0381f80083f80003f00003f00003f00003e00003e00003e00003f00003f00003f00003f00001f80001fc0180ff0780ffff807fff803fff800ffe0000600000300000380000380003f80003f00001e00000000000000000000000000000000000000000000000000000000000000000000',
        200: '21:23:03c00001e00000f0000070000000000000001fffc01fffc01fffc01fffc01fffc01f80001f80001f80001f80001f80001fffc01fffc01fffc01fffc01f80001f80001f80001f80001f80001f80001fffe01fffe01fffe01fffe01fffe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        201: '21:23:001e00003c000078000070000000000000001fffc01fffc01fffc01fffc01fffc01f80001f80001f80001f80001f80001fffc01fffc01fffc01fffc01f80001f80001f80001f80001f80001f80001fffe01fffe01fffe01fffe01fffe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        202: '21:23:01f80001fc00038e000707000000000000001fffc01fffc01fffc01fffc01fffc01f80001f80001f80001f80001f80001fffc01fffc01fffc01fffc01f80001f80001f80001f80001f80001f80001fffe01fffe01fffe01fffe01fffe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        203: '21:23:038e00038e00038e00038e000000000000001fffc01fffc01fffc01fffc01fffc01f80001f80001f80001f80001f80001fffc01fffc01fffc01fffc01f80001f80001f80001f80001f80001f80001fffe01fffe01fffe01fffe01fffe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        204: '11:13:78003c001e000e00000000001f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f80000000000000000000000000000000000000000000000000000000000000000000000000',
        205: '11:13:03c007800f000e00000000001f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f80000000000000000000000000000000000000000000000000000000000000000000000000',
        206: '11:13:7e007f00e380c1c0000000003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f00000000000000000000000000000000000000000000000000000000000000000000000000',
        207: '11:13:71c071c071c071c0000000001f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f80000000000000000000000000000000000000000000000000000000000000000000000000',
        208: '26:28:000000000000000000000000000000000000000000000000000000001ffc00001fffc0001ffff0001ffff8001ffffc001f83fc001f80fe001f807e001f807f001f803f00fff03f00fff03f00fff03f00fff03f00fff03f001f803f001f807f001f807e001f80fe001f83fc001ffffc001ffff8001ffff0001fffc0001ffe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        209: '26:28:00f1c00000fd800001df80000187000000000000000000001f807e001fc07e001fc07e001fe07e001fe07e001ff07e001ff07e001ff87e001ff87e001f7c7e001f7c7e001f3e7e001f3e7e001f1f7e001f1f7e001f0ffe001f0ffe001f07fe001f07fe001f03fe001f03fe001f01fe001f01fe001f00fe001f00fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        210: '26:28:00f0000000780000003c0000001c0000000000000000000000ffc00001ffe00007fff8000ffffc000ff3fc001fc0fe001f807e003f003f003f003f003f003f003f003f003e003f003e001f003e001f003f003f003f003f003f003f003f003f003f807f001fc0fe001fe1fe000ffffc0007fff80003fff00000ffc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        211: '26:28:00078000000f0000001e0000001c0000000000000000000000ffc00001ffe00007fff8000ffffc000ff3fc001fc0fe001f807e003f003f003f003f003f003f003f003f003e003f003e001f003e001f003f003f003f003f003f003f003f003f003f807f001fc0fe001fe1fe000ffffc0007fff80003fff00000ffc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        212: '26:28:007e0000007f000000e3800001c1c000000000000000000000ffc00001ffe00007fff8000ffffc000ff3fc001fc0fe001f807e003f003f003f003f003f003f003f003f003e003f003e001f003e001f003f003f003f003f003f003f003f003f003f807f001fc0fe001fe1fe000ffffc0007fff80003fff00000ffc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        213: '26:28:0078e000007ec00000efc00000c38000000000000000000000ffc00001ffe00007fff8000ffffc000ff3fc001fc0fe001f807e003f003f003f003f003f003f003f003f003e003f003e001f003e001f003f003f003f003f003f003f003f003f003f807f001fc0fe001fe1fe000ffffc0007fff80003fff00000ffc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        214: '26:28:0071c0000071c0000071c0000071c000000000000000000000ffc00001ffe00007fff8000ffffc000ff3fc001fc0fe001f807e003f003f003f003f003f003f003f003f003e003f003e001f003e001f003f003f003f003f003f003f003f003f003f807f001fc0fe001fe1fe000ffffc0007fff80003fff00000ffc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        215: '26:28:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060030000f0078000f80fc0007c0f80003e1f00001f3e00000ffc000007f8000003f0000003e0000007f000000ff800001ffc00001f3e00003e1f00007c0f8000f807c000700380002001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        216: '26:28:00000000000000000000000000000000000000000000010000ff838001ffe78007ffff000ffffe000ff3fc001fc0fe001f807e003f00ff003f01ff003f03bf003f07bf003e0f3f003e1e1f003e3c1f003f383f003f703f003fe03f003fc03f003f807f001fc0fe001fe1fe001ffffc003ffff8007bfff00070ffc000200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        217: '25:27:00f0000000780000003c0000001c000000000000000000001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001fc1f8000fe3f8000ffff80007fff00003ffe00001ff8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        218: '25:27:00078000000f0000001e0000001c000000000000000000001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001fc1f8000fe3f8000ffff80007fff00003ffe00001ff8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        219: '25:27:007e0000007f000000e3800001c1c00000000000000000001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001fc1f8000fe3f8000ffff80007fff00003ffe00001ff8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        220: '25:27:00e3800000e3800000e3800000e3800000000000000000001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001f80fc001fc1f8000fe3f8000ffff80007fff00003ffe00001ff8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        221: '22:24:003c0000780000f00000e000000000000000f801f8fc03f8fc03f07e07f07e07e03f0fc03f8fc01f9f800fff800fff0007fe0007fe0003fc0001fc0001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        222: '23:25:000000000000000000000000000000000000000000000000000000001f8000001f8000001f8000001f8000001f8000001fff80001fffe0001ffff0001ffff0001f83f8001f81f8001f81f8001f81f8001f81f8001f81f8001f83f8001ffff0001ffff0001fffe0001fffc0001ffe00001f8000001f8000001f8000001f8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        223: '22:24:00000000000000000000000000000000000000fc0007ff000fff801fffc01f87c01f07c01f03e01f07e01f1fe01f3e001f3c001f3c001f3e001f3f001f3fc01f3fe01f1ff01f07f01f03f81f01f81f01f81f01f81f37f01f3ff01f3fe01f3fc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        224: '21:23:00000000000000000000000007800003c00001c00000e0000070000070000000000000000ffc001fff001fff801fff80180fc00007c00007c003ffc01fffc03fffc03fffc03e07c07e07c07e0fc07e0fc03fbfc03fffc01ff7c00fe7c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        225: '21:23:000000000000000000000000000f00000e00001e00003c000078000070000000000000000ffc001fff001fff801fff80180fc00007c00007c003ffc01fffc03fffc03fffc03e07c07e07c07e0fc07e0fc03fbfc03fffc01ff7c00fe7c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        226: '21:23:00000000000000000000000000f80000fc0001fc0001ce00038e000707000000000000000ffc001fff001fff801fff80180fc00007c00007c003ffc01fffc03fffc03fffc03e07c07e07c07e0fc07e0fc03fbfc03fffc01ff7c00fe7c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        227: '21:23:00000000000000000000000000000003e30003f700037e00071e000000000000000000000ffc001fff001fff801fff80180fc00007c00007c003ffc01fffc03fffc03fffc03e07c07e07c07e0fc07e0fc03fbfc03fffc01ff7c00fe7c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        228: '21:23:000000000000000000000000000000038e00038e00038e00038e000000000000000000000ffc001fff001fff801fff80180fc00007c00007c003ffc01fffc03fffc03fffc03e07c07e07c07e0fc07e0fc03fbfc03fffc01ff7c00fe7c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        229: '21:23:00000000f80001fc0001de00038e00038600038e0001de0001fc0000f8000000000000000ffc001fff001fff801fff80180fc00007c00007c003ffc01fffc03fffc03fffc03e07c07e07c07e0fc07e0fc03fbfc03fffc01ff7c00fe7c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        230: '32:34:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ff81f80001ffe7fe0001ffffff0001ffffff800180ff0fc000007e07c000007c07c0003ffc07c001ffffffe003ffffffe003ffffffe003e07c000007e07c000007e0fe004007e0fe01c003fbffdfc003ffdfffc001ff8fffc000ff07ff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        231: '18:20:00000000000000000000000000000000000000000000000000000000000000000000000001fe0007ff000fff001fff003fc3003f00003f00007e00007e00007e00007e00007e00003e00003f00003f81001fff001fff000fff0003ff00003000001800001c00001c0001fc0001f80000f000000000000000000000000000000000000000000000000000000000000000000000',
        232: '21:23:00000000000000000000000007800003c00001c00000e00000700000700000000000000001fc0007ff000fff801fffc03f0fc03f07e03e03e07e03e07fffe07fffe07fffe07e00003e00003e00003f00c01fefc01fffc00fffc003ff80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        233: '21:23:000000000000000000000000000f00000e00001e00003c0000780000700000000000000001fc0007ff000fff801fffc03f0fc03f07e03e03e07e03e07fffe07fffe07fffe07e00003e00003e00003f00c01fefc01fffc00fffc003ff80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        234: '21:23:00000000000000000000000000f80000fc0001fc0001ce00038e0007070000000000000001fc0007ff000fff801fffc03f0fc03f07e03e03e07e03e07fffe07fffe07fffe07e00003e00003e00003f00c01fefc01fffc00fffc003ff80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        235: '21:23:000000000000000000000000000000038e00038e00038e00038e0000000000000000000001fc0007ff000fff801fffc03f0fc03f07e03e03e07e03e07fffe07fffe07fffe07e00003e00003e00003f00c01fefc01fffc00fffc003ff80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        236: '10:12:0000000000000000f000780038001c000e000e00000000001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f00000000000000000000000000000000000000000000000000000000000000000000000000',
        237: '10:12:000000000000000001e001c003c007800f000e00000000001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f00000000000000000000000000000000000000000000000000000000000000000000000000',
        238: '10:12:00000000000000001f001f803f8039c071c0e0e0000000001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f00000000000000000000000000000000000000000000000000000000000000000000000000',
        239: '10:12:0000000000000000000071c071c071c071c00000000000001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f001f00000000000000000000000000000000000000000000000000000000000000000000000000',
        240: '21:23:00000000000000000000000000000000000007e04003e3c001ffc000fe0007fc001ffe000c3e00001f00004f8007ffc00fffc01fffe03fffe03f07e03e03f07e03f07e03f07e03f07e03f03e03e03f07e03f07e01fffc01fffc00fff8003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        241: '22:24:00000000000000000000000000000001f18001fb8001bf00038f000000000000000000001f1f001f7fc01fffc01fffe01fefe01f87e01f83e01f03e01f03e01f03e01f03e01f03e01f03e01f03e01f03e01f03e01f03e01f03e01f03e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        242: '21:23:00000000000000000000000007800003c00001c00000e00000700000700000000000000001fc0007ff000fff801fffc03f8fe03f07e03e03e07e03f07e03f07e03f07e03f07e03f03e03e03f07e03f07e01fffc01fffc00fff8003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        243: '21:23:000000000000000000000000000f00000e00001e00003c0000780000700000000000000001fc0007ff000fff801fffc03f8fe03f07e03e03e07e03f07e03f07e03f07e03f07e03f03e03e03f07e03f07e01fffc01fffc00fff8003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        244: '21:23:00000000000000000000000000f80000fc0001fc0001ce00038e0007070000000000000001fc0007ff000fff801fffc03f8fe03f07e03e03e07e03f07e03f07e03f07e03f07e03f03e03e03f07e03f07e01fffc01fffc00fff8003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        245: '21:23:00000000000000000000000000000003e30003f700037e00071e0000000000000000000001fc0007ff000fff801fffc03f8fe03f07e03e03e07e03f07e03f07e03f07e03f07e03f03e03e03f07e03f07e01fffc01fffc00fff8003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        246: '21:23:000000000000000000000000000000038e00038e00038e00038e0000000000000000000001fc0007ff000fff801fffc03f8fe03f07e03e03e07e03f07e03f07e03f07e03f07e03f03e03e03f07e03f07e01fffc01fffc00fff8003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        247: '26:28:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001e0000001e0000001e0000001e0000001e000000000000000000001ffffc001ffffc001ffffc001ffffc000000000000000000001e0000001e0000001e0000001e0000001e0000001e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        248: '21:23:00000000000000000000000000000000000000000000000000000000000000000000002001fc7007ffe00fffc01fffc03f8fe03f0fe03e0fe07e1ff07e3bf07e73f07ee3f07fc3f03fc3e03f87e03f07e01fffc01fffc03fff803bfe00300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        249: '22:24:00000000000000000000000003c00001e00000e0000070000038000038000000000000003f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f07e03f07e01f8fe01fffe01fffe00ffbe007f3e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        250: '22:24:000000000000000000000000000780000700000f00001e00003c000038000000000000003f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f07e03f07e01f8fe01fffe01fffe00ffbe007f3e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        251: '22:24:00000000000000000000000000f80000fc0001fc0001ce00038e000707000000000000003f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f07e03f07e01f8fe01fffe01fffe00ffbe007f3e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        252: '22:24:000000000000000000000000000000038e00038e00038e00038e000000000000000000003f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f03e03f07e03f07e01f8fe01fffe01fffe00ffbe007f3e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        253: '20:22:000000000000000000000000001e00001c00003c0000780000f00000e000000000000000fc03e07c03e07c07e03e07c03e07c03f0fc01f0f801f0f801f8f800f9f000f9f0007df0007fe0007fe0003fe0003fc0001fc0001fc0001f80000f80000f00001f0001ff0001fe0001fc0001f8000000000000000000000000000000000000000000000000000000000000000000000',
        254: '22:24:0000000000000000000000000000000000001f00001f00001f00001f00001f00001f00001f00001f1f001f7f801fffc01fffe01fc7f01f83f01f01f01f01f01f01f01f01f81f01f81f01f01f01f01f83f01fc7f01fffe01fffe01f7fc01f3f801f00001f00001f00001f00001f00001f00001f0000000000000000000000000000000000000000000000000000000000000000',
        255: '20:22:000000000000000000000000000000071c00071c00071c00071c00000000000000000000fc03e07c03e07c07e03e07c03e07c03f0fc01f0f801f0f801f8f800f9f000f9f0007df0007fe0007fe0003fe0003fc0001fc0001fc0001f80000f80000f00001f0001ff0001fe0001fc0001f8000000000000000000000000000000000000000000000000000000000000000000000',
        8364: '21:23:000000000000000000000000000000000000007f8001ffe003ffe007ffe00ff0e00fc0201f80001f80007fff00ffff00ffff003f00003f00003f0000fffc00fffc00fff8001f80001f80000fc0200fe06007ffe003ffe001ffe000ffc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8211: '15:17:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003ffc003ffc003ffc003ffc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8212: '31:33:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003ffffff8003ffffff8003ffffff8003ffffff8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8222: '20:22:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f9f000f9f000f9f000f9f000f9f001f1f001f1e001e3e001c3c003c3800000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8220: '20:22:00000000000000000000000000000000000000000003c380038780078780078f000f8f001f1f001f1f001f1f001f1f001f1f001f1f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8221: '20:22:0000000000000000000000000000000000000000000f8f800f8f800f8f800f8f800f8f800f8f800f1f000f1e001e1e001e1c001c3c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8217: '12:14:00000000000000000000000000001f801f801f801f801f801f001f001e003c003c0038000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8226: '20:22:00000000000000000000000000000000000000000000000000000000000000000000000000000000600001f80003fc0007fe0007fe000ffe000ffe000ffe0007fe0007fc0003fc0001f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        338: '36:38:0000000000000000000000000000000000000000000000000000000000000000000000001fffff8000ffffff8003ffffff8007ffffff800fffffff801ff03e00001fc03e00003f803e00003f003e00003f003e00003f003fff803f003fff803e003fff803f003fff803f003e00003f003e00003f003e00003f803e00001fc03e00001ff03e00000fffffff8007ffffff8003ffffff8001ffffff80003fffff8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        339: '33:35:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001fc0fe00007ff3ff0000ffffffc001ffffffc003f8ff87e003f07f03e003e03f03f007e03f03f007e03ffff007e03ffff007e03ffff007e03f000003e03f000003f07f000003f07f806001fffff7e001ffffffe000fff3ffe0003fe1ff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        352: '22:24:070e00039e0001fc0000f80000000000000003ff8007ffc00fffc01fffc01fc7c03f00403e00003e00003f00003fe0001ffe001fff800fffc007ffe000ffe0000ff00003f00003f02003f03803f03f07e03fffe03fffc03fffc007ff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        353: '18:20:0000000000000000000000000e0e00071c0003bc0003f80001f00001f00000000000000007fc001fff003fff003fff003e07003c00003e00003fc0003ffc001ffe000fff0001ff80001f80000f80201f803f7f003fff003ffe003ffc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        381: '22:24:070e00039e0001fc0000f8000000000000003ffff03ffff03ffff03ffff03ffff00007e0000fe0000fc0001f80003f00007f00007e0000fc0001f80003f80003f00007e0000fe0001fc0001f80003ffff87ffff87ffff87ffff87ffff8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        382: '18:20:0000000000000000000000001c1c000e380007780007f00003e00003e0000000000000003fff003fff003fff003fff003fff00007f00007e0000fc0001f80003f00007e0000fc0001f80001f80003f00007fff007fff007fff007fff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
    },
    'd': {
        32: '13:15:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        33: '16:18:00000000000000000000000000000000000000000000000007e00007e00007e00007e00007e00007e00007e00007e00007e00007e00007e00007e00007e00007e00007e00003e00003e00003e00003e00000000000000000000007e00007e00007e00007e00007e00007e00007e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        34: '19:21:0000000000000000000000000000000000000000000000001f1e001f1e001f1e001f1e001f1e001f1e001f1e001f1e001f1e001f1e001f1e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        35: '30:32:000000000000000000000000000000000000000000000000000000000000000000000000000f0780000f0f00000f0f00001e0f00001e0f00001e1e00001e1e00003c1e000ffffff00ffffff00ffffff00ffffff000783c0000783c00007878000078780000f078003fffffc03fffffc03fffffc03fffffc03fffffc001e0f00001e1e00001e1e00003c1e00003c1e00003c1c00003c3c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        36: '25:27:00000000000000000000000000000000000000000000000000000000001c0000001c0000001c0000001c000000ff800003fff80007fff8000ffff8001ffff8001f9c18001f1c00001f1c00001f9c00001fdc00001fff00000fffe0000ffff00007fff80001fffc00001ffc00001cfc00001c7e00001c7e00101c7e001c1c7c001ffffc001ffff8001ffff8000fffe00001ff8000001c0000001c0000001c0000001c0000001c0000001c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        37: '36:38:0000000000000000000000000000000000000000000000000000000000000000000000000000000003c000f0000ff000f0001ff801e0003ffc01c0003c3e03c0007c3e0780007c1e0780007c1e0f00007c1e0f00007c1e1e00007c1e1e00003c3e3c00003e7c3c00001ffc7800001ff878000007f0f0fe000000e1ff800001e3ffc00003c3c7c00003c7c3e000078783e000078783e0000f0783e0000f0783e0001e0783e0001e07c3e0003c07c7c0003803ffc0007801ff8000f000ff0000f00018000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        38: '31:33:00000000000000000000000000000000000000000000000000000000000000000000000000000000000f800000007ff8000000fff8000001fff8000001fff8000003f838000003f008000003f000000003f800000003f800000001fc00000001fe00000003ff00000007ff01f8000fff81f0000fffc1f0001fdfe1f0001f8ff3f0003f07f3f0003f03ffe0003f01ffe0003f01ffc0003f80ffc0003f807f80001fc07f80001ffbffc0000fffffe00007fffff00003fff7f80001ffc3f800001c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        39: '11:13:000000000000000000000000000000001f001f001f001f001f001f001f001f001f001f001f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        40: '16:18:00000000000000000000000000000000000000000000f80001f80001f00003f00003e00003e00007e00007e0000fc0000fc0000fc0000fc0000f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80000fc0000fc0000fc0000fc00007e00007e00003e00003f00003f00001f00001f80000f800000000000000000000000000000000000000000000000000000000000000000000000000000000',
        41: '16:18:0000000000000000000000000000000000000000001f80000f80000fc00007c00007e00007e00003e00003f00003f00003f00001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f00003f00003f00003f00003e00007e00007c00007c0000fc0000f80001f8000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        42: '19:21:00000000000000000000000000000000000000000000000000e00000e00000e00000e00030e18078e7c07eefc01fff0007fc0003f80007fc001fff003eff807ce7c070e18000e08000e00000e00000e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        43: '30:32:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000780000007800000078000000780000007800000078000000780000007800000078000000780000fffffc00fffffc00fffffc00fffffc00fffffc000078000000780000007800000078000000780000007800000078000000780000007800000078000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        44: '14:16:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000fc00fc00fc00fc00fc00fc00fc01f801f801f001f003e003c003c0000000000000000000000000000000000000000000000',
        45: '15:17:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003ff8003ff8003ff8003ff8003ff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        46: '14:16:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000fc00fc00fc00fc00fc00fc00fc00fc000000000000000000000000000000000000000000000000000000000000000000000',
        47: '13:15:000000000000000000000000000000000078007800f000f000f000f001e001e001e001c003c003c003c007800780078007000f000f000f001e001e001e001e003c003c003c007800780078007800f000f00000000000000000000000000000000000000000000000000000000000',
        48: '25:27:0000000000000000000000000000000000000000000000000000000000000000003e000000ffc00003ffe00007fff0000ffff8000ff7f8001fc1fc001f80fc001f80fc003f80fe003f80fe003f80fe003f80fe003f807e003f807e003f807e003f807e003f807e003f80fe003f80fe003f80fe003f80fe001f80fc001fc1fc001fc1fc000ffff8000ffff80007fff00003ffe00000ff8000001c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        49: '25:27:000000000000000000000000000000000000000000000000000000000000000001ff80000fff80000fff80000fff80000fff80000f3f8000003f8000003f8000003f8000003f8000003f8000003f8000003f8000003f8000003f8000003f8000003f8000003f8000003f8000003f8000003f8000003f8000003f8000003f80000ffffe000ffffe000ffffe000ffffe000ffffe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        50: '25:27:0000000000000000000000000000000000000000000000000000000000000000007c00000fff80001fffe0001ffff0001ffff8001fdff8001c07f8001003fc000001fc000001fc000001fc000001f8000003f8000003f8000007f000000fe000001fc000003fc000007f000000fe000001fc000003f8000007f000000fe000001ffffc001ffffc001ffffc001ffffc001ffffc001ffffc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        51: '25:27:000000000000000000000000000000000000000000000000000000000000000000fc00000fffc0000fffe0000ffff0000ffff8000f9ff8000803f8000003fc000001fc000001f8000001f8000003f800001ff00001ffe00001ff800001ffe00001fff000001ff8000003fc000001fc000001fc000001fc000001fc002001fc003803fc003ffff8003ffff8003ffff0003fffe0001fff80000070000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        52: '25:27:0000000000000000000000000000000000000000000000000000000000000000000ff000001ff000001ff000003ff000007ff000007ff00000fff00001f7f00001f7f00003e7f00003e7f00007c7f0000f87f0000f87f0001f07f0001f07f0003e07f0003c07f0003ffffe003ffffe003ffffe003ffffe003ffffe003ffffe000007f0000007f0000007f0000007f0000007f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        53: '25:27:00000000000000000000000000000000000000000000000000000000000000000ffff8000ffff8000ffff8000ffff8000ffff8000f8000000f8000000f8000000f8000000f9c00000fffc0000fffe0000ffff0000ffff8000ffffc000c03fc000001fc000001fc000000fe000000fe000000fe000001fc001001fc001c03fc001ffff8001ffff8001ffff0001fffe00007ff8000003800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        54: '25:27:0000000000000000000000000000000000000000000000000000000000000000000f8000007ff80000fff80003fff80007fff80007fc78000fe008000fc000001fc000001f8000001f8000001f9fc0003ffff0003ffff8003ffffc003ffffc003fe1fe003fc0fe003fc0fe003fc07e001f807e001f807e001fc0fe001fc0fe000fc0fc000fe1fc0007fff80003fff80001ffe00000ffc000000c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        55: '25:27:00000000000000000000000000000000000000000000000000000000000000003ffffc003ffffc003ffffc003ffffc003ffffc000001fc000001f8000003f8000003f0000007f0000007f0000007e000000fe000000fc000001fc000001fc000003f8000003f8000003f0000007f0000007e000000fe000000fe000000fc000001fc000001f8000003f8000003f8000003f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        56: '25:27:0000000000000000000000000000000000000000000000000000000000000000003e000003ffe00007fff0000ffff8001ffffc001fe3fc001fc1fc001f80fc001f80fc001f80fc001fc1fc000fc1f8000ffff80003fff00001ffc00007fff0000ffff8001fc1fc001f80fc003f80fe003f80fe003f80fe003f80fe003f80fe003f80fc001fe3fc001ffffc000ffff80007fff00001ffc000001e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        57: '25:27:0000000000000000000000000000000000000000000000000000000000000000003c000001ff800007ffc0000fffe0000ffff0001fc3f8001f81f8003f81fc003f01fc003f01fc003f00fc003f01fe003f81fe003f81fe003fc3fe001ffffe001ffffe000ffffe0007fffe0001fcfc000000fc000000fc000001fc000001f8000803f8000f1ff0000fffe0000fffc0000fff80000fff00000060000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        58: '14:16:00000000000000000000000000000000000000000000000000000000000000000fc00fc00fc00fc00fc00fc00fc00fc00000000000000000000000000fc00fc00fc00fc00fc00fc00fc00fc000000000000000000000000000000000000000000000000000000000000000000000',
        59: '14:16:00000000000000000000000000000000000000000000000000000000000000000fc00fc00fc00fc00fc00fc00fc00fc00000000000000000000000000fc00fc00fc00fc00fc00fc00fc00fc00f801f801f001e001e003c0000000000000000000000000000000000000000000000',
        60: '30:32:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000040000001c000000fc000003fc00001ffc00007ff80003ffc0000fff00007ff80000ffe00000ff000000fc000000ff000000ffe000003ff800000fff000001ffe000007ff800000ffc000003fc0000007c0000001c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        61: '30:32:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000fffffc00fffffc00fffffc00fffffc000000000000000000000000000000000000000000fffffc00fffffc00fffffc00fffffc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        62: '30:32:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000080000000e0000000fc000000ff000000ffe000007ff800000fff000003ffc000007ff800000ffc000003fc0000007c000003fc00001ffc00007ff80003ffc0000fff00007ff80000ffe00000ff000000fc000000e00000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        63: '21:23:00000000000000000000000000000000000000000000000001f0000ffe003fff803fff803fffc03f3fc0380fc0200fe0000fe0000fc0000fc0001fc0003f80007f0000ff0001fe0001fc0003f80003f80003f00000000000000000000003f00003f00003f00003f00003f00003f00003f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        64: '36:38:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003fe0000000fff8000003fffe00000fffff00001fc01f80003f0007c0003c0003e000780001e000700000f000f03f387000e07fb87801e0fff83801c0f9f83801c1f0f83801c1e0783803c1e0783803c1e0783803c1e0783803c1e0783803c1e0787801c1e0787001c1f0f8f001c0f9fbe001e0ffffe000e07fbf8000f03f3e0000780000000078000000003e000200001f000e00001fc03f000007ffff000003fffc000000fff00000003fc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        65: '28:30:0000000000000000000000000000000000000000000000000000000000000000003fc000007fe000007fe000007fe00000fff00000fff00000fff00001fff80001f9f80001f9f80003f9fc0003f1fc0003f0fc0007f0fe0007f0fe0007e07e000fe07f000fe07f000fffff001fffff801fffff801fffff803fffffc03fffffc03f001fc07f000fe07f000fe07e000fe0fe0007f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        66: '27:29:00000000000000000000000000000000000000000000000000000000000000001fffe0001ffff8001ffffc001ffffe001ffffe001fc0ff001fc07f001fc07f001fc07f001fc07f001fc0fe001ffffe001ffffc001ffff8001ffffc001ffffe001fc0ff001fc07f001fc03f801fc03f801fc03f801fc03f801fc07f801fc0ff801fffff001fffff001ffffe001ffff8001fffe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        67: '26:28:00000000000000000000000000000000000000000000000000000000000000000007e000003ffc0000ffff0001ffff0003ffff0007ffff000ff807001ff001001fe000001fc000003fc000003f8000003f8000003f8000003f8000003f8000003f8000003f8000003f8000003f8000003fc000001fc000001fe000001ff003000ff80f0007ffff0003ffff0001ffff0000ffff00003ffc000003800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        68: '30:32:00000000000000000000000000000000000000000000000000000000000000001fffc0001ffff8001ffffe001fffff001fffff801fffffc01fc07fc01fc03fe01fc01fe01fc00fe01fc00ff01fc007f01fc007f01fc007f01fc007f01fc007f01fc007f01fc007f01fc00ff01fc00fe01fc01fe01fc03fe01fc07fc01fffff801fffff801fffff001ffffc001ffff8001fff8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        69: '25:27:00000000000000000000000000000000000000000000000000000000000000001ffffc001ffffc001ffffc001ffffc001ffffc001ffffc001fc000001fc000001fc000001fc000001fc000001ffff8001ffff8001ffff8001ffff8001ffff8001ffff8001fc000001fc000001fc000001fc000001fc000001fc000001ffffc001ffffc001ffffc001ffffc001ffffc001ffffc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        70: '25:27:00000000000000000000000000000000000000000000000000000000000000001ffffc001ffffc001ffffc001ffffc001ffffc001ffffc001fc000001fc000001fc000001fc000001fc000001ffff8001ffff8001ffff8001ffff8001ffff8001ffff8001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        71: '30:32:00000000000000000000000000000000000000000000000000000000000000000003f000003fff0000ffffc001ffffc003ffffc007ffffc00ff803c01ff000c01fe000001fc000003fc000003f8000003f8000003f8000003f80ffe03f80ffe03f80ffe03f80ffe03f80ffe03f800fe03fc00fe01fc00fe01fe00fe01ff00fe00ffc0fe007ffffe003ffffe001ffffe000ffffc0003ffe000003c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        72: '30:32:00000000000000000000000000000000000000000000000000000000000000001fc00fe01fc00fe01fc00fe01fc00fe01fc00fe01fc00fe01fc00fe01fc00fe01fc00fe01fc00fe01fc00fe01fffffe01fffffe01fffffe01fffffe01fffffe01fffffe01fc00fe01fc00fe01fc00fe01fc00fe01fc00fe01fc00fe01fc00fe01fc00fe01fc00fe01fc00fe01fc00fe01fc00fe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        73: '13:15:000000000000000000000000000000001fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc0000000000000000000000000000000000000000000000000000000000000000000000000',
        74: '13:15:000000000000000000000000000000003f803f803f803f803f803f803f803f803f803f803f803f803f803f803f803f803f803f803f803f803f803f803f803f803f803f803f803f803f803f807f80ff00ff00fe00fc00f800c0000000000000000000000000000000000000000000',
        75: '28:30:00000000000000000000000000000000000000000000000000000000000000001fc01fe01fc03fc01fc07f801fc0ff001fc0fe001fc1fe001fc3fc001fc7f8001fcff0001fdfe0001fffc0001fff80001fff00001ffe00001fff00001fff80001fffc0001fffe0001fdfe0001fcff0001fc7f8001fc3fc001fc1fe001fc0ff001fc0ff801fc07fc01fc03fe01fc01ff01fc00ff8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        76: '23:25:00000000000000000000000000000000000000000000000000000000000000001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc000001ffffc001ffffc001ffffc001ffffc001ffffc001ffffc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        77: '36:38:000000000000000000000000000000000000000000000000000000000000000000000000000000001ff000ff801ff801ff801ff801ff801ff803ff801ffc03ff801ffc03ff801ffc07ff801ffe07ff801ffe07ff801fff0fbf801fdf0fbf801fdf1fbf801fcf9f3f801fcf9f3f801fcffe3f801fc7fe3f801fc7fe3f801fc7fc3f801fc3fc3f801fc3fc3f801fc1f83f801fc1f83f801fc1f03f801fc0003f801fc0003f801fc0003f801fc0003f801fc0003f801fc0003f80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        78: '30:32:00000000000000000000000000000000000000000000000000000000000000001fe00fe01ff00fe01ff00fe01ff80fe01ff80fe01ffc0fe01ffc0fe01ffe0fe01ffe0fe01ffe0fe01fff0fe01fdf0fe01fdf8fe01fcf8fe01fcfcfe01fc7cfe01fc7efe01fc3efe01fc3ffe01fc1ffe01fc1ffe01fc0ffe01fc0ffe01fc07fe01fc07fe01fc03fe01fc03fe01fc01fe01fc01fe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        79: '31:33:000000000000000000000000000000000000000000000000000000000000000000000000000000000007c00000007ff8000001fffe000003ffff000007ffff80000fffffc0000ff03fe0001fe01fe0001fc00ff0001fc007f0003f8007f0003f8007f0003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8007f0003fc007f0001fc007f0001fc00ff0001fe01fe0000ff83fe00007ffffc00007ffff800003ffff000000fffe0000007ff8000000030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        80: '26:28:00000000000000000000000000000000000000000000000000000000000000001fffe0001ffff8001ffffc001ffffe001fffff001fc1ff001fc07f801fc03f801fc03f801fc03f801fc03f801fc07f801fc07f801fffff001fffff001ffffe001ffffc001ffff8001fffc0001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc000001fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        81: '31:33:000000000000000000000000000000000000000000000000000000000000000000000000000000000007c00000007ff8000001fffe000003ffff000007ffff80000fffffc0000ff03fe0001fe01fe0001fc00ff0001fc007f0003f8007f0003f8007f0003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8007f0003f8007f0001fc007f0001fc00ff0001fe01fe0000ff83fe00007ffffc00007ffff800003ffff000000fffe0000003ffc00000003fc000000007e000000003f000000003f800000001fc00000000fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        82: '28:30:00000000000000000000000000000000000000000000000000000000000000001fffe0001ffff8001ffffc001ffffe001ffffe001fc1fe001fc0ff001fc07f001fc07f001fc07f001fc07e001fc0fe001fc1fe001ffffc001ffff0001fffe0001ffff8001ffffc001fc3fc001fc1fe001fc0fe001fc0ff001fc07f001fc07f801fc03f801fc03f801fc01fc01fc01fc01fc00fe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        83: '26:28:0000000000000000000000000000000000000000000000000000000000000000003f000001fff80007fffc000ffffc000ffffc001ffffc001fc03c001f8004001f8000001f8000001f8000001fe000001fff00001fffe0000ffff00007fffc0003fffc00007ffe000007fe000001fe000000fe0000007e0000007e001800fe001f01fe001ffffe001ffffc001ffff8001ffff00003ffe000001c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        84: '25:27:0000000000000000000000000000000000000000000000000000000000000000ffffff00ffffff00ffffff00ffffff00ffffff00ffffff00007f0000007f0000007f0000007f0000007f0000007f0000007f0000007f0000007f0000007f0000007f0000007f0000007f0000007f0000007f0000007f0000007f0000007f0000007f0000007f0000007f0000007f0000007f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        85: '29:31:00000000000000000000000000000000000000000000000000000000000000001fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc00fe01fc00fe03f800ff07f8007ffff8007ffff0003fffe0001fffc00007ff000000780000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        86: '28:30:0000000000000000000000000000000000000000000000000000000000000000fe0007e07f000fe07f000fe07f000fc03f001fc03f801fc03f801f801f803f801fc03f801fc03f000fc07f000fe07f000fe07e0007e0fe0007f0fe0007f0fc0003f0fc0003f9fc0003f9f80001f9f80001fff80001fff00000fff00000fff00000ffe000007fe000007fe000007fc000003fc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        87: '40:42:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007f00fe00fc007f00fe00fc003f00ff00fc003f00ff01fc003f80ff01fc003f81ff01f8003f81ff81f8001f81ff81f8001f81ef83f8001fc1ef83f8001fc3e783f0000fc3e7c3f0000fc3e7c7f0000fc3c7c7f0000fe7c7c7e0000fe7c3c7e00007e7c3e7e00007e7c3efe00007f783efe00007ff81efc00007ff81ffc00003ff81ffc00003ff81ffc00003ff01ffc00003ff00ff800001ff00ff800001ff00ff800001fe00ff800001fe00ff8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        88: '28:30:00000000000000000000000000000000000000000000000000000000000000007f801fc03f801fc01fc03f801fc07f000fe07f000ff0fe0007f0fe0003f9fc0003fbf80001fff80000fff00000fff000007fe000007fc000003fc000007fe00000ffe00000fff00001fff80003fff80003f9fc0007f1fc0007f0fe000fe07f001fe07f001fc03f803f803fc03f801fc07f000fe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        89: '26:28:0000000000000000000000000000000000000000000000000000000000000000fc003f80fe007f00ff00ff007f00fe007f81fe003f81fc001fc3f8001fc3f8000fe7f0000ffff00007ffe00003ffe00003ffc00001ff800001ff800000ff0000007f0000007e0000007e0000007e0000007e0000007e0000007e0000007e0000007e0000007e0000007e0000007e0000007e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        90: '26:28:00000000000000000000000000000000000000000000000000000000000000003fffff003fffff003fffff003fffff003fffff003ffffe000001fe000003fc000007f8000007f000000ff000001fe000003fc000003f8000007f800000ff000000fe000001fc000003fc000007f8000007f000000fe000001fe000003fffff803fffff803fffff803fffff803fffff803fffff80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        91: '16:18:0000000000000000000000000000000000000000001ffc001ffc001ffc001ffc001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001ffc001ffc001ffc001ffc00000000000000000000000000000000000000000000000000000000000000000000000000000000',
        92: '13:15:00000000000000000000000000000000f000f00078007800780038003c003c003c001e001e001e000e000f000f000f00078007800780038003c003c003c001e001e001e001e000f000f000f000780078007800000000000000000000000000000000000000000000000000000000',
        93: '16:18:0000000000000000000000000000000000000000003ff8003ff8003ff8003ff80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f8003ff8003ff8003ff8003ff800000000000000000000000000000000000000000000000000000000000000000000000000000000',
        94: '30:32:0000000000000000000000000000000000000000000000000000000000000000000fc000000fe000001ff000003ff000007ff80000fcfc0001f87e0003f03f0003e00f80078007c00f0003c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        95: '18:20:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ffffc0ffffc0ffffc0000000000000000000000000000000000000000000000000',
        96: '18:20:0000000000000000000000000000000000003e00001f00000f000007800003c00003c00001e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        97: '24:26:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000fff80001fffe0001ffff0001ffff0001e07f8001003f8000001f8000001f80001fff8000ffff8001ffff8003ffff8003fc1f8003f01f8003f01f8003f01f8003f03f8003f87f8003ffff8001ffff8001ffdf80007f9f80001c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        98: '26:28:000000000000000000000000000000000000000000000000000000001f8000001f8000001f8000001f8000001f8000001f8000001f8000001f8000001f8fe0001f9ff8001fbffc001ffffc001ffffe001fe0fe001fc07f001fc07f001fc07f001f803f001f803f001f803f001f803f001fc07f001fc07f001fc07f001fe0fe001ffffe001ffffc001fbffc001f9ff8001f8ff000000180000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        99: '21:23:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ffc003ffe007ffe00fffe01fffe01fe0603f80003f80003f00003f00003f00003f00003f00003f00003f80003f80003fc0201ff9e00fffe007ffe003ffe001ffe0001e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        100: '26:28:000000000000000000000000000000000000000000000000000000000000fe000000fe000000fe000000fe000000fe000000fe000000fe000000fe0003fcfe0007fefe000ffffe001ffffe001ffffe001fc1fe003f81fe003f80fe003f00fe003f00fe003f00fe003f00fe003f00fe003f00fe003f80fe003f80fe003fc1fe001ffffe001ffffe000ffffe0007fefe0003fcfe00006000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        101: '24:26:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ff800003ffe00007fff0000ffff8001fe3f8001f81fc003f80fc003f00fc003f00fc003ffffe003ffffe003ffffe003ffffe003f0000003f0000003f8004003f801c001fe07c000ffffc000ffffc0003fffc0001ffe000001c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        102: '16:18:00000000000000000000000000000000000000000001ff0007ff0007ff000fff000fe0000fc0000fc0000fc0007ffe007ffe007ffe007ffe007ffe000fc0000fc0000fc0000fc0000fc0000fc0000fc0000fc0000fc0000fc0000fc0000fc0000fc0000fc0000fc0000fc0000fc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        103: '26:28:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003f8fe0007fefe000ffffe001ffffe001ffffe003fc1fe003f81fe003f80fe003f00fe003f00fe003f00fe003f00fe003f00fe003f00fe003f80fe003f81fe001fc3fe001ffffe000ffffe000ffefe0007fcfe0001f8fe000000fe000000fc000801fc000e07fc000ffff8000ffff0000fffe0000fff800000780000000000000000000000000000000000000000000000000000000000000000000000000000',
        104: '26:28:000000000000000000000000000000000000000000000000000000001f8000001f8000001f8000001f8000001f8000001f8000001f8000001f8000001f8ff0001f9ff8001fbff8001ffffc001ffffc001fe1fe001fc0fe001fc0fe001fc0fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        105: '12:14:00000000000000000000000000001f801f801f801f801f800000000000001f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f80000000000000000000000000000000000000000000000000000000000000000000000000',
        106: '12:14:00000000000000000000000000003f003f003f003f003f000000000000003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f007f00fe00fe00fc00f800e000000000000000000000000000000000000000',
        107: '24:26:000000000000000000000000000000000000000000000000000000001f8000001f8000001f8000001f8000001f8000001f8000001f8000001f8000001f80ff001f81fe001f83fc001f83f8001f87f0001f8fe0001f9fc0001fbf80001fff00001ffe00001ffe00001ffe00001fff00001fbf80001f9fc0001f8fe0001f8ff0001f87f8001f83fc001f81fc001f80fe001f807f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        108: '12:14:00000000000000000000000000001f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f80000000000000000000000000000000000000000000000000000000000000000000000000',
        109: '38:40:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001f8fe0fe001f9ff1ff801fbffbff801fffffffc01fffffffc01fe1ff1fc01fc1fe0fe01fc1fe0fe01fc0fc0fe01f80fc0fe01f80fc0fe01f80fc0fe01f80fc0fe01f80fc0fe01f80fc0fe01f80fc0fe01f80fc0fe01f80fc0fe01f80fc0fe01f80fc0fe01f80fc0fe01f80fc0fe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        110: '26:28:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001f8ff0001f9ff8001fbff8001ffffc001ffffc001fe1fe001fc0fe001fc0fe001fc0fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        111: '25:27:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ff800003ffe00007fff0000ffff8001ffffc001fc1fc003f80fe003f80fe003f00fe003f007e003f007e003f007e003f007e003f00fe003f80fe003f80fe003fc1fc001ff7fc000ffff8000ffff00007ffe00001ffc000001c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        112: '26:28:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001f8fe0001f9ff8001fbffc001ffffc001ffffe001fe0fe001fc07f001fc07f001fc07f001f803f001f803f001f803f001f803f001fc07f001fc07f001fc07f001fe0fe001ffffe001ffffc001fbffc001f9ff8001f8ff0001f8180001f8000001f8000001f8000001f8000001f8000001f8000001f80000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        113: '26:28:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003f8fe0007fefe000ffffe001ffffe001ffffe001fc1fe003f81fe003f80fe003f00fe003f00fe003f00fe003f00fe003f00fe003f00fe003f80fe003f80fe003fc1fe001ffffe001ffffe000ffffe0007fefe0003fcfe000060fe000000fe000000fe000000fe000000fe000000fe000000fe000000fe0000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        114: '18:20:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001f8fc01f9fc01fbfc01fffc01fffc01ff8c01fe0001fc0001fc0001fc0001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f80001f8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        115: '21:23:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007ff800fffc01fffc03fffc03f87c03f00403e00003f00003ff0003fff001fffc00fffe003ffe0003ff00007f00003f02003f03c07e03fffe03fffe03fffc01fff00007000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        116: '17:19:0000000000000000000000000000000000000000000000000000000fc0000fc0000fc0000fc0000fc0000fc000ffff00ffff00ffff00ffff00ffff000fc0000fc0000fc0000fc0000fc0000fc0000fc0000fc0000fc0000fc0000fc0000fc0000fff000fff0007ff0007ff0001ff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        117: '26:28:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001fc1fe001fc3fe001ffffe000ffffe000ffffe0007fefe0003fcfe000060000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        118: '23:25:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007e00fe007e00fc007f00fc003f00fc003f01f8003f81f8001f81f8001f83f0000fc3f0000fc3f0000fc7e00007e7e00007e7e00007efc00003ffc00003ffc00003ff800001ff800001ff000001ff000000ff000000fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        119: '33:35:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007e03e03f003f03f03f003f07f07e003f07f07e003f07f07e001f87f07e001f87f8fe001f8ff8fc001f8f78fc001f8f78fc000fcf7cfc000fdf3df8000fde3df8000fde3df80007fe3df80007fe1ff00007fe1ff00007fc1ff00003fc1ff00003fc1fe00003fc0fe00003f80fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        120: '23:25:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007f01fc003f01f8003f83f8001fc3f0000fc7e0000fefe00007ffc00003ff800003ff800001ff000000fe000000ff000001ff000003ff800003ffc00007efc0000fefe0000fc7f0001f83f0003f83f8003f01fc007f00fc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        121: '23:25:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007e00fe007e00fc007f00fc003f01fc003f01f8001f81f8001f81f8001f83f0000fc3f0000fc3f0000fc7e00007e7e00007e7e00003ffc00003ffc00003ffc00001ff800001ff800000ff000000ff000000ff0000007e0000007e0000007e0000007c000000fc00000ffc00000ff800000ff000000fe000000f8000000000000000000000000000000000000000000000000000000000000000000000',
        122: '21:23:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003fffe03fffe03fffe03fffe03fffe0000fe0001fc0003f80007f0000fe0001fe0003fc0003f80007f0000fe0001fc0003f80003fffe03fffe03fffe03fffe03fffe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        123: '26:28:000000000000000000000000000000000000000000000000000000000007f800000ff800001ff800003ff800003f8000003f0000003f0000003f0000003f0000003f0000003f0000003f0000003f0000003f0000007f000000fe00000ffe00000ffc00000ffc00000ffe000001fe0000007f0000003f0000003f0000003f0000003f0000003f0000003f0000003f0000003f0000003f0000003f8000003ff800001ff800001ff8000007f8000000f8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        124: '13:15:0000000000000000000000000000078007800780078007800780078007800780078007800780078007800780078007800780078007800780078007800780078007800780078007800780078007800780078007800780078007800780078000000000000000000000000000000000',
        125: '26:28:000000000000000000000000000000000000000000000000000000000ff800000ffc00000ffe00000ffe000000fe0000007f0000003f0000003f0000003f0000003f0000003f0000003f0000003f0000003f0000003f0000003f8000001ff800000ff800000ff800001ff800003fc000003f8000003f0000003f0000003f0000003f0000003f0000003f0000003f0000003f0000007f0000007e00000ffe00000ffe00000ffc00000ff800000fc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        126: '30:32:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001fc004007ff00c00fffffc00fffffc00f9fffc00c03ff8008007e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        160: '13:15:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        161: '16:18:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007e00007e00007e00007e00007e00007e00007e00000000000000000000003e00003e00003e00003e00007e00007e00007e00007e00007e00007e00007e00007e00007e00007e00007e00007e00007e00007e00007e000000000000000000000000000000000000000000000000000000000000000',
        162: '25:27:00000000000000000000000000000000000000000000000000000000000000000000000000000000000e0000000e0000000e0000000e0000000e0000000e0000007ff00001fff00003fff00007fff0000ffff0000ffe10000fee00001fce00001fce00001fce00001fce00001fce00001fce00001fce00001fce00000fee00000ffe100007fef00007fff00003fff00001fff000007ff000000f0000000e0000000e0000000e0000000e0000000e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        163: '25:27:00000000000000000000000000000000000000000000000000000000000000000007c000003ffc00007ffc0000fffc0001fffc0001ff7c0001fc040003f8000003f8000003f8000003f8000003f8000003f8000003f800001fffe0001fffe0001fffe0001fffe00003f8000003f8000003f8000003f8000003f8000003f8000003f800003ffffc003ffffc003ffffc003ffffc003ffffc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        164: '23:25:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000180030003c0078003e7cf8003ffff0001ffff0000fffe00007c7c0000f83e0000f01e0000f01e0000f01e0000f01e0000f01e0000f83e00007c7c0000fffe0001ffff0003ffff8003e7cf8003c0078001800300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        165: '25:27:00000000000000000000000000000000000000000000000000000000000000007f007f007f007f003f80fe003fc0fe001fc1fc000fe3f8000fe3f80007f7f00007f7f00003ffe0007fffff007fffff007fffff007fffff00007f8000007f0000007f00007fffff007fffff007fffff007fffff00007f0000007f0000007f0000007f0000007f0000007f0000007f0000007f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        166: '13:15:0000000000000000000000000000000000000000078007800780078007800780078007800780078007800780078007800780000000000000000000000780078007800780078007800780078007800780078007800780078007800000000000000000000000000000000000000000',
        167: '18:20:00000000000000000000000000000000000000000000000001f0000fff001fff003fff003f9f003f01003e00003f00003fc0001ff0000ffc001ffe003fff007eff807c3f80f80fc0f807c0fc07c0fc07c07f0f807fdf803fff001ffe000ffc0003fe0000ff00003f00001f00201f003e7f003fff003ffe003ffc0007e000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        168: '18:20:0000000000000000000000000000000000000000001f3e001f3e001f3e001f3e001f3e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        169: '36:38:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001fc0000000fff0000001fff8000003e07c000007801e00000f000f00001e0fc780001c3fe38000387fe1c00038ffe1c00071f820e00071f000e00071e000e00071e000e00071e000e00071e000e00071e000e00071f000e00071f820e00038ffe1c000387fe1c0001c3fe380001e0fc780000f000f000007801e000003e07c000001fff8000000fff00000003f8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        170: '20:22:00000000000000000000000000000000000000000000000000f0000ffe000fff000fff80080f8000078001ffc007ffc00fffc01f07c01e07c01e0fc01f1fc01fffc00fffc007e7c00000000000000000001fff801fff801fff801fff80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        171: '23:25:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002030000060700000e0f00003e1f00007e3e0000fcfc0001f1f80001e1f00001e1e00001f1f00001f8f80000fc7e00003e3f00001e1f00000e0f00000603000002010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        172: '30:32:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000fffffc00fffffc00fffffc00fffffc00fffffc0000003c0000003c0000003c0000003c0000003c0000003c0000003c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        173: '1:3:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        174: '36:38:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001fc0000000fff0000001fff8000003e07c000007801e00000f000f00001e7f8780001c7fe38000387fe1c0003871f1c0007070f0e0007070f0e0007071e0e000707fe0e000707fc0e000707780e0007073c0e0007073c0e0007071e0e0003871e1c0003870f1c0001c70f380001e000780000f000f000007801e000003e07c000001fff8000000fff00000003f8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        175: '18:20:0000000000000000000000000000000000000000001ffe001ffe001ffe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        176: '18:20:00000000000000000000000000000000000000000000000001e00007f8000ffc000f3c001e1e001c0e001c0e001c0e001e1e000f3c000ffc0007f80003e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        177: '30:32:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000780000007800000078000000780000007800000078000000780000fffffc00fffffc00fffffc00fffffc00007800000078000000780000007800000078000000780000007800000000000000000000fffffc00fffffc00fffffc00fffffc00fffffc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        178: '16:18:00000000000000000000000000000000000000000000000007c0003ff0003ff80038f800207c00007c0000780000780000f00001f00003e00007c0001f80003e00003ffc003ffc003ffc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        179: '16:18:0000000000000000000000000000000000000000000000000fc0003ff0003ff80030f80000780000780000f8000ff0000ff0000ff800007c00007c00007c00207c003ff8003ff8003fe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        180: '18:20:000000000000000000000000000000000000001f00003e00003c0000780000f00000f00001e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        181: '26:28:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001f807e001f807e001f807e001f807e001f807e001f807e001f807e001f807e001f807e001f807e001f807e001f807e001f807e001f807e001fc0fe001fc0fe001fe1fe001fffff801fffff801fffff801fffbf801fbf1f801f8c06001f8000001f8000001f8000001f8000001f8000001f8000001f800000000000000000000000000000000000000000000000000000000000000000000000000000',
        182: '23:25:000000000000000000000000000000000000000000000000000000000000000001fff00007fff0000ffff0001ff8f0001ff8f0001ff8f0003ff8f0003ff8f0003ff8f0003ff8f0001ff8f0001ff8f0001ff8f0000ff8f00007f8f00001f8f0000038f0000038f0000038f0000038f0000038f0000038f0000038f0000038f0000038f0000038f0000038f0000038f0000038f0000038f0000038f0000038f0000038f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        183: '14:16:000000000000000000000000000000000000000000000000000000000000000000000000000000000fc00fc00fc00fc00fc00fc00fc00fc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        184: '18:20:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e00000700000700000380000780007f00007f00007c000000000000000000000000000000000000000000000000000000000',
        185: '16:18:0000000000000000000000000000000000000000000000001fc0003fc0003fc00023c00003c00003c00003c00003c00003c00003c00003c00003c00003c0003ffc003ffc003ffc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        186: '20:22:00000000000000000000000000000000000000000000000000f00007fe000fff001fff801f0f803f07c03e07c03e07c03e07c03e07c03e07c03f07c01f8f800fff800fff0003fc000000000000000000001fff801fff801fff801fff80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        187: '23:25:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000180800001c0e00001e0f00001f0f80000fcfc00007e3e00003f1f00000f0f00000f0700001f1f00003f3f00007c7e0000f8fc0001f0f00001e0e00001c0c0000100800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        188: '37:39:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000078001fc00078003fc000f0003fc001e00023c001e00003c003c00003c003c00003c007800003c007800003c00f000003c00f000003c01e000003c01e000003c03c00003ffc381f003ffc783f003ffcf03f000000f07f000001e0ef000001e0ef000003c1cf000003c38f000007838f000007870f00000f07ffc0000f07ffc0001e07ffc0003c000f00003c000f000078000f0000780000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        189: '37:39:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000078001fc00078003fc000f0003fc001e00023c001e00003c003c00003c003c00003c007800003c007800003c00f000003c00f000003c01e000003c01e000003c03c1f003ffc38ffc03ffc78ffe03ffcf0e3e00000f081f00001e001f00001e001e00003c001e00003c003c000078007c00007800f80000f001f00000f007e00001e00f800003c00fff0003c00fff0007800fff000780000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        190: '37:39:000000000000000000000000000000000000000000000000000000000000000000000000000000000fc00078003ff00078003ff800f00030f801e000007801e000007803c00000f803c0000ff00780000ff00780000ff80f0000007c0f0000007c1e0000007c1e0000207c3c00003ff8381f003ff8783f003fe0f03f000000f07f000001e0ef000001e0ef000003c1cf000003c38f000007838f000007870f00000f07ffc0000f07ffc0001e07ffc0003c000f00003c000f000078000f0000780000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        191: '21:23:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007e00007e00007e00007e00007e00007e00007e00000000000000000000007e00007e0000fe0001fc0001fc0003f80007f0000fe0001fc0001fc0001f80001f80003f80201f80e01fe3e01fffe01fffe00fffe007ffc000fc00000000000000000000000000000000000000000000000000000000',
        192: '28:30:0000000000f80000007c0000003e0000001e0000000f0000000000000000000000000000003fc000007fe000007fe000007fe00000fff00000fff00000fff00001fff80001f9f80001f9f80003f9fc0003f1fc0003f0fc0007f0fe0007f0fe0007e07e000fe07f000fe07f000fffff001fffff801fffff801fffff803fffffc03fffffc03f001fc07f000fe07f000fe07e000fe0fe0007f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        193: '28:30:000000000001f0000003e0000007c00000078000000f0000000000000000000000000000003fc000007fe000007fe000007fe00000fff00000fff00000fff00001fff80001f9f80001f9f80003f9fc0003f1fc0003f0fc0007f0fe0007f0fe0007e07e000fe07f000fe07f000fffff001fffff801fffff801fffff803fffffc03fffffc03f001fc07f000fe07f000fe07e000fe0fe0007f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        194: '28:30:00000000001f8000003fc000003fc0000079e00000e07000000000000000000000000000003fc000007fe000007fe000007fe00000fff00000fff00000fff00001fff80001f9f80001f9f80003f9fc0003f1fc0003f0fc0007f0fe0007f0fe0007e07e000fe07f000fe07f000fffff001fffff801fffff801fffff803fffffc03fffffc03f001fc07f000fe07f000fe07e000fe0fe0007f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        195: '28:30:0000000000383000007e700000fff00000e7e00000c3e000000000000000000000000000003fc000007fe000007fe000007fe00000fff00000fff00000fff00001fff80001f9f80001f9f80003f9fc0003f1fc0003f0fc0007f0fe0007f0fe0007e07e000fe07f000fe07f000fffff001fffff801fffff801fffff803fffffc03fffffc03f001fc07f000fe07f000fe07e000fe0fe0007f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        196: '28:30:0000000000f9f00000f9f00000f9f00000f9f00000f9f000000000000000000000000000003fc000007fe000007fe000007fe00000fff00000fff00000fff00001fff80001f9f80001f9f80003f9fc0003f1fc0003f0fc0007f0fe0007f0fe0007e07e000fe07f000fe07f000fffff001fffff801fffff801fffff803fffffc03fffffc03f001fc07f000fe07f000fe07e000fe0fe0007f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        197: '28:30:000f0000003f8000003fc0000071e0000070e0000070e0000070e0000079e000003fc000007fe000007fe000007fe00000fff00000fff00000fff00001fff80001f9f80001f9f80003f9fc0003f1fc0003f0fc0007f0fe0007f0fe0007e07e000fe07f000fe07f000fffff001fffff801fffff801fffff803fffffc03fffffc03f001fc07f000fe07f000fe07e000fe0fe0007f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        198: '39:41:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001ffffff000003ffffff000003ffffff000003ffffff000007ffffff000007e3ffff00000fe3f80000000fe3f80000000fc3f80000001fc3f80000001fc3f80000001f83fffe00003f83fffe00003f03fffe00007f03fffe00007f03fffe00007e03fffe0000fffff8000000fffff8000000fffff8000001fffff8000001fffff8000003f803f8000003f803ffff0003f003ffff0007f003ffff0007e003ffff0007e003ffff000fe003ffff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        199: '26:28:00000000000000000000000000000000000000000000000000000000000000000007e000003ffc0000ffff0001ffff0003ffff0007ffff000ff807001ff001001fe000001fc000003fc000003f8000003f8000003f8000003f8000003f8000003f8000003f8000003f8000003f8000003fc000001fc000001fe000001ff003000ff80f0007ffff0003ffff0001ffff0000ffff00003ffc000003c0000000e0000000e000000070000000f000000fe000000fe000000f8000000000000000000000000000000000000000000000000000000000000000000000000000',
        200: '25:27:0000000003e0000001f0000000f8000000780000003c00000000000000000000000000001ffffc001ffffc001ffffc001ffffc001ffffc001ffffc001fc000001fc000001fc000001fc000001fc000001ffff8001ffff8001ffff8001ffff8001ffff8001ffff8001fc000001fc000001fc000001fc000001fc000001fc000001ffffc001ffffc001ffffc001ffffc001ffffc001ffffc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        201: '25:27:000000000007c000000f8000001f0000001e0000003c00000000000000000000000000001ffffc001ffffc001ffffc001ffffc001ffffc001ffffc001fc000001fc000001fc000001fc000001fc000001ffff8001ffff8001ffff8001ffff8001ffff8001ffff8001fc000001fc000001fc000001fc000001fc000001fc000001ffffc001ffffc001ffffc001ffffc001ffffc001ffffc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        202: '25:27:00000000007e000000ff000000ff000001e780000381c0000000000000000000000000001ffffc001ffffc001ffffc001ffffc001ffffc001ffffc001fc000001fc000001fc000001fc000001fc000001ffff8001ffff8001ffff8001ffff8001ffff8001ffff8001fc000001fc000001fc000001fc000001fc000001fc000001ffffc001ffffc001ffffc001ffffc001ffffc001ffffc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        203: '25:27:0000000003e7c00003e7c00003e7c00003e7c00003e7c0000000000000000000000000001ffffc001ffffc001ffffc001ffffc001ffffc001ffffc001fc000001fc000001fc000001fc000001fc000001ffff8001ffff8001ffff8001ffff8001ffff8001ffff8001fc000001fc000001fc000001fc000001fc000001fc000001ffffc001ffffc001ffffc001ffffc001ffffc001ffffc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        204: '13:15:0000f8007c003e001e000f000000000000001fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc000000000000000000000000000000000000000000000000000000000000000000000',
        205: '13:15:000001f003e007c007800f000000000000001fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc000000000000000000000000000000000000000000000000000000000000000000000',
        206: '13:15:00000fc01fe01fe03cf070380000000000001fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc000000000000000000000000000000000000000000000000000000000000000000000',
        207: '13:15:00007cf87cf87cf87cf87cf80000000000001fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc000000000000000000000000000000000000000000000000000000000000000000000',
        208: '30:32:00000000000000000000000000000000000000000000000000000000000000000fffe0000ffff8000ffffe000fffff000fffff800fffffc00fc07fe00fc01fe00fc00fe00fc00ff00fc007f00fc007f07ffe07f07ffe07f07ffe07f07ffe07f07ffe07f00fc007f00fc007f00fc00ff00fc00fe00fc01fe00fc07fc00fffffc00fffff800fffff000ffffe000ffff8000fffc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        209: '30:32:0000000000383000007e700000fff00000e7e00000c3e0000000000000000000000000001fe00fe01ff00fe01ff00fe01ff80fe01ff80fe01ffc0fe01ffc0fe01ffe0fe01ffe0fe01ffe0fe01fff0fe01fdf0fe01fdf8fe01fcf8fe01fcfcfe01fc7cfe01fc7efe01fc3efe01fc3ffe01fc1ffe01fc1ffe01fc0ffe01fc0ffe01fc07fe01fc07fe01fc03fe01fc03fe01fc01fe01fc01fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        210: '31:33:0000000000007c000000003e000000001f000000000f0000000007800000000000000000000000000007c00000007ff8000001fffe000003ffff000007ffff80000fffffc0000ff03fe0001fe01fe0001fc00ff0001fc007f0003f8007f0003f8007f0003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8007f0003fc007f0001fc007f0001fc00ff0001fe01fe0000ff83fe00007ffffc00007ffff800003ffff000000fffe0000007ff8000000030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        211: '31:33:00000000000000f800000001f000000003e000000003c000000007800000000000000000000000000007c00000007ff8000001fffe000003ffff000007ffff80000fffffc0000ff03fe0001fe01fe0001fc00ff0001fc007f0003f8007f0003f8007f0003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8007f0003fc007f0001fc007f0001fc00ff0001fe01fe0000ff83fe00007ffffc00007ffff800003ffff000000fffe0000007ff8000000030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        212: '31:33:0000000000000fc00000001fe00000001fe00000003cf000000070380000000000000000000000000007c00000007ff8000001fffe000003ffff000007ffff80000fffffc0000ff03fe0001fe01fe0001fc00ff0001fc007f0003f8007f0003f8007f0003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8007f0003fc007f0001fc007f0001fc00ff0001fe01fe0000ff83fe00007ffffc00007ffff800003ffff000000fffe0000007ff8000000030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        213: '31:33:0000000000001c180000003f380000007ff800000073f000000061f00000000000000000000000000007c00000007ff8000001fffe000003ffff000007ffff80000fffffc0000ff03fe0001fe01fe0001fc00ff0001fc007f0003f8007f0003f8007f0003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8007f0003fc007f0001fc007f0001fc00ff0001fe01fe0000ff83fe00007ffffc00007ffff800003ffff000000fffe0000007ff8000000030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        214: '31:33:0000000000007cf80000007cf80000007cf80000007cf80000007cf80000000000000000000000000007c00000007ff8000001fffe000003ffff000007ffff80000fffffc0000ff03fe0001fe01fe0001fc00ff0001fc007f0003f8007f0003f8007f0003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8003f8007f0003fc007f0001fc007f0001fc00ff0001fe01fe0000ff83fe00007ffffc00007ffff800003ffff000000fffe0000007ff8000000030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        215: '30:32:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010002000380070007c00f8007e01f8003f03f0001f87e0000fc7e00007cfc00007ff800003ff000001fe000000fc000001fe000003ff000007ff80000fcfc0000fc7e0001f83e0003f03f0007e01f8007c00f80038007000100020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        216: '31:33:000000000000000000000000000000000000000000000000000000000000000000000000000000000007c01800007ff83c0001fffe780003fffff00007ffffe0000fffffc0000ff03fe0001fe01fe0001fc01ff0001fc01ff0003f803ff0003f807ff0003f80f3f8003f81e3f8003f83c3f8003f8783f8003f8f03f8003f9e03f8003fbc03f8003fbc07f0003ff807f0001ff007f0001fe00ff0001fe01fe0000ff83fe0000fffffc0001fffff80003fffff000078fffe0000783ff8000030030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        217: '29:31:0000000000f80000007c0000003e0000001e0000000f00000000000000000000000000001fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc00fe01fc00fe03f800ff07f8007ffff8007ffff0003fffe0001fffc00007ff0000007800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        218: '29:31:000000000001f0000003e0000007c00000078000000f00000000000000000000000000001fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc00fe01fc00fe03f800ff07f8007ffff8007ffff0003fffe0001fffc00007ff0000007800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        219: '29:31:00000000000fc000001fe000001fe000003cf000007038000000000000000000000000001fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc00fe01fc00fe03f800ff07f8007ffff8007ffff0003fffe0001fffc00007ff0000007800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        220: '29:31:00000000007cf800007cf800007cf800007cf800007cf8000000000000000000000000001fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc01fc00fe01fc00fe03f800ff07f8007ffff8007ffff0003fffe0001fffc00007ff0000007800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        221: '26:28:000000000007c000000f8000001f0000001e0000003c0000000000000000000000000000fc003f80fe007f00ff00ff007f00fe007f81fe003f81fc001fc3f8001fc3f8000fe7f0000ffff00007ffe00003ffe00003ffc00001ff800001ff800000ff0000007f0000007e0000007e0000007e0000007e0000007e0000007e0000007e0000007e0000007e0000007e0000007e0000007e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        222: '27:29:00000000000000000000000000000000000000000000000000000000000000001fc000001fc000001fc000001fc000001fc000001fffe0001ffff8001ffffc001ffffe001fffff001fc1ff001fc07f801fc03f801fc03f801fc03f801fc03f801fc03f801fc07f801fc3ff001fffff001ffffe001ffffc001ffff8001fffe0001fc000001fc000001fc000001fc000001fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        223: '26:28:0000000000000000000000000000000000000000000000000000000001ffc00003ffe00007fff0000ffff8000fe3f8001fc0fc001fc0fc001f80fc001f83fc001f87fc001f8fc0001f8f80001f9f80001f9f80001f9fc0001f9fe0001f8ff8001f8ffc001f87fe001f83ff001f80ff001f807f001f803f001f803f001f803f001f987f001f9fff001f9ffe001f9ffe001f9ff8000001c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        224: '24:26:00000000000000000000000000000000000000000000000007c0000003e0000001e0000000f000000078000000780000003c00000000000000000000000000000fff80001fffe0001ffff0001ffff0001e07f8001003f8000001f8000001f80001fff8000ffff8001ffff8003ffff8003fc1f8003f01f8003f01f8003f01f8003f03f8003f87f8003ffff8001ffff8001ffdf80007f9f80001c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        225: '24:26:0000000000000000000000000000000000000000000000000003e0000007c00000078000000f0000001e0000001e0000003c00000000000000000000000000000fff80001fffe0001ffff0001ffff0001e07f8001003f8000001f8000001f80001fff8000ffff8001ffff8003ffff8003fc1f8003f01f8003f01f8003f01f8003f03f8003f87f8003ffff8001ffff8001ffdf80007f9f80001c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        226: '24:26:000000000000000000000000000000000000000000000000003c0000007e000000ff000000ff000001e7800001c3c0000381c0000000000000000000000000000fff80001fffe0001ffff0001ffff0001e07f8001003f8000001f8000001f80001fff8000ffff8001ffff8003ffff8003fc1f8003f01f8003f01f8003f01f8003f03f8003f87f8003ffff8001ffff8001ffdf80007f9f80001c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        227: '24:26:00000000000000000000000000000000000000000000000000e0c00001f9c00003ffc000039f8000030f8000000000000000000000000000000000000fff80001fffe0001ffff0001ffff0001e07f8001003f8000001f8000001f80001fff8000ffff8001ffff8003ffff8003fc1f8003f01f8003f01f8003f01f8003f03f8003f87f8003ffff8001ffff8001ffdf80007f9f80001c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        228: '24:26:0000000000000000000000000000000000000000000000000000000003e7c00003e7c00003e7c00003e7c00003e7c000000000000000000000000000000000000fff80001fffe0001ffff0001ffff0001e07f8001003f8000001f8000001f80001fff8000ffff8001ffff8003ffff8003fc1f8003f01f8003f01f8003f01f8003f03f8003f87f8003ffff8001ffff8001ffdf80007f9f80001c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        229: '24:26:000000000000000000180000007e000000ff000000ff000001c3800001c3800001c3800001c3800001e7000000ff0000007e00000018000000000000000000000fff80001fffe0001ffff0001ffff0001e07f8001003f8000001f8000001f80001fff8000ffff8001ffff8003ffff8003fc1f8003f01f8003f01f8003f01f8003f03f8003f87f8003ffff8001ffff8001ffdf80007f9f80001c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        230: '38:40:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000fff03fc001fffcfff001fffffff801fffffffc01e07ff1fe01003fe0fe00001fc07e00001fc07f001fff807f00ffffffff01ffffffff03ffffffff03fc1fffff03f01f800003f01fc00003f01fc00003f03fe00603f87ff03e03fffffffe01fff3fffe01ffe1fffe007f807ff8000c000700000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        231: '21:23:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ffc003ffe007ffe00fffe01fffe01fe0603f80003f80003f00003f00003f00003f00003f00003f00003f80003f80003fc0201ff9e00fffe007ffe003ffe001ffe0001e00000e00000e00000700000f0000fe0000fe0000f800000000000000000000000000000000000000000000000000000000000000',
        232: '24:26:00000000000000000000000000000000000000000000000003e0000001f0000000f0000000780000003c0000003c0000001e000000000000000000000000000000ff800003ffe00007fff0000ffff8001fe3f8001f81fc003f80fc003f00fc003f00fc003ffffe003ffffe003ffffe003ffffe003f0000003f0000003f8004003f801c001fe07c000ffffc000ffffc0003fffc0001ffe000001c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        233: '24:26:0000000000000000000000000000000000000000000000000001f0000003e0000003c00000078000000f0000000f0000001e000000000000000000000000000000ff800003ffe00007fff0000ffff8001fe3f8001f81fc003f80fc003f00fc003f00fc003ffffe003ffffe003ffffe003ffffe003f0000003f0000003f8004003f801c001fe07c000ffffc000ffffc0003fffc0001ffe000001c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        234: '24:26:000000000000000000000000000000000000000000000000001e0000003f0000007f8000007f800000f3c00000e1e00001c0e00000000000000000000000000000ff800003ffe00007fff0000ffff8001fe3f8001f81fc003f80fc003f00fc003f00fc003ffffe003ffffe003ffffe003ffffe003f0000003f0000003f8004003f801c001fe07c000ffffc000ffffc0003fffc0001ffe000001c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        235: '24:26:0000000000000000000000000000000000000000000000000000000001f3e00001f3e00001f3e00001f3e00001f3e0000000000000000000000000000000000000ff800003ffe00007fff0000ffff8001fe3f8001f81fc003f80fc003f00fc003f00fc003ffffe003ffffe003ffffe003ffffe003f0000003f0000003f8004003f801c001fe07c000ffffc000ffffc0003fffc0001ffe000001c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        236: '12:14:000000000000000000000000f000f80078003c001e001e000f000000000000003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f003f0000000000000000000000000000000000000000000000000000000000000000000000',
        237: '12:14:000000000000000000000000007c00f800f001e003c003c007800000000000001f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f8000000000000000000000000000000000000000000000000000000000000000000000',
        238: '12:14:0000000000000000000000000f001f803fc03fc079e070f0e0700000000000001f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f8000000000000000000000000000000000000000000000000000000000000000000000',
        239: '12:14:0000000000000000000000000000f9f0f9f0f9f0f9f0f9f000000000000000001f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f801f8000000000000000000000000000000000000000000000000000000000000000000000',
        240: '25:27:0000000000000000000000000000000000000000000000000000000003f8380001fdf80000fff000007f800003ff00000fff80000f8fc0000c0fc0000007e000003bf00003fff80007fff8000ffffc001ffffc003ff7fe003f80fe003f80fe003f007e003f007e003f007e003f007e003f00fe003f80fe003f80fe003fc1fc001ff7fc000ffff8000ffff00007ffe00001ffc000001c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        241: '26:28:0000000000000000000000000000000000000000000000000070600000fce00001ffe00001cfc0000187c000000000000000000000000000000000001f8ff0001f9ff8001fbff8001ffffc001ffffc001fe1fe001fc0fe001fc0fe001fc0fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        242: '25:27:00000000000000000000000000000000000000000000000003e0000001f0000000f0000000780000003c0000003c0000001e000000000000000000000000000000ff800003ffe00007fff0000ffff8001ffffc001fc1fc003f80fe003f80fe003f00fe003f007e003f007e003f007e003f007e003f00fe003f80fe003f80fe003fc1fc001ff7fc000ffff8000ffff00007ffe00001ffc000001c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        243: '25:27:0000000000000000000000000000000000000000000000000001f0000003e0000003c00000078000000f0000000f0000001e000000000000000000000000000000ff800003ffe00007fff0000ffff8001ffffc001fc1fc003f80fe003f80fe003f00fe003f007e003f007e003f007e003f007e003f00fe003f80fe003f80fe003fc1fc001ff7fc000ffff8000ffff00007ffe00001ffc000001c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        244: '25:27:000000000000000000000000000000000000000000000000003c0000007e000000ff000000ff000001e7800001c3c0000381c00000000000000000000000000000ff800003ffe00007fff0000ffff8001ffffc001fc1fc003f80fe003f80fe003f00fe003f007e003f007e003f007e003f007e003f00fe003f80fe003f80fe003fc1fc001ff7fc000ffff8000ffff00007ffe00001ffc000001c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        245: '25:27:00000000000000000000000000000000000000000000000000e0c00001f9c00003ffc000039f8000030f80000000000000000000000000000000000000ff800003ffe00007fff0000ffff8001ffffc001fc1fc003f80fe003f80fe003f00fe003f007e003f007e003f007e003f007e003f00fe003f80fe003f80fe003fc1fc001ff7fc000ffff8000ffff00007ffe00001ffc000001c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        246: '25:27:0000000000000000000000000000000000000000000000000000000003e7c00003e7c00003e7c00003e7c00003e7c0000000000000000000000000000000000000ff800003ffe00007fff0000ffff8001ffffc001fc1fc003f80fe003f80fe003f00fe003f007e003f007e003f007e003f007e003f00fe003f80fe003f80fe003fc1fc001ff7fc000ffff8000ffff00007ffe00001ffc000001c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        247: '30:32:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000fc000000fc000000fc000000fc000000fc000000fc00000000000000000000fffffc00fffffc00fffffc00fffffc00fffffc00000000000000000000fc000000fc000000fc000000fc000000fc000000fc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        248: '25:27:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000040000000e0000ff9e0003fffc0007fff8000ffff8001ffffc001fc1fc003f83fe003f83fe003f07fe003f0e7e003f1e7e003f3c7e003f787e003ff0fe003fe0fe003fc0fe003fc1fc001ff7fc000ffff8001ffff0001fffe00039ffc000381c000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        249: '26:28:00000000000000000000000000000000000000000000000003e0000001f0000000f0000000780000003c0000003c0000001e00000000000000000000000000001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001fc1fe001fc3fe001ffffe000ffffe000ffffe0007fefe0003fcfe000060000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        250: '26:28:0000000000000000000000000000000000000000000000000001f0000003e0000003c00000078000000f0000000f0000001e00000000000000000000000000001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001fc1fe001fc3fe001ffffe000ffffe000ffffe0007fefe0003fcfe000060000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        251: '26:28:000000000000000000000000000000000000000000000000001e0000003f0000007f8000007f800000f3c00000e1e00001c0e0000000000000000000000000001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001fc1fe001fc3fe001ffffe000ffffe000ffffe0007fefe0003fcfe000060000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        252: '26:28:0000000000000000000000000000000000000000000000000000000001f3e00001f3e00001f3e00001f3e00001f3e000000000000000000000000000000000001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001f80fe001fc1fe001fc3fe001ffffe000ffffe000ffffe0007fefe0003fcfe000060000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        253: '23:25:0000000000000000000000000000000000000000000000000003e0000007c00000078000000f0000001e0000001e0000003c00000000000000000000000000007e00fe007e00fc007f00fc003f01fc003f01f8001f81f8001f81f8001f83f0000fc3f0000fc3f0000fc7e00007e7e00007e7e00003ffc00003ffc00003ffc00001ff800001ff800000ff000000ff000000ff0000007e0000007e0000007e0000007c000000fc00000ffc00000ff800000ff000000fe000000f8000000000000000000000000000000000000000000000000000000000000000000000',
        254: '26:28:000000000000000000000000000000000000000000000000000000001f8000001f8000001f8000001f8000001f8000001f8000001f8000001f8000001f8fe0001f9ff8001fbffc001ffffc001ffffe001fe0fe001fc07f001fc07f001fc07f001f803f001f803f001f803f001f803f001fc07f001fc07f001fc07f001fe0fe001ffffe001ffffc001fbffc001f9ff8001f8ff0001f8180001f8000001f8000001f8000001f8000001f8000001f8000001f80000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        255: '23:25:0000000000000000000000000000000000000000000000000000000003e7c00003e7c00003e7c00003e7c00003e7c000000000000000000000000000000000007e00fe007e00fc007f00fc003f01fc003f01f8001f81f8001f81f8001f83f0000fc3f0000fc3f0000fc7e00007e7e00007e7e00003ffc00003ffc00003ffc00001ff800001ff800000ff000000ff000000ff0000007e0000007e0000007e0000007c000000fc00000ffc00000ff800000ff000000fe000000f8000000000000000000000000000000000000000000000000000000000000000000000',
        8364: '25:27:00000000000000000000000000000000000000000000000000000000000000000007c000003ff80000fffe0001fffe0003fffe0007fe7e0007f80e000ff002000fe000001fc000007fffe000ffffe000ffffe000ffffc0001f8000001f8000001f8000007fff8000ffff0000ffff0000fffe00001fc000000fe002000ff0060007f80e0007fffe0003fffe0001fffe0000fffe00003ff8000003000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8211: '18:20:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003fff003fff003fff003fff003fff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8212: '36:38:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003fffffffc03fffffffc03fffffffc03fffffffc03fffffffc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8222: '24:26:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000fc7e0000fc7e0000fc7e0000fc7e0000fc7e0000fc7e0000fc7e0000f87c0000f87c0001f0f80001f0f80001e0f00001e0e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8220: '24:26:000000000000000000000000000000000000000000000000000000000000000001e0f00001e0f00003e1f00003e3e00007c3e0000fc7e0000fc7e0000fc7e0000fc7e0000fc7e0000fc7e0000fc7e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8221: '24:26:000000000000000000000000000000000000000000000000000000000000000007e3f00007e3f00007e3f00007e3f00007e3f00007e3f00007c3e00007c7e0000f87c0000f87c0000f0780001f0f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8217: '14:16:000000000000000000000000000000000fc00fc00fc00fc00fc00fc00f801f801f001f001e003c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8226: '23:25:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007c000000fe000001ff000003ff800003ff800007ffc00007ffc00007ffc00007ffc00003ff800003ff800001ff800001ff0000007c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        338: '42:44:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ffffffe00007ffffffe0001fffffffe0003fffffffe0007fffffffe000ffffffffe000ff807f000001ff007f000001fe007f000003fc007f000003f8007f000003f8007fffc003f8007fffc003f8007fffc003f8007fffc003f8007fffc003f8007fffc003f8007f000003fc007f000003fc007f000001fe007f000001ff007f000000ffc07f000000ffffffffe0007fffffffe0003fffffffe0000fffffffe00007ffffffe00000ffffffe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        339: '39:41:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ff81ff000003ffc7ffc00007ffefffe0000ffffffff0001fffffc7f0001fc1ff03f8003f80ff01f8003f80fe01f8003f00fe01f8003f007ffffc003f007ffffc003f007ffffc003f007ffffc003f00fe0000003f80fe0000003f80ff0008003fc1ff0038001ff7ffc0f8000ffffffff8000ffffffff80007ffe7fff80001ff83ffe000001c00380000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        352: '26:28:0000000001c0e00001e1e00000f3c000007f8000003f00000000000000000000003f000001fff80007fffc000ffffc000ffffc001ffffc001fc03c001f8004001f8000001f8000001f8000001fe000001fff00001fffe0000ffff00007fffc0003fffc00007ffe000007fe000001fe000000fe0000007e0000007e001800fe001f01fe001ffffe001ffffc001ffff8001ffff00003ffe000001c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        353: '21:23:00000000000000000000000000000000000007038007878003870001cf0001fe0000fc0000fc0000000000000000000007ff800fffc01fffc03fffc03f87c03f00403e00003f00003ff0003fff001fffc00fffe003ffe0003ff00007f00003f02003f03c07e03fffe03fffe03fffc01fff00007000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        381: '26:28:0000000001c0e00001e1e00000f3c000007f8000003f00000000000000000000000000003fffff003fffff003fffff003fffff003fffff003ffffe000001fe000003fc000007f8000007f000000ff000001fe000003fc000003f8000007f800000ff000000fe000001fc000003fc000007f8000007f000000fe000001fe000003fffff803fffff803fffff803fffff803fffff803fffff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        382: '21:23:0000000000000000000000000000000000000e07000f0f00070e00039e0003fc0001f80001f8000000000000000000003fffe03fffe03fffe03fffe03fffe0000fe0001fc0003f80007f0000fe0001fe0003fc0003f80007f0000fe0001fc0003f80003fffe03fffe03fffe03fffe03fffe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
    },
    'p': {
        32: '9:11:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        33: '11:13:000000000000000000000f000f000f000f000f000f000f000f000f000f000f000f000e00000000000f000f000f000f000f00000000000000000000000000000000000000000000000000000000000000000000000000',
        34: '13:15:0000000000000000000038e038e038e038e038e038e038e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        35: '21:23:00000000000000000000000000000000e38000e38000e38000c30001c7001fffe01fffe01fffe0038e00038e00038e00038e003fffc03fffc03fffc0071c000718000638000e38000e3800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        36: '18:20:00000000000000000000000000c00000c00000c00007fc001ffe001ffe003cc6003cc0003cc0003fc0003ff0001ffc000ffe0001ff0000df0000cf0020cf0038df003ffe003ffc000ff00000c00000c00000c00000c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        37: '25:27:00000000000000000000000000000000000000000f0070003f80e0003fc0e00071c1c00071e1800070e3800070e3000071c7000079c600003fce00001f9c3800001cfe000039ff000039c7000071c7000061c70000e1c70000c1c70001c1c7000180fe0003807c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        38: '22:24:00000000000000000000000000000000f80003fe0007fe000ffe000f82000f80000f800007c00007e0000ff0f01ff0f03ef8f03c7de03c3fe03c3fe03c1fc03e0f803f1fc01fffe00ffff007f9f8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        39: '8:10:0000000000000000000038003800380038003800380038000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        40: '12:14:0000000000000000078007800f000f000f001e001e001e003e003c003c003c003c003c003c003e001e001e001e001e000f000f0007800780038000000000000000000000000000000000000000000000000000000000',
        41: '12:14:00000000000000003c001e001e000f000f000f000f80078007800780078007800780078007800780078007800f000f000f001e001e001c003c0000000000000000000000000000000000000000000000000000000000',
        42: '13:15:0000000000000000000003000300430063307bf03fe00f801fc03ff073784310030003000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        43: '21:23:0000000000000000000000000000000000000000000000000070000070000070000070000070000070000070000070001fffc01fffc01fffc0007000007000007000007000007000007000007000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        44: '10:12:000000000000000000000000000000000000000000000000000000000000000000000000000000001e001e001e001e003e003c0038003800700000000000000000000000000000000000000000000000000000000000',
        45: '10:12:0000000000000000000000000000000000000000000000000000000000007f807f807f807f80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        46: '10:12:000000000000000000000000000000000000000000000000000000000000000000000000000000001e001e001e001e001e00000000000000000000000000000000000000000000000000000000000000000000000000',
        47: '9:11:0000000000000000000003800380030007000700070006000e000e000c001c001c001c0018003800380030007000700070006000e000e000000000000000000000000000000000000000000000000000000000000000',
        48: '18:20:00000000000000000000000000000001e00007f8000ffc001ffe003e3e003e1f003c1f007c1f007c1f007c0f007c0f007c0f007c0f007c1f007c1f003c1f003e1f003f3e001ffc000ffc0007f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        49: '18:20:0000000000000000000000000000001ff0001ff0001ff0001df00001f00001f00001f00001f00001f00001f00001f00001f00001f00001f00001f00001f0001fff001fff001fff001fff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        50: '18:20:00000000000000000000000000000007e0003ff8003ffc003ffe00307e00203e00003e00003e00003e00003c00007c0000f80001f00003e00007c0000f80001f00003ffe003ffe003ffe003ffe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        51: '18:20:00000000000000000000000000000007e0003ff8003ffc003ffe00203e00003e00003e00003e00007c0007f80007f80007fc00007e00003e00001f00001f00003e00387e003ffe003ffc003ff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        52: '18:20:00000000000000000000000000000000fc0001fc0001fc0003fc0003fc00077c000f7c000e7c001e7c003c7c00387c00787c007fff007fff007fff007fff00007c00007c00007c00007c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        53: '18:20:0000000000000000000000000000001ffc001ffc001ffc001c00001c00001c00001de0001ff8001ffc001ffe00103e00001f00001f00001f00001f00203f00387e003ffe003ffc001ff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        54: '18:20:00000000000000000000000000000000f80003fe000ffe000ffe001f02003e00003e00003c00003df8003ffe003ffe003f1f003e1f003e0f003e0f003e0f003e1f001f1f001ffe000ffc0007f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        55: '18:20:0000000000000000000000000000003fff003fff003fff00003e00003e00003c00007c00007c0000f80000f80000f00001f00001e00003e00003e00003c00007c0000780000f80000f8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        56: '18:20:00000000000000000000000000000003f0000ffc001ffe003ffe003e1f003c1f003c1e003e1e001f7e000ffc000ff8001ffe003e1e003c1f003c1f003c1f003c1f003e1f003ffe001ffe000ff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        57: '18:20:00000000000000000000000000000003e0000ff8001ffc003ffc003c3e007c1e007c1f007c1f007c1f007c3f003e7f003fff001fff0007df00001e00001e00003e00107c001ffc001ff8001fe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        58: '10:12:00000000000000000000000000000000000000001e001e001e001e001e00000000000000000000001e001e001e001e001e00000000000000000000000000000000000000000000000000000000000000000000000000',
        59: '10:12:00000000000000000000000000000000000000001e001e001e001e001e00000000000000000000001e001e001e001e001e003c003c003800380000000000000000000000000000000000000000000000000000000000',
        60: '21:23:0000000000000000000000000000000000000000000000000000000000000001c00007c0003fc000ff0007fc001fe0001f80001e00001fc0000ff80001fe00007fc0000fc00003c0000040000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        61: '21:23:0000000000000000000000000000000000000000000000000000000000000000000000001fffc01fffc01fffc01fffc00000000000000000001fffc01fffc01fffc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        62: '21:23:0000000000000000000000000000000000000000000000000000000000001c00001f00001fe00007f80001ff00003fc00007c00003c0001fc0007f8003fc001ff0001f80001e0000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        63: '15:17:0000000000000000000000000000000f80003fe0003ff0003ff80030f80000f80000f80000f80001f00003e00007e00007c0000f80000f80000000000000000f80000f80000f80000f80000f8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        64: '25:27:000000000000000000000000000000000000000000000000001e000000ffc00003ffe00007c0f0000f0038000e001c001c000c00187fce00387fc60030e3c60030e1c60031c1c60031c1c60031c1c60030e1ce0030e3dc0038fffc00187ff8001c3dc0001c0000000f0020000780e00003ffe00001ffc000003f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        65: '20:22:00000000000000000000000000000001f80003f80003fc0003fc0007fc0007be0007be000f9e000f1f000f1f001f0f001f0f801fff803fff803fffc03fffc07c03c07c03e07803e0f803e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        66: '19:21:0000000000000000000000000000003ffc003fff003fff003e1f803e0f803e0f803e0f003fff003ffe003ffe003fff003e0f803e0f803e07803e07803e0f803fff803fff803fff003ffc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        67: '18:20:000000000000000000000000000000007c0003ff0007ff800fff801f83803f00803e00003e00007c00007c00007c00007c00007c00007c00003e00003e00003f00801fe7800fff8007ff8001ff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        68: '21:23:0000000000000000000000000000003ffc003fff003fff803fffc03e0fc03e07e03e03e03e03e03e01f03e01f03e01f03e01e03e03e03e03e03e07e03e0fc03fffc03fff803ffe003ff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        69: '17:19:0000000000000000000000000000003ffe003ffe003ffe003ffe003e00003e00003e00003ffe003ffe003ffe003ffe003e00003e00003e00003e00003e00003ffe003ffe003ffe003ffe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        70: '17:19:0000000000000000000000000000003ffe003ffe003ffe003ffe003e00003e00003e00003ffe003ffe003ffe003ffe003e00003e00003e00003e00003e00003e00003e00003e00003e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        71: '21:23:000000000000000000000000000000007e0003ffc007ffc00fffc01f81c03f00403e00003e00007c00007c00007c1fe07c1fe07c1fe07c03e03e03e03e03e03f03e01fe7e00fffe007ffe001ff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        72: '21:23:0000000000000000000000000000003e03e03e03e03e03e03e03e03e03e03e03e03e03e03fffe03fffe03fffe03fffe03e03e03e03e03e03e03e03e03e03e03e03e03e03e03e03e03e03e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        73: '9:11:000000000000000000003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e00000000000000000000000000000000000000000000000000000000000000000000000000',
        74: '9:11:000000000000000000007c007c007c007c007c007c007c007c007c007c007c007c007c007c007c007c007c007c007c007c007c00fc00f800f000e0000000000000000000000000000000000000000000000000000000',
        75: '20:22:0000000000000000000000000000003e07e03e0fc03e1f803e3f003e7e003efc003ef8003ff0003fe0003fe0003ff0003ff8003ef8003efc003e7e003e3f003e1f803e0fc03e07e03e03f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        76: '16:18:0000000000000000000000000000003e00003e00003e00003e00003e00003e00003e00003e00003e00003e00003e00003e00003e00003e00003e00003e00003ffe003ffe003ffe003ffe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        77: '25:27:00000000000000000000000000000000000000003f80fe003f80fe003f80fe003fc1fe003fc1fe003fe3fe003fe3fe003ee3be003ef7be003e77be003e7f3e003e7f3e003e3e3e003e3e3e003e3e3e003e1c3e003e003e003e003e003e003e003e003e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        78: '21:23:0000000000000000000000000000003f03e03f83e03f83e03f83e03fc3e03fc3e03fe3e03ee3e03ef3e03ef3e03e7be03e7be03e3fe03e3fe03e1fe03e1fe03e0fe03e0fe03e07e03e07e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        79: '21:23:00000000000000000000000000000000f80003ff000fff801fffc01f87e03f03e03e03f03e01f07c01f07c01f07c01f07c01f07c01f07c01f03e01f03e03e03f07e01fdfe00fffc007ff8003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        80: '18:20:0000000000000000000000000000003ffc003fff003fff803e1f803e0f803e0f803e07803e0f803e0f803fff803fff003ffe003ff8003e00003e00003e00003e00003e00003e00003e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        81: '21:23:00000000000000000000000000000000f80003ff000fff801fffc01f87e03f03e03e03f03e01f07c01f07c01f07c01f07c01f07c01f07c01f03e01f03e03e03f07e01fdfc00fffc007ff8003fe00001f00000f800007800003c0000000000000000000000000000000000000000000000000000000000000000000000000000000',
        82: '19:21:0000000000000000000000000000003ffc003ffe003fff003e3f003e1f803e0f803e0f003e0f003e3f003ffe003ff8003ffe003e3e003e1f003e1f003e0f803e0f803e07c03e07c03e03e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        83: '18:20:00000000000000000000000000000003f0000ffe001ffe003ffe003e0e003c00003c00003e00003fc0003ff8001ffe000fff0001ff00001f00000f00000f00301f003f3f003fff003ffe001ff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        84: '17:19:000000000000000000000000000000ffff80ffff80ffff80ffff8003e00003e00003e00003e00003e00003e00003e00003e00003e00003e00003e00003e00003e00003e00003e00003e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        85: '20:22:0000000000000000000000000000003e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c01e07c01f07c01fdf800fff800fff0003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        86: '20:22:000000000000000000000000000000f803e07803e07c03c07c07c03c07c03e07803e0f801e0f801f0f001f1f000f1f000f9e000fbe0007be0007fc0007fc0003fc0003f80003f80001f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        87: '28:30:0000000000000000000000000000000000000000781f03e07c1f83e07c1f83c03c1f83c03c1f87c03e3f87c03e3bc7c03e39c7801e39c7801e39cf801f79ef801f71ef800f70ef000f70ef000ff0ff000ff0ff000fe0fe0007e07e0007e07e0007e07e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        88: '19:21:0000000000000000000000000000007c07c03e07c03e0f801f1f000f9f000fbe0007fc0003fc0003f80001f80003f80003fc0007fc000fbe000f9f001f1f001f0f803e0f807c07c07c03e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        89: '18:20:000000000000000000000000000000f00f80f81f00fc1f007c3e003e7e003e7c001ff8001ff8000ff00007f00007e00003e00003e00003e00003e00003e00003e00003e00003e00003e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        90: '18:20:0000000000000000000000000000007fff807fff807fff807fff00003f00003e00007c0000f80001f80001f00003e00007c0000fc0000f80001f00003e00007fff807fff807fff807fff80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        91: '12:14:00000000000000003fc03fc03fc03c003c003c003c003c003c003c003c003c003c003c003c003c003c003c003c003c003c003c003fc03fc03fc000000000000000000000000000000000000000000000000000000000',
        92: '9:11:00000000000000000000e000600070007000700030003800380018001c001c001c000c000e000e000e000600070007000300038003800380000000000000000000000000000000000000000000000000000000000000',
        93: '12:14:00000000000000003f803f803f8007800780078007800780078007800780078007800780078007800780078007800780078007803f803f803f8000000000000000000000000000000000000000000000000000000000',
        94: '21:23:00000000000000000000000000000000f80001fc0001fe0003de00078f000f07801c01c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        95: '13:15:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000fff8fff8fff80000000000000000000000000000000000000000',
        96: '13:15:00000000000038001c000e000600070000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        97: '17:19:00000000000000000000000000000000000000000000000000000000000007c0003ff8003ffc003ffc00203e00001e0007fe001ffe003ffe007c1e007c3e007c3e007c7e007ffe003fde001f9e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        98: '18:20:0000000000000000000000003e00003e00003e00003e00003e00003e38003efc003ffe003fff003f1f003e0f803e0f803e0f803e0f803e0f803e0f803e0f003f1f003fff003ffe003efc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        99: '15:17:00000000000000000000000000000000000000000000000000000000000001e0000ff8001ff8003ff8003e08007c00007c00007c00007c00007c00007c00007e00003f08003ff8001ff80007f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        100: '18:20:000000000000000000000000001f00001f00001f00001f00001f00031f000fdf001fff003fff003e3f007c1f007c1f007c1f007c1f007c1f007c1f003c1f003e3f003fff001fff000fdf00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        101: '17:19:00000000000000000000000000000000000000000000000000000000000001e0000ff8001ffc003ffe003e1e007c1f007c1f007fff007fff007fff007c00007c00003e06003ffe001ffe0007fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        102: '11:13:00000000000000000fe01fe01fe01e001e001e00ffe0ffe0ffe01e001e001e001e001e001e001e001e001e001e001e001e00000000000000000000000000000000000000000000000000000000000000000000000000',
        103: '18:20:0000000000000000000000000000000000000000000000000000000000000300000fdf001fff003fff003e3f007c1f007c1f007c1f007c1f007c1f007c1f003e1f003fff001fff001fff00079f00001f00001f00187e001ffc001ff8000ff000000000000000000000000000000000000000000000000000000000000000000000',
        104: '18:20:0000000000000000000000003e00003e00003e00003e00003e00003e38003efc003ffe003fff003f1f003e1f003e1f003e0f003e0f003e0f003e0f003e0f003e0f003e0f003e0f003e0f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        105: '9:11:00000000000000003e003e003e003e00000000003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e00000000000000000000000000000000000000000000000000000000000000000000000000',
        106: '9:11:00000000000000003e003e003e003e00000000003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003c003c007c00fc00f800f000000000000000000000000000000000000000000000000000',
        107: '17:19:0000000000000000000000003e00003e00003e00003e00003e00003e00003e1f003e3e003e7c003ef8003ff0003fe0003fc0003fe0003ff0003ff0003ef8003e7c003e3e003e1f003e1f80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        108: '9:11:00000000000000003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e00000000000000000000000000000000000000000000000000000000000000000000000000',
        109: '26:28:00000000000000000000000000000000000000000000000000000000000000000000000000000000007038003efcfe003ffffe003fffff003f3f9f003e1f0f003e1f0f003e1e0f003e1e0f003e1e0f003e1e0f003e1e0f003e1e0f003e1e0f003e1e0f003e1e0f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        110: '18:20:0000000000000000000000000000000000000000000000000000000000000038003efc003ffe003fff003f1f003e1f003e1f003e0f003e0f003e0f003e0f003e0f003e0f003e0f003e0f003e0f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        111: '17:19:00000000000000000000000000000000000000000000000000000000000001e0000ff8001ffc003ffe003e3f007c1f007c1f007c0f007c0f007c0f007c1f007c1f003e3e003ffe001ffc0007f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        112: '18:20:0000000000000000000000000000000000000000000000000000000000000038003efc003ffe003fff003f1f003e0f803e0f803e0f803e0f803e0f803e0f803e0f003f1f003fff003ffe003efc003e00003e00003e00003e00003e00003e0000000000000000000000000000000000000000000000000000000000000000000000',
        113: '18:20:0000000000000000000000000000000000000000000000000000000000000300000fdf001fff003fff003e3f007c1f007c1f007c1f007c1f007c1f007c1f003c1f003e3f003fff001fff000fdf00001f00001f00001f00001f00001f00001f00000000000000000000000000000000000000000000000000000000000000000000',
        114: '12:14:000000000000000000000000000000000000000000303ef03ff03ff03f903e003e003e003e003e003e003e003e003e003e003e0000000000000000000000000000000000000000000000000000000000000000000000',
        115: '15:17:00000000000000000000000000000000000000000000000000000000000007c0001ff8003ff8007ff8007808007800007f00003ff0001ff8000ffc00007c00003c00207c003ff8003ff8003ff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        116: '12:14:0000000000000000000000001e001e001e001e001e00ffe0ffe0ffe01e001e001e001e001e001e001e001e001fe01fe01fe007e000000000000000000000000000000000000000000000000000000000000000000000',
        117: '18:20:0000000000000000000000000000000000000000000000000000000000003c1f003c1f003c1f003c1f003c1f003c1f003c1f003c1f003c1f003c1f003e1f003f7f003fff001fff000fdf00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        118: '16:18:000000000000000000000000000000000000000000000000000000000000781f00781e007c1e003c3e003c3c003e3c001e7c001e78001f78000ff8000ff00007f00007f00007e00003e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        119: '23:25:00000000000000000000000000000000000000000000000000000000000000000000000000000000783c3c007c7c3c003c7c7c003c7c7c003c7e78003c6e78003eee78001eeef8001ee6f0001ee7f0001fc7f0000fc7f0000fc7e0000fc3e0000f83e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        120: '16:18:0000000000000000000000000000000000000000000000000000000000007c3e003c3c003e7c001f78000ff0000ff00007e00007e00007f0000ff0001ff8001e7c003e3c007c3e00781f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        121: '16:18:000000000000000000000000000000000000000000000000000000000000781f00781e007c1e003c3e003c3c001e3c001e7c001f78000f78000f78000ff00007f00007f00003e00003e00003e00003c00007c0001f80001f80001f0000000000000000000000000000000000000000000000000000000000000000000000000000',
        122: '15:17:0000000000000000000000000000000000000000000000000000000000007ff8007ff8007ff80000f80001f00003e00003e00007c0000f80001f00003e00007ff8007ff8007ff8007ff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        123: '18:20:000000000000000000000000007e0000fe0001fe0001f00001e00001e00001e00001e00001e00001e00003e0001fc0001f80001fc00007e00001e00001e00001e00001e00001e00001e00001e00001fe0000fe0000fe00001e00000000000000000000000000000000000000000000000000000000000000000000000000000000',
        124: '9:11:00000000000000001c001c001c001c001c001c001c001c001c001c001c001c001c001c001c001c001c001c001c001c001c001c001c001c001c001c001c001c0000000000000000000000000000000000000000000000',
        125: '18:20:0000000000000000000000001f80001fc0001fe00003e00001e00001e00001e00001e00001e00001e00001f00001fe00007e0000fe0001f80001e00001e00001e00001e00001e00001e00003e0001fe0001fc0001fc0001e0000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        126: '21:23:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000fc0401ff9c01fffc0183f80100f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        160: '9:11:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        161: '11:13:00000000000000000000000000000000000000000f000f000f000f000f00000000000e000f000f000f000f000f000f000f000f000f000f000f000f000000000000000000000000000000000000000000000000000000',
        162: '18:20:00000000000000000000000000000000000000600000600000600000600000f00007fc000ffc001ffc001f64003e60003e60003e60003e60003e60003e60001f60001fe4000ffc000ffc0003fc00006000006000006000006000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        163: '18:20:00000000000000000000000000000000fc0003fe0007fe0007fe0007c0000f80000f80000f80000f80000f80003ff8003ff8003ff8000f80000f80000f80000f80003ffe003ffe003ffe003ffe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        164: '16:18:000000000000000000000000000000000000000000000000000000000000300c00799e003ffc001ff8001e78001c38001818001818001c38001c38001ff8003ffc007bde00700e00200400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        165: '18:20:0000000000000000000000000000007c0f807c1f003e1f003e3e001f3c000ffc000ff8007fff807fff807fff8003e00003e0007fff807fff8003e00003e00003e00003e00003e00003e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        166: '9:11:0000000000000000000000001c001c001c001c001c001c001c001c001c001c001c000000000000001c001c001c001c001c001c001c001c001c001c001c00000000000000000000000000000000000000000000000000',
        167: '13:15:000000000000000000000f803fe03fe07c6078007c003f001fc03fe07bf0f0f0f078f070f8707ef03fe01fc007e001e000f071e07fe07fc00f0000000000000000000000000000000000000000000000000000000000',
        168: '13:15:000000000000000039c039c039c039c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        169: '25:27:0000000000000000000000000000000000000000007f000001ffc00003c0e00007007000061f30000c7f18000cff18000ce0080008e00c0019e00c0019e00c0008e00c000cf018000cff18000e7f1800061e30000380700001c1e00000ff8000003f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        170: '14:16:000000000000000000000f801fe01ff0007007f01ff03c70387038f03ff01f70000000003ff03ff03ff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        171: '16:18:000000000000000000000000000000000000000000000000000000000000000000000000010400031c000f3c001e78003cf00038e00038e0003cf0000f3c00071c00030c00010400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        172: '21:23:0000000000000000000000000000000000000000000000000000000000000000000000000000001fffc01fffc01fffc00000c00000c00000c00000c00000c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        173: '1:3:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        174: '25:27:0000000000000000000000000000000000000000007f000001ffc00003c0e00007007000067e30000c7f18000c6398000c63880008670c00187f0c00187e0c0008660c000c6718000c6318000e639800060030000380700001c1e00000ff8000003f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        175: '13:15:00000000000000003fc03fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        176: '13:15:000000000000000000000f001f8019c030c030c030c018c01f800f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        177: '21:23:0000000000000000000000000000000000000000000000000070000070000070000070000070001fffc01fffc01fffc01fffc00070000070000070000070000000000000001fffc01fffc01fffc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        178: '11:13:000000000000000000001e007f80738001c00380038007000e001c0038007fc07fc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        179: '11:13:000000000000000000003e007f806380038003801f001f8003c001c043c07f807f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        180: '13:15:00000000000001e001c003800700060000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        181: '19:21:0000000000000000000000000000000000000000000000000000000000003e0f003e0f003e0f003e0f003e0f003e0f003e0f003e0f003e0f003e1f003e1f003f3f403fffc03ff7c03ff7c03e00003e00003e00003e00003e00003e0000000000000000000000000000000000000000000000000000000000000000000000000000',
        182: '16:18:0000000000000000000000000000000ffc001ffc003f9c003f9c003f9c003f9c003f9c003f9c003f9c001f9c00079c00019c00019c00019c00019c00019c00019c00019c00019c00019c00019c00019c00019c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        183: '10:12:00000000000000000000000000000000000000000000000000001e001e001e001e001e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        184: '13:15:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000300010001801f801f00000000000000000000000000000000000000000000000000',
        185: '11:13:000000000000000000000e003e003e000e000e000e000e000e000e000e003fc03fc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        186: '14:16:0000000000000000000007801fe03ff0387038787878787838783cf01ff00fe0000000003ff03ff03ff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        187: '16:18:00000000000000000000000000000000000000000000000000000000000000000000000030c00038e0003cf0001e78000f3c00030c00071c000f3c001e78003ce00030c000208000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        188: '26:28:00000000000000000000000000000000000000000e0070003e0070003e00e0000e00c0000e01c0000e0180000e0380000e0300000e0700000e0e1c003fce1c003fdc3c00001c7c0000387c000030dc0000719c0000619c0000e1ff0000c1ff0001c01c0003801c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        189: '26:28:00000000000000000000000000000000000000000e0070003e0070003e00e0000e00c0000e01c0000e0180000e0380000e0300000e0700000e0e3c003fceff003fdce700001c0380003807000030070000700e0000601c0000e0380000c0700001c0ff800380ff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        190: '26:28:00000000000000000000000000000000000000003e0070007f8070006380e0000380c0000381c0001f0180001f83800003c3000001c7000043ce1c007f8e1c007f1c3c00001c7c0000387c000030dc0000719c0000619c0000e1ff0000c1ff0001c01c0003801c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        191: '15:17:00000000000000000000000000000000000000000000000000000000000003c00003c00003c00003c00003c00000000000000003c00003c00007c0000f80001f00003e00003e00003c00003c08003e38003ff8001ff8000ff800000000000000000000000000000000000000000000000000000000000000000000000000000000',
        192: '20:22:03800001c00000e00000600000000000000001f80003f80003fc0003fc0007fc0007be0007be000f9e000f1f000f1f001f0f001f0f801fff803fff803fffc03fffc07c03c07c03e07803e0f803e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        193: '20:22:00380000780000700000e00000000000000001f80003f80003fc0003fc0007fc0007be0007be000f9e000f1f000f1f001f0f001f0f801fff803fff803fffc03fffc07c03c07c03e07803e0f803e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        194: '20:22:00f00001f800039800070c0000000000000001f80003f80003fc0003fc0007fc0007be0007be000f9e000f1f000f1f001f0f001f0f801fff803fff803fffc03fffc07c03c07c03e07803e0f803e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        195: '20:22:018c0003ec00067c0006380000000000000001f80003f80003fc0003fc0007fc0007be0007be000f9e000f1f000f1f001f0f001f0f801fff803fff803fffc03fffc07c03c07c03e07803e0f803e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        196: '20:22:039c00039c00039c00039c0000000000000001f80003f80003fc0003fc0007fc0007be0007be000f9e000f1f000f1f001f0f001f0f801fff803fff803fffc03fffc07c03c07c03e07803e0f803e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        197: '20:22:00e00001f00003980003180003180001b80001f80003f80003fc0003fc0007fc0007be0007be000f9e000f1f000f1f001f0f001f0f801fff803fff803fffc03fffc07c03c07c03e07803e0f803e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        198: '27:29:000000000000000000000000000000000000000001ffff8001ffff8001ffff8003efff8003cf800007cf800007cf8000078fff800f8fff800f8fff800f0fff801fff80001fff80003fff80003fff80003c0f80007c0fffc07c0fffc0780fffc0f80fffc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        199: '18:20:000000000000000000000000000000007c0003ff0007ff800fff801f83803f00803e00003e00007c00007c00007c00007c00007c00007c00003e00003e00003f00801fe7800fff8007ff8001ff00001800000800000c0000fc0000f800000000000000000000000000000000000000000000000000000000000000000000000000',
        200: '17:19:07000003800001c00000c0000000000000003ffe003ffe003ffe003ffe003e00003e00003e00003ffe003ffe003ffe003ffe003e00003e00003e00003e00003e00003ffe003ffe003ffe003ffe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        201: '17:19:00700000f00000e00001c0000000000000003ffe003ffe003ffe003ffe003e00003e00003e00003ffe003ffe003ffe003ffe003e00003e00003e00003e00003e00003ffe003ffe003ffe003ffe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        202: '17:19:01e00003f0000730000e18000000000000003ffe003ffe003ffe003ffe003e00003e00003e00003ffe003ffe003ffe003ffe003e00003e00003e00003e00003e00003ffe003ffe003ffe003ffe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        203: '17:19:0738000738000738000738000000000000003ffe003ffe003ffe003ffe003e00003e00003e00003ffe003ffe003ffe003ffe003e00003e00003e00003e00003e00003ffe003ffe003ffe003ffe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        204: '9:11:700038001c000c00000000003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e0000000000000000000000000000000000000000000000000000000000000000000000',
        205: '9:11:07000f000e001c00000000003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e0000000000000000000000000000000000000000000000000000000000000000000000',
        206: '9:11:1e003f007300e180000000003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e0000000000000000000000000000000000000000000000000000000000000000000000',
        207: '9:11:7380738073807380000000003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e0000000000000000000000000000000000000000000000000000000000000000000000',
        208: '21:23:0000000000000000000000000000001ffc001fff001fff801fffc01e07e01e03e01e03e01e01f0ffc1f0ffc1f0ffc1f0ffc1f01e01f01e03e01e07e01e0fc01fffc01fff801fff001ff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        209: '21:23:018c0003ec00067c000638000000000000003f03e03f83e03f83e03f83e03fc3e03fc3e03fe3e03ee3e03ef3e03ef3e03e7be03e7be03e3fe03e3fe03e1fe03e1fe03e0fe03e0fe03e07e03e07e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        210: '21:23:01c00000e00000700000300000000000f80003ff000fff801fffc01f87e03f03e03e03f03e01f07c01f07c01f07c01f07c01f07c01f07c01f03e01f03e03e03f07e01fdfe00fffc007ff8003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        211: '21:23:001c00003c0000380000700000000000f80003ff000fff801fffc01f87e03f03e03e03f03e01f07c01f07c01f07c01f07c01f07c01f07c01f03e01f03e03e03f07e01fdfe00fffc007ff8003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        212: '21:23:00780000fc0001cc0003860000000000f80003ff000fff801fffc01f87e03f03e03e03f03e01f07c01f07c01f07c01f07c01f07c01f07c01f03e01f03e03e03f07e01fdfe00fffc007ff8003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        213: '21:23:00c60001f600033e00031c0000000000f80003ff000fff801fffc01f87e03f03e03e03f03e01f07c01f07c01f07c01f07c01f07c01f07c01f03e01f03e03e03f07e01fdfe00fffc007ff8003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        214: '21:23:01ce0001ce0001ce0001ce0000000000f80003ff000fff801fffc01f87e03f03e03e03f03e01f07c01f07c01f07c01f07c01f07c01f07c01f03e01f03e03e03f07e01fdfe00fffc007ff8003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        215: '21:23:0000000000000000000000000000000000000000000000000000000401000e01801e03c00f0780078f0003de0001fc0000f80000f80001fc0003fe0003df00078f000f07801e03c00c0180000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        216: '21:23:00000000000000000000000000f81003ff300ffff01fffe01f87e03f03e03e07f03e0ff07c1df07c39f07c31f07c61f07ce1f07dc1f03f81f03f03e03f07e01fdfe03fffc077ff8063fe00400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        217: '20:22:03800001c00000e0000060000000000000003e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c01e07c01f07c01fdf800fff800fff0003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        218: '20:22:00380000780000700000e0000000000000003e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c01e07c01f07c01fdf800fff800fff0003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        219: '20:22:00780000fc0001cc000386000000000000003e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c01e07c01f07c01fdf800fff800fff0003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        220: '20:22:01ce0001ce0001ce0001ce000000000000003e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c03e07c01e07c01f07c01fdf800fff800fff0003fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        221: '18:20:00e00001e00001c000038000000000000000f00f80f81f00fc1f007c3e003e7e003e7c001ff8001ff8000ff00007f00007e00003e00003e00003e00003e00003e00003e00003e00003e00003e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        222: '19:21:0000000000000000000000000000003e00003e00003e00003ff8003ffe003fff003fff803e0f803e0f803e07803e0f803e0f803e1f803fff803fff003ffe003e00003e00003e00003e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        223: '18:20:00000000000000000000000007f8000ffc001ffe003e1e003e1e003e1e003e7e003ef0003ef0003ef0003ef8003efc003e7f003e3f003e1f803e0f803e07803e0f803eff803eff003efe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        224: '17:19:0000000000000000000e000007000003800001800001c00000000007c0003ff8003ffc003ffc00203e00001e0007fe001ffe003ffe007c1e007c3e007c3e007c7e007ffe003fde001f9e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        225: '17:19:00000000000000000000780000700000e00001c00001800000000007c0003ff8003ffc003ffc00203e00001e0007fe001ffe003ffe007c1e007c3e007c3e007c7e007ffe003fde001f9e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        226: '17:19:00000000000000000003c00003e0000770000e30000c180000000007c0003ff8003ffc003ffc00203e00001e0007fe001ffe003ffe007c1e007c3e007c3e007c7e007ffe003fde001f9e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        227: '17:19:0000000000000000000000000718000790000df0000c700000000000000007c0003ff8003ffc003ffc00203e00001e0007fe001ffe003ffe007c1e007c3e007c3e007c7e007ffe003fde001f9e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        228: '17:19:0000000000000000000000000e70000e70000e70000e700000000000000007c0003ff8003ffc003ffc00203e00001e0007fe001ffe003ffe007c1e007c3e007c3e007c7e007ffe003fde001f9e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        229: '17:19:00000001c00003e00007700006300006300006700003e00001c00000000007c0003ff8003ffc003ffc00203e00001e0007fe001ffe003ffe007c1e007c3e007c3e007c7e007ffe003fde001f9e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        230: '26:28:0000000000000000000000000000000000000000000000000000000000000000000000000000000007c0f0003ff3fc003ffffe003fffff00203f0f80001e0f8007fe07801fffff803fffff807c1fff807c3e00007c3e00807c7f03807fffff803fe7ff801fc3fe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        231: '15:17:00000000000000000000000000000000000000000000000000000000000001e0000ff8001ff8003ff8003e08007c00007c00007c00007c00007c00007c00007e00003f08003ff8001ff80007f80000c00000400000600007e00007c000000000000000000000000000000000000000000000000000000000000000000000000000',
        232: '17:19:00000000000000000007000003800001c00000c00000e00000000001e0000ff8001ffc003ffe003e1e007c1f007c1f007fff007fff007fff007c00007c00003e06003ffe001ffe0007fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        233: '17:19:000000000000000000003c0000380000700000e00000c00000000001e0000ff8001ffc003ffe003e1e007c1f007c1f007fff007fff007fff007c00007c00003e06003ffe001ffe0007fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        234: '17:19:00000000000000000001e00001f00003b800071800060c0000000001e0000ff8001ffc003ffe003e1e007c1f007c1f007fff007fff007fff007c00007c00003e06003ffe001ffe0007fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        235: '17:19:00000000000000000000000007380007380007380007380000000000000001e0000ff8001ffc003ffe003e1e007c1f007c1f007fff007fff007fff007c00007c00003e06003ffe001ffe0007fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        236: '9:11:000000000000e0007000380018001c00000000003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e00000000000000000000000000000000000000000000000000000000000000000000000000',
        237: '9:11:000000000000078007000e001c001800000000003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e00000000000000000000000000000000000000000000000000000000000000000000000000',
        238: '9:11:00000000000078007c00ee00c6008300000000007c007c007c007c007c007c007c007c007c007c007c007c007c007c007c00000000000000000000000000000000000000000000000000000000000000000000000000',
        239: '9:11:0000000000000000e700e700e700e7000000000000003e003e003e003e003e003e003e003e003e003e003e003e003e003e003e0000000000000000000000000000000000000000000000000000000000000000000000',
        240: '17:19:000000000000000000000000078e0003fe0003f0001ff0001cf000007800003c000ffe001ffe003fff003e1f007c1f007c0f007c0f007c0f007c1f007c1f003e3e003ffe001ffc0007f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        241: '18:20:000000000000000000000000038c0003c80006f8000638000000000000000038003efc003ffe003fff003f1f003e1f003e1f003e0f003e0f003e0f003e0f003e0f003e0f003e0f003e0f003e0f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        242: '17:19:00000000000000000007000003800001c00000c00000e00000000001e0000ff8001ffc003ffe003e3f007c1f007c1f007c0f007c0f007c0f007c1f007c1f003e3e003ffe001ffc0007f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        243: '17:19:000000000000000000003c0000380000700000e00000c00000000001e0000ff8001ffc003ffe003e3f007c1f007c1f007c0f007c0f007c0f007c1f007c1f003e3e003ffe001ffc0007f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        244: '17:19:00000000000000000003c00003e0000770000e30000c180000000001e0000ff8001ffc003ffe003e3f007c1f007c1f007c0f007c0f007c0f007c1f007c1f003e3e003ffe001ffc0007f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        245: '17:19:0000000000000000000000000718000790000df0000c700000000000000001e0000ff8001ffc003ffe003e3f007c1f007c1f007c0f007c0f007c0f007c1f007c1f003e3e003ffe001ffc0007f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        246: '17:19:0000000000000000000000000e70000e70000e70000e700000000000000001e0000ff8001ffc003ffe003e3f007c1f007c1f007c0f007c0f007c0f007c1f007c1f003e3e003ffe001ffc0007f800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        247: '21:23:0000000000000000000000000000000000000000000000000000000070000070000070000070000000000000001fffc01fffc01fffc0000000000000007000007000007000007000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        248: '17:19:00000000000000000000000000000000000000000000000000000000000001e3000fff001ffe003ffe003e3f007c3f007c7f007cef007dcf007f8f007f1f003e1f003e3e003ffe003ffc0077f800600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        249: '18:20:00000000000000000007000003800001c00000c00000e0000000000000003c1f003c1f003c1f003c1f003c1f003c1f003c1f003c1f003c1f003c1f003e1f003f7f003fff001fff000fdf00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        250: '18:20:000000000000000000003c0000380000700000e00000c0000000000000003c1f003c1f003c1f003c1f003c1f003c1f003c1f003c1f003c1f003c1f003e1f003f7f003fff001fff000fdf00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        251: '18:20:00000000000000000001e00001f00003b800071800060c000000000000003c1f003c1f003c1f003c1f003c1f003c1f003c1f003c1f003c1f003c1f003e1f003f7f003fff001fff000fdf00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        252: '18:20:0000000000000000000000000738000738000738000738000000000000000000003c1f003c1f003c1f003c1f003c1f003c1f003c1f003c1f003c1f003c1f003e1f003f7f003fff001fff000fdf00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        253: '16:18:00000000000000000000780000700000e00001c000018000000000000000781f00781e007c1e003c3e003c3c001e3c001e7c001f78000f78000f78000ff00007f00007f00003e00003e00003e00003c00007c0001f80001f80001f0000000000000000000000000000000000000000000000000000000000000000000000000000',
        254: '18:20:0000000000000000000000003e00003e00003e00003e00003e00003e38003efc003ffe003fff003f1f003e0f803e0f803e0f803e0f803e0f803e0f803e0f003f1f003fff003ffe003efc003e00003e00003e00003e00003e00003e0000000000000000000000000000000000000000000000000000000000000000000000000000',
        255: '16:18:0000000000000000000000000e70000e70000e70000e7000000000000000000000781f00781e007c1e003c3e003c3c001e3c001e7c001f78000f78000f78000ff00007f00007f00003e00003e00003e00003c00007c0001f80001f80001f0000000000000000000000000000000000000000000000000000000000000000000000',
        8364: '18:20:00000000000000000000000000000001f00007fc000ffe001ffe003f06003e02007c0000fff800fff000fff0007c00007c0000ffe000ffc0007c00007e00003e02003f8e001ffe000ffe0003fc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8211: '13:15:00000000000000000000000000000000000000000000000000000000000000007fe07fe07fe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8212: '25:27:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007fffff007fffff007fffff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8222: '17:19:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001e78001e78001e78001e78001e78001c70003c700038e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8220: '17:19:000000000000000000000000000000071c000f3c000e3c001e78001e78001e78001e78001e7800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8221: '17:19:0000000000000000000000000000000f3c000f3c000f3c000f3c001e38001e78001c7000187000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8217: '10:12:000000000000000000001e001e001e001e001c003c0038003800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        8226: '16:18:00000000000000000000000000000000000000000000000000000000000003e00007f0000ff0000ff0000ff0000ff0000ff0000ff00007e000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        338: '29:31:000000000000000000000000000000000000000001ffffe007ffffe00fffffe01fffffe03f81e0003e01e0003e01e0007c01ffe07c01ffe07c01ffe07c01ffe07c01e0007e01e0003e01e0003f01e0001fc1e0001ffffff00ffffff003fffff000fffff0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        339: '28:30:0000000000000000000000000000000000000000000000000000000000000000000000000000000001c078000ff9fe001fffff003fffff803e3f87c07c1f03c07c1f03c07c0fffc07c0fffc07c0fffc07c1f00007c1f80403e3f81c03fffffc01fffffc007f1ff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        352: '18:20:0e180007300003f00001e00000000003f0000ffe001ffe003ffe003e0e003c00003c00003e00003fc0003ff8001ffe000fff0001ff00001f00000f00000f00301f003f3f003fff003ffe001ff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        353: '15:17:0000000000000000001c60000ce0000fc00007c00003800000000007c0001ff8003ff8007ff8007808007800007f00003ff0001ff8000ffc00007c00003c00207c003ff8003ff8003ff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        381: '18:20:0e180007300003f00001e0000000000000007fff807fff807fff807fff00003f00003e00007c0000f80001f80001f00003e00007c0000fc0000f80001f00003e00007fff807fff807fff807fff80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        382: '15:17:0000000000000000001c60000ce0000fc00007c0000380000000000000007ff8007ff8007ff80000f80001f00003e00003e00007c0000f80001f00003e00007ff8007ff8007ff8007ff800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
    },
}


def br_ink(rows, x, y):
    # brother_ql reverses pixels horizontally before writing 90-byte raster lines.
    if x < 0 or x >= 696 or y < 0 or y >= len(rows):
        return
    bit_x = 707 - x  # original 696 dots at position 12 in 720-dot head, mirrored
    b = bit_x // 8
    rows[y][b] = rows[y][b] | (1 << (7 - (bit_x % 8)))


def br_text_width(value, kind):
    mp = BR_FONT_GLYPHS[kind]
    w = 0
    for c in str(value or ''):
        spec = mp.get(ord(c), mp.get(63))
        w += int(spec.split(':', 1)[0])
    return w


def br_text(rows, value, kind, x, y):
    mp = BR_FONT_GLYPHS[kind]
    glyph_height = BR_FONT_HEIGHTS[kind]
    xpos = x
    for c in str(value or ''):
        spec = mp.get(ord(c), mp.get(63))
        pieces = spec.split(':', 2)
        advance = int(pieces[0])
        width = int(pieces[1])
        if xpos + width > 690:
            raise Exception('Brother Raster-Text zu breit: ' + str(value)[:70])
        ink = bytes.fromhex(pieces[2])
        stride = (width + 7) // 8
        for ry in range(glyph_height):
            y2 = y + ry
            if y2 < 0 or y2 >= len(rows):
                continue
            off = ry * stride
            for bx in range(stride):
                val = ink[off + bx]
                if val:
                    for bit in range(8):
                        if val & (128 >> bit) and bx * 8 + bit < width:
                            br_ink(rows, xpos + bx * 8 + bit, y2)
        xpos += advance
    return xpos


def br_rectangle(rows, x1, y1, x2, y2, thick):
    for d in range(thick):
        for x in range(x1, x2 + 1):
            br_ink(rows, x, y1 + d)
            br_ink(rows, x, y2 - d)
        for y in range(y1, y2 + 1):
            br_ink(rows, x1 + d, y)
            br_ink(rows, x2 - d, y)


def br_clear(rows, x, y):
    if x < 0 or x >= 696 or y < 0 or y >= len(rows):
        return
    bit_x = 707 - x
    b = bit_x // 8
    rows[y][b] = rows[y][b] & (255 - (1 << (7 - (bit_x % 8))))


def br_seg(rows, x0, y0, x1, y1, th):
    n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
    h = th // 2
    for k in range(n + 1):
        x = int(round(x0 + (x1 - x0) * k / float(n)))
        y = int(round(y0 + (y1 - y0) * k / float(n)))
        for a in range(th):
            for b in range(th):
                br_ink(rows, x + a - h, y + b - h)


def br_polyline(rows, pts, th):
    for k in range(len(pts) - 1):
        br_seg(rows, pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1], th)


def br_fill_poly(rows, pts, dither):
    if len(pts) < 3:
        return
    ys = [p[1] for p in pts]
    y_min = int(min(ys))
    y_max = int(max(ys))
    for y in range(y_min, y_max + 1):
        yc = y + 0.5
        xs = []
        for k in range(len(pts)):
            a = pts[k]
            b = pts[(k + 1) % len(pts)]
            if (a[1] <= yc < b[1]) or (b[1] <= yc < a[1]):
                xs.append(a[0] + (yc - a[1]) * (b[0] - a[0]) / float(b[1] - a[1]))
        xs.sort()
        for k in range(0, len(xs) - 1, 2):
            for x in range(int(round(xs[k])), int(round(xs[k + 1])) + 1):
                if not dither or (x + y) % 2 == 0:
                    br_ink(rows, x, y)


def br_path_polys(d, sc, x0, y0):
    toks = []
    cur = ''
    for ch in str(d or ''):
        if ch in 'MLQZmlqz':
            if cur.strip():
                toks.append(cur.strip())
            toks.append(ch.upper())
            cur = ''
        elif ch in ' ,':
            if cur:
                toks.append(cur)
            cur = ''
        else:
            cur += ch
    if cur.strip():
        toks.append(cur.strip())
    polys = []
    pl = []
    i = 0
    cmd = 'M'
    px = 0.0
    py = 0.0
    sx = 0.0
    sy = 0.0
    while i < len(toks):
        t = toks[i]
        if t in ('M', 'L', 'Q', 'Z'):
            cmd = t
            i += 1
            if t == 'Z':
                pl.append((sx, sy))
                polys.append(pl)
                pl = []
            continue
        if cmd == 'M':
            px = float(toks[i])
            py = float(toks[i + 1])
            i += 2
            if pl:
                polys.append(pl)
            pl = [(px, py)]
            sx = px
            sy = py
            cmd = 'L'
        elif cmd == 'L':
            px = float(toks[i])
            py = float(toks[i + 1])
            i += 2
            pl.append((px, py))
        elif cmd == 'Q':
            cx = float(toks[i])
            cy = float(toks[i + 1])
            ex = float(toks[i + 2])
            ey = float(toks[i + 3])
            i += 4
            for k in range(1, 9):
                tt = k / 8.0
                pl.append(((1 - tt) * (1 - tt) * px + 2 * (1 - tt) * tt * cx + tt * tt * ex,
                           (1 - tt) * (1 - tt) * py + 2 * (1 - tt) * tt * cy + tt * tt * ey))
            px = ex
            py = ey
        else:
            i += 1
    if pl:
        polys.append(pl)
    out = []
    for pl in polys:
        sp = []
        for p in pl:
            sp.append((x0 + p[0] * sc, y0 + p[1] * sc))
        out.append(sp)
    return out


def svg_attr(e, name):
    k = ' ' + name + '="'
    if k not in e:
        return ''
    return e.split(k, 1)[1].split('"', 1)[0]


def zone_pts(z, sc, x0, y0):
    if z[1] == 'r':
        q = [int(v) for v in z[2].split(' ')]
        pts = [(q[0], q[1]), (q[0] + q[2], q[1]), (q[0] + q[2], q[1] + q[3]), (q[0], q[1] + q[3])]
    else:
        pts = [(int(p.split(',')[0]), int(p.split(',')[1])) for p in z[2].split(' ')]
    out = []
    for p in pts:
        out.append((x0 + p[0] * sc, y0 + p[1] * sc))
    return out


def br_fill_rect(rows, x1, y1, x2, y2):
    for yy in range(int(y1), int(y2) + 1):
        for xx in range(int(x1), int(x2) + 1):
            br_ink(rows, xx, yy)


def br_text_inv(rows, value, kind, x, y):
    # White text on a black bar (clears the glyph pixels).
    mp = BR_FONT_GLYPHS[kind]
    glyph_height = BR_FONT_HEIGHTS[kind]
    xpos = x
    for c in str(value or ''):
        spec = mp.get(ord(c), mp.get(63))
        pieces = spec.split(':', 2)
        advance = int(pieces[0])
        width = int(pieces[1])
        ink = bytes.fromhex(pieces[2])
        stride = (width + 7) // 8
        for ry in range(glyph_height):
            y2 = y + ry
            if y2 < 0 or y2 >= len(rows):
                continue
            off = ry * stride
            for bx in range(stride):
                val = ink[off + bx]
                if val:
                    for bit in range(8):
                        if val & (128 >> bit) and bx * 8 + bit < width:
                            br_clear(rows, xpos + bx * 8 + bit, y2)
        xpos += advance
    return xpos


def br_marker(rows, t, bx0, by0, bx1, by1, ox, oy, W, H):
    # Defect number in a white disc with black ring; next to small places so the place itself stays visible.
    tw = br_text_width(t, 'p')
    r = max(24, tw // 2 + 9)
    mp = marker_pos(bx0 - ox, by0 - oy, bx1 - ox, by1 - oy, W, H, r)
    cx = int(ox + mp[0])
    cy = int(oy + mp[1])
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            dd = dx * dx + dy * dy
            if dd <= r * r:
                if dd >= (r - 4) * (r - 4):
                    br_ink(rows, cx + dx, cy + dy)
                else:
                    br_clear(rows, cx + dx, cy + dy)
    br_text(rows, t, 'p', cx - tw // 2, cy - 20)


def br_drawing_custom(rows, g, view, marks, nums, x0, y0, wpx):
    # Own drawing: 1-bit line raster from "Zeichnungen einrichten" + shaded places + numbers.
    c = cdraw(g[1:]).get(view)
    if not c:
        return
    W = c['w']
    H = c['h']
    sc = wpx / float(W)
    hpx = int(H * sc)
    x0 = int(x0)
    y0 = int(y0)
    braw = (c['bits'].raw or b'') if c['bits'] else b''
    if braw[:4] == b'IQB1':
        bw = braw[4] * 256 + braw[5]
        bh = braw[6] * 256 + braw[7]
        stride = (bw + 7) // 8
        data = braw[8:]
        if bw and bh and len(data) >= stride * bh:
            for ty in range(hpx):
                sy = int(ty * bh / float(hpx))
                if sy >= bh:
                    continue
                ro = sy * stride
                for tx in range(wpx):
                    sx = int(tx * bw / float(wpx))
                    if data[ro + (sx >> 3)] & (128 >> (sx & 7)):
                        br_ink(rows, x0 + tx, y0 + ty)
    else:
        br_polyline(rows, [(x0, y0), (x0 + wpx, y0), (x0 + wpx, y0 + hpx), (x0, y0 + hpx), (x0, y0)], 2)
    for z in c['z']:
        if z[0] in marks:
            pts = [(x0 + z[2] * sc, y0 + z[3] * sc), (x0 + (z[2] + z[4]) * sc, y0 + z[3] * sc),
                   (x0 + (z[2] + z[4]) * sc, y0 + (z[3] + z[5]) * sc), (x0 + z[2] * sc, y0 + (z[3] + z[5]) * sc)]
            br_fill_poly(rows, pts, True)
            br_polyline(rows, pts + [pts[0]], 4)
    for z in c['z']:
        if z[0] in marks and z[0] in nums:
            br_marker(rows, nums[z[0]], x0 + z[2] * sc, y0 + z[3] * sc, x0 + (z[2] + z[4]) * sc, y0 + (z[3] + z[5]) * sc, x0, y0, wpx, hpx)
    sd = LOC_SIDE.get(view, ['R', 'L'])
    br_text(rows, sd[0], 'p', x0, y0)
    br_text(rows, sd[1], 'p', int(x0 + wpx - br_text_width(sd[1], 'p')), y0)


def br_drawing(rows, g, view, marks, nums, x0, y0, wpx):
    # Same drawing as the PDF: garment outline + details, marked places shaded, defect numbers in white discs.
    if is_custom(g):
        br_drawing_custom(rows, g, view, marks, nums, x0, y0, wpx)
        return
    pr = LOC_PROD.get(g) or LOC_PROD['gen']
    sc = wpx / 240.0
    geo = pr.get(view, [])
    for z in geo:
        if z[0] in marks:
            br_fill_poly(rows, zone_pts(z, sc, x0, y0), True)
    for pl in br_path_polys(pr['out'], sc, x0, y0):
        br_polyline(rows, pl, 3)
    for e in str(pr['deco'].get(view, '')).split('<')[1:]:
        tag = e.split(' ', 1)[0]
        cls = svg_attr(e, 'class')
        if cls in ('lq', 'lmg', 'llg', 'ldk', 'llt') or tag in ('text', '/text'):
            continue
        if tag == 'path':
            for pl in br_path_polys(svg_attr(e, 'd'), sc, x0, y0):
                br_polyline(rows, pl, 2)
        elif tag == 'line':
            br_seg(rows, x0 + float(svg_attr(e, 'x1')) * sc, y0 + float(svg_attr(e, 'y1')) * sc,
                   x0 + float(svg_attr(e, 'x2')) * sc, y0 + float(svg_attr(e, 'y2')) * sc, 2)
        elif tag == 'rect':
            rx = x0 + float(svg_attr(e, 'x')) * sc
            ry = y0 + float(svg_attr(e, 'y')) * sc
            rw = float(svg_attr(e, 'width')) * sc
            rh = float(svg_attr(e, 'height')) * sc
            br_polyline(rows, [(rx, ry), (rx + rw, ry), (rx + rw, ry + rh), (rx, ry + rh), (rx, ry)], 2)
        elif tag == 'circle':
            ccx = x0 + float(svg_attr(e, 'cx')) * sc
            ccy = y0 + float(svg_attr(e, 'cy')) * sc
            cr = float(svg_attr(e, 'r')) * sc
            cps = []
            for k in range(17):
                cps.append((ccx + cr * BR_COS[k % 16], ccy + cr * BR_SIN[k % 16]))
            br_polyline(rows, cps, 2)
    for z in geo:
        if z[0] in marks:
            pts = zone_pts(z, sc, x0, y0)
            br_polyline(rows, pts + [pts[0]], 3)
    for z in geo:
        if z[0] in marks and z[0] in nums:
            pts = zone_pts(z, sc, x0, y0)
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            br_marker(rows, nums[z[0]], min(xs), min(ys), max(xs), max(ys), x0, y0, wpx, int((pr['B'] + 6) * sc))
    sd = LOC_SIDE.get(view, ['R', 'L'])
    br_text(rows, sd[0], 'p', int(x0), int(y0))
    br_text(rows, sd[1], 'p', int(x0 + wpx - br_text_width(sd[1], 'p')), int(y0))


BR_COS = [1.0, 0.924, 0.707, 0.383, 0.0, -0.383, -0.707, -0.924, -1.0, -0.924, -0.707, -0.383, 0.0, 0.383, 0.707, 0.924]
BR_SIN = [0.0, 0.383, 0.707, 0.924, 1.0, 0.924, 0.707, 0.383, 0.0, -0.383, -0.707, -0.924, -1.0, -0.924, -0.707, -0.383]


def brother_raw_label(al):
    # Draw all the same fields used by PDF: QA code, DEFEKT, size, article,
    # separate numbered reasons, full product, date and inspector.
    layout = label_layout(al)
    plan = []
    y = 88
    for line in layout['sku']:
        plan.append((line, 'a', 28, y))
        y += 44
    y += 3
    for gi, group in enumerate(layout['reasons']):
        for line in group:
            # A reason wraps exactly as in the PDF. No cropping or shortening.
            if line.startswith('» ') or line.startswith('   '):
                kind = 'a'
                if br_text_width(line, kind) > 650:
                    raise Exception('Ort ist zu breit fuer Brother RAW: ' + str(line)[:70])
                plan.append((line, kind, 28, y))
                y += 47
            else:
                kind = 'd'
                if br_text_width(line, 'd') > 620:
                    kind = 'a'
                if br_text_width(line, kind) > 640:
                    raise Exception('Defektgrund ist zu breit fuer Brother RAW: ' + str(line)[:70])
                plan.append((line, kind + 'inv', 30, y + 6))
                y += 68
        if gi < len(layout['reasons']) - 1:
            y += 5
    dtasks = []
    dm = layout.get('draw') or [0, 0]
    dplan = label_draw_plan(al) if dm[1] else ['', []]
    if dplan[1]:
        y += 10
        wv = int(dm[0] * BR_RAW_DOTS_PER_MM)
        hv = 0
        for vv in dplan[1]:
            hv = max(hv, int(wv * draw_ratio(dplan[0], vv[0])))
        for k, vv in enumerate(dplan[1]):
            dx0 = 28 + k * (wv + 14)
            dtasks.append([vv, dx0, y, wv])
            cap = dict(LOC_VIEWS).get(vv[0], '')
            plan.append((cap, 'p', dx0 + max(0, (wv - br_text_width(cap, 'p')) // 2), y + hv + 2))
        y += hv + 50
    y += 4
    for line in layout['product']:
        plan.append((line, 'p', 28, y))
        y += 35
    y += 3
    for line in layout['foot']:
        plan.append((line, 'p', 28, y))
        y += 35
    # Do not truncate longer labels. Use original PDF mm as a lower bound.
    pixels = max(int(round(layout['mm'] * BR_RAW_DOTS_PER_MM)), y + 16)
    if pixels > 11811:
        raise Exception('Brother RAW Etikett ueber 1000mm: bitte Defekte aufteilen')
    if pixels < 150:
        pixels = 150
    # A Python list of bytes remains usable under Odoo server-action safe_eval.
    rows = [[0] * 90 for n in range(pixels)]
    name = str(al.name or 'QC')
    br_text(rows, name, 'h', 28, 10)
    badge_text = 'DEFEKT'
    badge_width = br_text_width(badge_text, 'p') + 25
    badge_x = max(345, br_text_width(name, 'h') + 58)
    if badge_x + badge_width > 680:
        badge_x = 680 - badge_width
    if badge_x < 345:
        badge_x = 345
    br_rectangle(rows, badge_x, 19, badge_x + badge_width, 68, 3)
    for dt in dtasks:
        br_drawing(rows, dplan[0], dt[0][0], dt[0][1], dt[0][2], dt[1], dt[2], dt[3])
    br_text(rows, badge_text, 'p', badge_x + 12, 20)
    for line, kind, x, yy in plan:
        if kind.endswith('inv'):
            k2 = kind[:-3]
            br_fill_rect(rows, x - 10, yy - 7, x + br_text_width(line, k2) + 12, yy + BR_FONT_HEIGHTS[k2] + 3)
            br_text_inv(rows, line, k2, x, yy)
        else:
            br_text(rows, line, kind, x, yy)
    # Brother QL native raster: auto-select single-colour or dual-colour
    # for the installed 62 mm continuous roll; autocut.
    header = (b'\x1b\x69\x61\x01' + bytes(200) + b'\x1b\x40'
              + b'\x1b\x69\x61\x01' + b'\x1b\x69\x53'
              + b'\x1b\x69\x7a' + bytes([0xCE if BR_TWO_COLOR else 0x8E, 0x0A, 62, 0])
              + pixels.to_bytes(4, 'little') + bytes(2)
              + b'\x1b\x69\x4d\x40' + b'\x1b\x69\x41\x01'
              + b'\x1b\x69\x4b' + bytes([0x09 if BR_TWO_COLOR else 0x08]) + b'\x1b\x69\x64\x23\x00')
    chunks = [header]
    for one_row in rows:
        if BR_TWO_COLOR:
            chunks.append(b'\x77\x01\x5a' + bytes(one_row))
            chunks.append(b'\x77\x02\x5a' + BR_RAW_WHITE_ROW)
        else:
            chunks.append(b'\x67\x00\x5a' + bytes(one_row))
    chunks.append(b'\x1a')  # End of last page: feed and cut.
    raw = b''.join(chunks)
    if len(raw) != 244 + pixels * (186 if BR_TWO_COLOR else 93):
        raise Exception('Brother RAW buffer validation failed')
    return raw


def pn_print(al):
    if not PNP:
        return 'no printer set (iq.qc_printnode_printer_id)'
    printer_name = (PNP.name or '').upper()
    # A Brother label must never fall back to the old CUPS PDF path.
    # The RAW queue must exist and be selected in Odoo's Direct Print printer list.
    if 'BROTHER' in printer_name:
        if '_RAW' not in printer_name and ' RAW' not in printer_name:
            return 'Brother RAW queue not selected. Create Brother_QL_820NWB_RAW in macOS, sync in Direct Print and rerun installer; NO PDF was sent.'
        try:
            payload = brother_raw_label(al)
            data = b64encode(payload).decode()
            # VentorTech's qweb-text path is used by existing ZPL RAW labels.
            # The destination must be a macOS RAW printer queue, not a driver/PDF queue.
            prm = {'title': 'QC ' + al.name + ' Brother DK22251 RAW', 'type': 'qweb-text'}
            try:
                PNP.printnode_print_b64(data, prm, check_printer_format=False)
                return ''
            except Exception as first:
                # Do not repeat a binary print job blindly: risk of duplicate labels.
                return 'Brother RAW dispatch failed: ' + str(first).replace('|', '/')[:160]
        except Exception as exc:
            return 'Brother RAW generation failed: ' + str(exc).replace('|', '/')[:160]
    if MODE == 'pdf':
        pdf, error = render_label_pdf(al)
        if error:
            return error
        data = b64encode(pdf).decode()
        prm = {'title': 'QC ' + al.name, 'type': 'qweb-pdf'}
    else:
        data = b64encode(zpl_label(al).encode('utf-8')).decode()
        prm = {'title': 'QC ' + al.name, 'type': 'qweb-text'}
    try:
        PNP.printnode_print_b64(data, prm, check_printer_format=False)
        return ''
    except Exception as e1:
        try:
            PNP.printnode_print_b64(data, prm)
            return ''
        except Exception as e2:
            return (str(e2) or str(e1) or 'print error').replace('|', '/')[:200]


def pdf_download_response(al):
    if is_note(al):
        return request.make_response('Hinweise bekommen kein Etikett.', status=400)
    pdf, error = render_label_pdf(al)
    if error:
        return request.make_response('Etikett-PDF nicht verfügbar: ' + error, headers=[('Content-Type', 'text/plain; charset=utf-8')], status=500)
    return request.make_response(pdf, headers=[('Content-Type', 'application/pdf'),
        ('Content-Disposition', 'attachment; filename="' + (al.name or 'QC-Etikett').replace('"', '') + '.pdf"'),
        ('Cache-Control', 'private, no-store'), ('X-Content-Type-Options', 'nosniff')])


def label_html(al):
    chk = al.check_id if 'check_id' in AF else False
    p = al.product_id or (chk.product_id if chk else False)
    who = ''
    if 'description' in AF and al.description:
        d = str(al.description)
        if 'Prüfer:' in d:
            who = d.split('Prüfer:')[1].split('<')[0].strip()[:30]
    return ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>' + esc(al.name) + '</title>'
            '<style>@page{size:50mm 30mm;margin:0}*{box-sizing:border-box}body{margin:0;font-family:Arial,sans-serif}'
            '.lb{width:50mm;height:30mm;padding:1.6mm 2.2mm;overflow:hidden;display:flex;flex-direction:column}'
            '.h{display:flex;justify-content:space-between;align-items:baseline}.n{font:800 12pt Arial;line-height:1}.x{font:800 8pt Arial;border:1.2pt solid #000;padding:0 1mm}'
            '.a{font:800 9pt Arial;margin-top:1mm;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
            '.d{font:800 9.5pt Arial;line-height:1.1;margin-top:1mm;max-height:8.6mm;overflow:hidden;flex:1}'
            '.p{font:6.5pt Arial;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.f{font:6pt Arial;color:#222}'
            '.ctl{padding:16px;font-family:Arial}.ctl a,.ctl button{display:block;width:100%;max-width:340px;margin:0 0 10px;padding:16px;border:0;border-radius:12px;font:800 18px Arial;text-align:center;text-decoration:none}'
            '@media print{.ctl{display:none}}@media screen{.lb{border:1px dashed #999;margin:16px;zoom:1.6}}</style></head><body>'
            '<div class="lb"><div class="h"><span class="n">' + esc(al.name) + '</span><span class="x">DEFEKT</span></div>'
            '<div class="a">' + ('Gr. ' + esc(al_size(al)) + ' · Art.-Nr. ' + esc(p.default_code or p.product_tmpl_id.default_code or '–') if p else '') + '</div>'
            '<div class="d">' + esc(', '.join([tl(t) for t in tags_of(al)]) or (al.title if 'title' in AF else '')) + '</div>'
            '<div class="p">' + esc(p.product_tmpl_id.name if p else '') + '</div>'
            '<div class="f">' + loc(al.create_date).strftime('%d.%m.%Y') + (' · ' + esc(who) if who else '') + '</div></div>'
            '<div class="ctl"><button onclick="window.print()" style="background:#151515;color:#fff">Etikett drucken</button>'
            '<a href="' + QB + '&amp;tmpl=' + str(p.product_tmpl_id.id if p else 0) + (('&amp;pick=' + str(al.picking_id.id)) if 'picking_id' in AF and al.picking_id else '') + '" style="background:#e9e9e6;color:#151515">Weiter prüfen</a></div>'
            '<script>setTimeout(function(){window.print()},500)</script></body></html>')



# ------------------------------------------------------------------ v19.16 manager login (same PIN + same cookie as the warehouse calendar)
MPIN_Q = (P.get_param('iq.delivery_calendar_manager_pin') or '').strip()
QSESSION = 1800  # 30 minutes


def msig(exp):
    x = 2166136261
    for ch in (KEY + '|' + PW + '|M|' + MPIN_Q + '|' + str(exp)):
        x = ((x ^ ord(ch)) * 16777619) % 4294967296
    y2 = 2166136261
    for ch in (str(exp) + '#' + MPIN_Q + '#' + PW + '#M'):
        y2 = ((y2 ^ ord(ch)) * 16777619) % 4294967296
    return '%08x%08x' % (x, y2)


NOWTS = int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds())
ADM = False
ADM_LEFT = 0
mcv = (request.httprequest.cookies.get('iq_emp') or '').split('.') if request else []
if len(MPIN_Q) >= 8 and len(mcv) == 3 and mcv[0] == 'M' and mcv[1].isdigit() and int(mcv[1]) >= NOWTS:
    ADM = msig(mcv[1]) == mcv[2]
    ADM_LEFT = (int(mcv[1]) - NOWTS) // 60 if ADM else 0
CAL_URL = '/website/action/iq-delivery-calendar?key=' + KEY
TFV = (P.get_param('iq.qc_pwfail') or '0|0').split('|')
TF_N = int(TFV[0]) if TFV[0].isdigit() else 0
TF_TS = int(TFV[1]) if len(TFV) > 1 and TFV[1].isdigit() else 0
TEAM_LOCKED = TF_N >= 5 and NOWTS - TF_TS < 900  # v19.16.6: 5 wrong team passwords -> 15 min lock
PHOTO_WINDOW = 7200  # v19.16.5: inspectors may add photos for 2 h after saving a defect; later only managers


# ------------------------------------------------------------------ v19.16 packing defective garments into boxes
# Stored WITHOUT new fields: one text attachment per box on the product template, name iq_qc_box_0001.txt
#   H|<box no>|<open|closed>|<created ts>|<closed ts>|<receipt id>
#   V|<variant id>|<qty>
PACKPRE = 'iq_qc_box_'
PACKTAG = 'Beim Verpacken gefunden'
PACKMARK = '[IQ-QC-PACK]'
GONEPRE = 'iq_qc_gone_'  # v19.16.3: defective pieces already handed over (e.g. supplier took them) – same format + N|note


def boxes_of(tid):
    # supplier phone: only the boxes of this supplier; IQ team: all boxes (supplier boxes are marked)
    allb = recs_of(tid, PACKPRE)
    if not GUEST:
        return allb
    own = []
    for x in allb:
        if x.get('sup') == GUEST.id:
            own.append(x)
    return own


def box_next_no(tid):
    allb = recs_of(tid, PACKPRE)
    return (allb[-1]['n'] + 1) if allb else 1


def box_sup_name(b):
    if not b.get('sup'):
        return ''
    co = (env['res.partner'].sudo().browse(b['sup']).exists().name or '').split()
    return (co[0].rstrip('.,') if co else 'Lieferanten') + '-Prüfung'


def date_ts(ds_):
    # 'YYYY-MM-DD' or 'TT.MM.JJJJ' -> unix ts (11:00 UTC), else now
    ds_ = str(ds_ or '').strip()
    if len(ds_) == 10 and ds_[2] == '.' and ds_[5] == '.' and ds_.replace('.', '').isdigit():
        ds_ = ds_[6:] + '-' + ds_[3:5] + '-' + ds_[:2]
    if len(ds_) == 10 and ds_[4] == '-' and ds_[7] == '-' and ds_.replace('-', '').isdigit() and 1 <= int(ds_[5:7]) <= 12 and 1 <= int(ds_[8:10]) <= 31:
        try:
            return int((datetime.datetime(int(ds_[:4]), int(ds_[5:7]), int(ds_[8:10]), 11, 0) - datetime.datetime(1970, 1, 1)).total_seconds())
        except Exception:
            return NOWTS
    return NOWTS


def gone_of(tid):
    return recs_of(tid, GONEPRE)


def recs_of(tid, pre):
    out = []
    for a in Att.search([('res_model', '=', 'product.template'), ('res_id', '=', int(tid)), ('name', '=like', pre + '%')], order='name'):
        b = {'att': a, 'n': 0, 'state': 'open', 'c': '', 'x': '', 'pick': 0, 'items': {}, 'pre': pre, 'note': ''}
        for ln in (a.raw or b'').decode('utf-8', 'ignore').split(chr(10)):
            pr = ln.strip().split('|')
            if pr[0] == 'H' and len(pr) >= 6:
                b['n'] = int(pr[1]) if pr[1].isdigit() else 0
                b['state'] = pr[2] if pr[2] in ('closed', 'gone') else 'open'
                b['c'] = pr[3]
                b['x'] = pr[4]
                b['pick'] = int(pr[5]) if pr[5].isdigit() else 0
            elif pr[0] == 'G' and len(pr) == 2:
                b['g'] = pr[1]
            elif pr[0] == 'N' and len(pr) >= 2:
                b['note'] = '|'.join(pr[1:])
            elif pr[0] == 'S' and len(pr) == 2 and pr[1].isdigit():
                b['sup'] = int(pr[1])
            elif pr[0] == 'V' and len(pr) == 3 and pr[1].isdigit() and pr[2].isdigit():
                b['items'][int(pr[1])] = b['items'].get(int(pr[1]), 0) + int(pr[2])
        if b['n']:
            out.append(b)
    return sorted(out, key=lambda b: b['n'])


def box_save(b, tid):
    lines = ['H|' + str(b['n']) + '|' + b['state'] + '|' + str(b['c']) + '|' + str(b['x']) + '|' + str(b['pick'] or 0)]
    if b.get('note'):
        lines.append('N|' + b['note'].replace(chr(10), ' ').replace(chr(13), ' '))
    if b.get('g'):
        lines.append('G|' + str(b['g']))
    if b.get('sup'):
        lines.append('S|' + str(b['sup']))
    for vid in b['items']:
        if b['items'][vid] > 0:
            lines.append('V|' + str(vid) + '|' + str(b['items'][vid]))
    raw = chr(10).join(lines).encode('utf-8')
    if b.get('att'):
        b['att'].write({'raw': raw})
    else:
        b['att'] = Att.create({'name': b.get('pre', PACKPRE) + ('%04d' % b['n']) + '.txt', 'raw': raw, 'mimetype': 'text/plain', 'res_model': 'product.template', 'res_id': int(tid)})
    return b


def box_total(b):
    t = 0
    for vid in b['items']:
        t += b['items'][vid]
    return t


def box_items(b):
    # -> [[size label, article no, qty, variant id]] sorted by size
    out = []
    for vid in b['items']:
        q = b['items'][vid]
        if q > 0:
            v = Prod.browse(vid).exists() if vid else Prod.browse([])
            out.append([size_of(v) if v else '?', (v.default_code or '') if v else '', q, vid])
    return sorted(out, key=lambda r: (sz_parts(r[0])[0], size_rank(r[0]), r[0]))


def ts_txt(ts):
    if not str(ts or '').isdigit():
        return ''
    return loc(datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(ts))).strftime('%d.%m.%Y %H:%M')


def box_label_lines(t, b):
    pk = Pick.browse(b['pick']).exists() if b['pick'] else Pick.browse([])
    po = (pk.purchase_id.name if 'purchase_id' in PKF and pk.purchase_id else '') if pk else ''
    return {'product': label_wrap_text(t.name or '-', 20.0), 'items': box_items(b), 'total': box_total(b),
            'foot': ('NICHT BUCHEN · ' + (ts_txt(b['x']) or ts_txt(b['c']))[:10]),
            'deliv': (((po + ' / ' if po else '') + (pk.name or '')) if pk else '') + ((' · ' if pk else '') + box_sup_name(b) if b.get('sup') else '')}


def box_mm(L):
    need = 2.8 + 8.0 + 3.0 * len(L['product']) + 1.5 + 8.6 * len(L['items']) + 7.5 + 3.0 * (2 if L['deliv'] else 1) + 2.0
    for c in LABEL_LENGTHS:
        if c >= need:
            return c
    return LABEL_LENGTHS[-1]


def box_pdf_html(t, b):
    L = box_label_lines(t, b)
    mm = box_mm(L)
    rows = ''
    for it in L['items']:
        rows += ('<div class="it"><div class="q">' + str(it[2]) + ' ×</div><div class="s"><b>Gr. ' + esc(it[0]) + '</b><br><small>Art.-Nr. ' + esc(it[1] or '-') + '</small></div></div>')
    return ('<!DOCTYPE html><html><head><meta charset="utf-8"><style>@page{size:62mm ' + str(mm) + 'mm;margin:0}'
            'html,body{margin:0;padding:0;width:62mm;font-family:Arial,Helvetica,sans-serif;color:#000}'
            '.lb{box-sizing:border-box;width:62mm;height:' + str(mm) + 'mm;padding:1.4mm 2.4mm}'
            '.h{display:flex;justify-content:space-between;align-items:center;height:7.5mm}.h b{font-size:17pt}.h span{border:1.3pt solid #000;padding:0 1.2mm;font-weight:bold;font-size:9pt}'
            '.p{font-size:7.5pt;line-height:3mm;font-weight:bold}.it{display:flex;align-items:center;border-bottom:.4pt solid #000;height:8.6mm}'
            '.q{width:14mm;font-size:15pt;font-weight:bold}.s{font-size:10pt;line-height:3.9mm}.s small{font-size:7pt}'
            '.t{background:#000;color:#fff;font-weight:bold;font-size:11pt;padding:.6mm 1.4mm;margin-top:1mm}.f{font-size:7.5pt;line-height:3mm;margin-top:.8mm}'
            '</style></head><body><div class="lb"><div class="h"><b>KARTON ' + str(b['n']) + '</b><span>DEFEKT</span></div>'
            + ''.join(['<div class="p">' + esc(x) + '</div>' for x in L['product']]) + rows
            + '<div class="t">SUMME: ' + str(L['total']) + ' Stk.</div><div class="f">' + esc(L['foot']) + '</div>'
            + (('<div class="f">Lieferung: ' + esc(L['deliv']) + '</div>') if L['deliv'] else '') + '</div></body></html>')


def box_pdf(t, b):
    try:
        L = box_label_lines(t, b)
        rep = env['ir.actions.report'].sudo().search([('report_name', '=', 'iq_qc.label_62x' + str(box_mm(L)))], limit=1)
        if not rep:
            return [False, 'PDF-Format fehlt']
        pdf = env['ir.actions.report'].sudo()._run_wkhtmltopdf([box_pdf_html(t, b)], report_ref=rep)
        if not pdf or not pdf.startswith(b'%PDF'):
            return [False, 'PDF wurde nicht korrekt erzeugt']
        return [pdf, '']
    except Exception as e:
        return [False, 'PDF: ' + str(e).replace('|', '/')[:200]]


def br_encode(rows):
    pixels = len(rows)
    header = (b'\x1b\x69\x61\x01' + bytes(200) + b'\x1b\x40'
              + b'\x1b\x69\x61\x01' + b'\x1b\x69\x53'
              + b'\x1b\x69\x7a' + bytes([0xCE if BR_TWO_COLOR else 0x8E, 0x0A, 62, 0])
              + pixels.to_bytes(4, 'little') + bytes(2)
              + b'\x1b\x69\x4d\x40' + b'\x1b\x69\x41\x01'
              + b'\x1b\x69\x4b' + bytes([0x09 if BR_TWO_COLOR else 0x08]) + b'\x1b\x69\x64\x23\x00')
    chunks = [header]
    for one_row in rows:
        if BR_TWO_COLOR:
            chunks.append(b'\x77\x01\x5a' + bytes(one_row))
            chunks.append(b'\x77\x02\x5a' + BR_RAW_WHITE_ROW)
        else:
            chunks.append(b'\x67\x00\x5a' + bytes(one_row))
    chunks.append(b'\x1a')
    return b''.join(chunks)


def box_raw(t, b):
    L = box_label_lines(t, b)
    plan = []
    y = 92
    for line in L['product']:
        plan.append((line, 'p', 28, y))
        y += 35
    y += 10
    lines_y = []
    for it in L['items']:
        plan.append((str(it[2]) + ' ×', 'h', 28, y))
        sl = 'Gr. ' + it[0]
        kind = 'd' if br_text_width(sl, 'd') <= 470 else 'a'
        plan.append((sl, kind, 190, y + 2))
        plan.append(('Art.-Nr. ' + (it[1] or '-'), 'p', 190, y + 52))
        y += 102
        lines_y.append(y - 6)
    y += 8
    tot_y = y
    y += 72
    plan.append((L['foot'], 'p', 28, y))
    y += 38
    if L['deliv']:
        plan.append(('Lieferung: ' + L['deliv'], 'p', 28, y))
        y += 38
    pixels = max(y + 20, int(round(box_mm(L) * BR_RAW_DOTS_PER_MM)))
    rows = [[0] * 90 for n in range(pixels)]
    br_text(rows, 'KARTON ' + str(b['n']), 'h', 28, 10)
    bw = br_text_width('DEFEKT', 'p') + 25
    br_rectangle(rows, 668 - bw, 19, 668, 68, 3)
    br_text(rows, 'DEFEKT', 'p', 668 - bw + 12, 20)
    for ly in lines_y:
        br_fill_rect(rows, 28, ly, 668, ly + 1)
    tt = 'SUMME: ' + str(L['total']) + ' Stk.'
    br_fill_rect(rows, 20, tot_y, 676, tot_y + 62)
    br_text_inv(rows, tt, 'd', 32, tot_y + 4)
    for line, kind, x, yy in plan:
        br_text(rows, line, kind, x, yy)
    return br_encode(rows)


def box_print(t, b):
    # -> '' when sent to the printer, otherwise the reason (then the PDF is offered)
    if not PRINT_ENABLED or not PNP:
        return 'D'
    if 'BROTHER' in (PNP.name or '').upper():
        if '_RAW' not in (PNP.name or '').upper() and ' RAW' not in (PNP.name or '').upper():
            return 'Brother RAW-Drucker nicht gewählt'
        try:
            PNP.printnode_print_b64(b64encode(box_raw(t, b)).decode(), {'title': 'Karton ' + str(b['n']) + ' ' + (t.name or '')[:30], 'type': 'qweb-text'}, check_printer_format=False)
            return ''
        except Exception as e:
            return 'Druck fehlgeschlagen: ' + str(e).replace('|', '/')[:150]
    pdf, err = box_pdf(t, b)
    if err:
        return err
    try:
        PNP.printnode_print_b64(b64encode(pdf).decode(), {'title': 'Karton ' + str(b['n']), 'type': 'qweb-pdf'}, check_printer_format=False)
        return ''
    except Exception as e:
        return 'Druck fehlgeschlagen: ' + str(e).replace('|', '/')[:150]


def odoo_defects_by_size(tid):
    out = {}
    for al in QA.search([('product_id.product_tmpl_id', '=', int(tid))] + SUPXA):
        if is_note(al):
            continue
        s = al_size(al)
        out[s] = out.get(s, 0) + 1
    return out


def packed_by_size(boxes):
    out = {}
    ids = {}
    for b in boxes:
        for it in box_items(b):
            out[it[0]] = out.get(it[0], 0) + it[2]
            ids[it[0]] = it[3]
    return [out, ids]



# v19.16.6: report – print button only after every photo has loaded
REP_JS = ('<script>(function(){var b=document.getElementById("rprint"),st=document.getElementById("rstat");if(!b)return;'
          'var ims=[].slice.call(document.querySelectorAll("img")),n=ims.length,d=0,bad=0;'
          'function upd(){if(d>=n){b.disabled=false;b.textContent="Drucken / als PDF speichern";st.textContent=bad?(bad+" Foto(s) konnten nicht geladen werden – bitte Seite neu laden."):("Alle "+n+" Fotos geladen.")}else{b.textContent="Fotos werden geladen … ("+d+"/"+n+")"}}'
          'ims.forEach(function(im){if(im.complete){d++;if(!im.naturalWidth)bad++}else{im.addEventListener("load",function(){d++;upd()});im.addEventListener("error",function(){d++;bad++;upd()})}});'
          'b.onclick=function(){window.print()};upd()})();</script>')

# v19.16.7: quality check completed per product (attachment, no new field)
DONEFILE = 'iq_qc_done.txt'


def qc_done_of(tid):
    a = Att.search([('res_model', '=', 'product.template'), ('res_id', '=', int(tid)), ('name', '=', DONEFILE)], limit=1)
    if not a:
        return False
    pr = (a.raw or b'').decode('utf-8', 'ignore').split('|', 1)
    return [pr[0], pr[1] if len(pr) > 1 else '']


# v19.16.7: inspector name first and mandatory (start page + check page)
WHO_CARD = ('<div class="card whoc" id="whoc"><div class="whoh"><span class="whon">!</span><b id="whot">Wer prüft? Bitte zuerst deinen Namen eingeben</b>'
            '<a href="#" id="whoe" class="whoe">ändern</a></div>'
            '<div class="whob"><input type="text" id="who" placeholder="Dein Name – Pflichtfeld" autocomplete="off"><small>Der Name wird auf diesem Handy gemerkt.</small></div></div>')
WHO_JS = ('function lsw(k,v){try{if(v===undefined)return localStorage.getItem(k)||"";localStorage.setItem(k,v)}catch(e){return ""}}'
          'var W=document.getElementById("who"),WC=document.getElementById("whoc");W.value=lsw("iq_qc_who");'
          'function whoUi(){var ok=!!W.value.trim(),ed=WC.classList.contains("wed");WC.classList.toggle("wok",ok&&!ed);WC.classList.toggle("wneed",!ok);'
          'document.getElementById("whot").textContent=ok?("Prüfer: "+W.value.trim()):"Wer prüft? Bitte zuerst deinen Namen eingeben";'
          'document.querySelector("#whoc .whon").textContent=ok?"✓":"!";W.classList.toggle("needname",!ok)}'
          'document.getElementById("whoe").onclick=function(e){e.preventDefault();WC.classList.add("wed");whoUi();W.focus();W.select()};'
          'W.onchange=function(){lsw("iq_qc_who",W.value.trim());if(W.value.trim())WC.classList.remove("wed");whoUi()};'
          'W.oninput=function(){lsw("iq_qc_who",W.value.trim());WC.classList.toggle("wneed",!W.value.trim())};'
          'W.onkeydown=function(e){if(e.key==="Enter"){e.preventDefault();W.blur();W.onchange()}};whoUi();'
          'function needName(){if(W.value.trim())return false;try{beep("err")}catch(e){}if(window.flash)try{flash("Bitte zuerst deinen Namen eingeben (oben)","#b91c1c")}catch(e){}'
          'WC.classList.remove("shake");void WC.offsetWidth;WC.classList.add("shake");W.scrollIntoView({block:"center"});W.focus();return true}')

# v19.16.10: real icons instead of emoji
ICB = '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 8l-9-5-9 5v8l9 5 9-5z"/><path d="M3 8l9 5 9-5"/><path d="M12 13v8"/></svg>'
ICW = '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3L2 21h20z"/><path d="M12 10v5"/><path d="M12 18h.01"/></svg>'


PACK_JS = r"""
(function(){
  var err=document.getElementById('perr'),busy=false;
  function say(t){err.textContent=t;err.style.display=t?'block':'none';if(t&&err.scrollIntoView)err.scrollIntoView({block:'center'})}
  function beep(ok){try{var c=new (window.AudioContext||window.webkitAudioContext)(),o=c.createOscillator(),g=c.createGain();o.frequency.value=ok?1100:220;o.connect(g);g.connect(c.destination);g.gain.value=.15;o.start();o.stop(c.currentTime+(ok?.12:.4))}catch(e){}
    if(navigator.vibrate)try{navigator.vibrate(ok?30:[80,60,80])}catch(e){}}
  function post(data,done){if(busy)return;busy=true;var fd=new FormData();fd.append('csrf_token',CSRF);fd.append('key',KEY);fd.append('tmpl',TMPL);
    for(var k in data)fd.append(k,data[k]);
    fetch(location.pathname,{method:'POST',body:fd,credentials:'same-origin'}).then(function(r){return r.text()}).then(function(t){busy=false;var a=t.split('|');
      if(a[0]==='OK'){done(a)}else{beep(false);say(a[1]||t);var s=document.getElementById('pscan');if(s){s.value='';s.focus()}}})
    .catch(function(){busy=false;beep(false);say('Keine Verbindung – bitte nochmal.')})}
  function reload(){location.reload()}
  // v19.16.2 scanning: works with and without Enter at the end (TC22 / DataWedge keyboard output), focused field or not
  var scan=document.getElementById('pscan'),sto=null,SB='',ST=0,GTO=null;
  function sendCode(v){v=(v||'').trim();if(v.length<3||!BOXN)return;if(scan)scan.value='';
    if(scan)scan.placeholder='Wird gebucht: '+v+' …';
    post({act:'pack_add',n:BOXN,code:v,d:'1'},function(a){beep(true);say('');var t=document.getElementById('ptot');if(t)t.textContent=a[3]+' Stk.';
      var ok=document.getElementById('pok');if(ok){ok.textContent='✓ Gr. '+a[1]+' – jetzt '+a[2]+' Stk. in diesem Karton';ok.style.display='block'}
      setTimeout(reload,350)})}
  if(scan){
    scan.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key==='Tab'){e.preventDefault();clearTimeout(sto);sendCode(scan.value)}});
    scan.addEventListener('input',function(){clearTimeout(sto);var v=scan.value.trim();if(v.length>=6)sto=setTimeout(function(){sendCode(scan.value)},250)});
    setTimeout(function(){try{scan.focus()}catch(e){}},100);
    document.addEventListener('click',function(e){var tg=e.target.tagName;if(tg!=='INPUT'&&tg!=='SELECT'&&tg!=='BUTTON'&&tg!=='A'&&tg!=='SUMMARY')scan.focus()})}
  // scanner keystrokes while the field is NOT focused
  document.addEventListener('keydown',function(e){var t=e.target,tag=(t&&t.tagName)||'';if(tag==='TEXTAREA'||tag==='INPUT'||tag==='SELECT')return;
    var n=Date.now();if(n-ST>120)SB='';ST=n;clearTimeout(GTO);
    if(e.key==='Enter'||e.key==='Tab'){if(SB.length>=4){e.preventDefault();var c=SB;SB='';sendCode(c)}return}
    if(e.key&&e.key.length===1){SB+=e.key;GTO=setTimeout(function(){if(SB.length>=6){var c=SB;SB='';sendCode(c)}},200)}});
  document.querySelectorAll('.psz,.pbtn').forEach(function(b){b.onclick=function(){post({act:'pack_add',n:BOXN,vid:b.getAttribute('data-v'),d:b.getAttribute('data-d')},function(){beep(true);reload()})}});
  var nb=document.getElementById('pnew');
  if(nb)nb.onclick=function(){var p=document.getElementById('ppick');post({act:'pack_new',pick:p?p.value:''},reload)};
  var cl=document.getElementById('pclose');
  if(cl)cl.onclick=function(){if(!confirm('Karton '+BOXN+' abschließen und Etikett drucken?'))return;cl.disabled=true;cl.textContent='Wird abgeschlossen …';
    post({act:'pack_close',n:BOXN},function(a){if(a[1]==='D'){if(a[3])alert('Drucker: '+a[3]+' – PDF wird geöffnet.');window.open(PDFU+a[2],'_blank')}setTimeout(reload,400)});setTimeout(function(){cl.disabled=false},3000)};
  var dl=document.getElementById('pdel');
  if(dl)dl.onclick=function(){post({act:'pack_del',n:BOXN},reload)};
  document.querySelectorAll('.pre').forEach(function(b){b.onclick=function(){post({act:'pack_print',n:b.getAttribute('data-n')},function(a){if(a[1]==='D'){if(a[3])alert('Drucker: '+a[3]+' – PDF wird geöffnet.');window.open(PDFU+a[2],'_blank')}else{say('');alert('Etikett gedruckt ✓')}})}});
  document.querySelectorAll('.pop').forEach(function(b){b.onclick=function(){if(confirm('Karton '+b.getAttribute('data-n')+' wieder öffnen, um etwas zu ändern?'))post({act:'pack_open',n:b.getAttribute('data-n')},reload)}});
  function today(){var d=new Date();return ('0'+d.getDate()).slice(-2)+'.'+('0'+(d.getMonth()+1)).slice(-2)+'.'+d.getFullYear()}
  document.querySelectorAll('.pbg').forEach(function(b){b.onclick=function(){var n=b.getAttribute('data-n');
    var who=prompt('Karton '+n+' abgegeben – wer hat ihn mitgenommen / wohin?','Holfelder mitgenommen');if(who===null)return;who=who.trim();if(!who){say('Bitte eintragen, wer den Karton mitgenommen hat.');return}
    var dt=prompt('Datum der Abgabe (TT.MM.JJJJ)',today());if(dt===null)return;
    post({act:'pack_boxgone',n:n,note:who,date:dt.trim()},reload)}});
  document.querySelectorAll('.pbb').forEach(function(b){b.onclick=function(){if(confirm('Abgabe von Karton '+b.getAttribute('data-n')+' rückgängig machen? Der Karton zählt dann wieder als „im Lager“.'))post({act:'pack_boxback',n:b.getAttribute('data-n')},reload)}});
  var gs=document.getElementById('pgsave');
  if(gs)gs.onclick=function(){var d={act:'pack_gone'},n=0;document.querySelectorAll('.pgq').forEach(function(i){var q=parseInt(i.value||'0',10)||0;if(q>0){d['gq_'+i.getAttribute('data-v')]=String(q);n+=q}});
    d.note=(document.getElementById('pgnote').value||'').trim();d.date=document.getElementById('pgdate').value||'';var p=document.getElementById('pgpick');if(p)d.pick=p.value;
    if(!n){say('Keine Menge eingetragen.');return}if(!d.note){say('Bitte eintragen, wer die Teile mitgenommen hat.');document.getElementById('pgnote').focus();return}
    if(!confirm(n+' Teil(e) als abgegeben speichern ('+d.note+')?'))return;post(d,reload)};
  document.querySelectorAll('.pgdel').forEach(function(b){b.onclick=function(){if(confirm('Diesen Abgabe-Eintrag löschen?'))post({act:'pack_gone_del',n:b.getAttribute('data-n')},reload)}});
  var fx=document.getElementById('pfix');
  if(fx)fx.onclick=function(){var d={act:'pack_fix'},n=0;document.querySelectorAll('.pfx').forEach(function(i){var q=parseInt(i.value||'0',10)||0;if(q>0){d['fix_'+i.getAttribute('data-v')]=String(q);n+=q}});
    var p=document.getElementById('pfpick');if(p)d.pick=p.value;if(!n){say('Keine Menge eingetragen.');return}
    if(!confirm(n+' Defekt(e) in Odoo nachtragen?'))return;post(d,function(a){alert(a[1]+' Defekt(e) nachgetragen ✓');reload()})};
})();
"""


# ------------------------------------------------------------------ routing

# ------------------------------------------------------------------ v19.17 supplier check (guest mode), e.g. Holfelder checks the goods himself
# The supplier uses the NORMAL check screen (scan -> OK / Defekt with reason, place on the drawing, photo, label).
# Every record he saves is a normal quality.check / quality.alert, marked in note / description:
#   [Lieferantenprüfung <name> IQ-SUP:<partner id>]
# They count like every other check: same dashboard, product cards, QC details, inspector table ("Holfelder – Name"), report.
# "Mitgenommen" (pieces taken) per product and day: text file on the supplier contact iq_qc_sup_YYYY-MM-DD.txt (T lines).
SUPPRE = 'iq_qc_sup_'
SUPCSS = ('<style>.sp-c{background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:14px;margin:0 0 12px}'
          '.sp-c h2{margin:0 0 10px;font:800 15px Arial;letter-spacing:.5px;text-transform:uppercase}.sp-c input[type=password]{width:100%;padding:13px;border:1px solid #d1d5db;border-radius:9px;font-size:17px;box-sizing:border-box}'
          '.sp-save{width:100%;border:0;border-radius:12px;padding:16px;font:800 19px Arial;background:#151515;color:#fff;margin-top:10px;cursor:pointer}'
          '.sp-t{width:100%;border-collapse:collapse;font-size:14.5px}.sp-t td,.sp-t th{padding:8px 5px;border-top:1px solid #eee;text-align:left;vertical-align:top}.sp-t th{font:700 11px Arial;text-transform:uppercase;color:#6b7280;border:0}.sp-t .r{text-align:right}'
          '.sp-end{margin-left:auto;background:#333;color:#fff;border:0;border-radius:8px;padding:9px 12px;font:700 13px Arial;cursor:pointer}.sp-tk{display:flex;gap:6px;align-items:center;margin-top:4px}.sp-tk input{width:80px!important;padding:8px!important;font-size:16px}'
          '.sp-tk button{border:0;background:#151515;color:#fff;border-radius:7px;padding:9px 12px;font:700 13px Arial}[hidden]{display:none!important}.sp-d{color:#b91c1c;font-weight:800}.sp-g{color:#15803d;font-weight:800}'
          '.sp-badge{display:block;background:#b45309;color:#fff;text-align:center;font:700 13px Arial;padding:6px}</style>')


def gresp(html):
    # supplier pages are always German – no partial English translation (EN cookie of the IQ team on this phone)
    return request.make_response(html, headers=[('Content-Type', 'text/html; charset=utf-8'), ('X-Robots-Tag', 'noindex'), ('Cache-Control', 'no-store')])


def gtxt(s):
    return request.make_response(s, headers=[('Content-Type', 'text/plain; charset=utf-8'), ('Cache-Control', 'no-store')])


def gsig(pid, exp):
    x = 2166136261
    for ch in ('G|' + KEY + '|' + PW + '|' + MPIN_Q + '|' + str(pid) + '|' + str(exp)):
        x = ((x ^ ord(ch)) * 16777619) % 4294967296
    y2 = 2166136261
    for ch in (str(exp) + '#G#' + str(pid) + '#' + MPIN_Q + '#' + KEY):
        y2 = ((y2 ^ ord(ch)) * 16777619) % 4294967296
    return '%08x%08x' % (x, y2)


Partner = env['res.partner'].sudo()
GUEST = Partner.browse([])
GUEST_END = 0
gcv = (request.httprequest.cookies.get('iq_qcg') or '').split('.') if request else []
if len(MPIN_Q) >= 8 and len(gcv) == 3 and gcv[0].isdigit() and gcv[1].isdigit() and int(gcv[1]) >= NOWTS and gsig(gcv[0], gcv[1]) == gcv[2]:
    GUEST = Partner.browse(int(gcv[0])).exists()
    GUEST_END = int(gcv[1])
SUPID = ('IQ-SUP:' + str(GUEST.id) + ']') if GUEST else ''
GNAME = (GUEST.commercial_partner_id.name or GUEST.name or '') if GUEST else ''
SUPNOTE = ('<br>[Lieferantenprüfung ' + esc(GNAME) + ' ' + SUPID) if GUEST else ''
SUPDESC = ('<p>[Lieferantenprüfung ' + esc(GNAME) + ' ' + SUPID + '</p>') if GUEST else ''
if GUEST:
    EN = False  # supplier pages always German
# supplier checks count like every other check (same lists, figures, reports); only the supplier phone shows just its own
if 'note' in CF and GUEST:
    AUTO = AUTO + [('note', 'ilike', SUPID)]
SUPXA = [('description', 'ilike', SUPID)] if ('description' in AF and GUEST) else []


def sup_id_of(s):
    s = str(s or '')
    if 'IQ-SUP:' not in s:
        return 0
    v = s.split('IQ-SUP:', 1)[1].split(']', 1)[0]
    return int(v) if v.isdigit() else 0


def sup_label(text, nm):
    # 'Holfelder-Prüfung · Max' (company of the supplier mark + name typed on the phone)
    sid = sup_id_of(text)
    co = ((env['res.partner'].sudo().browse(sid).exists().name or '') if sid else '').split()
    co = co[0].rstrip('.,') if co else 'Lieferanten'
    n0 = ' '.join(str(nm or '').split())
    for pre in [co + ' – ', co + ' - ', co + ': ', co + ' ']:
        if n0.lower().startswith(pre.lower()):
            n0 = n0[len(pre):]
    return co + '-Prüfung' + ((' · ' + n0) if n0 else '')


def sup_pick_of(partner, p):
    # any receipt of this supplier with this article – open or already booked (not cancelled)
    if not p:
        return Pick.browse([])
    return Pick.search([('picking_type_code', '=', 'incoming'), ('state', '!=', 'cancel'), ('partner_id', 'child_of', partner.id), ('move_ids.product_id', '=', p.id)] + SUPDOM,
                       order='id desc', limit=1)


def sup_tmpl_ok(partner, t):
    if not t:
        return False
    return Pick.search_count([('picking_type_code', '=', 'incoming'), ('state', '!=', 'cancel'), ('partner_id', 'child_of', partner.id),
                              ('move_ids.product_id.product_tmpl_id', '=', t.id)] + SUPDOM) > 0


def sup_file(partner, day):
    return Att.search([('res_model', '=', 'res.partner'), ('res_id', '=', partner.id), ('name', '=', SUPPRE + day.isoformat() + '.txt')], limit=1)


def sup_lines(a):
    out = []
    if a:
        for ln in (a.raw or b'').decode('utf-8', 'ignore').split(chr(10)):
            if ln.strip():
                out.append(ln.split('|'))
    return out


def sup_add(partner, line):
    a = sup_file(partner, today)
    body = ((a.raw or b'').decode('utf-8', 'ignore') if a else '') + line.replace(chr(10), ' ').replace(chr(13), ' ') + chr(10)
    if a:
        a.write({'raw': body.encode('utf-8')})
    else:
        Att.create({'name': SUPPRE + today.isoformat() + '.txt', 'raw': body.encode('utf-8'), 'mimetype': 'text/plain', 'res_model': 'res.partner', 'res_id': partner.id})


def sup_clean(s):
    return ' '.join(str(s or '').replace('|', '/').split())[:120]


def sup_taken(pid, day, tid):
    # pieces taken (last T line wins) for supplier, day (date) and product template id
    n = 0
    for l in sup_lines(Att.search([('res_model', '=', 'res.partner'), ('res_id', '=', pid), ('name', '=', SUPPRE + day.isoformat() + '.txt')], limit=1)):
        if l[0] == 'T' and len(l) >= 4 and l[2] == str(tid) and l[3].isdigit():
            n = int(l[3])
    return n


def sup_groups(cs):
    # supplier checks -> {(day, supplier id, template id): [checked, ok, defect]} + order of keys
    g = {}
    order = []
    for c in cs:
        sid = sup_id_of(c.note if 'note' in CF else '')
        if not sid:
            continue
        k = (loc(c.create_date).date() if c.create_date else today, sid, c.product_id.product_tmpl_id.id)
        if k not in g:
            g[k] = [0, 0, 0]
            order.append(k)
        g[k][0] += 1
        if c.quality_state == 'fail':
            g[k][2] += 1
        else:
            g[k][1] += 1
    return [g, order]


# which requests a phone in supplier mode may use (everything else shows the supplier start page)
GPASS = False
if GUEST:
    gmeth = request.httprequest.method
    gact = str(params.get('act') or '')
    if gmeth == 'POST' and gact in ('ok', 'defect'):
        gp0 = Prod.browse(int(params.get('pid'))).exists() if str(params.get('pid') or '').isdigit() else Prod.browse([])
        gk0 = get_pick()
        GPASS = bool(gp0) and bool(sup_pick_of(GUEST, gp0)) and (not gk0 or Pick.search_count([('id', '=', gk0.id), ('partner_id', 'child_of', GUEST.id)]) > 0)
    elif gmeth == 'POST' and gact == 'undo':
        gc0 = QC.browse([int(x) for x in str(params.get('cid') or '').split(',') if x.strip().isdigit()]).exists()
        GPASS = bool(gc0) and 'note' in CF and len([c for c in gc0 if SUPID not in str(c.note or '')]) == 0
    elif gmeth == 'POST' and gact in ('finish_photo', 'photo_add', 'print', 'del'):
        ga0 = QA.browse(int(params.get('aid'))).exists() if str(params.get('aid') or '').isdigit() else QA.browse([])
        GPASS = bool(ga0) and SUPID in str(ga0.description or '')
    elif gmeth == 'GET' and params.get('view') == 'pack':
        # v19.18d: supplier packs his own defects into his own boxes
        GPASS = (not str(params.get('tmpl') or '').isdigit()) or sup_tmpl_ok(GUEST, Tmpl.browse(int(params.get('tmpl'))).exists())
    elif gmeth == 'POST' and gact in ('pack_new', 'pack_add', 'pack_close', 'pack_print', 'pack_del'):
        GPASS = str(params.get('tmpl') or '').isdigit() and sup_tmpl_ok(GUEST, Tmpl.browse(int(params.get('tmpl'))).exists())
    elif gmeth == 'GET' and params.get('boxpdf'):
        gbp = str(params.get('boxpdf') or '').split('-')
        GPASS = len(gbp) == 2 and gbp[0].isdigit() and sup_tmpl_ok(GUEST, Tmpl.browse(int(gbp[0])).exists())
    elif gmeth == 'GET' and str(params.get('tmpl') or '').isdigit() and not params.get('view') and not params.get('edit'):
        GPASS = sup_tmpl_ok(GUEST, Tmpl.browse(int(params.get('tmpl'))).exists())
    elif gmeth == 'GET' and (params.get('photo_for') or params.get('label') or params.get('pdf_label')):
        gaid = str(params.get('photo_for') or params.get('label') or params.get('pdf_label') or '')
        ga0 = QA.browse(int(gaid)).exists() if gaid.isdigit() else QA.browse([])
        GPASS = bool(ga0) and SUPID in str(ga0.description or '')
    elif gmeth == 'GET' and str(params.get('img') or '').isdigit():
        gi0 = Att.browse(int(params.get('img'))).exists()
        GPASS = bool(gi0) and gi0.res_model == 'quality.alert' and SUPID in str(QA.browse(gi0.res_id).exists().description or '')

if not KEY or params.get('key') != KEY or not PW:
    response = request.make_response('Not found', headers=[('Content-Type', 'text/plain; charset=utf-8')], status=404)
elif request.httprequest.method == 'POST' and params.get('pw') is not None and TEAM_LOCKED:
    response = resp(head('Gesperrt') + '<div class="wrap"><div class="card" style="max-width:480px;margin:40px auto"><h2>Zu viele falsche Versuche</h2><p>Das Team-Passwort ist für 15 Minuten gesperrt. Bitte später erneut versuchen.</p></div></div></body></html>')
elif request.httprequest.method == 'POST' and params.get('pw') is not None:
    if params.get('pw') != PW:
        P.set_param('iq.qc_pwfail', str((0 if NOWTS - TF_TS >= 900 else TF_N) + 1) + '|' + str(NOWTS))
    else:
        P.set_param('iq.qc_pwfail', False)
    if params.get('pw') == PW:
        response = request.make_response('', headers=[('Location', QB)], status=303)
        response.set_cookie('iq_cal', TOKEN, max_age=2592000, httponly=True, secure=True, samesite='Lax')
    else:
        response = request.make_response('', headers=[('Location', QB + '&bad=1')], status=303)
elif not authed:
    response = resp(head('Qualitätskontrolle') + '<div class="top"><div class="in"><img src="' + LOGO + '" alt="IQ"><h1>Qualitätskontrolle</h1></div></div><div class="wrap"><div class="card">'
                    '<form method="post" action=""><input type="hidden" name="csrf_token" value="' + request.csrf_token() + '"><input type="hidden" name="key" value="' + KEY + '">'
                    '<h2>Team-Passwort</h2><input type="password" name="pw" autofocus style="width:100%;padding:12px;border:1px solid #d1d5db;border-radius:8px;font-size:16px;margin-bottom:10px">'
                    '<button class="big blk">Anmelden</button>' + ('<p class="err" style="display:block">Falsches Passwort.</p>' if params.get('bad') else '')
                    + '<p class="mut">Gleiches Passwort wie der Lagerkalender. Einmal pro Handy, dann 30 Tage gemerkt.</p></form></div></div></body></html>')

elif GUEST and not GPASS:
    # v19.17: phone in supplier mode – start page, scan, end, pieces taken; everything else of IQ is not reachable
    ga = str(params.get('act') or '')
    gpost = request.httprequest.method == 'POST'
    if gpost and ga == 'sup_end':
        fkg = 'iq.cal_pinfail.M'
        fvg = (P.get_param(fkg) or '0|0').split('|')
        fails_g = int(fvg[0]) if fvg[0].isdigit() else 0
        fts_g = int(fvg[1]) if len(fvg) > 1 and fvg[1].isdigit() else 0
        if fails_g >= 5 and NOWTS - fts_g < 900:
            response = request.make_response('', headers=[('Location', QB + '&gerr=lock')], status=303)
        elif str(params.get('mpin') or '').strip() == MPIN_Q:
            P.set_param(fkg, False)
            expm = NOWTS + QSESSION
            response = request.make_response('', headers=[('Location', QB + '&view=dash&gend=1')], status=303)
            response.delete_cookie('iq_qcg')
            response.set_cookie('iq_emp', 'M.' + str(expm) + '.' + msig(expm), max_age=QSESSION, httponly=True, secure=True, samesite='Lax')
        else:
            P.set_param(fkg, str((0 if NOWTS - fts_g >= 900 else fails_g) + 1) + '|' + str(NOWTS))
            response = request.make_response('', headers=[('Location', QB + '&gerr=pin')], status=303)
    elif gpost and ga == 'scan':
        p = scan_prod(params.get('code'))
        pk = sup_pick_of(GUEST, p) if p else Pick.browse([])
        if not p:
            response = gtxt('ERR|Barcode nicht gefunden: ' + esc(params.get('code') or ''))
        elif not pk:
            response = gtxt('ERR|Gehört nicht zu dieser Prüfung: ' + esc((p.display_name or '')[:60]))
        else:
            response = gtxt('OK|' + str(p.id) + '|' + str(p.product_tmpl_id.id) + '|' + size_of(p) + '|' + (p.product_tmpl_id.name or '').replace('|', ' ')
                            + '|' + str(pk.id) + '|' + pick_label(pk).replace('|', ' ') + '|')
    elif gpost and ga == 'sup_take':
        tid = str(params.get('tmpl') or '')
        qn = str(params.get('qty') or '0').strip()
        if tid.isdigit() and qn.isdigit():
            sup_add(GUEST, 'T|' + str(NOWTS) + '|' + tid + '|' + str(int(qn)) + '|')
        response = request.make_response('', headers=[('Location', QB + '&gm=take')], status=303)
    elif gpost:
        response = gtxt('ERR|In der Lieferantenprüfung nicht möglich.')
    else:
        gcs = QC.search([('quality_state', 'in', ['pass', 'fail']), ('create_date', '>=', datetime.datetime.combine(today, datetime.time(0, 0)) - datetime.timedelta(hours=2))] + AUTO, order='create_date asc')
        gg = sup_groups(gcs)
        trs = ''
        for k in gg[1]:
            if k[0] != loc(now).date():
                continue
            v = gg[0][k]
            tk = sup_taken(GUEST.id, today, k[2])
            trs += ('<tr><td><b>' + esc(Tmpl.browse(k[2]).name) + '</b></td><td class="r">' + str(v[0]) + '</td><td class="r sp-g">' + str(v[1]) + '</td><td class="r sp-d">' + str(v[2]) + '</td></tr>'
                    + '<tr><td colspan="4" style="border-top:0;padding-top:0"><form method="post" action="" class="sp-tk"><input type="hidden" name="csrf_token" value="' + request.csrf_token() + '"><input type="hidden" name="key" value="' + KEY + '">'
                    + '<input type="hidden" name="act" value="sup_take"><input type="hidden" name="tmpl" value="' + str(k[2]) + '"><span style="font-size:13px">Mitgenommen:</span><input type="number" min="0" name="qty" value="' + str(tk or v[2]) + '">'
                    + '<button>' + ('Ändern' if tk else 'Speichern') + '</button></form></td></tr>')
        gerr = str(params.get('gerr') or '')
        gm = str(params.get('gm') or '')
        endt = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=GUEST_END)
        html = (head('Lieferantenprüfung') + SUPCSS + topbar('Prüfung · ' + esc(GNAME), '')
                + '<div class="wrap">'
                + '<form method="post" action="" class="sp-c" id="gend"' + ('' if (gerr or params.get('gshow')) else ' hidden') + '><h2>Prüfung beenden (IQ Dogsport)</h2>'
                + '<input type="hidden" name="csrf_token" value="' + request.csrf_token() + '"><input type="hidden" name="key" value="' + KEY + '"><input type="hidden" name="act" value="sup_end">'
                + '<input type="password" name="mpin" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" placeholder="PIN (nur IQ Dogsport) – Buchstaben und Zahlen">'
                + ('<p class="sp-d">' + ('Falscher PIN.' if gerr == 'pin' else 'Zu viele Versuche – bitte in 15 Minuten erneut.') + '</p>' if gerr else '')
                + '<button class="sp-save">Beenden</button></form>'
                + ('<div class="sp-c" style="background:#ecfdf3;border-color:#a7e3bd;font-weight:700">Gespeichert.</div>' if gm else '')
                + WHO_CARD
                + '<div class="scan" id="scan"><div class="sp">Etikett scannen</div><div class="bp">danach OK oder Defekt – wie gewohnt</div></div>'
                + '<a class="big" href="' + QB + '&amp;view=pack" style="display:block;text-align:center;text-decoration:none;background:#151515;color:#fff;margin:0 0 12px">Defekte verpacken</a>'
                + '<div class="sp-c"><h2>Heute geprüft</h2>' + (('<table class="sp-t"><tr><th>Produkt</th><th class="r">Geprüft</th><th class="r">OK</th><th class="r">Defekt</th></tr>' + trs + '</table>'
                                                                  + '<p class="mut" style="font-size:13px">„Mitgenommen“: wie viele Teile ihr heute mitnehmt – eintragen und speichern.</p>') if trs else '<p class="mut">Noch nichts geprüft.</p>') + '</div>'
                + '<p class="mut" style="font-size:12px;text-align:center">Lieferantenprüfung – alle Ergebnisse gehen in die IQ-Qualitätsprüfung (als Prüfer „Firma – Name“). Aktiv bis ' + loc(endt).strftime('%H:%M') + ' Uhr.</p></div>'
                + '<script>var CSRF="' + request.csrf_token() + '",KEY="' + KEY + '";' + ('try{localStorage.removeItem("iq_qc_who")}catch(e){};' if params.get('gfirst') else '') + SCANJS + WHO_JS
                + 'window.onScan=function(c){if(needName())return;scanPost(c,{},function(a){if(a[0]!=="OK"){beep("err");var s=document.getElementById("scan");s.innerHTML="<div class=sp style=color:#b91c1c>"+(a[1]||"Fehler")+"</div>";return}'
                + 'beep("ok");goScan(a,false)})};'
                + 'var GE=document.getElementById("gend"),GB=document.getElementById("gendb");if(GB)GB.onclick=function(e){e.preventDefault();GE.hidden=!GE.hidden;if(!GE.hidden)GE.querySelector("input[type=password]").focus()};</script></body></html>')
        response = gresp(html)

elif request.httprequest.method == 'POST' and params.get('act') == 'sup_start':
    spid = str(params.get('sup') or '')
    hrs = str(params.get('hrs') or '10')
    if not ADM:
        response = request.make_response('', headers=[('Location', QB + '&view=mlogin&next=' + (QB + '&view=dash').replace('&', '%26'))], status=303)
    elif not spid.isdigit() or not Partner.browse(int(spid)).exists() or len(MPIN_Q) < 8:
        response = request.make_response('', headers=[('Location', QB + '&view=dash')], status=303)
    else:
        gexp = NOWTS + 3600 * (int(hrs) if hrs.isdigit() and 0 < int(hrs) <= 14 else 10)
        response = request.make_response('', headers=[('Location', QB + '&gfirst=1')], status=303)
        response.set_cookie('iq_qcg', spid + '.' + str(gexp) + '.' + gsig(spid, gexp), max_age=gexp - NOWTS, httponly=True, secure=True, samesite='Lax')
        response.delete_cookie('iq_emp')

elif request.httprequest.method == 'POST' and params.get('act') in ('mlogin', 'mlogout'):
    # v19.16: manager login on the QC page – same PIN and same session cookie as the warehouse calendar (30 minutes)
    nx = str(params.get('next') or '')
    nx = nx if (nx.startswith('?key=' + KEY) and chr(10) not in nx and chr(13) not in nx) else QB + '&view=dash'
    if params.get('act') == 'mlogout':
        response = request.make_response('', headers=[('Location', nx)], status=303)
        response.delete_cookie('iq_emp')
    else:
        fkm = 'iq.cal_pinfail.M'
        fvm = (P.get_param(fkm) or '0|0').split('|')
        fails_m = int(fvm[0]) if fvm[0].isdigit() else 0
        fts_m = int(fvm[1]) if len(fvm) > 1 and fvm[1].isdigit() else 0
        if len(MPIN_Q) < 8:
            response = request.make_response('', headers=[('Location', QB + '&view=mlogin&err=setup&next=' + nx.replace('&', '%26'))], status=303)
        elif fails_m >= 5 and NOWTS - fts_m < 900:
            response = request.make_response('', headers=[('Location', QB + '&view=mlogin&err=lock&next=' + nx.replace('&', '%26'))], status=303)
        elif str(params.get('mpin') or '').strip() == MPIN_Q:
            P.set_param(fkm, False)
            expm = NOWTS + QSESSION
            response = request.make_response('', headers=[('Location', nx)], status=303)
            response.set_cookie('iq_emp', 'M.' + str(expm) + '.' + msig(expm), max_age=QSESSION, httponly=True, secure=True, samesite='Lax')
        else:
            P.set_param(fkm, str((0 if NOWTS - fts_m >= 900 else fails_m) + 1) + '|' + str(NOWTS))
            response = request.make_response('', headers=[('Location', QB + '&view=mlogin&err=pin&next=' + nx.replace('&', '%26'))], status=303)

elif request.httprequest.method == 'POST' and str(params.get('act') or '').startswith('pack_'):
    # v19.16: packing defective garments into boxes (everyone; "nachtragen" only for managers)
    act_p = params.get('act')
    ts_ = str(params.get('tmpl') or '')
    t = Tmpl.browse(int(ts_)).exists() if ts_.isdigit() else Tmpl.browse([])
    bxs = boxes_of(t.id) if t else []
    ns_ = str(params.get('n') or '')
    b = False
    for x in bxs:
        if ns_.isdigit() and x['n'] == int(ns_):
            b = x
    openb = False
    for x in bxs:
        if x['state'] == 'open' and (GUEST or not x.get('sup')):
            openb = x
    if not t:
        response = txt('ERR|Produkt nicht gefunden.')
    elif act_p == 'pack_new':
        if openb:
            response = txt('ERR|Karton ' + str(openb['n']) + ' ist noch offen – bitte zuerst abschließen.')
        else:
            nn = box_next_no(t.id)
            pk_s = str(params.get('pick') or '')
            box_save({'att': False, 'n': nn, 'state': 'open', 'c': str(NOWTS), 'x': '', 'pick': int(pk_s) if pk_s.isdigit() else 0, 'items': {}, 'sup': GUEST.id if GUEST else 0}, t.id)
            response = txt('OK|' + str(nn))
    elif act_p == 'pack_add':
        if not b or b['state'] != 'open':
            response = txt('ERR|Kein offener Karton.')
        else:
            v = Prod.browse([])
            vs_ = str(params.get('vid') or '')
            if vs_.isdigit():
                v = Prod.browse(int(vs_)).exists()
            elif params.get('code'):
                v = scan_prod(str(params.get('code')))
            dq = str(params.get('d') or '1')
            dqi = int(dq) if dq.lstrip('-').isdigit() else 1
            if not v:
                response = txt('ERR|Barcode nicht gefunden: ' + str(params.get('code') or '')[:40])
            elif v.product_tmpl_id.id != t.id:
                response = txt('ERR|Falsches Produkt: ' + (v.product_tmpl_id.name or '')[:60])
            else:
                b['items'][v.id] = max(0, b['items'].get(v.id, 0) + max(-50, min(50, dqi)))
                box_save(b, t.id)
                response = txt('OK|' + size_of(v) + '|' + str(b['items'][v.id]) + '|' + str(box_total(b)))
    elif act_p in ('pack_close', 'pack_print'):
        if not b:
            response = txt('ERR|Karton nicht gefunden.')
        elif not box_total(b):
            response = txt('ERR|Der Karton ist leer.')
        elif act_p == 'pack_close' and b['state'] != 'open':
            response = txt('ERR|Karton ist nicht offen.')
        else:
            if act_p == 'pack_close':
                b['state'] = 'closed'
                b['x'] = str(NOWTS)
                box_save(b, t.id)
            er_ = box_print(t, b)
            response = txt('OK|' + ('P' if not er_ else 'D') + '|' + str(b['n']) + '|' + ('' if er_ in ('', 'D') else er_))
    elif act_p == 'pack_open' and GUEST:
        response = txt('ERR|Nur IQ Dogsport kann einen Karton wieder öffnen.')
    elif act_p == 'pack_open':
        if not b:
            response = txt('ERR|Karton nicht gefunden.')
        elif openb and openb['n'] != b['n']:
            response = txt('ERR|Karton ' + str(openb['n']) + ' ist noch offen – bitte zuerst abschließen.')
        elif b['state'] == 'gone':
            response = txt('ERR|Karton ist schon abgegeben – zuerst „Rückgängig“.')
        else:
            b['state'] = 'open'
            box_save(b, t.id)
            response = txt('OK|' + str(b['n']))
    elif act_p == 'pack_del':
        if not b:
            response = txt('ERR|Karton nicht gefunden.')
        elif box_total(b):
            response = txt('ERR|Nur leere Kartons können gelöscht werden.')
        else:
            b['att'].unlink()
            response = txt('OK|deleted')
    elif act_p in ('pack_boxgone', 'pack_boxback'):
        # v19.16.4: whole closed box handed over (e.g. supplier took it) / undo – managers only
        if not ADM:
            response = txt('ERR|Nur für Führungskräfte – bitte oben anmelden.')
        elif not b:
            response = txt('ERR|Karton nicht gefunden.')
        elif act_p == 'pack_boxgone':
            note = str(params.get('note') or '').strip()[:120]
            if b['state'] != 'closed':
                response = txt('ERR|Nur abgeschlossene Kartons können abgegeben werden.')
            elif not note:
                response = txt('ERR|Bitte eintragen, wer den Karton mitgenommen hat.')
            else:
                b['state'] = 'gone'
                b['note'] = note
                b['g'] = str(date_ts(params.get('date')))
                box_save(b, t.id)
                response = txt('OK|' + str(b['n']))
        else:
            if b['state'] != 'gone':
                response = txt('ERR|Karton ist nicht als abgegeben markiert.')
            else:
                b['state'] = 'closed'
                b['note'] = ''
                b['g'] = ''
                box_save(b, t.id)
                response = txt('OK|' + str(b['n']))
    elif act_p in ('pack_gone', 'pack_gone_del'):
        # v19.16.3: record / delete pieces that already left (e.g. supplier took them) – managers only
        gns = gone_of(t.id)
        if not ADM:
            response = txt('ERR|Nur für Führungskräfte – bitte oben anmelden.')
        elif act_p == 'pack_gone_del':
            gd = False
            for x in gns:
                if ns_.isdigit() and x['n'] == int(ns_):
                    gd = x
            if not gd:
                response = txt('ERR|Eintrag nicht gefunden.')
            else:
                gd['att'].unlink()
                response = txt('OK|deleted')
        else:
            items = {}
            for v in t.product_variant_ids:
                qs_ = str(params.get('gq_' + str(v.id)) or '0')
                if qs_.isdigit() and int(qs_) > 0:
                    items[v.id] = min(500, int(qs_))
            qs_ = str(params.get('gq_0') or '0')
            if qs_.isdigit() and int(qs_) > 0:
                items[0] = min(500, int(qs_))
            note = str(params.get('note') or '').strip()[:120]
            gts = date_ts(params.get('date'))
            pk_s = str(params.get('pick') or '')
            if not items:
                response = txt('ERR|Keine Menge eingetragen.')
            elif not note:
                response = txt('ERR|Bitte eintragen, wer die Teile mitgenommen hat / wohin sie gingen.')
            else:
                nn = (gns[-1]['n'] + 1) if gns else 1
                box_save({'att': False, 'n': nn, 'state': 'closed', 'c': str(NOWTS), 'x': str(gts), 'pick': int(pk_s) if pk_s.isdigit() else 0, 'items': items, 'pre': GONEPRE, 'note': note}, t.id)
                response = txt('OK|' + str(nn))
    elif act_p == 'pack_fix':
        if not ADM:
            response = txt('ERR|Nur für Führungskräfte – bitte oben anmelden.')
        else:
            pk_s = str(params.get('pick') or '')
            pk = Pick.browse(int(pk_s)).exists() if pk_s.isdigit() else Pick.browse([])
            tid_tag = False
            if TAG:
                ex = TAG.search([('name', '=ilike', PACKTAG)], limit=1)
                tid_tag = ex.id if ex else TAG.create({'name': PACKTAG}).id
            made = 0
            for v in t.product_variant_ids:
                qs_ = str(params.get('fix_' + str(v.id)) or '0')
                q = min(200, int(qs_)) if qs_.isdigit() else 0
                for k in range(q):
                    cv = {'product_id': v.id, 'quality_state': 'fail'}
                    if pk and 'picking_id' in CF:
                        cv['picking_id'] = pk.id
                    if 'note' in CF:
                        cv['note'] = PACKMARK + ' beim Verpacken gefunden'
                    c = QC.create(cv)
                    av = {'product_id': v.id, 'product_tmpl_id': t.id}
                    if 'title' in AF:
                        av['title'] = PACKTAG + ' · Gr. ' + size_of(v)
                    if 'tag_ids' in AF and tid_tag:
                        av['tag_ids'] = [(6, 0, [tid_tag])]
                    if 'check_id' in AF:
                        av['check_id'] = c.id
                    if pk and 'picking_id' in AF:
                        av['picking_id'] = pk.id
                    if 'description' in AF:
                        av['description'] = '<p>' + PACKMARK + ' Beim Verpacken der Defekt-Kartons gefunden – keine Einzeldokumentation, kein Foto.</p><p>Größe: ' + esc(size_of(v)) + '</p>'
                    QA.create(av)
                    made += 1
            response = txt('OK|' + str(made))
    else:
        response = txt('ERR|Unbekannte Aktion.')

elif params.get('boxpdf'):
    bp = str(params.get('boxpdf') or '').split('-')
    t = Tmpl.browse(int(bp[0])).exists() if len(bp) == 2 and bp[0].isdigit() and bp[1].isdigit() else Tmpl.browse([])
    b = False
    if t:
        for x in boxes_of(t.id):
            if x['n'] == int(bp[1]):
                b = x
    if not b:
        response = request.make_response('Karton nicht gefunden', headers=[('Content-Type', 'text/plain; charset=utf-8')], status=404)
    else:
        pdf, er_ = box_pdf(t, b)
        if er_:
            response = request.make_response('PDF nicht verfügbar: ' + er_, headers=[('Content-Type', 'text/plain; charset=utf-8')], status=500)
        else:
            response = request.make_response(pdf, headers=[('Content-Type', 'application/pdf'), ('Content-Disposition', 'inline; filename="Karton-' + str(b['n']) + '.pdf"'), ('Cache-Control', 'private, no-store')])


# ------------------------------------------------------------------ actions (fetch POST from the phone)
elif request.httprequest.method == 'POST' and params.get('act') in ('qc_done', 'qc_reopen'):
    # v19.16.7: manager marks the quality check of a product as completed (final report) or opens it again
    t = Tmpl.browse(int(params.get('tmpl') or 0)).exists() if str(params.get('tmpl') or '').isdigit() else Tmpl.browse([])
    if not ADM:
        response = txt('ERR|Nur für Führungskräfte – bitte oben anmelden.')
    elif not t:
        response = txt('ERR|Produkt nicht gefunden.')
    else:
        old = Att.search([('res_model', '=', 'product.template'), ('res_id', '=', t.id), ('name', '=', DONEFILE)])
        old.unlink()
        if params.get('act') == 'qc_done':
            Att.create({'name': DONEFILE, 'raw': (str(NOWTS) + '|' + str(params.get('note') or '')[:200]).encode('utf-8'), 'mimetype': 'text/plain', 'res_model': 'product.template', 'res_id': t.id})
        response = txt('OK|' + params.get('act'))

elif request.httprequest.method == 'POST' and params.get('act') == 'defect_edit':
    # v19.16.6: manager edits an existing defect / note (reason, place, size, note, type, photos) – change is written to the chatter
    al = QA.browse(int(params.get('aid') or 0)).exists() if str(params.get('aid') or '').isdigit() else QA.browse([])
    p = Prod.browse(int(params.get('pid') or 0)).exists() if str(params.get('pid') or '').isdigit() else Prod.browse([])
    if not ADM:
        response = txt('ERR|Bearbeiten nur für Führungskräfte – Anmeldung abgelaufen? Bitte in einem neuen Tab anmelden und erneut speichern.')
    elif not al or not p:
        response = txt('ERR|Defekt oder Größe nicht gefunden.')
    elif al.product_id and p.product_tmpl_id.id != al.product_id.product_tmpl_id.id:
        response = txt('ERR|Größe gehört zu einem anderen Produkt.')
    else:
        isnote = params.get('kind') == 'note'
        garm = params.get('garm') if (params.get('garm') in LOC_PROD or is_custom(params.get('garm'))) else 'gen'
        defs = []
        for ln in (params.get('defs') or '').split(chr(10))[:20]:
            if chr(9) not in ln:
                continue
            pr = ln.split(chr(9), 1)
            rn = loc_clean(clean_reason(pr[0].strip()[:60]))
            if not rn:
                continue
            zs = []
            for z in pr[1].split(','):
                z = z.strip()
                if loc_code_ok(z) and z not in zs:
                    zs.append(z)
            found = False
            for d0 in defs:
                if d0[0] == rn:
                    found = True
                    for z in zs:
                        if z not in d0[1]:
                            d0[1].append(z)
            if not found:
                defs.append([rn, zs[:12]])
        if not defs:
            response = txt('ERR|Bitte mindestens einen Grund angeben.')
        else:
            old_title = (al.title or '') if 'title' in AF else ''
            old_size = size_of(al.product_id) if al.product_id else '?'
            old_note = is_note(al)
            tids = []
            if TAG:
                for d0 in defs:
                    ex = TAG.search([('name', '=ilike', d0[0])], limit=1)
                    tids.append(ex.id if ex else TAG.create({'name': d0[0]}).id)
            # photos: remove the ticked ones (only photos of this defect), add new ones
            delids = [int(x) for x in request.httprequest.form.getlist('delph') if str(x).isdigit()]
            ndel = 0
            if delids:
                dl_ = Att.search([('id', 'in', delids), ('res_model', '=', 'quality.alert'), ('res_id', '=', al.id)])
                ndel = len(dl_)
                dl_.unlink()
            nadd = 0
            for fi0 in range(1, 21):
                for fl in request.httprequest.files.getlist('photo_' + str(fi0)):
                    data = fl.read()
                    if data and len(data) <= 12000000 and (fl.mimetype or 'image/jpeg').lower().startswith('image/'):
                        nadd += 1
                        Att.create({'name': al.name + '-E' + str(fi0) + '-' + str(nadd) + '.jpg', 'raw': data, 'mimetype': fl.mimetype or 'image/jpeg', 'res_model': 'quality.alert', 'res_id': al.id})
            nph = Att.search_count([('res_model', '=', 'quality.alert'), ('res_id', '=', al.id), ('mimetype', '=like', 'image%')])
            # description: keep everything after the free note (Prüfer, import marks, references), rebuild size / place / note
            d = str(al.description or '') if 'description' in AF else ''
            d = d.replace(MISSING_HTML, '').replace('<p>' + NOTEMARK + ' kein Defekt – wird gebucht, beobachten</p>', '')
            cut = len(d)
            for mk in ['<p>Prüfer:', '<p>Größe:', '<p>Nachgetragen']:
                ix = d.find(mk)
                if 0 <= ix < cut:
                    cut = ix
            keep = ''
            for pp in d[cut:].split('</p>'):
                if not pp.strip() or 'Größe:' in pp or LOCMARK in pp:
                    continue
                keep += pp + '</p>'
            nnote = str(params.get('note') or '').strip()
            hasloc = len([d0 for d0 in defs if d0[1]]) > 0
            vals = {}
            if 'description' in AF:
                vals['description'] = ((('<p>' + NOTEMARK + ' kein Defekt – wird gebucht, beobachten</p>') if isnote else '') + (('<p>' + esc(nnote) + '</p>') if nnote else '') + keep
                                       + '<p>Größe: ' + esc(size_of(p)) + '</p>' + (('<p>' + LOCMARK + garm + '] ' + ' | '.join([d0[0] + '=' + ','.join(d0[1]) for d0 in defs]) + '</p>') if hasloc else '')
                                       + (MISSING_HTML if (not nph and not hasloc and not isnote) else ''))
            if 'title' in AF:
                tparts = []
                for d0 in defs:
                    tparts.append(d0[0] + ((' @ ' + ', '.join([loc_short(z, garm) for z in d0[1]])) if d0[1] else ''))
                vals['title'] = ('Hinweis: ' if isnote else '') + '; '.join(tparts)[:240] + ' · Gr. ' + size_of(p)
            if 'tag_ids' in AF and TAG:
                vals['tag_ids'] = [(6, 0, tids)]
            if p.id != al.product_id.id:
                vals['product_id'] = p.id
            al.write(vals)
            chk = al.check_id if 'check_id' in AF else False
            if chk:
                cvals = {'quality_state': 'pass' if isnote else 'fail'}
                if p.id != chk.product_id.id:
                    cvals['product_id'] = p.id
                chk.write(cvals)
            chg = []
            if old_note != isnote:
                chg.append('Typ: ' + ('Defekt' if old_note else 'Hinweis') + ' → ' + ('Hinweis – kein Defekt' if isnote else 'Defekt'))
            if old_size != size_of(p):
                chg.append('Größe: ' + old_size + ' → ' + size_of(p))
            if 'title' in AF and old_title != vals.get('title'):
                chg.append('Grund/Ort: ' + old_title + ' → ' + vals.get('title'))
            if ndel:
                chg.append(str(ndel) + ' Foto(s) entfernt')
            if nadd:
                chg.append(str(nadd) + ' Foto(s) hinzugefügt')
            chg.append('Notiz: ' + (nnote or '–'))
            try:
                al.message_post(body='Geändert auf der QC-Seite (Führungskraft, ' + loc(now).strftime('%d.%m.%Y %H:%M') + '): ' + ' · '.join(chg))
            except Exception:
                pass
            rp_ = ''
            if params.get('reprint') == '1' and not isnote:
                if PRINT_ENABLED:
                    rp_ = 'P' if not pn_print(al) else 'D'
                else:
                    rp_ = 'D'
            response = txt('OK|' + str(al.id) + '|' + rp_)

elif request.httprequest.method == 'POST' and params.get('act') in ('ok', 'defect') and get_pick() and not pick_open(get_pick()) and not GUEST:
    response = txt('ERR|Lieferung schon gebucht – QC nur für offene Wareneingänge. Nichts gespeichert.')
elif request.httprequest.method == 'POST' and params.get('act') == 'ok':
    p = Prod.browse(int(params.get('pid') or 0)).exists()
    if not p:
        response = txt('ERR|Größe fehlt')
    else:
        pick = get_pick()
        v = {'product_id': p.id, 'quality_state': 'pass'}
        if pick and 'picking_id' in CF:
            v['picking_id'] = pick.id
        if 'note' in CF and params.get('who'):
            v['note'] = 'Prüfer: ' + esc(params.get('who'))
        if SUPNOTE and 'note' in CF:
            v['note'] = (v.get('note') or '') + SUPNOTE
        qty = int(params.get('qty') or 1) if str(params.get('qty') or '1').isdigit() else 1
        qty = max(1, min(qty, 200))
        ids = []
        for i in range(qty):
            ids.append(str(QC.create(v).id))
        response = txt('OK|' + ','.join(ids) + '|' + counts(p.product_tmpl_id, pick))
elif request.httprequest.method == 'POST' and params.get('act') == 'scan':
    p = scan_prod(params.get('code'))
    if not p:
        response = txt('ERR|Barcode nicht gefunden: ' + esc(params.get('code') or ''))
    else:
        r = choose_pick(p, str(params.get('pick') or ''), str(params.get('rpick') or ''))
        pk = r[0]
        response = txt('OK|' + str(p.id) + '|' + str(p.product_tmpl_id.id) + '|' + size_of(p) + '|' + (p.product_tmpl_id.name or '').replace('|', ' ')
                       + '|' + (str(pk.id) if pk else '') + '|' + (pick_label(pk).replace('|', ' ') if pk else '') + '|' + r[1])
elif request.httprequest.method == 'POST' and params.get('act') == 'undo':
    c = QC.browse([int(x) for x in str(params.get('cid') or '').split(',') if x.strip().isdigit()]).exists()
    if c and c[0].create_date and (now - c[0].create_date).total_seconds() < 900:
        tmpl = c[0].product_id.product_tmpl_id
        if 'check_id' in AF:
            al = QA.search([('check_id', 'in', c.ids)])
            Att.search([('res_model', '=', 'quality.alert'), ('res_id', 'in', al.ids)]).unlink()
            al.unlink()
        c.unlink()
        response = txt('OK|0|' + counts(tmpl, get_pick()))
    else:
        response = txt('ERR|Rückgängig nur bis 15 Minuten nach dem Speichern.')
elif request.httprequest.method == 'POST' and params.get('act') == 'defect':
    p = Prod.browse(int(params.get('pid') or 0)).exists() if str(params.get('pid') or '').isdigit() else Prod.browse([])
    files = request.httprequest.files.getlist('photo')
    fphotos = []
    for fi0 in range(1, 21):
        for fl in request.httprequest.files.getlist('photo_' + str(fi0)):
            if (fl.mimetype or 'image/jpeg').lower().startswith('image/'):
                fphotos.append([fi0, fl])
    if not p:
        response = txt('ERR|Größe fehlt')
    else:
        pick = get_pick()
        names = [reason_spelling(x.strip()[:60]) for x in (params.get('tags') or '').split('\n') if x.strip()]
        newt = reason_spelling((params.get('newtag') or '').strip()[:60])
        if newt and newt not in names:
            names.append(newt)
        isnote = params.get('kind') == 'note'
        garm = params.get('garm') if (params.get('garm') in LOC_PROD or is_custom(params.get('garm'))) else 'gen'
        defs = []
        for ln in (params.get('defs') or '').split(chr(10))[:20]:
            if chr(9) not in ln:
                continue
            pr = ln.split(chr(9), 1)
            rn = loc_clean(clean_reason(pr[0].strip()[:60]))
            zs = []
            for z in pr[1].split(','):
                z = z.strip()
                if loc_code_ok(z) and z not in zs:
                    zs.append(z)
            if not rn:
                continue
            merged = False
            for d0 in defs:
                if d0[0] == rn:
                    for z in zs:
                        if z not in d0[1]:
                            d0[1].append(z)
                    merged = True
            if not merged:
                defs.append([rn, zs[:12]])
        if defs:
            names = []
            for d0 in defs:
                if d0[0] not in names:
                    names.append(d0[0])
        noplace = [d0[0] for d0 in defs if not d0[1]]
        if not names:
            response = txt('ERR|Bitte einen Fehlergrund wählen.')
        elif noplace and not isnote:
            response = txt('ERR|Bitte für jeden Fehler den Ort auf der Zeichnung wählen: ' + ', '.join(noplace))
        else:
            reqid = str(params.get('reqid') or '')[:64]
            reqmark = '[IQ-QC-REQ:' + reqid + ']' if reqid and reqid.replace('-', '').isalnum() and 'note' in CF else ''
            existing = QC.search([('product_id', '=', p.id), ('note', 'ilike', reqmark)], limit=1) if reqmark else QC.browse([])
            al = QA.search([('check_id', '=', existing.id)], limit=1) if existing and 'check_id' in AF else QA.browse([])
            if not al:
                tids = []
                if TAG:
                    for nm in names:
                        ex = TAG.search([('name', '=ilike', nm)], limit=1)
                        tids.append(ex.id if ex else TAG.create({'name': nm}).id)
                cv = {'product_id': p.id, 'quality_state': 'pass' if isnote else 'fail'}
                if pick and 'picking_id' in CF:
                    cv['picking_id'] = pick.id
                if 'note' in CF:
                    cv['note'] = ('Prüfer: ' + esc(params.get('who')) if params.get('who') else '') + ((' ' + reqmark) if reqmark else '') + SUPNOTE
                c = QC.create(cv)
                tnames = ', '.join(names)
                av = {'product_id': p.id, 'product_tmpl_id': p.product_tmpl_id.id}
                if 'title' in AF:
                    if defs:
                        tparts = []
                        for d0 in defs:
                            tparts.append(d0[0] + ((' @ ' + ', '.join([loc_short(z, garm) for z in d0[1]])) if d0[1] else ''))
                        av['title'] = ('Hinweis: ' if isnote else '') + '; '.join(tparts)[:240] + ' · Gr. ' + size_of(p)
                    else:
                        av['title'] = ('Hinweis: ' if isnote else '') + (tnames or 'Defekt')[:120] + ' · Gr. ' + size_of(p)
                if 'tag_ids' in AF and tids:
                    av['tag_ids'] = [(6, 0, tids)]
                if 'check_id' in AF:
                    av['check_id'] = c.id
                if pick and 'picking_id' in AF:
                    av['picking_id'] = pick.id
                if 'description' in AF:
                    av['description'] = (('<p>' + NOTEMARK + ' kein Defekt – wird gebucht, beobachten</p>') if isnote else '') + (('<p>' + esc(params.get('note') or '') + '</p>') if params.get('note') else '') + (('<p>Prüfer: ' + esc(params.get('who')) + '</p>') if params.get('who') else '') + '<p>Größe: ' + esc(size_of(p)) + '</p>' + (('<p>' + LOCMARK + garm + '] ' + ' | '.join([d0[0] + '=' + ','.join(d0[1]) for d0 in defs]) + '</p>') if defs else '') + (MISSING_HTML if not files and not fphotos and not [d0 for d0 in defs if d0[1]] else '') + SUPDESC
                al = QA.create(av)
                for i, f in enumerate(files):
                    data = f.read()
                    if data:
                        Att.create({'name': al.name + '-' + str(i + 1) + '.jpg', 'raw': data, 'mimetype': f.mimetype or 'image/jpeg', 'res_model': 'quality.alert', 'res_id': al.id})
                for i, fp in enumerate(fphotos):
                    data = fp[1].read()
                    if data and len(data) <= 12000000:
                        Att.create({'name': al.name + '-F' + str(fp[0]) + '-TC22-' + str(i + 1) + '.jpg', 'raw': data, 'mimetype': fp[1].mimetype or 'image/jpeg', 'res_model': 'quality.alert', 'res_id': al.id})
            c = al.check_id if 'check_id' in AF and al.check_id else existing
            if isnote:
                response = txt('OK|' + str(c.id if c else 0) + '|' + str(al.id) + '|' + al.name + '|N|')
            else:
                perr = pn_print(al) if PRINT_ENABLED else 'download'
                response = txt('OK|' + str(c.id if c else 0) + '|' + str(al.id) + '|' + al.name + '|' + ('D' if perr == 'download' else ('1' if not perr else '0')) + '|' + ('' if perr == 'download' else perr))

elif request.httprequest.method == 'POST' and params.get('act') == 'finish_photo':
    aid = str(params.get('aid') or '')
    al = QA.browse(int(aid)).exists() if aid.isdigit() else QA.browse([])
    if not al:
        response = txt('ERR|Defekt nicht gefunden')
    else:
        # v19.9: photos are optional (the location drawing documents the defect).
        response = txt('OK|' + str(photo_count(al)))

elif request.httprequest.method == 'POST' and params.get('act') == 'photo_add':
    aid = str(params.get('aid') or '')
    al = QA.browse(int(aid)).exists() if aid.isdigit() else QA.browse([])
    f = request.httprequest.files.get('photo')
    if not al:
        response = txt('ERR|Defekt nicht gefunden')
    elif not ADM and al.create_date and (now - al.create_date).total_seconds() > PHOTO_WINDOW:
        response = txt('ERR|Fotos können nur direkt bei der Prüfung hinzugefügt werden. Später nur durch Führungskräfte.')
    elif not f:
        response = txt('ERR|Bitte Foto auswählen')
    elif not (f.mimetype or '').lower().startswith('image/'):
        response = txt('ERR|Nur Bilddateien sind erlaubt')
    else:
        token = str(params.get('token') or '')[:64]
        token = token if token and token.replace('-', '').isalnum() else ''
        fidx = str(params.get('fidx') or '')
        fpre = ('-F' + fidx) if fidx.isdigit() and 0 < int(fidx) <= 20 else ''
        attname = al.name + fpre + '-TC22-' + token + '.jpg' if token else al.name + fpre + '-TC22-' + str(photo_count(al) + 1) + '.jpg'
        existing_photo = Att.search([('res_model', '=', 'quality.alert'), ('res_id', '=', al.id), ('name', '=', attname)], limit=1) if token else Att.browse([])
        if existing_photo:
            attachment = existing_photo
        else:
            data = f.read()
            if not data or len(data) > 12000000:
                attachment = False
            else:
                attachment = Att.create({'name': attname, 'raw': data, 'mimetype': f.mimetype or 'image/jpeg', 'res_model': 'quality.alert', 'res_id': al.id})
        if not attachment:
            response = txt('ERR|Foto leer oder größer als 12 MB')
        else:
            if 'description' in AF and MISSING_HTML in str(al.description or ''):
                al.write({'description': str(al.description).replace(MISSING_HTML, '')})
            response = txt('OK|' + str(attachment.id) + '|' + str(photo_count(al)))

elif request.httprequest.method == 'POST' and params.get('act') == 'print':
    al = QA.browse(int(params.get('aid') or 0)).exists() if str(params.get('aid') or '').isdigit() else QA.browse([])
    if not al:
        response = txt('ERR|Defekt nicht gefunden')
    else:
        perr = pn_print(al)
        response = txt(('OK|' + al.name) if not perr else ('ERR|Druck fehlgeschlagen: ' + perr))
elif request.httprequest.method == 'POST' and params.get('act') == 'del':
    al = QA.browse(int(params.get('aid') or 0)).exists() if str(params.get('aid') or '').isdigit() else QA.browse([])
    if not al:
        response = txt('ERR|Defekt nicht gefunden')
    elif not ADM and not (al.create_date and (now - al.create_date).total_seconds() <= PHOTO_WINDOW):
        response = txt('ERR|Löschen nur für Führungskräfte – bitte oben anmelden.')
    else:
        nm = al.name
        chk = al.check_id if 'check_id' in AF else False
        Att.search([('res_model', '=', 'quality.alert'), ('res_id', '=', al.id)]).unlink()
        al.unlink()
        if chk:
            chk.unlink()
        response = txt('OK|' + nm)

# ------------------------------------------------------------------ photo (for dashboard thumbnails)
# ------------------------------------------------------------------ one-time paper import
elif request.httprequest.method == 'POST' and params.get('act') == 'import':
    OK_ROWS = [
        ('WMD', 'S', 5, 'Pappe "WMD"', '13.11.2026'),
        ('WMD', 'M', 15, 'Pappe "WMD"', '13.11.2026'),
        ('WMD', 'L', 5, 'Pappe "WMD"', '13.11.2026'),
        ('WMD', 'XL', 15, 'Pappe "WMD"', '13.11.2026'),
        ('WMD', '3XL', 10, 'Pappe "WMD"', '13.11.2026'),
        ('WMD', 'XL', 5, 'Papierliste', '14.11.2026'),
        ('WMD', '2XL', 5, 'Papierliste', '14.11.2026'),
        ('WMD', 'S', 4, 'Papierliste', '14.11.2026'),
        ('WMD', 'M', 11, 'Papierliste', '14.11.2026'),
        ('WMD', 'XL', 9, 'Pappe "Hamza"', '14.11.2026'),
        ('WMD', 'S', 4, 'Pappe "Hamza"', '14.11.2026'),
        ('WMD', '2XL', 5, 'Pappe "Hamza"', '14.11.2026'),
        ('WMD', 'L', 5, 'Pappe "Hamza"', '14.11.2026'),
        ('WMD', '', 30, 'Papierliste (Größen nicht bestätigt)', '15.11.2026'),
        ('WMD', 'L', 16, 'Pappe "Hamza"', '15.11.2026'),
        ('WMD', 'S', 5, 'Pappe "Hamza"', '15.11.2026'),
        ('WMD', 'XS', 5, 'Pappe "Parka Damen"', ''),
        ('WMD', '2XL', 5, 'Pappe "Parka Damen"', ''),
        ('WMD', '', 12, 'Sprenger-Karte B "Winter Woman" (letzte Lieferung)', ''),
        ('WMD', 'M', 12, 'Zettel "DWM"', '16.11.2026'),
        ('WMD', 'L', 40, 'Zettel "DWM"', '16.11.2026'),
        ('WMD', 'XL', 5, 'Zettel "DWM"', '16.11.2026'),
        ('WMD', 'XL', 8, 'Sprenger-Karte (heute)', '16.11.2026'),
        ('WMD', 'L', 24, 'Sprenger-Karte (heute)', '16.11.2026'),
        ('WMD', 'M', 3, 'Sprenger-Karte (heute)', '16.11.2026'),
        ('WPU', 'S', 10, 'Pappe "Parka Männer"', '11.11.2026'),
        ('WPU', 'M', 9, 'Pappe "Parka Männer"', '11.11.2026'),
        ('WPU', 'L', 10, 'Pappe "Parka Männer"', '11.11.2026'),
        ('WPU', 'XL', 9, 'Pappe "Parka Männer"', '11.11.2026'),
        ('WPU', '2XL', 5, 'Pappe "Parka Männer"', '11.11.2026'),
        ('WPU', '4XL', 4, 'Pappe "Parka Männer"', '11.11.2026'),
        ('WPU', '2XL', 6, 'Sprenger-Karte A "L–2XL"', '12.–13.11.2026'),
        ('WPU', '3XL', 5, 'Sprenger-Karte A "L–2XL"', '12.–13.11.2026'),
        ('WPU', 'M', 10, 'Sprenger-Karte A "L–2XL"', '12.–13.11.2026'),
        ('WPU', '4XL', 8, 'Sprenger-Karte A "L–2XL"', '12.–13.11.2026'),
        ('WPU', 'L', 14, 'Sprenger-Karte A "L–2XL"', '12.–13.11.2026'),
    ]
    DEFECTS = [  # article, report no., tag on the garment, date, size ('' = unknown), reason chip, description, photo files
        ('WMD', 'W01', 'WMD 1', '11.11.2026', '', 'Futter defekt', 'Left jacket pocket defective (sleeve/pocket lining).', ['W01-1.jpg']),
        ('WMD', 'W02', '', '13.11.2026', 'L', 'Tasche defekt', 'Hole in the right pocket.', ['W02-1.jpg', 'W02-2.jpg']),
        ('WMD', 'W03', '', '13.11.2026', 'M', 'Innentasche zugenäht', 'Inner pocket sewn shut.', ['W03-1.jpg', 'W03-2.jpg']),
        ('WMD', 'W04', '', '13.11.2026', 'XL', 'Nahtfehler', 'Sewing defect.', ['W04-1.jpg', 'W04-2.jpg']),
        ('WMD', 'W05', '', '13.11.2026', 'M', 'Druckknopf defekt', 'Snap button of the extension does not close.', ['W05-1.jpg', 'W05-2.jpg']),
        ('WMD', 'W06', '', '14.11.2026', 'S', 'Druckknopf defekt', 'Button broken.', ['W06-1.jpg']),
        ('WMD', 'W07', '', '14.11.2026', 'M', 'Nahtfehler', 'Stitching issue, back lower part (hole in the seam).', ['W07-1.jpg', 'W07-2.jpg']),
        ('WMD', 'W08', '', '14.11.2026', 'M', 'Nahtfehler', 'Stitching issue left shoulder front and right front.', ['W08-1.jpg', 'W08-2.jpg']),
        ('WMD', 'W09', 'D1', '14.11.2026', 'M', 'Nahtfehler', 'Red stitching front right top; loose stitching inside at the bottom.', ['W09-1.jpg', 'W09-2.jpg']),
        ('WMD', 'W10', 'D2', '14.11.2026', 'S', 'Nahtfehler', 'Loose stitching under the left shoulder.', ['W10-1.jpg', 'W10-2.jpg']),
        ('WMD', 'W11', 'D3', '14.11.2026', 'M', 'Nahtfehler', 'Loose stitching under the right shoulder.', ['W11-1.jpg', 'W11-2.jpg']),
        ('WMD', 'W12', 'D4', '14.11.2026', 'M', 'Nahtfehler', 'Red thread stitching front left; blue stitching right.', ['W12-1.jpg', 'W12-2.jpg']),
        ('WMD', 'W13', 'D5', '14.11.2026', 'M', 'Nahtfehler', 'Stitching issue at the left shoulder joint.', ['W13-1.jpg']),
        ('WMD', 'W14', 'D6', '14.11.2026', '', 'Nahtfehler', 'Double stitch line right shoulder back; red thread front right and left.', ['W14-1.jpg', 'W14-2.jpg']),
        ('WMD', 'W15', 'D7', '14.11.2026', '', 'Nahtfehler', 'Red stitching bottom right; black stitching bottom left; blue stitching left chest.', ['W15-1.jpg', 'W15-2.jpg']),
        ('WMD', 'W16', '', '14.11.2026', 'XL', 'Nahtfehler', 'Yellow sewing line on the back above the big pocket.', ['W16-1.jpg', 'W16-2.jpg']),
        ('WMD', 'W17', 'D8', '14.11.2026', 'M', 'Nahtfehler', 'Red stitching left chest, slightly also right.', ['W17-1.jpg', 'W17-2.jpg']),
        ('WMD', 'W18', 'D9', '15.11.2026', '', 'Nahtfehler', 'Right shoulder joint loose; spot on right shoulder back; blue stitching left shoulder back.', ['W18-1.jpg', 'W18-2.jpg']),
        ('WMD', 'W19', '', '15.11.2026', 'L', 'Nahtfehler', 'Red stitching on the bottom part, right side.', ['W19-1.jpg', 'W19-2.jpg']),
        ('WMD', 'W20', 'D10', '15.11.2026', '', 'Nahtfehler', 'Stitching on the left bottom side; black stitching right shoulder front.', ['W20-1.jpg', 'W20-2.jpg']),
        ('WMD', 'W21', 'D11', '15.11.2026', '', 'Nahtfehler', 'Loose stitching left shoulder back.', ['W21-1.jpg']),
        ('WMD', 'W22', '', '15.11.2026', 'S', 'Futter defekt', 'Cuff lining at the wrist broken.', ['W22-1.jpg', 'W22-2.jpg']),
        ('WMD', 'W23', '', '15.11.2026', '', 'Nahtfehler', 'Stitching issue left bottom (red stitching).', ['W23-1.jpg', 'W23-2.jpg']),
        ('WMD', 'W24', '', '15.11.2026', '', 'Nahtfehler', 'Double sewing on the right shoulder back; red stitching left bottom (main seam).', ['W24-1.jpg', 'W24-2.jpg']),
        ('WMD', 'W25', 'D12', '15.11.2026', '', 'Nahtfehler', 'Red stitching on the back left and lower left back.', ['W25-1.jpg']),
        ('WMD', 'W26', 'D13', '15.11.2026', '', 'Nahtfehler', 'Red stitching left back side.', ['W26-1.jpg', 'W26-2.jpg']),
        ('WMD', 'W27', 'D15', '15.11.2026', 'L', 'Nahtfehler', 'Black stitching lines right back shoulder.', ['W27-1.jpg']),
        ('WMD', 'W28', 'D16', '15.11.2026', '', 'MOLLE-Schlaufe blockiert', 'Right MOLLE loop is blocked.', ['W28-1.jpg']),
        ('WMD', 'W29', 'D17', '15.11.2026', '', 'Nahtfehler', 'Stitching issue left/right back shoulder.', ['W29-1.jpg']),
        ('WMD', 'W30', 'D18', '15.11.2026', '4XL', 'Nahtfehler', 'Back zip not stitched cleanly.', ['W30-1.jpg']),
        ('WMD', 'W31', '', '', 'L', 'Stoff beschädigt', 'Material fault on the front placket.', ['W31-1.jpg']),
        ('WMD', 'W32', '', '', 'L', 'Tasche defekt', 'Sewing fault at the right outer pocket, at the magnet.', ['W32-1.jpg', 'W32-2.jpg']),
        ('WMD', 'W33', '', '', 'XL', 'Nahtfehler', 'Seam fault.', ['W33-1.jpg']),
        ('WMD', 'W34', '', '', 'XL', 'Tasche defekt', 'Right pocket – loose / open stitching.', ['W34-1.jpg']),
        ('WMD', 'W35', '', '', 'XL', 'Lose Fäden', 'Loose threads at the collar / hood snap.', ['W35-1.jpg']),
        ('WMD', 'W36', '', '', 'L', 'Nahtfehler', 'Seam fault.', ['W36-1.jpg']),
        ('WMD', 'W37', '', '', 'L', 'Druckknopf defekt', 'Top snap button on the zip-off.', ['W37-1.jpg']),
        ('WMD', 'W38', '', '', 'M', 'Futter defekt', 'Right sleeve, bottom – cuff lining open.', ['W38-1.jpg']),
        ('WMD', 'W39', '', '', 'M', 'Nahtfehler', 'Seam fault.', ['W39-1.jpg']),
        ('WMD', 'W40', '', '', 'L', 'Stoff beschädigt', 'Hole in the fabric next to the front zip.', ['W40-1.jpg']),
        ('WMD', 'W41', '', '', 'L', 'Nahtfehler', 'Seam fault.', ['W41-1.jpg']),
        ('WMD', 'W42', '', '', 'L', 'Stoff beschädigt', 'Weaving fault in the fabric.', ['W42-1.jpg', 'W42-2.jpg']),
        ('WMD', 'W43', '', '', 'L', 'Druckknopf defekt', 'Front placket at the snap buttons.', ['W43-1.jpg']),
        ('WMD', 'W44', '', '', 'L', 'Reißverschluss defekt', 'Front zip – fabric puckered / caught at the zip.', ['W44-1.jpg', 'W44-2.jpg']),
        ('WMD', 'W45', '', '', 'L', 'Nahtfehler', 'Seam fault.', ['W45-1.jpg']),
        ('WMD', 'W46', '', '', 'M', 'Nahtfehler', 'Collar / zip-off area at the snap buttons – stitching not clean.', ['W46-1.jpg']),
        ('WMD', 'W47', '', '', 'M', 'Nahtfehler', 'Front placket – uneven stitching, lining visible.', ['W47-1.jpg']),
        ('WMD', 'W48', '', '', 'M', 'Lose Fäden', 'Front zip – loose thread / stitching at the zip.', ['W48-1.jpg']),
        ('WMD', 'W49', '', '', 'M', 'Futter defekt', 'Lining torn open with loose threads.', ['W49-1.jpg']),
        ('WMD', 'W50', '', '', 'M', 'Nicht wasserdicht', 'Material not waterproof – customer complaint (customer got very wet after short use). No photo.', []),
        ('WPU', 'P01', 'WPU 1', '11.11.2026', '', 'Loch Brusttasche', 'Hole in the chest pocket.', ['P01-1.jpg']),
        ('WPU', 'P02', 'WPU 2', '11.11.2026', '', 'Innentasche zugenäht', 'Inner chest pocket sewn shut.', ['P02-1.jpg', 'P02-2.jpg']),
        ('WPU', 'P03', 'WPU 3', '11.11.2026', '', 'Innentasche zugenäht', 'Inner pocket sewn shut.', ['P03-1.jpg']),
        ('WPU', 'P04', 'WPU 4', '11.11.2026', '', 'Brusttasche defekt', 'Chest pocket defective (pocket lining torn).', ['P04-1.jpg']),
    ]
    errs = []
    if imp_done():
        errs.append('Schon importiert – nichts gemacht.')
    VARS = {}
    UNKV = {}
    PK = {}
    for art in ['WMD', 'WPU']:
        vs = imp_vars(art)
        if not vs:
            errs.append('Keine Varianten mit interner Referenz ' + ICODES[art] + '… gefunden.')
            continue
        VARS[art] = vs
        UNKV[art] = imp_var(vs, 'M') or vs[0]
        pid = str(params.get('pick_' + art) or '')
        PK[art] = Pick.browse(int(pid)).exists() if pid.isdigit() else Pick.browse([])
        if not PK[art]:
            errs.append('Bitte Wareneingang für ' + art + ' wählen.')
    for r in OK_ROWS:
        if r[0] in VARS and r[1] and not imp_var(VARS[r[0]], r[1]):
            errs.append(r[0] + ' Größe ' + r[1] + ' nicht gefunden.')
    for d in DEFECTS:
        if d[0] in VARS and d[4] and not imp_var(VARS[d[0]], d[4]):
            errs.append(d[1] + ' Größe ' + d[4] + ' nicht gefunden.')
    UP = {}
    for f in request.httprequest.files.getlist('photo'):
        nm = (f.filename or '').split('/')[-1].split(chr(92))[-1]
        UP[nm] = [f.read(), f.mimetype or 'image/jpeg']
    if not UP:
        errs.append('Keine Fotos ausgewählt.')
    if errs:
        response = txt('ERR|' + ' '.join(list(dict.fromkeys(errs))[:6]))
    else:
        TIDS = {}
        if TAG:
            for nm in list(set([d[5] for d in DEFECTS])):
                ex = TAG.search([('name', '=ilike', nm)], limit=1)
                TIDS[nm] = ex.id if ex else TAG.create({'name': nm}).id
        nok = 0
        nbad = 0
        nph = 0
        miss = []
        for art, size, qty, sheet, day in OK_ROWS:
            v = imp_var(VARS[art], size) if size else UNKV[art]
            vals = {'product_id': v.id, 'quality_state': 'pass',
                    'note': '<p>Nachgetragen (Papierprüfung) · ' + sheet + (' · Prüfdatum ' + day if day else '') + ' · ' + IMARK + '</p>' + ('<p>' + UNK + '</p>' if not size else '')}
            if 'picking_id' in CF:
                vals['picking_id'] = PK[art].id
            QC.create([dict(vals) for i in range(qty)])
            nok += qty
        for art, no, gtag, day, size, reason, text, pfiles in DEFECTS:
            v = imp_var(VARS[art], size) if size else UNKV[art]
            cv = {'product_id': v.id, 'quality_state': 'fail', 'note': '<p>Nachgetragen · ' + no + (' · ' + day if day else '') + ' · ' + IMARK + '</p>' + ('<p>' + UNK + '</p>' if not size else '')}
            if 'picking_id' in CF:
                cv['picking_id'] = PK[art].id
            c = QC.create(cv)
            av = {'product_id': v.id, 'product_tmpl_id': v.product_tmpl_id.id}
            if 'title' in AF:
                av['title'] = reason + ' · Gr. ' + (size or '?')
            if TAG:
                av['tag_ids'] = [(6, 0, [TIDS[reason]])]
            if 'check_id' in AF:
                av['check_id'] = c.id
            if 'picking_id' in AF:
                av['picking_id'] = PK[art].id
            if 'description' in AF:
                av['description'] = ('<p>' + no + (' · Etikett ' + gtag if gtag else '') + (' · geprüft ' + day if day else '') + ' – ' + text + '</p>'
                                     + '<p>Nachgetragen aus Papierprüfung / Fotos · ' + IMARK + '</p><p>Größe: ' + (size or ('? ' + UNK)) + '</p>')
            al = QA.create(av)
            k = 0
            for fn in pfiles:
                if fn in UP:
                    k += 1
                    Att.create({'name': al.name + '-' + str(k) + '.jpg', 'raw': UP[fn][0], 'mimetype': UP[fn][1], 'res_model': 'quality.alert', 'res_id': al.id})
                    nph += 1
                else:
                    miss.append(fn)
            nbad += 1
        log('IQ QC paper import done: ' + str(nok) + ' OK, ' + str(nbad) + ' defects, ' + str(nph) + ' photos' + (' | missing: ' + ', '.join(miss) if miss else ''))
        response = txt('OK|' + str(nok) + ' OK-Prüfungen, ' + str(nbad) + ' Defekte und ' + str(nph) + ' Fotos importiert.' + (' Fehlende Fotos: ' + ', '.join(miss) if miss else ''))

elif request.httprequest.method == 'POST' and params.get('act') == 'import_undo':
    al = QA.search([('description', 'ilike', IMARK)]) if 'description' in AF else QA.browse([])
    Att.search([('res_model', '=', 'quality.alert'), ('res_id', 'in', al.ids)]).unlink()
    na = len(al)
    al.unlink()
    cs = QC.search([('note', 'ilike', IMARK)]) if 'note' in CF else QC.browse([])
    nc = len(cs)
    cs.unlink()
    log('IQ QC paper import UNDO: deleted ' + str(na) + ' defects, ' + str(nc) + ' checks')
    response = txt('OK|Import rückgängig gemacht: ' + str(na) + ' Defekte und ' + str(nc) + ' Prüfungen gelöscht.')

# ------------------------------------------------------------------ one-time import Holfelder MFJ 4.0 (P00053, already booked – documentation only)
elif request.httprequest.method == 'POST' and params.get('act') == 'import_hf':
    HF_OK = [  # article, size, OK qty (= checked minus defects), source
        ('MJD_GR', 'XS', 3), ('MJD_GR', 'S', 10), ('MJD_GR', 'M', 16), ('MJD_GR', 'L', 14), ('MJD_GR', 'XL', 5), ('MJD_GR', '2XL', 3), ('MJD_GR', '3XL', 1), ('MJD_GR', '4XL', 1),
        ('MJD_BK', 'XS', 1), ('MJD_BK', 'S', 9), ('MJD_BK', 'M', 20), ('MJD_BK', 'L', 10), ('MJD_BK', 'XL', 8), ('MJD_BK', '2XL', 3),
        ('MFJ_GR', 'S', 3), ('MFJ_GR', 'M', 7), ('MFJ_GR', 'L', 8), ('MFJ_GR', 'XL', 6), ('MFJ_GR', '2XL', 4), ('MFJ_GR', '3XL', 3), ('MFJ_GR', '4XL', 2),
    ]
    HF_SRC = {'MJD_GR': 'Qualitätsbericht 05.11.2026 · LS 2026-344396 · Liste „Nur Endzahl“', 'MJD_BK': 'Qualitätsbericht 05.11.2026 · LS 2026-344396 · Liste „Nur Endzahl“',
              'MFJ_GR': 'Qualitätsbericht 10.11.2026 · LS 2026-344819 · Liste „Checked“'}
    HF_DEF = [  # article, no., size, reason chip, description (from the report), photo files
        ('MJD_GR', 'HD01', 'M', 'Nahtfehler', 'Ungleichmäßige Naht / Patch-Verarbeitung (IQ-Patch, Patch-Kante, Patch-Ecke).', ['HD01-1.jpg', 'HD01-2.jpg', 'HD01-3.jpg', 'HD01-4.jpg']),
        ('MJD_GR', 'HD02', 'XL', 'Loch Innentasche', 'Loch in der rechten Innentasche; ungleichmäßige Naht / Patch-Verarbeitung.', ['HD02-1.jpg']),
        ('MJD_GR', 'HD03', 'XL', 'Nahtfehler', 'Ungleichmäßige Naht / Patch-Verarbeitung, sichtbare Fehlstiche bzw. nicht versäuberte Kanten.', []),
        ('MJD_BK', 'HD04', 'XS', 'Nahtfehler', 'Überschüssiger Stoff an der Naht, nicht sauber vernäht.', ['HD04-1.jpg', 'HD04-2.jpg']),
        ('MJD_BK', 'HD05', 'M', 'IQ-Patch fehlt', 'IQ-Patch fehlt auf einer Schulterseite.', ['HD05-1.jpg', 'HD05-2.jpg']),
        ('MJD_BK', 'HD06', 'L', 'Tasche defekt', 'In den unteren Taschen fehlen die Futtertaschen.', ['HD06-1.jpg']),
        ('MJD_BK', 'HD07', '3XL', 'Tasche defekt', 'Innentasche beschädigt.', ['HD07-1.jpg', 'HD07-2.jpg']),
        ('MJD_BK', 'HD08', '4XL', 'Tasche defekt', 'Kleine Tasche und Innentasche beschädigt.', ['HD08-1.jpg', 'HD08-2.jpg']),
        ('MFJ_GR', 'HD09', 'S', 'Nahtfehler', 'Nähte am linken Ärmel nicht sauber vernäht.', ['HD09-1.jpg', 'HD09-2.jpg']),
        ('MFJ_GR', 'HD10', 'S', 'Stoff beschädigt', 'Ecke der Taschenpatte: kleines Loch, Naht an der Ecke nicht sauber vernäht.', ['HD10-1.jpg']),
    ]
    HF_NOTE = [  # Damen jackets accepted for sale – size/colour not recorded
        ('HN01', 'Nahtfehler', 'Ärmelnaht: ungleichmäßige Naht.', ['HN01-1.jpg']),
        ('HN02', 'Lose Fäden', 'Naht mit losem Fadenende.', ['HN02-1.jpg']),
        ('HN03', 'Nahtfehler', 'Nahtkante: ausgefranste / ungleichmäßige Naht.', ['HN03-1.jpg']),
        ('HN04', 'Nahtfehler', 'Bündchenkante: unregelmäßige Verarbeitung.', ['HN04-1.jpg']),
        ('HN05', 'Nahtfehler', 'Naht: unregelmäßige Stiche / Fehlstiche.', ['HN05-1.jpg']),
        ('HN06', 'Nahtfehler', 'Naht: unregelmäßige Stiche / Fehlstiche (Detail).', ['HN06-1.jpg']),
        ('HN07', 'Lose Fäden', 'Bei der Prüfung entfernte lose Fadenenden.', ['HN07-1.jpg']),
        ('HN08', 'Nahtfehler', 'Naht am Ende des Brust-Reißverschlusses ausgefranst.', ['HN08-1.jpg']),
    ]
    errs = []
    if hf_done():
        errs.append('Schon importiert – nichts gemacht.')
    VARS = {}
    PK = {}
    for art in ['MJD_GR', 'MJD_BK', 'MFJ_GR']:
        vs = imp_vars(art)
        if not vs:
            errs.append('Keine Varianten für ' + art + ' (' + ICODES[art] + '…) gefunden.')
            continue
        VARS[art] = vs
    for key, arts in [('D', ['MJD_GR', 'MJD_BK']), ('U', ['MFJ_GR'])]:
        pid = str(params.get('pick_' + key) or '')
        pk = Pick.browse(int(pid)).exists() if pid.isdigit() else Pick.browse([])
        if not pk:
            errs.append('Bitte Wareneingang wählen (' + ('Damen' if key == 'D' else 'Unisex') + ').')
        elif arts[0] in VARS and not [m for m in pk.move_ids if m.product_id.id in VARS[arts[0]].ids]:
            errs.append(pk.name + ' enthält keine ' + ('MFJ 4.0 Damen' if key == 'D' else 'MFJ 4.0 Unisex grau') + ' – bitte anderen Wareneingang wählen.')
        for a in arts:
            PK[a] = pk
    for r in HF_OK:
        if r[0] in VARS and not imp_var(VARS[r[0]], r[1]):
            errs.append(r[0] + ' Größe ' + r[1] + ' nicht gefunden.')
    for d in HF_DEF:
        if d[0] in VARS and not imp_var(VARS[d[0]], d[2]):
            errs.append(d[1] + ' Größe ' + d[2] + ' nicht gefunden.')
    UP = {}
    for f in request.httprequest.files.getlist('photo'):
        nm = (f.filename or '').split('/')[-1].split(chr(92))[-1]
        UP[nm] = [f.read(), f.mimetype or 'image/jpeg']
    if not UP:
        errs.append('Keine Fotos ausgewählt.')
    if errs:
        response = txt('ERR|' + ' '.join(list(dict.fromkeys(errs))[:6]))
    else:
      try:
        TIDS = {}
        if TAG:
            for nm in list(set([d[3] for d in HF_DEF] + [n[1] for n in HF_NOTE])):
                ex = TAG.search([('name', '=ilike', nm)], limit=1)
                TIDS[nm] = ex.id if ex else TAG.create({'name': nm}).id
        nok = 0
        nbad = 0
        nnt = 0
        nph = 0
        miss = []
        for art, size, qty in HF_OK:
            v = imp_var(VARS[art], size)
            vals = {'product_id': v.id, 'quality_state': 'pass', 'note': '<p>Nachgetragen · ' + HF_SRC[art] + ' · ' + HFMARK + '</p>'}
            if 'picking_id' in CF:
                vals['picking_id'] = PK[art].id
            QC.create([dict(vals) for i in range(qty)])
            nok += qty
        for art, no, size, reason, text, pfiles in HF_DEF:
            v = imp_var(VARS[art], size)
            cv = {'product_id': v.id, 'quality_state': 'fail', 'note': '<p>Nachgetragen · ' + no + ' · ' + HF_SRC[art] + ' · ' + HFMARK + '</p>'}
            if 'picking_id' in CF:
                cv['picking_id'] = PK[art].id
            c = QC.create(cv)
            av = {'product_id': v.id, 'product_tmpl_id': v.product_tmpl_id.id}
            if 'title' in AF:
                av['title'] = reason + ' · Gr. ' + size
            if TAG:
                av['tag_ids'] = [(6, 0, [TIDS[reason]])]
            if 'check_id' in AF:
                av['check_id'] = c.id
            if 'picking_id' in AF:
                av['picking_id'] = PK[art].id
            if 'description' in AF:
                av['description'] = '<p>' + no + ' – ' + text + '</p><p>Nicht verkaufsfähig, nicht gebucht · ' + HF_SRC[art] + ' · ' + HFMARK + '</p>'
            al = QA.create(av)
            k = 0
            for fn in pfiles:
                if fn in UP:
                    k += 1
                    Att.create({'name': al.name + '-' + str(k) + '.jpg', 'raw': UP[fn][0], 'mimetype': UP[fn][1], 'res_model': 'quality.alert', 'res_id': al.id})
                    nph += 1
                else:
                    miss.append(fn)
            nbad += 1
        nv = imp_var(VARS['MJD_GR'], 'M') or VARS['MJD_GR'][0]
        for no, reason, text, pfiles in HF_NOTE:
            av = {'product_id': nv.id, 'product_tmpl_id': nv.product_tmpl_id.id}
            if 'title' in AF:
                av['title'] = 'Hinweis: ' + reason + ' · Gr. ?'
            if TAG:
                av['tag_ids'] = [(6, 0, [TIDS[reason]])]
            if 'picking_id' in AF:
                av['picking_id'] = PK['MJD_GR'].id
            if 'description' in AF:
                av['description'] = ('<p>' + NOTEMARK + ' kein Defekt – wird gebucht, beobachten</p><p>' + no + ' – ' + text + '</p><p>Jacke angenommen (Verkauf) · ' + HF_SRC['MJD_GR'] + ' · ' + HFMARK + '</p>'
                                     + '<p>Größe: ? ' + UNK + '</p>')
            al = QA.create(av)
            k = 0
            for fn in pfiles:
                if fn in UP:
                    k += 1
                    Att.create({'name': al.name + '-' + str(k) + '.jpg', 'raw': UP[fn][0], 'mimetype': UP[fn][1], 'res_model': 'quality.alert', 'res_id': al.id})
                    nph += 1
                else:
                    miss.append(fn)
            nnt += 1
        log('IQ QC Holfelder import done: ' + str(nok) + ' OK, ' + str(nbad) + ' defects, ' + str(nnt) + ' notes, ' + str(nph) + ' photos' + (' | missing: ' + ', '.join(miss) if miss else ''))
        response = txt('OK|' + str(nok) + ' OK-Prüfungen, ' + str(nbad) + ' Defekte, ' + str(nnt) + ' Hinweise und ' + str(nph) + ' Fotos importiert.' + (' Fehlende Fotos: ' + ', '.join(miss) if miss else ''))
      except Exception as e:
        xal = QA.search([('description', 'ilike', HFMARK)]) if 'description' in AF else QA.browse([])
        Att.search([('res_model', '=', 'quality.alert'), ('res_id', 'in', xal.ids)]).unlink()
        xal.unlink()
        (QC.search([('note', 'ilike', HFMARK)]) if 'note' in CF else QC.browse([])).unlink()
        log('IQ QC Holfelder import ERROR (nothing kept): ' + str(e))
        response = txt('ERR|Fehler beim Import – nichts gespeichert: ' + str(e)[:300])

elif request.httprequest.method == 'POST' and params.get('act') == 'import_hf_undo':
    al = QA.search([('description', 'ilike', HFMARK)]) if 'description' in AF else QA.browse([])
    Att.search([('res_model', '=', 'quality.alert'), ('res_id', 'in', al.ids)]).unlink()
    na = len(al)
    al.unlink()
    cs = QC.search([('note', 'ilike', HFMARK)]) if 'note' in CF else QC.browse([])
    nc = len(cs)
    cs.unlink()
    log('IQ QC Holfelder import UNDO: deleted ' + str(na) + ' defects/notes, ' + str(nc) + ' checks')
    response = txt('OK|Import rückgängig gemacht: ' + str(na) + ' Defekte/Hinweise und ' + str(nc) + ' Prüfungen gelöscht.')

elif params.get('view') == 'import_hf':
    nd = hf_done()
    sel = ''
    for key, art, lab, want in [('D', 'MJD_BK', 'MFJ 4.0 Damen (LS 2026-344396)', 'WH1/IN/00058'), ('U', 'MFJ_GR', 'MFJ 4.0 Unisex grau (LS 2026-344819)', '')]:
        pks = imp_picks(art)
        if not want:
            for pk in pks:
                if not want and pk.purchase_id and pk.purchase_id.name == 'P00053':
                    want = pk.name
        sel += ('<label style="display:block;font-weight:700;margin:12px 0 4px">Wareneingang für ' + lab + '</label><select id="pick_' + key + '" style="width:100%;padding:10px;font-size:15px">'
                + (''.join(['<option value="' + str(pk.id) + '"' + (' selected' if want and pk.name == want else '') + '>' + esc(pk.name) + ' · ' + esc(pk.purchase_id.name or pk.origin or '') + ' · ' + esc(pk.partner_id.name or '') + (' · gebucht' if pk.state == 'done' else ' · offen') + '</option>' for pk in pks]) or '<option value="">– kein Wareneingang gefunden –</option>') + '</select>')
    if nd:
        body = ('<div class="card"><h2>Holfelder-Import MFJ 4.0</h2><p><b>Schon importiert</b> (' + str(nd) + ' Prüfungen).</p>'
                + '<button class="big" id="undo" style="background:var(--red);color:#fff">Import rückgängig machen</button><p id="msg"></p></div>')
    else:
        body = ('<div class="card"><h2>Holfelder-Import MFJ 4.0 (einmalig)</h2>'
                + '<p>Nur Dokumentation – ändert keinen Bestand, keine Mengen, keinen Wareneingang. Importiert die Qualitätsberichte 05.11. (Damen) und 10.11. (Unisex grau): '
                + '137 OK-Prüfungen, 10 Defekte (nicht gebucht), 8 Hinweise – mit Fotos.</p>'
                + sel
                + '<label style="display:block;font-weight:700;margin:16px 0 4px">Fotos (alle Dateien aus dem Ordner HF_photos auswählen)</label>'
                + '<input type="file" id="ph" multiple accept="image/*" style="width:100%;padding:10px;border:1px dashed #999;border-radius:8px">'
                + '<p class="mut" id="cnt"></p><button class="big blk" id="go">Hochladen &amp; importieren</button>'
                + '<div style="height:8px;background:#eee;border-radius:4px;margin-top:10px"><div id="bar" style="height:8px;width:0;background:#151515;border-radius:4px"></div></div><p id="msg"></p></div>')
    html = (head('Holfelder-Import') + topbar('Holfelder-Import', QB + '&amp;view=dash') + '<div class="wrap">' + body + '</div>'
            + '<script>var CSRF="' + request.csrf_token() + '",KEY="' + KEY + '";var m=document.getElementById("msg");'
            + 'function send(fd){var x=new XMLHttpRequest();x.open("POST",location.pathname);'
            + 'x.upload.onprogress=function(e){var b=document.getElementById("bar");if(b&&e.lengthComputable)b.style.width=Math.round(100*e.loaded/e.total)+"%"};'
            + 'x.onload=function(){var t=x.responseText||"",a=t.split("|");if(a[0]!=="OK"&&a[0]!=="ERR"){var d=document.createElement("div");d.innerHTML=t;var tx=(d.textContent||"").replace(/\\s+/g," ").trim();a=["ERR","Serverfehler (HTTP "+x.status+"): "+tx.slice(0,400)+(x.status==400?" – Seite neu laden (F5) und nochmal.":"")]}'
            + 'm.style.color=a[0]==="OK"?"green":"#b91c1c";m.textContent="";var b=document.createElement("b");b.textContent=a[1];m.appendChild(b);if(a[0]==="OK"){m.insertAdjacentHTML("beforeend","<br><a href=?key="+KEY+"&view=dash>Zum Dashboard</a>")}var g=document.getElementById("go");if(g){g.disabled=false;g.textContent="Hochladen & importieren"}};'
            + 'x.onerror=function(){m.textContent="Keine Verbindung – bitte nochmal."};x.send(fd)}'
            + 'var ph=document.getElementById("ph");if(ph)ph.onchange=function(){document.getElementById("cnt").textContent=ph.files.length+" Fotos ausgewählt (erwartet: 25)"};'
            + 'var go=document.getElementById("go");if(go)go.onclick=function(){if(!ph.files.length){m.textContent="Bitte zuerst die Fotos auswählen.";return}'
            + 'var fd=new FormData();fd.append("csrf_token",CSRF);fd.append("key",KEY);fd.append("act","import_hf");'
            + '["D","U"].forEach(function(a){fd.append("pick_"+a,document.getElementById("pick_"+a).value)});'
            + 'for(var i=0;i<ph.files.length;i++)fd.append("photo",ph.files[i],ph.files[i].name);go.disabled=true;go.textContent="Lädt hoch …";m.textContent="";send(fd)};'
            + 'var un=document.getElementById("undo");if(un)un.onclick=function(){if(!confirm("Import wirklich rückgängig machen?"))return;var fd=new FormData();fd.append("csrf_token",CSRF);fd.append("key",KEY);fd.append("act","import_hf_undo");send(fd)};'
            + '</script></body></html>')
    response = resp(html)

elif params.get('view') == 'mlogin':
    nx = str(params.get('next') or (QB + '&view=dash'))
    er_ = str(params.get('err') or '')
    msg = {'pin': 'PIN falsch.', 'lock': 'Zu viele falsche Versuche – bitte 15 Minuten warten.', 'setup': 'Keine Manager-PIN eingerichtet (Systemparameter iq.delivery_calendar_manager_pin, mind. 8 Zeichen).'}.get(er_, '')
    body = ('<div class="card" style="max-width:480px;margin:20px auto"><h2>Anmelden – Führungskraft</h2>'
            + '<p class="mut" style="margin-top:-4px">Dieselbe Manager-PIN wie im Lager- &amp; Teamkalender. Die Anmeldung gilt 30 Minuten.</p>'
            + (('<p class="err" style="display:block">' + esc(msg) + '</p>') if msg else '')
            + '<form method="post" action=""><input type="hidden" name="csrf_token" value="' + request.csrf_token() + '"><input type="hidden" name="key" value="' + esc(KEY) + '">'
            + '<input type="hidden" name="act" value="mlogin"><input type="hidden" name="next" value="' + esc(nx) + '">'
            + '<input type="password" name="mpin" placeholder="Manager-PIN" autocomplete="off" autofocus style="width:100%;margin-bottom:10px">'
            + '<button class="big blk" type="submit">Anmelden</button></form></div>')
    response = resp(head('Anmelden') + topbar('Anmelden', '') + '<div class="wrap">' + body + '</div></body></html>')

elif params.get('view') == 'pack':
    # v19.16: "Defekte verpacken" – scan defective garments into numbered boxes, print a box label, compare with Odoo
    ts_ = str(params.get('tmpl') or '')
    t = Tmpl.browse(int(ts_)).exists() if ts_.isdigit() else Tmpl.browse([])
    if not t:
        q = (params.get('q') or '').strip()
        cand = Tmpl.browse([])
        for al in QA.search(SUPXA, order='id desc', limit=3000):
            if al.product_id and al.product_id.product_tmpl_id not in cand:
                cand |= al.product_id.product_tmpl_id
        for a in (Att.search([('res_model', '=', 'product.template'), ('name', '=like', PACKPRE + '%')]) if not GUEST else Att.browse([])):
            x = Tmpl.browse(a.res_id).exists()
            if x and x not in cand:
                cand |= x
        if GUEST:
            for a in Att.search([('res_model', '=', 'product.template'), ('name', '=like', PACKPRE + '%')]):
                x = Tmpl.browse(a.res_id).exists()
                if x and x not in cand and boxes_of(x.id):
                    cand |= x
        if q and GUEST:
            q = ''
        if q:
            cand = Tmpl.search(['|', ('name', 'ilike', q), ('default_code', 'ilike', q)], limit=30) | Tmpl.search([('product_variant_ids.default_code', 'ilike', q)], limit=30)
        rows_p = ''
        for x in sorted(cand, key=lambda x: (x.name or '').lower()):
            bx = boxes_of(x.id)
            pk_n = 0
            gn_n = 0
            for b in bx:
                if b['state'] == 'gone':
                    gn_n += box_total(b)
                else:
                    pk_n += box_total(b)
            for b in gone_of(x.id):
                gn_n += box_total(b)
            od = 0
            for k in odoo_defects_by_size(x.id).values():
                od += k
            df = pk_n + gn_n - od
            rows_p += ('<a class="dl" style="text-decoration:none;display:flex;justify-content:space-between;gap:10px;align-items:center" href="' + QB + '&amp;view=pack&amp;tmpl=' + str(x.id) + '">'
                       + '<span><b>' + esc(x.name) + '</b><br><small class="mut">' + str(len(bx)) + ' Karton(s) · ' + str(pk_n) + ' Stk. verpackt' + ((' · ' + str(gn_n) + ' abgegeben') if gn_n else '') + ' · Odoo: ' + str(od) + ' Defekte</small></span>'
                       + (('<span class="pdif">' + ('+' if df > 0 else '') + str(df) + '</span>') if ((bx or gn_n) and df) else '') + '<span>→</span></a>')
        body = ('<div class="card"><h2>Defekte verpacken</h2><p class="mut" style="margin-top:-4px">Produkt wählen, Karton beginnen, defekte Teile scannen, Karton abschließen – das Etikett mit Größen, Art.-Nr. und Summe wird gedruckt.</p>'
                + '<form method="get" action="" style="display:flex;gap:8px"><input type="hidden" name="key" value="' + esc(KEY) + '"><input type="hidden" name="view" value="pack">'
                + '<input type="search" name="q" value="' + esc(q) + '" placeholder="Produkt suchen (Name oder Art.-Nr.)" style="flex:1"><button class="btn">Suchen</button></form></div>'
                + '<div class="card"><h2>Produkte</h2>' + (rows_p or '<p class="mut">Nichts gefunden.</p>') + '</div>')
        response = resp(head('Defekte verpacken') + topbar('Defekte verpacken', QB + '&amp;view=dash') + '<div class="wrap">' + body + '</div></body></html>')
    else:
        bxs = boxes_of(t.id)
        openb = False
        for x in bxs:
            if x['state'] == 'open' and (GUEST or not x.get('sup')):
                openb = x
        picks = Pick.search([('picking_type_code', '=', 'incoming'), ('state', '!=', 'cancel'), ('move_ids.product_id.product_tmpl_id', '=', t.id)] + SUPDOM, order='scheduled_date desc', limit=12)
        popts = ''.join(['<option value="' + str(k.id) + '">' + esc(pick_label(k)) + '</option>' for k in picks])
        vars_ = sorted(t.product_variant_ids, key=lambda v: (sz_parts(size_of(v))[0], size_rank(size_of(v))))
        if openb:
            cur = ''
            for it in box_items(openb):
                cur += ('<div class="prow"><span class="pq">' + str(it[2]) + ' ×</span><span class="ps"><b>Gr. ' + esc(it[0]) + '</b><small>' + esc(it[1]) + '</small></span>'
                        + '<button type="button" class="pbtn" data-v="' + str(it[3]) + '" data-d="-1">−</button><button type="button" class="pbtn" data-v="' + str(it[3]) + '" data-d="1">+</button></div>')
            szb = ''
            for v in vars_:
                szb += '<button type="button" class="psz" data-v="' + str(v.id) + '" data-d="1">' + esc(size_of(v)) + '</button>'
            box_html = ('<div class="card pbox"><div class="pbh"><h2>Karton ' + str(openb['n']) + ' <span class="popen">offen</span></h2><b id="ptot">' + str(box_total(openb)) + ' Stk.</b></div>'
                        + '<input id="pscan" class="pscan" placeholder="Barcode scannen …" autocomplete="off" autofocus inputmode="none" enterkeyhint="done">'
                        + '<p class="pok" id="pok"></p><p class="mut" style="font-size:13px;margin:6px 0">Ohne Scanner: Größe antippen (+1).</p><div class="pszg">' + szb + '</div>'
                        + '<h3 style="margin:12px 0 6px">Inhalt</h3>' + (cur or '<p class="mut" id="pempty">Noch leer – erstes Teil scannen.</p>')
                        + '<button type="button" class="big ok" id="pclose" style="margin-top:12px">Karton abschließen &amp; Etikett drucken</button>'
                        + ('<button type="button" class="btn dsec" id="pdel" style="margin-top:8px">Leeren Karton löschen</button>' if not box_total(openb) else '') + '</div>')
        else:
            nn = box_next_no(t.id)
            box_html = ('<div class="card pbox"><h2>Neuer Karton</h2>'
                        + ('<label class="qlbl" style="font-size:14px">Lieferung</label><select id="ppick" style="width:100%;margin-bottom:10px">' + popts + '<option value="">ohne Lieferung</option></select>' if popts else '')
                        + '<button type="button" class="big ok" id="pnew">Karton ' + str(nn) + ' beginnen</button></div>')
        od = odoo_defects_by_size(t.id)
        bx_in = [b for b in bxs if b['state'] != 'gone']
        bx_gone = [b for b in bxs if b['state'] == 'gone']
        pkd = packed_by_size(bx_in)
        gns = gone_of(t.id) if not GUEST else []
        gnd = packed_by_size(gns + bx_gone)
        keys = []
        for k in list(od.keys()) + list(pkd[0].keys()) + list(gnd[0].keys()):
            if k not in keys:
                keys.append(k)
        keys = sorted(keys, key=lambda s: (s == '?', sz_parts(s)[0], size_rank(s), s))
        vid_of = {}
        for v in vars_:
            vid_of[size_of(v)] = v.id
        crow = ''
        to_ = 0
        tp_ = 0
        tg_ = 0
        fix_rows = ''
        fix_sum = 0
        for k in keys:
            o = od.get(k, 0)
            pz = pkd[0].get(k, 0)
            gz = gnd[0].get(k, 0)
            to_ += o
            tp_ += pz
            tg_ += gz
            d = pz + gz - o
            crow += ('<tr><td>' + esc(k if k != '?' else '? (ohne Größe)') + '</td><td class="r">' + str(o) + '</td><td class="r">' + str(pz) + '</td><td class="r">' + (str(gz) if gz else '–') + '</td><td class="r' + (' pbad' if d else '') + '">'
                     + (('+' if d > 0 else '') + str(d) if d else '✓') + '</td></tr>')
            if d > 0 and k != '?' and k in vid_of:
                fix_rows += ('<div class="prow"><span class="ps"><b>Gr. ' + esc(k) + '</b></span><input type="number" min="0" max="200" class="pfx" data-v="' + str(vid_of[k]) + '" value="' + str(d) + '" style="width:90px"></div>')
                fix_sum += d
        dtot = tp_ + tg_ - to_
        crow += ('<tr class="ptr"><td>Summe</td><td class="r">' + str(to_) + '</td><td class="r">' + str(tp_) + '</td><td class="r">' + str(tg_) + '</td><td class="r' + (' pbad' if dtot else '') + '">' + (('+' if dtot > 0 else '') + str(dtot) if dtot else '✓') + '</td></tr>')
        cmp_html = ('<div class="card"><h2>Vergleich: Odoo ↔ Kartons</h2><p class="pprod">' + esc(t.name) + '</p>'
                    + ('<p class="pwarn">' + ('In den Kartons (+ abgegeben) sind ' + str(dtot) + ' Teile mehr als in Odoo erfasst.' if dtot > 0 else 'In Odoo sind ' + str(-dtot) + ' Defekte mehr erfasst als verpackt oder abgegeben.') + '</p>' if dtot and (bxs or gns) else '')
                    + '<div style="overflow-x:auto"><table class="pcmp"><tr><th>Größe</th><th class="r">Odoo Defekte</th><th class="r">In Kartons</th><th class="r">Abgegeben</th><th class="r">Differenz</th></tr>' + crow + '</table></div>'
                    + ('<p class="mut" style="font-size:12px">„? (ohne Größe)“ = Defekte aus dem Papier-Import ohne Größe – sie liegen in den Kartons unter ihrer echten Größe.</p>' if od.get('?') else ''))
        if fix_rows and dtot > 0:
            if ADM:
                cmp_html += ('<details class="pfix"><summary>Fehlende in Odoo nachtragen</summary><p class="mut" style="font-size:13px">Legt pro Teil einen Defekt mit Grund „' + PACKTAG + '“ an (ohne Foto). '
                             + 'Insgesamt fehlen ' + str(dtot) + (' – bitte Mengen prüfen, Defekte „ohne Größe“ sind evtl. schon dabei.' if fix_sum > dtot else '.') + '</p>' + fix_rows
                             + ('<label class="qlbl" style="font-size:14px;margin-top:8px">Lieferung</label><select id="pfpick" style="width:100%">' + popts + '</select>' if popts else '')
                             + '<button type="button" class="btn" id="pfix" style="margin-top:10px">Jetzt in Odoo nachtragen</button></details>')
            else:
                cmp_html += '<p class="mut" style="font-size:13px">Fehlende Defekte nachtragen: <a href="' + QB + '&amp;view=mlogin&amp;next=' + (QB + '&view=pack&tmpl=' + str(t.id)).replace('&', '%26') + '">als Führungskraft anmelden</a>.</p>'
        cmp_html += '</div>'
        # v19.16.3: pieces already handed over (e.g. supplier took them)
        glst = ''
        for b in bx_gone[::-1]:
            glst += ('<div class="pli"><div><b>Karton ' + str(b['n']) + ' (ganzer Karton)</b> <span class="pgone">abgegeben</span>'
                     + '<br><small class="mut">' + esc(b['note']) + ' · ' + ts_txt(b.get('g'))[:10] + '</small>'
                     + '<div class="pit">' + ', '.join([esc(it[0]) + ' × ' + str(it[2]) for it in box_items(b)]) + '</div></div>'
                     + '<div class="pact"><b class="pn">' + str(box_total(b)) + '</b></div></div>')
        for b in gns[::-1]:
            pk = Pick.browse(b['pick']).exists() if b['pick'] else Pick.browse([])
            glst += ('<div class="pli"><div><b>' + esc(b['note'] or 'Abgegeben') + '</b> <span class="pgone">abgegeben</span>'
                     + '<br><small class="mut">' + (ts_txt(b['x'])[:10]) + ((' · ' + esc(pick_label(pk))) if pk else '') + '</small>'
                     + '<div class="pit">' + ', '.join([esc(it[0] if it[0] != '?' else 'Größe unbekannt') + ' × ' + str(it[2]) for it in box_items(b)]) + '</div></div>'
                     + '<div class="pact"><b class="pn">' + str(box_total(b)) + '</b>'
                     + (('<button type="button" class="btn dsec pgdel" data-n="' + str(b['n']) + '">Löschen</button>') if ADM else '') + '</div></div>')
        if ADM:
            gin = ''
            for v in vars_:
                gin += '<label class="pgi"><span>' + esc(size_of(v)) + '</span><input type="number" min="0" max="500" class="pgq" data-v="' + str(v.id) + '" placeholder="0"></label>'
            gin += '<label class="pgi"><span>Größe unbekannt</span><input type="number" min="0" max="500" class="pgq" data-v="0" placeholder="0"></label>'
            gform = ('<details class="pfix"' + ('' if gns else ' open') + '><summary>Abgabe erfassen</summary>'
                     + '<p class="mut" style="font-size:13px">Defekte Teile, die nicht mehr bei uns sind (z. B. vom Lieferanten mitgenommen). Sie zählen im Vergleich mit, kommen aber in keinen Karton.</p>'
                     + '<input type="text" id="pgnote" maxlength="120" placeholder="Wer / wohin? z. B. Holfelder mitgenommen" style="margin-bottom:8px">'
                     + '<input type="date" id="pgdate" value="' + loc(now).strftime('%Y-%m-%d') + '" style="width:100%;padding:12px;border:1px solid #d1d5db;border-radius:8px;font-size:16px;margin-bottom:8px">'
                     + ('<select id="pgpick" style="width:100%;margin-bottom:8px">' + popts + '<option value="">ohne Lieferung</option></select>' if popts else '')
                     + '<div class="pgg">' + gin + '</div><button type="button" class="btn" id="pgsave" style="margin-top:10px;background:var(--grn)">Abgabe speichern</button></details>')
        else:
            gform = '<p class="mut" style="font-size:13px">Abgabe erfassen: <a href="' + QB + '&amp;view=mlogin&amp;next=' + (QB + '&view=pack&tmpl=' + str(t.id)).replace('&', '%26') + '">als Führungskraft anmelden</a>.</p>'
        gone_html = ('<div class="card"><h2>Bereits abgegeben (' + str(tg_) + ' Stk.)</h2>' + (glst or '<p class="mut">Nichts abgegeben.</p>') + gform + '</div>')
        lst = ''
        for b in bxs[::-1]:
            items = box_items(b)
            pk = Pick.browse(b['pick']).exists() if b['pick'] else Pick.browse([])
            lst += ('<div class="pli' + (' pligone' if b['state'] == 'gone' else '') + '"><div><b>Karton ' + str(b['n']) + '</b> '
                    + (('<span class="pgone" style="background:#b45309;color:#fff">' + esc(box_sup_name(b)) + '</span> ') if b.get('sup') else '')
                    + {'open': '<span class="popen">offen</span>', 'gone': '<span class="pgone">abgegeben</span>'}.get(b['state'], '<span class="pcl">abgeschlossen</span>')
                    + '<br><small class="mut">' + (ts_txt(b['x']) or ts_txt(b['c'])) + ((' · ' + esc(pick_label(pk))) if pk else '') + '</small>'
                    + (('<div class="pgn">Abgegeben: ' + esc(b['note']) + ' · ' + ts_txt(b.get('g'))[:10] + '</div>') if b['state'] == 'gone' else '')
                    + '<div class="pit">' + (', '.join([esc(it[0]) + ' × ' + str(it[2]) for it in items]) or '<span class="mut">leer</span>') + '</div></div>'
                    + '<div class="pact"><b class="pn">' + str(box_total(b)) + '</b>'
                    + (('<button type="button" class="btn dsec pre" data-n="' + str(b['n']) + '">Etikett</button><a class="btn dsec" target="_blank" href="' + QB + '&amp;boxpdf=' + str(t.id) + '-' + str(b['n']) + '">PDF</a>'
                        + ('' if (openb or b['state'] == 'gone' or GUEST) else '<button type="button" class="btn dsec pop" data-n="' + str(b['n']) + '">Öffnen</button>')
                        + (('<button type="button" class="btn dsec pbg" data-n="' + str(b['n']) + '">Karton abgegeben</button>') if (ADM and b['state'] == 'closed') else '')
                        + (('<button type="button" class="btn dsec pbb" data-n="' + str(b['n']) + '">Rückgängig</button>') if (ADM and b['state'] == 'gone') else '')) if b['state'] in ('closed', 'gone') else '') + '</div></div>')
        body = ('<div class="card" style="padding:12px 16px"><h2 style="margin:0">' + esc(t.name) + '</h2><small class="mut">' + str(len(bx_in)) + ' Karton(s) im Lager · ' + str(tp_) + ' Stk. verpackt' + ((' · ' + str(len(bx_gone)) + ' Karton(s) abgegeben') if bx_gone else '') + '</small></div>'
                + '<p class="err" id="perr"></p>' + box_html + cmp_html
                + '<div class="card"><h2>Alle Kartons</h2>' + (lst or '<p class="mut">Noch keine Kartons.</p>') + '</div>' + ('' if GUEST else gone_html)
                + '<p><a href="' + QB + '&amp;view=pack">← Alle Produkte</a></p>')
        response = resp(head('Defekte verpacken') + topbar('Defekte verpacken', QB + '&amp;view=pack') + '<div class="wrap">' + body + '</div>'
                        + '<script>var CSRF=' + jsq(request.csrf_token()) + ',KEY=' + jsq(KEY) + ',TMPL=' + jsq(str(t.id)) + ',BOXN=' + jsq(str(openb['n']) if openb else '')
                        + ',PDFU=' + jsq(QB + '&boxpdf=' + str(t.id) + '-') + ';' + PACK_JS + '</script></body></html>')

elif params.get('view') == 'draw' and not ADM:
    response = resp(head('Zeichnungen einrichten') + topbar('Zeichnungen einrichten', QB + '&amp;view=dash') + '<div class="wrap"><div class="card" style="max-width:520px;margin:20px auto">'
                    + '<h2>Nur für Führungskräfte</h2><p>Zeichnungen einrichten ist nur nach Anmeldung als Führungskraft möglich.</p>'
                    + '<a class="big blk" style="display:block;text-align:center;text-decoration:none" href="' + QB + '&amp;view=mlogin&amp;next=' + qself().replace('&', '%26') + '">Anmelden</a></div></div></body></html>')

elif params.get('view') == 'draw':
    # v19.14: "Zeichnungen einrichten" – own drawing per product (upload pictures, drag boxes, name them)
    tid_s = str(params.get('tmpl') or '')
    t = Tmpl.browse(int(tid_s)).exists() if tid_s.isdigit() else Tmpl.browse([])
    own_ids = list(set(Att.search([('res_model', '=', 'product.template'), ('name', '=', 'iq_qc_draw.txt')]).mapped('res_id')))
    own = Tmpl.browse(own_ids).exists()
    if not t:
        q = (params.get('q') or '').strip()
        cand = Tmpl.browse([])
        for c in QC.search([('quality_state', 'in', ['pass', 'fail'])], order='id desc', limit=600):
            if c.product_id.product_tmpl_id not in cand:
                cand |= c.product_id.product_tmpl_id
        cand |= own
        if q:
            cand = Tmpl.search(['|', ('name', 'ilike', q), ('default_code', 'ilike', q)], limit=30) | Tmpl.search([('product_variant_ids.default_code', 'ilike', q)], limit=30)
        rows_d = ''
        for x in sorted(cand, key=lambda x: (x.name or '').lower()):
            g = garm_of(x)
            st = ('<b style="color:var(--grn)">Eigene Zeichnung</b> (' + ', '.join([v[1] for v in loc_views(g)]) + ')') if is_custom(g) else ('Standard: ' + {'wmd': 'Wintermantel', 'wpu': 'Parka', 'mfjd': 'MFJ 4.0 Damen', 'mfjh': 'MFJ 4.0 Herren', 'gen': 'einfache Jacke'}.get(g, g))
            rows_d += '<a class="dl" style="text-decoration:none;display:flex;justify-content:space-between;gap:10px" href="' + QB + '&amp;view=draw&amp;tmpl=' + str(x.id) + '"><span><b>' + esc(x.name) + '</b><br><small class="mut">' + st + '</small></span><span>Bearbeiten →</span></a>'
        body = ('<div class="card"><h2>Zeichnungen einrichten</h2><p class="mut" style="margin-top:-4px">Für jedes Produkt eigene Bilder (z. B. Screenshots aus der Tech-Pack-PDF des Lieferanten) hochladen und die Teile als Kästen markieren. '
                + 'Diese Zeichnung erscheint dann beim Prüfen auf dem TC22, auf dem Etikett und im QC-Bericht.</p>'
                + '<form method="get" action="" style="display:flex;gap:8px"><input type="hidden" name="key" value="' + esc(KEY) + '"><input type="hidden" name="view" value="draw">'
                + '<input type="search" name="q" value="' + esc(q) + '" placeholder="Produkt suchen (Name oder Art.-Nr.)" style="flex:1"><button class="btn">Suchen</button></form></div>'
                + '<div class="card"><h2>Produkte</h2>' + (rows_d or '<p class="mut">Nichts gefunden.</p>') + '</div>')
        response = resp(head('Zeichnungen einrichten') + topbar('Zeichnungen einrichten', QB + '&amp;view=dash') + '<div class="wrap">' + body + '</div></body></html>')
    else:
        g = garm_of(t)
        cd = cdraw(t.id)
        js_views = []
        for v in ['V', 'H', 'I']:
            c = cd.get(v)
            if c:
                zs = []
                for z in c['z']:
                    zs.append('[' + jsq(z[0]) + ',' + jsq(z[1]) + ',' + str(z[2]) + ',' + str(z[3]) + ',' + str(z[4]) + ',' + str(z[5]) + ']')
                js_views.append(v + ':{src:' + jsq(QB + '&dimg=' + str(c['img'])) + ',w:' + str(c['w']) + ',h:' + str(c['h']) + ',z:[' + ','.join(zs) + ']}')
            else:
                js_views.append(v + ':{src:"",w:0,h:0,z:[]}')
        copy_opts = ''.join(['<option value="' + str(x.id) + '">' + esc(x.name) + '</option>' for x in own if x.id != t.id])
        parts = ['Kapuze', 'Kragen', 'Kragen / Kapuze', 'Schulter rechts', 'Schulter links', 'Brust rechts', 'Brust links', 'Brusttasche rechts', 'Brusttasche links',
                 'Front-Reißverschluss / Leiste', 'Druckknöpfe', 'Ärmel rechts', 'Ärmel links', 'Bündchen rechts', 'Bündchen links', 'Seitentasche rechts', 'Seitentasche links',
                 'Pattentasche rechts', 'Pattentasche links', 'Bauchtasche / Kängurutasche', 'Kordel / Tunnelzug', 'Saum / Bund', 'Rücken oben', 'Rücken Mitte', 'Rücken unten',
                 'Rückentasche', 'Patch Ärmel rechts', 'Patch Ärmel links', 'Innentasche rechts', 'Innentasche links', 'Futter rechts', 'Futter links', 'Futter Rücken',
                 'Nacken / Etikett', 'Zip-off', 'Unterteil rechts', 'Unterteil links', 'MOLLE-Schlaufe', 'Gürtel / Schnalle', 'Magnetfach', 'MagDock-Clip']
        body = ('<div class="card"><h2>Zeichnung: ' + esc(t.name) + '</h2>'
                + '<p class="mut" style="margin-top:-4px">' + (('Dieses Produkt hat eine <b>eigene Zeichnung</b>.') if is_custom(g) else ('Zurzeit wird die Standard-Zeichnung benutzt. Bild hochladen, um eine eigene anzulegen.')) + '</p>'
                + '<ol class="dsteps"><li>Seite wählen (Vorne / Hinten / Innen) und <b>Bild hochladen</b> – z. B. Screenshot aus der Tech-Pack-PDF.</li>'
                + '<li>Mit Finger oder Maus ein <b>Rechteck über ein Teil ziehen</b> und unten einen Namen geben (z. B. „Kapuze“).</li>'
                + '<li>Rechts/links immer <b>vom Träger aus</b>: auf der Vorderseite ist „rechts“ im Bild links.</li>'
                + '<li>Unten Manager-PIN eingeben und <b>Speichern</b>.</li></ol>'
                + '<div class="lseg" id="dv"><button type="button" data-v="V" class="on">Vorne</button><button type="button" data-v="H">Hinten</button><button type="button" data-v="I">Innen</button></div>'
                + '<div id="dstage" class="dstage"><img id="dimgel" alt=""><div id="dboxes"></div><div id="dempty">Noch kein Bild für diese Seite.</div></div>'
                + '<div class="drow"><label class="btn dup">Bild hochladen<input type="file" accept="image/*" id="dfile" hidden></label>'
                + '<button type="button" class="btn dsec" id="dclear">Bild dieser Seite entfernen</button></div>'
                + '<p class="mut" id="dinfo" style="font-size:13px"></p>'
                + '<h3 style="margin:14px 0 6px">Teile auf dieser Seite</h3><div id="dzl"></div><datalist id="dparts">' + ''.join(['<option value="' + esc(x) + '">' for x in parts]) + '</datalist></div>'
                + '<div class="card"><h2>Speichern</h2><div class="drow"><span class="mut" style="flex:1;min-width:160px;font-size:13px">Angemeldet als Führungskraft (noch ' + str(ADM_LEFT) + ' Min.)</span>'
                + '<button type="button" class="btn" id="dsave" style="background:var(--grn)">Zeichnung speichern</button></div><p id="dmsg" style="font-weight:700"></p></div>'
                + (('<div class="card"><h2>Von anderem Produkt übernehmen</h2><p class="mut" style="margin-top:-4px">Gleiches Modell in anderer Farbe oder Variante? Zeichnung + Kästen kopieren.</p><div class="drow"><select id="dfrom" style="flex:1">' + copy_opts + '</select>'
                    + '<button type="button" class="btn" id="dcopy">Übernehmen</button></div></div>') if copy_opts else '')
                + ('<div class="card"><button type="button" class="btn dsec" id="ddel" style="color:var(--red);border-color:var(--red)">Eigene Zeichnung löschen (zurück zur Standard-Zeichnung)</button></div>' if is_custom(g) else '')
                + '<p><a href="' + QB + '&amp;view=draw">← Alle Produkte</a></p>')
        html = (head('Zeichnung einrichten') + topbar('Zeichnung einrichten', QB + '&amp;view=draw') + '<div class="wrap">' + body + '</div>'
                + '<script>var CSRF=' + jsq(request.csrf_token()) + ',KEY=' + jsq(KEY) + ',TMPL=' + jsq(str(t.id)) + ',DV={' + ','.join(js_views) + '};' + EDIT_JS + '</script></body></html>')
        response = resp(html)

elif params.get('view') == 'import':
    nd = imp_done()
    sel = ''
    for art, lab in [('WMD', 'Wintermantel Damen (PO 10319)'), ('WPU', 'Unisex Winter Parka (PO 10337)')]:
        pks = imp_picks(art)
        sel += ('<label style="display:block;font-weight:700;margin:12px 0 4px">Wareneingang für ' + lab + '</label><select id="pick_' + art + '" style="width:100%;padding:10px;font-size:15px">'
                + (''.join(['<option value="' + str(pk.id) + '">' + esc(pick_label(pk)) + '</option>' for pk in pks]) or '<option value="">– kein Wareneingang gefunden –</option>') + '</select>')
    if nd:
        body = ('<div class="card"><h2>Papier-Import</h2><p><b>Schon importiert</b> (' + str(nd) + ' Prüfungen).</p>'
                + '<p class="mut">Falls etwas falsch ist: rückgängig machen und neu importieren.</p>'
                + '<button class="big" id="undo" style="background:var(--red);color:#fff">Import rückgängig machen</button><p id="msg"></p></div>')
    else:
        body = ('<div class="card"><h2>Papier-Import (einmalig)</h2>'
                + '<p>Importiert die Papierprüfungen 11.–16.11.2026: Wintermantel Damen 263 OK + 50 Defekte, Unisex Parka 90 OK + 4 Defekte – mit Fotos.</p>'
                + sel
                + '<label style="display:block;font-weight:700;margin:16px 0 4px">Fotos (alle Dateien aus dem Ordner QC_photos auswählen)</label>'
                + '<input type="file" id="ph" multiple accept="image/*" style="width:100%;padding:10px;border:1px dashed #999;border-radius:8px">'
                + '<p class="mut" id="cnt"></p><button class="big blk" id="go">Hochladen &amp; importieren</button>'
                + '<div style="height:8px;background:#eee;border-radius:4px;margin-top:10px"><div id="bar" style="height:8px;width:0;background:#151515;border-radius:4px"></div></div><p id="msg"></p></div>')
    html = (head('Papier-Import') + topbar('Papier-Import', QB + '&amp;view=dash') + '<div class="wrap">' + body + '</div>'
            + '<script>var CSRF="' + request.csrf_token() + '",KEY="' + KEY + '";var m=document.getElementById("msg");'
            + 'function send(fd){var x=new XMLHttpRequest();x.open("POST",location.pathname);'
            + 'x.upload.onprogress=function(e){var b=document.getElementById("bar");if(b&&e.lengthComputable)b.style.width=Math.round(100*e.loaded/e.total)+"%"};'
            + 'x.onload=function(){var a=x.responseText.split("|");m.style.color=a[0]==="OK"?"green":"#b91c1c";m.innerHTML="<b>"+(a[1]||x.responseText)+"</b>"+(a[0]==="OK"?"<br><a href=?key="+KEY+"&view=dash>Zum Dashboard</a>":"");var g=document.getElementById("go");if(g){g.disabled=false;g.textContent="Hochladen & importieren"}};'
            + 'x.onerror=function(){m.textContent="Keine Verbindung – bitte nochmal."};x.send(fd)}'
            + 'var ph=document.getElementById("ph");if(ph)ph.onchange=function(){document.getElementById("cnt").textContent=ph.files.length+" Fotos ausgewählt (erwartet: 78)"};'
            + 'var go=document.getElementById("go");if(go)go.onclick=function(){if(!ph.files.length){m.textContent="Bitte zuerst die Fotos auswählen.";return}'
            + 'var fd=new FormData();fd.append("csrf_token",CSRF);fd.append("key",KEY);fd.append("act","import");'
            + '["WMD","WPU"].forEach(function(a){fd.append("pick_"+a,document.getElementById("pick_"+a).value)});'
            + 'for(var i=0;i<ph.files.length;i++)fd.append("photo",ph.files[i],ph.files[i].name);go.disabled=true;go.textContent="Lädt hoch …";m.textContent="";send(fd)};'
            + 'var un=document.getElementById("undo");if(un)un.onclick=function(){if(!confirm("Import wirklich rückgängig machen?"))return;var fd=new FormData();fd.append("csrf_token",CSRF);fd.append("key",KEY);fd.append("act","import_undo");send(fd)};'
            + '</script></body></html>')
    response = resp(html)

elif request.httprequest.method == 'POST' and params.get('act') in ('draw_save', 'draw_copy', 'draw_del'):
    # v19.14: save / copy / delete a product's own drawing (managers only: manager PIN of the warehouse calendar)
    MPD = (P.get_param('iq.delivery_calendar_manager_pin') or '').strip()
    fkd = 'iq.cal_pinfail.M'
    fvd = (P.get_param(fkd) or '0|0').split('|')
    fails_d = int(fvd[0]) if fvd[0].isdigit() else 0
    fts_d = int(fvd[1]) if len(fvd) > 1 and fvd[1].isdigit() else 0
    nowts_d = int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds())
    tid_s = str(params.get('tmpl') or '')
    t = Tmpl.browse(int(tid_s)).exists() if tid_s.isdigit() else Tmpl.browse([])
    DRAWN = ['iq_qc_draw.txt']
    for v in ['V', 'H', 'I']:
        DRAWN += ['iq_qc_draw_' + v + '.jpg', 'iq_qc_draw_' + v + '_line.png', 'iq_qc_draw_' + v + '.bits']
    if not ADM:
        response = txt('ERR|Anmeldung abgelaufen – bitte in einem neuen Tab als Führungskraft anmelden, dann hier nochmal speichern.')
    elif not t:
        response = txt('ERR|Produkt nicht gefunden.')
    else:
        act_d = params.get('act')
        mine = Att.search([('res_model', '=', 'product.template'), ('res_id', '=', t.id), ('name', 'in', DRAWN)])
        if act_d == 'draw_del':
            mine.unlink()
            response = txt('OK|deleted')
        elif act_d == 'draw_copy':
            fs_ = str(params.get('from') or '')
            src_t = Tmpl.browse(int(fs_)).exists() if fs_.isdigit() else Tmpl.browse([])
            src_a = Att.search([('res_model', '=', 'product.template'), ('res_id', '=', src_t.id), ('name', 'in', DRAWN)]) if src_t else Att.browse([])
            if not src_a or src_t.id == t.id:
                response = txt('ERR|Das andere Produkt hat keine eigene Zeichnung.')
            else:
                mine.unlink()
                for a in src_a:
                    Att.create({'name': a.name, 'raw': a.raw, 'mimetype': a.mimetype, 'res_model': 'product.template', 'res_id': t.id})
                response = txt('OK|copied')
        else:
            cfg_out = []
            err_d = ''
            for v in ['V', 'H', 'I']:
                names_v = ['iq_qc_draw_' + v + '.jpg', 'iq_qc_draw_' + v + '_line.png', 'iq_qc_draw_' + v + '.bits']
                if params.get('clear_' + v) == '1':
                    Att.search([('res_model', '=', 'product.template'), ('res_id', '=', t.id), ('name', 'in', names_v)]).unlink()
                    continue
                fimg = request.httprequest.files.get('img_' + v)
                if fimg:
                    dimg = fimg.read()
                    fline = request.httprequest.files.get('line_' + v)
                    fbits = request.httprequest.files.get('bits_' + v)
                    dline = fline.read() if fline else b''
                    dbits = fbits.read() if fbits else b''
                    if not dimg or len(dimg) > 6000000 or not (fimg.mimetype or 'image/jpeg').lower().startswith('image/'):
                        err_d = 'Bild ' + v + ' leer oder größer als 6 MB'
                        continue
                    Att.search([('res_model', '=', 'product.template'), ('res_id', '=', t.id), ('name', 'in', names_v)]).unlink()
                    Att.create({'name': names_v[0], 'raw': dimg, 'mimetype': 'image/jpeg', 'res_model': 'product.template', 'res_id': t.id})
                    if dline:
                        Att.create({'name': names_v[1], 'raw': dline, 'mimetype': 'image/png', 'res_model': 'product.template', 'res_id': t.id})
                    if dbits[:4] == b'IQB1':
                        Att.create({'name': names_v[2], 'raw': dbits, 'mimetype': 'application/octet-stream', 'res_model': 'product.template', 'res_id': t.id})
                has_img = Att.search_count([('res_model', '=', 'product.template'), ('res_id', '=', t.id), ('name', '=', names_v[0])])
                ws_ = str(params.get('w_' + v) or '')
                hs_ = str(params.get('h_' + v) or '')
                if not has_img or not ws_.isdigit() or not hs_.isdigit():
                    continue
                cfg_out.append('SIZE|' + v + '|' + ws_ + '|' + hs_)
                for zl in str(params.get('zones_' + v) or '').split(chr(10))[:80]:
                    zp = zl.split(chr(9))
                    if len(zp) != 6 or not loc_code_ok(zp[0]) or zp[0][:1] != v:
                        continue
                    nm = zp[1].replace('|', '/').replace(chr(13), ' ').strip()[:60]
                    nums_ok = True
                    for x in zp[2:]:
                        if not x.isdigit():
                            nums_ok = False
                    if nm and nums_ok:
                        cfg_out.append('Z|' + zp[0] + '|' + nm + '|' + '|'.join(zp[2:]))
            Att.search([('res_model', '=', 'product.template'), ('res_id', '=', t.id), ('name', '=', 'iq_qc_draw.txt')]).unlink()
            if cfg_out:
                Att.create({'name': 'iq_qc_draw.txt', 'raw': chr(10).join(cfg_out).encode('utf-8'), 'mimetype': 'text/plain', 'res_model': 'product.template', 'res_id': t.id})
            response = txt(('ERR|' + err_d) if err_d else 'OK|saved')

elif params.get('dimg'):
    a = Att.browse(int(params.get('dimg') or 0)).exists() if str(params.get('dimg')).isdigit() else Att.browse([])
    if a and a.res_model == 'product.template' and (a.name or '').startswith('iq_qc_draw_'):
        response = request.make_response(a.raw, headers=[('Content-Type', a.mimetype or 'image/jpeg'), ('Cache-Control', 'private, max-age=600')])
    else:
        response = request.make_response('Not found', headers=[('Content-Type', 'text/plain')], status=404)

elif params.get('img'):
    a = Att.browse(int(params.get('img') or 0)).exists() if str(params.get('img')).isdigit() else Att.browse([])
    if a and a.res_model == 'quality.alert':
        response = request.make_response(a.raw, headers=[('Content-Type', a.mimetype or 'image/jpeg'), ('Cache-Control', 'private, max-age=86400')])
    else:
        response = request.make_response('Not found', headers=[('Content-Type', 'text/plain')], status=404)

# ------------------------------------------------------------------ direct PDF file, without PrintNode or a connected printer
elif params.get('pdf_label'):
    aid = str(params.get('pdf_label') or '')
    al = QA.browse(int(aid)).exists() if aid.isdigit() else QA.browse([])
    response = pdf_download_response(al) if al else request.make_response('Defekt nicht gefunden', status=404)

# ------------------------------------------------------------------ step 2 of QC + photos added later
elif params.get('photo_for'):
    aid = str(params.get('photo_for') or '')
    al = QA.browse(int(aid)).exists() if aid.isdigit() else QA.browse([])
    if not al or not al.product_id:
        response = txt('Defekt nicht gefunden')
    elif params.get('stage') == 'late' and not ADM:
        response = resp(head('Foto hinzufügen') + topbar('Foto hinzufügen', QB + '&amp;view=dash') + '<div class="wrap"><div class="card" style="max-width:520px;margin:20px auto">'
                        + '<h2>Nur für Führungskräfte</h2><p>Fotos zu einem gespeicherten Defekt kann nur eine Führungskraft nachträglich hinzufügen.</p>'
                        + '<a class="big blk" style="display:block;text-align:center;text-decoration:none" href="' + QB + '&amp;view=mlogin&amp;next=' + qself().replace('&', '%26') + '">Anmelden</a></div></div></body></html>')
    else:
        stage2 = params.get('stage') == '2'
        noteentry = is_note(al)
        pr = params.get('pr') or ''
        pe = (params.get('pe') or '')[:180]
        ap = al.product_id
        ppick = al.picking_id if 'picking_id' in AF else False
        scan_url = '?key=' + KEY + '&tmpl=' + str(ap.product_tmpl_id.id) + (('&pick=' + str(ppick.id)) if ppick else '')
        detail_url = '?key=' + KEY + '&view=prod&tmpl=' + str(ap.product_tmpl_id.id) + (('&pick=' + str(ppick.id)) if ppick else '')
        return_url = scan_url if stage2 or params.get('back') == 'scan' else detail_url
        ims = Att.search([('res_model', '=', 'quality.alert'), ('res_id', '=', al.id), ('mimetype', '=like', 'image%')], order='id')
        reason = ', '.join(tags_of(al)) or (al.title if 'title' in AF else 'Defekt')
        lg = locs_of(al)
        fblocks = ''
        for fi0, it in enumerate(lg[1]):
            fi = str(fi0 + 1)
            fpics = ''
            for im in ims:
                if ('-F' + fi + '-') in (im.name or ''):
                    fpics += '<div class="photo-ok"><img src="' + QB + '&amp;img=' + str(im.id) + '" alt=""><span>Foto hochgeladen</span></div>'
            names = []
            for z in it[1]:
                names.append(loc_label(z, lg[0]))
            fblocks += ('<div class="fblk"><div class="fbh"><b>' + fi + '. ' + esc(it[0]) + '</b><span>' + esc(', '.join(names) or 'ohne Ort') + '</span></div>'
                        + loc_draws(lg[0], it[1], 'mini') + '<div class="fph" id="ph-' + fi + '">' + fpics + '</div>'
                        + ('' if stage2 else '<button type="button" class="smallaction" data-f="' + fi + '">Foto zu Fehler ' + fi + '</button>') + '</div>')
        cardpics = ''.join(['<div class="photo-ok"><img src="' + QB + '&amp;img=' + str(im.id) + '" alt=""><span>Foto hochgeladen</span></div>' for im in ims if not (fblocks and '-F' in (im.name or ''))])
        nophoto = 'Kein Foto – die Zeichnung zeigt die Stelle' if lg[1] else 'Kein Foto (optional)'
        sz = sz_parts(size_of(ap))[1]
        intro = ('Hinweis gespeichert' if noteentry else ('Gespeichert – Etikett-PDF herunterladen und an die Jacke kleben' if not PRINT_ENABLED else 'Gespeichert – Etikett an die Jacke kleben')) if stage2 else 'Foto hinzufügen'
        status = ('Druckauftrag an Brother gesendet' if pr == '1' else ('PDF bereit – noch kein Druckauftrag gesendet' if pr in ('D', 'B') else ('Druck fehlgeschlagen: ' + pe if pr == '0' else ''))) if stage2 and not noteentry else ''
        html = (head('Fotos zu ' + esc(al.name)) + topbar('Foto · ' + esc(al.name), scan_url.replace('&', '&amp;') if stage2 else detail_url.replace('&', '&amp;')) + '<div class="wrap">'
                + '<div class="photo-hint">' + intro + '</div>'
                + '<div class="photo-head"><div class="mut" style="font-weight:700">' + ('Schritt 2 von 2 · ' if stage2 else '') + ('Hinweis – kein Defekt' if noteentry else 'Defekt') + '</div>'
                + '<div class="qa">' + esc(al.name) + '</div><div class="detail">Gr. ' + esc(sz) + ' · ' + esc(reason) + '</div>'
                + '<div class="mut" style="font-size:12px;margin-top:8px">' + esc(ap.product_tmpl_id.name) + ' · Art.-Nr. ' + esc(ap.default_code or ap.product_tmpl_id.default_code or '–') + '</div></div>'
                + (('<div class="card"><h2>Etikett</h2><div id="print-status" class="mut">' + esc(status) + '</div>'
                    + '<a id="download_pdf" class="' + ('smallaction' if PRINT_ENABLED else 'big blk') + '" href="' + QB + '&amp;pdf_label=' + str(al.id) + '" download="' + esc(al.name) + '.pdf">Etikett-PDF herunterladen</a>'
                    + (' <button type="button" id="printer" class="smallaction">Nochmal drucken</button>' if PRINT_ENABLED else '') + '</div>') if stage2 and not noteentry else '')
                + (('<div class="card"><h2>Fehler an dieser Jacke</h2>' + fblocks + '</div>') if fblocks else '')
                + '<div class="card"' + (' style="display:none"' if stage2 and fblocks else '') + '><h2>' + ('Weitere Fotos (optional)' if fblocks else 'Fotos · sofortiger Upload · optional') + '</h2><div id="photos">' + cardpics + '</div>'
                + '<div id="counter" data-count="' + str(len(ims)) + '" class="mut" style="margin:10px 0">' + (str(len(ims)) + ' Foto(s) hochgeladen' if ims else nophoto) + '</div>'
                + '<input type="file" id="cam" accept="image/*" capture="environment" style="display:none">'
                + '<button type="button" class="big blk" id="take">Foto aufnehmen</button><button type="button" class="smallaction" id="retry" style="display:none">Upload wiederholen</button>'
                + '<p class="mut" id="photo-status" style="font-weight:700"></p><p class="err" id="err"></p></div>'
                + '<button type="button" class="big ok" id="done">' + ('Fertig – nächstes Teil scannen' if return_url == scan_url else 'Fertig – zurück zu den Details') + '</button>'
                + (('<button type="button" class="smallaction" id="cancel" style="width:100%;color:var(--red);border-color:var(--red)">Abbrechen – ' + ('Hinweis' if noteentry else 'Defekt') + ' löschen</button>') if stage2 else '')
                + '</div><script>var CSRF=' + jsq(request.csrf_token()) + ',KEY=' + jsq(KEY) + ',AID=' + jsq(str(al.id)) + ',QA=' + jsq(al.name) + ',CID=' + jsq(str(al.check_id.id) if 'check_id' in AF and al.check_id else '0')
                + ',STAGE2=' + ('true' if stage2 else 'false') + ',ISNOTE=' + ('true' if noteentry else 'false') + ',HAS_PRINTER=' + ('true' if PRINT_ENABLED else 'false')
                + ',RETURN_URL=' + jsq(return_url) + ',SCAN_URL=' + jsq(scan_url) + ',NOPH=' + jsq(nophoto) + ';' + PHOTO_JS + '</script></body></html>')
        response = resp(html)

# ------------------------------------------------------------------ label
elif params.get('label'):
    al = QA.browse(int(params.get('label'))).exists() if str(params.get('label')).isdigit() else QA.browse([])
    response = (resp(label_html(al)) if params.get('preview') == '1' else pdf_download_response(al)) if al else txt('Etikett nicht gefunden')

# ------------------------------------------------------------------ dashboard
elif params.get('view') == 'dash':
    per = params.get('per') or 'all'
    q = (params.get('q') or '').strip()
    ql = q.lower()
    since = {'1': today, '7': today - datetime.timedelta(days=7), '30': today - datetime.timedelta(days=30)}.get(per, False)
    dom = [('quality_state', 'in', ['pass', 'fail'])] + AUTO
    if since:
        dom.append(('create_date', '>=', datetime.datetime.combine(since, datetime.time(0, 0)) - datetime.timedelta(hours=2)))
    cs = QC.search(dom, order='create_date desc')
    agg = {}
    sess = {}
    for c in cs:
        t = c.product_id.product_tmpl_id
        if t.id not in agg:
            agg[t.id] = [t, 0, 0, {}, 0]
        agg[t.id][1] += 1
        if c.quality_state == 'fail':
            agg[t.id][2] += 1
        pid = c.picking_id.id if 'picking_id' in CF and c.picking_id else 0
        sk = str(t.id)
        if sk not in sess:
            sess[sk] = [t, [], c.create_date, 0, 0, 0]
        if pid and c.picking_id not in sess[sk][1]:
            sess[sk][1].append(c.picking_id)
        if not pid:
            sess[sk][5] += 1
        sess[sk][3] += 1
        if c.quality_state == 'fail':
            sess[sk][4] += 1
    adom = [('product_tmpl_id', 'in', list(agg.keys()))]
    if since:
        adom.append(('create_date', '>=', datetime.datetime.combine(since, datetime.time(0, 0)) - datetime.timedelta(hours=2)))
    als = QA.search(adom + SUPXA, order='create_date desc')
    nts = {}
    for al in als:
        if is_note(al):
            nts[al.product_tmpl_id.id] = nts.get(al.product_tmpl_id.id, 0) + 1
    als = [a for a in als if not is_note(a)]
    for al in als:
        if al.product_tmpl_id.id in agg:
            agg[al.product_tmpl_id.id][4] += 1
            for tn in tags_of(al):
                agg[al.product_tmpl_id.id][3][tn] = agg[al.product_tmpl_id.id][3].get(tn, 0) + 1
    keep = [k for k in agg if not ql or ql in (agg[k][0].name or '').lower() or [r for r in agg[k][3] if ql in r.lower() or ql in tl(r).lower()]]
    tot = sum([agg[k][1] for k in keep])
    bad = sum([agg[k][2] for k in keep])
    rate = (100.0 * bad / tot) if tot else 0
    qs = ('&amp;q=' + esc(q)) if q else ''
    fl = ''.join(['<a class="' + ('on' if per == k else '') + '" href="' + QB + '&amp;view=dash&amp;per=' + k + qs + '">' + l + '</a>' for k, l in [('1', 'Heute'), ('7', '7 Tage'), ('30', '30 Tage'), ('all', 'Gesamt')]])
    srch = ('<form method="get" action="" class="noprint" style="margin-bottom:10px"><input type="hidden" name="key" value="' + KEY + '"><input type="hidden" name="view" value="dash">'
            '<input type="hidden" name="per" value="' + esc(per) + '"><input type="search" name="q" value="' + esc(q) + '" placeholder="Produkt oder Grund suchen"></form>')
    srows = ''
    for s in sorted([sess[k] for k in sess if int(k) in keep], key=lambda s: s[2], reverse=True)[:8]:
        r = 100.0 * s[4] / s[3] if s[3] else 0
        srows += ('<tr><td class="rn"><b>' + esc(s[0].name) + '</b><br><small class="mut">' + ', '.join([esc(pk.origin or pk.name) for pk in s[1][:4]] + (['+' + str(len(s[1]) - 4)] if len(s[1]) > 4 else []) + ([str(s[5]) + '× ohne Lieferung'] if s[5] else [])) + ' · zuletzt ' + loc(s[2]).strftime('%d.%m. %H:%M') + '</small></td>'
                  + '<td class="r rc" data-l="Geprüft">' + str(s[3]) + '</td><td class="r rc' + (' neg' if s[4] else '') + '" data-l="Defekt">' + str(s[4]) + '</td><td class="r rc" data-l="Quote">' + ('%.1f' % r).replace('.', ',') + ' %</td>'
                  + '<td class="r rl"><a href="' + QB + '&amp;view=report&amp;tmpl=' + str(s[0].id) + '">Bericht</a><br class="dsk"><a href="' + QB + '&amp;view=prod&amp;tmpl=' + str(s[0].id) + '" style="font-size:12px">Details</a></td></tr>')
    drows = ''
    for al in [a for a in als if a.product_tmpl_id.id in keep and (not ql or ql in (a.product_tmpl_id.name or '').lower() or [r for r in tags_of(a) if ql in r.lower() or ql in tl(r).lower()])][:10]:
        im = Att.search([('res_model', '=', 'quality.alert'), ('res_id', '=', al.id), ('mimetype', '=like', 'image%')], order='id', limit=1)
        drows += ('<a class="dl" style="text-decoration:none;grid-template-columns:64px 1fr" href="' + QB + '&amp;view=prod&amp;tmpl=' + str(al.product_tmpl_id.id) + '">'
                  + ('<img loading="lazy" style="width:64px;height:64px" src="' + QB + '&amp;img=' + str(im.id) + '" alt="">' if im else (('<div class="ndraw">' + loc_svg(locs_of(al)[0], (loc_codes(al) or ['V-'])[0][:1], loc_codes(al), {}, False, 'mini') + '</div>') if loc_codes(al) else '<div style="width:64px;height:64px;border-radius:8px;background:#eee"></div>'))
                  + '<div><b>' + esc(al.name) + '</b> · ' + esc(al.product_tmpl_id.name) + ' · Gr. <b>' + esc(al_size(al)) + '</b><br>'
                  + ''.join(['<span class="tag">' + esc(tl(t)) + '</span> ' for t in tags_of(al)]) + (('<small>» ' + esc(loc_text(al)) + '</small><br>') if loc_text(al) else '') + '<small class="mut">' + loc(al.create_date).strftime('%d.%m. %H:%M') + '</small></div></a>')
    cards = ''
    for v in sorted([agg[k] for k in keep], key=lambda v: -(v[2] * 1.0 / v[1] if v[1] else 0)):
        r = 100.0 * v[2] / v[1] if v[1] else 0
        top = sorted(v[3].items(), key=lambda kv: -kv[1])[:3]
        nog = v[2] - v[4]
        info = ' · '.join([esc(tl(k)) + ' (' + str(n) + ')' for k, n in top] + ([str(nog) + ' ohne Grund'] if nog > 0 else []) + ([str(nts[v[0].id]) + ' Hinweise (kein Defekt)'] if nts.get(v[0].id) else []))
        cards += ('<a class="pc ' + ('hi' if r >= 10 else ('mid' if r >= 5 else 'lo')) + '" href="' + QB + '&amp;view=prod&amp;tmpl=' + str(v[0].id) + '"><h3>' + esc(v[0].name) + '</h3>'
                  + '<div class="ctx" style="margin:0"><span>Geprüft <b>' + str(v[1]) + '</b></span><span style="color:var(--grn)">OK <b style="color:var(--grn)">' + str(v[1] - v[2]) + '</b></span>'
                  + '<span style="color:var(--red)">Defekt <b style="color:var(--red)">' + str(v[2]) + '</b></span><span><b>' + ('%.1f' % r).replace('.', ',') + ' %</b></span></div>'
                  + '<div class="bar"><i style="width:' + ('%.1f' % min(r, 100)) + '%"></i></div>'
                  + '<small class="mut">' + (info or 'Keine Defekte') + ' →</small></a>')
    # v19.15: open goods receipts with clothing (products with sizes) that still need QC – shown at the top of the dashboard
    todo = ''
    tdom = [('picking_type_code', '=', 'incoming'), ('state', 'not in', ['done', 'cancel', 'draft'])] + SUPDOM
    tseen = {}
    tn = 0
    for pk in Pick.search(tdom, order='scheduled_date asc', limit=80):
        ptm = {}
        for mv in pk.move_ids:
            if mv.state == 'cancel':
                continue
            t = mv.product_id.product_tmpl_id
            ptm[t.id] = ptm.get(t.id, 0.0) + (mv.product_uom_qty or 0.0)
        for tid in ptm:
            t = Tmpl.browse(tid)
            if tid not in tseen:
                cl = False
                for vv in t.product_variant_ids[:30]:
                    if size_rank(size_of(vv)) < 50:
                        cl = True
                tseen[tid] = cl
            if not tseen[tid]:
                continue
            ck = QC.search_count([('picking_id', '=', pk.id), ('product_id.product_tmpl_id', '=', tid), ('quality_state', 'in', ['pass', 'fail'])] + AUTO) if 'picking_id' in CF else 0
            dl = int(ptm[tid])
            pct = min(100.0, 100.0 * ck / dl) if dl else 0.0
            g = garm_of(t)
            if not ADM:
                dst = ''
            elif is_custom(g):
                dst = '<span class="tds tdsok">✓ Eigene Zeichnung</span>'
            elif g == 'gen':
                dst = '<span class="tds tdswarn">' + ICW + 'Keine Zeichnung – <u>einrichten</u></span>'
            else:
                dst = '<span class="tds">Standard-Zeichnung</span>'
            od = pk.scheduled_date and pk.scheduled_date < now
            tn += 1
            todo += ('<div class="tdc' + (' od' if od else '') + '"><div class="tdh"><b>' + esc(t.name) + '</b>'
                     + ('<span class="tdod">Überfällig</span>' if od else '') + '</div>'
                     + '<div class="mut" style="font-size:13px">' + esc(pk.partner_id.commercial_partner_id.name or '') + ' · ' + esc(pk.origin or pk.name)
                     + (' · erwartet ' + loc(pk.scheduled_date).strftime('%d.%m.%Y') if pk.scheduled_date else '') + ' (' + esc(pk.name) + ')</div>'
                     + '<div class="tdn"><span>Geprüft <b>' + str(ck) + '</b> / ' + str(dl) + ' Stk.</span><span>' + ('%.0f' % pct) + ' %</span></div>'
                     + '<div class="bar tdbar"><i style="width:' + ('%.1f' % pct) + '%"></i></div>'
                     + '<div class="tdf">' + (('<a class="tdl" href="' + QB + '&amp;view=draw&amp;tmpl=' + str(tid) + '">' + dst + '</a>') if dst else '<span></span>')
                     + '<a class="btn tdgo" href="' + ctx_q(t, pk) + '">Prüfen starten →</a></div>'
                     + (('<form method="post" action="" style="margin:8px 0 0;text-align:right"><input type="hidden" name="csrf_token" value="' + request.csrf_token() + '"><input type="hidden" name="key" value="' + KEY + '">'
                         + '<input type="hidden" name="act" value="sup_start"><input type="hidden" name="hrs" value="10"><input type="hidden" name="sup" value="' + str(pk.partner_id.commercial_partner_id.id) + '">'
                         + '<button class="btn" style="background:#fff;color:#b45309;border:1px solid #b45309;min-height:34px;padding:6px 10px;font-size:13px" onclick="return confirm(' + chr(39) + 'Lieferanten-Prüfung für ' + esc(pk.partner_id.commercial_partner_id.name or '').replace(chr(39), ' ') + ' auf diesem Gerät starten? Beenden nur mit Manager-PIN.' + chr(39) + ')">Lieferant prüft selbst (Gastmodus)</button></form>') if ADM else '')
                     + '</div>')
    todo_html = ('<div class="card todo"><h2>Zu prüfen – offene Wareneingänge (' + str(tn) + ')</h2>'
                 + '<p class="mut" style="margin-top:-4px;font-size:13px">Bekleidung aus offenen Wareneingängen (Erwartet / Teilweise gebucht). „Prüfen starten“ öffnet die Prüfung mit dieser Lieferung.</p>'
                 + '<div class="tdg">' + todo + '</div></div>') if todo else ''
    # v19.17: supplier checks (separate from the IQ figures above)
    scs = QC.search([('quality_state', 'in', ['pass', 'fail']), ('note', 'ilike', 'IQ-SUP:')], order='create_date desc', limit=5000) if 'note' in CF else QC.browse([])
    sgg = sup_groups(scs)
    sdr = ''
    for k in sgg[1][:25]:
        spn = Partner.browse(k[1]).exists()
        v = sgg[0][k]
        sdr += ('<tr><td>' + k[0].strftime('%d.%m.%Y') + '</td><td>' + esc(spn.name if spn else '') + '</td><td>' + esc(Tmpl.browse(k[2]).name) + '</td><td class="r">' + str(v[0]) + '</td><td class="r" style="color:#b91c1c;font-weight:700">' + str(v[2])
                + '</td><td class="r">' + str(sup_taken(k[1], k[0], k[2])) + '</td><td class="r"><a href="' + QB + '&amp;view=prod&amp;tmpl=' + str(k[2]) + '">QC Details</a></td></tr>')
    sstart = ''
    if ADM:
        sops = ''
        for spr in Pick.search([('picking_type_code', '=', 'incoming'), ('state', '!=', 'cancel')] + SUPDOM, order='id desc', limit=500).mapped('partner_id').mapped('commercial_partner_id'):
            sops += '<option value="' + str(spr.id) + '">' + esc(spr.name) + '</option>'
        sstart = ('<form method="post" action="" style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:8px"><input type="hidden" name="csrf_token" value="' + request.csrf_token() + '"><input type="hidden" name="key" value="' + KEY + '">'
                  + '<input type="hidden" name="act" value="sup_start"><select name="sup" required style="width:auto;display:inline-block;min-width:240px;max-width:100%"><option value="">Lieferant wählen …</option>' + sops + '</select>'
                  + '<select name="hrs" style="width:auto;display:inline-block"><option value="4">4 Std.</option><option value="8">8 Std.</option><option value="10" selected>10 Std.</option><option value="12">12 Std.</option></select>'
                  + '<button class="btn" style="background:#b45309;min-height:44px" onclick="return confirm(\'Dieses Gerät in den Lieferanten-Modus schalten? Beenden nur mit Manager-PIN.\')">Lieferanten-Prüfung auf diesem Gerät starten</button></form>'
                  + '<p class="mut" style="font-size:12.5px;margin:6px 0 0">Der Lieferant prüft dann mit der normalen Prüfseite (Scan, OK / Defekt mit Ort, Foto, Etikett) – nur Artikel aus seinen Lieferungen (offen und gebucht). Kein Dashboard, keine anderen Lieferanten. Beenden mit Manager-PIN oder automatisch nach Ablauf.</p>')
    sup_html = (('<div class="card"><h2>Lieferanten-Prüfungen</h2><p class="mut" style="margin-top:-4px;font-size:13px">Vom Lieferanten selbst geprüft – ist in allen Zahlen und Listen enthalten (Prüfer „Firma – Name“). Hier zusätzlich: wie viel er mitgenommen hat.</p>'
                 + ('<table class="rtab"><tr><th>Datum</th><th>Lieferant</th><th>Produkt</th><th class="r">Geprüft</th><th class="r">Defekt</th><th class="r">Mitgenommen</th><th></th></tr>' + sdr + '</table>' if sdr else '')
                 + sstart + '</div>') if (sdr or ADM) else '')
    html = (head('QC Dashboard') + topbar('QC Dashboard', '') + '<div class="wrap wide">'
            + '<div class="dtop"><div class="dbtns"><a class="big ok noprint start-check" style="text-align:center;text-decoration:none;padding:16px;margin:0" href="' + QB + '">Prüfen starten</a>'
            + '<a class="big noprint dpack" href="' + QB + '&amp;view=pack">Defekte verpacken</a></div>'
            + '<div class="fl" style="margin:0">' + fl + '</div>' + srch.replace('margin-bottom:10px', 'margin:0') + '</div>'
            + '<div class="kp"><div><small>Geprüft</small><b>' + str(tot) + '</b></div><div class="g"><small>OK</small><b>' + str(tot - bad) + '</b></div>'
            + '<div class="d"><small>Defekt</small><b>' + str(bad) + '</b></div><div><small>Defektquote</small><b>' + ('%.1f' % rate).replace('.', ',') + ' %</b></div></div>'
            + todo_html + sup_html
            + '<div class="dg"><div class="dside">'
            + ('<div class="card"><h2>Letzte Prüfberichte</h2><table class="rtab"><tr><th>Produkt / Lieferung</th><th class="r">Geprüft</th><th class="r">Defekt</th><th class="r">Quote</th><th></th></tr>' + srows + '</table></div>' if srows else '')
            + ('<div class="card nd"><h2>Neueste Defekte</h2>' + drows + '</div>' if drows else '')
            + '</div><div class="dmain"><h2>Produkte</h2><div class="pgrid">'
            + (cards or '<div class="card mut">Noch keine Prüfungen.</div>') + '</div></div></div>'
            + '<p class="mut" style="font-size:12px">Rot = Defektquote ab 10 %, Gelb = ab 5 %, Grün = darunter. Klick auf ein Produkt zeigt Größen, Gründe und alle Fotos.'
            + (' · <a class="noprint" href="' + QB + '&amp;view=draw">Zeichnungen einrichten</a>' if ADM else '') + ' · <a class="noprint" href="' + QB + '&amp;view=import">Papier-Import</a> · <a class="noprint" href="' + QB + '&amp;view=import_hf">Holfelder-Import</a></p></div></body></html>')
    if params.get('gend'):
        html = html.replace('</body>', '<script>try{localStorage.removeItem("iq_qc_who")}catch(e){}</script></body>')
    response = resp(html)

# ------------------------------------------------------------------ product details + report
elif params.get('view') in ('prod', 'report'):
    tmpl = Tmpl.browse(int(params.get('tmpl') or 0)).exists() if str(params.get('tmpl') or '').isdigit() else Tmpl.browse([])
    pick = get_pick()
    if not tmpl:
        response = txt('Produkt nicht gefunden')
    else:
        rep = params.get('view') == 'report'
        # Source of truth: one quality.check per inspected piece (not photo counts or alert tags).
        cs_all = checks_for(tmpl, pick, False)
        local_today = loc(now).date()
        period = str(params.get('period') or 'all')
        if period not in ('all', 'today', '7', '30'):
            period = 'all'
        inspector = inspector_key(str(params.get('inspector') or ''))
        people = {}
        for c in cs_all:
            nm = check_who(c)
            k = inspector_key(nm)
            if k not in people:
                people[k] = nm
        cs = [c for c in cs_all if in_period(c.create_date, period, local_today) and (not inspector or inspector_key(check_who(c)) == inspector)]
        # Inspector totals follow exactly the selected period and inspector filter.
        # The old today-only table went to zero at midnight, although yesterday's
        # checks (e.g. Manuela, 18 Nov) remained in the database.
        period_stats = {}
        for c in cs:
            nm = check_who(c)
            k = inspector_key(nm)
            if k not in period_stats:
                period_stats[k] = [nm, 0, 0, 0]
            period_stats[k][1] += 1
            if c.quality_state == 'fail':
                period_stats[k][3] += 1
            else:
                period_stats[k][2] += 1
        selected_check_ids = set([c.id for c in cs])
        bys = {}
        for c in cs:
            s = chk_size(c)
            if s not in bys:
                bys[s] = [0, 0]
            bys[s][0] += 1
            if c.quality_state == 'fail':
                bys[s][1] += 1
        adom = [('product_tmpl_id', '=', tmpl.id)]
        if pick and 'picking_id' in AF:
            adom.append(('picking_id', '=', pick.id))
        als_all = QA.search(adom + SUPXA, order='create_date desc')
        notes_all = [a for a in als_all if is_note(a)]
        if period == 'all' and not inspector:
            # Unfiltered legacy view must remain unchanged, including imported note-only alerts.
            als_view = als_all
        else:
            als_view = []
            for al in als_all:
                if 'check_id' in AF and al.check_id:
                    if al.check_id.id in selected_check_ids:
                        als_view.append(al)
                elif in_period(al.create_date, period, local_today) and (not inspector or inspector_key(who_of(al) or 'Prüfer nicht angegeben') == inspector):
                    # Legacy note-only alerts without quality.check are for evidence, not inspected-piece totals.
                    als_view.append(al)
        notes = [a for a in als_view if is_note(a)]
        als = [a for a in als_view if not is_note(a)]
        nbys = {}
        for al in notes:
            nbys[al_size(al)] = nbys.get(al_size(al), 0) + 1
        bko = ''
        if pick:
            dem = {}
            for mv in pick.move_ids:
                if mv.product_id.product_tmpl_id.id == tmpl.id and mv.state != 'cancel':
                    dem[mv.product_id.id] = dem.get(mv.product_id.id, 0) + int(round(mv.product_uom_qty or 0))
            okv = {}
            badv = {}
            unk = 0
            for c in cs_all:
                if chk_size(c) == '?':
                    unk += 1
                elif c.quality_state == 'pass':
                    okv[c.product_id.id] = okv.get(c.product_id.id, 0) + 1
                else:
                    badv[c.product_id.id] = badv.get(c.product_id.id, 0) + 1
            nv = {}
            for al in notes_all:
                nv[al.product_id.id] = nv.get(al.product_id.id, 0) + 1
            vids = sorted(list(set(list(dem.keys()) + list(okv.keys()) + list(badv.keys()))), key=lambda i: size_rank(size_of(Prod.browse(i))))
            tt = [0, 0, 0, 0, 0]
            brow = ''
            for i in vids:
                d = dem.get(i, 0)
                o = okv.get(i, 0)
                b = badv.get(i, 0)
                h = nv.get(i, 0)
                op = max(0, d - o - b)
                tt = [tt[0] + d, tt[1] + o, tt[2] + h, tt[3] + b, tt[4] + op]
                brow += ('<tr><td><b>' + esc(size_of(Prod.browse(i))) + '</b></td><td class="r">' + str(d) + '</td><td class="r" style="color:var(--grn);font-weight:700">' + str(min(o, d) if d else o) + ('<small class="neg"> (+' + str(o - d) + ' mehr als geliefert)</small>' if d and o > d else '') + '</td>'
                         + '<td class="r">' + (str(h) if h else '–') + '</td><td class="r' + (' neg' if b else '') + '">' + str(b) + '</td><td class="r">' + str(op) + '</td></tr>')
            brow += ('<tr style="border-top:2px solid #151515"><td><b>Summe</b></td><td class="r"><b>' + str(tt[0]) + '</b></td><td class="r" style="color:var(--grn)"><b>' + str(tt[1]) + '</b></td><td class="r"><b>' + str(tt[2]) + '</b></td>'
                     + '<td class="r neg"><b>' + str(tt[3]) + '</b></td><td class="r"><b>' + str(tt[4]) + '</b></td></tr>')
            bko = ('<div class="card"><h2>Buchungsübersicht – ' + esc(pick.name) + (' (offen)' if pick_open(pick) else ' (schon gebucht)') + '</h2>'
                   + '<div style="overflow-x:auto"><table style="min-width:520px"><tr><th>Größe</th><th class="r">Geliefert</th><th class="r">OK – wird gebucht</th><th class="r">davon Hinweis</th><th class="r">Defekt – nicht gebucht</th><th class="r">Nicht geprüft</th></tr>' + brow + '</table></div>'
                   + ('<p class="mut" style="font-size:12px">' + str(unk) + ' Prüfungen ohne Größe (Papier-Import) sind hier nicht enthalten.</p>' if unk else '')
                   + '<p class="mut" style="font-size:12px">Gebucht wird nur „OK“: Button „QC: OK-Mengen übernehmen“ im Wareneingang (Aktionsmenü), danach Prüfen/Validieren in Odoo. Defekte und nicht geprüfte Teile werden nicht gebucht.</p></div>')
        reasons = {}
        for al in als:
            for tn in (tags_of(al) or ['Ohne Grund']):
                reasons[tn] = reasons.get(tn, 0) + 1
        tot = len(cs)
        bad = len([c for c in cs if c.quality_state == 'fail'])
        srows = ''.join(['<tr><td><b>' + esc(s) + '</b></td><td class="r">' + str(v[0]) + '</td><td class="r">' + str(v[0] - v[1]) + '</td><td class="r hcol">' + (str(nbys[s]) if nbys.get(s) else '–') + '</td><td class="r' + (' neg' if v[1] else '') + '">' + str(v[1]) + '</td>'
                         + '<td class="r">' + ('%.1f' % (100.0 * v[1] / v[0] if v[0] else 0)).replace('.', ',') + ' %</td></tr>' for s, v in sorted(bys.items(), key=lambda kv: size_rank(kv[0]))])
        rrows = ''.join(['<tr><td>' + esc(k) + '</td><td class="r">' + str(n) + '</td><td class="r">' + ('%.0f' % (100.0 * n / bad if bad else 0)) + ' %</td></tr>' for k, n in sorted(reasons.items(), key=lambda kv: -kv[1])])
        dl = ''
        nl = ''
        fsz = []
        frs = []
        fos = []
        heat = {}
        hgar = ''
        nloc = 0
        for al in list(als) + list(notes):
            isn = is_note(al)
            ims = Att.search([('res_model', '=', 'quality.alert'), ('res_id', '=', al.id), ('mimetype', '=like', 'image%')], order='id')
            desc = str(al.description or '') if 'description' in AF else ''
            imp = IMARK in desc or HFMARK in desc
            note = desc.replace(MISSING_HTML, '').split('<p>Prüfer:')[0].split('<p>Größe:')[0].split('<p>Nachgetragen')[0].replace(NOTEMARK + ' kein Defekt – wird gebucht, beobachten', '').replace('<p>', '').replace('</p>', ' ').strip()
            who = desc.split('Prüfer:')[1].split('<')[0].strip() if 'Prüfer:' in desc else ''
            if 'IQ-SUP:' in desc:
                who = sup_label(desc, who)
            szv = al_size(al)
            tgs = tags_of(al) or ['Ohne Grund']
            if szv not in fsz and not isn:
                fsz.append(szv)
            for t in tgs:
                if t not in frs and not isn:
                    frs.append(t)
            pics = ''.join(['<img loading="lazy" src="' + QB + '&amp;img=' + str(i.id) + '" data-g="' + str(al.id) + '" alt="">' for i in ims])
            if rep and isn:
                continue
            lg = locs_of(al)
            lcodes = loc_codes(al)
            wo = ''
            for it in lg[1]:
                names = []
                for z in it[1]:
                    names.append(loc_label(z, lg[0]))
                wo += '<div class="wo"><b>' + esc(it[0]) + '</b> » ' + esc(', '.join(names) or 'ohne Ort') + '</div>'
            if lcodes and not isn:
                nloc += 1
                if not hgar:
                    hgar = lg[0]
                for z in lcodes:
                    heat[z] = heat.get(z, 0) + 1
                    if z not in fos:
                        fos.append(z)
            ldr = loc_draws(lg[0], lcodes, 'mini') if lcodes else ''
            if lcodes and not ldr:
                ldr = '<b>' + esc(loc_label('X-ALL')) + '</b>'
            if rep:
                # v19.16.6: report card – every photo complete (not cropped), drawing below, no links, no names
                card = ('<div class="rk">' + (('<div class="rph' + (' r1' if len(ims) == 1 else '') + '">' + ''.join(['<img class="rimg" src="' + QB + '&amp;img=' + str(i.id) + '" alt="">' for i in ims]) + '</div>') if ims else '')
                        + '<div class="bd"><div class="hd"><span class="szp">' + esc(szv) + '</span>' + ''.join(['<span class="rs">' + esc(t) + '</span>' for t in tgs]) + '</div>'
                        + wo + ('<div class="tx">' + esc(note.replace(PACKMARK + ' Beim Verpacken der Defekt-Kartons gefunden – keine Einzeldokumentation, kein Foto.', 'Beim Verpacken gefunden – ohne Einzelfoto.')) + '</div>' if note else '')
                        + (('<div class="rdraw">' + ldr + '</div>') if ldr else '')
                        + '<div class="meta">' + esc(al.name) + ' · ' + loc(al.create_date).strftime('%d.%m.%Y') + (' · Lieferantenprüfung ' + esc(Partner.browse(sup_id_of(desc)).name or '') if 'IQ-SUP:' in desc else '') + (' · ' + esc(al.picking_id.name) if 'picking_id' in AF and al.picking_id else '') + (' · ' + str(len(ims)) + ' Fotos' if len(ims) > 1 else '') + '</div></div></div>')
                dl += card
                continue
            card = ('<div class="dk' + (' nt' if isn else '') + '" data-s="' + esc(szv) + '" data-r="' + esc('|'.join(tgs)) + '" data-o="' + esc('|'.join(lcodes)) + '">'
                   + (('<div class="pics' + (' one' if len(ims) == 1 else '') + (' hasd' if ldr else '') + '"' + ((' data-n="+' + str(len(ims) - 1) + '"') if len(ims) > 1 else '') + '>' + pics + (('<div class="pdraw">' + ldr + '</div>') if ldr else '') + '</div>') if ims else (('<div class="nopic locpic">' + ldr + '</div>') if ldr else '<div class="nopic photo-missing">Foto fehlt</div>'))
                   + '<div class="bd"><div class="hd"><span class="szp">' + esc(szv) + '</span>' + ('<span class="rs">Foto fehlt</span>' if not ims and not ldr else '') + ('<span class="rs nt">Hinweis – kein Defekt</span>' if isn else '') + ''.join(['<span class="rs' + (' nt' if isn else '') + '">' + esc(t) + '</span>' for t in tgs]) + '</div>'
                   + wo + ('<div class="tx">' + esc(note) + '</div>' if note else '')
                   + '<div class="meta">' + esc(al.name) + ' · ' + loc(al.create_date).strftime('%d.%m.%Y %H:%M') + (' · <b>Lieferantenprüfung</b>' if 'IQ-SUP:' in desc else '') + (' · ' + esc(who) if who else '')
                   + (' · ' + esc(al.picking_id.name) if 'picking_id' in AF and al.picking_id else '') + (' · ' + str(len(ims)) + ' Fotos' if len(ims) > 1 else '') + (' <span class="imp">nachgetragen</span>' if imp else '') + '</div>'
                   + ('' if rep else '<div class="ac noprint"><a href="/odoo/quality.alert/' + str(al.id) + '" target="_blank">In Odoo öffnen ↗</a>' + ('' if isn else ((' · <a href="' + QB + '&amp;pdf_label=' + str(al.id) + '" download>PDF herunterladen</a>' + (' · <a href="#" data-rp="' + str(al.id) + '">Etikett neu drucken</a>' if PRINT_ENABLED else ''))))
                   + ((' · <a href="' + QB + '&amp;tmpl=' + str(al.product_id.product_tmpl_id.id) + '&amp;defect=' + str(al.product_id.id) + '&amp;edit=' + str(al.id) + ('&amp;kind=note' if isn else '') + (('&amp;pick=' + str(al.picking_id.id)) if 'picking_id' in AF and al.picking_id else '') + '" style="font-weight:800">Bearbeiten</a>') if ADM else '')
                   + ((' · <a href="' + QB + '&amp;photo_for=' + str(al.id) + '&amp;stage=late">Foto hinzufügen</a> · <a href="#" data-del="' + str(al.id) + '" data-n="' + esc(al.name) + '" style="color:var(--red)">Löschen</a>') if ADM else '') + '</div>')
                   + '</div></div>')
            if isn:
                nl += card
            else:
                dl += card
        fsz = sorted(fsz, key=lambda x: size_rank(x))
        flt = ''
        if len(als) > 1:
            flt = ('<div class="flt" id="fs"><span class="lb">Größe</span><button class="on" data-v="">Alle Größen</button>' + ''.join(['<button data-v="' + esc(x) + '">' + esc(x) + '</button>' for x in fsz]) + '</div>'
                   + '<div class="flt" id="fr"><span class="lb">Grund</span><button class="on" data-v="">Alle Gründe</button>' + ''.join(['<button data-v="' + esc(x) + '">' + esc(x) + '</button>' for x in frs]) + '</div>'
                   + (('<div class="flt" id="fo"><span class="lb">Ort</span><button class="on" data-v="">Alle Orte</button>' + ''.join(['<button data-v="' + esc(kv[0]) + '">' + esc(loc_label(kv[0], hgar or garm_of(tmpl))) + ' (' + str(kv[1]) + ')</button>' for kv in sorted(heat.items(), key=lambda kv: -kv[1])]) + '</div>') if fos else ''))
        heat_html = ''
        if heat:
            hg = hgar or garm_of(tmpl)
            figs = ''
            for v in LOC_VIEWS:
                vn = 0
                for z in heat:
                    if z.startswith(v[0] + '-'):
                        vn += heat[z]
                hsvg = loc_svg(hg, v[0], [], heat, False, 'heat')
                if (vn or v[0] != 'I') and hsvg:
                    figs += '<figure class="lfig">' + hsvg + '<figcaption>' + v[1] + ' (' + str(vn) + ')</figcaption></figure>'
            hrows = ''
            for kv in sorted(heat.items(), key=lambda kv: -kv[1]):
                hrows += '<tr><td>' + esc(loc_label(kv[0], hg)) + '</td><td class="r">' + str(kv[1]) + '</td><td class="r">' + ('%.0f' % (100.0 * kv[1] / nloc if nloc else 0)) + ' %</td></tr>'
            heat_html = ('<div class="card"><h2>Wo sind die Defekte? (' + str(nloc) + ' Defekte mit Ort)</h2>'
                         + '<p class="mut" style="font-size:13px;margin-top:-4px">Rechts/links vom Träger aus gesehen. Zahl = Anzahl Defekte an dieser Stelle.</p>'
                         + '<div class="ldr-row heat">' + figs + '</div>'
                         + '<table class="heatt"><tr><th>Ort</th><th class="r">Anzahl</th><th class="r">Anteil</th></tr>' + hrows + '</table></div>')
        picks = Pick.browse(list(set([c.picking_id.id for c in cs_all if 'picking_id' in CF and c.picking_id])))
        pfl = ('<div class="fl noprint"><a class="' + ('' if pick else 'on') + '" href="' + QB + '&amp;view=prod&amp;tmpl=' + str(tmpl.id) + '">Alle Lieferungen</a>'
               + ''.join(['<a class="' + ('on' if pick and pk.id == pick.id else '') + '" href="' + QB + '&amp;view=prod&amp;tmpl=' + str(tmpl.id) + '&amp;pick=' + str(pk.id) + '" title="' + esc(pick_label(pk)) + '">' + esc(pick_short(pk)) + '</a>' for pk in picks]) + '</div>') if picks else ''
        chosen_label = people.get(inspector, 'Prüfer nicht angegeben') if inspector else 'Alle Prüfer'
        # HTML GET form makes period/inspector persistent when switching to the printable report.
        opts_time = [('all', 'Alle Zeiträume'), ('today', 'Heute'), ('7', 'Letzte 7 Tage'), ('30', 'Letzte 30 Tage')]
        time_opts = ''.join(['<option value="' + v + '"' + (' selected' if period == v else '') + '>' + lab + '</option>' for v, lab in opts_time])
        people_opts = '<option value="">Alle Prüfer</option>' + ''.join(['<option value="' + esc(k) + '"' + (' selected' if inspector == k else '') + '>' + esc(people[k]) + '</option>' for k in sorted(people, key=lambda x: people[x].lower())])
        base_url = QB + '&amp;view=prod&amp;tmpl=' + str(tmpl.id) + (('&amp;pick=' + str(pick.id)) if pick else '')
        filter_bar = ('<form method="get" action="" class="card qcfilter noprint">'
                      + '<input type="hidden" name="key" value="' + esc(KEY) + '">'
                      + '<input type="hidden" name="view" value="' + ('report' if rep else 'prod') + '">'
                      + '<input type="hidden" name="tmpl" value="' + str(tmpl.id) + '">'
                      + (('<input type="hidden" name="pick" value="' + str(pick.id) + '">') if pick else '')
                      + '<div class="qcfilter-row"><label class="qcfilter-item"><b>Zeitraum</b><select name="period" aria-label="Zeitraum auswählen" onchange="this.form.submit()">' + time_opts + '</select></label>'
                      + '<label class="qcfilter-item"><b>Prüfer</b><select name="inspector" aria-label="Prüfer auswählen" onchange="this.form.submit()">' + people_opts + '</select></label>'
                      + '<a class="reset" href="' + base_url + '">Filter zurücksetzen</a></div>'
                      + '<p class="qcfilter-note">Nur angezeigte Prüfungen und Defekte · Gesamtbestand in der Buchungsübersicht bleibt unverändert.</p></form>')
        period_total = [0, 0, 0]
        day_rows = ''
        for k in sorted(period_stats, key=lambda x: period_stats[x][1], reverse=True):
            val = period_stats[k]
            period_total = [period_total[0] + val[1], period_total[1] + val[2], period_total[2] + val[3]]
            day_rows += ('<tr' + (' class="warnrow"' if val[0] == 'Prüfer nicht angegeben' else '') + '><td><b>' + esc(val[0]) + '</b></td>'
                         + '<td>' + str(val[1]) + '</td><td>' + str(val[2]) + '</td><td>' + str(val[3]) + '</td></tr>')
        if not day_rows:
            day_rows = '<tr><td colspan="4" class="mut">Keine Prüfungen im gewählten Zeitraum.</td></tr>'
        daily_box = ('<div class="card"><div class="today-head"><h2>Prüfungen nach Prüfer</h2><span class="today-pill">' + str(period_total[0]) + ' geprüft</span></div>'
                     + '<div class="today-table-wrap"><table class="today-table"><tr><th>Prüfer</th><th>Geprüft</th><th>OK</th><th>Defekt</th></tr>' + day_rows + '</table></div>'
                     + '<p class="qcfilter-note">Zeitraum: ' + esc(dict(opts_time).get(period, 'Alle Zeiträume')) + ' · ' + ('Lieferung ' + esc(pick.name) if pick else 'Alle Lieferungen') + '. Grundlage: Speicherdatum der QC-Prüfung.</p></div>')
        active_query = (('&amp;period=' + esc(period)) if period != 'all' else '') + (('&amp;inspector=' + esc(inspector)) if inspector else '')
        title = ('QC-Bericht' if rep else 'QC Details') + ' – ' + esc(tmpl.name)
        qdone = qc_done_of(tmpl.id)
        rfinal = bool(qdone)
        html = (head(title) + ('' if rep else topbar('QC Details', QB + '&amp;view=dash')) + '<div class="wrap wide' + (' rep' if rep else '') + '">'
                + ('<div class="noprint rbar"><button class="btn" id="rprint" disabled>Fotos werden geladen …</button> <button class="btn" style="background:#e9e9e6;color:#151515" onclick="history.back()">Zurück</button>'

                   + '<p class="mut" id="rstat" style="font-size:13px;margin:6px 0 0">Der Druck-Knopf wird aktiv, sobald alle Fotos geladen sind.</p></div>' if rep else '')
                + (('<div class="rhead"><img src="' + LOGO + '" alt="IQ Dogsport"><span>IQ Dogsport GmbH · Qualitätsprüfung Wareneingang</span></div>') if rep else '')
                + ('' if (not rep or rfinal) else '<div class="rnotfinal"><b>ZWISCHENSTAND – NICHT FINAL</b><br>Die Qualitätsprüfung ist noch nicht abgeschlossen. Zahlen können sich bis zum Endbericht noch ändern.</div>')
                + ('' if rep else ('<div class="card qdone' + (' on' if qdone else '') + '">' + (('<b>✓ Prüfung abgeschlossen</b> am ' + ts_txt(qdone[0])[:10] + ((' – ' + esc(qdone[1])) if qdone[1] else '') + ' · Der QC-Bericht ist ein Endbericht.') if qdone else '<b>Prüfung läuft</b> · Der QC-Bericht ist ein Zwischenstand (nicht final).')
                                   + ((' <button class="btn" id="qdbtn" data-a="' + ('qc_reopen' if qdone else 'qc_done') + '">' + ('Wieder öffnen' if qdone else 'Prüfung abschließen') + '</button>') if ADM else '') + '</div>'))
                + '<div class="card"><h2>' + (('Qualitätsprüfbericht' + (' – Endbericht' if rfinal else ' – Zwischenstand')) if rep else 'Produkt') + '</h2><div style="font:800 20px Arial">' + esc(tmpl.name) + '</div>'
                + '<div class="mut">' + (('Lieferung ' + esc(pick_label(pick)) + ' · ') if pick else 'Alle Lieferungen · ') + 'Stand ' + loc(now).strftime('%d.%m.%Y %H:%M') + (' · ' + esc(chosen_label) if (inspector and not rep) else '') + (' · ' + dict(opts_time).get(period, '') if period != 'all' else '') + '</div></div>'
                + ('' if rep else (pfl + filter_bar + daily_box)) + bko
                + '<div class="kp"><div><small>Geprüft</small><b>' + str(tot) + '</b></div><div class="g"><small>OK</small><b>' + str(tot - bad) + '</b></div><div class="d"><small>Defekt</small><b>' + str(bad) + '</b></div>'
                + '<div><small>Defektquote</small><b>' + ('%.1f' % (100.0 * bad / tot if tot else 0)).replace('.', ',') + ' %</b></div></div>'
                + ('' if rep else '<div class="noprint" style="margin-bottom:12px"><a class="btn" href="' + QB + '&amp;view=report&amp;tmpl=' + str(tmpl.id) + ('&amp;pick=' + str(pick.id) if pick else '') + active_query + '">QC-Bericht erstellen</a> '
                   + '<a class="btn" style="background:var(--grn)" href="' + ctx_q(tmpl, pick) + '">Weiter prüfen</a> '
                   + (('<a class="btn" style="background:#e9e9e6;color:#151515" href="' + QB + '&amp;view=draw&amp;tmpl=' + str(tmpl.id) + '">Zeichnung einrichten</a>') if ADM else '') + '</div>')
                + '<div class="two"><div class="card"><h2>Nach Größe</h2><table><tr><th>Größe</th><th class="r">Geprüft</th><th class="r">OK</th><th class="r hcol">Hinweis</th><th class="r">Defekt</th><th class="r">Quote</th></tr>' + srows + '</table></div>'
                + '<div class="card"><h2>Fehlergründe</h2>' + (('<table><tr><th>Grund</th><th class="r">Anzahl</th><th class="r">Anteil</th></tr>' + rrows + '</table>') if rrows else '<p class="mut">Keine Defekte.</p>') + '</div>'
                + '</div>' + heat_html + '<div class="card"><h2>' + ('Defekte' if rep else 'Alle Defekte') + ' (<span id="dn">' + str(len(als)) + '</span>)</h2>' + ('' if rep else flt) + '<div class="' + ('rkg' if rep else 'dkg') + '">' + (dl or '<p class="mut">Keine Defekte.</p>') + '</div></div>'
                + (('<div class="card' + (' hidep' if rep else '') + '"><h2>Hinweise – kein Defekt (' + str(len(notes)) + ')</h2><p class="mut" style="font-size:13px;margin-top:-4px">Auffällig, aber in Ordnung: diese Teile werden gebucht. Fotos zum Nachweis für den Lieferanten, im Auge behalten.</p><div class="dkg">' + nl + '</div></div>') if nl else '') + '</div>'
                + '<div class="lbx" id="lbx"><img id="lbi" alt=""><button class="x" id="lbc">×</button><button class="pv" id="lbp">‹</button><button class="nx" id="lbn">›</button><div class="cap" id="lbt"></div></div>'
                + '<script>var CSRF="' + request.csrf_token() + '",KEY="' + KEY + '";'
                + 'function post(d,cb){var fd=new FormData();fd.append("csrf_token",CSRF);fd.append("key",KEY);for(var k in d)fd.append(k,d[k]);'
                + 'fetch(location.pathname,{method:"POST",body:fd,credentials:"same-origin"}).then(function(r){return r.text()}).then(function(t){var a=t.split("|");if(a[0]==="OK")cb(a);else alert(a[1]||t)}).catch(function(){alert("Keine Verbindung – bitte nochmal.")})}'
                + 'document.querySelectorAll("[data-rp]").forEach(function(b){b.onclick=function(e){e.preventDefault();post({act:"print",aid:b.dataset.rp},function(){b.textContent="Gedruckt"})}});'
                + 'document.querySelectorAll("[data-del]").forEach(function(b){b.onclick=function(e){e.preventDefault();if(!confirm(b.dataset.n+" wirklich löschen? Fotos und Prüfung werden mit gelöscht."))return;'
                + 'post({act:"del",aid:b.dataset.del},function(){location.reload()})}});'
                + 'var FS="",FR="",FO="";function filt(){var n=0;document.querySelectorAll(".dk").forEach(function(d){var ok=(!FS||d.dataset.s===FS)&&(!FR||("|"+d.dataset.r+"|").indexOf("|"+FR+"|")>=0)&&(!FO||("|"+(d.dataset.o||"")+"|").indexOf("|"+FO+"|")>=0);d.style.display=ok?"":"none";if(ok)n++});var dn=document.getElementById("dn");if(dn)dn.textContent=n}'
                + '["fs","fr","fo"].forEach(function(id){var g=document.getElementById(id);if(!g)return;g.querySelectorAll("button").forEach(function(b){b.onclick=function(){g.querySelectorAll("button").forEach(function(x){x.classList.remove("on")});b.classList.add("on");if(id==="fs")FS=b.dataset.v;else if(id==="fo")FO=b.dataset.v;else FR=b.dataset.v;filt()}})});'
                + 'var LB=[],LI=0,lbx=document.getElementById("lbx"),lbi=document.getElementById("lbi");function lshow(){lbi.src=LB[LI].src;document.getElementById("lbt").textContent=(LI+1)+" / "+LB.length+" · "+LB[LI].cap}'
                + 'document.querySelectorAll(".dk .pics img").forEach(function(im){im.onclick=function(){LB=[];document.querySelectorAll(".dk").forEach(function(d){if(d.style.display==="none")return;var cap="Gr. "+d.dataset.s+" · "+d.dataset.r.split("|").join(", ");d.querySelectorAll(".pics img").forEach(function(x){if(x===im)LI=LB.length;LB.push({src:x.src,cap:cap})})});lshow();lbx.classList.add("show")}});'
                + 'function lmove(d){if(!LB.length)return;LI=(LI+d+LB.length)%LB.length;lshow()}'
                + 'if(lbx){document.getElementById("lbc").onclick=function(){lbx.classList.remove("show")};document.getElementById("lbp").onclick=function(){lmove(-1)};document.getElementById("lbn").onclick=function(){lmove(1)};'
                + 'lbx.onclick=function(e){if(e.target===lbx)lbx.classList.remove("show")};document.addEventListener("keydown",function(e){if(!lbx.classList.contains("show"))return;if(e.key==="Escape")lbx.classList.remove("show");if(e.key==="ArrowLeft")lmove(-1);if(e.key==="ArrowRight")lmove(1)});'
                + 'var tx0=0;lbx.addEventListener("touchstart",function(e){tx0=e.touches[0].clientX},{passive:true});lbx.addEventListener("touchend",function(e){var dx=e.changedTouches[0].clientX-tx0;if(Math.abs(dx)>50)lmove(dx<0?1:-1)})}'
                + 'var QD=document.getElementById("qdbtn");if(QD)QD.onclick=function(){var a=QD.dataset.a,n="";if(a==="qc_done"){n=prompt("Prüfung für dieses Produkt abschließen? Der QC-Bericht wird dann zum Endbericht. Optional: Bemerkung","");if(n===null)return}else if(!confirm("Prüfung wieder öffnen? Der Bericht wird wieder ein Zwischenstand."))return;post({act:a,tmpl:"' + str(tmpl.id) + '",note:n},function(){location.reload()})};'
                + '</script>' + (REP_JS if rep else '') + '</body></html>')
        if rep:
            # no clickable links in the report (the link contains the access key)
            html = html.replace('<a ', '<span ').replace('</a>', '</span>')
        response = resp(html)

# ------------------------------------------------------------------ check screen (product chosen)
elif params.get('tmpl') and str(params.get('tmpl')).isdigit():
    tmpl = Tmpl.browse(int(params.get('tmpl'))).exists()
    pick = get_pick()
    if tmpl and not pick and not params.get('defect') and params.get('nopick') != '1' and params.get('np') != '1':
        opk = open_picks(tmpl)
        if len(opk) == 1:
            pick = opk
    if not tmpl:
        response = txt('Produkt nicht gefunden')
    elif params.get('defect') and params.get('edit') and not ADM:
        response = resp(head('Bearbeiten') + topbar('Bearbeiten', QB + '&amp;view=dash') + '<div class="wrap"><div class="card" style="max-width:520px;margin:20px auto">'
                        + '<h2>Nur für Führungskräfte</h2><p>Defekte bearbeiten kann nur eine angemeldete Führungskraft.</p>'
                        + '<a class="big blk" style="display:block;text-align:center;text-decoration:none" href="' + QB + '&amp;view=mlogin&amp;next=' + qself().replace('&', '%26') + '">Anmelden</a></div></div></body></html>')
    elif params.get('defect'):
        p = Prod.browse(int(params.get('defect'))).exists() if str(params.get('defect')).isdigit() else Prod.browse([])
        NT = params.get('kind') == 'note'
        ED = QA.browse(int(params.get('edit'))).exists() if str(params.get('edit') or '').isdigit() and ADM else QA.browse([])
        used = {}
        for al in QA.search([('product_tmpl_id', '=', tmpl.id)], limit=300, order='create_date desc'):
            for tn in tags_of(al):
                tn = clean_reason(tn)
                used[tn] = used.get(tn, 0) + 1
        names = [n for n in DEF_TAGS if not reason_hidden(n)]
        for pin in PIN_TAGS:
            if pin not in names:
                names.append(pin)
        if TAG:
            for old_name in TAG.search([], limit=60).mapped('name'):
                tn = clean_reason(old_name)
                if tn not in names and not reason_hidden(tn):
                    names.append(tn)
        for tn in used:
            if tn not in names and not reason_hidden(tn):
                names.append(tn)
        tg = sorted(names, key=lambda n: (-used.get(n, 0), tl(n).lower()))
        topr = tg[:6]
        # Always show these as tap buttons, even when they were not used yet (most important defects).
        for pin in PIN_TAGS:
            if pin not in topr and not reason_hidden(pin):
                topr.append(pin)
        rchips = '<div class="chips chips-primary" id="rchips">' + ''.join(['<button type="button" data-n="' + esc(n) + '">' + esc(tl(n)) + '</button>' for n in topr]) + '</div>'
        ropts = ('<option value="">Anderer Grund? Hier alle Gründe A–Z …</option>'
                 + ''.join(['<option value="' + esc(n) + '">' + esc(tl(n)) + '</option>' for n in sorted([x for x in tg if x not in topr], key=lambda n: tl(n).lower())])
                 + '<option value="__new">Neuer Grund (eingeben) …</option>')
        primary = ''.join(['<button type="button" data-n="' + esc(n) + '">' + esc(tl(n)) + '</button>' for n in tg[:6]])
        secondary = ''.join(['<button type="button" data-n="' + esc(n) + '">' + esc(tl(n)) + '</button>' for n in tg[6:]])
        chips = ('<div id="chips"><div class="chips chips-primary">' + primary + '</div>'
                 + (('<details class="reason-more"><summary>Weitere Fehlergründe (' + str(len(tg[6:])) + ')</summary>'
                     + '<div class="reason-more-body"><input type="search" id="reason-search" placeholder="Grund suchen…" autocomplete="off" aria-label="Grund suchen">'
                     + '<div class="chips chips-secondary">' + secondary + '</div></div></details>') if secondary else '')
                 + '<div class="reason-selection" id="reason-selection" aria-live="polite" hidden></div></div>')
        g0 = garm_of(tmpl)
        lviews = loc_views(g0) or LOC_VIEWS
        lpick = ('<div class="lpick"><div class="lseg" id="lview">' + ''.join(['<button type="button" data-v="' + v[0] + '"' + (' class="on"' if v[0] == lviews[0][0] else '') + '>' + v[1] + '</button>' for v in lviews]) + '</div>')
        for v in lviews:
            lpick += '<div class="ldraw" data-v="' + v[0] + '"' + ('' if v[0] == lviews[0][0] else ' hidden') + '>' + loc_svg(g0, v[0], [], {}, True, 'int') + '</div>'
        lpick += ('<p class="lhint">Rechts/links immer vom Träger aus gesehen.</p>'
                  + '<button type="button" class="lzall" data-z="X-ALL" data-l="' + esc(loc_label('X-ALL')) + '">' + esc(loc_label('X-ALL')) + '</button>'
                  + '<div id="zsel" class="none"></div></div>')
        if not p or p.product_tmpl_id.id != tmpl.id:
            response = txt('Größe fehlt')
        else:
            edhtml = ''
            edjs = ''
            if ED:
                eback = QB + '&view=prod&tmpl=' + str(tmpl.id)
                ekind = QB + '&amp;tmpl=' + str(tmpl.id) + '&amp;defect=' + str(p.id) + '&amp;edit=' + str(ED.id) + (('&amp;pick=' + str(pick.id)) if pick else '')
                eopts = ''.join(['<option value="' + str(v.id) + '"' + (' selected' if v.id == p.id else '') + '>' + esc(size_of(v)) + '</option>' for v in sorted(tmpl.product_variant_ids, key=lambda v: (sz_parts(size_of(v))[0], size_rank(size_of(v))))])
                eims = Att.search([('res_model', '=', 'quality.alert'), ('res_id', '=', ED.id), ('mimetype', '=like', 'image%')], order='id')
                edefs = []
                for it in locs_of(ED)[1]:
                    edefs.append([clean_reason(it[0]), tl(clean_reason(it[0])), it[1]])
                if not edefs:
                    for tn in tags_of(ED):
                        edefs.append([clean_reason(tn), tl(clean_reason(tn)), []])
                ed_d = str(ED.description or '') if 'description' in AF else ''
                enote = ed_d.replace(MISSING_HTML, '').split('<p>Prüfer:')[0].split('<p>Größe:')[0].split('<p>Nachgetragen')[0].replace(NOTEMARK + ' kein Defekt – wird gebucht, beobachten', '').replace('<p>', '').replace('</p>', ' ').strip()
                enote = enote.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#x27;', "'").replace('&#39;', "'")
                edhtml = ('<div class="card edbox"><h2>Bearbeiten: ' + esc(ED.name) + '</h2>'
                          + '<div class="edrow"><a class="' + ('' if NT else 'on') + '" href="' + ekind + '">Defekt</a><a class="' + ('on' if NT else '') + '" href="' + ekind + '&amp;kind=note">Hinweis – kein Defekt</a></div>'
                          + '<label class="qlbl" style="font-size:14px;margin-top:10px">Größe</label><select id="esize" style="width:100%">' + eopts + '</select>'
                          + (('<label class="qlbl" style="font-size:14px;margin-top:10px">Vorhandene Fotos – zum Entfernen anhaken</label><div class="ephs">'
                              + ''.join(['<label class="eph"><img src="' + QB + '&amp;img=' + str(i.id) + '" alt=""><span><input type="checkbox" class="ephx" value="' + str(i.id) + '"> entfernen</span></label>' for i in eims]) + '</div>') if eims else '')
                          + ('' if NT else '<label class="erp"><input type="checkbox" id="ereprint"> Danach Etikett neu drucken <small>(optional – nur wenn ein neues Etikett gebraucht wird)</small></label>')
                          + '<p class="mut" style="font-size:13px;margin:8px 0 0">Die Fehler unten sind schon eingetragen: mit ✕ entfernen, neue wie gewohnt hinzufügen (Schritt 1–3). Neue Fotos gehören zu einem neuen Fehler oder über „Foto hinzufügen“ auf der Karte.</p></div>')
                edjs = ',EDIT=' + jsq(str(ED.id)) + ',EDEFS=[' + ','.join(['[' + jsq(e0[0]) + ',' + jsq(e0[1]) + ',[' + ','.join([jsq(z) for z in e0[2]]) + ']]' for e0 in edefs]) + '] ' + ',ENOTE=' + jsq(enote) + ',BACK=' + jsq(eback)
            html = (head(('Hinweis' if NT else 'Defekt') + (' bearbeiten' if ED else ' erfassen')) + topbar(('Hinweis' if NT else 'Defekt') + (' bearbeiten' if ED else ' erfassen'), ctx_q(tmpl, pick)) + '<div class="wrap">' + edhtml
                    + ('<div class="swb" style="display:block">Hinweis – kein Defekt: das Teil ist in Ordnung und wird gebucht. Kein Etikett.</div>' if NT else '')
                    + '<div class="ctx"><span><b>' + esc(tmpl.name) + '</b><br>' + (esc(pick_label(pick)) if pick else 'ohne Lieferung') + '</span><span style="font:800 24px Arial;color:var(--fg);text-align:right;white-space:nowrap">' + (('<small style="display:block;font:700 13px Arial;color:var(--mut)">' + esc(sz_parts(size_of(p))[0]) + '</small>') if sz_parts(size_of(p))[0] else '') + 'Gr. ' + esc(sz_parts(size_of(p))[1]) + '</span></div>'
                    + '<ol class="qsteps"><li id="st1" class="cur"><b>1</b> Grund</li><li id="st2"><b>2</b> Wo?</li><li id="st3"><b>3</b> Foto' + (' <small>(optional)</small>' if NT else '') + '</li></ol>'
                    + '<div class="card reason-card" id="qcard"><h2 id="defno">' + ('Hinweis' if NT else 'Fehler') + ' 1</h2>'
                    + '<div class="qsec" id="rbox"><div class="qlbl"><b>1</b> ' + ('Was ist auffällig?' if NT else 'Grund') + ' <small>– antippen</small></div>' + rchips
                    + '<select id="reason" class="qsel qsel2" aria-label="Weitere Gründe">' + ropts + '</select>'
                    + '<input type="text" id="newtag" class="qnew" placeholder="Grund eingeben, z. B. Kordel fehlt" hidden></div>'
                    + '<div class="qsec qwrap"><div class="qlbl"><b>2</b> Wo ist ' + ('es' if NT else 'der Fehler') + '?' + (' <small>(optional)</small>' if NT else '') + '</div>'
                    + '<div id="wo" class="qlock">' + lpick + '</div><button type="button" class="qcover" id="wo-lock">Zuerst Grund wählen ①</button></div>'
                    + '<div class="qsec qwrap"><div class="qlbl"><b>3</b> Foto vom Fehler' + (' <small>(optional)</small>' if NT else '') + '</div>'
                    + '<div id="fotos" class="qlock"><div id="fthumbs" class="qths"></div><div id="fstate"></div>'
                    + '<input type="file" id="fcam" accept="image/*" capture="environment" style="display:none">'
                    + '<button type="button" class="big blk" id="fbtn">Foto aufnehmen</button>'
                    + '</div>'
                    + '<button type="button" class="qcover" id="ph-lock">Zuerst Ort auf der Zeichnung wählen ②</button></div>'
                    + '<button type="button" class="smallaction" id="addf" disabled>+ Weiteren ' + ('Hinweis' if NT else 'Fehler') + ' an dieser Jacke</button></div>'
                    + '<div class="card" id="flist-card" hidden><h2>' + ('Hinweise' if NT else 'Fehler') + ' an dieser Jacke (<span id="fn">0</span>)</h2><div id="flist"></div></div>'
                    + '<details class="card note-optional"><summary>Notiz (optional)</summary><textarea id="note" rows="2" placeholder="z. B. Stelle, Größe des Lochs"></textarea></details>'
                    + '<div class="savebar"><p class="err" id="err"></p><p id="savehint"></p><div class="qsrow"><a class="qback" href="' + ctx_q(tmpl, pick) + '">← Zurück</a><button class="big blk ' + ('' if ED else ('icon-note' if NT else ('icon-printer' if PRINT_ENABLED else 'icon-download'))) + '" id="save">' + ('✓ Änderungen speichern' if ED else ('Hinweis speichern' if NT else ('Etikett drucken' if PRINT_ENABLED else 'Etikett-PDF erstellen'))) + '</button></div></div>'
                    + '<p class="mut" style="font-size:13px;text-align:center">' + ('Nur die Änderungen werden gespeichert – es wird kein Etikett gedruckt (außer oben angehakt).' if ED else '') + ('' if ED else ('Hinweis wird mit Fotos gespeichert. Kein Etikett.' if NT else ('Beim Drucken werden alle Fehler und Fotos gespeichert und ein Etikett gedruckt.' if PRINT_ENABLED else 'Beim Klick werden alle Fehler und Fotos gespeichert und das Etikett-PDF erstellt.'))) + '</p>'
                    + '<a class="noprint" href="' + ctx_q(tmpl, pick) + '" style="display:block;text-align:center;margin-top:8px">Abbrechen</a></div>'
                    + '<script>var CSRF=' + jsq(request.csrf_token()) + ',KEY=' + jsq(KEY) + ',PID=' + jsq(str(p.id)) + ',PICK=' + jsq(str(pick.id) if pick else '')
                    + ',KIND=' + jsq('note' if NT else '') + ',GARM=' + jsq(g0) + ',SVT=' + jsq('Änderungen speichern' if ED else ('Hinweis speichern' if NT else ('Etikett drucken' if PRINT_ENABLED else 'Etikett-PDF erstellen'))) + edjs + ';' + DEFECT_JS + '</script></body></html>')
            response = resp(html)

    else:
        vs = sorted(tmpl.product_variant_ids, key=lambda v: (size_rank(size_of(v)), size_of(v)))
        cs = checks_for(tmpl, pick, False)
        per = {}
        for c in cs:
            if chk_size(c) != '?':
                per[c.product_id.id] = per.get(c.product_id.id, 0) + 1
        SP = str(params.get('sp') or '')
        SP = SP if SP.isdigit() and int(SP) in tmpl.product_variant_ids.ids else ''
        groups = []
        gmap = {}
        for v in sorted(vs, key=lambda v: (sz_parts(size_of(v))[0].lower(), size_rank(size_of(v)))):
            cz = sz_parts(size_of(v))
            if cz[0] not in gmap:
                gmap[cz[0]] = []
                groups.append(cz[0])
            gmap[cz[0]].append('<button type="button" data-p="' + str(v.id) + '" data-s="' + esc(size_of(v)) + '" data-c="' + esc(cz[0]) + '" data-z="' + esc(cz[1]) + '">' + esc(cz[1]) + '<small>' + str(per.get(v.id, 0)) + '</small></button>')
        szb = ''.join([(('<div class="szh">' + esc(g) + '</div>') if g else '') + '<div class="sz">' + ''.join(gmap[g]) + '</div>' for g in groups])
        okn = len([c for c in cs if c.quality_state == 'pass'])
        np = params.get('np') == '1' and not pick
        LOCK = bool(pick) and not pick_open(pick) and not GUEST
        rdom = [('product_id.product_tmpl_id', '=', tmpl.id), ('quality_state', 'in', ['pass', 'fail'])] + AUTO
        rdom.append(('picking_id', '=', pick.id) if pick and 'picking_id' in CF else ('create_date', '>=', datetime.datetime.combine(today, datetime.time(0, 0)) - datetime.timedelta(hours=2)))
        rcs = QC.search(rdom, order='create_date desc, id desc', limit=80)
        ral = {}
        if 'check_id' in AF and rcs:
            for al in QA.search([('check_id', 'in', rcs.ids)]):
                ral[al.check_id.id] = al
        grp = []
        for c in rcs:
            al = ral.get(c.id)
            kind = ('N' if is_note(al) else 'D') if al else ('O' if c.quality_state == 'pass' else 'D')
            g = grp[-1] if grp else None
            if g and kind == 'O' and g[0] == 'O' and g[2] == c.product_id.id and abs((g[3] - c.create_date).total_seconds()) <= 3:
                g[1] += 1
                g[3] = c.create_date
            else:
                if len(grp) >= 6:
                    break
                grp.append([kind, 1, c.product_id.id, c.create_date, al, c.create_date, chk_size(c)])
        lrows = ''
        for g in grp[:6]:
            t = loc(g[5]).strftime('%H:%M')
            if g[0] == 'O':
                lrows += '<div class="le leo"><span>' + t + '</span><b>' + (str(g[1]) + '× ' if g[1] > 1 else '') + 'OK</b><span>Gr. ' + esc(g[6]) + '</span></div>'
            else:
                al = g[4]
                lrows += ('<div class="le ' + ('len' if g[0] == 'N' else 'led') + '"><span>' + t + '</span><b>' + ('! Hinweis' if g[0] == 'N' else 'Defekt') + '</b><span>Gr. ' + esc(g[6]) + (' · ' + esc(', '.join(tags_of(al))) if al else '')
                          + (' · <a href="' + QB + '&amp;view=prod&amp;tmpl=' + str(tmpl.id) + ('&amp;pick=' + str(pick.id) if pick else '') + '">' + esc(al.name) + ' →</a>' if al else '') + ((' · » ' + esc(loc_text(al))) if al and loc_text(al) else '') + ((' · ' + ('' if al and loc_codes(al) else '<strong class="photo-missing">Foto fehlt</strong> · ') + '<a href="' + QB + '&amp;photo_for=' + str(al.id) + '&amp;stage=late&amp;back=scan">Foto hinzufügen</a>') if al and not photo_count(al) else '') + '</span></div>')
        recv = {}
        if pick:
            for mv in pick.move_ids:
                if mv.product_id.product_tmpl_id.id == tmpl.id and mv.state != 'cancel':
                    qv = mv.quantity if mv.state == 'done' else (mv.product_uom_qty or mv.quantity)
                    recv[mv.product_id.id] = recv.get(mv.product_id.id, 0) + int(round(qv or 0))
        cntall = {}
        for c in cs:
            if chk_size(c) != '?':
                cntall[c.product_id.id] = cntall.get(c.product_id.id, 0) + 1
        jrecv = '{' + ','.join(['"' + str(k) + '":' + str(v) for k, v in recv.items()]) + '}'
        jcnt = '{' + ','.join(['"' + str(k) + '":' + str(v) for k, v in cntall.items()]) + '}'
        jsz = '{' + ','.join(['"' + str(v.id) + '":"' + esc(size_of(v)).replace('"', '') + '"' for v in vs]) + '}'
        jord = '[' + ','.join(['"' + str(v.id) + '"' for v in vs if v.id in recv]) + ']'
        html = (head('Prüfen') + topbar('Prüfen', QB) + '<div class="flash" id="fl"></div><div class="wrap">'
                + '<div class="swb" id="swb" style="display:none"></div>'
                + ('<div class="swb" style="display:block;background:#fde8e8;color:#991b1b">Lieferung ' + esc(pick.name) + ' ist schon gebucht – QC nur für offene Wareneingänge. Bitte andere Lieferung wählen.</div>' if LOCK else '')
                + ('' if pick else '<div class="swb" style="display:flex;justify-content:space-between;align-items:center;gap:8px;background:#fde8e8;color:#991b1b"><span>Keine Lieferung gewählt – Zahlen gelten für alle Lieferungen.</span><a class="btn" style="white-space:nowrap" href="' + QB + '&amp;pt=' + str(tmpl.id) + '">Lieferung wählen →</a></div>')
                + WHO_CARD
                + '<div class="ctx"><span><b>' + esc(tmpl.name) + '</b><br>' + (('Lieferung: ' + esc(pick_label(pick))) if pick else ('<span style="color:var(--red)">' + ('ohne Lieferung – kein offener Wareneingang gefunden' if np else 'ohne Lieferung') + '</span>'))
                + ' · <a href="' + QB + '&amp;pt=' + str(tmpl.id) + '">Lieferung ändern</a></span>'
                + '<a href="' + QB + '&amp;view=prod&amp;tmpl=' + str(tmpl.id) + ('&amp;pick=' + str(pick.id) if pick else '') + '" style="font-size:13px;white-space:nowrap">Details →</a></div>'
                + '<div class="pmsg" id="pmsg" style="display:none"><span id="pmt"></span><button id="pmr" style="display:none">Nochmal drucken</button></div>'
                + '<div class="card"><div class="scan" id="scan"><div class="sp" id="sph">Etikett scannen</div><div class="bc" id="bc"></div><div class="bs" id="bs">–</div><div class="bn" id="bn"></div><div class="bprog" id="bprog"></div><div class="bp">' + (esc(pick_short(pick)) if pick else '') + '</div></div>'
                + '<div class="mrow"><label><input type="checkbox" id="auto"> Auto-OK: jeder Scan = 1× OK</label><a href="#" id="mtog">Größe manuell wählen (Etikett nicht lesbar)</a></div>'
                + '<div id="manual"><div id="sz">' + szb + '</div><div class="mcode"><input type="text" id="mcode" placeholder="Barcode eintippen" inputmode="text"><button type="button" class="btn" id="mgo">OK</button></div></div>'
                + '<div class="qty" id="qty"><span>Anzahl</span><button type="button" class="on" data-q="1">1</button><button type="button" data-q="2">2</button><button type="button" data-q="3">3</button><button type="button" data-q="5">5</button><button type="button" data-q="10">10</button><button type="button" data-q="x">…</button></div>'
                + '<button class="big ok" id="ok" disabled>Kein Defekt</button><button class="big bad" id="bad" disabled>Defekt</button>'
                + '<button class="big hnt" id="hnt" disabled>Hinweis – kein Defekt</button>'
                + '<div class="cnt"><div><b id="c0">' + str(len(cs)) + '</b><small>Geprüft</small></div><div class="g"><b id="c1">' + str(okn) + '</b><small>OK</small></div><div class="d"><b id="c2">' + str(len(cs) - okn) + '</b><small>Defekt</small></div></div>'
                + '<div class="last"><span id="last"></span><span><button id="undo" style="display:none">Rückgängig</button><button id="lwd" style="display:none">Letzter war Defekt</button></span></div></div>'
                + '<div class="card"><h2>Letzte Eingaben</h2><div id="lel">' + (lrows or '<p class="mut" id="le0">Noch nichts gespeichert.</p>') + '</div></div>'
                + ('<div class="card"><h2>Fortschritt dieser Lieferung (geprüft / geliefert)</h2><div class="prg" id="prog"></div></div>' if recv else '')
                + '<div id="qov" class="qov" hidden><div class="qovb"><div class="qsp"></div><b id="qovt"></b><span id="qovs"></span><small>Nächstes Teil scannen</small></div></div>'
                + '</div>'
                + '<script>var CSRF="' + request.csrf_token() + '",KEY="' + KEY + '",PICK="' + (str(pick.id) if pick else '') + '",TM="' + str(tmpl.id) + '",SP="' + SP + '",TN="' + esc(tmpl.name).replace('"', '') + '",pid="",sz="",lastId="",qty=1,mode="",lastPid="",lastN=0,lastOk=false,lastCode="",lastScanT=0;'
                + 'var RECV=' + jrecv + ',CNT=' + jcnt + ',SZN=' + jsz + ',ORD=' + jord + ',LOCK=' + ('true' if LOCK else 'false') + ';'
                + SCANJS
                + 'function ls(k,v){try{if(v===undefined)return localStorage.getItem(k)||"";localStorage.setItem(k,v)}catch(e){return ""}}'
                + WHO_JS + 'if(PICK)remPick(TM,PICK);'
                + 'function over(p,n){return RECV[p]!==undefined&&(CNT[p]||0)+n>RECV[p]}'
                + 'function renderProg(){var g=document.getElementById("prog");if(g){var h="";ORD.forEach(function(p){var c=CNT[p]||0,r=RECV[p]||0,cl=c>r?"ov":(c===r&&r>0?"dn":""),w=r?Math.min(100,Math.round(100*c/r)):0;'
                + 'h+="<b>"+SZN[p]+"</b><div class=\\"br "+cl+"\\"><i style=\\"width:"+w+"%\\"></i></div><span class=\\"n "+cl+"\\">"+c+" / "+r+"</span>"});g.innerHTML=h}'
                + 'var bp=document.getElementById("bprog");if(pid&&RECV[pid]!==undefined){var c2=CNT[pid]||0;bp.textContent="Gr. "+sz+": "+c2+" / "+RECV[pid]+" geprüft"+(c2>RECV[pid]?" – mehr geprüft als geliefert":(c2===RECV[pid]?" – alle geprüft":""));bp.className="bprog"+(c2>=RECV[pid]?" ov":"")}else bp.textContent=""}'
                + 'var AU=document.getElementById("auto");AU.checked=ls("iq_qc_auto")==="1";AU.onchange=function(){ls("iq_qc_auto",AU.checked?"1":"0")};'
                + 'var MT=document.getElementById("mtog"),MT0=MT.textContent;MT.onclick=function(e){e.preventDefault();var o=document.getElementById("manual").classList.toggle("open");MT.textContent=o?"Größenauswahl ausblenden":MT0};'
                + 'function show(){var sc=document.getElementById("scan");document.getElementById("bs").textContent=pid?(szz||sz):"–";document.getElementById("bc").textContent=pid?szc:"";document.getElementById("bn").textContent=pid?TN:"";'
                + 'document.getElementById("sph").textContent=pid?(mode==="scan"?"Gescannt":"Größe gewählt"):(lastId?"Nächstes Etikett scannen":"Etikett scannen");sc.classList.toggle("hit",!!pid);'
                + 'document.getElementById("ok").disabled=!pid||LOCK;document.getElementById("bad").disabled=!pid||LOCK;document.getElementById("hnt").disabled=!pid||LOCK;okt();renderProg()}'
                + 'var szz="",szc="";function sel(b,m){document.querySelectorAll("#sz button").forEach(function(x){x.classList.remove("on")});if(b){b.classList.add("on");pid=b.dataset.p;sz=b.dataset.s;szz=b.dataset.z||sz;szc=b.dataset.c||""}else{pid="";sz="";szz="";szc=""}mode=m||"";show()}'
                + 'function okt(){document.getElementById("ok").textContent=pid?"Kein Defekt · Gr. "+sz+(qty>1?" · "+qty+" Stück":""):"Kein Defekt"}'
                + 'function setq(n,b){qty=n;document.querySelectorAll("#qty button").forEach(function(x){x.classList.remove("on")});b.classList.add("on");okt()}'
                + 'document.querySelectorAll("#qty button").forEach(function(b){b.onclick=function(){var n=b.dataset.q;if(n==="x"){n=parseInt(prompt("Wie viele OK-Teile in dieser Größe?","20"),10);if(!(n>0&&n<=200))return;b.textContent=n}setq(+n,b)}});'
                + 'document.querySelectorAll("#sz button").forEach(function(b){b.onclick=function(){sel(b,"man")}});'
                + 'function flash(t,c){var f=document.getElementById("fl");f.textContent=t;f.style.background=c;f.classList.add("show");setTimeout(function(){f.classList.remove("show")},900)}'
                + 'function upd(a){document.getElementById("c0").textContent=a[0];document.getElementById("c1").textContent=a[1];document.getElementById("c2").textContent=a[2]}'
                + 'function post(d,cb){var fd=new FormData();fd.append("csrf_token",CSRF);fd.append("key",KEY);fd.append("pick",PICK);for(var k in d)fd.append(k,d[k]);'
                + 'fetch(location.pathname,{method:"POST",body:fd,credentials:"same-origin"}).then(function(r){return r.text()}).then(function(t){var a=t.split("|");if(a[0]==="OK")cb(a);else{beep("err");flash(a[1]||"Fehler","#b91c1c")}})'
                + '.catch(function(){beep("err");flash("Keine Verbindung – nicht gespeichert","#b91c1c")})}'
                + 'function qov(st,t){var o=document.getElementById("qov");if(!o)return;clearTimeout(window.qovT);o.hidden=false;o.className="qov"+(st?" okd":"");document.getElementById("qovt").textContent=st?"✓ Gespeichert":"Speichert …";document.getElementById("qovs").textContent=st?t:"";window.qovT=setTimeout(function(){o.hidden=true},st?1200:6000)}'
                + 'var busy=false;function doOK(auto){if(busy||!pid)return;if(needName())return;var n=qty,s0=sz,m0=mode,p0=pid;'
                + 'if(over(p0,n)){if(auto){beep("err");flash("Mehr als geliefert – bitte OK selbst tippen","#b91c1c");return}if(!confirm("Gr. "+s0+": "+((CNT[p0]||0)+n)+" > "+RECV[p0]+" – mehr geprüft als geliefert. Trotzdem speichern?"))return}'
                + 'busy=true;qov(0,"");post({act:"ok",pid:p0,qty:n,who:W.value.trim()},function(a){busy=false;qov(1,(n>1?n+"× ":"")+"Kein Defekt · Gr. "+s0);lastId=a[1];upd(a.slice(2));CNT[p0]=(CNT[p0]||0)+n;lastPid=p0;lastN=n;lastOk=true;document.getElementById("lwd").style.display="inline-block";addLe("<span>"+new Date().toTimeString().slice(0,5)+"</span><b>"+(n>1?n+"× ":"")+"OK</b><span>Gr. "+s0+" · gespeichert</span>");'
                + 'flash(""+(n>1?n+"× ":"")+"OK gespeichert · Gr. "+s0,"#15803d");var b=document.querySelector("#sz button.on small");if(b)b.textContent=(+b.textContent+n);'
                + 'document.getElementById("last").textContent="Zuletzt: "+(n>1?n+"× ":"")+"OK · Gr. "+s0+" · "+new Date().toLocaleTimeString().slice(0,5);document.getElementById("undo").style.display="inline-block";'
                + 'if(n>1){var q1=document.querySelector("#qty button");var xb=document.querySelector("#qty button[data-q=x]");xb.textContent="…";setq(1,q1)}sel(null,"")});setTimeout(function(){busy=false},1500)}'
                + 'document.getElementById("ok").onclick=function(){doOK(false)};'
                + 'document.getElementById("hnt").onclick=function(){if(needName()||LOCK)return;if(pid)location.href="?key="+KEY+"&tmpl="+TM+"&defect="+pid+"&kind=note"+(PICK?"&pick="+PICK:"")};'
                + 'function addLe(h){var l=document.getElementById("lel"),z=document.getElementById("le0");if(z)z.remove();var d=document.createElement("div");d.className="le leo fresh";d.innerHTML=h;l.insertBefore(d,l.firstChild);while(l.children.length>6)l.removeChild(l.lastChild)}'
                + 'document.getElementById("bad").onclick=function(){if(needName()||LOCK)return;if(pid)location.href="?key="+KEY+"&tmpl="+TM+"&defect="+pid+(PICK?"&pick="+PICK:"")};'
                + 'function pickVar(id){var b=document.querySelector("#sz button[data-p=\'"+id+"\']");if(b)sel(b,"scan");return !!b}'
                + 'window.onScan=function(c){var sc=document.getElementById("scan");if(needName())return;var tn=Date.now();if(c===lastCode&&tn-lastScanT<3000){lastScanT=tn;beep("err");flash("Doppelt gescannt? Nicht gezählt","#b45309");return}lastCode=c;lastScanT=tn;scanPost(c,{pick:PICK,rpick:remPick(TM)},function(a){'
                + 'if(a[0]!=="OK"){beep("err");sel(null,"");document.getElementById("sph").innerHTML="<span style=color:#b91c1c>"+(a[1]||"Fehler")+"</span>";return}'
                + 'if(a[2]===TM&&(a[5]===PICK||(!a[5]&&a[7]!=="M"))){if(!pickVar(a[1])){beep("err");return}if(over(a[1],1)){beep("err");flash("Mehr als geliefert – bitte OK selbst tippen","#b91c1c");return}beep("ok");if(AU.checked)doOK(true);return}'
                + 'beep("sw");goScan(a,AU.checked)})};'
                + 'document.getElementById("mgo").onclick=function(){var v=document.getElementById("mcode").value.trim();if(v){window.onScan(v);document.getElementById("mcode").value=""}};'
                + 'document.getElementById("mcode").onkeydown=function(e){if(e.key==="Enter"){e.preventDefault();document.getElementById("mgo").click()}};'
                + 'try{var swn=sessionStorage.getItem("iq_qc_sw");if(swn&&SP){sessionStorage.removeItem("iq_qc_sw");var sw=document.getElementById("swb");sw.textContent="Gewechselt zu "+swn;sw.style.display="block";setTimeout(function(){sw.style.display="none"},5000);beep("sw")}}catch(e){}'
                + 'if(SP){pickVar(SP);try{if(sessionStorage.getItem("iq_qc_autook")){sessionStorage.removeItem("iq_qc_autook");doOK(true)}}catch(e){}}renderProg();if(!W.value.trim())W.classList.add("needname");'
                + 'try{var L=sessionStorage.getItem("iq_qc_last");if(L){var q=L.split("|");lastId=q[0];document.getElementById("last").textContent="Zuletzt: "+q[1];document.getElementById("undo").style.display="inline-block";sessionStorage.removeItem("iq_qc_last");show()}'
                + 'var DONE=sessionStorage.getItem("iq_qc_done");if(DONE){sessionStorage.removeItem("iq_qc_done");var db=document.getElementById("pmsg");db.style.display="flex";db.className="pmsg ok";document.getElementById("pmt").textContent=DONE+" gespeichert";setTimeout(function(){db.style.display="none"},14000)}'
                + 'var M=sessionStorage.getItem("iq_qc_msg");if(M){sessionStorage.removeItem("iq_qc_msg");var m=M.split("|"),box=document.getElementById("pmsg"),tx=document.getElementById("pmt"),rb=document.getElementById("pmr");box.style.display="flex";'
                + 'if(m[2]==="N"){box.className="pmsg nt";tx.textContent="Hinweis "+m[1]+" gespeichert (kein Defekt, wird gebucht)";setTimeout(function(){box.style.display="none"},12000)}'
                + 'else if(m[2]==="1"){box.className="pmsg ok";tx.textContent="Defekt "+m[1]+" gespeichert · Etikett gedruckt";setTimeout(function(){box.style.display="none"},12000)}'
                + 'else{box.className="pmsg warn";tx.textContent="Defekt "+m[1]+" gespeichert – Etikett NICHT gedruckt ("+(m[3]||"Drucker")+")";rb.style.display="inline-block";'
                + 'rb.onclick=function(){rb.disabled=true;post({act:"print",aid:m[0]},function(a){box.className="pmsg ok";tx.textContent=m[1]+" · Etikett gedruckt";rb.style.display="none"});setTimeout(function(){rb.disabled=false},3000)}}}}catch(e){}'
                + 'document.getElementById("lwd").onclick=function(){if(!lastId||!lastOk||!lastPid)return;var one=String(lastId).split(",").pop();post({act:"undo",cid:one},function(a){CNT[lastPid]=Math.max(0,(CNT[lastPid]||0)-1);'
                + 'location.href="?key="+KEY+"&tmpl="+TM+"&defect="+lastPid+(PICK?"&pick="+PICK:"")})};'
                + 'document.getElementById("undo").onclick=function(){if(!lastId||!confirm("Letzte Eingabe löschen?"))return;post({act:"undo",cid:lastId},function(a){upd(a.slice(2));lastId="";if(lastOk&&lastPid){CNT[lastPid]=Math.max(0,(CNT[lastPid]||0)-lastN)}lastOk=false;document.getElementById("lwd").style.display="none";renderProg();'
                + 'document.getElementById("last").textContent="Rückgängig gemacht";document.getElementById("undo").style.display="none";flash("Gelöscht","#6b7280")})};</script></body></html>')
        response = resp(html)

# ------------------------------------------------------------------ start: choose product (+ delivery)
else:
    q = (params.get('q') or '').strip()
    pt = str(params.get('pt') or '')
    if pt.isdigit():
        tmpl = Tmpl.browse(int(pt)).exists()
        d60 = datetime.datetime.combine(today - datetime.timedelta(days=90), datetime.time(0, 0))
        pks = open_picks(tmpl)
        spq = ('&amp;sp=' + str(params.get('sp'))) if str(params.get('sp') or '').isdigit() else ''
        rows = ''.join(['<a href="' + QB + '&amp;tmpl=' + str(tmpl.id) + '&amp;pick=' + str(pk.id) + spq + '"><span><b>' + esc(pk.origin or pk.name) + '</b> · ' + esc(pk.partner_id.name or '') + '<br><small>Wareneingang ' + esc(pk.name) + '</small></span><small>' + ((pk.date_done or pk.scheduled_date).strftime('%d.%m.%Y') if (pk.date_done or pk.scheduled_date) else '')
                        + '<br>' + ('gebucht' if pk.state == 'done' else 'offen') + '</small></a>' for pk in pks])
        html = (head('Lieferung wählen') + topbar('Lieferung wählen', QB) + '<div class="wrap"><div class="ctx"><b>' + esc(tmpl.name) + '</b></div>'
                + (('<div class="swb">Bitte Lieferung für dieses Produkt wählen</div>') if spq else '')
                + '<div class="card"><h2>2 · Zu welcher Lieferung?</h2><div class="list">' + (rows or '<p class="mut">Kein offener Wareneingang für dieses Produkt. QC ist nur für offene (noch nicht gebuchte) Wareneingänge.</p>')
                + '<a href="' + QB + '&amp;tmpl=' + str(tmpl.id) + spq + '&amp;nopick=1"><span>Ohne Lieferung prüfen</span><small>→</small></a></div></div></div></body></html>')
        response = resp(html)
    else:
        if len(q) >= 2:
            ts = Tmpl.search(['|', ('name', 'ilike', q), ('default_code', 'ilike', q), ('type', 'in', ['consu', 'product'])], limit=30)
            hd = 'Suchergebnis'
        else:
            recent = QC.search([('quality_state', 'in', ['pass', 'fail'])] + AUTO, order='create_date desc', limit=400)
            seen = []
            for c in recent:
                t = c.product_id.product_tmpl_id
                if t not in seen:
                    seen.append(t)
            ts = seen[:12]
            hd = 'Zuletzt geprüft'
        rows = ''.join(['<a href="' + QB + '&amp;pt=' + str(t.id) + '"><span><b>' + esc(t.name) + '</b><br><small>' + str(len(t.product_variant_ids)) + ' Größen/Varianten</small></span><small>→</small></a>' for t in ts])
        html = (head('Qualitätskontrolle') + topbar('Qualitätskontrolle', '') + '<div class="wrap">'
                + WHO_CARD
                + '<a class="arrbtn" href="' + CAL_URL + '&amp;arr=1">' + ICB + 'Wareneingang melden<small>Ware angekommen? Lieferschein + Menge erfassen</small></a>'
                + '<div class="card"><h2>1 · Produkt wählen</h2><form method="get" action=""><input type="hidden" name="key" value="' + KEY + '">'
                + '<input type="search" name="q" value="' + esc(q) + '" placeholder="Produkt suchen, z. B. Wintermantel"></form></div>'
                + '<div class="scan" id="scan"><div class="sp">Etikett scannen</div><div class="bp">oder Produkt oben suchen</div></div>'
                + '<div class="card"><h2>' + hd + '</h2><div class="list">' + (rows or '<p class="mut">Nichts gefunden. Bitte oben suchen.</p>') + '</div></div></div>'
                + '<script>var CSRF="' + request.csrf_token() + '",KEY="' + KEY + '";' + SCANJS + WHO_JS
                + 'window.onScan=function(c){if(needName())return;scanPost(c,{},function(a){if(a[0]!=="OK"){beep("err");var s=document.getElementById("scan");s.innerHTML="<div class=sp style=color:#b91c1c>"+(a[1]||"Fehler")+"</div>";return}'
                + 'beep("ok");goScan(a,false)})};</script></body></html>')
        response = resp(html)'''

SA = env['ir.actions.server'].sudo()
CP = env['ir.config_parameter'].sudo()
if not CP.get_param('iq.delivery_calendar_key') or not CP.get_param('iq.delivery_calendar_password'):
    log('IQ QC page NOT installed: the Wareneingang / warehouse calendar is not installed in this database yet (system parameters iq.delivery_calendar_key / iq.delivery_calendar_password missing). Install it first.')
elif 'quality.check' not in env or 'quality.alert' not in env:
    log('IQ QC page NOT installed: Quality app (quality.check / quality.alert) is not installed in this database.')
else:
    qm = env['ir.model'].sudo().search([('model', '=', 'quality.check')], limit=1)
    gfield = 'group_ids' if 'group_ids' in SA._fields else 'groups_id'
    vals = {'name': 'IQ QC page', 'model_id': qm.id, 'state': 'code', 'code': PAGE,
            'website_published': True, 'website_path': 'iq-qc',
            gfield: [(6, 0, [env.ref('base.group_public').id, env.ref('base.group_user').id, env.ref('base.group_portal').id])]}
    qa = SA.search([('name', '=', 'IQ QC page')], limit=1)
    if qa:
        qa.write(vals)
    else:
        qa = SA.create(vals)
    # label size for PDF printers (62 x 30 mm): paper format + hidden report entry
    PF = env['report.paperformat'].sudo()
    pff = PF.fields_get()
    pvals = {'name': 'IQ QC Label 62x30', 'format': 'custom', 'page_width': 30, 'page_height': 62, 'orientation': 'Landscape',
             'margin_top': 0, 'margin_bottom': 0, 'margin_left': 0, 'margin_right': 0, 'header_line': False,
             'header_spacing': 0, 'dpi': 96, 'disable_shrinking': True}
    pvals = dict([(k, v) for k, v in pvals.items() if k in pff])
    pf = PF.search([('name', '=', 'IQ QC Label 62x30')], limit=1)
    if pf:
        pf.write(pvals)
    else:
        pf = PF.create(pvals)
    RA = env['ir.actions.report'].sudo()
    rvals = {'name': 'IQ QC Label 62x30', 'model': 'quality.alert', 'report_type': 'qweb-pdf',
             'report_name': 'iq_qc.label_62x30', 'paperformat_id': pf.id}
    rep = RA.search([('report_name', '=', 'iq_qc.label_62x30')], limit=1)
    if rep:
        rep.write(rvals)
    else:
        rep = RA.create(rvals)
    # Additional variable-length PDFs, same original report pattern; no additional business fields.
    # Odoo requires an actual report.paperformat for EACH page length (CSS @page alone is not enough).
    for label_mm in [26, 30, 34, 38, 42, 46, 50, 54, 58, 62, 66, 70, 74, 78, 82, 86, 90, 94, 98, 110, 130, 160, 200, 240, 280, 320, 400, 500, 650, 800, 1000]:
        dyn_name = 'IQ QC Label 62x' + str(label_mm)
        dyn_format = PF.search([('name', '=', dyn_name)], limit=1)
        dyn_vals = dict(pvals)
        # v9 proven trick: physical 62 mm width is page_height=62 with Landscape orientation.
        dyn_vals.update({'name': dyn_name, 'page_width': label_mm, 'page_height': 62, 'orientation': 'Landscape'})
        if dyn_format:
            dyn_format.write(dyn_vals)
        else:
            dyn_format = PF.create(dyn_vals)
        dyn_report_name = 'iq_qc.label_62x' + str(label_mm)
        dyn_report = RA.search([('report_name', '=', dyn_report_name)], limit=1)
        dyn_report_vals = {'name': dyn_name, 'model': 'quality.alert', 'report_type': 'qweb-pdf',
                           'report_name': dyn_report_name, 'paperformat_id': dyn_format.id}
        if dyn_report:
            dyn_report.write(dyn_report_vals)
        else:
            RA.create(dyn_report_vals)
    CP.set_param('iq.qc_label_output_mode', LABEL_OUTPUT_MODE)
    # Printer-specific options are deliberately separate from PDF page length.
    # Do not overwrite administrator adjustments when the installer is rerun.
    if not CP.get_param('iq.qc_brother_paper'):
        CP.set_param('iq.qc_brother_paper', '62mm')
    if not CP.get_param('iq.qc_brother_rotation'):
        CP.set_param('iq.qc_brother_rotation', '90')
    pinfo = 'Direct Print app not installed – PDF download available'
    if 'printnode.printer' in env:
        Pr = env['printnode.printer'].sudo()
        if PRINTER_NAME:
            # Match the exact name from Odoo Direct Print (PrintNode normally uses underscores).
            # Keep a space/underscore fallback for different macOS/CUPS naming conventions.
            selected = Pr.search([('name', '=', PRINTER_NAME)], limit=1)
            if not selected:
                selected = Pr.search([('name', '=', PRINTER_NAME.replace(' ', '_'))], limit=1)
            if not selected:
                selected = Pr.search([('name', '=', PRINTER_NAME.replace('_', ' '))], limit=1)
            if not selected:
                selected = Pr.search([('name', 'ilike', PRINTER_NAME)], limit=1)
            if selected:
                CP.set_param('iq.qc_printnode_printer_id', str(selected.id))
                # Brother RAW consumes 62mm DK-22251 raster bytes, never PDF or Zebra ZPL.
                if 'BROTHER' in (selected.name or '').upper():
                    CP.set_param('iq.qc_label_mode', 'brother-raw')
                log('IQ QC printer selected: ' + (selected.name or '') + ' | Odoo printer ID ' + str(selected.id))
            else:
                log('IQ QC printer NOT changed: cannot find printer named ' + PRINTER_NAME + ' in Direct Print; existing printer kept.')
        cur = CP.get_param('iq.qc_printnode_printer_id') or ''
        prn = Pr.browse(int(cur)).exists() if cur.isdigit() else Pr.browse([])
        mode = CP.get_param('iq.qc_label_mode') or ('zpl' if [w for w in ['ZPL', 'ZD4', 'ZD2', 'ZEBRA', 'ZDESIGNER'] if w in (prn.name or '').upper()] else 'pdf')
        pinfo = ('printer: ' + (prn.name or '') + ' (id ' + str(prn.id) + ') | mode: ' + mode) if prn else 'NO printer selected – set system parameter iq.qc_printnode_printer_id'
    log('IQ QC page installed (v19.18e supplier check + packing + DK-44205) | link for the phones: /website/action/iq-qc?key=' + (CP.get_param('iq.delivery_calendar_key') or '?') + ' | ' + pinfo
        + ' | OUTPUT: ' + (CP.get_param('iq.qc_label_output_mode') or '')
        + ' | label format: ' + pf.name + ' (id ' + str(pf.id) + '), report id ' + str(rep.id))

# ---- menu "QC Dashboard" in the Goods Receipts app (same as qc_2026-11-16_menu_qc_dashboard.py)
UrlAct = env['ir.actions.act_url'].sudo()
Menu = env['ir.ui.menu'].sudo()

key = CP.get_param('iq.delivery_calendar_key') or ''
page = SA.search([('name', '=', 'IQ QC page')], limit=1)
cal_act = UrlAct.search([('name', 'in', ['Warehouse & team calendar', 'Lager- & Teamkalender'])], limit=1)
cal_menu = Menu.with_context(active_test=False).search([('action', '=', 'ir.actions.act_url,' + str(cal_act.id))], limit=1) if cal_act else Menu.browse([])
if not cal_menu:
    cal_menu = Menu.with_context(active_test=False).search([('name', 'in', ['Warehouse & team calendar', 'Lager- & Teamkalender', 'Upcoming deliveries', 'Kommende Lieferungen', 'Goods Receipt', 'Wareneingang'])], limit=1)
if not cal_menu:
    root = Menu.search([('parent_id', '=', False), ('name', 'in', ['Goods Receipts', 'Wareneingänge', 'Wareneingaenge'])], limit=1)
    cal_menu = Menu.search([('parent_id', '=', root.id)], order='sequence desc', limit=1) if root else Menu.browse([])

if not page:
    log('IQ QC menu NOT added: the QC page was not installed (see the line above).')
elif not cal_menu:
    log('IQ QC menu NOT added: the Goods Receipts app menu was not found.')
else:
    url = '/website/action/' + (page.website_path or str(page.id)) + '?key=' + key + '&view=dash'
    ua = UrlAct.search([('name', 'in', ['QC Dashboard', 'QC-Dashboard'])], limit=1)
    if ua:
        ua.write({'url': url, 'target': 'new'})
    else:
        ua = UrlAct.create({'name': 'QC Dashboard', 'url': url, 'target': 'new'})
    uref = 'ir.actions.act_url,' + str(ua.id)
    m = Menu.with_context(active_test=False).search([('action', '=', uref)], limit=1)
    vals = {'name': 'QC Dashboard', 'parent_id': cal_menu.parent_id.id, 'action': uref, 'sequence': (cal_menu.sequence or 12) + 1, 'active': True}
    if m:
        m.write(vals)
    else:
        m = Menu.create(vals)
    m.update_field_translations('name', {'en_US': 'QC Dashboard', 'de_DE': 'QC-Dashboard'})
    log('IQ QC menu added: "QC Dashboard" in ' + (cal_menu.parent_id.complete_name or cal_menu.parent_id.name or '') + ' -> ' + url)

# ---- button "QC: OK-Mengen übernehmen" on receipts (Action menu) – only for Inventory Administrators for now
BTN_CODE = r'''# IQ QC: OK-Mengen übernehmen (button on the receipt, Action menu)
# Sets the receipt quantity per size = OK count from the QC page (incl. "Hinweis – kein Defekt").
# Defective and not-yet-checked pieces (all sizes of a checked product) get 0. Products not QC-checked on this receipt at all stay unchanged.
# Does NOT validate. Writes a summary into the chatter.
UNK = '[Größe unbekannt]'
QC = env['quality.check'].sudo()
QCF = QC.fields_get(['point_id', 'note', 'picking_id'])
for pk in records:
    if pk.picking_type_code != 'incoming':
        raise UserError('Nur für Wareneingänge.')
    if pk.state in ('done', 'cancel'):
        raise UserError('Wareneingang ' + pk.name + ' ist schon gebucht oder storniert – nichts geändert.')
    dom = [('picking_id', '=', pk.id), ('quality_state', 'in', ['pass', 'fail'])]
    if 'point_id' in QCF:
        dom.append(('point_id', '=', False))
    ok = {}
    bad = {}
    unk = 0
    tmpls = []
    for c in QC.search(dom):
        if c.product_id.product_tmpl_id.id not in tmpls:
            tmpls.append(c.product_id.product_tmpl_id.id)
        if 'note' in QCF and UNK in str(c.note or ''):
            unk += 1
        elif c.quality_state == 'pass':
            ok[c.product_id.id] = ok.get(c.product_id.id, 0) + 1
        else:
            bad[c.product_id.id] = bad.get(c.product_id.id, 0) + 1
    rows = []
    for mv in pk.move_ids:
        pid = mv.product_id.id
        if mv.state in ('done', 'cancel') or mv.product_id.product_tmpl_id.id not in tmpls:
            continue
        dem = mv.product_uom_qty or 0
        o = ok.get(pid, 0)
        b = bad.get(pid, 0)
        q = min(o, dem)
        mv.quantity = q
        sz = ', '.join(mv.product_id.product_template_attribute_value_ids.mapped('name')) or (mv.product_id.default_code or mv.product_id.display_name)
        rows.append([sz, int(dem), o, b, int(max(0, dem - o - b)), int(q), (o > dem)])
    if not rows:
        raise UserError('Für ' + pk.name + ' gibt es keine QC-Prüfungen – nichts geändert.')
    tr = ''.join(['<tr><td>' + r[0] + '</td><td style="text-align:right">' + str(r[1]) + '</td><td style="text-align:right">' + str(r[2]) + '</td><td style="text-align:right">' + str(r[3]) + '</td><td style="text-align:right">' + str(r[4]) + '</td><td style="text-align:right"><b>' + str(r[5]) + '</b>' + (' – Warnung: mehr OK als geliefert' if r[6] else '') + '</td></tr>' for r in rows])
    body = ('<p><b>QC: OK-Mengen übernommen</b> von ' + env.user.name + ' – noch NICHT gebucht. Bitte prüfen und dann Validieren.</p>'
            + '<table border="1" cellpadding="3" style="border-collapse:collapse"><tr><th>Größe</th><th>Geliefert</th><th>OK</th><th>Defekt</th><th>Nicht geprüft</th><th>Menge gesetzt</th></tr>' + tr + '</table>'
            + '<p>Defekte und nicht geprüfte Teile = 0 (werden nicht gebucht). Beim Validieren: „Rückstand erstellen“ solange die Reklamation offen ist, sonst „Kein Rückstand“.</p>'
            + ('<p>' + str(unk) + ' Prüfungen ohne Größe wurden nicht gezählt.</p>' if unk else ''))
    env['mail.message'].sudo().create({'model': 'stock.picking', 'res_id': pk.id, 'body': body, 'message_type': 'comment',
                                       'subtype_id': env.ref('mail.mt_note').id, 'author_id': env.user.partner_id.id})
action = {'type': 'ir.actions.client', 'tag': 'display_notification',
          'params': {'title': 'QC-Mengen übernommen', 'message': 'OK-Mengen gesetzt – noch nicht gebucht. Bitte prüfen und Validieren.', 'type': 'success', 'sticky': False,
                     'next': {'type': 'ir.actions.client', 'tag': 'soft_reload'}}}
'''
try:
    IM = env['ir.model'].sudo()
    pmodel = IM.search([('model', '=', 'stock.picking')], limit=1)
    saf = SA.fields_get(['group_ids', 'groups_id', 'binding_model_id', 'binding_view_types'])
    bvals = {'name': 'QC: OK-Mengen übernehmen', 'model_id': pmodel.id, 'state': 'code', 'code': BTN_CODE}
    if 'binding_model_id' in saf:
        bvals['binding_model_id'] = pmodel.id
    if 'binding_view_types' in saf:
        bvals['binding_view_types'] = 'form,list'
    grp = env.ref('stock.group_stock_manager', raise_if_not_found=False)
    gf = 'group_ids' if 'group_ids' in saf else ('groups_id' if 'groups_id' in saf else '')
    if grp and gf:
        bvals[gf] = [(6, 0, [grp.id])]
    ba = SA.search([('name', '=', 'QC: OK-Mengen übernehmen')], limit=1)
    if ba:
        ba.write(bvals)
    else:
        ba = SA.create(bvals)
    log('IQ QC button added: "QC: OK-Mengen übernehmen" on receipts (Action menu), id ' + str(ba.id) + ', only for group: ' + (grp.display_name if grp and gf else 'ALL USERS (group field not found)'))
except Exception as e:
    log('IQ QC button NOT added: ' + str(e))

# ---------------------------------------------------------------- one-time: own drawings from the CD tech packs (only if the product has no own drawing yet)
#   Wintermantel Damen (CD 167918), Winter Parka Unisex (CD 1610007), IQ Hundesportweste 4.0 Unisex (CD 167904 Mens Dog vest 3.0)
QC_DRAW_SEED = None  # PUBLIC COPY: supplier tech-pack drawings removed (the drawing step below is skipped and logged)
VEST_SEED = None  # PUBLIC COPY: removed

try:
    AttS = env['ir.attachment'].sudo()
    PT = env['product.template'].sudo().with_context(active_test=False)
    seeded = []
    jobs = []
    for skey, scode in [('wmd', 'IQD-EKL-WMD'), ('wpu', 'IQD-EKL-WPU')]:
        jobs.append([QC_DRAW_SEED[skey], env['product.product'].sudo().with_context(active_test=False).search([('default_code', '=like', scode + '%')]).mapped('product_tmpl_id')])
    jobs.append([VEST_SEED, PT.search([('name', 'ilike', 'Hundesportweste 4.0')])])
    for job in jobs:
        sd = job[0]
        for st in job[1]:
            if AttS.search_count([('res_model', '=', 'product.template'), ('res_id', '=', st.id), ('name', '=', 'iq_qc_draw.txt')]):
                continue
            for fname in sd['files']:
                AttS.create({'name': fname, 'datas': sd['files'][fname][1], 'mimetype': sd['files'][fname][0], 'res_model': 'product.template', 'res_id': st.id})
            AttS.create({'name': 'iq_qc_draw.txt', 'raw': sd['cfg'].encode('utf-8'), 'mimetype': 'text/plain', 'res_model': 'product.template', 'res_id': st.id})
            seeded.append(st.name)
    log('IQ QC drawings: ' + (('set up for ' + ', '.join(seeded)) if seeded else 'nothing new (already set up)'))
except Exception as e:
    log('IQ QC drawings NOT set up: ' + str(e))
