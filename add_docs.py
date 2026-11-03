"""Adds the 03.11.2026 page (carrier fallback for ticket deliveries) to index.html and daily/log.js.
Usage from the repo root: python3 add_docs.py   (safe to run twice)"""
import os, sys
root = sys.argv[1] if len(sys.argv) > 1 else "."
LINK = "odoo/carrier-fallback-ticket-deliveries-2026-11-03/"
TITLE = "Exchange deliveries from tickets without carrier – fallback rule"
TEXT = "Helpdesk Replace creates the delivery directly, so the order carrier is not propagated; since Auto Set Carrier (7) was archived nothing filled it. New rule: empty carrier on Delivery Orders → Germany DHL, others GLS. Cause, code, safety checks, tests, rollout."
ok = True
p = os.path.join(root, "index.html"); s = open(p, encoding="utf-8").read()
if f'href="{LINK}"' in s:
    print("index.html: card already present - unchanged")
else:
    i = s.find('<a class="card" href="odoo/dhl-go-live-2026-10-27/">')
    if i == -1: i = s.find('<a class="card"')
    if i == -1:
        print("index.html: no card found - NOT changed"); ok = False
    else:
        card = f'''<a class="card" href="{LINK}">
      <b>{TITLE}</b>
      <span>{TEXT}</span>
      <em>03.11.2026 · Staging</em>
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
    date: "2026-11-03",
    area: "Odoo · Shipping",
    title: "{TITLE}",
    summary: "WH1/OUT/07574 (ticket #00889) had no carrier: ticket Replace creates the delivery directly, no Propagation of carrier, rules 8/45 only on quotations, Auto Set Carrier archived since 27.10. New staging rule 'IQ – Delivery: carrier when empty' (DE → DHL Parcel DE, else GLS Germany, never overwrites). Edit trigger only on Carrier/Contact/Operation Type/Status.",
    status: "Staging",
    link: "{LINK}"
  }},
'''
        open(p, "w", encoding="utf-8").write(head + entry + s[end:]); print("daily/log.js: entry added")
sys.exit(0 if ok else 1)
