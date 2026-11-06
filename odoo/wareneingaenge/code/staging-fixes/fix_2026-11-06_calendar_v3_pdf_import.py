# IQ Goods Receipts – update 06.11.2026
# 1) Calendar page: new IQ design (logo, summary tiles, phone list view), password + month absences kept
# 2) Menu "Public calendar" renamed to "Lager- & Teamkalender" / "Warehouse & team calendar"
# 3) Import delivery overview: PDF delivery notes (e.g. Holfelder) -> calendar entry on the EXISTING PO card, PDF attached
# Run once: Scheduled Action (Model: Contact, Active = off) -> Save -> Run Manually -> reload.
# Changes only: page code, menu/action names, code of "IQ Lieferübersicht verarbeiten". No new fields.

PAGE = r'''P = env['ir.config_parameter'].sudo()
KEY = P.get_param('iq.delivery_calendar_key') or ''
PW = P.get_param('iq.delivery_calendar_password') or ''
params = request.params if request else {}
de = params.get('lang', 'de') != 'en'
LOGO = 'https://iq-dogsport.de/cdn/shop/files/iq-dogogsport-logo-sw-White.png?v=1761656363&width=240'
h = 2166136261
for ch in (PW + '|' + KEY):
    h = ((h ^ ord(ch)) * 16777619) % 4294967296
h2 = 2166136261
for ch in (KEY + '#' + PW):
    h2 = ((h2 ^ ord(ch)) * 16777619) % 4294967296
TOKEN = '%08x%08x' % (h, h2)
authed = bool(PW) and request.httprequest.cookies.get('iq_cal') == TOKEN
base = '?key=' + KEY + ('' if de else '&lang=en')
TITLE = 'Lager- &amp; Teamkalender' if de else 'Warehouse &amp; team calendar'
CSS = """
:root{--bg:#f4f4f2;--card:#fff;--fg:#151515;--mut:#6b7280;--line:#e5e5e2;--red:#a51d1b;--soft:#fdecea}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}
a{color:inherit}
.top{background:#151515;color:#fff;border-bottom:4px solid var(--red)}
.top .in{max-width:1400px;margin:0 auto;padding:14px 18px;display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:space-between}
.brand{display:flex;align-items:center;gap:14px}.brand img{height:38px;width:auto;display:block}
.brand h1{font:800 20px/1.1 Arial,sans-serif;margin:0;letter-spacing:.2px}.brand p{margin:2px 0 0;color:#bdbdbd;font-size:12.5px}
nav{display:flex;gap:6px;align-items:center;flex-wrap:wrap}
nav a{padding:7px 12px;border:1px solid #3a3a3a;border-radius:6px;text-decoration:none;color:#fff;background:#222}
nav a:hover{border-color:#fff}nav b{font-size:16px;margin:0 6px;min-width:140px;text-align:center}
wrap,.wrap{display:block;max-width:1400px;margin:0 auto;padding:16px 18px}
.kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-bottom:14px}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 14px}
.kpi small{display:block;color:var(--mut);font:700 11px Arial;letter-spacing:1.2px;text-transform:uppercase}
.kpi b{display:block;font:800 22px/1.2 Arial;margin-top:4px}.kpi span{color:var(--mut);font-size:12.5px}
.kpi.red{border-color:#f3b4b0;background:var(--soft)}.kpi.red b{color:var(--red)}
main{display:grid;grid-template-columns:1fr 330px;gap:16px}
.grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr)) repeat(2,minmax(0,.55fr));background:var(--line);gap:1px;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.dh{background:#ecece9;padding:7px;text-align:center;font:700 11px Arial;letter-spacing:1px;text-transform:uppercase;color:var(--mut)}
.day{background:var(--card);min-height:112px;padding:5px}.day.we{background:#fafaf8}.day.out{background:#f7f7f5}.day.out .dn{color:#c4c4c0}
.dn{font:700 12px Arial;margin-bottom:4px;display:inline-block;min-width:22px;height:22px;line-height:22px;text-align:center}
.today{box-shadow:inset 0 0 0 2px var(--red)}.today .dn{background:var(--red);color:#fff;border-radius:50%}
.ev{border-left:4px solid;background:#f4f4f2;border-radius:4px;padding:4px 6px;margin-bottom:4px;font-size:12px}
.ev b{font-size:13px}.ev span{display:block;color:var(--mut);font-size:11px}.ev.od{background:var(--soft)}
.ab{display:flex;align-items:center;gap:5px;font-size:11.5px;color:#374151;margin-bottom:3px}
.av{display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:50%;color:#fff;font:700 9px Arial;flex:none}
aside{display:flex;flex-direction:column;gap:12px}
.box{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 14px}
.box h3{margin:0 0 8px;font:800 12px Arial;letter-spacing:1.2px;text-transform:uppercase}
.box.red{border-color:#f3b4b0;background:var(--soft)}.box.red h3{color:var(--red)}
.row{display:flex;justify-content:space-between;align-items:flex-start;gap:8px;padding:6px 0;border-top:1px solid var(--line)}.row:first-of-type{border-top:0}
.row span{min-width:0}.row small{display:block;color:var(--mut)}.row b{white-space:nowrap}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px}
.row.total{border-top:2px solid var(--fg);font-weight:700}.mut{color:var(--mut)}.now{font-weight:700}
.tag{display:inline-block;font:700 10px Arial;letter-spacing:.8px;text-transform:uppercase;background:var(--red);color:#fff;border-radius:3px;padding:1px 5px;margin-left:6px;vertical-align:middle}
.agenda{display:none}
footer{max-width:1400px;margin:0 auto;padding:0 18px 20px;color:var(--mut);font-size:12px;display:flex;justify-content:space-between}
@media(max-width:980px){main{grid-template-columns:1fr}.kpis{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:700px){.grid{display:none}.agenda{display:block}.brand img{height:30px}.brand h1{font-size:17px}nav b{min-width:0}}
.agenda .d{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin-bottom:8px}
.agenda .d h4{margin:0 0 6px;font:800 13px Arial}.agenda .d.today{box-shadow:inset 0 0 0 2px var(--red)}
"""

def page_head(t):
    return ('<!doctype html><html lang="' + ('de' if de else 'en') + '"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<meta name="robots" content="noindex"><title>' + t + ' – IQ Dogsport</title><style>' + CSS + '</style>')

if not KEY or params.get('key') != KEY or not PW:
    response = request.make_response('Not found', headers=[('Content-Type', 'text/plain; charset=utf-8')], status=404)
elif params.get('logout'):
    response = request.make_response('', headers=[('Location', base)], status=303)
    response.delete_cookie('iq_cal')
elif request.httprequest.method == 'POST' and params.get('pw') == PW:
    response = request.make_response('', headers=[('Location', base + ('&m=' + params.get('m') if params.get('m') else ''))], status=303)
    response.set_cookie('iq_cal', TOKEN, max_age=2592000, httponly=True, secure=True, samesite='Lax')
elif not authed:
    err = request.httprequest.method == 'POST'
    lp = (page_head(TITLE) + '<style>.lg{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:16px}'
          '.lg form{background:#fff;border:1px solid var(--line);border-radius:10px;width:340px;max-width:100%;overflow:hidden}'
          '.lg .hd{background:#151515;border-bottom:4px solid var(--red);padding:18px;text-align:center}.lg .hd img{height:44px}'
          '.lg .bd{padding:22px}.lg h2{margin:0 0 4px;font:800 18px Arial}.lg p{margin:0 0 14px;color:var(--mut)}'
          '.lg input{width:100%;padding:11px;border:1px solid #d1d5db;border-radius:6px;font-size:15px;margin-bottom:10px}'
          '.lg button{width:100%;padding:11px;border:0;border-radius:6px;background:var(--red);color:#fff;font:700 15px Arial;cursor:pointer}'
          '.lg .e{color:var(--red);margin:10px 0 0;font-weight:700}</style></head><body><div class="lg"><form method="post" action="">'
          '<div class="hd"><img src="' + LOGO + '" alt="IQ Dogsport"></div><div class="bd"><h2>' + TITLE + '</h2>'
          '<p>' + ('Nur für das IQ Dogsport Team. Bitte Passwort eingeben.' if de else 'IQ Dogsport team only. Please enter the password.') + '</p>'
          '<input type="hidden" name="csrf_token" value="' + request.csrf_token() + '"><input type="hidden" name="key" value="' + KEY + '">'
          + ('' if de else '<input type="hidden" name="lang" value="en">')
          + ('<input type="hidden" name="m" value="' + params.get('m') + '">' if params.get('m') else '')
          + '<input type="password" name="pw" placeholder="' + ('Passwort' if de else 'Password') + '" autofocus autocomplete="current-password">'
          + '<button>' + ('Anmelden' if de else 'Sign in') + '</button>'
          + ('<p class="e">' + ('Falsches Passwort.' if de else 'Wrong password.') + '</p>' if err else '') + '</div></form></div></body></html>')
    response = request.make_response(lp, headers=[('Content-Type', 'text/html; charset=utf-8'), ('X-Robots-Tag', 'noindex'), ('Cache-Control', 'no-store')])
else:
    L = {
        'sub': 'Lieferungen ins Lager und Abwesenheiten im Team' if de else 'Deliveries to the warehouse and team absences',
        'today': 'Heute' if de else 'Today', 'total': 'Gesamt' if de else 'Total',
        'deliv': 'Lieferungen' if de else 'deliveries', 'deliv1': 'Lieferung' if de else 'delivery', 'pcs': 'Stk.' if de else 'pcs.',
        'k_today': 'Heute erwartet' if de else 'Expected today', 'k_month': 'Diesen Monat' if de else 'This month',
        'k_od': 'Überfällig' if de else 'Overdue', 'k_abs': 'Heute abwesend' if de else 'Absent today',
        'nobody': 'niemand' if de else 'nobody', 'none_today': 'keine' if de else 'none',
        'overdue': 'Überfällig – noch nicht angekommen' if de else 'Overdue – not arrived yet',
        'month_list': 'Lieferungen im ' if de else 'Deliveries in ', 'by_sup': 'Stück pro Lieferant' if de else 'Pieces per supplier',
        'abs': 'Abwesend im ' if de else 'Absent in ', 'noabs': 'Niemand abwesend.' if de else 'Nobody absent.',
        'nodel': 'Keine Lieferungen.' if de else 'No deliveries.', 'po': 'Bestellung' if de else 'PO', 'plan': 'Geplant' if de else 'Planned',
        'away': 'abwesend' if de else 'absent', 'upd': 'Stand' if de else 'Updated', 'logout': 'Abmelden' if de else 'Sign out',
        'now': 'jetzt' if de else 'now',
    }
    MONTHS = (['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'] if de else
              ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    DAYS = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'] if de else ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    LDAYS = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag'] if de else ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
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
    people = []
    for lv in env['hr.leave'].sudo().search([('state', '=', 'validate'), ('request_date_from', '<=', max(gend, today)), ('request_date_to', '>=', min(gstart, today))], order='request_date_from asc'):
        parts = (lv.employee_id.name or '').split()
        nm = parts[0] + (' ' + parts[-1][0] + '.' if len(parts) > 1 else '') if parts else ''
        ini = (parts[0][0] + (parts[-1][0] if len(parts) > 1 else '')).upper() if parts else '?'
        if nm not in people:
            people.append(nm)
        absn.append({'n': nm, 'i': ini, 'a': lv.request_date_from, 'b': lv.request_date_to or lv.request_date_from})
    PCOL = ['#475569', '#7c3aed', '#0f766e', '#b45309', '#be185d', '#1d4ed8', '#4d7c0f', '#9f1239']
    pcol = lambda n: PCOL[people.index(n) % len(PCOL)] if n in people else '#475569'
    av = lambda a: '<i class="av" style="background:' + pcol(a['n']) + '">' + esc(a['i']) + '</i>'

    def link(d):
        return '?key=' + KEY + '&amp;m=' + d.strftime('%Y-%m') + ('' if de else '&amp;lang=en')

    def evhtml(e, d):
        od = ' od' if d < today else ''
        return ('<div class="ev' + od + '" style="border-left-color:' + col(e['sup']) + '" title="' + esc(e['sup'] + ' · ' + e['prod']) + '">'
                + '<b>' + num(e['qty']) + '</b> ' + esc(e['prod']) + '<span>' + esc(e['sup']) + (' · ' + esc(e['ship']) if e['ship'] else '')
                + (' · ' + esc(e['ref']) if e['ref'] else '') + '</span></div>')

    def abhtml(d):
        out = ''
        if d.weekday() < 5:
            for a in absn:
                if a['a'] <= d <= a['b']:
                    out += '<div class="ab">' + av(a) + esc(a['n']) + '</div>'
        return out

    # KPIs
    tday = [x for x in ev if x['d'] == today]
    mev = [x for x in ev if first <= x['d'] <= last]
    odl = [x for x in ev if x['d'] < today]
    absnow = [a for a in absn if a['a'] <= today <= a['b'] and today.weekday() < 5]
    k = ['<div class="kpis">',
         '<div class="kpi"><small>' + L['k_today'] + '</small><b>' + (num(sum(x['qty'] for x in tday)) + ' ' + L['pcs'] if tday else L['none_today']) + '</b><span>' + str(len(tday)) + ' ' + (L['deliv1'] if len(tday) == 1 else L['deliv']) + '</span></div>',
         '<div class="kpi"><small>' + L['k_month'] + ' · ' + MONTHS[m - 1] + '</small><b>' + num(sum(x['qty'] for x in mev)) + ' ' + L['pcs'] + '</b><span>' + str(len(mev)) + ' ' + (L['deliv1'] if len(mev) == 1 else L['deliv']) + '</span></div>',
         '<div class="kpi' + (' red' if odl else '') + '"><small>' + L['k_od'] + '</small><b>' + str(len(odl)) + '</b><span>' + num(sum(x['qty'] for x in odl)) + ' ' + L['pcs'] + '</span></div>',
         '<div class="kpi"><small>' + L['k_abs'] + '</small><b>' + str(len(absnow)) + '</b><span>' + (', '.join([esc(a['n']) for a in absnow]) or L['nobody']) + '</span></div>',
         '</div>']

    # grid
    g = ['<div class="grid">']
    for dn in DAYS:
        g.append('<div class="dh">' + dn + '</div>')
    d = gstart
    while d <= gend:
        cls = 'day' + (' we' if d.weekday() >= 5 else '') + (' out' if d.month != m else '') + (' today' if d == today else '')
        g.append('<div class="' + cls + '"><div class="dn">' + str(d.day) + '</div>' + abhtml(d))
        for e in [x for x in ev if x['d'] == d]:
            g.append(evhtml(e, d))
        g.append('</div>')
        d = d + datetime.timedelta(days=1)
    g.append('</div>')

    # agenda (phones)
    ag = ['<div class="agenda">']
    d = first
    anyday = False
    while d <= last:
        evs = [x for x in ev if x['d'] == d]
        abs_ = abhtml(d)
        if evs or abs_ or d == today:
            anyday = True
            ag.append('<div class="d' + (' today' if d == today else '') + '"><h4>' + LDAYS[d.weekday()] + ', ' + d.strftime('%d.%m.') + (' <span class="tag">' + L['today'] + '</span>' if d == today else '') + '</h4>'
                      + abs_ + ''.join([evhtml(e, d) for e in evs]) + ('' if (evs or abs_) else '<span class="mut">' + L['nodel'] + '</span>') + '</div>')
        d = d + datetime.timedelta(days=1)
    if not anyday:
        ag.append('<p class="mut">' + L['nodel'] + '</p>')
    ag.append('</div>')

    # side
    s = ['<aside>']
    cur = [a for a in absn if a['a'] <= last and a['b'] >= first]
    s.append('<div class="box"><h3>' + L['abs'] + MONTHS[m - 1] + '</h3>')
    if not cur:
        s.append('<p class="mut" style="margin:0">' + L['noabs'] + '</p>')
    for a in cur:
        isnow = a['a'] <= today <= a['b']
        s.append('<div class="row' + (' now' if isnow else '') + '"><span>' + av(a) + ' ' + esc(a['n']) + (' <span class="tag">' + L['now'] + '</span>' if isnow else '') + '</span><b>'
                 + a['a'].strftime('%d.%m.') + (' &ndash; ' + a['b'].strftime('%d.%m.') if a['b'] != a['a'] else '') + '</b></div>')
    s.append('</div>')
    if odl:
        s.append('<div class="box red"><h3>' + L['overdue'] + '</h3>')
        for e in odl:
            s.append('<div class="row"><span>' + e['d'].strftime('%d.%m.') + ' ' + esc(e['prod']) + '<small>' + esc(e['sup']) + (' · ' + esc(e['ref']) if e['ref'] else '') + '</small></span><b>' + num(e['qty']) + '</b></div>')
        s.append('</div>')
    s.append('<div class="box"><h3>' + L['month_list'] + MONTHS[m - 1] + '</h3>')
    if not mev:
        s.append('<p class="mut" style="margin:0">' + L['nodel'] + '</p>')
    for e in mev:
        tag = L['po'] if e['kind'] == 'po' else L['plan']
        s.append('<div class="row"><span><i class="dot" style="background:' + col(e['sup']) + '"></i>' + e['d'].strftime('%d.%m.') + ' ' + esc(e['prod'])
                 + '<small>' + esc(e['sup']) + (' · ' + esc(e['ship']) if e['ship'] else '') + ' · ' + tag + (' ' + esc(e['ref']) if e['ref'] else '') + '</small></span><b>' + num(e['qty']) + '</b></div>')
    s.append('</div>')
    if mev:
        tot = {}
        cnt = {}
        for e in mev:
            tot[e['sup']] = tot.get(e['sup'], 0) + e['qty']
            cnt[e['sup']] = cnt.get(e['sup'], 0) + 1
        s.append('<div class="box"><h3>' + L['by_sup'] + '</h3>')
        for kk in sorted(tot, key=lambda kk: -tot[kk]):
            s.append('<div class="row"><span><i class="dot" style="background:' + col(kk) + '"></i>' + esc(kk) + '<small>' + str(cnt[kk]) + ' ' + (L['deliv1'] if cnt[kk] == 1 else L['deliv']) + '</small></span><b>' + num(tot[kk]) + '</b></div>')
        s.append('<div class="row total"><span>' + L['total'] + '</span><b>' + num(sum(tot.values())) + ' ' + L['pcs'] + '</b></div></div>')
    s.append('</aside>')

    langlink = ('?key=' + KEY + '&amp;m=' + first.strftime('%Y-%m') + '&amp;lang=en') if de else ('?key=' + KEY + '&amp;m=' + first.strftime('%Y-%m'))
    html = (page_head(TITLE) + '<meta http-equiv="refresh" content="600"></head><body>'
            + '<div class="top"><div class="in"><div class="brand"><img src="' + LOGO + '" alt="IQ Dogsport"><div><h1>' + TITLE + '</h1><p>' + L['sub'] + '</p></div></div>'
            + '<nav><a href="' + link(prv) + '">&larr;</a><b>' + MONTHS[m - 1] + ' ' + str(y) + '</b><a href="' + link(nxt) + '">&rarr;</a>'
            + '<a href="' + link(today) + '">' + L['today'] + '</a><a href="' + langlink + '">' + ('EN' if de else 'DE') + '</a></nav></div></div>'
            + '<div class="wrap">' + ''.join(k) + '<main><div>' + ''.join(g) + ''.join(ag) + '</div>' + ''.join(s) + '</main></div>'
            + '<footer><span>' + L['upd'] + ': ' + datetime.datetime.now().strftime('%d.%m.%Y %H:%M') + ' UTC</span><a href="?key=' + KEY + '&amp;logout=1">' + L['logout'] + '</a></footer></body></html>')
    response = request.make_response(html, headers=[('Content-Type', 'text/html; charset=utf-8'), ('X-Robots-Tag', 'noindex'), ('Cache-Control', 'no-store')])
'''

