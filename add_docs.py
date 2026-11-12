"""Adds the 12.11.2026 page (DHL return label without outbound shipment) to index.html and daily/log.js,
and a short update note to the 29.10 return-label page. Usage from the repo root: python3 add_docs.py (safe to run twice)"""
import os, sys
root = sys.argv[1] if len(sys.argv) > 1 else "."
LINK = "odoo/dhl-return-label-without-outbound-2026-11-12/"
TITLE = "DHL return label for returns without outbound DHL shipment"
TEXT = "Returns from Helpdesk tickets (and old/GLS orders) had no label button and BrowseInfo refused the label. Button now shows on open incoming transfers with carrier; server action calls the DHL return API directly when no outbound DHL shipment exists. Live 12.11."
ok = True
p = os.path.join(root, "index.html"); s = open(p, encoding="utf-8").read()
if f'href="{LINK}"' in s:
    print("index.html: card already present - unchanged")
else:
    i = s.find('<a class="card"')
    if i == -1:
        print("index.html: no card found - NOT changed"); ok = False
    else:
        card = f'''<a class="card" href="{LINK}">
      <b>{TITLE}</b>
      <span>{TEXT}</span>
      <em>12.11.2026 · Live</em>
    </a>
    '''
        open(p, "w", encoding="utf-8").write(s[:i] + card + s[i:]); print("index.html: card added")
p = os.path.join(root, "daily", "log.js"); s = open(p, encoding="utf-8").read()
if LINK in s:
    print("daily/log.js: entry already present - unchanged")
else:
    end = s.rfind("];")
    if end == -1:
        print("daily/log.js: closing ]; not found - NOT changed"); ok = False
    else:
        head = s[:end].rstrip()
        if not head.endswith(","): head += ","
        entry = f'''
  {{
    date: "2026-11-12",
    area: "Odoo · Returns / DHL",
    title: "{TITLE}",
    summary: "WH1/RET/00701 (ticket #00996): no return_id -> button hidden, BrowseInfo check 'no validated outbound DHL shipment'. View: not is_return_picking -> not carrier_id. Server action 1777 v2: return = is_return_picking or Returns operation type; no outbound DHL -> env['dhl.request'].create_return_shipment directly. Tested: label 545935501591.",
    status: "Live",
    link: "{LINK}"
  }},
'''
        open(p, "w", encoding="utf-8").write(head + entry + s[end:]); print("daily/log.js: entry added")
p = os.path.join(root, "odoo", "dhl-return-label-email-2026-10-29", "index.html")
if os.path.exists(p):
    s = open(p, encoding="utf-8").read()
    if "dhl-return-label-without-outbound-2026-11-12" in s:
        print("29.10 page: note already present - unchanged")
    elif "<main>" in s:
        note = '<div class="warn" style="background:#fff5d6;border-left:4px solid #b7791f;padding:8px 12px;margin:10px 0"><strong>Update 12.11.2026:</strong> server action and button view changed (v2) – returns without outbound DHL shipment (e.g. from tickets) now get a label. See <a href="../dhl-return-label-without-outbound-2026-11-12/">DHL return label without outbound shipment</a>. Code files on this page are v2.</div>'
        open(p, "w", encoding="utf-8").write(s.replace("<main>", "<main>" + note, 1)); print("29.10 page: update note added")
    else:
        print("29.10 page: <main> not found - NOT changed")
else:
    print("29.10 page not found (odoo/dhl-return-label-email-2026-10-29/) - push the 29.10 docs first; note skipped")
sys.exit(0 if ok else 1)
