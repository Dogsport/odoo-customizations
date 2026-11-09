# IQ Warehouse & team calendar – "My hours & vacation" (employee PIN) + Team overview (manager PIN)   09.11.2026
# Run once: Scheduled Action (Model: Contact, Active = off) -> paste -> Save -> Run Manually -> reload.
# Changes ONLY the code of the server action "IQ Public delivery calendar". No new fields.
# Manager PIN: Settings -> Technical -> System Parameters -> key  iq.delivery_calendar_manager_pin  (at least 8 digits).
# Afterwards check Settings -> Technical -> Logging, search "IQ my-hours".

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
.ab.pend{background:#fff4e5;border:1px dashed #f59e0b;border-radius:4px;padding:1px 4px;color:#92400e}.ab.pend .av{opacity:.75}
.tag.pend{background:#f59e0b}.row.pend{color:#92400e}.lgd{display:flex;gap:12px;flex-wrap:wrap;font-size:11.5px;color:var(--mut);margin:8px 0 0}.lgd i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:4px;vertical-align:-1px}
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
elif params.get('melogout') or (request.httprequest.method == 'POST' and params.get('pin') is not None) or params.get('view') == 'me':
    # ------------------------------------------------------------------ personal view (employee PIN) + manager view (manager PIN)
    ICP = env['ir.config_parameter'].sudo()
    Emp = env['hr.employee'].sudo()
    Leave = env['hr.leave'].sudo()
    LT = env['hr.leave.type'].sudo()
    Alloc = env['hr.leave.allocation'].sudo()
    MPIN = (ICP.get_param('iq.delivery_calendar_manager_pin') or '').strip()
    if len(MPIN) < 8:
        MPIN = ''
    SESSION = 600
    nowdt = datetime.datetime.now()
    nowts = int((nowdt - datetime.datetime(1970, 1, 1)).total_seconds())
    today = datetime.date.today()
    esc = lambda s: (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    hbase = base.replace('&', '&amp;')
    me_url = base + '&view=me'
    ltf = LT.fields_get()
    lvf = Leave.fields_get()
    otypes = LT.search([('overtime_deductible', '=', True)]) if 'overtime_deductible' in ltf else LT
    is_sick = lambda t: bool([w for w in ['krank', 'sick'] if w in (t.name or '').lower()])

    def short(e):
        parts = (e.name or '').split()
        return (parts[0] + (' ' + parts[-1][0] + '.' if len(parts) > 1 else '')) if parts else ''

    def sig(who, pin, exp):
        x = 2166136261
        for ch in (KEY + '|' + PW + '|' + str(who) + '|' + (pin or '') + '|' + str(exp)):
            x = ((x ^ ord(ch)) * 16777619) % 4294967296
        y2 = 2166136261
        for ch in (str(exp) + '#' + (pin or '') + '#' + PW + '#' + str(who)):
            y2 = ((y2 ^ ord(ch)) * 16777619) % 4294967296
        return '%08x%08x' % (x, y2)

    def hm(v, signed=False):
        neg = v < 0
        mins = int(round(abs(v) * 60))
        t = str(mins // 60) + ':' + ('0' + str(mins % 60))[-2:]
        return ('−' if neg else ('+' if signed and mins else '')) + t

    def dnum(v):
        s = ('%.1f' % v).replace('.0', '')
        return s.replace('.', ',') if de else s

    def olink(model, rid, label, cls=''):
        return ('<a class="ol ' + cls + '" target="_blank" href="/web#model=' + model + '&amp;id=' + str(rid) + '&amp;view_type=form" title="' + ('In Odoo öffnen' if de else 'Open in Odoo') + '">' + label + ' <span class="arr">↗</span></a>')

    T = {
        'title': 'Meine Stunden &amp; Urlaub' if de else 'My hours &amp; vacation',
        'team': 'Team-Übersicht' if de else 'Team overview',
        'mgr': '— Führungskraft / Manager —',
        'pick': 'Name wählen' if de else 'Choose your name',
        'pin': 'PIN (Mitarbeitende: wie am Zeiterfassungs-Terminal)' if de else 'PIN (employees: same as the attendance kiosk)',
        'show': 'Anzeigen' if de else 'Show',
        'wrong': 'Name oder PIN falsch.' if de else 'Wrong name or PIN.',
        'locked': 'Zu viele Versuche. Bitte in 15 Minuten erneut versuchen.' if de else 'Too many attempts. Please try again in 15 minutes.',
        'back': '&larr; Kalender' if de else '&larr; Calendar',
        'backteam': '&larr; Team' if de else '&larr; Team',
        'out': 'Abmelden' if de else 'Sign out',
        'auto': 'Aus Datenschutzgründen wirst du nach 10 Minuten automatisch abgemeldet.' if de else 'For privacy you are signed out automatically after 10 minutes.',
        'ot_rem': 'Überstunden-Saldo' if de else 'Overtime balance',
        'ot_earn': 'Überstunden verdient' if de else 'Overtime earned',
        'ot_used': 'Überstunden genutzt' if de else 'Overtime used',
        'vac_rem': 'Urlaub übrig' if de else 'Vacation left',
        'days': 'Tage' if de else 'days', 'day': 'Tag' if de else 'day', 'h': 'Std.' if de else 'h',
        'valid': 'gültig bis' if de else 'valid until',
        'calc': 'So setzt sich der Saldo zusammen' if de else 'How the balance is made up',
        'earned': 'Verdient (alle Tage mit Mehrarbeit)' if de else 'Earned (all days with extra hours)',
        'used': 'Genutzt / abgezogen' if de else 'Used / deducted',
        'other': 'Sonstige Korrekturen' if de else 'Other corrections',
        'bal': 'Saldo heute' if de else 'Balance today',
        'permonth': 'Überstunden pro Monat' if de else 'Overtime per month',
        'month': 'Monat' if de else 'Month', 'plus': 'Verdient' if de else 'Earned', 'minus': 'Abgezogen' if de else 'Deducted',
        'uselist': 'Wann Stunden abgezogen wurden' if de else 'When hours were deducted',
        'nouse': 'Noch keine Stunden abgezogen.' if de else 'No hours deducted yet.',
        'timeoff': 'Freizeitausgleich' if de else 'Time off in lieu',
        'manual': 'Manuelle Korrektur' if de else 'Manual correction',
        'short': 'Weniger gearbeitet als Soll (Minusstunden)' if de else 'Worked less than planned (minus hours)',
        'vac': 'Urlaub' if de else 'Vacation',
        'ent': 'Anspruch' if de else 'Entitlement', 'taken': 'Genommen' if de else 'Taken',
        'planned': 'Geplant' if de else 'Planned', 'req': 'Beantragt' if de else 'Requested', 'left': 'Übrig' if de else 'Left',
        'novac': 'Kein Urlaubsanspruch hinterlegt.' if de else 'No vacation entitlement on file.',
        'allreq': 'Alle Anträge' if de else 'All requests', 'when': 'Zeitraum' if de else 'Dates', 'type': 'Art' if de else 'Type',
        'amount': 'Umfang' if de else 'Amount', 'noreq': 'Keine Anträge in diesem Jahr.' if de else 'No requests this year.',
        'open_s': 'offen' if de else 'open',
        'open_note': ('Noch nicht genehmigt: %d – bitte bei Bedarf direkt mit der Führungskraft sprechen.' if de else 'Not approved yet: %d – talk to the manager directly if needed.'),
        'employee': 'Mitarbeiter' if de else 'Employee', 'sick': 'Krank' if de else 'Sick', 'absnow': 'Abwesenheit' if de else 'Absence',
        'k_emp': 'Mitarbeitende' if de else 'Employees', 'k_open': 'Offene Anträge' if de else 'Open requests',
        'k_absent': 'Heute abwesend' if de else 'Absent today', 'k_neg': 'Minus-Saldo' if de else 'Negative balance',
        'todo': 'Zu genehmigen' if de else 'To approve', 'nothing': 'Keine offenen Anträge.' if de else 'No open requests.',
        'next30': 'Abwesenheiten nächste 30 Tage' if de else 'Absences next 30 days', 'noabs': 'Keine.' if de else 'None.',
        'details': 'Details' if de else 'Details', 'today': 'heute' if de else 'today',
        'hint': 'Klick auf einen Namen zeigt alle Details. Klick auf ↗ öffnet den Datensatz in Odoo (Odoo-Login nötig).' if de else 'Click a name for all details. Click ↗ to open the record in Odoo (Odoo login needed).',
        'empform': 'Mitarbeiter in Odoo' if de else 'Employee in Odoo',
    }
    MONTHS_S = (['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'] if de else
                ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    MECSS = ('<style>.me-k{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-bottom:14px}'
             '.me-g{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}.col{display:flex;flex-direction:column;gap:14px}'
             '.box table{width:100%;border-collapse:collapse;font-size:13.5px}.box td,.box th{padding:7px 5px;border-top:1px solid var(--line);text-align:left;vertical-align:middle}'
             '.box th{font:700 11px Arial;letter-spacing:.8px;text-transform:uppercase;color:var(--mut);border-top:0}'
             '.box td.r,.box th.r{text-align:right;white-space:nowrap}.pos{color:#047857}.neg{color:var(--red)}'
             '.sum td{border-top:2px solid var(--fg);font-weight:700}'
             '.st{display:inline-block;font:700 11px Arial;border-radius:4px;padding:3px 8px;white-space:nowrap}.st-ok{background:#dcfce7;color:#166534}.st-op{background:#f59e0b;color:#fff}.st-no{background:#fee2e2;color:#991b1b}.st-sick{background:#e0e7ff;color:#3730a3}'
             'tr.rq-op td{background:#fff7ed}tr.rq-no td{color:#991b1b;text-decoration:line-through;text-decoration-color:#fca5a5}tr.rq-no td:last-child{text-decoration:none}'
             '.note-op{background:#fff7ed;border:1px solid #f59e0b;color:#92400e;border-radius:6px;padding:8px 10px;margin:0 0 10px;font-weight:700}'
             '.kpi.op{border-color:#f59e0b;background:#fff7ed}.kpi.op b{color:#b45309}.opn{color:#b45309;font-weight:700}'
             '.lgd{display:flex;gap:12px;flex-wrap:wrap;font-size:11.5px;color:var(--mut);margin:10px 0 0}.lgd i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:4px;vertical-align:-1px}'
             'a.ol{text-decoration:none;color:inherit;border-bottom:1px dotted #9ca3af}a.ol:hover{color:var(--red);border-color:var(--red)}a.ol .arr{font-size:11px;color:#9ca3af}'
             'a.nm{font-weight:700;text-decoration:none;color:var(--fg)}a.nm:hover{color:var(--red)}'
             '.who{color:#bdbdbd;font-size:12.5px}.pf{max-width:400px;margin:30px auto;background:#fff;border:1px solid var(--line);border-radius:10px;padding:22px}'
             '.pf h2{margin:0 0 14px;font:800 18px Arial}.pf label{display:block;font-weight:700;margin:10px 0 4px}'
             '.pf select,.pf input{width:100%;padding:11px;border:1px solid #d1d5db;border-radius:6px;font-size:16px;background:#fff}'
             '.pf button{width:100%;margin-top:14px;padding:12px;border:0;border-radius:6px;background:var(--red);color:#fff;font:700 15px Arial;cursor:pointer}'
             '.pf .e{color:var(--red);font-weight:700;margin:12px 0 0}'
             '.me-k~.box,.wrap>.box,.box.team{overflow-x:auto;min-width:0}.me-g>*{min-width:0}.team{overflow-x:auto}.team table{min-width:860px}.team tr:hover td{background:#fafaf8}.team .warn td{background:#fff7ed}'
             '.hint{color:var(--mut);font-size:12px;margin:8px 0 0}'
             '@media(max-width:980px){.me-k{grid-template-columns:repeat(2,minmax(0,1fr))}.me-g{grid-template-columns:1fr}}'
             '@media(max-width:700px){table.rqt td,table.rqt th{font-size:12.5px;padding:6px 3px}table.rqt .st{font-size:10px;padding:2px 5px;white-space:normal;display:inline-block;max-width:92px;text-align:center}}</style>')

    def shell(inner, who, refresh, mgr_back=False):
        nav = '<a href="' + hbase + '">' + T['back'] + '</a>'
        if mgr_back:
            nav += '<a href="' + hbase + '&amp;view=me">' + T['backteam'] + '</a>'
        if who:
            nav += '<a href="' + hbase + '&amp;melogout=1">' + T['out'] + '</a>'
        return (page_head(T['title'].replace('&amp;', '&')) + MECSS
                + ('<meta http-equiv="refresh" content="' + str(SESSION) + ';url=' + hbase + '&amp;melogout=1">' if refresh else '')
                + '</head><body><div class="top"><div class="in"><div class="brand"><img src="' + LOGO + '" alt="IQ Dogsport"><div><h1>' + (T['team'] if who == '*' else T['title']) + '</h1>'
                + ('<p class="who">' + esc(who) + '</p>' if who and who != '*' else '') + '</div></div>'
                + '<nav>' + nav + '</nav></div></div>'
                + '<div class="wrap">' + inner + '</div>'
                + ('<footer><span>' + T['auto'] + '</span></footer>' if who else '') + '</body></html>')

    emps = Emp.search([('pin', '!=', False)], order='name asc')

    def picker(msg):
        sel = str(params.get('emp') or '')
        opts = ('<option value="M"' + (' selected' if sel == 'M' else '') + '>' + T['mgr'] + '</option>' if MPIN else '')
        opts += ''.join(['<option value="' + str(e.id) + '"' + (' selected' if str(e.id) == sel else '') + '>' + esc(short(e)) + '</option>' for e in emps])
        return ('<form class="pf" method="post" action=""><h2>' + T['title'] + '</h2>'
                + '<input type="hidden" name="csrf_token" value="' + request.csrf_token() + '"><input type="hidden" name="key" value="' + KEY + '">'
                + ('' if de else '<input type="hidden" name="lang" value="en">')
                + '<label>' + T['pick'] + '</label><select name="emp" required><option value=""></option>' + opts + '</select>'
                + '<label>' + T['pin'] + '</label><input type="password" name="pin" inputmode="numeric" autocomplete="off" required>'
                + '<button>' + T['show'] + '</button>' + ('<p class="e">' + msg + '</p>' if msg else '') + '</form>')

    def html_resp(body):
        return request.make_response(body, headers=[('Content-Type', 'text/html; charset=utf-8'), ('X-Robots-Tag', 'noindex'), ('Cache-Control', 'no-store')])

    # ------------------------------------------------------------------ data
    def ot_data(emp):
        lines = []
        OTM = 'hr.attendance.overtime.line' if 'hr.attendance.overtime.line' in env else ('hr.attendance.overtime' if 'hr.attendance.overtime' in env else '')
        if OTM:
            OT = env[OTM].sudo()
            fg = OT.fields_get()
            dom = [('employee_id', '=', emp.id)]
            if 'status' in fg:
                dom.append(('status', '=', 'approved'))
            dfield = 'manual_duration' if 'manual_duration' in fg else 'duration'
            for o in OT.search(dom, order='date asc'):
                v = o[dfield] or 0.0
                if abs(v) < 0.005 or not o.date:
                    continue
                why = ''
                for rf in ['reason', 'name', 'description', 'note']:
                    if rf in fg and fg[rf].get('type') in ('char', 'text') and o[rf]:
                        why = o[rf]
                        break
                lines.append({'d': o.date, 'v': v, 'why': why, 'id': o.id, 'm': OTM})
        earned = sum([l['v'] for l in lines if l['v'] > 0])
        bal = emp.total_overtime if 'total_overtime' in Emp.fields_get(['total_overtime']) else earned + sum([l['v'] for l in lines if l['v'] < 0])
        items = [{'d': l['d'], 'v': -l['v'], 'what': (T['manual'] + ': ' + l['why']) if l['why'] else T['short'], 'm': l['m'], 'id': l['id']} for l in lines if l['v'] < 0]
        if otypes:
            for lv in Leave.search([('employee_id', '=', emp.id), ('holiday_status_id', 'in', otypes.ids), ('state', '=', 'validate')], order='request_date_from asc'):
                hrs = lv.number_of_hours if 'number_of_hours' in lvf else (lv.number_of_days or 0) * 8
                dd = lv.request_date_from.strftime('%d.%m.%Y') + ('' if lv.request_date_to == lv.request_date_from else ' – ' + lv.request_date_to.strftime('%d.%m.%Y'))
                items.append({'d': lv.request_date_from, 'v': hrs, 'what': T['timeoff'] + ' (' + dd + ')', 'm': 'hr.leave', 'id': lv.id})
        items = sorted(items, key=lambda u: u['d'], reverse=True)
        used = earned - bal
        return {'lines': lines, 'earned': earned, 'bal': bal, 'used': used, 'items': items, 'other': used - sum([u['v'] for u in items])}

    def vac_data(emp):
        out = []
        allocs = Alloc.search([('employee_id', '=', emp.id), ('state', '=', 'validate')])
        for t in allocs.mapped('holiday_status_id'):
            if t.id in otypes.ids or is_sick(t):
                continue
            al = Alloc.browse([a.id for a in allocs if a.holiday_status_id.id == t.id and a.date_from and a.date_from <= today and (not a.date_to or a.date_to >= today)])
            if not al:
                continue
            start = min(al.mapped('date_from'))
            ends = [a.date_to for a in al if a.date_to]
            end = max(ends) if ends and len(ends) == len(al) else False
            ldom = [('employee_id', '=', emp.id), ('holiday_status_id', '=', t.id), ('state', 'in', ['confirm', 'validate1', 'validate']), ('request_date_from', '>=', start)]
            if end:
                ldom.append(('request_date_from', '<=', end))
            lvs = Leave.search(ldom)
            ent = sum(al.mapped('number_of_days'))
            tk = sum([l.number_of_days for l in lvs if l.state == 'validate' and l.request_date_from <= today])
            pl = sum([l.number_of_days for l in lvs if l.state == 'validate' and l.request_date_from > today])
            rq = sum([l.number_of_days for l in lvs if l.state != 'validate'])
            out.append({'t': t, 'ent': ent, 'tk': tk, 'pl': pl, 'rq': rq, 'left': ent - tk - pl - rq, 'end': end, 'al': al})
        return out

    def req_data(emp):
        return sorted(Leave.search([('employee_id', '=', emp.id), ('state', 'in', ['confirm', 'validate1', 'validate', 'refuse']),
                                    ('request_date_to', '>=', datetime.date(today.year, 1, 1))]), key=lambda r: r.request_date_from, reverse=True)

    def amount(r):
        hourly = ('request_unit' in ltf and r.holiday_status_id.request_unit == 'hour') or (r.holiday_status_id.id in otypes.ids)
        return (hm(r.number_of_hours if 'number_of_hours' in lvf else 0) + ' ' + T['h']) if hourly else (dnum(r.number_of_days) + ' ' + (T['day'] if r.number_of_days == 1 else T['days']))

    def dates(r):
        return r.request_date_from.strftime('%d.%m.%Y') + ('' if r.request_date_to == r.request_date_from else ' – ' + r.request_date_to.strftime('%d.%m.%Y'))

    ST = {'validate': ('ok', 'Genehmigt' if de else 'Approved'), 'confirm': ('op', 'Offen – noch nicht genehmigt' if de else 'Open – not approved yet'),
          'validate1': ('op', 'Offen – 2. Genehmigung' if de else 'Open – second approval'), 'refuse': ('no', 'Abgelehnt' if de else 'Refused')}

    # ------------------------------------------------------------------ one person (employee view, or manager looking at an employee)
    def L_(model, rid, label, mgr):
        return olink(model, rid, label) if mgr else label

    def render_person(emp, mgr):
        od = ot_data(emp)
        vd = vac_data(emp)
        reqs = req_data(emp)
        n_open = len([r for r in reqs if r.state in ('confirm', 'validate1')])
        vleft = sum([v['left'] for v in vd])
        vend = ([v['end'] for v in vd if v['end']] or [False])[0]
        valid_txt = (T['valid'] + ' ' + vend.strftime('%d.%m.%Y')) if vend else ''
        kp = ('<div class="me-k">'
              + '<div class="kpi' + (' red' if od['bal'] < 0 else '') + '"><small>' + T['ot_rem'] + '</small><b>' + L_('hr.employee', emp.id, hm(od['bal'], True) + ' ' + T['h'], mgr) + '</b><span>' + today.strftime('%d.%m.%Y') + '</span></div>'
              + '<div class="kpi"><small>' + T['ot_earn'] + '</small><b>' + hm(od['earned']) + ' ' + T['h'] + '</b><span>&nbsp;</span></div>'
              + '<div class="kpi"><small>' + T['ot_used'] + '</small><b>' + hm(od['used']) + ' ' + T['h'] + '</b><span>&nbsp;</span></div>'
              + '<div class="kpi' + (' op' if n_open else '') + '"><small>' + T['vac_rem'] + '</small><b>' + dnum(vleft) + ' ' + (T['day'] if vleft == 1 else T['days']) + '</b><span>'
              + (('<span class="opn">' + str(n_open) + ' ' + T['open_s'] + '</span> · ') if n_open else '') + valid_txt + '</span></div></div>')
        rr = ''
        for r in reqs:
            cls, lab = ST[r.state]
            if r.state == 'validate':
                lab = lab + ' · ' + (T['planned'] if r.request_date_from > today else T['taken'])
            rr += ('<tr class="rq-' + cls + '"><td>' + L_('hr.leave', r.id, dates(r), mgr) + '</td><td>' + esc(r.holiday_status_id.name) + '</td><td class="r">' + amount(r)
                   + '</td><td class="r"><span class="st st-' + cls + '">' + lab + '</span></td></tr>')
        reqbox = ('<div class="box"><h3>' + T['allreq'] + ' ' + str(today.year) + '</h3>'
                  + ('<div class="note-op">' + T['open_note'].replace('%d', str(n_open)) + '</div>' if n_open else '')
                  + ('<table class="rqt"><tr><th>' + T['when'] + '</th><th>' + T['type'] + '</th><th class="r">' + T['amount'] + '</th><th class="r">Status</th></tr>' + rr + '</table>' if rr else '<p class="mut" style="margin:0">' + T['noreq'] + '</p>')
                  + '<div class="lgd"><span><i style="background:#16a34a"></i>' + ST['validate'][1] + '</span><span><i style="background:#f59e0b"></i>' + ('Offen' if de else 'Open') + '</span><span><i style="background:#dc2626"></i>' + ST['refuse'][1] + '</span></div></div>')
        calc = ('<div class="box"><h3>' + T['calc'] + '</h3><table>'
                + '<tr><td>' + T['earned'] + '</td><td class="r pos">' + hm(od['earned'], True) + '</td></tr>'
                + '<tr><td>' + T['used'] + '</td><td class="r neg">−' + hm(od['used'] - od['other']) + '</td></tr>'
                + ('<tr><td>' + T['other'] + '</td><td class="r ' + ('neg' if od['other'] > 0 else 'pos') + '">' + hm(-od['other'], True) + '</td></tr>' if abs(od['other']) >= 0.02 else '')
                + '<tr class="sum"><td>' + T['bal'] + '</td><td class="r">' + L_('hr.employee', emp.id, hm(od['bal'], True), mgr) + '</td></tr></table></div>')
        mrows = ''
        yy = today.year
        mm = today.month
        for i in range(12):
            p = sum([l['v'] for l in od['lines'] if l['v'] > 0 and l['d'].year == yy and l['d'].month == mm])
            n = sum([u['v'] for u in od['items'] if u['d'].year == yy and u['d'].month == mm])
            if p or n:
                mrows += '<tr><td>' + MONTHS_S[mm - 1] + ' ' + str(yy) + '</td><td class="r pos">' + (hm(p, True) if p else '–') + '</td><td class="r neg">' + ('−' + hm(n) if n else '–') + '</td></tr>'
            mm -= 1
            if mm == 0:
                mm = 12
                yy -= 1
        monbox = ('<div class="box"><h3>' + T['permonth'] + '</h3><table><tr><th>' + T['month'] + '</th><th class="r">' + T['plus'] + '</th><th class="r">' + T['minus'] + '</th></tr>' + mrows + '</table></div>')
        ul = ''.join(['<tr><td>' + L_(u['m'], u['id'], u['d'].strftime('%d.%m.%Y'), mgr) + '</td><td>' + esc(u['what']) + '</td><td class="r neg">−' + hm(u['v']) + '</td></tr>' for u in od['items']])
        usebox = '<div class="box"><h3>' + T['uselist'] + '</h3>' + ('<table>' + ul + '</table>' if ul else '<p class="mut" style="margin:0">' + T['nouse'] + '</p>') + '</div>'
        vac_html = ''
        for v in vd:
            alink = L_('hr.leave.allocation', v['al'][0].id, dnum(v['ent']), mgr) if len(v['al']) == 1 else dnum(v['ent'])
            vac_html += ('<div class="box"><h3>' + esc(v['t'].name) + (' · ' + T['valid'] + ' ' + v['end'].strftime('%d.%m.%Y') if v['end'] else '') + '</h3><table>'
                         + '<tr><td>' + T['ent'] + '</td><td class="r">' + alink + '</td></tr>'
                         + '<tr><td>' + T['taken'] + '</td><td class="r">' + dnum(v['tk']) + '</td></tr>'
                         + '<tr><td>' + T['planned'] + '</td><td class="r">' + dnum(v['pl']) + '</td></tr>'
                         + ('<tr><td>' + T['req'] + '</td><td class="r">' + dnum(v['rq']) + '</td></tr>' if v['rq'] else '')
                         + '<tr class="sum"><td>' + T['left'] + '</td><td class="r">' + dnum(v['left']) + ' ' + (T['day'] if v['left'] == 1 else T['days']) + '</td></tr></table></div>')
        if not vac_html:
            vac_html = '<div class="box"><h3>' + T['vac'] + '</h3><p class="mut" style="margin:0">' + T['novac'] + '</p></div>'
        top = ('<p class="hint" style="margin:0 0 10px">' + olink('hr.employee', emp.id, T['empform']) + '</p>') if mgr else ''
        return top + kp + reqbox + '<div class="me-g"><div class="col">' + calc + monbox + usebox + '</div><div class="col">' + vac_html + '</div></div>'

    # ------------------------------------------------------------------ manager: whole team on one page
    def render_team():
        allemp = Emp.search([], order='name asc')
        rows = []
        todo = []
        n_abs = 0
        n_neg = 0
        soon = []
        lim = today + datetime.timedelta(days=30)
        for e in allemp:
            od = ot_data(e)
            vd = vac_data(e)
            reqs = req_data(e)
            opn = [r for r in reqs if r.state in ('confirm', 'validate1')]
            todo += opn
            sick = sum([r.number_of_days for r in reqs if r.state == 'validate' and is_sick(r.holiday_status_id) and r.request_date_from.year == today.year])
            cur = [r for r in reqs if r.state == 'validate' and r.request_date_from <= today <= r.request_date_to]
            nxt = sorted([r for r in reqs if r.state in ('validate', 'confirm', 'validate1') and r.request_date_from > today], key=lambda r: r.request_date_from)
            for r in reqs:
                if r.state in ('validate', 'confirm', 'validate1') and r.request_date_to >= today and r.request_date_from <= lim:
                    soon.append(r)
            if cur:
                n_abs += 1
            if od['bal'] < 0:
                n_neg += 1
            vleft = sum([v['left'] for v in vd])
            vent = sum([v['ent'] for v in vd])
            vtk = sum([v['tk'] for v in vd])
            alloc1 = [v['al'][0] for v in vd if len(v['al']) == 1]
            dnm = '?view=me&amp;key=' + KEY + '&amp;emp=' + str(e.id) + ('' if de else '&amp;lang=en')
            if cur:
                absc = '<span class="st ' + ('st-sick' if is_sick(cur[0].holiday_status_id) else 'st-ok') + '">' + olink('hr.leave', cur[0].id, esc(cur[0].holiday_status_id.name) + ' ' + T['today']) + '</span>'
            elif nxt:
                absc = olink('hr.leave', nxt[0].id, nxt[0].request_date_from.strftime('%d.%m.') + ' ' + esc(nxt[0].holiday_status_id.name)) + (' <span class="st st-op">?</span>' if nxt[0].state != 'validate' else '')
            else:
                absc = '<span class="mut">–</span>'
            rows.append((0 if opn else 1, e.name, '<tr' + (' class="warn"' if opn else '') + '><td><a class="nm" href="' + dnm + '">' + esc(e.name) + '</a></td>'
                         + '<td class="r ' + ('neg' if od['bal'] < 0 else '') + '">' + olink('hr.employee', e.id, hm(od['bal'], True)) + '</td>'
                         + '<td class="r">' + (olink('hr.leave.allocation', alloc1[0].id, dnum(vleft) + ' / ' + dnum(vent)) if alloc1 else (dnum(vleft) + ' / ' + dnum(vent) if vd else '<span class="mut">–</span>')) + '</td>'
                         + '<td class="r">' + (dnum(vtk) if vd else '–') + '</td>'
                         + '<td class="r">' + (''.join([olink('hr.leave', r.id, '<span class="st st-op">' + r.request_date_from.strftime('%d.%m.') + '</span>') + ' ' for r in opn]) if opn else '<span class="mut">–</span>') + '</td>'
                         + '<td class="r">' + (dnum(sick) if sick else '<span class="mut">0</span>') + '</td>'
                         + '<td>' + absc + '</td></tr>'))
        rows = sorted(rows, key=lambda x: (x[0], x[1]))
        kp = ('<div class="me-k">'
              + '<div class="kpi"><small>' + T['k_emp'] + '</small><b>' + str(len(allemp)) + '</b><span>&nbsp;</span></div>'
              + '<div class="kpi' + (' op' if todo else '') + '"><small>' + T['k_open'] + '</small><b>' + str(len(todo)) + '</b><span>' + T['todo'] + '</span></div>'
              + '<div class="kpi"><small>' + T['k_absent'] + '</small><b>' + str(n_abs) + '</b><span>&nbsp;</span></div>'
              + '<div class="kpi' + (' red' if n_neg else '') + '"><small>' + T['k_neg'] + '</small><b>' + str(n_neg) + '</b><span>' + T['ot_rem'] + '</span></div></div>')
        td = ''.join(['<tr class="rq-op"><td>' + esc(r.employee_id.name) + '</td><td>' + olink('hr.leave', r.id, dates(r)) + '</td><td>' + esc(r.holiday_status_id.name)
                      + '</td><td class="r">' + amount(r) + '</td><td class="r"><span class="st st-op">' + ST[r.state][1] + '</span></td></tr>' for r in sorted(todo, key=lambda r: r.request_date_from)])
        todobox = ('<div class="box"><h3>' + T['todo'] + '</h3>' + ('<table class="rqt"><tr><th>' + T['employee'] + '</th><th>' + T['when'] + '</th><th>' + T['type'] + '</th><th class="r">' + T['amount'] + '</th><th class="r">Status</th></tr>' + td + '</table>' if td else '<p class="mut" style="margin:0">' + T['nothing'] + '</p>') + '</div>')
        teambox = ('<div class="box team" style="margin-top:14px"><h3>' + T['team'] + '</h3><table><tr><th>' + T['employee'] + '</th><th class="r">' + T['ot_rem'] + '</th><th class="r">' + T['vac_rem'] + ' / ' + T['ent'] + '</th><th class="r">' + T['taken']
                   + '</th><th class="r">' + T['k_open'] + '</th><th class="r">' + T['sick'] + ' ' + str(today.year) + '</th><th>' + T['absnow'] + '</th></tr>' + ''.join([x[2] for x in rows]) + '</table>'
                   + '<p class="hint">' + T['hint'] + '</p></div>')
        sb = ''
        for r in sorted(soon, key=lambda r: r.request_date_from):
            cls = 'op' if r.state != 'validate' else ('sick' if is_sick(r.holiday_status_id) else 'ok')
            sb += ('<tr' + (' class="rq-op"' if cls == 'op' else '') + '><td>' + esc(r.employee_id.name) + '</td><td>' + olink('hr.leave', r.id, dates(r)) + '</td><td><span class="st st-' + cls + '">' + esc(r.holiday_status_id.name)
                   + (' · ' + T['open_s'] if cls == 'op' else '') + '</span></td><td class="r">' + amount(r) + '</td></tr>')
        soonbox = '<div class="box" style="margin-top:14px"><h3>' + T['next30'] + '</h3>' + ('<table class="rqt">' + sb + '</table>' if sb else '<p class="mut" style="margin:0">' + T['noabs'] + '</p>') + '</div>'
        return kp + todobox + teambox + soonbox

    # ------------------------------------------------------------------ routing
    if params.get('melogout'):
        response = request.make_response('', headers=[('Location', base)], status=303)
        response.delete_cookie('iq_emp')
    elif request.httprequest.method == 'POST' and params.get('pin') is not None:
        who = str(params.get('emp') or '')
        pin_in = (params.get('pin') or '').strip()
        fkey = 'iq.cal_pinfail.' + (who if (who.isdigit() or who == 'M') else '0')
        fv = (ICP.get_param(fkey) or '0|0').split('|')
        fails = int(fv[0]) if fv[0].isdigit() else 0
        fts = int(fv[1]) if len(fv) > 1 and fv[1].isdigit() else 0
        emp = Emp.browse(int(who)).exists() if who.isdigit() else Emp
        good = (who == 'M' and MPIN and pin_in == MPIN) or (emp and emp.pin and pin_in == emp.pin)
        if fails >= 5 and nowts - fts < 900:
            response = html_resp(shell(picker(T['locked']), '', False))
        elif good:
            ICP.set_param(fkey, False)
            exp = nowts + SESSION
            wid = 'M' if who == 'M' else str(emp.id)
            response = request.make_response('', headers=[('Location', me_url)], status=303)
            response.set_cookie('iq_emp', wid + '.' + str(exp) + '.' + sig(wid, MPIN if who == 'M' else emp.pin, exp), max_age=SESSION, httponly=True, secure=True, samesite='Lax')
        else:
            if who.isdigit() or who == 'M':
                ICP.set_param(fkey, str((0 if nowts - fts >= 900 else fails) + 1) + '|' + str(nowts))
            response = html_resp(shell(picker(T['wrong']), '', False))
    else:
        cv = (request.httprequest.cookies.get('iq_emp') or '').split('.')
        emp = Emp
        mgr = False
        if len(cv) == 3 and cv[1].isdigit() and int(cv[1]) >= nowts:
            if cv[0] == 'M' and MPIN and sig('M', MPIN, int(cv[1])) == cv[2]:
                mgr = True
            elif cv[0].isdigit():
                cand = Emp.browse(int(cv[0])).exists()
                if cand and cand.pin and sig(str(cand.id), cand.pin, int(cv[1])) == cv[2]:
                    emp = cand
        if mgr:
            pe = str(params.get('emp') or '')
            target = Emp.browse(int(pe)).exists() if pe.isdigit() else Emp
            if target:
                response = html_resp(shell(render_person(target, True), target.name, True, True))
            else:
                response = html_resp(shell(render_team(), '*', True))
        elif emp:
            response = html_resp(shell(render_person(emp, False), emp.name, True))
        else:
            response = html_resp(shell(picker(''), '', False))
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
        'pend': 'offen' if de else 'open', 'pend_t': 'Beantragt, noch nicht genehmigt' if de else 'Requested, not approved yet',
        'appr': 'Genehmigt' if de else 'Approved',
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
    for lv in env['hr.leave'].sudo().search([('state', 'in', ['validate', 'confirm', 'validate1']), ('request_date_from', '<=', max(gend, today)), ('request_date_to', '>=', min(gstart, today))], order='request_date_from asc'):
        parts = (lv.employee_id.name or '').split()
        nm = parts[0] + (' ' + parts[-1][0] + '.' if len(parts) > 1 else '') if parts else ''
        ini = (parts[0][0] + (parts[-1][0] if len(parts) > 1 else '')).upper() if parts else '?'
        if nm not in people:
            people.append(nm)
        absn.append({'n': nm, 'i': ini, 'a': lv.request_date_from, 'b': lv.request_date_to or lv.request_date_from, 'p': lv.state != 'validate'})
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
            for a in sorted(absn, key=lambda a: a['p']):
                if a['a'] <= d <= a['b']:
                    out += ('<div class="ab pend" title="' + L['pend_t'] + '">' + av(a) + esc(a['n']) + ' ?</div>') if a['p'] else ('<div class="ab">' + av(a) + esc(a['n']) + '</div>')
        return out

    # KPIs
    tday = [x for x in ev if x['d'] == today]
    mev = [x for x in ev if first <= x['d'] <= last]
    odl = [x for x in ev if x['d'] < today]
    absnow = [a for a in absn if a['a'] <= today <= a['b'] and today.weekday() < 5 and not a['p']]
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
    cur = sorted([a for a in absn if a['a'] <= last and a['b'] >= first], key=lambda a: a['a'])
    s.append('<div class="box"><h3>' + L['abs'] + MONTHS[m - 1] + '</h3>')
    if not cur:
        s.append('<p class="mut" style="margin:0">' + L['noabs'] + '</p>')
    for a in cur:
        isnow = a['a'] <= today <= a['b'] and not a['p']
        s.append('<div class="row' + (' now' if isnow else '') + (' pend' if a['p'] else '') + '"><span>' + av(a) + ' ' + esc(a['n']) + (' <span class="tag">' + L['now'] + '</span>' if isnow else '') + (' <span class="tag pend">' + L['pend'] + '</span>' if a['p'] else '') + '</span><b>'
                 + a['a'].strftime('%d.%m.') + (' &ndash; ' + a['b'].strftime('%d.%m.') if a['b'] != a['a'] else '') + '</b></div>')
    if [a for a in cur if a['p']]:
        s.append('<div class="lgd"><span><i style="background:#475569"></i>' + L['appr'] + '</span><span><i style="background:#fff4e5;border:1px dashed #f59e0b"></i>' + L['pend_t'] + '</span></div>')
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
            + '<a href="' + link(today) + '">' + L['today'] + '</a><a href="?key=' + KEY + '&amp;view=me' + ('' if de else '&amp;lang=en') + '" style="background:#a51d1b;border-color:#a51d1b">' + ('Meine Stunden &amp; Urlaub' if de else 'My hours &amp; vacation') + '</a><a href="' + langlink + '">' + ('EN' if de else 'DE') + '</a></nav></div></div>'
            + '<div class="wrap">' + ''.join(k) + '<main><div>' + ''.join(g) + ''.join(ag) + '</div>' + ''.join(s) + '</main></div>'
            + '<footer><span>' + L['upd'] + ': ' + datetime.datetime.now().strftime('%d.%m.%Y %H:%M') + ' UTC</span><a href="?key=' + KEY + '&amp;logout=1">' + L['logout'] + '</a></footer></body></html>')
    response = request.make_response(html, headers=[('Content-Type', 'text/html; charset=utf-8'), ('X-Robots-Tag', 'noindex'), ('Cache-Control', 'no-store')])
'''

SA = env['ir.actions.server'].sudo()
cal = SA.search([('name', '=', 'IQ Public delivery calendar')], limit=1)
if not cal:
    raise UserError('IQ Public delivery calendar not found – nothing was changed.')
cal.write({'code': PAGE})

ICP = env['ir.config_parameter'].sudo()
mp = (ICP.get_param('iq.delivery_calendar_manager_pin') or '').strip()
OTM = 'hr.attendance.overtime.line' if 'hr.attendance.overtime.line' in env else ('hr.attendance.overtime' if 'hr.attendance.overtime' in env else 'NONE')
fg = env[OTM].sudo().fields_get() if OTM != 'NONE' else {}
dfield = 'manual_duration' if 'manual_duration' in fg else ('duration' if 'duration' in fg else 'NONE')
LT = env['hr.leave.type'].sudo()
ot_types = LT.search([('overtime_deductible', '=', True)]).mapped('name') if 'overtime_deductible' in LT.fields_get() else []
pins = env['hr.employee'].sudo().search_count([('pin', '!=', False)])
nopin = env['hr.employee'].sudo().search([('pin', '=', False)]).mapped('name')
log('IQ my-hours installed | manager PIN: ' + ('OK' if len(mp) >= 8 else ('TOO SHORT – needs 8+ digits' if mp else 'NOT SET – add system parameter iq.delivery_calendar_manager_pin'))
    + ' | overtime model: ' + OTM + ' / field: ' + dfield + ' / status filter: ' + ('yes' if 'status' in fg else 'no')
    + ' | overtime time-off types: ' + (', '.join(ot_types) or 'none')
    + ' | employees with PIN: ' + str(pins) + ' | without PIN: ' + (', '.join(nopin) or 'none'))