PROCESS = r'''
Line = env['x_wareneingang_line'].sudo()
WE = env['x_wareneingang'].sudo()
PO = env['purchase.order'].sudo()
DE = (env.lang or 'en_US').startswith('de')

def target(h):
    t = (h or '').strip().lower()
    if 'customer style' in t or 'description' in t or 'bezeichnung' in t or 'product' in t or 'artikel' in t:
        return 'x_product_text'
    if 'reference' in t or t.startswith('ref') or 'order' in t or 'auftrag' in t or 'bestell' in t:
        return 'x_supplier_ref'
    if t in ('no', 'no.', 'nr', 'nr.', 'item no.', 'art.-nr.', 'art. nr.') or t.startswith('style'):
        return 'x_style_no'
    if 'shipment' in t or 'versand' in t or 'transport' in t:
        return 'x_shipment'
    if 'qty' in t or 'quantity' in t or 'menge' in t:
        return 'x_qty'
    if 'date' in t or 'datum' in t or 'termin' in t:
        return 'x_date'
    if 'amount' in t or 'betrag' in t or 'wert' in t or 'value' in t:
        return 'x_amount'
    if 'valuta' in t or 'currency' in t or 'währung' in t:
        return 'x_currency'
    return False

def attach_src(we, up, raw, fname, attached, de):
    if not we or we.id in attached:
        return
    attached.append(we.id)
    Att = env['ir.attachment'].sudo()
    if Att.search_count([('res_model', '=', 'x_wareneingang'), ('res_id', '=', we.id), ('name', '=', fname), ('file_size', '=', len(raw))]):
        return
    att = Att.create({'name': fname, 'datas': up.x_file, 'res_model': 'x_wareneingang', 'res_id': we.id})
    we.message_post(body=('Quelle: Lieferübersicht ' if de else 'Source: delivery overview ') + fname + ' (' + (up.x_name or '') + ')', attachment_ids=[att.id])

for up in records:
    if not up.x_file or not up.x_supplier_id:
        raise UserError('Bitte Lieferant wählen und Excel-Datei hochladen.' if DE else 'Please choose a supplier and upload an Excel file.')
    if (up.x_file_name or '').lower().endswith('.pdf'):
        sup = up.x_supplier_id
        Att = env['ir.attachment'].sudo()
        fname = up.x_file_name
        att = Att.search([('res_model', '=', 'x_iq_delivery_upload'), ('res_id', '=', up.id), ('name', '=', fname)], limit=1)
        if not att:
            att = Att.create({'name': fname, 'datas': up.x_file, 'mimetype': 'application/pdf', 'res_model': 'x_iq_delivery_upload', 'res_id': up.id})
        txt = att.index_content or ''
        if len(txt.strip()) < 20:
            up.write({'x_result': '<div class="alert alert-danger">' + ('Der Text im PDF konnte nicht gelesen werden (eingescanntes PDF?). Bitte die Lieferung im Wareneingang manuell eintragen.' if DE else 'The PDF text could not be read (scanned PDF?). Please add the delivery manually.') + '</div>'})
            continue
        flat = ' '.join(txt.split())
        # ---- purchase order: PO number or vendor reference (e.g. AB 2026-232475) in the text
        cand = PO.search([('partner_id', 'child_of', sup.commercial_partner_id.id), ('state', 'in', ['purchase', 'done'])], order='id desc')
        cand = cand.filtered(lambda p: p.receipt_status != 'full') + cand.filtered(lambda p: p.receipt_status == 'full')
        po = PO
        for p in cand:
            refs = [p.name]
            r = (p.partner_ref or '').strip()
            if r:
                refs.append(r)
                core = r.split()[-1]
                if len(core) >= 6:
                    refs.append(core)
            if [x for x in refs if x and x in flat]:
                po = p
                break
        if not po:
            up.write({'x_result': '<div class="alert alert-warning">' + ('Keine passende Bestellung gefunden. Im PDF steht keine Bestellnummer (P0…) und keine Auftragsnummer, die bei einer Bestellung von ' if DE else 'No matching purchase order found. The PDF contains no PO number and no order number stored on a purchase order of ') + sup.name + ('. Bitte die Lieferanten-Auftragsnummer in der Bestellung (Feld Lieferantenreferenz) prüfen.' if DE else '. Please check the vendor reference on the purchase order.') + '</div>'})
            continue
        # ---- delivery note number
        dn = ''
        for kw in ['Lieferscheinnummer', 'Lieferschein-Nr', 'Lieferschein Nr', 'Lieferschein', 'Delivery note']:
            pos_ = flat.find(kw)
            if pos_ >= 0:
                for tok in flat[pos_ + len(kw):pos_ + len(kw) + 40].replace(':', ' ').split():
                    if [c for c in tok if c.isdigit()] and len(tok) >= 4:
                        dn = tok.strip('.,;')
                        break
            if dn:
                break
        if not dn:
            dn = fname.rsplit('.', 1)[0]
        # ---- date: delivery date in the PDF if it is in the future, otherwise today (goods arrived)
        def find_dates(t):
            out = []
            for k in range(len(t) - 9):
                c = t[k:k + 10]
                if c[2] == '.' and c[5] == '.' and c[:2].isdigit() and c[3:5].isdigit() and c[6:].isdigit():
                    try:
                        out.append((k, datetime.date(int(c[6:]), int(c[3:5]), int(c[:2]))))
                    except Exception:
                        pass
            return out
        today = datetime.date.today()
        ddate = today
        for kw in ['Liefertermin', 'Lieferdatum', 'Anlieferung']:
            pos_ = flat.find(kw)
            if pos_ >= 0:
                near = [d for k, d in find_dates(flat[pos_:pos_ + 60])]
                if near and near[0] > today:
                    ddate = near[0]
                break
        # ---- quantities per article from the PDF
        # Holfelder layout: "IQ DOGSPORT | Multifunktionsjacke 4.0, Herren, grau, S" ... "HBM-Cross-Docking-1 (40)"
        groups = []
        gqty = {}
        npos = 0
        cur = ''
        for ln in txt.splitlines():
            s = ln.strip()
            if ' | ' in s and not s.startswith(sup.name or '#') and 'Holfelder GmbH' not in s:
                art = s.split(' | ', 1)[1]
                cur = art.split(',')[0].strip()
                if cur.lower().startswith('porto') or cur.lower().startswith('spedition'):
                    cur = ''
                continue
            if cur and s.endswith(')') and '(' in s:
                n = s[s.rfind('(') + 1:-1].strip()
                if n.isdigit():
                    if cur not in gqty:
                        groups.append(cur)
                        gqty[cur] = 0
                    gqty[cur] += int(n)
                    npos += 1
                    cur = ''
        goods = po.order_line.filtered(lambda l: l.product_qty > 0 and l.product_id and l.product_id.type != 'service')
        if not groups:
            open_qty = sum([max(l.product_qty - l.qty_received, 0) for l in goods])
            names = []
            for l in goods.filtered(lambda l: l.qty_received < l.product_qty) or goods:
                n = (l.product_id.product_tmpl_id.name or '').split(' – ')[0]
                if n not in names:
                    names.append(n)
            g0 = (names[0] + (' +' + str(len(names) - 1) if len(names) > 1 else '')) if names else po.name
            groups = [g0]
            gqty[g0] = open_qty
        qty_note = (('aus PDF, ' + str(npos) + ' Positionen') if DE else ('read from PDF, ' + str(npos) + ' lines')) if npos else ('Artikel im PDF nicht erkannt – offene Menge der Bestellung' if DE else 'articles not recognised in PDF – open quantity of the purchase order')
        # ---- card of this PO (never a new delivery card if the PO already has one)
        we = WE.search([('x_studio_purchase_order', '=', po.id)], limit=1)
        new_card = False
        if not we:
            we = WE.create({'x_name': po.name, 'x_studio_purchase_order': po.id, 'x_studio_supplier': po.partner_id.id,
                            'x_supplier_ref': po.partner_ref or False})
            new_card = True
        shipment = ('Lieferschein ' if DE else 'Delivery note ') + dn
        # same delivery note uploaded again: replace its open calendar entries
        old = Line.search([('x_wareneingang_id', '=', we.id), ('x_shipment', '=', shipment), ('x_done', '=', False)])
        replaced = len(old)
        old.unlink()
        rows = ''
        total = 0
        for g in groups:
            Line.create({'x_wareneingang_id': we.id, 'x_partner_id': sup.id, 'x_supplier_ref': po.partner_ref or po.name,
                         'x_product_text': g, 'x_shipment': shipment, 'x_qty': gqty[g], 'x_date': ddate,
                         'x_name': ' · '.join([x for x in [po.partner_ref or po.name, g, shipment] if x])})
            total += gqty[g]
            rows += '<li>' + g + ': <b>' + str(int(gqty[g])) + (' Stk.' if DE else ' pcs') + '</b></li>'
        qty = total
        action_txt = (('ersetzt' if DE else 'replaced') if replaced else ('angelegt' if DE else 'created'))
        prod_txt = ', '.join(groups)
        # ---- attach the PDF to the card (once)
        raw = b64decode(up.x_file)
        if not Att.search_count([('res_model', '=', 'x_wareneingang'), ('res_id', '=', we.id), ('name', '=', fname), ('file_size', '=', len(raw))]):
            catt = Att.create({'name': fname, 'datas': up.x_file, 'mimetype': 'application/pdf', 'res_model': 'x_wareneingang', 'res_id': we.id})
            we.message_post(body=(('Lieferschein ' + dn + ' hochgeladen: ' + str(int(qty)) + ' Stk. am ' + ddate.strftime('%d.%m.%Y')) if DE else ('Delivery note ' + dn + ' uploaded: ' + str(int(qty)) + ' pcs on ' + ddate.strftime('%d.%m.%Y'))), attachment_ids=[catt.id])
        if not up.x_name:
            up.write({'x_name': sup.name + ' – ' + dn})
        up.write({'x_result': '<div class="alert alert-success mb-2">' + ('PDF verarbeitet.' if DE else 'PDF processed.') + '</div><ul>'
                  + '<li>' + ('Bestellung: ' if DE else 'Purchase order: ') + '<b>' + po.name + '</b>' + (' (' + po.partner_ref + ')' if po.partner_ref else '') + '</li>'
                  + '<li>' + ('Wareneingangs-Karte: ' if DE else 'Goods receipt card: ') + we.x_name + (' (neu)' if new_card and DE else (' (new)' if new_card else '')) + '</li>'
                  + '<li>' + ('Kalendereinträge ' if DE else 'Calendar entries ') + action_txt + ' (' + str(len(groups)) + (') am ' if DE else ') on ') + ddate.strftime('%d.%m.%Y') + ' · ' + qty_note + ':<ul>' + rows + '</ul></li>'
                  + '<li>' + ('PDF an die Karte angehängt.' if DE else 'PDF attached to the card.') + '</li>'
                  + '<li class="text-muted">' + ('Nach dem Buchen des Wareneingangs bitte in „Anstehende Lieferungen“ den Haken „Angekommen“ setzen.' if DE else 'After booking the receipt, tick "Arrived" in Upcoming deliveries.') + '</li></ul>'})
        continue
    sup = up.x_supplier_id
    if not up.x_name:
        up.write({'x_name': sup.name + ' – ' + datetime.date.today().strftime('%d.%m.%Y')})
    fname = up.x_file_name or 'upload.xlsx'
    ftype = 'text/csv' if fname.lower().endswith('.csv') else ('application/vnd.ms-excel' if fname.lower().endswith('.xls') else 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    imp = env['base_import.import'].sudo().create({'res_model': 'x_wareneingang_line', 'file': b64decode(up.x_file),
                                                   'file_name': fname, 'file_type': ftype})
    options = {'has_headers': True, 'advanced': False, 'keep_matches': False, 'name_create_enabled_fields': {},
               'import_set_empty_fields': [], 'import_skip_records': [], 'fallback_values': {}, 'skip': 0, 'limit': 5000,
               'encoding': '', 'separator': '', 'quoting': '"', 'date_format': '', 'datetime_format': '',
               'float_thousand_separator': ',', 'float_decimal_separator': '.'}
    prev = imp.parse_preview(options)
    if prev.get('error'):
        up.write({'x_result': '<div class="alert alert-danger">' + str(prev.get('error')) + '</div>'})
        continue
    options = prev.get('options') or options
    headers = prev.get('headers') or []
    used = []
    fields = []
    for h in headers:
        f = target(h)
        if f and f not in used:
            used.append(f)
            fields.append(f)
        else:
            fields.append(False)
    if 'x_supplier_ref' not in used or 'x_date' not in used:
        up.write({'x_result': '<div class="alert alert-danger">' + ('Spalten für Bestellnummer und Lieferdatum nicht gefunden. Gefundene Spalten: ' if DE else 'Columns for order no. and delivery date not found. Columns found: ') + ', '.join([str(h) for h in headers]) + '</div>'})
        continue
    res = imp.with_context(default_x_partner_id=sup.id).execute_import(fields, headers, options)
    errors = [m for m in (res.get('messages') or []) if m.get('type') == 'error']
    if errors or not res.get('ids'):
        up.write({'x_result': '<div class="alert alert-danger">' + '<br/>'.join([str(m.get('message')) for m in errors]) + '</div>'})
        continue
    new = Line.browse(res['ids'])
    new.write({'x_partner_id': sup.id})
    raw = b64decode(up.x_file)
    attached = []
    created = []
    linked = []
    changed = []
    same = 0
    added = 0
    for l in new:
        ref = (l.x_supplier_ref or '').strip()
        old = Line.search([('id', 'not in', new.ids), ('x_partner_id', '=', sup.id), ('x_supplier_ref', '=', ref),
                           ('x_style_no', '=', l.x_style_no), ('x_shipment', '=', l.x_shipment)], limit=1)
        if old:
            msgs = []
            if old.x_date != l.x_date:
                msgs.append(('Liefertermin ' if DE else 'Delivery date ') + (old.x_date.strftime('%d.%m.%Y') if old.x_date else '–') + ' → ' + (l.x_date.strftime('%d.%m.%Y') if l.x_date else '–'))
            if old.x_qty != l.x_qty:
                msgs.append(('Menge ' if DE else 'Qty ') + str(int(old.x_qty)) + ' → ' + str(int(l.x_qty)))
            if msgs:
                old.write({'x_date': l.x_date, 'x_qty': l.x_qty, 'x_amount': l.x_amount})
                txt = (old.x_product_text or '') + ' ' + (old.x_shipment or '') + ': ' + ', '.join(msgs)
                if old.x_wareneingang_id:
                    old.x_wareneingang_id.message_post(body=('Lieferübersicht aktualisiert – ' if DE else 'Delivery overview updated – ') + txt)
                changed.append(ref + ' – ' + txt)
            else:
                same += 1
            attach_src(old.x_wareneingang_id, up, raw, fname, attached, DE)
            l.unlink()
            continue
        we = WE.search([('x_supplier_ref', '=', ref), '|', ('x_studio_supplier', '=', sup.id),
                        ('x_studio_purchase_order.partner_id', 'child_of', sup.commercial_partner_id.id)], limit=1) if ref else WE
        if not we:
            po = PO.search([('partner_ref', '=', ref), ('partner_id', 'child_of', sup.commercial_partner_id.id)], limit=1) if ref else PO
            if po:
                we = WE.search([('x_studio_purchase_order', '=', po.id)], limit=1)
                if not we:
                    we = WE.create({'x_name': po.name, 'x_studio_purchase_order': po.id, 'x_studio_supplier': po.partner_id.id})
                we.write({'x_supplier_ref': ref})
                linked.append(ref + ' → ' + po.name)
            else:
                we = WE.create({'x_name': ref + ' – ' + (l.x_product_text or ''), 'x_studio_supplier': sup.id, 'x_supplier_ref': ref})
                created.append(we.x_name)
        l.write({'x_wareneingang_id': we.id, 'x_name': ' · '.join([x for x in [ref, l.x_product_text, l.x_shipment] if x])})
        attach_src(we, up, raw, fname, attached, DE)
        added += 1
    h = ['<div class="alert alert-success mb-2">' + ('Datei verarbeitet.' if DE else 'File processed.') + '</div><ul>']
    h.append('<li>' + ('Neue Lieferungen (ohne Bestellung): ' if DE else 'New deliveries (no PO): ') + str(len(created)) + '</li>')
    for c in created:
        h.append('<li class="ms-3">' + c + '</li>')
    h.append('<li>' + ('Mit Bestellung verknüpft: ' if DE else 'Linked to purchase orders: ') + str(len(linked)) + '</li>')
    for c in linked:
        h.append('<li class="ms-3">' + c + '</li>')
    h.append('<li>' + ('Neue Lieferpositionen: ' if DE else 'New shipment lines: ') + str(added) + '</li>')
    h.append('<li>' + ('Geändert: ' if DE else 'Changed: ') + str(len(changed)) + '</li>')
    for c in changed:
        h.append('<li class="ms-3 text-warning">' + c + '</li>')
    h.append('<li>' + ('Unverändert: ' if DE else 'Unchanged: ') + str(same) + '</li>')
    h.append('<li>' + ('Datei an Karten angehängt: ' if DE else 'File attached to cards: ') + str(len(attached)) + '</li></ul>')
    up.write({'x_result': ''.join(h)})
'''

