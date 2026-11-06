# IQ Goods Receipts – public delivery calendar (no login), staging 05.11.2026
# Creates a published website server action "IQ Public delivery calendar".
# Link: <your odoo>/website/action/iq-delivery-calendar?key=<KEY>   (exact link: see the log line)
# Run: Scheduled Action (Model: Contact, Active = off) -> Save -> Run Manually.
# Change the key later: Settings -> Technical -> System Parameters -> iq.delivery_calendar_key

KEY = ''  # public copy: key removed
PATH = 'iq-delivery-calendar'

PAGE = r'''
P = env['ir.config_parameter'].sudo()
KEY = P.get_param('iq.delivery_calendar_key') or ''
params = request.params if request else {}
if not KEY or params.get('key') != KEY:
    response = request.make_response('Not found', headers=[('Content-Type', 'text/plain; charset=utf-8')], status=404)
else:
    de = params.get('lang', 'de') != 'en'
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

    def link(d):
        return '?key=' + KEY + '&amp;m=' + d.strftime('%Y-%m') + ('' if de else '&amp;lang=en')

    # ---------- calendar grid
    g = ['<div class="grid">']
    for dn in DAYS:
        g.append('<div class="dh">' + dn + '</div>')
    d = gstart
    while d <= gend:
        cls = 'day' + (' out' if d.month != m else '') + (' today' if d == today else '')
        g.append('<div class="' + cls + '"><div class="dn">' + str(d.day) + '</div>')
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

    langlink = ('?key=' + KEY + '&amp;m=' + first.strftime('%Y-%m') + '&amp;lang=en') if de else ('?key=' + KEY + '&amp;m=' + first.strftime('%Y-%m'))
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
.ev.od{background:#fee2e2}aside{display:flex;flex-direction:column;gap:12px}
.box{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px}.box h3{margin:0 0 8px;font-size:14px}.box.red{border-color:#fca5a5;background:#fef2f2}.box.red h3{color:var(--red)}
.row{display:flex;justify-content:space-between;gap:8px;padding:5px 0;border-top:1px solid var(--line)}.row:first-of-type{border-top:0}
.row span{min-width:0}.row small{display:block;color:var(--mut)}.row b{white-space:nowrap}.row i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px}
.row.total{border-top:2px solid var(--fg);font-weight:700}.muted{color:var(--mut)}footer{color:var(--mut);font-size:12px;padding:0 18px 16px}
@media(max-width:900px){main{grid-template-columns:1fr}.day{min-height:70px}.ev span{display:none}}
</style></head><body><header><div><h1>""" + L['title'] + """</h1><p>IQ Dogsport · """ + L['sub'] + """</p></div>
<nav><a href=""" + '"' + link(prv) + '"' + """>&larr;</a><b>""" + MONTHS[m - 1] + ' ' + str(y) + """</b><a href=""" + '"' + link(nxt) + '"' + """>&rarr;</a>
<a href=""" + '"' + link(today) + '"' + """>""" + L['today'] + """</a><a href=""" + '"' + langlink + '"' + """>""" + ('EN' if de else 'DE') + """</a></nav></header>
<main>""" + ''.join(g) + ''.join(s) + """</main><footer>""" + L['upd'] + ': ' + datetime.datetime.now().strftime('%d.%m.%Y %H:%M') + """ UTC</footer></body></html>"""
    response = request.make_response(html, headers=[('Content-Type', 'text/html; charset=utf-8'), ('X-Robots-Tag', 'noindex')])
'''

P = env['ir.config_parameter'].sudo()
if not P.get_param('iq.delivery_calendar_key'):
    P.set_param('iq.delivery_calendar_key', KEY)
model = env['ir.model'].sudo().search([('model', '=', 'x_wareneingang_line')], limit=1)
SA = env['ir.actions.server'].sudo()
if 'website_published' not in SA._fields:
    raise UserError('Website app fields not found on server actions')
sa = SA.search([('name', '=', 'IQ Public delivery calendar')], limit=1)
vals = {'name': 'IQ Public delivery calendar', 'model_id': model.id, 'state': 'code', 'code': PAGE,
        'website_published': True, 'website_path': PATH}
if sa:
    sa.write(vals)
else:
    sa = SA.create(vals)
log('IQ public calendar: ' + (sa.website_url or '') + '?key=' + P.get_param('iq.delivery_calendar_key'))
