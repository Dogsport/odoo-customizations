# IQ Goods Receipts – public delivery calendar: page password + absences for the shown month
# Updates ONLY the page code of the server action "IQ Public delivery calendar".
# Run once: Scheduled Action (Model: Contact, Active = off) -> Save -> Run Manually.
# Password: Settings -> Technical -> System Parameters -> iq.delivery_calendar_password
# Changing the password signs out all devices.

PASSWORD = '<PASSWORD-REMOVED>'

PAGE = r'''
P = env['ir.config_parameter'].sudo()
KEY = P.get_param('iq.delivery_calendar_key') or ''
PW = P.get_param('iq.delivery_calendar_password') or ''
params = request.params if request else {}
de = params.get('lang', 'de') != 'en'
h = 2166136261
for ch in (PW + '|' + KEY):
    h = ((h ^ ord(ch)) * 16777619) % 4294967296
h2 = 2166136261
for ch in (KEY + '#' + PW):
    h2 = ((h2 ^ ord(ch)) * 16777619) % 4294967296
TOKEN = '%08x%08x' % (h, h2)
authed = bool(PW) and request.httprequest.cookies.get('iq_cal') == TOKEN
base = '?key=' + KEY + ('' if de else '&lang=en')
login_err = False
if not KEY or params.get('key') != KEY or not PW:
    response = request.make_response('Not found', headers=[('Content-Type', 'text/plain; charset=utf-8')], status=404)
elif params.get('logout'):
    response = request.make_response('', headers=[('Location', base)], status=303)
    response.delete_cookie('iq_cal')
elif request.httprequest.method == 'POST' and params.get('pw') == PW:
    response = request.make_response('', headers=[('Location', base + ('&m=' + params.get('m') if params.get('m') else ''))], status=303)
    response.set_cookie('iq_cal', TOKEN, max_age=2592000, httponly=True, secure=True, samesite='Lax')
elif not authed:
    login_err = request.httprequest.method == 'POST'
    T1 = 'Anstehende Lieferungen' if de else 'Upcoming deliveries'
    T2 = 'Bitte Passwort eingeben' if de else 'Please enter the password'
    T3 = 'Anmelden' if de else 'Sign in'
    T4 = 'Falsches Passwort.' if de else 'Wrong password.'
    lp = ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">'
          '<title>IQ Dogsport</title><style>body{margin:0;background:#f6f7f9;font:15px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;color:#1f2328;display:flex;min-height:100vh;align-items:center;justify-content:center}'
          'form{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:28px;width:320px;max-width:calc(100vw - 32px)}h1{font-size:19px;margin:0 0 4px}p{margin:0 0 16px;color:#6b7280}'
          'input{width:100%;box-sizing:border-box;padding:10px;border:1px solid #d1d5db;border-radius:6px;font-size:15px;margin-bottom:10px}button{width:100%;padding:10px;border:0;border-radius:6px;background:#111;color:#fff;font-size:15px;font-weight:600}.e{color:#dc2626;margin:8px 0 0}</style></head><body>'
          '<form method="post" action=""><h1>' + T1 + '</h1><p>IQ Dogsport · ' + T2 + '</p>'
          '<input type="hidden" name="csrf_token" value="' + request.csrf_token() + '"><input type="hidden" name="key" value="' + KEY + '">'
          + ('' if de else '<input type="hidden" name="lang" value="en">')
          + ('<input type="hidden" name="m" value="' + params.get('m') + '">' if params.get('m') else '')
          + '<input type="password" name="pw" autofocus autocomplete="current-password"><button>' + T3 + '</button>'
          + ('<p class="e">' + T4 + '</p>' if login_err else '') + '</form></body></html>')
    response = request.make_response(lp, headers=[('Content-Type', 'text/html; charset=utf-8'), ('X-Robots-Tag', 'noindex'), ('Cache-Control', 'no-store')])
else:
    staff = True
    cq = ''
    L = {
        'title': 'Anstehende Lieferungen' if de else 'Upcoming deliveries',
        'sub': 'Was kommt wann ins Lager' if de else 'What arrives in the warehouse, and when',
        'today': 'Heute' if de else 'Today',
        'month_list': 'Lieferungen in diesem Monat' if de else 'Deliveries this month',
        'by_sup': 'Stück pro Lieferant' if de else 'Pieces per supplier',
        'total': 'Gesamt' if de else 'Total',
        'deliv': 'Lieferungen' if de else 'deliveries',
        'deliv1': 'Lieferung' if de else 'delivery',
        'pcs': 'Stk.' if de else 'pcs.',
        'overdue': 'Überfällig (noch nicht angekommen)' if de else 'Overdue (not arrived yet)',
        'none': 'Keine Lieferungen in diesem Monat.' if de else 'No deliveries this month.',
        'po': 'Bestellung' if de else 'PO',
        'plan': 'Geplant' if de else 'Planned',
        'upd': 'Stand' if de else 'Updated',
        'abs': 'Abwesend im ' if de else 'Absent in ',
        'noabs': 'In diesem Monat ist niemand abwesend.' if de else 'Nobody is absent this month.',
        'logout': 'Abmelden' if de else 'Sign out',
        'code': 'Mitarbeiter-Code' if de else 'Staff code',
        'show': 'Abwesenheiten anzeigen' if de else 'Show absences',
        'wrong': 'Code falsch.' if de else 'Wrong code.',
        'away': 'abwesend' if de else 'absent',
    }
    MONTHS = (['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'] if de else
              ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    DAYS = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'] if de else ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    esc = lambda s: (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    num = lambda q: '{:,.0f}'.format(q or 0).replace(',', '.' if de else ',')
    today = datetime.date.today()
    y = today.year
    m = today.month
    mp = params.get('m') or ''
    if len(mp) == 7 and mp[:4].isdigit() and mp[5:].isdigit() and 1 <= int(mp[5:]) <= 12:
        y = int(mp[:4])
        m = int(mp[5:])
    first = datetime.date(y, m, 1)
    nxt = datetime.date(y + (1 if m == 12 else 0), 1 if m == 12 else m + 1, 1)
    prv = datetime.date(y - (1 if m == 1 else 0), 12 if m == 1 else m - 1, 1)
    last = nxt - datetime.timedelta(days=1)
    gstart = first - datetime.timedelta(days=first.weekday())
    gend = last + datetime.timedelta(days=6 - last.weekday())

    # ---------- collect events
    ev = []
    Line = env['x_wareneingang_line'].sudo()
    WE = env['x_wareneingang'].sudo()
    for l in Line.search([('x_done', '=', False), ('x_date', '!=', False)], order='x_date asc'):
        ev.append({'d': l.x_date, 'sup': l.x_partner_id.commercial_partner_id.name or '', 'prod': l.x_product_text or '',
                   'ship': l.x_shipment or '', 'qty': l.x_qty or 0, 'ref': l.x_supplier_ref or '', 'kind': 'plan'})
    picks = env['stock.picking'].sudo().search([('picking_type_code', '=', 'incoming'), ('purchase_id', '!=', False),
                                                ('state', 'not in', ['done', 'cancel', 'draft'])], order='scheduled_date asc')
    for p in picks:
        card = WE.search([('x_studio_purchase_order', '=', p.purchase_id.id)], limit=1)
        if card and card.x_schedule_ids.filtered(lambda x: not x.x_done):
            continue
        moves = p.move_ids.filtered(lambda mv: mv.state != 'cancel')
        names = []
        for mv in moves:
            n = (mv.product_id.product_tmpl_id.name or '').split(' – ')[0]
            if n not in names:
                names.append(n)
        prod = names[0] if names else ''
        if len(names) > 1:
            prod += ' +' + str(len(names) - 1)
        ev.append({'d': p.scheduled_date.date() if p.scheduled_date else today, 'sup': p.partner_id.commercial_partner_id.name or '',
                   'prod': prod, 'ship': '', 'qty': sum(moves.mapped('product_uom_qty')), 'ref': p.purchase_id.name, 'kind': 'po'})

    ev = sorted(ev, key=lambda e: e['d'])
    COLORS = ['#2563eb', '#db2777', '#059669', '#d97706', '#7c3aed', '#0891b2', '#dc2626', '#65a30d']
    sups = []
    for e in ev:
        if e['sup'] not in sups:
            sups.append(e['sup'])
    col = lambda s: COLORS[sups.index(s) % len(COLORS)] if s in sups else '#6b7280'

    absn = []
    if staff:
        lo = gstart
        hi = gend
        for lv in env['hr.leave'].sudo().search([('state', '=', 'validate'), ('request_date_from', '<=', hi), ('request_date_to', '>=', lo)], order='request_date_from asc'):
            parts = (lv.employee_id.name or '').split()
            nm = parts[0] + (' ' + parts[-1][0] + '.' if len(parts) > 1 else '') if parts else ''
            absn.append({'n': nm, 'a': lv.request_date_from, 'b': lv.request_date_to or lv.request_date_from})

    def link(d):
        return '?key=' + KEY + '&amp;m=' + d.strftime('%Y-%m') + ('' if de else '&amp;lang=en') + cq

    # ---------- calendar grid
    g = ['<div class="grid">']
    for dn in DAYS:
        g.append('<div class="dh">' + dn + '</div>')
    d = gstart
    while d <= gend:
        cls = 'day' + (' out' if d.month != m else '') + (' today' if d == today else '')
        g.append('<div class="' + cls + '"><div class="dn">' + str(d.day) + '</div>')
        if d.weekday() < 5:
            for a in absn:
                if a['a'] <= d <= a['b']:
                    g.append('<div class="ab">' + esc(a['n']) + ' &middot; ' + L['away'] + '</div>')
        for e in [x for x in ev if x['d'] == d]:
            od = ' od' if d < today else ''
            g.append('<div class="ev' + od + '" style="border-left-color:' + col(e['sup']) + '" title="' + esc(e['sup'] + ' · ' + e['prod']) + '">'
                     + '<b>' + num(e['qty']) + '</b> ' + esc(e['prod']) + '<span>' + esc(e['sup']) + (' · ' + esc(e['ship']) if e['ship'] else '')
                     + (' · ' + esc(e['ref']) if e['ref'] else '') + '</span></div>')
        g.append('</div>')
        d = d + datetime.timedelta(days=1)
    g.append('</div>')

    # ---------- side panel
    mev = [x for x in ev if first <= x['d'] <= last]
    s = ['<aside>']
    cur = [a for a in absn if a['a'] <= last and a['b'] >= first]
    s.append('<div class="box grey"><h3>' + L['abs'] + MONTHS[m - 1] + '</h3>')
    if not cur:
        s.append('<p class="muted">' + L['noabs'] + '</p>')
    for a in cur:
        nowc = ' style="font-weight:700"' if a['a'] <= today <= a['b'] else ''
        s.append('<div class="row"' + nowc + '><span>' + esc(a['n']) + '</span><b>' + a['a'].strftime('%d.%m.') + (' &ndash; ' + a['b'].strftime('%d.%m.') if a['b'] != a['a'] else '') + '</b></div>')
    s.append('</div>')
    odl = [x for x in ev if x['d'] < today]
    if odl:
        s.append('<div class="box red"><h3>' + L['overdue'] + '</h3>')
        for e in odl:
            s.append('<div class="row"><span>' + e['d'].strftime('%d.%m.') + ' ' + esc(e['prod']) + '<small>' + esc(e['sup']) + '</small></span><b>' + num(e['qty']) + '</b></div>')
        s.append('</div>')
    s.append('<div class="box"><h3>' + L['month_list'] + '</h3>')
    if not mev:
        s.append('<p class="muted">' + L['none'] + '</p>')
    for e in mev:
        tag = L['po'] if e['kind'] == 'po' else L['plan']
        s.append('<div class="row"><span><i style="background:' + col(e['sup']) + '"></i>' + e['d'].strftime('%d.%m.') + ' ' + esc(e['prod'])
                 + '<small>' + esc(e['sup']) + (' · ' + esc(e['ship']) if e['ship'] else '') + ' · ' + tag + (' ' + esc(e['ref']) if e['ref'] else '') + '</small></span><b>' + num(e['qty']) + '</b></div>')
    s.append('</div>')
    if mev:
        tot = {}
        cnt = {}
        for e in mev:
            tot[e['sup']] = tot.get(e['sup'], 0) + e['qty']
            cnt[e['sup']] = cnt.get(e['sup'], 0) + 1
        s.append('<div class="box"><h3>' + L['by_sup'] + '</h3>')
        for k in sorted(tot, key=lambda k: -tot[k]):
            s.append('<div class="row"><span><i style="background:' + col(k) + '"></i>' + esc(k) + '<small>' + str(cnt[k]) + ' ' + (L['deliv1'] if cnt[k] == 1 else L['deliv']) + '</small></span><b>' + num(tot[k]) + '</b></div>')
        s.append('<div class="row total"><span>' + L['total'] + '<small>' + str(len(mev)) + ' ' + L['deliv'] + '</small></span><b>' + num(sum(tot.values())) + ' ' + L['pcs'] + '</b></div></div>')
    s.append('</aside>')

    langlink = (('?key=' + KEY + '&amp;m=' + first.strftime('%Y-%m') + '&amp;lang=en') if de else ('?key=' + KEY + '&amp;m=' + first.strftime('%Y-%m'))) + cq
    html = """<!doctype html><html lang=""" + '"' + ('de' if de else 'en') + '"' + """><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="refresh" content="600">
<title>""" + L['title'] + """ – IQ Dogsport</title><style>
:root{--bg:#f6f7f9;--card:#fff;--fg:#1f2328;--mut:#6b7280;--line:#e5e7eb;--acc:#714b67;--red:#dc2626}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}
header{display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;padding:14px 18px;background:var(--card);border-bottom:1px solid var(--line)}
h1{font-size:20px;margin:0}header p{margin:2px 0 0;color:var(--mut)}nav{display:flex;gap:6px;align-items:center}
nav a{padding:6px 12px;border:1px solid var(--line);border-radius:6px;text-decoration:none;color:var(--fg);background:#fff}nav b{font-size:17px;margin:0 8px;min-width:150px;text-align:center}
main{display:grid;grid-template-columns:1fr 340px;gap:16px;padding:16px}
.grid{display:grid;grid-template-columns:repeat(7,1fr);background:var(--line);gap:1px;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.dh{background:#f0f1f3;padding:6px;text-align:center;font-weight:600;font-size:12px;color:var(--mut)}
.day{background:var(--card);min-height:110px;padding:4px}.day.out{background:#fafafa}.day.out .dn{color:#c0c4cc}
.dn{font-weight:600;font-size:12px;margin-bottom:3px}.today .dn{background:var(--red);color:#fff;border-radius:50%;width:22px;height:22px;display:flex;align-items:center;justify-content:center}
.ev{border-left:4px solid;background:#f3f4f6;border-radius:4px;padding:3px 5px;margin-bottom:3px;font-size:12px}.ev span{display:block;color:var(--mut);font-size:11px}
.ev.od{background:#fee2e2}.ab{font-size:11px;color:#4b5563;background:#eef2ff;border-radius:4px;padding:1px 5px;margin-bottom:3px}.box.grey{background:#f8fafc}aside{display:flex;flex-direction:column;gap:12px}
.box{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px}.box h3{margin:0 0 8px;font-size:14px}.box.red{border-color:#fca5a5;background:#fef2f2}.box.red h3{color:var(--red)}
.row{display:flex;justify-content:space-between;gap:8px;padding:5px 0;border-top:1px solid var(--line)}.row:first-of-type{border-top:0}
.row span{min-width:0}.row small{display:block;color:var(--mut)}.row b{white-space:nowrap}.row i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px}
.row.total{border-top:2px solid var(--fg);font-weight:700}.muted{color:var(--mut)}footer{color:var(--mut);font-size:12px;padding:0 18px 16px}
@media(max-width:900px){main{grid-template-columns:1fr}.day{min-height:70px}.ev span{display:none}}
</style></head><body><header><div><h1>""" + L['title'] + """</h1><p>IQ Dogsport · """ + L['sub'] + """</p></div>
<nav><a href=""" + '"' + link(prv) + '"' + """>&larr;</a><b>""" + MONTHS[m - 1] + ' ' + str(y) + """</b><a href=""" + '"' + link(nxt) + '"' + """>&rarr;</a>
<a href=""" + '"' + link(today) + '"' + """>""" + L['today'] + """</a><a href=""" + '"' + langlink + '"' + """>""" + ('EN' if de else 'DE') + """</a></nav></header>
<main>""" + ''.join(g) + ''.join(s) + """</main><footer><a href="?key=""" + KEY + """&amp;logout=1" style="color:inherit;float:right">""" + L['logout'] + """</a>""" + L['upd'] + ': ' + datetime.datetime.now().strftime('%d.%m.%Y %H:%M') + """ UTC</footer></body></html>"""
    response = request.make_response(html, headers=[('Content-Type', 'text/html; charset=utf-8'), ('X-Robots-Tag', 'noindex'), ('Cache-Control', 'no-store')])'''

CP = env['ir.config_parameter'].sudo()
if not CP.get_param('iq.delivery_calendar_password'):
    CP.set_param('iq.delivery_calendar_password', PASSWORD)
sa = env['ir.actions.server'].sudo().search([('name', '=', 'IQ Public delivery calendar')], limit=1)
if not sa:
    raise UserError('IQ Public delivery calendar not found')
sa.write({'code': PAGE})
log('IQ public calendar: password protection on. Password: ' + CP.get_param('iq.delivery_calendar_password'))