SA = env['ir.actions.server'].sudo()
done = []
# 1) PDF import first - every server action that still has the old "PDF not supported" code
procs = SA.search([('name', '=', 'IQ Lieferübersicht verarbeiten')]) | SA.search([('code', 'ilike', 'PDF files are not supported'), ('usage', '!=', 'ir_cron')])
if not procs:
    raise UserError('Server action "IQ Lieferübersicht verarbeiten" not found')
procs.write({'code': PROCESS})
done.append('import: PDF on in ' + str(len(procs)) + ' action(s) ' + str(procs.ids))

# 2) calendar page (password is set if it is missing)
ICP = env['ir.config_parameter'].sudo()
if not ICP.get_param('iq.delivery_calendar_password'):
    ICP.set_param('iq.delivery_calendar_password', '<PASSWORD-REMOVED>')
    done.append('page password set to <PASSWORD-REMOVED>')
cal = SA.search([('name', '=', 'IQ Public delivery calendar')])
if cal:
    cal.write({'code': PAGE})
    done.append('calendar page updated')
else:
    done.append('calendar page NOT found')

UA = env['ir.actions.act_url'].sudo()
ua = UA.search([('name', 'in', ['Public calendar', 'Öffentlicher Lieferkalender', 'Warehouse & team calendar', 'Lager- & Teamkalender'])], limit=1)
if ua:
    ua.write({'name': 'Warehouse & team calendar'})
    ua.update_field_translations('name', {'en_US': 'Warehouse & team calendar', 'de_DE': 'Lager- & Teamkalender'})
    m = env['ir.ui.menu'].sudo().with_context(active_test=False).search([('action', '=', 'ir.actions.act_url,' + str(ua.id))], limit=1)
    if m:
        m.write({'name': 'Warehouse & team calendar'})
        m.update_field_translations('name', {'en_US': 'Warehouse & team calendar', 'de_DE': 'Lager- & Teamkalender'})
        done.append('menu renamed')
log('IQ update 06.11. (calendar v3 + PDF import): ' + ' | '.join(done))
