# IQ Warehouse & team calendar – update 23.11.2026: "Ware angekommen" made simple + admins notice at once
#  - header responsive at every width: buttons stay in ONE row and swipe/scroll sideways instead of breaking into new lines;
#    wide screens: page uses the full width (fluid) and logo + buttons share ONE line -> bigger calendar;
#    on phones: one slim line (month, arrows, Heute) + the swipe row of buttons
#  - search in "Ware angekommen" also finds products WITHOUT an order -> "Ohne Bestellung melden: <product>" (product prefilled)
#  - goods without order: only name + product + quantity + photo of the delivery note; supplier is OPTIONAL
#    (supplier, delivery note no., boxes, note are under "Mehr (optional)")
#  - every report moves the Goods Receipt card to the column "Ware angekommen" (needs
#    fix_2026-11-23_goods_receipts_arrived_column.py) and creates a To-Do in Odoo
#    (goes to the Settings admins by default; or set system parameter iq.arrival_notify_logins = login1,login2)
#  - without order the card gets the product + counted pieces (shown on the card)
#  - hand scanner works everywhere in "Ware angekommen": product without order = scan -> product filled in, +1 counted
#    (packaging barcode = its quantity); delivery with order = +1 at the right size; list = scan to search.
#    Service products (fees, advertising …) no longer appear in the product list.
#  - after saving: one clear screen "Gemeldet – die Ware ist im Lager" (no QC link); no role words (manager etc.) on these pages;
#    open orders that may fit are only shown as a hint (no tick box needed any more)
#  - "My hours & vacation": button "Abwesenheit beantragen" -> normal Odoo Time Off request (type with balance, Extra Hours with
#    available hours, dates, morning/afternoon or hours, description, optional file) -> To Approve -> Second Approval -> Approved;
#    open requests can be withdrawn ("Zurückziehen"). Only the types IQ uses are offered, as icon tiles: Vacation (with days left),
#    Extra Hours (hours available), Sick Time Off, Unpaid (other list: system parameter iq.timeoff_types). No new fields.
#  - header: logo left; month controls (← November →, Heute) + action buttons together on the RIGHT, thin divider between them
#  - list "Welche Lieferung ist angekommen?" no longer shows planned deliveries that are already booked (same rule as calendar)
# IQ Warehouse & team calendar – update 20.11.2026 (d): planned deliveries that are already BOOKED in Odoo no longer show as
#  "overdue / not arrived": the received quantity of the purchase order is matched to its planned deliveries (oldest first);
#  partly covered -> only the rest is shown. Contains everything of (b) and (c): goods arrival + real icons.
# IQ Warehouse & team calendar – update 20.11.2026 (b): "📦 Ware angekommen" for the warehouse (team password + name)
#  - big button in the calendar header + "📦 Angekommen?" under every delivery that is due (today, overdue, next 3 days)
#  - list of all expected deliveries (search) -> one delivery: name, photo/PDF of the delivery note (+ no.), per size quantity
#    on the delivery note + counted (difference shown at once), boxes, note -> saved on the Goods Receipt card, the purchase order
#    and the open receipt (chatter + files). NOTHING is booked or changed in the receipt quantities (booking after QC).
#  - "Ware ohne Bestellung melden": first shows open orders / planned deliveries of that supplier or product (avoid duplicates);
#    only after ticking "gehört zu keiner Bestellung" a Goods Receipt card "Ohne Bestellung" is created (supplier, delivery note no.,
#    products, counts, files). Managers see it red in the calendar and on the manager dashboard ("Bestellung anlegen");
#    a purchase order with vendor reference = delivery note no. is linked automatically (existing automation).
#  - calendar: arrived = amber entry, without PO = red entry; arrived orders are no longer shown as overdue / expected.
#  - header redesigned for phones. No new fields (arrival report = small text file on the card).
# IQ Warehouse & team calendar – update 20.11.2026: link "QC Dashboard" in the calendar's top menu (opens the QC Dashboard page).
#  Nothing else changed. Manager login is shared with the QC page (log in on one page = logged in on both).
# IQ Warehouse & team calendar – update 19.11.2026: managers can ADD planned deliveries right in the calendar
#  - "+ Lieferung eintragen" button (and a small + in every day) -> manager PIN (same as "Meine Stunden & Urlaub -> Führungskraft / Manager")
#  - form: date, quantity, purchase order (optional, supplier/order no./products filled from the order), supplier, supplier order no., product, note
#  - saved as a "Delivery schedule" line on the Goods Receipt card of that order (card created if missing; without PO a card with supplier + order no.)
#  - a note is written in the card's chatter and in the purchase order's chatter (who/what/when)
#  - managers see "✎ Bearbeiten" under planned entries: change date/quantity, "✓ Angekommen" or delete
#  - partial deliveries: one entry per partial delivery (own date + quantity)
#  - everyone else only sees the entries. No new fields.
# Earlier update 17.11.2026: calendar entries open the GOODS RECEIPT card (Goods Receipts app), not the purchase order
#  - month view entries, "Overdue – not arrived" box, monthly delivery list and search results link to the Goods Receipt card of the order
#  - opens inside the Goods Receipts app (its own window action); if an order has no card yet, it still opens the purchase order
# Includes everything from 09.–13.11 (dashboard, invoices, reminder stages). Changes only the server action "IQ Public delivery calendar". No new fields.
# Run once: Scheduled Action (Model: Contact, Active = off) -> paste -> Save -> Run Manually.
# Afterwards check Settings -> Technical -> Logging, search "IQ calendar 23.11".

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
# 19.11.2026: managers (manager PIN session, 10 min) may add / edit planned deliveries in the calendar
ADM = False
MPIN0 = (P.get_param('iq.delivery_calendar_manager_pin') or '').strip()
cv0 = (request.httprequest.cookies.get('iq_emp') or '').split('.') if request else []
nowts0 = int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds())
if len(MPIN0) >= 8 and len(cv0) == 3 and cv0[0] == 'M' and cv0[1].isdigit() and int(cv0[1]) >= nowts0:
    x0 = 2166136261
    for ch in (KEY + '|' + PW + '|M|' + MPIN0 + '|' + cv0[1]):
        x0 = ((x0 ^ ord(ch)) * 16777619) % 4294967296
    y0 = 2166136261
    for ch in (cv0[1] + '#' + MPIN0 + '#' + PW + '#M'):
        y0 = ((y0 ^ ord(ch)) * 16777619) % 4294967296
    ADM = ('%08x%08x' % (x0, y0)) == cv0[2]
TITLE = 'Lager- &amp; Teamkalender' if de else 'Warehouse &amp; team calendar'
# 20.11.2026: arrival reports ("Ware angekommen") are stored as a small text file on the Goods Receipt card (no new fields)
ATT = env['ir.attachment'].sudo()
ARRPRE = 'Wareneingang-Meldung '


def arr_int(x):
    x = str(x or '').strip()
    return int(x) if x.isdigit() else 0


def arr_parse(a):
    try:
        first = (a.raw or b'').decode('utf-8', 'ignore').split(chr(10), 1)[0]
    except Exception:
        return False
    pr = first.split('|')
    if len(pr) < 12 or pr[0] != 'IQ-ARRIVAL':
        return False
    return {'att': a.id, 'wid': a.res_id, 'ts': arr_int(pr[1]), 'who': pr[2], 'pick': arr_int(pr[3]), 'lid': arr_int(pr[4]), 'boxes': pr[5], 'lsno': pr[6],
            'ls': arr_int(pr[7]), 'cnt': arr_int(pr[8]), 'ord': arr_int(pr[9]), 'prod': pr[10], 'po': arr_int(pr[11])}


def arr_date(ts):
    return (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=ts, hours=1)).date()


def arr_records(days):
    out = []
    lim = datetime.datetime.now() - datetime.timedelta(days=days)
    for a in ATT.search([('res_model', '=', 'x_wareneingang'), ('name', '=like', ARRPRE + '%'), ('create_date', '>=', lim)], order='id'):
        r = arr_parse(a)
        if r:
            out.append(r)
    return out


ICB = '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 8l-9-5-9 5v8l9 5 9-5z"/><path d="M3 8l9 5 9-5"/><path d="M12 13v8"/></svg>'
ICC = '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/></svg>'
ICW = '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3L2 21h20z"/><path d="M12 10v5"/><path d="M12 18h.01"/></svg>'
ICK = '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5L20 7"/></svg>'
ACSS = ('<style>[hidden]{display:none!important}.ic{width:1.15em;height:1.15em;vertical-align:-.2em;margin-right:.35em;flex:none}.af{max-width:640px;margin:14px auto;padding:0 12px 40px}.af .box{padding:14px 16px;margin-bottom:12px}.af h2{margin:0 0 10px;font:800 17px Arial;display:flex;align-items:center;gap:8px}'
        '.sn{display:inline-flex;width:26px;height:26px;border-radius:50%;background:#151515;color:#fff;font:800 14px Arial;align-items:center;justify-content:center;flex:0 0 26px}'
        '.af input,.af textarea{width:100%;padding:12px;border:1px solid #d1d5db;border-radius:8px;font-size:17px;background:#fff}.af textarea{min-height:70px}'
        '.af label.l{display:block;font:700 13px Arial;margin:10px 0 4px}.hint{color:var(--mut);font-size:13px;margin:0 0 8px}'
        '.whob{border:3px solid #dc2626;background:#fef2f2}.whob.ok{border:1px solid var(--line);background:#fff}.whob.ok .whoi{display:none}.whob .whol{display:none;align-items:center;gap:8px;font-weight:800}'
        '.whob.ok .whol{display:flex}.whob.ok h2{display:none}.whol i{display:inline-flex;width:24px;height:24px;border-radius:50%;background:#16a34a;color:#fff;font-style:normal;align-items:center;justify-content:center}'
        '.whol a{margin-left:auto;font-weight:400;font-size:13px;color:#555}'
        '.fbtn{display:block;width:100%;padding:16px;border:2px dashed #151515;border-radius:10px;background:#fafaf8;font:800 16px Arial;cursor:pointer;text-align:center}'
        '.ths{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}.ths span{position:relative}.ths img{width:84px;height:84px;object-fit:cover;border-radius:8px;border:1px solid #ddd}.ths .pdf{display:flex;width:84px;height:84px;align-items:center;justify-content:center;border:1px solid #ddd;border-radius:8px;font:800 13px Arial;background:#fff}'
        '.ths button{position:absolute;top:-6px;right:-6px;width:24px;height:24px;border-radius:50%;border:0;background:#dc2626;color:#fff;font-weight:800}'
        '.qhead,.qr,.qtot,.nhead,.nrow{display:grid;grid-template-columns:1fr 92px 92px 56px;gap:6px;align-items:center}.nhead,.nrow{grid-template-columns:1fr 92px 92px}'
        '.qhead span,.nhead span{font:700 10px/1.2 Arial;letter-spacing:.5px;text-transform:uppercase;color:var(--mut);text-align:center}.qhead span:first-child,.nhead span:first-child{text-align:left}'
        '.qr{padding:6px 0;border-top:1px solid var(--line)}.qn{font-weight:800;font-size:15px}.qn small{display:block;font-weight:400;color:var(--mut);font-size:12px}'
        '.qr input,.nrow input{padding:10px 6px;text-align:center;font-size:18px}.nrow input:first-child{text-align:left}.nrow{margin-bottom:6px}'
        '.qd{text-align:right;font-size:13px}.qd.m{color:#dc2626}.qd.p{color:#d97706}.qd.ok{color:#16a34a}.tg{font:800 12px Arial;letter-spacing:.5px;text-transform:uppercase;color:#555;margin:12px 0 2px}'
        '.qtot{border-top:2px solid #151515;padding-top:8px;margin-top:4px;font-weight:800}.qtot b{text-align:center}'
        '.b{display:inline-block;padding:11px 14px;border:1px solid #d1d5db;border-radius:8px;background:#fff;font:700 14px Arial;text-decoration:none;color:#111;cursor:pointer}.b.add{margin-top:10px;width:100%}'
        '.save{display:block;width:100%;padding:18px;border:0;border-radius:12px;background:#16a34a;color:#fff;font:800 19px Arial;cursor:pointer;margin-top:6px}.save.red{background:#b91c1c}.save:disabled{opacity:.6}'
        '.err{background:#fef2f2;border:1px solid #fca5a5;color:#991b1b;border-radius:8px;padding:10px 12px;font-weight:700}'
        '.ahead b{display:block;font:800 18px Arial}.ahead span{display:block;color:var(--mut);font-size:13px}.ahead .prev{color:#166534;font-weight:700}'
        '.lst{margin-top:10px}.it{display:flex;justify-content:space-between;gap:10px;padding:12px 4px;border-top:1px solid var(--line);text-decoration:none;color:inherit;align-items:center}'
        '.it .l b{display:block;font-size:15px}.it .l small{color:var(--mut)}.it .r{text-align:right;white-space:nowrap}.it .r b{display:block;font-size:17px}'
        '.st{display:inline-block;font:700 11px Arial;border-radius:5px;padding:2px 7px;background:#e5e7eb;margin-top:2px}.st.od{background:#fde8e8;color:#991b1b}.st.td{background:#dcfce7;color:#166534}'
        '.nopo{display:block;background:#fff7ed;border:2px solid #f59e0b;border-radius:10px;padding:14px 16px;text-decoration:none;color:#7c2d12}.nopo small{display:block;margin-top:2px}'
        '.match{background:#fffbeb;border:2px solid #f59e0b;border-radius:10px;padding:12px;margin-top:10px}.match b{display:block;margin-bottom:6px;color:#92400e}'
        '.match a{display:flex;justify-content:space-between;gap:8px;padding:10px;border-radius:8px;background:#fff;border:1px solid #f6d28b;margin-top:6px;text-decoration:none;color:#111;font-weight:700}'
        '.match a small{display:block;font-weight:400;color:var(--mut)}.chk{display:flex;gap:8px;align-items:flex-start;background:#fff7ed;border:1px solid #f59e0b;border-radius:8px;padding:12px;margin:0 0 10px;font-weight:700}.chk input{width:22px;height:22px;flex:0 0 22px}'
        '.adone{text-align:center;padding:26px 16px!important}.adone .big{font:900 54px Arial;color:#16a34a}.adone.warn .big{color:#d97706}.adone .btns{display:flex;flex-direction:column;gap:8px;margin-top:14px}.adone .go{background:#16a34a;color:#fff;border-color:#16a34a}'
        '.anav a{white-space:nowrap}@media(max-width:560px){.qhead,.qr,.qtot{grid-template-columns:1fr 70px 70px 40px}.nhead,.nrow{grid-template-columns:1fr 70px 70px}.qr input,.nrow input{font-size:16px;padding:9px 4px}.top .in{padding:10px 12px}.brand p{display:none}}</style>')

WHO_HTML = ('<div class="box whob" id="whob"><h2><span class="sn" style="background:#dc2626">1</span>' + ('Wer meldet? Bitte deinen Namen eingeben' if de else 'Who is reporting? Please enter your name') + '</h2>'
            '<input class="whoi" name="who" id="who" autocomplete="off" placeholder="' + ('Dein Name – Pflichtfeld' if de else 'Your name – required') + '">'
            '<div class="whol"><i>✓</i><span id="whon"></span><a href="#" id="whoe">' + ('ändern' if de else 'change') + '</a></div></div>')
LS_HTML = ('<div class="box"><h2><span class="sn">2</span>' + ('Lieferschein' if de else 'Delivery note') + '</h2>'
           '<input type="file" id="files" accept="image/*,application/pdf" multiple hidden><button type="button" class="fbtn" id="fbtn">' + ICC + ('Lieferschein fotografieren / PDF wählen' if de else 'Photograph delivery note / choose PDF') + '</button>'
           '<div class="ths" id="ths"></div><label class="l">' + ('Lieferschein-Nr. (optional)' if de else 'Delivery note no. (optional)') + '</label><input name="lsno" autocomplete="off" placeholder="z. B. LS 2026-344819"></div>')
MORE_HTML = ('<div class="box"><h2><span class="sn">4</span>' + ('Kartons und Notiz' if de else 'Boxes and note') + ' <small class="hint" style="margin:0">(optional)</small></h2>'
             '<label class="l">' + ('Anzahl Kartons / Paletten' if de else 'Number of boxes / pallets') + '</label><input name="boxes" autocomplete="off" inputmode="numeric" placeholder="z. B. 12 Kartons">'
             '<label class="l">' + ('Notiz' if de else 'Note') + '</label><textarea name="note" placeholder="' + ('z. B. 2 Kartons beschädigt' if de else 'e.g. 2 boxes damaged') + '"></textarea></div>')
ARR_JS = r"""
(function(){
  var F=document.getElementById('af'),W=document.getElementById('who'),WB=document.getElementById('whob'),E=document.getElementById('aerr'),FILES=[];
  function ls(k,v){try{if(v===undefined)return localStorage.getItem(k)||'';localStorage.setItem(k,v)}catch(e){return ''}}
  function whoUi(){var ok=!!W.value.trim();WB.classList.toggle('ok',ok&&!WB.classList.contains('ed'));document.getElementById('whon').textContent=(DE?'Gemeldet von: ':'Reported by: ')+W.value.trim()}
  W.value=ls('iq_qc_who');whoUi();
  W.onchange=function(){ls('iq_qc_who',W.value.trim());if(W.value.trim())WB.classList.remove('ed');whoUi()};
  W.onkeydown=function(e){if(e.key==='Enter'){e.preventDefault();W.blur();W.onchange()}};
  document.getElementById('whoe').onclick=function(e){e.preventDefault();WB.classList.add('ed');WB.classList.remove('ok');W.focus()};
  function say(t){E.textContent=t;E.hidden=!t;if(t&&E.scrollIntoView)E.scrollIntoView({block:'center'})}
  var fi=document.getElementById('files');
  document.getElementById('fbtn').onclick=function(){fi.click()};
  function thumbs(){var b=document.getElementById('ths');b.innerHTML='';FILES.forEach(function(f,i){var s=document.createElement('span');
    if(f.type.indexOf('pdf')>=0){var d=document.createElement('div');d.className='pdf';d.textContent='PDF';s.appendChild(d)}else{var im=document.createElement('img');im.src=URL.createObjectURL(f);s.appendChild(im)}
    var x=document.createElement('button');x.type='button';x.textContent='✕';x.onclick=function(){FILES.splice(i,1);thumbs()};s.appendChild(x);b.appendChild(s)});
    document.getElementById('fbtn').innerHTML=ICC+(FILES.length?((DE?'weiteres Foto / PDF':'another photo / PDF')+' ('+FILES.length+')'):(DE?'Lieferschein fotografieren / PDF wählen':'Photograph delivery note / choose PDF'))}
  function compress(f){return new Promise(function(res){if(f.type.indexOf('image/')!==0){res(f);return}var im=new Image(),u=URL.createObjectURL(f);
    im.onload=function(){try{var mx=2000,sc=Math.min(1,mx/Math.max(im.width,im.height)),c=document.createElement('canvas');c.width=Math.round(im.width*sc);c.height=Math.round(im.height*sc);
      c.getContext('2d').drawImage(im,0,0,c.width,c.height);URL.revokeObjectURL(u);c.toBlob(function(b){res(b?new File([b],'lieferschein.jpg',{type:'image/jpeg'}):f)},'image/jpeg',0.85)}catch(e){res(f)}};
    im.onerror=function(){res(f)};im.src=u})}
  fi.onchange=function(){var fs=[].slice.call(fi.files||[]);fi.value='';Promise.all(fs.map(compress)).then(function(r){FILES=FILES.concat(r);thumbs()})};
  window.arrSend=function(extra){
    if(!W.value.trim()){WB.classList.remove('ok');WB.classList.add('ed');say(DE?'Bitte zuerst deinen Namen eingeben (oben).':'Please enter your name first (top).');W.focus();return}
    var fd=new FormData(F);fd.delete('files');fd.append('csrf_token',CSRF);fd.append('key',KEY);fd.append('arr','1');fd.append('act',ACT);fd.set('who',W.value.trim());
    FILES.forEach(function(f){fd.append('files',f,f.name||'lieferschein.jpg')});
    var bt=document.getElementById('asave'),t0=bt.textContent;bt.disabled=true;bt.textContent=DE?'Speichert …':'Saving …';say('');
    fetch(location.pathname,{method:'POST',body:fd,credentials:'same-origin'}).then(function(r){return r.text()}).then(function(t){var a=t.split('|');
      if(a[0]==='OK'){location.href=BQ+'&arr=done&w='+a[1]}else{bt.disabled=false;bt.textContent=t0;say(a[1]||t)}})
    .catch(function(){bt.disabled=false;bt.textContent=t0;say(DE?'Keine Verbindung – bitte nochmal.':'No connection – please try again.')})};
})();
"""
QTY_JS = r"""
(function(){
  function v(i){return i.value===''?null:Math.max(0,parseInt(i.value,10)||0)}
  function upd(){var tl=0,tc=0,to=0,any=false;document.querySelectorAll('.qr').forEach(function(r){var o=+r.dataset.o||0,l=v(r.querySelector('.qls')),c=v(r.querySelector('.qcn')),d=r.querySelector('.qd');
    if(l!==null)tl+=l;if(c!==null)tc+=c;var ref=l!==null?l:(c!==null?o:null);
    if(c===null&&l===null){d.textContent='';d.className='qd'}else if(c===null){d.textContent='?';d.className='qd'}else{any=true;var df=c-(l!==null?l:o);d.textContent=df===0?'✓':(df>0?'+'+df:String(df));d.className='qd '+(df===0?'ok':(df>0?'p':'m'))}});
    document.getElementById('tls').textContent=tl;document.getElementById('tcn').textContent=tc;var tdf=document.getElementById('tdf');
    if(tl&&tc){var x=tc-tl;tdf.textContent=x===0?'✓':(x>0?'+'+x:String(x));tdf.className=x===0?'qd ok':(x>0?'qd p':'qd m')}else tdf.textContent=''}
  document.querySelectorAll('.qr input').forEach(function(i){i.oninput=upd});
  iqScan(BQ,DE,function(r){var i=document.querySelector('.qcn[data-pid="'+r.pid+'"]');
    if(!i){iqToast(r.name+(DE?' – gehört nicht zu dieser Lieferung':' – not part of this delivery'),false);return}
    i.value=(parseInt(i.value||'0',10)||0)+r.qty;i.dispatchEvent(new Event('input'));i.closest('.qr').scrollIntoView({block:'center'});
    iqToast(r.name+' · '+(DE?'gezählt ':'counted ')+i.value,true)});
  document.getElementById('fillo').onclick=function(){document.querySelectorAll('.qr').forEach(function(r){var i=r.querySelector('.qls');if(i.value===''&&+r.dataset.o)i.value=r.dataset.o});upd()};
  document.getElementById('asave').onclick=function(){var any=false;document.querySelectorAll('.qr input').forEach(function(i){if(i.value!=='')any=true});
    var miss=[];document.querySelectorAll('.qr').forEach(function(r){if(r.querySelector('.qls').value!==''&&r.querySelector('.qcn').value==='')miss.push(1)});
    if(miss.length&&!confirm(DE?(miss.length+' Größe(n) haben eine Lieferschein-Menge, aber noch keine Zählung. Trotzdem speichern?'):(miss.length+' size(s) have a delivery note quantity but no count yet. Save anyway?')))return;
    window.arrSend()};
  upd();
})();
"""
SCAN_JS = r"""
window.iqScan=function(BQ,DE,cb){
  var buf='',last=0,tm=null,tb=null;
  function toast(t,ok){if(!tb){tb=document.createElement('div');tb.style.cssText='position:fixed;left:12px;right:12px;bottom:16px;z-index:99;padding:14px 16px;border-radius:12px;font:700 16px Arial;color:#fff;text-align:center;box-shadow:0 6px 20px rgba(0,0,0,.25)';document.body.appendChild(tb)}
    tb.textContent=t;tb.style.background=ok?'#15803d':'#b91c1c';tb.hidden=false;clearTimeout(tb._t);tb._t=setTimeout(function(){tb.hidden=true},ok?2200:4500)}
  window.iqToast=toast;
  function done(){var code=buf.trim();buf='';clearTimeout(tm);if(code.length<6)return;var a=document.activeElement;
    if(a&&(a.tagName==='INPUT'||a.tagName==='TEXTAREA')){setTimeout(function(){var v=String(a.value||''),i=v.lastIndexOf(code);if(i>=0)a.value=v.slice(0,i)+v.slice(i+code.length);else if(a.type==='number')a.value=''},0)}
    fetch(BQ+'&arr=1&bc='+encodeURIComponent(code),{credentials:'same-origin'}).then(function(r){return r.text()}).then(function(t){var p=t.split('|');
      if(p[0]==='OK')cb({ok:true,name:p[1],tmpl:p[2],pid:p[3],qty:Math.max(1,parseInt(p[4],10)||1),code:code});
      else toast((DE?'Barcode nicht gefunden: ':'Barcode not found: ')+code+(DE?' – bitte Produkt eintippen':' – please type the product'),false)})
    .catch(function(){toast(DE?'Keine Verbindung – nochmal scannen.':'No connection – scan again.',false)})}
  document.addEventListener('keydown',function(e){var now=Date.now();
    if(e.key==='Enter'||e.key==='Tab'){if(buf.length>=6&&now-last<80){e.preventDefault();e.stopPropagation();done()}else buf='';return}
    if(!e.key||e.key.length!==1)return;
    if(now-last>50)buf='';buf+=e.key;last=now;clearTimeout(tm);tm=setTimeout(function(){if(buf.length>=6)done();else buf=''},150)},true);
};
"""
NOPO_JS = r"""
(function(){
  var S=document.getElementById('nsup'),M=document.getElementById('match'),C={},shown=0;
  function low(s){return (s||'').toLowerCase()}
  function check(){var s=low(S.value.trim()),ps=[];document.querySelectorAll('.nrow input[name^=prod_]').forEach(function(i){if(i.value.trim().length>=3)ps.push(low(i.value.trim()))});
    var hits=ITEMS.filter(function(it){var bys=s.length>=3&&low(it[0]).indexOf(s)>=0;var byp=ps.some(function(p){return low(it[1]).indexOf(p.split(' – ')[0].slice(0,18))>=0||p.indexOf(low(it[1]).split(' +')[0].slice(0,18))>=0});return bys||byp}).slice(0,8);
    shown=hits.length;C.hidden=!shown;if(!shown){M.hidden=true;M.innerHTML='';return}
    var h='<b>'+(DE?'Gehört die Ware zu einer dieser Lieferungen? Dann einfach antippen. Sonst unten normal melden.':'Does it belong to one of these deliveries? Then just tap it. Otherwise report it below as usual.')+'</b>';
    hits.forEach(function(it){h+='<a href="'+BQ+it[6]+'"><span>'+esc(it[1])+'<small>'+esc(it[0])+(it[2]?' · '+esc(it[2]):'')+(it[3]&&it[3]!==it[2]?' · '+esc(it[3]):'')+' · '+(DE?'erwartet ':'expected ')+it[4]+'</small></span><span>'+it[5]+' →</span></a>'});
    M.innerHTML=h;M.hidden=false}
  function esc(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;')}
  S.oninput=check;S.onchange=check;document.querySelectorAll('.nrow input[name^=prod_]').forEach(function(i){i.onchange=check;i.oninput=check});
  document.getElementById('nadd').onclick=function(){var h=document.querySelector('.nrow[hidden]');if(h){h.hidden=false;h.querySelector('input').focus()}if(!document.querySelector('.nrow[hidden]'))this.hidden=true};
  document.getElementById('asave').onclick=function(){
    var p1=document.querySelector('.nrow input[name=prod_1]');if(p1&&!p1.value.trim()){alert(DE?'Bitte das Produkt eingeben.':'Please enter the product.');p1.focus();return}
    
    window.arrSend()};
  window.nopoCheck=check;
  check();
  iqScan(BQ,DE,function(r){var hit=null,emp=null;
    document.querySelectorAll('.nrow').forEach(function(w){var i=w.querySelector('input[name^=prod_]');if(!hit&&i.value.trim().toLowerCase()===r.name.toLowerCase())hit=w;if(!emp&&!w.hidden&&!i.value.trim())emp=w});
    if(!hit){if(!emp){emp=document.querySelector('.nrow[hidden]');if(emp)emp.hidden=false}if(!emp){iqToast(DE?'Keine freie Zeile mehr':'No free row left',false);return}hit=emp;hit.querySelector('input[name^=prod_]').value=r.name}
    if(!document.querySelector('.nrow[hidden]'))document.getElementById('nadd').hidden=true;
    var c=hit.querySelector('input[name^=cnt_]');c.value=(parseInt(c.value||'0',10)||0)+r.qty;check();
    iqToast(r.name+' · '+(DE?'gezählt ':'counted ')+c.value,true)});
})();
"""

CSS = """
:root{--bg:#f4f4f2;--card:#fff;--fg:#151515;--mut:#6b7280;--line:#e5e5e2;--red:#a51d1b;--soft:#fdecea}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}
a{color:inherit}
.top{background:#151515;color:#fff;border-bottom:4px solid var(--red)}
.top .in{max-width:none;margin:0 auto;padding:14px 18px;display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:space-between}
.brand{display:flex;align-items:center;gap:14px}.brand img{height:38px;width:auto;display:block}
.brand h1{font:800 20px/1.1 Arial,sans-serif;margin:0;letter-spacing:.2px}.brand p{margin:2px 0 0;color:#bdbdbd;font-size:12.5px}
nav{display:flex;gap:6px;align-items:center;flex-wrap:wrap}
nav a{padding:7px 12px;border:1px solid #3a3a3a;border-radius:6px;text-decoration:none;color:#fff;background:#222}
nav a:hover{border-color:#fff}nav b{font-size:16px;margin:0 6px;min-width:140px;text-align:center}
wrap,.wrap{display:block;max-width:none;margin:0 auto;padding:16px 18px}
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
.ev b{font-size:13px}.ev span{display:block;color:var(--mut);font-size:11px}.ev.dlv{background:#ecfdf3;border-left-color:#16a34a!important}.ev.dlv b:before{content:'✓ ';color:#16a34a}.tag.dn{background:#16a34a}.srch{display:flex;gap:8px;margin:0 0 14px}.srch input{flex:1;min-width:0;padding:10px 12px;border:1px solid #d1d5db;border-radius:6px;font-size:15px;background:#fff}.srch button,.srch a.x{padding:10px 14px;border:0;border-radius:6px;background:#151515;color:#fff;font:700 14px Arial;text-decoration:none;cursor:pointer}.srch a.x{background:#e5e7eb;color:#111}.res table{width:100%;border-collapse:collapse;font-size:13.5px}.res td,.res th{padding:7px 5px;border-top:1px solid var(--line);text-align:left}.res th{font:700 11px Arial;letter-spacing:.8px;text-transform:uppercase;color:var(--mut);border-top:0}.res td.r{text-align:right;white-space:nowrap}.res .s{display:inline-block;font:700 11px Arial;border-radius:4px;padding:3px 8px;white-space:nowrap}.s-dn{background:#dcfce7;color:#166534}.s-ex{background:#dbeafe;color:#1e40af}.s-od{background:#fee2e2;color:#991b1b}.res{margin-bottom:14px;overflow-x:auto}
a.evl,a.rowl{display:block;color:inherit;text-decoration:none}a.evl:hover .ev{outline:2px solid #151515;outline-offset:-1px}a.rowl:hover .row{background:#fafaf8}
.ev.od{background:var(--soft)}
.lf{display:flex;gap:6px}.lf button{padding:8px 14px;border:0;border-radius:6px;background:#151515;color:#fff;font:700 13px Arial}.lx{padding:8px 12px;border-radius:6px;background:#e5e7eb;color:#111;text-decoration:none}
.lgd2{display:flex;gap:14px;flex-wrap:wrap;color:var(--mut);font-size:12px;margin-top:10px}.lgd2 i{font-style:normal}
.ft.re.on{background:var(--red)}.ft.ord.on{background:#1d4ed8}.ft.ok.on{background:#16a34a}
.fts{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 12px}.ft{padding:6px 12px;border-radius:999px;background:#f3f4f6;color:#111;text-decoration:none;font-size:13px}.ft.on{background:#151515;color:#fff}
.lf input{padding:8px 10px;border:1px solid #d1d5db;border-radius:6px;font-size:14px;min-width:220px}
.tag.dn{background:#16a34a}.srch{display:flex;gap:8px;margin:0 0 14px}.srch input{flex:1;min-width:0;padding:10px 12px;border:1px solid #d1d5db;border-radius:6px;font-size:15px;background:#fff}.srch button,.srch a.x{padding:10px 14px;border:0;border-radius:6px;background:#151515;color:#fff;font:700 14px Arial;text-decoration:none;cursor:pointer}.srch a.x{background:#e5e7eb;color:#111}
.res table{width:100%;border-collapse:collapse;font-size:13.5px}.res td,.res th{padding:7px 5px;border-top:1px solid var(--line);text-align:left}.res th{font:700 11px Arial;letter-spacing:.8px;text-transform:uppercase;color:var(--mut);border-top:0}.res td.r{text-align:right;white-space:nowrap}.res .s{display:inline-block;font:700 11px Arial;border-radius:4px;padding:3px 8px;white-space:nowrap}.s-dn{background:#dcfce7;color:#166534}.s-ex{background:#dbeafe;color:#1e40af}.s-od{background:#fee2e2;color:#991b1b}.res{margin-bottom:14px;overflow-x:auto}
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
footer{max-width:none;margin:0 auto;padding:0 18px 20px;color:var(--mut);font-size:12px;display:flex;justify-content:space-between}
@media(max-width:980px){main{grid-template-columns:1fr}.kpis{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:700px){.grid{display:none}.agenda{display:block}.brand img{height:30px}.brand h1{font-size:17px}nav b{min-width:0}}
.agenda .d{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin-bottom:8px}
.agenda .d h4{margin:0 0 6px;font:800 13px Arial}
.day{position:relative}.addd{position:absolute;top:4px;right:5px;width:22px;height:22px;line-height:20px;text-align:center;border-radius:50%;border:1px solid #16a34a;color:#16a34a;text-decoration:none;font:800 15px Arial;background:#fff}
.addd:hover{background:#16a34a;color:#fff}.agenda .addd{position:static;display:inline-block;margin-left:8px}
.ev.arr{background:#fff7e6;border-left-color:#f59e0b!important}.ev.arr b:before{content:'';display:inline-block;width:12px;height:12px;margin-right:4px;vertical-align:-1px;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2392400e' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 8l-9-5-9 5v8l9 5 9-5z'/%3E%3Cpath d='M3 8l9 5 9-5'/%3E%3Cpath d='M12 13v8'/%3E%3C/svg%3E") no-repeat center/contain}.ev.nopo{background:#fde8e8;border-left-color:#dc2626!important}.ev.nopo b:before{content:'';display:inline-block;width:12px;height:12px;margin-right:4px;vertical-align:-1px;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23b91c1c' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 3L2 21h20z'/%3E%3Cpath d='M12 10v5'/%3E%3Cpath d='M12 18h.01'/%3E%3C/svg%3E") no-repeat center/contain}
.arrl{display:block;font-size:11.5px;color:#92400e;text-decoration:none;margin:-2px 0 6px 6px;font-weight:700}.arrl:hover{text-decoration:underline}
nav.cnav{flex:1 1 660px;width:auto;min-width:0;flex-wrap:nowrap;gap:8px;margin-left:18px;justify-content:flex-end}@media(min-width:701px){.top nav.cnav .nbtn{flex:0 1 auto;margin-left:10px;padding-left:16px;border-left:1px solid #3a3a3a;gap:8px}}nav.cnav .nbtn{display:flex;gap:6px;flex:1 1 auto;min-width:0;overflow-x:auto;scrollbar-width:none;padding:2px 0}nav.cnav .nbtn::-webkit-scrollbar{display:none}nav.cnav .nbtn a{flex:0 0 auto}nav.cnav .nbtn.more{-webkit-mask-image:linear-gradient(90deg,#000 88%,transparent);mask-image:linear-gradient(90deg,#000 88%,transparent)}nav a.arrb{background:#f59e0b;border-color:#f59e0b;color:#151515;font-weight:800}.ic{width:1.15em;height:1.15em;vertical-align:-.2em;margin-right:.35em}.dcd small .ic{width:1.2em;height:1.2em}
@media(max-width:700px){.top .in{padding:10px 12px;gap:10px}.brand p{display:none}.brand img{height:28px}
 nav.cnav{display:grid;grid-template-columns:44px 1fr 44px auto;gap:6px;width:100%;align-items:center}
 nav.cnav a,nav.cnav b{text-align:center;padding:9px 10px;font-size:14px;white-space:nowrap}nav.cnav b{min-width:0;margin:0;font-size:16px;padding:0;overflow:hidden;text-overflow:ellipsis}
 nav.cnav .nbtn{grid-column:1/-1;margin-left:0;display:flex;gap:8px;overflow-x:auto;-webkit-overflow-scrolling:touch;scroll-snap-type:x proximity;padding:2px 24px 4px 0;margin-right:-12px;scrollbar-width:none}
 nav.cnav .nbtn::-webkit-scrollbar{display:none}
 nav.cnav .nbtn a{flex:0 0 auto;scroll-snap-align:start;font-size:14px;padding:11px 14px}nav.cnav .nbtn .arrb{font-size:15px}
 .kpis{gap:8px}.kpi{padding:10px 12px}.kpi b{font-size:19px}}
.edt{display:block;font-size:11px;color:#166534;text-decoration:none;margin:-2px 0 5px 6px}.edt:hover{text-decoration:underline}.agenda .d.today{box-shadow:inset 0 0 0 2px var(--red)}
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
elif params.get('arr') or (request.httprequest.method == 'POST' and params.get('act') in ('arr_save', 'nopo_save')):
    # ------------------------------------------------------------------ 20.11.2026: "Ware angekommen" – warehouse reports arrived goods (team password + name)
    # Nothing is booked: counts + delivery note go onto the Goods Receipt card, the purchase order and the open receipt (chatter + files).
    Line = env['x_wareneingang_line'].sudo()
    WE = env['x_wareneingang'].sudo()
    PO = env['purchase.order'].sudo()
    Pick = env['stock.picking'].sudo()
    Partner = env['res.partner'].sudo()
    Tmpl = env['product.template'].sudo()
    aday = datetime.date.today()
    bq = base.replace('&', '&amp;')
    WEACT = env['ir.actions.act_window'].sudo().search([('res_model', '=', 'x_wareneingang')], order='id', limit=1)

    def aesc(s):
        return str(s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

    def ajs(s):
        return '"' + str(s or '').replace(chr(92), chr(92) + chr(92)).replace('"', chr(92) + '"').replace(chr(10), ' ').replace(chr(13), ' ').replace('<', chr(92) + 'u003c') + '"'

    def apost(rec, txt, atts):
        try:
            if rec:
                if atts:
                    rec.message_post(body=txt, attachment_ids=atts)
                else:
                    rec.message_post(body=txt)
        except Exception:
            pass

    def anum(s):
        s = str(s or '').strip().replace('.', '').replace(',', '.')
        try:
            return max(0, int(round(float(s)))) if s else -1
        except Exception:
            return -1

    def ashort(n):
        return (n or '').split(' – ')[0]

    def vname(p):
        at = ' / '.join([x for x in p.product_template_attribute_value_ids.mapped('name') if x])
        return ashort(p.product_tmpl_id.name) + ((' · ' + at) if at else '')

    def card_url(card):
        return (('/odoo/action-' + str(WEACT.id) + '/' + str(card.id)) if WEACT else ('/odoo/x_wareneingang/' + str(card.id))) if card else ''

    def apage(title, inner, back=True):
        return (page_head(TITLE) + ACSS + '</head><body><div class="top"><div class="in"><div class="brand"><img src="' + LOGO + '" alt="IQ Dogsport"><div><h1>' + title + '</h1><p>'
                + ('Wareneingang melden – wird nicht gebucht' if de else 'Report arrived goods – nothing is booked') + '</p></div></div><nav class="anav"><a href="' + bq + '">'
                + ('&larr; Kalender' if de else '&larr; Calendar') + '</a>' + (('<a href="' + bq + '&amp;arr=1">' + ('Alle Lieferungen' if de else 'All deliveries') + '</a>') if back else '') + '</nav></div></div>'
                + '<div class="af">' + inner + '</div></body></html>')

    def aresp(html):
        return request.make_response(html, headers=[('Content-Type', 'text/html; charset=utf-8'), ('X-Robots-Tag', 'noindex'), ('Cache-Control', 'no-store')])

    def atxt(t):
        return request.make_response(t, headers=[('Content-Type', 'text/plain; charset=utf-8'), ('Cache-Control', 'no-store')])

    def arr_stage():
        st = env['x_wareneingang_stage'].sudo().search([('x_name', 'in', ['Goods arrived', 'Ware angekommen', 'Arrived – to check', 'Angekommen – prüfen'])], limit=1)
        return st

    def arr_flag(card, summ):
        # 23.11.: card goes to the column "Ware angekommen" (if installed) + To-Do in Odoo, so nobody misses it
        try:
            st = arr_stage()
            if st and (card.x_studio_stage_id.x_studio_sequence or 0) < 30:
                card.write({'x_studio_stage_id': st.id})
        except Exception:
            pass
        try:
            logins = [x.strip() for x in (env['ir.config_parameter'].sudo().get_param('iq.arrival_notify_logins') or '').split(',') if x.strip()]
            users = env['res.users'].sudo().search([('login', 'in', logins)]) if logins else env.ref('base.group_system').users.filtered(lambda u: u.active and not u.share and u.id > 1)
            atype = env.ref('mail.mail_activity_data_todo')
            mid = env['ir.model'].sudo().search([('model', '=', 'x_wareneingang')], limit=1).id
            for u in users[:6]:
                env['mail.activity'].sudo().create({'res_model_id': mid, 'res_id': card.id, 'activity_type_id': atype.id, 'user_id': u.id,
                                                    'summary': summ[:110], 'date_deadline': aday})
        except Exception:
            pass

    def plan_cover():
        # booked quantity of a PO is matched to its planned deliveries (oldest first) – same rule as the calendar
        cov = {}
        cpos = []
        for l0 in Line.search([('x_done', '=', False), ('x_date', '!=', False)]):
            po0 = l0.x_wareneingang_id.x_studio_purchase_order
            if po0 and po0.id not in cpos:
                cpos.append(po0.id)
        for pid0 in cpos:
            rem = 0.0
            for ol0 in PO.browse(pid0).order_line:
                if ol0.product_id and ol0.product_id.type != 'service':
                    rem += ol0.qty_received or 0.0
            for l0 in Line.search([('x_wareneingang_id.x_studio_purchase_order', '=', pid0), ('x_date', '!=', False)], order='x_date asc, id asc'):
                if rem <= 0:
                    break
                q0 = l0.x_qty or 0.0
                if rem >= q0 * 0.98:
                    cov[l0.id] = 0
                    rem -= q0
                else:
                    cov[l0.id] = q0 - rem
                    rem = 0
        return cov

    def open_items():
        # every delivery that is still expected: planned lines (not arrived) + open receipts of purchase orders without planned lines
        items = []
        seen_po = []
        cov = plan_cover()
        for l in Line.search([('x_done', '=', False), ('x_date', '!=', False), ('x_date', '<=', aday + datetime.timedelta(days=45))], order='x_date asc'):
            po = l.x_wareneingang_id.x_studio_purchase_order
            if po and po.id not in seen_po:
                seen_po.append(po.id)
            if po and po.receipt_status == 'full':
                continue
            lq = l.x_qty or 0
            if l.id in cov:
                if cov[l.id] <= 0:
                    continue
                lq = cov[l.id]
            items.append({'d': l.x_date, 'sup': (l.x_partner_id.commercial_partner_id.name or (po.partner_id.commercial_partner_id.name if po else '') or ''), 'prod': l.x_product_text or '',
                          'qty': lq, 'ref': (po.name if po else '') or (l.x_supplier_ref or ''), 'sref': l.x_supplier_ref or (po.partner_ref if po else '') or '',
                          'url': '&arr=1&lid=' + str(l.id) + (('&po=' + str(po.id)) if po else '&wid=' + str(l.x_wareneingang_id.id)), 'ship': l.x_shipment or ''})
        for p in Pick.search([('picking_type_code', '=', 'incoming'), ('purchase_id', '!=', False), ('state', 'not in', ['done', 'cancel', 'draft'])], order='scheduled_date asc'):
            po = p.purchase_id
            if po.id in seen_po:
                continue
            seen_po.append(po.id)
            names = []
            qty = 0.0
            for mv in p.move_ids:
                if mv.state != 'cancel':
                    qty += mv.product_uom_qty or 0.0
                    n = ashort(mv.product_id.product_tmpl_id.name)
                    if n not in names:
                        names.append(n)
            dp = po.date_planned or p.scheduled_date
            items.append({'d': dp.date() if dp else aday, 'sup': po.partner_id.commercial_partner_id.name or '', 'prod': (names[0] + (' +' + str(len(names) - 1) if len(names) > 1 else '')) if names else '',
                          'qty': qty, 'ref': po.name, 'sref': po.partner_ref or '', 'url': '&arr=1&po=' + str(po.id), 'ship': ''})
        return sorted(items, key=lambda it: (0 if it['d'] <= aday else 1, abs((it['d'] - aday).days)))

    act = params.get('act') if request.httprequest.method == 'POST' else ''
    who = str(params.get('who') or '').strip()[:40]
    if params.get('bc') and not act:
        # 23.11.: barcode scan (hand scanner) -> product; packaging barcode -> its quantity
        bcq = str(params.get('bc') or '').strip()[:64]
        Prod = env['product.product'].sudo()
        bp = Prod.search([('barcode', '=', bcq)], limit=1)
        bqty = 1
        if not bp:
            bp = Prod.search([('default_code', '=', bcq)], limit=1)
        if not bp:
            try:
                pk = env['product.packaging'].sudo().search([('barcode', '=', bcq)], limit=1)
                if pk:
                    bp = pk.product_id
                    bqty = int(pk.qty or 1)
            except Exception:
                pass
        response = atxt(('OK|' + vname(bp).replace('|', '/') + '|' + ashort(bp.product_tmpl_id.name).replace('|', '/') + '|' + str(bp.id) + '|' + str(bqty)) if bp else 'NO|')
    elif act in ('arr_save', 'nopo_save') and not who:
        response = atxt('ERR|' + ('Bitte deinen Namen eingeben (oben).' if de else 'Please enter your name (top).'))
    elif act == 'arr_save':
        po = PO.browse(int(params.get('po'))).exists() if str(params.get('po') or '').isdigit() else PO
        ln = Line.browse(int(params.get('lid'))).exists() if str(params.get('lid') or '').isdigit() else Line
        card = WE.browse(int(params.get('wid'))).exists() if str(params.get('wid') or '').isdigit() else WE
        if ln and not card:
            card = ln.x_wareneingang_id
        if po and not card:
            card = WE.search([('x_studio_purchase_order', '=', po.id)], limit=1)
            if not card:
                card = WE.create({'x_name': po.name, 'x_studio_purchase_order': po.id, 'x_studio_supplier': po.partner_id.id, 'x_supplier_ref': po.partner_ref or False})
        if not card:
            response = atxt('ERR|' + ('Lieferung nicht gefunden.' if de else 'Delivery not found.'))
        else:
            rows = []
            if po:
                for ol in po.order_line:
                    if ol.product_id and ol.product_id.type != 'service' and ol.product_qty > 0:
                        lsq = anum(params.get('ls_' + str(ol.id)))
                        cq = anum(params.get('cnt_' + str(ol.id)))
                        if lsq >= 0 or cq >= 0:
                            rows.append([vname(ol.product_id), int(ol.product_qty - (ol.qty_received or 0)), lsq, cq])
            else:
                lsq = anum(params.get('ls_0'))
                cq = anum(params.get('cnt_0'))
                if lsq >= 0 or cq >= 0:
                    rows.append([(ln.x_product_text if ln else '') or (card.x_name or ''), int(ln.x_qty or 0) if ln else 0, lsq, cq])
            files = [f for f in request.httprequest.files.getlist('files') if f and f.filename]
            if not rows and not files:
                response = atxt('ERR|' + ('Bitte mindestens eine Menge eintragen oder den Lieferschein hochladen.' if de else 'Please enter at least one quantity or upload the delivery note.'))
            else:
                pick = Pick.search([('purchase_id', '=', po.id), ('picking_type_code', '=', 'incoming'), ('state', 'not in', ['done', 'cancel'])], order='id', limit=1) if po else Pick
                stamp = datetime.datetime.now()
                tsn = int((stamp - datetime.datetime(1970, 1, 1)).total_seconds())
                dtxt = (stamp + datetime.timedelta(hours=1)).strftime('%d.%m.%Y %H:%M')
                lsno = str(params.get('lsno') or '').strip()[:60].replace('|', '/')
                boxes = str(params.get('boxes') or '').strip()[:30].replace('|', '/')
                anote_ = str(params.get('note') or '').strip()[:500]
                att_ids = []
                patt = []
                for i, f in enumerate(files[:10]):
                    data = f.read()
                    if not data or len(data) > 15000000:
                        continue
                    ext = '.pdf' if 'pdf' in (f.mimetype or '') else '.jpg'
                    nm = 'Lieferschein ' + (lsno + ' ' if lsno else '') + dtxt.replace(':', '-') + ('-' + str(i + 1) if len(files) > 1 else '') + ext
                    att_ids.append(ATT.create({'name': nm, 'raw': data, 'mimetype': f.mimetype or 'image/jpeg', 'res_model': 'x_wareneingang', 'res_id': card.id}).id)
                    if pick:
                        patt.append(ATT.create({'name': nm, 'raw': data, 'mimetype': f.mimetype or 'image/jpeg', 'res_model': 'stock.picking', 'res_id': pick.id}).id)
                ls_t = sum([r[2] for r in rows if r[2] > 0])
                c_t = sum([r[3] for r in rows if r[3] > 0])
                o_t = sum([r[1] for r in rows])
                prod1 = (rows[0][0].split(' · ')[0] if rows else (ln.x_product_text if ln else '')) or ''
                body = ['IQ-ARRIVAL|' + str(tsn) + '|' + who.replace('|', '/') + '|' + str(pick.id if pick else 0) + '|' + str(ln.id if ln else 0) + '|' + boxes + '|' + lsno + '|'
                        + str(ls_t) + '|' + str(c_t) + '|' + str(o_t) + '|' + prod1.replace('|', '/')[:80] + '|' + str(po.id if po else 0),
                        'Wareneingang gemeldet am ' + dtxt + ' von ' + who, 'Lieferung: ' + (po.name if po else (card.x_name or '')) + ' · ' + (card.x_studio_supplier.name or ''),
                        'Lieferschein-Nr.: ' + (lsno or '–') + ' · Kartons/Paletten: ' + (boxes or '–'), '']
                for r in rows:
                    body.append(r[0] + ': offen ' + str(r[1]) + ' · laut Lieferschein ' + (str(r[2]) if r[2] >= 0 else '–') + ' · gezählt ' + (str(r[3]) if r[3] >= 0 else '–'))
                if anote_:
                    body += ['', 'Notiz: ' + anote_]
                ATT.create({'name': ARRPRE + dtxt.replace(':', '-') + '.txt', 'raw': chr(10).join(body).encode('utf-8'), 'mimetype': 'text/plain', 'res_model': 'x_wareneingang', 'res_id': card.id})
                vals = {'x_studio_arrival_date': aday}
                card.write(vals)
                if ln:
                    ln.write({'x_done': True})
                summ = (('Ware angekommen – gemeldet von ' if de else 'Goods arrived – reported by ') + who + ' (' + dtxt + '): '
                        + ', '.join([r[0] + (' LS ' + str(r[2]) if r[2] >= 0 else '') + (' / gezählt ' + str(r[3]) if r[3] >= 0 else '') for r in rows])
                        + ((' · Lieferschein-Nr. ' + lsno) if lsno else '') + ((' · ' + boxes + ' Kartons/Paletten') if boxes else '') + ((' · ' + anote_) if anote_ else '')
                        + (' · ' + str(len(att_ids)) + ' Datei(en)' if att_ids else '') + ' – noch nicht gebucht.')
                apost(card, summ, att_ids)
                arr_flag(card, ('Ware angekommen: ' if de else 'Goods arrived: ') + prod1 + ' · ' + (str(c_t) + (' gezählt' if de else ' counted') if c_t else ('LS ' + str(ls_t))) + ' · ' + who)
                if po:
                    apost(po, summ, [])
                if pick:
                    apost(pick, summ, patt)
                response = atxt('OK|' + str(card.id))
    elif act == 'nopo_save':
        sup_txt = str(params.get('sup') or '').strip()[:80]
        sup = (Partner.search([('name', '=ilike', sup_txt)], limit=1) or Partner.search([('name', 'ilike', sup_txt)], limit=1)) if sup_txt else Partner
        rows = []
        for i in range(1, 11):
            pn = str(params.get('prod_' + str(i)) or '').strip()[:120].replace('|', '/')
            lsq = anum(params.get('ls_' + str(i)))
            cq = anum(params.get('cnt_' + str(i)))
            if pn:
                rows.append([pn, 0, lsq, cq])
        files = [f for f in request.httprequest.files.getlist('files') if f and f.filename]
        if not rows:
            response = atxt('ERR|' + ('Bitte mindestens ein Produkt eingeben.' if de else 'Please enter at least one product.'))
        else:
            stamp = datetime.datetime.now()
            tsn = int((stamp - datetime.datetime(1970, 1, 1)).total_seconds())
            dtxt = (stamp + datetime.timedelta(hours=1)).strftime('%d.%m.%Y %H:%M')
            lsno = str(params.get('lsno') or '').strip()[:60].replace('|', '/')
            boxes = str(params.get('boxes') or '').strip()[:30].replace('|', '/')
            anote_ = str(params.get('note') or '').strip()[:500]
            t1 = Tmpl.search([('name', '=ilike', rows[0][0].split(' · ')[0])], limit=1)
            cvals = {'x_name': ('Ohne Bestellung · ' if de else 'No PO · ') + rows[0][0][:60] + ((' · ' + (sup.name if sup else sup_txt)) if (sup or sup_txt) else ''),
                     'x_studio_supplier': sup.id if sup else False, 'x_supplier_ref': lsno or False, 'x_studio_arrival_date': aday,
                     'x_studio_notes': '<p>' + aesc(('Ware ohne Bestellung angekommen, gemeldet von ' if de else 'Goods without purchase order arrived, reported by ') + who + ' (' + dtxt + ').') + '</p>'
                     + ''.join(['<p>' + aesc(r[0] + ': laut Lieferschein ' + (str(r[2]) if r[2] >= 0 else '–') + ' · gezählt ' + (str(r[3]) if r[3] >= 0 else '–')) + '</p>' for r in rows])
                     + (('<p>' + aesc('Lieferant laut Lieferschein: ' + sup_txt) + '</p>') if (sup_txt and not sup) else ('' if sup else '<p>Lieferant unbekannt</p>')) + (('<p>' + aesc(anote_) + '</p>') if anote_ else '')}
            if t1:
                cvals['x_studio_product'] = t1.id
            card = WE.create(cvals)
            for r in rows:
                try:
                    Line.create({'x_wareneingang_id': card.id, 'x_date': aday, 'x_qty': (r[3] if r[3] >= 0 else max(r[2], 0)), 'x_product_text': r[0][:120], 'x_done': True,
                                 'x_shipment': ('angekommen' if de else 'arrived') + ((' · LS ' + str(r[2])) if r[2] >= 0 else '') + ((' · gezählt ' + str(r[3])) if r[3] >= 0 else '')})
                except Exception:
                    pass
            att_ids = []
            for i, f in enumerate(files[:10]):
                data = f.read()
                if not data or len(data) > 15000000:
                    continue
                ext = '.pdf' if 'pdf' in (f.mimetype or '') else '.jpg'
                att_ids.append(ATT.create({'name': 'Lieferschein ' + (lsno + ' ' if lsno else '') + dtxt.replace(':', '-') + ('-' + str(i + 1) if len(files) > 1 else '') + ext,
                                           'raw': data, 'mimetype': f.mimetype or 'image/jpeg', 'res_model': 'x_wareneingang', 'res_id': card.id}).id)
            ls_t = sum([r[2] for r in rows if r[2] > 0])
            c_t = sum([r[3] for r in rows if r[3] > 0])
            body = ['IQ-ARRIVAL|' + str(tsn) + '|' + who.replace('|', '/') + '|0|0|' + boxes + '|' + lsno + '|' + str(ls_t) + '|' + str(c_t) + '|0|' + rows[0][0][:80] + '|0',
                    'Ware OHNE Bestellung gemeldet am ' + dtxt + ' von ' + who, 'Lieferant: ' + sup_txt, 'Lieferschein-Nr.: ' + (lsno or '–') + ' · Kartons/Paletten: ' + (boxes or '–'), '']
            for r in rows:
                body.append(r[0] + ': laut Lieferschein ' + (str(r[2]) if r[2] >= 0 else '–') + ' · gezählt ' + (str(r[3]) if r[3] >= 0 else '–'))
            if anote_:
                body += ['', 'Notiz: ' + anote_]
            ATT.create({'name': ARRPRE + dtxt.replace(':', '-') + '.txt', 'raw': chr(10).join(body).encode('utf-8'), 'mimetype': 'text/plain', 'res_model': 'x_wareneingang', 'res_id': card.id})
            apost(card, ('ACHTUNG: Ware OHNE Bestellung angekommen – gemeldet von ' if de else 'ATTENTION: Goods WITHOUT purchase order arrived – reported by ') + who + ' (' + dtxt + '): '
                  + ', '.join([r[0] + (' LS ' + str(r[2]) if r[2] >= 0 else '') + (' / gezählt ' + str(r[3]) if r[3] >= 0 else '') for r in rows])
                  + ((' · Lieferschein-Nr. ' + lsno) if lsno else '') + ' – Bitte Bestellung anlegen (Lieferantenreferenz = ' + (lsno or 'Lieferschein-Nr.') + ', dann wird sie automatisch verknüpft).', att_ids)
            c_one = rows[0][3] if rows[0][3] >= 0 else max(rows[0][2], 0)
            arr_flag(card, ('Ware angekommen (ohne Bestellung): ' if de else 'Goods arrived (no PO): ') + rows[0][0][:50] + ' · ' + str(c_one) + ' Stk.' + (' +' + str(len(rows) - 1) if len(rows) > 1 else '') + ' · ' + who)
            response = atxt('OK|' + str(card.id))
    elif params.get('arr') == 'done':
        card = WE.browse(int(params.get('w'))).exists() if str(params.get('w') or '').isdigit() else WE
        nopo = card and not card.x_studio_purchase_order
        inner = ('<div class="box adone"><div class="big">' + ICK + '</div><h2>' + ('Gemeldet – die Ware ist im Lager' if de else 'Reported – the goods are in the warehouse') + '</h2>'
                 + '<p>' + ('In Odoo steht sie jetzt im Wareneingang in der Spalte „Ware angekommen“ – mit Menge, Lieferschein und Datum.' if de else 'In Odoo it is now in Goods Receipts in the column “Goods arrived” – with quantity, delivery note and date.') + '</p>'
                 + '<div class="btns"><a class="b go" href="' + bq + '&amp;arr=1">' + ('Nächste Ware melden' if de else 'Report next goods') + '</a><a class="b" href="' + bq + '">' + ('Zum Kalender' if de else 'To the calendar') + '</a></div></div>')
        response = aresp(apage(TITLE, inner, False))
    elif params.get('nopo'):
        # ---------------- goods without a purchase order: first check if they belong to an open order (avoid duplicates)
        its = open_items()
        js_items = ','.join(['[' + ajs(it['sup']) + ',' + ajs(it['prod']) + ',' + ajs(it['ref']) + ',' + ajs(it['sref']) + ',' + ajs(it['d'].strftime('%d.%m.')) + ',' + str(int(it['qty'])) + ',' + ajs(it['url']) + ']' for it in its])
        sups = Partner.search([('supplier_rank', '>', 0)], order='name', limit=400) if 'supplier_rank' in Partner.fields_get(['supplier_rank']) else Partner
        sopts = ''.join(['<option value="' + aesc(x.name) + '">' for x in sups])
        tps = Tmpl.search([('purchase_ok', '=', True), ('type', '!=', 'service')], order='name', limit=1500) if 'purchase_ok' in Tmpl.fields_get(['purchase_ok']) else Tmpl.search([('type', '!=', 'service')], limit=1500)
        popts = ''.join(['<option value="' + aesc(x.name) + '">' for x in tps])
        prow = ''
        for i in range(1, 11):
            prow += ('<div class="nrow"' + ('' if i == 1 else ' hidden') + ' data-i="' + str(i) + '"><input name="prod_' + str(i) + '" list="tpl" placeholder="' + ('Produkt' if de else 'Product') + ' ' + str(i) + '" autocomplete="off">'
                     + '<input name="ls_' + str(i) + '" type="number" min="0" inputmode="numeric" placeholder="–"><input name="cnt_' + str(i) + '" type="number" min="0" inputmode="numeric" placeholder="–"></div>')
        pre = str(params.get('prod') or '').strip()[:120]
        prow = prow.replace('name="prod_1" list="tpl"', 'name="prod_1" list="tpl" value="' + aesc(pre) + '"', 1)
        inner = ('<form id="af" onsubmit="return false">' + WHO_HTML
                 + '<datalist id="tpl">' + popts + '</datalist><datalist id="suplist">' + sopts + '</datalist>'
                 + '<div class="box"><h2><span class="sn">2</span>' + ('Was ist gekommen?' if de else 'What arrived?') + '</h2><div class="nhead"><span>' + ('Produkt' if de else 'Product') + '</span><span>' + ('laut Lieferschein' if de else 'on del. note') + '</span><span>' + ('gezählt' if de else 'counted') + '</span></div>' + prow
                 + '<p class="hint" style="margin:6px 0 8px">' + ('Mit dem Scanner: Barcode scannen = Produkt eintragen und +1 gezählt.' if de else 'With the scanner: scan a barcode = product filled in and +1 counted.') + '</p><button type="button" class="b add" id="nadd">+ ' + ('weiteres Produkt' if de else 'another product') + '</button><div id="match" class="match" hidden></div></div>'
                 + LS_HTML.replace('<span class="sn">2</span>', '<span class="sn">3</span>').replace('<label class="l">' + ('Lieferschein-Nr. (optional)' if de else 'Delivery note no. (optional)') + '</label><input name="lsno" autocomplete="off" placeholder="z. B. LS 2026-344819">', '')
                 + '<details class="box more"><summary>' + ('Mehr (optional): Lieferant, Lieferschein-Nr., Kartons, Notiz' if de else 'More (optional): supplier, delivery note no., boxes, note') + '</summary>'
                 + '<label class="l">' + ('Lieferant – leer lassen, wenn unbekannt' if de else 'Supplier – leave empty if unknown') + '</label><input name="sup" id="nsup" list="suplist" autocomplete="off">'
                 + '<label class="l">' + ('Lieferschein-Nr.' if de else 'Delivery note no.') + '</label><input name="lsno" autocomplete="off" placeholder="z. B. LS 2026-344819">'
                 + '<label class="l">' + ('Anzahl Kartons / Paletten' if de else 'Number of boxes / pallets') + '</label><input name="boxes" autocomplete="off">'
                 + '<label class="l">' + ('Notiz' if de else 'Note') + '</label><textarea name="note"></textarea></details>'
                 
                 + '<p class="err" id="aerr" hidden></p><button type="button" class="save red" id="asave">' + ICK + ('Ware melden' if de else 'Report goods') + '</button>'
                 + '<p class="hint" style="text-align:center">' + ('Danach steht die Ware in Odoo in der Spalte „Ware angekommen“.' if de else 'Afterwards the goods are in Odoo in the column “Goods arrived”.') + '</p></form>'
                 + '<script>var CSRF=' + ajs(request.csrf_token()) + ',KEY=' + ajs(KEY) + ',BQ=' + ajs(base) + ',ACT="nopo_save",ICC=' + ajs(ICC) + ',DE=' + ('true' if de else 'false') + ',ITEMS=[' + js_items + '];' + SCAN_JS + ARR_JS + NOPO_JS + '</script>')
        response = aresp(apage(('Ware ohne Bestellung' if de else 'Goods without PO'), inner))
    elif params.get('po') or params.get('lid') or params.get('wid'):
        # ---------------- report one delivery
        po = PO.browse(int(params.get('po'))).exists() if str(params.get('po') or '').isdigit() else PO
        ln = Line.browse(int(params.get('lid'))).exists() if str(params.get('lid') or '').isdigit() else Line
        card = WE.browse(int(params.get('wid'))).exists() if str(params.get('wid') or '').isdigit() else WE
        if ln and not card:
            card = ln.x_wareneingang_id
        if not po and card and card.x_studio_purchase_order:
            po = card.x_studio_purchase_order
        if po and not card:
            card = WE.search([('x_studio_purchase_order', '=', po.id)], limit=1)
        sup = (po.partner_id.commercial_partner_id.name if po else '') or (ln.x_partner_id.commercial_partner_id.name if ln else '') or (card.x_studio_supplier.name if card else '') or ''
        rows = ''
        if po:
            grp = ''
            for ol in sorted([x for x in po.order_line if x.product_id and x.product_id.type != 'service' and x.product_qty > 0], key=lambda x: (x.product_id.product_tmpl_id.name or '', x.id)):
                tn = ashort(ol.product_id.product_tmpl_id.name)
                if tn != grp:
                    grp = tn
                    rows += '<div class="tg">' + aesc(tn) + '</div>'
                at = ' / '.join([x for x in ol.product_id.product_template_attribute_value_ids.mapped('name') if x]) or tn
                opn = int(ol.product_qty - (ol.qty_received or 0))
                rows += ('<div class="qr" data-o="' + str(max(0, opn)) + '"><span class="qn">' + aesc(at) + '<small>' + ('offen' if de else 'open') + ' ' + str(max(0, opn)) + (' · ' + ('schon gebucht' if de else 'booked') + ' ' + str(int(ol.qty_received)) if ol.qty_received else '') + '</small></span>'
                         + '<input type="number" min="0" inputmode="numeric" name="ls_' + str(ol.id) + '" class="qls" placeholder="–"><input type="number" min="0" inputmode="numeric" name="cnt_' + str(ol.id) + '" class="qcn" data-pid="' + str(ol.product_id.id) + '" placeholder="–"><b class="qd"></b></div>')
        else:
            opn = int(ln.x_qty or 0) if ln else 0
            rows += ('<div class="qr" data-o="' + str(opn) + '"><span class="qn">' + aesc((ln.x_product_text if ln else '') or (card.x_name if card else '')) + '<small>' + ('erwartet' if de else 'expected') + ' ' + str(opn) + '</small></span>'
                     + '<input type="number" min="0" inputmode="numeric" name="ls_0" class="qls" placeholder="–"><input type="number" min="0" inputmode="numeric" name="cnt_0" class="qcn" placeholder="–"><b class="qd"></b></div>')
        prev = [r for r in arr_records(120) if card and r['wid'] == card.id]
        head_ = ('<div class="box ahead"><b>' + aesc(sup) + '</b><span>' + aesc(' · '.join([x for x in [(po.name if po else ''), ((po.partner_ref or '') if po else (card.x_supplier_ref or '' if card else '')), ((ln.x_shipment or '') if ln else '')] if x])) + '</span>'
                 + (('<span>' + ('Erwartet am ' if de else 'Expected on ') + (ln.x_date.strftime('%d.%m.%Y') if ln and ln.x_date else (po.date_planned.strftime('%d.%m.%Y') if po and po.date_planned else '')) + '</span>'))
                 + ''.join(['<span class="prev">✓ ' + ('schon gemeldet am ' if de else 'already reported on ') + arr_date(r['ts']).strftime('%d.%m.') + ' (' + aesc(r['who']) + ', ' + str(r['cnt']) + ' ' + ('gezählt' if de else 'counted') + ')</span>' for r in prev]) + '</div>')
        inner = ('<form id="af" onsubmit="return false">' + head_ + WHO_HTML + LS_HTML
                 + '<div class="box"><h2><span class="sn">3</span>' + ('Menge' if de else 'Quantity') + '</h2><p class="hint">' + ('Pro Größe eintragen, was auf dem Lieferschein steht und was ihr gezählt habt. Leer lassen, wenn nicht geliefert.' if de else 'Per size: what the delivery note says and what you counted. Leave empty if not delivered.') + '</p>'
                 + '<div class="qhead"><span></span><span>' + ('Lieferschein' if de else 'Del. note') + '</span><span>' + ('gezählt' if de else 'counted') + '</span><span></span></div>' + rows
                 + '<div class="qtot"><span>' + ('Summe' if de else 'Total') + '</span><b id="tls">0</b><b id="tcn">0</b><b id="tdf"></b></div>'
                 + ('<p class="hint" style="margin:6px 0 8px">' + ('Mit dem Scanner: jedes Teil scannen = +1 gezählt bei der richtigen Größe.' if de else 'With the scanner: scan each item = +1 counted at the right size.') + '</p>' if po else '')
                 + '<button type="button" class="b add" id="fillo">' + ('Lieferschein = offene Menge übernehmen' if de else 'Delivery note = open quantity') + '</button></div>'
                 + MORE_HTML
                 + '<input type="hidden" name="po" value="' + (str(po.id) if po else '') + '"><input type="hidden" name="lid" value="' + (str(ln.id) if ln else '') + '"><input type="hidden" name="wid" value="' + (str(card.id) if card else '') + '">'
                 + '<p class="err" id="aerr" hidden></p><button type="button" class="save" id="asave">' + ICK + ('Wareneingang speichern' if de else 'Save arrival') + '</button>'
                 + '<p class="hint" style="text-align:center">' + ('Wird nur gemeldet – noch nicht gebucht.' if de else 'Only reported – not booked yet.') + '</p></form>'
                 + '<script>var CSRF=' + ajs(request.csrf_token()) + ',KEY=' + ajs(KEY) + ',BQ=' + ajs(base) + ',ACT="arr_save",ICC=' + ajs(ICC) + ',DE=' + ('true' if de else 'false') + ';' + SCAN_JS + ARR_JS + QTY_JS + '</script>')
        response = aresp(apage(('Ware angekommen' if de else 'Goods arrived'), inner))
    else:
        # ---------------- list: which delivery has arrived?
        its = open_items()
        arrived = {}
        for r in arr_records(14):
            arrived[r['wid']] = r
        lst = ''
        for it in its:
            st = ('<span class="st od">' + ('überfällig' if de else 'overdue') + '</span>') if it['d'] < aday else (('<span class="st td">' + ('heute' if de else 'today') + '</span>') if it['d'] == aday else '<span class="st">' + it['d'].strftime('%d.%m.') + '</span>')
            lst += ('<a class="it" href="' + bq + it['url'].replace('&', '&amp;') + '" data-s="' + aesc((it['sup'] + ' ' + it['prod'] + ' ' + it['ref'] + ' ' + it['sref'] + ' ' + it['ship']).lower()) + '">'
                    + '<span class="l"><b>' + aesc(it['prod']) + '</b><small>' + aesc(it['sup']) + (' · ' + aesc(it['ref']) if it['ref'] else '') + (' · ' + aesc(it['sref']) if it['sref'] and it['sref'] != it['ref'] else '') + (' · ' + aesc(it['ship']) if it['ship'] else '') + '</small></span>'
                    + '<span class="r"><b>' + '{:,.0f}'.format(it['qty']).replace(',', '.') + '</b>' + st + '</span></a>')
        pjs = '['
        ptps = Tmpl.search([('purchase_ok', '=', True), ('type', '!=', 'service')], order='name', limit=2500) if 'purchase_ok' in Tmpl.fields_get(['purchase_ok']) else Tmpl.search([('type', '!=', 'service')], order='name', limit=2500)
        for x in ptps:
            pjs += ('' if pjs == '[' else ',') + ajs(x.name or '')
        pjs += ']'
        inner = ('<div class="box"><h2>' + ('Welche Lieferung ist angekommen?' if de else 'Which delivery has arrived?') + '</h2>'
                 + '<input type="search" id="fs" placeholder="' + ('Suchen oder Barcode scannen …' if de else 'Search or scan a barcode …') + '" autocomplete="off">'
                 + '<div class="lst" id="lst">' + (lst or '<p class="mut">' + ('Keine erwarteten Lieferungen.' if de else 'No expected deliveries.') + '</p>') + '</div>'
                 + '<p class="mut" id="none" hidden>' + ('Nichts gefunden.' if de else 'Nothing found.') + '</p></div>'
                 + '<div class="box" id="pbox" hidden><h2>' + ('Ohne Bestellung melden:' if de else 'Report without order:') + '</h2><div id="plist"></div></div>'
                 + '<a class="nopo" id="nopoa" href="' + bq + '&amp;arr=1&amp;nopo=1"><b>' + ICW + ('Nicht in der Liste? Ware ohne Bestellung melden' if de else 'Not in the list? Report goods without PO') + '</b><small>'
                 + ('Einfach Produkt + Menge + Foto vom Lieferschein.' if de else 'Just product + quantity + photo of the delivery note.') + '</small></a>'
                 + '<script>' + SCAN_JS + '(function(){var P=' + pjs + ',BQ=' + ajs(base) + ',DE=' + ('true' if de else 'false') + ';var f=document.getElementById("fs"),pb=document.getElementById("pbox"),pl=document.getElementById("plist"),na=document.getElementById("nopoa");'
                 + 'function esc(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/"/g,"&quot;")}'
                 + 'f.oninput=function(){var q=f.value.trim().toLowerCase(),n=0;document.querySelectorAll("#lst .it").forEach(function(a){var ok=!q||a.dataset.s.indexOf(q)>=0;a.style.display=ok?"":"none";if(ok)n++});document.getElementById("none").hidden=n>0;'
                 + 'na.href=BQ+"&arr=1&nopo=1"+(q?"&prod="+encodeURIComponent(f.value.trim()):"");'
                 + 'if(q.length<3){pb.hidden=true;return}var h="",k=0;P.forEach(function(p){if(k<6&&p.toLowerCase().indexOf(q)>=0){k++;h+=\'<a class="it" href="\'+BQ+"&arr=1&nopo=1&prod="+encodeURIComponent(p)+\'"><span class="l"><b>\'+esc(p)+\'</b><small>\'+(DE?"oben nicht dabei? – hier melden":"not in the list above? – report here")+\'</small></span><span class="r">→</span></a>\'}});pl.innerHTML=h;pb.hidden=!k};iqScan(BQ,DE,function(r){f.value=r.tmpl;f.oninput();var x=pl.querySelector("a");if(x&&r.name)x.href=BQ+"&arr=1&nopo=1&prod="+encodeURIComponent(r.name);iqToast(r.name,true)})})();</script>')
        response = aresp(apage(('Ware angekommen' if de else 'Goods arrived'), inner))
elif (params.get('plan') and params.get('pin') is None) or (request.httprequest.method == 'POST' and params.get('act') in ('plan_save', 'plan_done', 'plan_del')):
    # ------------------------------------------------------------------ 19.11.2026: add / edit planned deliveries (managers only, manager PIN)
    Line = env['x_wareneingang_line'].sudo()
    WE = env['x_wareneingang'].sudo()
    PO = env['purchase.order'].sudo()
    Partner = env['res.partner'].sudo()

    def pesc(s):
        return str(s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

    def pjs(s):
        return '"' + str(s or '').replace(chr(92), chr(92) + chr(92)).replace('"', chr(92) + '"').replace(chr(10), ' ').replace(chr(13), ' ').replace('<', chr(92) + 'u003c') + '"'

    def note(rec, txt):
        try:
            if rec:
                rec.message_post(body=txt)
        except Exception:
            pass

    PCSS = ('<style>.pf{max-width:560px;margin:18px auto;padding:0 14px}.pf .box{padding:18px}.pf h2{margin:0 0 4px;font:800 20px Arial}'
            '.pf label{display:block;font:700 13px Arial;margin:12px 0 4px}.pf small.h{display:block;color:var(--mut);font-size:12px;margin-top:3px}'
            '.pf input{width:100%;padding:11px;border:1px solid #d1d5db;border-radius:6px;font-size:16px;background:#fff}'
            '.pf .two{display:grid;grid-template-columns:1fr 1fr;gap:10px}.pf .btns{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}'
            '.pf button,.pf a.b{padding:12px 16px;border:0;border-radius:6px;font:700 15px Arial;cursor:pointer;text-decoration:none;display:inline-block}'
            '.pf .save{background:var(--red);color:#fff;flex:1 1 200px}.pf .ok{background:#16a34a;color:#fff}.pf .del{background:#fff;color:var(--red);border:1px solid var(--red)}'
            '.pf a.b{background:#e5e7eb;color:#111}.pf .err{background:var(--soft);color:var(--red);border:1px solid #f3b4b0;border-radius:6px;padding:9px 11px;font-weight:700;margin:10px 0 0}'
            '.pf .inf{background:#f0f9ff;border:1px solid #bae6fd;border-radius:6px;padding:9px 11px;font-size:13px;margin-top:12px}'
            '@media(max-width:520px){.pf .two{grid-template-columns:1fr}}</style>')

    def ppage(inner):
        return (page_head(TITLE) + PCSS + '</head><body><div class="top"><div class="in"><div class="brand"><img src="' + LOGO + '" alt="IQ Dogsport"><div><h1>' + TITLE + '</h1><p>'
                + ('Lieferung eintragen – nur Führungskräfte' if de else 'Add delivery – managers only') + '</p></div></div><nav><a href="' + base.replace('&', '&amp;') + '">'
                + ('&larr; Kalender' if de else '&larr; Calendar') + '</a></nav></div></div><div class="pf"><div class="box">' + inner + '</div></div></body></html>')

    def presp(html):
        return request.make_response(html, headers=[('Content-Type', 'text/html; charset=utf-8'), ('X-Robots-Tag', 'noindex'), ('Cache-Control', 'no-store')])

    pid_s = str(params.get('plan') or params.get('lid') or 'new')
    ln = Line.browse(int(pid_s)).exists() if pid_s.isdigit() else Line
    pnext = base + '&plan=' + (str(ln.id) if ln else 'new') + (('&d=' + str(params.get('d'))[:10]) if params.get('d') else '')
    MPIN1 = (P.get_param('iq.delivery_calendar_manager_pin') or '').strip()
    if not ADM:
        if len(MPIN1) < 8:
            inner = ('<h2>' + ('Nicht eingerichtet' if de else 'Not set up') + '</h2><p class="mut">'
                     + ('Es gibt noch keine Manager-PIN (Systemparameter iq.delivery_calendar_manager_pin, mindestens 8 Ziffern).' if de else 'No manager PIN yet (system parameter iq.delivery_calendar_manager_pin, at least 8 digits).') + '</p>')
        else:
            inner = ('<h2>' + ('Lieferung eintragen' if de else 'Add delivery') + '</h2><p class="mut">'
                     + ('Nur Führungskräfte. Bitte die Manager-PIN eingeben (dieselbe wie bei „Meine Stunden &amp; Urlaub → Führungskraft / Manager“).' if de else
                        'Managers only. Please enter the manager PIN (the same as in “My hours &amp; vacation → Manager”).') + '</p>'
                     + '<form method="post" action=""><input type="hidden" name="csrf_token" value="' + request.csrf_token() + '"><input type="hidden" name="key" value="' + KEY + '">'
                     + ('' if de else '<input type="hidden" name="lang" value="en">') + '<input type="hidden" name="emp" value="M"><input type="hidden" name="next" value="' + pesc(pnext) + '">'
                     + '<label>' + ('Manager-PIN' if de else 'Manager PIN') + '</label><input type="password" name="pin" inputmode="numeric" autocomplete="off" autofocus>'
                     + '<div class="btns"><button class="save">' + ('Weiter' if de else 'Continue') + '</button><a class="b" href="' + base.replace('&', '&amp;') + '">' + ('Abbrechen' if de else 'Cancel') + '</a></div></form>')
        response = presp(ppage(inner))
    else:
        act = params.get('act') if request.httprequest.method == 'POST' else ''
        who_txt = ('Kalender (Führungskraft)' if de else 'calendar (manager)')
        err = ''
        vals_in = {}
        if act == 'plan_del' and ln:
            card = ln.x_wareneingang_id
            txt = ('Geplante Lieferung gelöscht: ' if de else 'Planned delivery deleted: ') + (ln.x_product_text or '') + ' · ' + str(int(ln.x_qty or 0)) + ' · ' + (ln.x_date.strftime('%d.%m.%Y') if ln.x_date else '') + ' – ' + who_txt
            dm = ln.x_date.strftime('%Y-%m') if ln.x_date else ''
            ln.unlink()
            note(card, txt)
            note(card.x_studio_purchase_order if card else False, txt)
            response = request.make_response('', headers=[('Location', base + (('&m=' + dm) if dm else ''))], status=303)
        elif act == 'plan_done' and ln:
            ln.write({'x_done': True})
            txt = ('Geplante Lieferung als angekommen markiert: ' if de else 'Planned delivery marked as arrived: ') + (ln.x_product_text or '') + ' · ' + str(int(ln.x_qty or 0)) + ' · ' + (ln.x_date.strftime('%d.%m.%Y') if ln.x_date else '') + ' – ' + who_txt
            note(ln.x_wareneingang_id, txt)
            response = request.make_response('', headers=[('Location', base + (('&m=' + ln.x_date.strftime('%Y-%m')) if ln.x_date else ''))], status=303)
        else:
            response = False
            if act == 'plan_save':
                ds = str(params.get('date') or '')[:10]
                dd = False
                if len(ds) == 10 and ds[:4].isdigit() and ds[5:7].isdigit() and ds[8:10].isdigit():
                    try:
                        dd = datetime.date(int(ds[:4]), int(ds[5:7]), int(ds[8:10]))
                    except Exception:
                        dd = False
                qs = str(params.get('qty') or '').strip().replace('.', '').replace(',', '.')
                qty = 0.0
                try:
                    qty = float(qs) if qs else 0.0
                except Exception:
                    qty = 0.0
                po_txt = str(params.get('po') or '').strip()
                po = PO.search([('name', '=', po_txt.split(' ')[0])], limit=1) if po_txt else PO
                sup_txt = str(params.get('sup') or '').strip()
                sup = po.partner_id if po else (Partner.search([('name', '=ilike', sup_txt)], limit=1) or (Partner.search([('name', 'ilike', sup_txt)], limit=1) if sup_txt else Partner))
                ref = str(params.get('ref') or '').strip()[:60] or ((po.partner_ref or '') if po else '')
                prod = str(params.get('prod') or '').strip()[:120]
                ship = str(params.get('ship') or '').strip()[:120]
                vals_in = {'date': ds, 'qty': str(params.get('qty') or ''), 'po': po_txt, 'sup': sup_txt, 'ref': ref, 'prod': prod, 'ship': ship}
                if not dd:
                    err = 'Bitte ein Datum wählen.' if de else 'Please choose a date.'
                elif qty <= 0:
                    err = 'Bitte die Stückzahl eingeben.' if de else 'Please enter the quantity.'
                elif po_txt and not po:
                    err = ('Bestellung „' if de else 'Purchase order “') + po_txt + ('“ nicht gefunden.' if de else '” not found.')
                elif not po and not sup and not ref:
                    err = 'Ohne Bestellung bitte Lieferant oder Auftragsnr. angeben.' if de else 'Without a purchase order please enter supplier or order no.'
                elif not prod:
                    err = 'Bitte das Produkt eingeben.' if de else 'Please enter the product.'
                else:
                    card = ln.x_wareneingang_id if ln else WE
                    if po and (not card or card.x_studio_purchase_order != po):
                        card = WE.search([('x_studio_purchase_order', '=', po.id)], limit=1)
                        if not card:
                            card = WE.create({'x_name': po.name, 'x_studio_purchase_order': po.id, 'x_studio_supplier': po.partner_id.id, 'x_supplier_ref': po.partner_ref or False})
                    if not card and ref:
                        card = WE.search([('x_supplier_ref', '=', ref)], limit=1)
                    if not card:
                        card = WE.create({'x_name': (ref + ' – ' if ref else '') + prod, 'x_studio_supplier': sup.id if sup else False, 'x_supplier_ref': ref or False})
                    vals = {'x_wareneingang_id': card.id, 'x_partner_id': (sup.commercial_partner_id.id if sup else False), 'x_supplier_ref': ref or False,
                            'x_product_text': prod, 'x_qty': qty, 'x_date': dd, 'x_shipment': ship or False, 'x_done': False,
                            'x_name': ' · '.join([x for x in [ref, prod, ship] if x])}
                    txt = (str(int(qty)) + (' Stk. ' if de else ' pcs ') + prod + ' am ' + dd.strftime('%d.%m.%Y') + ((' · ' + ship) if ship else '') + ' – ' + who_txt)
                    if ln:
                        ln.write(vals)
                        txt = ('Geplante Lieferung geändert: ' if de else 'Planned delivery changed: ') + txt
                    else:
                        ln = Line.create(vals)
                        txt = ('Geplante Lieferung eingetragen: ' if de else 'Planned delivery added: ') + txt
                    note(card, txt)
                    note(po if po else card.x_studio_purchase_order, txt)
                    response = request.make_response('', headers=[('Location', base + '&m=' + dd.strftime('%Y-%m'))], status=303)
            if not response:
                # ---------------- the form
                if not vals_in:
                    if ln:
                        vals_in = {'date': ln.x_date.strftime('%Y-%m-%d') if ln.x_date else '', 'qty': str(int(ln.x_qty or 0)),
                                   'po': (ln.x_wareneingang_id.x_studio_purchase_order.name or '') if ln.x_wareneingang_id else '',
                                   'sup': ln.x_partner_id.name or '', 'ref': ln.x_supplier_ref or '', 'prod': ln.x_product_text or '', 'ship': ln.x_shipment or ''}
                    else:
                        d0 = str(params.get('d') or '')[:10]
                        vals_in = {'date': d0 if len(d0) == 10 else datetime.date.today().strftime('%Y-%m-%d'), 'qty': '', 'po': str(params.get('po') or ''), 'sup': '', 'ref': '', 'prod': '', 'ship': ''}
                pos = PO.search([('state', 'in', ['purchase', 'done']), ('receipt_status', '!=', 'full')], order='date_order desc', limit=200)
                pjson = []
                popts = ''
                for o in pos:
                    prods = []
                    for ol in o.order_line:
                        if ol.product_id and ol.product_id.type != 'service':
                            nm = (ol.product_id.product_tmpl_id.name or '').split(' – ')[0]
                            if nm and nm not in prods:
                                prods.append(nm)
                    pjson.append(pjs(o.name) + ':[' + pjs(o.partner_id.commercial_partner_id.name) + ',' + pjs(o.partner_ref or '') + ',[' + ','.join([pjs(x) for x in prods]) + ']]')
                    popts += '<option value="' + pesc(o.name) + '">' + pesc((o.partner_id.commercial_partner_id.name or '') + ((' · ' + o.partner_ref) if o.partner_ref else '') + ((' · ' + prods[0]) if prods else '')) + '</option>'
                sups = Partner.search([('supplier_rank', '>', 0)], order='name', limit=300) if 'supplier_rank' in Partner.fields_get(['supplier_rank']) else Partner
                sopts = ''.join(['<option value="' + pesc(x.name) + '">' for x in sups])
                editing = bool(ln)
                inner = ('<h2>' + (('Lieferung bearbeiten' if de else 'Edit delivery') if editing else ('Lieferung eintragen' if de else 'Add delivery')) + '</h2>'
                         + '<p class="mut" style="margin:0">' + ('Erscheint im Kalender. Mit Bestellung auch im Wareneingang dieser Bestellung (Lieferplan).' if de else
                                                                  'Shows in the calendar. With a purchase order also in that order’s goods receipt (delivery schedule).') + '</p>'
                         + ('<p class="err">' + pesc(err) + '</p>' if err else '')
                         + '<form method="post" action="" id="pf"><input type="hidden" name="csrf_token" value="' + request.csrf_token() + '"><input type="hidden" name="key" value="' + KEY + '">'
                         + ('' if de else '<input type="hidden" name="lang" value="en">') + '<input type="hidden" name="lid" value="' + (str(ln.id) if ln else '') + '"><input type="hidden" name="plan" value="' + (str(ln.id) if ln else 'new') + '">'
                         + '<input type="hidden" name="act" id="act" value="plan_save">'
                         + '<div class="two"><div><label>' + ('Datum der Lieferung' if de else 'Delivery date') + '</label><input type="date" name="date" required value="' + pesc(vals_in['date']) + '"></div>'
                         + '<div><label>' + ('Menge (Stück)' if de else 'Quantity (pcs)') + '</label><input type="number" name="qty" min="1" step="1" inputmode="numeric" required value="' + pesc(vals_in['qty']) + '"></div></div>'
                         + '<label>' + ('Bestellung (optional)' if de else 'Purchase order (optional)') + '</label><input name="po" id="po" list="polist" autocomplete="off" placeholder="' + ('z. B. P00076 – leer lassen, wenn es keine gibt' if de else 'e.g. P00076 – leave empty if there is none') + '" value="' + pesc(vals_in['po']) + '">'
                         + '<datalist id="polist">' + popts + '</datalist>'
                         + '<div class="two"><div><label>' + ('Lieferant' if de else 'Supplier') + '</label><input name="sup" id="sup" list="suplist" autocomplete="off" value="' + pesc(vals_in['sup']) + '"><datalist id="suplist">' + sopts + '</datalist></div>'
                         + '<div><label>' + ('Auftragsnr. Lieferant' if de else 'Supplier order no.') + '</label><input name="ref" id="ref" autocomplete="off" placeholder="z. B. 167904" value="' + pesc(vals_in['ref']) + '"></div></div>'
                         + '<label>' + ('Produkt' if de else 'Product') + '</label><input name="prod" id="prod" list="prodlist" autocomplete="off" required value="' + pesc(vals_in['prod']) + '"><datalist id="prodlist"></datalist>'
                         + '<label>' + ('Notiz / Sendung' if de else 'Note / shipment') + '</label><input name="ship" autocomplete="off" placeholder="' + ('z. B. Nacharbeit Charge 1' if de else 'e.g. rework batch 1') + '" value="' + pesc(vals_in['ship']) + '">'
                         + '<small class="h">' + ('Wird im Kalender unter dem Produkt angezeigt.' if de else 'Shown in the calendar below the product.') + '</small>'
                         + '<div class="btns"><button class="save" type="submit">' + ('Speichern' if de else 'Save') + '</button>'
                         + (('<button class="ok" type="submit" onclick="document.getElementById(\'act\').value=\'plan_done\'">' + ('✓ Angekommen' if de else '✓ Arrived') + '</button>'
                             + '<button class="del" type="submit" onclick="if(!confirm(\'' + ('Diese geplante Lieferung löschen?' if de else 'Delete this planned delivery?') + '\'))return false;document.getElementById(\'act\').value=\'plan_del\'">' + ('Löschen' if de else 'Delete') + '</button>') if editing else '')
                         + '<a class="b" href="' + base.replace('&', '&amp;') + '">' + ('Abbrechen' if de else 'Cancel') + '</a></div></form>'
                         + '<div class="inf">' + ('Mehrere Teillieferungen? Jede Teillieferung einzeln eintragen (eigenes Datum + Menge). Wenn sie da ist: „✓ Angekommen“.' if de else
                                                  'Several partial deliveries? Add each one separately (own date + quantity). When it has arrived: “✓ Arrived”.') + '</div>'
                         + '<script>var POS={' + ','.join(pjson) + '};(function(){var po=document.getElementById("po"),sup=document.getElementById("sup"),ref=document.getElementById("ref"),prod=document.getElementById("prod"),dl=document.getElementById("prodlist");'
                         + 'function fill(first){var k=(po.value||"").trim().split(" ")[0],o=POS[k];dl.innerHTML="";if(!o)return;sup.value=o[0];sup.readOnly=true;if(!ref.value||!first)ref.value=o[1]||ref.value;'
                         + 'o[2].forEach(function(n){var x=document.createElement("option");x.value=n;dl.appendChild(x)});if(o[2].length===1&&!prod.value)prod.value=o[2][0]}'
                         + 'po.addEventListener("change",function(){sup.readOnly=false;fill(false)});po.addEventListener("input",function(){if(POS[(po.value||"").trim()])fill(false);else sup.readOnly=false});fill(true)})();</script>')
                response = presp(ppage(inner))
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
        return ('<a class="ol ' + cls + '" target="_blank" href="/odoo/' + model + '/' + str(rid) + '" title="' + ('In Odoo öffnen' if de else 'Open in Odoo') + '">' + label + ' <span class="arr">↗</span></a>')

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
        'usedv': 'Genommen + geplant' if de else 'Taken + planned', 'ofpl': 'davon geplant' if de else 'of which planned',
        'allocreq': 'Urlaubsanspruch (Zuteilung)' if de else 'Vacation entitlement (allocation)',
        'otreq': 'Überstunden zu genehmigen' if de else 'Overtime to approve', 'days_n': 'Tage' if de else 'days',
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
    MECSS = ('<style>.me-k{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-bottom:14px}.me-k.two{grid-template-columns:repeat(2,minmax(0,1fr))}'
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
             '.pname{display:flex;align-items:center;gap:14px;background:#fff;border:1px solid var(--line);border-left:5px solid var(--red);border-radius:8px;padding:12px 16px;margin:0 0 14px}'
             '.pname i{flex:none;width:46px;height:46px;border-radius:50%;background:#151515;color:#fff;display:flex;align-items:center;justify-content:center;font:800 17px Arial;font-style:normal}'
             '.pname b{display:block;font:800 22px/1.2 Arial}.pname span{color:var(--mut);font-size:13px}.pname .pl{margin-left:auto;font-size:13px}'
             '@media(max-width:700px){.pname b{font-size:18px}.pname .pl{display:none}}'
             '.who{color:#bdbdbd;font-size:12.5px}.pf{max-width:400px;margin:30px auto;background:#fff;border:1px solid var(--line);border-radius:10px;padding:22px}'
             '.pf h2{margin:0 0 14px;font:800 18px Arial}.pf label{display:block;font-weight:700;margin:10px 0 4px}'
             '.pf select,.pf input{width:100%;padding:11px;border:1px solid #d1d5db;border-radius:6px;font-size:16px;background:#fff}'
             '.pf button{width:100%;margin-top:14px;padding:12px;border:0;border-radius:6px;background:var(--red);color:#fff;font:700 15px Arial;cursor:pointer}'
             '.pf .e{color:var(--red);font-weight:700;margin:12px 0 0}'
             '.me-k~.box,.wrap>.box,.box.team{overflow-x:auto;min-width:0}.me-g>*{min-width:0}.team{overflow-x:auto}.team table{min-width:860px}.team tr:hover td{background:#fafaf8}.team .warn td{background:#fff7ed}'
             '.hint{color:var(--mut);font-size:12px;margin:8px 0 0}'
             '.ih{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between;margin-bottom:8px}.ih h3{margin:0}.ik{display:flex;gap:8px;flex-wrap:wrap;align-items:center}'
             '.ik .k{background:#f3f4f6;border-radius:6px;padding:5px 10px;font-size:12.5px}.ik .k.red{background:#fee2e2;color:#991b1b}'
             '.lall{background:#151515;color:#fff!important;text-decoration:none;border-radius:6px;padding:7px 12px;font:700 13px Arial}'
             '.sh{display:flex;justify-content:space-between;align-items:baseline;gap:10px;flex-wrap:wrap;margin:4px 0 8px}.sh h2{margin:0;font:800 13px Arial;letter-spacing:1px;text-transform:uppercase}.sh span{color:var(--mut);font-size:12px}'
             '.dgrd{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-bottom:16px}.dcd{display:block;text-decoration:none;color:var(--fg);background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 16px}'
             '.dcd small{display:block;font:700 11px Arial;letter-spacing:1px;text-transform:uppercase;color:var(--mut)}.dcd b{display:block;font:800 30px/1.15 Arial;margin:4px 0 2px}.dcd span{font-size:13px;color:var(--mut)}a.dcd:hover{outline:2px solid #151515;outline-offset:-1px}'
             '.dcd.red{background:#fdecea;border-color:#f3b4b0;border-left:6px solid #b91c1c}.dcd.red b,.dcd.red small,.dcd.red span{color:#991b1b}'
             '.dcd.amb{background:#fff7e6;border-color:#f6d28b;border-left:6px solid #d97706}.dcd.amb b,.dcd.amb small,.dcd.amb span{color:#92400e}'
             '.dcd.ok{background:#ecfdf3;border-color:#a7e3bd;border-left:6px solid #16a34a}.dcd.ok b,.dcd.ok small,.dcd.ok span{color:#166534}'
             '.dcd.dd{background:#f7fbf8}.dcd.dd b{color:#15803d}.dcd.nt b{color:var(--fg)}'
             '.agb{display:flex;height:30px;border-radius:6px;overflow:hidden;margin:6px 0 8px;gap:2px}.ag{display:flex;align-items:center;padding:0 8px;min-width:6px;overflow:hidden;white-space:nowrap;font:700 11.5px Arial}.ag span{overflow:hidden;text-overflow:ellipsis}'
             '.a0{background:#e5e7eb;color:#374151}.a1{background:#fde68a;color:#78350f}.a2{background:#fca5a5;color:#7f1d1d}.a3{background:#b91c1c;color:#fff}'
             '.agl{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:12.5px;color:var(--mut);margin-bottom:6px}.agl i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:-1px}.agl b{color:var(--fg)}'
             'h4.sub{margin:12px 0 2px;font:700 11px Arial;letter-spacing:1px;text-transform:uppercase;color:var(--mut)}'
             '.fl{display:inline-block;font:700 11px Arial;border-radius:999px;padding:3px 9px;white-space:nowrap;margin:1px 0}.fl-r{background:#b91c1c;color:#fff}.fl-y{background:#fde68a;color:#78350f}.fl-g{background:#dcfce7;color:#166534}.fl-op{background:#fff7e6;color:#92400e;border:1px solid #f6d28b}'
             '.team tr.rf td{background:#fff5f5}.team tr.rf td:first-child{box-shadow:inset 4px 0 0 #b91c1c}.team tr.yf td{background:#fffbeb}.team tr.yf td:first-child{box-shadow:inset 4px 0 0 #d97706}.amb{color:#b45309;font-weight:700}td.neg{font-weight:700}'
             '@media(max-width:700px){.dgrd{grid-template-columns:1fr}.dgrd.dsm{grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}.dsm .dcd{padding:9px 8px}.dsm .dcd b{font-size:20px}.dsm .dcd small{font-size:9.5px;letter-spacing:.3px}.dsm .dcd span{font-size:11px}.dcd b{font-size:26px}.ag span{display:none}}'
             '.dgrd.d4{grid-template-columns:repeat(4,minmax(0,1fr))}.fl-r1{background:#f3f4f6;color:#374151}small.rd{display:block;color:var(--mut);font-size:11px;margin-top:2px}'
             '.box.m3b{border:1px solid #f3b4b0;border-left:6px solid #b91c1c;margin-bottom:16px}.box.m3b h3{color:#991b1b}.team table.ivm{min-width:0}'
             '@media(max-width:980px){.dgrd.d4{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:700px){.ivm th:nth-child(3),.ivm td:nth-child(3){display:none}}'
             '.st-nd{background:#e5e7eb;color:#374151}.team table.ivc{min-width:0}'
             '@media(max-width:700px){.team table.ivt{min-width:0}.ivt th:nth-child(3),.ivt td:nth-child(3),.ivt th:nth-child(4),.ivt td:nth-child(4),.ivt th:nth-child(5),.ivt td:nth-child(5),.ivt th:nth-child(6),.ivt td:nth-child(6),.ivt th:nth-child(9),.ivt td:nth-child(9){display:none}.ivt td,.ivt th{padding-left:4px;padding-right:4px;font-size:12.5px}.ivt td:first-child{white-space:nowrap}.ivc th:nth-child(2),.ivc td:nth-child(2){display:none}.ivt th{letter-spacing:0}.ih .lall{width:100%;text-align:center}}'
             '.fts{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 12px}.ft{padding:6px 12px;border-radius:999px;background:#f3f4f6;color:#111;text-decoration:none;font-size:13px}.ft.on{background:#151515;color:#fff}'
             '@media(max-width:980px){.me-k{grid-template-columns:repeat(2,minmax(0,1fr))}.me-g{grid-template-columns:1fr}}'
             '@media(max-width:700px){table.rqt td,table.rqt th{font-size:12.5px;padding:6px 3px}table.rqt .st{font-size:10px;padding:2px 5px;white-space:normal;display:inline-block;max-width:92px;text-align:center}}'
             '.lvf{max-width:560px}.lvf textarea{width:100%;padding:11px;border:1px solid #d1d5db;border-radius:6px;font:15px Arial}.lvf input[type=file]{padding:8px}.lvf [hidden]{display:none!important}'
             '.rqh{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:6px}.rqh h3{margin:0}'
             '.lreq{background:var(--red);color:#fff!important;text-decoration:none;border-radius:6px;padding:9px 14px;font:700 14px Arial;white-space:nowrap}'
             'form.wd{display:block;margin:4px 0 0}form.wd button{border:1px solid #d1d5db;background:#fff;border-radius:5px;padding:3px 9px;font:700 11.5px Arial;color:#374151;cursor:pointer}form.wd button:hover{border-color:var(--red);color:var(--red)}'
             '.lvt{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.pf .lt{position:relative;display:flex;flex-direction:column;gap:3px;border:2px solid #e5e7eb;border-radius:10px;padding:12px;cursor:pointer;margin:0;font-weight:400;background:#fff}'
             '.pf .lt input{position:absolute;opacity:0;width:1px;height:1px;pointer-events:none}.lt .ic svg{width:28px;height:28px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}'
             '.lt .ic{display:block;height:28px;margin-bottom:4px}.lt b{font:700 15px Arial}.lt small{color:var(--mut);font-size:12.5px;line-height:1.3}.lt-vac .ic{color:#d97706}.lt-ot .ic{color:#2563eb}.lt-sick .ic{color:#dc2626}.lt-oth .ic{color:#6b7280}'
             '.pf .lt.on{border-color:var(--red);background:#fff5f5;box-shadow:0 0 0 3px rgba(185,28,28,.12)}.lhint{background:#f3f4f6;border-radius:8px;padding:10px 12px;font-size:13.5px;margin:10px 0 0;line-height:1.4}'
             '.lmsg{background:#ecfdf3;border:1px solid #a7e3bd;border-left:6px solid #16a34a;color:#166534;border-radius:8px;padding:12px 14px;margin:0 0 14px;font-weight:700}.lmsg.bad{background:#fdecea;border-color:#f3b4b0;border-left-color:#b91c1c;color:#991b1b}</style>')

    def shell(inner, who, refresh, mgr_back=False):
        nav = '<a href="' + hbase + '">' + T['back'] + '</a>'
        if mgr_back:
            nav += '<a href="' + hbase + '&amp;view=me">' + T['backteam'] + '</a>'
        if who:
            nav += '<a href="' + hbase + '&amp;melogout=1">' + T['out'] + '</a>'
        return (page_head(T['title'].replace('&amp;', '&')) + MECSS
                + ('<meta http-equiv="refresh" content="' + str(SESSION) + ';url=' + hbase + '&amp;melogout=1">' if refresh else '')
                + '</head><body><div class="top"><div class="in"><div class="brand"><img src="' + LOGO + '" alt="IQ Dogsport"><div><h1>' + (T['team'] if who == '*' else (IT['k'] if who == '**' else (esc(who) if who else T['title']))) + '</h1>'
                + ('<p class="who">' + T['title'] + '</p>' if who and who not in ('*', '**') else '') + '</div></div>'
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

    EF = Emp.fields_get(['allocation_display', 'allocation_remaining_display'])

    def fnum(s):
        try:
            return float(str(s or '0').replace(',', '.').split()[0])
        except Exception:
            return 0.0

    def vac_data(emp):
        allocs = Alloc.search([('employee_id', '=', emp.id), ('state', '=', 'validate')])
        al = Alloc.browse([a.id for a in allocs if a.date_from and a.date_from <= today and (not a.date_to or a.date_to >= today)
                           and a.holiday_status_id.id not in otypes.ids and not is_sick(a.holiday_status_id)])
        if not al:
            return []
        tids = al.mapped('holiday_status_id').ids
        start = min(al.mapped('date_from'))
        ends = [a.date_to for a in al if a.date_to]
        end = max(ends) if ends and len(ends) == len(al) else False
        ldom = [('employee_id', '=', emp.id), ('holiday_status_id', 'in', tids), ('state', 'in', ['confirm', 'validate1', 'validate']), ('request_date_from', '>=', start)]
        if end:
            ldom.append(('request_date_from', '<=', end))
        lvs = Leave.search(ldom)
        pl = sum([l.number_of_days for l in lvs if l.state == 'validate' and l.request_date_from > today])
        rq = sum([l.number_of_days for l in lvs if l.state != 'validate'])
        if 'allocation_display' in EF and 'allocation_remaining_display' in EF:
            ent = fnum(emp.allocation_display)
            left = fnum(emp.allocation_remaining_display)
        else:
            ent = sum(al.mapped('number_of_days'))
            left = ent - sum([l.number_of_days for l in lvs])
        return [{'t': al[0].holiday_status_id, 'ent': ent, 'left': left, 'used': ent - left, 'pl': pl, 'rq': rq, 'end': end, 'al': al}]

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
        kp = ('<div class="me-k two">'
              + '<div class="kpi' + (' red' if od['bal'] < 0 else '') + '"><small>' + T['ot_rem'] + '</small><b>' + L_('hr.employee', emp.id, hm(od['bal'], True) + ' ' + T['h'], mgr) + '</b><span>' + today.strftime('%d.%m.%Y') + '</span></div>'
              + '<div class="kpi' + (' op' if n_open else '') + '"><small>' + T['vac_rem'] + '</small><b>' + dnum(vleft) + ' ' + (T['day'] if vleft == 1 else T['days']) + '</b><span>'
              + (('<span class="opn">' + str(n_open) + ' ' + T['open_s'] + '</span> · ') if n_open else '') + valid_txt + '</span></div></div>')
        rr = ''
        for r in reqs:
            cls, lab = ST[r.state]
            if r.state == 'validate':
                lab = lab + ' · ' + (T['planned'] if r.request_date_from > today else T['taken'])
            rr += ('<tr class="rq-' + cls + '"><td>' + L_('hr.leave', r.id, dates(r), mgr) + '</td><td>' + esc(r.holiday_status_id.name) + '</td><td class="r">' + amount(r)
                   + '</td><td class="r"><span class="st st-' + cls + '">' + lab + '</span>'
                   + (('<form method="post" action="" class="wd" onsubmit="return confirm(' + chr(39) + ('Antrag wirklich zurückziehen?' if de else 'Really withdraw this request?') + chr(39) + ')">'
                       + '<input type="hidden" name="csrf_token" value="' + request.csrf_token() + '"><input type="hidden" name="key" value="' + KEY + '"><input type="hidden" name="view" value="me">'
                       + '<input type="hidden" name="lact" value="cancel"><input type="hidden" name="lid" value="' + str(r.id) + '">' + ('' if de else '<input type="hidden" name="lang" value="en">')
                       + '<button>' + ('Zurückziehen' if de else 'Withdraw') + '</button></form>') if (not mgr and r.state in ('confirm', 'validate1')) else '')
                   + '</td></tr>')
        reqbox = ('<div class="box" id="req"><div class="rqh"><h3>' + T['allreq'] + ' ' + str(today.year) + '</h3>' + ('' if mgr else '<a class="lreq" href="' + hbase + '&amp;view=me&amp;lnew=1">+ ' + ('Abwesenheit beantragen' if de else 'Request time off') + '</a>') + '</div>'
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
            alink = dnum(v['ent'])
            vac_html += ('<div class="box"><h3>' + esc(v['t'].name) + (' · ' + T['valid'] + ' ' + v['end'].strftime('%d.%m.%Y') if v['end'] else '') + '</h3><table>'
                         + '<tr><td>' + T['ent'] + '</td><td class="r">' + alink + '</td></tr>'
                         + '<tr><td>' + T['usedv'] + '</td><td class="r">' + dnum(v['used']) + '</td></tr>'
                         + ('<tr><td class="mut">' + T['ofpl'] + '</td><td class="r mut">' + dnum(v['pl']) + '</td></tr>' if v['pl'] else '')
                         + ('<tr><td>' + T['req'] + '</td><td class="r"><span class="st st-op">' + dnum(v['rq']) + '</span></td></tr>' if v['rq'] else '')
                         + '<tr class="sum"><td>' + T['left'] + '</td><td class="r">' + dnum(v['left']) + ' ' + (T['day'] if v['left'] == 1 else T['days']) + '</td></tr></table></div>')
        if not vac_html:
            vac_html = '<div class="box"><h3>' + T['vac'] + '</h3><p class="mut" style="margin:0">' + T['novac'] + '</p></div>'
        parts = (emp.name or '').split()
        ini = ((parts[0][0] if parts else '?') + (parts[-1][0] if len(parts) > 1 else '')).upper()
        top = ('<div class="pname"><i>' + esc(ini) + '</i><div><b>' + esc(emp.name) + '</b><span>' + (emp.job_title and esc(emp.job_title) + ' · ' or '')
               + T['title'] + ' · ' + today.strftime('%d.%m.%Y') + '</span></div>'
               + ('<span class="pl">' + olink('hr.employee', emp.id, T['empform']) + '</span>' if mgr else '') + '</div>')
        return top + kp + reqbox + '<div class="me-g"><div class="col">' + calc + monbox + usebox + '</div><div class="col">' + vac_html + '</div></div>'

    # ------------------------------------------------------------------ manager: posted customer invoices not paid yet
    AM = env['account.move'].sudo()
    INV_DOM = [('move_type', '=', 'out_invoice'), ('state', '=', 'posted'), ('payment_state', 'in', ['not_paid', 'partial'])]
    IT = {
        'h': 'Offene Rechnungen (gebucht, nicht bezahlt)' if de else 'Unpaid invoices (posted, not paid)',
        'k': 'Offene Rechnungen' if de else 'Unpaid invoices', 'od': 'überfällig' if de else 'overdue',
        'inv': 'Rechnung' if de else 'Invoice', 'cust': 'Kunde' if de else 'Customer', 'date': 'Datum' if de else 'Date',
        'due': 'Fällig' if de else 'Due', 'days': 'Tage' if de else 'Days', 'total': 'Betrag' if de else 'Total', 'open': 'Offen' if de else 'Open',
        'np': 'Nicht bezahlt' if de else 'Not paid', 'pp': 'Teilweise bezahlt' if de else 'Partly paid', 'all': 'Alle %n anzeigen' if de else 'Show all %n',
        'none': 'Keine offenen Rechnungen.' if de else 'No unpaid invoices.', 'sum': 'Summe offen' if de else 'Total open',
        'bycust': 'Nach Kunde' if de else 'By customer', 'n': 'Rechnungen' if de else 'invoices', 'odays': 'Überfällig' if de else 'Overdue',
        'f_all': 'Alle' if de else 'All', 'f_od': 'Überfällig' if de else 'Overdue', 'f_nd': 'Noch nicht fällig' if de else 'Not due yet',
        'hint': 'Klick auf die Rechnungsnummer öffnet die Rechnung in Odoo (Odoo-Login nötig).' if de else 'Click the invoice number to open it in Odoo (Odoo login needed).',
    }

    DT = {
        'now': 'Jetzt erledigen' if de else 'Act now', 'now_l': 'Rot = sofort · Gelb = bald · Grün = erledigt / OK' if de else 'Red = now · Yellow = soon · Green = done / OK',
        'od_inv': 'Überfällige Rechnungen' if de else 'Overdue invoices', 'oldest': 'älteste' if de else 'oldest', 'days': 'Tage' if de else 'days',
        'no_od': 'Keine überfällig' if de else 'None overdue', 'appr': 'Anträge genehmigen' if de else 'Requests to approve', 'none': 'Nichts offen' if de else 'Nothing open',
        'since': 'ältester seit' if de else 'oldest since', 'flags': 'Team-Hinweise' if de else 'Team alerts', 'allok': 'Alles in Ordnung' if de else 'All fine',
        'done': 'Schon erledigt (letzte 30 Tage)' if de else 'Done (last 30 days)', 'paid': 'Zahlungen eingegangen' if de else 'Payments received',
        'decided': 'Anträge entschieden' if de else 'Requests decided', 'apprd': 'genehmigt' if de else 'approved', 'refd': 'abgelehnt' if de else 'refused',
        'opentot': 'Offene Rechnungen gesamt' if de else 'Open invoices total', 'age': 'Offene Rechnungen nach Alter' if de else 'Open invoices by age',
        'nd': 'nicht fällig' if de else 'not due', 'b1': '1–30 Tage' if de else '1–30 days', 'b2': '31–90 Tage' if de else '31–90 days', 'b3': 'über 90 Tage' if de else 'over 90 days',
        'top': 'Am dringendsten' if de else 'Most urgent', 'f_neg': 'Minus-Saldo' if de else 'Negative balance', 'f_novac': 'Kein Urlaub übrig' if de else 'No vacation left',
        'f_hi': 'Sehr viel Plus' if de else 'Very high overtime', 'f_left': 'Viel Resturlaub' if de else 'Much vacation left', 'ok': 'OK',
        'note': 'Hinweis' if de else 'Alert',
        'rem': 'Mahnstufe' if de else 'Reminder', 'r1': 'Erinnerung' if de else 'Reminder', 'r2': '1. Mahnung' if de else '1st reminder', 'r3': '2. Mahnung' if de else '2nd reminder',
        'm3c': 'Nach 2. Mahnung unbezahlt' if de else 'Unpaid after 2nd reminder', 'm3h': 'Nach 3 Erinnerungen weiter unbezahlt – bitte selbst nachfassen' if de else 'Still unpaid after 3 reminders – please follow up',
        'm3none': 'Keine' if de else 'None', 'sent': 'verschickt am' if de else 'sent on', 'f_m3': '2. Mahnung' if de else '2nd reminder', 'since_s': 'seit' if de else 'for',
        'm3hint': 'Der Kunde hat Erinnerung, 1. und 2. Mahnung bekommen (automatisch). Florian und Patricia haben dazu eine Aufgabe in Odoo.' if de else 'The customer got all 3 automatic reminders. Florian and Patricia have a To-Do in Odoo.', 'chk': 'prüfen' if de else 'review',
    }

    def eur(v):
        s = '{:,.2f}'.format(v or 0)
        return (s.replace(',', '#').replace('.', ',').replace('#', '.') if de else s) + ' €'

    REM = {}

    def inv_rows(invs):
        out = ''
        for mv in invs:
            due = mv.invoice_date_due or mv.invoice_date
            dd = (today - due).days if due else 0
            out += ('<tr class="' + ('rq-op' if dd > 0 else '') + '"><td>' + olink('account.move', mv.id, esc(mv.name)) + '</td><td>' + esc(mv.partner_id.commercial_partner_id.name or mv.partner_id.name or '') + '</td>'
                    + '<td class="r">' + (mv.invoice_date.strftime('%d.%m.%Y') if mv.invoice_date else '') + '</td><td class="r">' + (due.strftime('%d.%m.%Y') if due else '') + '</td>'
                    + '<td class="r ' + ('neg' if dd > 0 else 'mut') + '">' + (str(dd) + (' Tage' if de else ' days') if dd > 0 else '–') + '</td>'
                    + '<td class="r">' + eur(mv.amount_total_signed) + '</td><td class="r' + (' neg' if dd > 0 else '') + '"><b>' + eur(mv.amount_residual_signed) + '</b></td>'
                    + '<td class="r">' + rem_chip(mv) + '</td>'
                    + '<td class="r"><span class="st ' + ('st-no' if dd > 30 else ('st-op' if dd > 0 else 'st-nd')) + '">' + (IT['pp'] if mv.payment_state == 'partial' else IT['np']) + '</span></td></tr>')
        return out

    def rem_chip(mv):
        r = REM.get(mv.id)
        if not r:
            return '<span class="mut">–</span>'
        return ('<span class="fl ' + ['', 'fl-r1', 'fl-y', 'fl-r'][r[0]] + '" title="' + DT['sent'] + ' ' + r[1].strftime('%d.%m.%Y') + '">' + DT['r' + str(r[0])] + '</span>'
                + '<small class="rd">' + r[1].strftime('%d.%m.') + '</small>')

    def inv_head():
        return ('<tr><th>' + IT['inv'] + '</th><th>' + IT['cust'] + '</th><th class="r">' + IT['date'] + '</th><th class="r">' + IT['due'] + '</th><th class="r">' + IT['odays']
                + '</th><th class="r">' + IT['total'] + '</th><th class="r">' + IT['open'] + '</th><th class="r">' + DT['rem'] + '</th><th class="r">Status</th></tr>')

    def inv_data():
        invs = AM.search(INV_DOM)
        REM.clear()
        if invs:
            for m in env['mail.message'].sudo().search([('model', '=', 'account.move'), ('res_id', 'in', invs.ids), ('body', 'ilike', 'IQ-REMINDER-')], order='date asc'):
                b = str(m.body or '')
                n = 3 if 'IQ-REMINDER-3' in b else (2 if 'IQ-REMINDER-2' in b else (1 if 'IQ-REMINDER-1' in b else 0))
                if n and n >= (REM.get(m.res_id) or [0])[0]:
                    REM[m.res_id] = [n, m.date.date() if m.date else today]
        invs = sorted(invs, key=lambda mv: (-(REM.get(mv.id) or [0])[0], mv.invoice_date_due or mv.invoice_date or today))
        od = [mv for mv in invs if (mv.invoice_date_due or mv.invoice_date or today) < today]
        return invs, od

    def inv_box(invs, od):
        tot = sum([mv.amount_residual_signed for mv in invs])
        allurl = hbase + '&amp;view=me&amp;inv=all'
        if not invs:
            return '<div class="box inv" id="inv" style="margin-top:14px"><h3>' + IT['h'] + '</h3><p class="mut" style="margin:0">' + IT['none'] + '</p></div>'
        bk = [0.0, 0.0, 0.0, 0.0]
        for mv in invs:
            dd = (today - (mv.invoice_date_due or mv.invoice_date or today)).days
            bk[0 if dd <= 0 else (1 if dd <= 30 else (2 if dd <= 90 else 3))] += mv.amount_residual_signed
        lab = [DT['nd'], DT['b1'], DT['b2'], DT['b3']]
        cls = ['a0', 'a1', 'a2', 'a3']
        bar = ''.join(['<div class="ag ' + cls[i] + '" style="flex:' + str(max(bk[i], 0.0001)) + '" title="' + lab[i] + ': ' + eur(bk[i]) + '"><span>' + ((lab[i] + ' · ' + eur(bk[i])) if bk[i] >= 0.15 * sum(bk) else '') + '</span></div>' for i in range(4) if bk[i] > 0])
        leg = ''.join(['<span class="lgi"><i class="' + cls[i] + '"></i>' + lab[i] + ' <b>' + eur(bk[i]) + '</b></span>' for i in range(4)])
        return ('<div class="box inv" id="inv" style="margin-top:14px"><div class="ih"><h3>' + DT['age'] + '</h3><div class="ik"><span class="k">' + str(len(invs)) + ' ' + IT['n'] + ' · <b>' + eur(tot) + '</b></span>'
                + '<a class="lall" href="' + allurl + '">' + IT['all'].replace('%n', str(len(invs))) + ' →</a></div></div>'
                + '<div class="agb">' + bar + '</div><div class="agl">' + leg + '</div>'
                + '<h4 class="sub">' + DT['top'] + '</h4><div class="team"><table class="rqt ivt">' + inv_head() + inv_rows(invs[:5]) + '</table></div><p class="hint">' + IT['hint'] + '</p></div>')

    def render_invoices():
        invs, od = inv_data()
        flt = params.get('f') or 'all'
        if flt == 'od':
            rows = od
        elif flt == 'nd':
            rows = [mv for mv in invs if mv not in od]
        elif flt == 'm3':
            rows = [mv for mv in invs if (REM.get(mv.id) or [0])[0] >= 3]
        else:
            rows = invs
        tot = sum([mv.amount_residual_signed for mv in invs])
        tod = sum([mv.amount_residual_signed for mv in od])
        base_i = hbase + '&amp;view=me&amp;inv=all'
        tabs = ''.join(['<a class="ft' + (' on' if flt == fk else '') + '" href="' + base_i + '&amp;f=' + fk + '">' + fl + '</a>'
                        for fk, fl in [('all', IT['f_all'] + ' (' + str(len(invs)) + ')'), ('od', IT['f_od'] + ' (' + str(len(od)) + ')'), ('nd', IT['f_nd'] + ' (' + str(len(invs) - len(od)) + ')'), ('m3', DT['f_m3'] + ' (' + str(len([1 for k in REM if REM[k][0] >= 3])) + ')')]])
        per = {}
        for mv in invs:
            cn = mv.partner_id.commercial_partner_id.name or mv.partner_id.name or ''
            if cn not in per:
                per[cn] = [0, 0.0, 0.0]
            per[cn][0] += 1
            per[cn][1] += mv.amount_residual_signed
            if mv in od:
                per[cn][2] += mv.amount_residual_signed
        cust = sorted(per.items(), key=lambda kv: -kv[1][1])
        crow = ''.join(['<tr><td>' + esc(cn) + '</td><td class="r">' + str(v[0]) + '</td><td class="r"><b>' + eur(v[1]) + '</b></td><td class="r ' + ('neg' if v[2] else 'mut') + '">' + (eur(v[2]) if v[2] else '–') + '</td></tr>' for cn, v in cust])
        kp = ('<div class="me-k">'
              + '<div class="kpi"><small>' + IT['k'] + '</small><b>' + str(len(invs)) + '</b><span>' + eur(tot) + '</span></div>'
              + '<div class="kpi' + (' red' if od else '') + '"><small>' + IT['f_od'] + '</small><b>' + str(len(od)) + '</b><span>' + eur(tod) + '</span></div>'
              + '<div class="kpi"><small>' + IT['f_nd'] + '</small><b>' + str(len(invs) - len(od)) + '</b><span>' + eur(tot - tod) + '</span></div>'
              + '<div class="kpi"><small>' + IT['bycust'] + '</small><b>' + str(len(per)) + '</b><span>' + IT['cust'] + '</span></div></div>')
        return (kp + '<div class="box"><h3>' + IT['h'] + '</h3><div class="fts">' + tabs + '</div><div class="team"><table class="rqt ivt">' + inv_head() + inv_rows(rows) + '</table></div>'
                + '<p class="hint">' + IT['hint'] + '</p></div>'
                + '<div class="box" style="margin-top:14px"><h3>' + IT['bycust'] + '</h3><div class="team"><table class="ivc"><tr><th>' + IT['cust'] + '</th><th class="r">' + IT['n']
                + '</th><th class="r">' + IT['open'] + '</th><th class="r">' + IT['f_od'] + '</th></tr>' + crow + '</table></div></div>')

    # ------------------------------------------------------------------ manager: whole team on one page
    def render_team():
        allemp = Emp.search([], order='name asc')
        rows = []
        todo = []
        n_abs = 0
        n_neg = 0
        n_red = 0
        n_yel = 0
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
            vtk = sum([v['used'] for v in vd])
            dnm = '?view=me&amp;key=' + KEY + '&amp;emp=' + str(e.id) + ('' if de else '&amp;lang=en')
            if cur:
                absc = '<span class="st ' + ('st-sick' if is_sick(cur[0].holiday_status_id) else 'st-ok') + '">' + olink('hr.leave', cur[0].id, esc(cur[0].holiday_status_id.name) + ' ' + T['today']) + '</span>'
            elif nxt:
                absc = olink('hr.leave', nxt[0].id, nxt[0].request_date_from.strftime('%d.%m.') + ' ' + esc(nxt[0].holiday_status_id.name)) + (' <span class="st st-op">?</span>' if nxt[0].state != 'validate' else '')
            else:
                absc = '<span class="mut">–</span>'
            fl = []
            if od['bal'] < 0:
                fl.append(('r', DT['f_neg']))
            if vd and (vleft < 0 or (vleft <= 0 and [r for r in opn if not is_sick(r.holiday_status_id)])):
                fl.append(('r', DT['f_novac']))
            if od['bal'] > 100:
                fl.append(('y', DT['f_hi']))
            if vd and today.month >= 10 and vleft > 10:
                fl.append(('y', DT['f_left']))
            lvl = 0 if [f for f in fl if f[0] == 'r'] else (1 if fl else (2 if opn else 3))
            if lvl == 0:
                n_red += 1
            elif lvl == 1:
                n_yel += 1
            flagc = ''.join(['<span class="fl fl-' + f[0] + '">' + f[1] + '</span> ' for f in fl]) if fl else ('<span class="fl fl-op">' + DT['chk'] + '</span>' if opn else '<span class="fl fl-g">' + DT['ok'] + '</span>')
            balc = 'neg' if od['bal'] < 0 else ('amb' if od['bal'] > 100 else '')
            vacc = 'neg' if [f for f in fl if f[1] == DT['f_novac']] else ('amb' if [f for f in fl if f[1] == DT['f_left']] else '')
            rows.append((lvl, e.name, '<tr class="' + ['rf', 'yf', 'warn', ''][lvl] + '"><td><a class="nm" href="' + dnm + '">' + esc(e.name) + '</a></td><td>' + flagc + '</td>'
                         + '<td class="r ' + balc + '">' + olink('hr.employee', e.id, hm(od['bal'], True)) + '</td>'
                         + '<td class="r ' + vacc + '">' + (('<a class="ol" href="' + dnm + '#req">' + dnum(vleft) + ' / ' + dnum(vent) + '</a>') if vd else '<span class="mut">–</span>') + '</td>'
                         + '<td class="r">' + (('<a class="ol" href="' + dnm + '#req">' + dnum(vtk) + '</a>') if vd else '–') + '</td>'
                         + '<td class="r">' + (''.join([olink('hr.leave', r.id, '<span class="st st-op">' + r.request_date_from.strftime('%d.%m.') + '</span>') + ' ' for r in opn]) if opn else '<span class="mut">–</span>') + '</td>'
                         + '<td class="r">' + (dnum(sick) if sick else '<span class="mut">0</span>') + '</td>'
                         + '<td>' + absc + '</td></tr>'))
        rows = sorted(rows, key=lambda x: (x[0], x[1]))
        td = ''.join(['<tr class="rq-op"><td>' + esc(r.employee_id.name) + '</td><td>' + olink('hr.leave', r.id, dates(r)) + '</td><td>' + esc(r.holiday_status_id.name)
                      + '</td><td class="r">' + amount(r) + '</td><td class="r"><span class="st st-op">' + T['open_s'] + '</span></td></tr>' for r in sorted(todo, key=lambda r: r.request_date_from)])
        seen = [r.id for r in todo]
        for r in Leave.search([('state', 'in', ['confirm', 'validate1'])], order='request_date_from asc'):
            if r.id in seen:
                continue
            todo.append(r)
            td += ('<tr class="rq-op"><td>' + esc(r.employee_id.name) + '</td><td>' + olink('hr.leave', r.id, dates(r)) + '</td><td>' + esc(r.holiday_status_id.name)
                   + '</td><td class="r">' + amount(r) + '</td><td class="r"><span class="st st-op">' + T['open_s'] + '</span></td></tr>')
        n_alloc = 0
        for a in Alloc.search([('state', 'in', ['confirm', 'validate1'])]):
            n_alloc += 1
            td += ('<tr class="rq-op"><td>' + esc(a.employee_id.name or '') + '</td><td>' + olink('hr.leave.allocation', a.id, ((a.date_from.strftime('%d.%m.%Y') if a.date_from else '') + (' – ' + a.date_to.strftime('%d.%m.%Y') if a.date_to else '')) or '↗')
                   + '</td><td>' + T['allocreq'] + ' · ' + esc(a.holiday_status_id.name) + '</td><td class="r">+' + dnum(a.number_of_days) + ' ' + T['days_n'] + '</td><td class="r"><span class="st st-op">' + T['open_s'] + '</span></td></tr>')
        n_ot = 0
        OTM2 = 'hr.attendance.overtime.line' if 'hr.attendance.overtime.line' in env else ''
        if OTM2 and 'status' in env[OTM2].sudo().fields_get(['status']):
            otl = env[OTM2].sudo().search([('status', '=', 'to_approve')])
            ofg = env[OTM2].sudo().fields_get(['duration', 'manual_duration'])
            OTF = 'duration' if 'duration' in ofg else ('manual_duration' if 'manual_duration' in ofg else '')
            per = {}
            for o in otl:
                k2 = o.employee_id.id
                if k2 not in per:
                    per[k2] = [o.employee_id, 0.0, 0, o.date, o.date]
                per[k2][1] += (o[OTF] if OTF else 0.0) or 0.0
                per[k2][2] += 1
                per[k2][3] = min(per[k2][3], o.date) if o.date and per[k2][3] else (per[k2][3] or o.date)
                per[k2][4] = max(per[k2][4], o.date) if o.date and per[k2][4] else (per[k2][4] or o.date)
            for k2 in per:
                e2, hrs2, cnt2, d1, d2 = per[k2]
                n_ot += 1
                td += ('<tr class="rq-op"><td>' + esc(e2.name) + '</td><td>' + olink('hr.employee', e2.id, ((d1.strftime('%d.%m.%Y') if d1 else '') + (' – ' + d2.strftime('%d.%m.%Y') if d2 and d2 != d1 else '')))
                       + '</td><td>' + T['otreq'] + ' (' + str(cnt2) + ')</td><td class="r">' + hm(hrs2, True) + ' ' + T['h'] + '</td><td class="r"><span class="st st-op">' + T['open_s'] + '</span></td></tr>')
        n_todo = len(todo) + n_alloc + n_ot
        todobox = ('<div class="box" id="todo" style="margin-top:14px"><h3>' + T['todo'] + ' (' + str(n_todo) + ')</h3>' + ('<table class="rqt"><tr><th>' + T['employee'] + '</th><th>' + T['when'] + '</th><th>' + T['type'] + '</th><th class="r">' + T['amount'] + '</th><th class="r">Status</th></tr>' + td + '</table>' if td else '<p class="mut" style="margin:0">' + T['nothing'] + '</p>') + '</div>')
        teambox = ('<div class="box team" id="team" style="margin-top:14px"><h3>' + T['team'] + ' (' + str(len(allemp)) + ')</h3><table><tr><th>' + T['employee'] + '</th><th>' + DT['note'] + '</th><th class="r">' + T['ot_rem'] + '</th><th class="r">' + T['vac_rem'] + ' / ' + T['ent'] + '</th><th class="r">' + T['taken']
                   + '</th><th class="r">' + T['k_open'] + '</th><th class="r">' + T['sick'] + ' ' + str(today.year) + '</th><th>' + T['absnow'] + '</th></tr>' + ''.join([x[2] for x in rows]) + '</table>'
                   + '<p class="hint">' + T['hint'] + '</p></div>')
        sb = ''
        for r in sorted(soon, key=lambda r: r.request_date_from):
            cls = 'op' if r.state != 'validate' else ('sick' if is_sick(r.holiday_status_id) else 'ok')
            sb += ('<tr' + (' class="rq-op"' if cls == 'op' else '') + '><td>' + esc(r.employee_id.name) + '</td><td>' + olink('hr.leave', r.id, dates(r)) + '</td><td><span class="st st-' + cls + '">' + esc(r.holiday_status_id.name)
                   + (' · ' + T['open_s'] if cls == 'op' else '') + '</span></td><td class="r">' + amount(r) + '</td></tr>')
        soonbox = '<div class="box" style="margin-top:14px"><h3>' + T['next30'] + '</h3>' + ('<table class="rqt">' + sb + '</table>' if sb else '<p class="mut" style="margin:0">' + T['noabs'] + '</p>') + '</div>'
        invs, od = inv_data()
        tod = sum([mv.amount_residual_signed for mv in od])
        old = max([(today - (mv.invoice_date_due or mv.invoice_date or today)).days for mv in od]) if od else 0
        oldreq = min([r.request_date_from for r in todo if r.request_date_from] or [today])
        ac_inv = ('<a class="dcd ' + ('red' if od else 'ok') + '" href="' + hbase + '&amp;view=me&amp;inv=all&amp;f=od"><small>' + DT['od_inv'] + '</small><b>' + str(len(od)) + '</b><span>'
                  + ((eur(tod) + ' · ' + DT['oldest'] + ' ' + str(old) + ' ' + DT['days']) if od else DT['no_od']) + ' →</span></a>')
        ac_req = ('<a class="dcd ' + ('amb' if n_todo else 'ok') + '" href="#todo"><small>' + DT['appr'] + '</small><b>' + str(n_todo) + '</b><span>'
                  + ((DT['since'] + ' ' + oldreq.strftime('%d.%m.')) if n_todo and todo else (DT['none'] if not n_todo else '')) + ' ↓</span></a>')
        ac_tm = ('<a class="dcd ' + ('red' if n_red else ('amb' if n_yel else 'ok')) + '" href="#team"><small>' + DT['flags'] + '</small><b>' + str(n_red + n_yel) + '</b><span>'
                 + ((str(n_red) + ' ' + ('rot' if de else 'red') + ' · ' + str(n_yel) + ' ' + ('gelb' if de else 'yellow')) if n_red + n_yel else DT['allok']) + ' ↓</span></a>')
        m3 = [mv for mv in invs if (REM.get(mv.id) or [0])[0] >= 3]
        sm3 = sum([mv.amount_residual_signed for mv in m3])
        ac_m3 = ('<a class="dcd ' + ('red' if m3 else 'ok') + '" href="' + ('#m3' if m3 else hbase + '&amp;view=me&amp;inv=all&amp;f=m3') + '"><small>' + DT['m3c'] + '</small><b>' + str(len(m3)) + '</b><span>'
                 + (eur(sm3) if m3 else DT['m3none']) + (' ↓' if m3 else '') + '</span></a>')
        npo = []
        for r in arr_records(120):
            cdx = env['x_wareneingang'].sudo().browse(r['wid']).exists()
            if cdx and not cdx.x_studio_purchase_order and cdx.id not in npo:
                npo.append(cdx.id)
        ac_npo = ('<a class="dcd red" style="grid-column:1/-1" href="?key=' + KEY + '#nopo"><small>' + ICW + ('Ware ohne Bestellung angekommen' if de else 'Goods arrived without purchase order') + '</small><b>' + str(len(npo)) + '</b><span>'
                  + ('Bestellung anlegen (Lieferantenreferenz = Lieferschein-Nr.) →' if de else 'Create the purchase order (vendor reference = delivery note no.) →') + '</span></a>') if npo else ''
        act = '<div class="sh"><h2>' + DT['now'] + '</h2><span>' + DT['now_l'] + '</span></div><div class="dgrd d4">' + ac_npo + ac_m3 + ac_inv + ac_req + ac_tm + '</div>'
        m3rows = ''
        for mv in m3:
            r = REM[mv.id]
            m3rows += ('<tr class="rf"><td>' + olink('account.move', mv.id, esc(mv.name)) + '</td><td>' + esc(mv.partner_id.commercial_partner_id.name or mv.partner_id.name or '') + '</td>'
                       + '<td class="r">' + r[1].strftime('%d.%m.%Y') + '</td><td class="r neg">' + str((today - r[1]).days) + ' ' + DT['days'] + '</td>'
                       + '<td class="r neg"><b>' + eur(mv.amount_residual_signed) + '</b></td></tr>')
        m3box = ('<div class="box m3b" id="m3"><h3>' + DT['m3h'] + ' (' + str(len(m3)) + ')</h3><div class="team"><table class="rqt ivm"><tr><th>' + IT['inv'] + '</th><th>' + IT['cust'] + '</th><th class="r">' + DT['r3'] + ' ' + DT['sent']
                 + '</th><th class="r">' + ('Unbezahlt' if de else 'Unpaid') + '</th><th class="r">' + IT['open'] + '</th></tr>' + m3rows + '</table></div><p class="hint">' + DT['m3hint'] + ' ' + IT['hint'] + '</p></div>') if m3 else ''
        d30 = today - datetime.timedelta(days=30)
        npay = 0
        spay = 0.0
        if 'account.payment' in env:
            PayM = env['account.payment'].sudo()
            pf = PayM.fields_get(['state', 'amount_company_signed', 'amount', 'payment_type', 'partner_type', 'date'])
            pdom = [('payment_type', '=', 'inbound'), ('partner_type', '=', 'customer'), ('date', '>=', d30), ('state', 'not in', ['draft', 'cancel', 'canceled', 'rejected'])]
            pays = PayM.search(pdom)
            npay = len(pays)
            spay = sum(pays.mapped('amount_company_signed' if 'amount_company_signed' in pf else 'amount'))
        dl = Leave.search([('state', 'in', ['validate', 'refuse']), ('write_date', '>=', datetime.datetime.combine(d30, datetime.time(0, 0)))])
        n_ap = len([r for r in dl if r.state == 'validate'])
        n_rf = len(dl) - n_ap
        if OTM2 and 'status' in env[OTM2].sudo().fields_get(['status']):
            dol = env[OTM2].sudo().search([('status', 'in', ['approved', 'refused']), ('write_date', '>=', datetime.datetime.combine(d30, datetime.time(0, 0))), ('manual_duration', '!=', 0)]) if 'manual_duration' in env[OTM2].sudo().fields_get(['manual_duration']) else []
            n_ap += len([o for o in dol if o.status == 'approved'])
            n_rf += len([o for o in dol if o.status == 'refused'])
        done = ('<div class="sh"><h2>' + DT['done'] + '</h2></div><div class="dgrd dsm">'
                + '<div class="dcd dd"><small>' + DT['paid'] + '</small><b>' + str(npay) + '</b><span>' + eur(spay) + '</span></div>'
                + '<div class="dcd dd"><small>' + DT['decided'] + '</small><b>' + str(n_ap + n_rf) + '</b><span>' + str(n_ap) + ' ' + DT['apprd'] + ' · ' + str(n_rf) + ' ' + DT['refd'] + '</span></div>'
                + '<a class="dcd nt" href="' + hbase + '&amp;view=me&amp;inv=all"><small>' + DT['opentot'] + '</small><b>' + str(len(invs)) + '</b><span>' + eur(sum([mv.amount_residual_signed for mv in invs])) + ' →</span></a></div>')
        return act + m3box + done + todobox + inv_box(invs, od) + teambox + soonbox

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
            nx = str(params.get('next') or '')
            nx = nx if (nx.startswith('?key=' + KEY + '&') and chr(10) not in nx and chr(13) not in nx) else me_url
            response = request.make_response('', headers=[('Location', nx)], status=303)
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
            if params.get('inv'):
                response = html_resp(shell(render_invoices(), '**', True, True))
            elif target:
                response = html_resp(shell(render_person(target, True), target.name, True, True))
            else:
                response = html_resp(shell(render_team(), '*', True))
        elif emp:
            # 23.11.: request time off + withdraw an open request (same Odoo workflow: To Approve -> Second Approval -> Approved)
            lact = str(params.get('lact') or '')
            lresp = None
            LTc = LT.with_context(employee_id=emp.id, holiday_status_display_name=True)
            rqa = LT.fields_get(['requires_allocation']).get('requires_allocation', {}).get('type')
            tdom = [('company_id', 'in', [emp.company_id.id, False])]
            if rqa == 'boolean':
                tdom = tdom + ['|', ('requires_allocation', '=', False), ('has_valid_allocation', '=', True)]
            elif rqa == 'selection':
                tdom = tdom + ['|', ('requires_allocation', '=', 'no'), ('has_valid_allocation', '=', True)]
            ltypes0 = LTc.search(tdom)
            # only the types IQ uses: valid allocation (vacation) + Extra Hours + "Sick Time Off" + "Unpaid"
            # (other list via system parameter iq.timeoff_types = English names, comma separated)
            lallow = [x.strip().lower() for x in (ICP.get_param('iq.timeoff_types') or '').split(',') if x.strip()]
            lkeep = []
            for t0 in LT.with_context(lang='en_US').browse(ltypes0.ids):
                en = (t0.name or '').strip().lower()
                alloc_t = (t0.requires_allocation if rqa == 'boolean' else (rqa == 'selection' and t0.requires_allocation == 'yes'))
                if lallow:
                    ok = en in lallow
                else:
                    ok = bool(alloc_t) or t0.id in otypes.ids or en in ('sick time off', 'unpaid')
                if ok:
                    lkeep.append(t0.id)
            ltypes = LTc.browse([x for x in ltypes0.ids if x in lkeep])
            lerr = ''
            lshow_form = bool(params.get('lnew'))
            if request.httprequest.method == 'POST' and lact == 'cancel':
                lid = str(params.get('lid') or '')
                lv = Leave.browse(int(lid)).exists() if lid.isdigit() else Leave
                if lv and lv.employee_id.id == emp.id and lv.state in ('confirm', 'validate1'):
                    lv._force_cancel(('Vom Mitarbeitenden zurückgezogen (Seite „Meine Stunden & Urlaub“).' if de else 'Withdrawn by the employee (page "My hours & vacation").'), 'mail.mt_note')
                    lresp = request.make_response('', headers=[('Location', me_url + '&lm=w')], status=303)
                else:
                    lresp = request.make_response('', headers=[('Location', me_url + '&lm=x')], status=303)
            elif request.httprequest.method == 'POST' and lact == 'req':
                lshow_form = True
                tid = str(params.get('ltype') or '')
                lt = LTc.browse(int(tid)) if tid.isdigit() else LT
                if not lt or lt.id not in ltypes.ids:
                    lerr = 'Bitte die Art der Abwesenheit wählen.' if de else 'Please choose the type of time off.'
                df = dt = False
                try:
                    df = datetime.datetime.strptime(str(params.get('dfrom') or ''), '%Y-%m-%d').date()
                    dt = datetime.datetime.strptime(str(params.get('dto') or params.get('dfrom') or ''), '%Y-%m-%d').date()
                except Exception:
                    lerr = lerr or ('Bitte die Daten prüfen.' if de else 'Please check the dates.')
                unit = lt.request_unit if lt else 'day'
                if not lerr and unit == 'hour':
                    dt = df
                if not lerr and dt < df:
                    lerr = '„Bis“ liegt vor „Von“.' if de else '"To" is before "From".'
                vals = {}
                if not lerr:
                    vals = {'employee_id': emp.id, 'holiday_status_id': lt.id, 'request_date_from': df, 'request_date_to': dt,
                            'name': str(params.get('desc') or '').strip()[:500]}
                    if unit == 'half_day':
                        pf = str(params.get('pfrom') or 'am')
                        pt = str(params.get('pto') or 'pm')
                        vals['request_date_from_period'] = pf if pf in ('am', 'pm') else 'am'
                        vals['request_date_to_period'] = pt if pt in ('am', 'pm') else 'pm'
                        if df == dt and vals['request_date_from_period'] == 'pm' and vals['request_date_to_period'] == 'am':
                            lerr = 'Am selben Tag: Nachmittag bis Vormittag geht nicht.' if de else 'Same day: afternoon to morning is not possible.'
                    if unit == 'hour':
                        h1 = str(params.get('hfrom') or '').split(':')
                        h2 = str(params.get('hto') or '').split(':')
                        if len(h1) == 2 and len(h2) == 2 and (h1[0] + h1[1] + h2[0] + h2[1]).isdigit():
                            vals['request_hour_from'] = int(h1[0]) + int(h1[1]) / 60.0
                            vals['request_hour_to'] = int(h2[0]) + int(h2[1]) / 60.0
                            if vals['request_hour_to'] <= vals['request_hour_from']:
                                lerr = '„Bis“-Uhrzeit muss nach „Von“ liegen.' if de else '"To" time must be after "From".'
                        else:
                            lerr = 'Bitte Uhrzeit von / bis eingeben.' if de else 'Please enter the time from / to.'
                if not lerr:
                    LV = Leave.with_user(emp.user_id).sudo() if emp.user_id else Leave
                    sp = False
                    try:
                        sp = env.cr.savepoint()
                    except Exception:
                        sp = False
                    newlv = Leave
                    try:
                        newlv = LV.create(vals)
                        fls = [f for f in request.httprequest.files.getlist('lfile') if f and f.filename]
                        aids = []
                        for f in fls[:3]:
                            aids.append(env['ir.attachment'].sudo().create({'name': f.filename, 'raw': f.read(), 'mimetype': f.mimetype or 'application/octet-stream',
                                                                             'res_model': 'hr.leave', 'res_id': newlv.id}).id)
                        if aids:
                            newlv.message_post(body=('Datei vom Mitarbeitenden hochgeladen.' if de else 'File uploaded by the employee.'), attachment_ids=aids, subtype_xmlid='mail.mt_note')
                        if sp:
                            sp.close(rollback=False)
                    except Exception as e:
                        if sp:
                            sp.close(rollback=True)
                        newlv = Leave
                        lerr = (str(e) or 'Fehler').replace(chr(10), ' ').strip()[:400]
                    if newlv and not lerr:
                        lresp = request.make_response('', headers=[('Location', me_url + '&lm=ok')], status=303)
            if lresp is None:
                if lshow_form:
                    bal = ot_data(emp)['bal']
                    opts = ''
                    sel = str(params.get('ltype') or '')
                    I_SUN = '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
                    I_CLK = '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
                    I_MED = '<svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="4"/><path d="M12 8v8M8 12h8"/></svg>'
                    I_CAL = '<svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M8 2v4M16 2v4M10 13l4 4M14 13l-4 4"/></svg>'
                    if len(ltypes) == 1 and not sel:
                        sel = str(ltypes[0].id)
                    for t in ltypes:
                        alloc_t = (t.requires_allocation if rqa == 'boolean' else (rqa == 'selection' and t.requires_allocation == 'yes'))
                        nm_l = (t.name or '').lower()
                        if t.id in otypes.ids and not alloc_t:
                            ic, kind, info = I_CLK, 'ot', hm(bal) + ' ' + T['h'] + (' verfügbar' if de else ' available')
                            hint = ('Wird von deinem Überstunden-Saldo abgezogen. Wähle Tag und Uhrzeit.' if de else 'Taken from your overtime balance. Choose the day and the time.')
                        elif alloc_t:
                            rem = t.virtual_remaining_leaves or 0.0
                            mx = t.max_leaves or 0.0
                            ic, kind = I_SUN, 'vac'
                            info = dnum(rem) + ' ' + (T['day'] if rem == 1 else T['days']) + (' übrig von ' if de else ' left of ') + dnum(mx)
                            hint = ('Wird von deinem Urlaub abgezogen. Halbe Tage möglich (Vormittag / Nachmittag).' if de else 'Taken from your vacation. Half days possible (morning / afternoon).')
                        elif is_sick(t):
                            ic, kind, info = I_MED, 'sick', ('AU optional anhängen' if de else 'sick note optional')
                            hint = ('Für eine Krankmeldung. Die AU-Bescheinigung kannst du unten anhängen (optional).' if de else 'For being sick. You can attach the sick note below (optional).')
                        else:
                            ic, kind, info = I_CAL, 'oth', ('ohne Bezahlung' if de and ('unpaid' in nm_l or 'unbezahlt' in nm_l) else ('unpaid' if 'unpaid' in nm_l or 'unbezahlt' in nm_l else ''))
                            hint = ('Wird nicht vom Urlaub abgezogen.' if de else 'Not taken from your vacation.')
                        opts += ('<label class="lt lt-' + kind + '"><input type="radio" name="ltype" value="' + str(t.id) + '" data-u="' + (t.request_unit or 'day') + '" data-h="' + esc(hint) + '"'
                                 + (' checked' if sel == str(t.id) else '') + ' required><span class="ic">' + ic + '</span><b>' + esc(t.name) + '</b><small>' + esc(info) + '</small></label>')
                    tv = lambda k, d: esc(str(params.get(k) or d))
                    sv = lambda k, v, d: ' selected' if str(params.get(k) or d) == v else ''
                    inner = ('<form class="pf lvf" method="post" action="" enctype="multipart/form-data"><h2>' + ('Abwesenheit beantragen' if de else 'Request time off') + '</h2>'
                             + '<input type="hidden" name="csrf_token" value="' + request.csrf_token() + '"><input type="hidden" name="key" value="' + KEY + '">'
                             + '<input type="hidden" name="view" value="me"><input type="hidden" name="lact" value="req">' + ('' if de else '<input type="hidden" name="lang" value="en">')
                             + '<label>' + ('Was möchtest du beantragen?' if de else 'What do you want to request?') + '</label><div class="lvt" id="lvt">' + opts + '</div><p class="lhint" id="lhint" hidden></p>'
                             + '<div class="two"><div><label>' + ('Von' if de else 'From') + '</label><input type="date" name="dfrom" id="dfrom" required value="' + tv('dfrom', today.isoformat()) + '"></div>'
                             + '<div id="wto"><label>' + ('Bis' if de else 'To') + '</label><input type="date" name="dto" id="dto" value="' + tv('dto', today.isoformat()) + '"></div></div>'
                             + '<div class="two" id="whalf" hidden><div><label>' + ('Beginn' if de else 'Start') + '</label><select name="pfrom"><option value="am"' + sv('pfrom', 'am', 'am') + '>' + ('Vormittag' if de else 'Morning') + '</option><option value="pm"' + sv('pfrom', 'pm', 'am') + '>' + ('Nachmittag' if de else 'Afternoon') + '</option></select></div>'
                             + '<div><label>' + ('Ende' if de else 'End') + '</label><select name="pto"><option value="am"' + sv('pto', 'am', 'pm') + '>' + ('Vormittag' if de else 'Morning') + '</option><option value="pm"' + sv('pto', 'pm', 'pm') + '>' + ('Nachmittag' if de else 'Afternoon') + '</option></select></div></div>'
                             + '<div class="two" id="whour" hidden><div><label>' + ('Uhrzeit von' if de else 'Time from') + '</label><input type="time" name="hfrom" value="' + tv('hfrom', '08:00') + '"></div>'
                             + '<div><label>' + ('Uhrzeit bis' if de else 'Time to') + '</label><input type="time" name="hto" value="' + tv('hto', '12:00') + '"></div></div>'
                             + '<label>' + ('Beschreibung (optional)' if de else 'Description (optional)') + '</label><textarea name="desc" rows="2">' + tv('desc', '') + '</textarea>'
                             + '<label>' + ('Datei anhängen (optional, z. B. AU-Bescheinigung)' if de else 'Attach file (optional, e.g. sick note)') + '</label><input type="file" name="lfile" accept="image/*,application/pdf">'
                             + ('<p class="e">' + esc(lerr) + '</p>' if lerr else '')
                             + '<button>' + ('Antrag senden' if de else 'Send request') + '</button>'
                             + '<p class="hint" style="text-align:center">' + ('Der Antrag geht in Odoo Abwesenheiten in den normalen Ablauf: Zu genehmigen → Zweite Genehmigung → Genehmigt.' if de else 'The request goes into the normal Odoo Time Off workflow: To Approve → Second Approval → Approved.') + '</p>'
                             + '<p style="text-align:center;margin:10px 0 0"><a href="' + hbase + '&amp;view=me">' + ('Abbrechen' if de else 'Cancel') + '</a></p></form>'
                             + '<script>(function(){var f=document.getElementById("dfrom"),t=document.getElementById("dto"),h=document.getElementById("lhint");'
                             + 'function u(){var o=document.querySelector("#lvt input:checked"),k=o?o.getAttribute("data-u"):"day";document.getElementById("whalf").hidden=k!=="half_day";document.getElementById("whour").hidden=k!=="hour";document.getElementById("wto").hidden=k==="hour";'
                             + 'h.hidden=!o;if(o)h.textContent=o.getAttribute("data-h");document.querySelectorAll("#lvt .lt").forEach(function(l){l.classList.toggle("on",l.querySelector("input").checked)})}'
                             + 'document.querySelectorAll("#lvt input").forEach(function(i){i.onchange=u});f.onchange=function(){t.min=f.value;if(!t.value||t.value<f.value)t.value=f.value};t.min=f.value;u()})();</script>')
                    lresp = html_resp(shell(inner, emp.name, True))
                else:
                    lm = str(params.get('lm') or '')
                    msg = {'ok': ('Antrag gesendet – er steht unten als „Offen“, bis er genehmigt ist.' if de else 'Request sent – it is listed below as “Open” until it is approved.'),
                           'w': ('Antrag zurückgezogen.' if de else 'Request withdrawn.'),
                           'x': ('Dieser Antrag kann nicht mehr zurückgezogen werden.' if de else 'This request can no longer be withdrawn.')}.get(lm, '')
                    lresp = html_resp(shell((('<div class="lmsg' + (' bad' if lm == 'x' else '') + '">' + msg + '</div>') if msg else '') + render_person(emp, False), emp.name, True))
            response = lresp
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
        'done': 'Geliefert' if de else 'Delivered', 'open_po': 'Klick öffnet die Bestellung in Odoo' if de else 'Click to open the purchase order in Odoo',
        'status': 'Status', 'done_s': 'geliefert' if de else 'delivered', 'expected': 'Erwartet' if de else 'Expected',
        'srch': 'Suche: Bestellung, Lieferant, Produkt, Lieferschein …' if de else 'Search: order, supplier, product, delivery note …',
        'go': 'Suchen' if de else 'Search', 'clear': '×', 'res': 'Suchergebnis' if de else 'Search result', 'nores': 'Nichts gefunden.' if de else 'Nothing found.',
        'date': 'Datum' if de else 'Date', 'status': 'Status', 'what': 'Was' if de else 'What', 'qty': 'Stück' if de else 'Pieces', 'show': 'im Kalender' if de else 'in calendar',
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
    Pick = env['stock.picking'].sudo()
    Move = env['stock.move'].sudo()

    def pick_info(p, field):
        # products + pieces of one receipt; kit parts are counted as sets
        names = []
        qty = 0.0
        kit = {}
        for mv in p.move_ids:
            if mv.state == 'cancel':
                continue
            n = (mv.product_id.product_tmpl_id.name or '').split(' – ')[0]
            pl = mv.purchase_line_id
            if pl and mv.product_id != pl.product_id:
                n = (pl.product_id.product_tmpl_id.name or '').split(' – ')[0]
                kit[pl.id] = kit.get(pl.id, 0.0) + (mv[field] or 0.0)
            else:
                qty += mv[field] or 0.0
            if n not in names:
                names.append(n)
        for plid in kit:
            pl = env['purchase.order.line'].sudo().browse(plid)
            total = sum(Move.search([('purchase_line_id', '=', plid), ('state', '!=', 'cancel')]).mapped('product_uom_qty'))
            qty += round(kit[plid] / total * pl.product_qty) if total and pl.product_qty else 0
        return names, qty

    WEACT = env['ir.actions.act_window'].sudo().search([('res_model', '=', 'x_wareneingang')], order='id', limit=1)
    WECARD = {}

    def card_of(poid):
        if poid not in WECARD:
            WECARD[poid] = WE.search([('x_studio_purchase_order', '=', poid)], limit=1).id or 0
        return WECARD[poid]

    def ev_url(e):
        wid = e.get('wid') or (card_of(e['poid']) if e.get('poid') else 0)
        if wid:
            return ('/odoo/action-' + str(WEACT.id) + '/' + str(wid)) if WEACT else ('/odoo/x_wareneingang/' + str(wid))
        return ('/odoo/purchase.order/' + str(e['poid'])) if e.get('poid') else ''

    def add_ev(store, order, key, d, sup, names, qty, ship, ref, kind, poid=0, wid=0):
        if key not in store:
            store[key] = {'d': d, 'sup': sup, 'names': [], 'ship': [], 'qty': 0.0, 'ref': ref, 'kind': kind, 'poid': poid, 'wid': wid}
            order.append(key)
        e = store[key]
        e['qty'] += qty
        for n in names:
            if n and n not in e['names']:
                e['names'].append(n)
        if ship and ship not in e['ship']:
            e['ship'].append(ship)

    def finish(store, order):
        out = []
        for k in order:
            e = store[k]
            e['prod'] = (e['names'][0] + (' +' + str(len(e['names']) - 1) if len(e['names']) > 1 else '')) if e['names'] else ''
            e['ship'] = ', '.join(e['ship'])
            out.append(e)
        return out

    def collect(line_dom, open_dom, done_dom):
        store = {}
        order = []
        # planned lines from delivery overviews / PDFs (one entry per order and day; ignored once the PO is fully received)
        for l in Line.search(line_dom, order='x_date asc'):
            po = l.x_wareneingang_id.x_studio_purchase_order
            if po and po.receipt_status == 'full':
                continue
            ref = po.name if po else (l.x_supplier_ref or '')
            key = ('p', po.id if po else (l.x_wareneingang_id.id or ref), l.x_date)
            lq = l.x_qty or 0
            if l.id in COVER:
                if COVER[l.id] <= 0:
                    continue
                lq = COVER[l.id]
            add_ev(store, order, key, l.x_date, l.x_partner_id.commercial_partner_id.name or '', [l.x_product_text or ''], lq, l.x_shipment or '', ref, 'plan', po.id if po else 0, l.x_wareneingang_id.id or 0)
            store[key].setdefault('lids', []).append(l.id)
        # open receipts of purchase orders without planned lines (one entry per order and day)
        for p in Pick.search(open_dom, order='scheduled_date asc'):
            card = WE.search([('x_studio_purchase_order', '=', p.purchase_id.id)], limit=1)
            if card and [x for x in card.x_schedule_ids if not x.x_done]:
                continue
            # date = "Expected Arrival" of the purchase order (what you change on the PO); receipt date only as fallback
            dp = p.purchase_id.date_planned or p.scheduled_date
            d = dp.date() if dp else today
            names, qty = pick_info(p, 'product_uom_qty')
            # 20.11.: already reported as arrived (after this receipt was created) -> not "expected" any more; partial -> only the rest
            pts = int((p.create_date - datetime.datetime(1970, 1, 1)).total_seconds()) if p.create_date else 0
            arrd = []
            for r in (ARRW.get(card.id, []) if card else []):
                if r['ts'] >= pts:
                    arrd.append(r)
            if arrd:
                acnt = sum([(r['cnt'] or r['ls']) for r in arrd])
                if not acnt or acnt >= qty * 0.98:
                    continue
                qty = qty - acnt
            add_ev(store, order, ('o', p.purchase_id.id, d), d, p.partner_id.commercial_partner_id.name or '', names, qty, (('Rest' if de else 'rest') if arrd else ''), p.purchase_id.name, 'po', p.purchase_id.id)
        # delivered: validated receipts, one entry per order and day, with the delivered pieces
        for p in Pick.search(done_dom, order='date_done asc'):
            d = p.date_done.date()
            names, qty = pick_info(p, 'quantity')
            add_ev(store, order, ('d', p.purchase_id.id, d), d, p.partner_id.commercial_partner_id.name or '', names, qty, '', p.purchase_id.name, 'done', p.purchase_id.id)
        return sorted(finish(store, order), key=lambda e: e['d'])

    # 20.11.c: planned deliveries that are already BOOKED in Odoo (received quantity of the PO) are not "expected"/"overdue" any more.
    # The booked pieces of an order are matched to its planned deliveries in date order (oldest first); partly covered -> only the rest.
    COVER = {}
    cpos = []
    for l0 in Line.search([('x_done', '=', False), ('x_date', '!=', False)]):
        po0 = l0.x_wareneingang_id.x_studio_purchase_order
        if po0 and po0.id not in cpos:
            cpos.append(po0.id)
    for pid0 in cpos:
        po0 = env['purchase.order'].sudo().browse(pid0)
        rem = 0.0
        for ol0 in po0.order_line:
            if ol0.product_id and ol0.product_id.type != 'service':
                rem += ol0.qty_received or 0.0
        for l0 in Line.search([('x_wareneingang_id.x_studio_purchase_order', '=', pid0), ('x_date', '!=', False)], order='x_date asc, id asc'):
            if rem <= 0:
                break
            q0 = l0.x_qty or 0.0
            if rem >= q0 * 0.98:
                COVER[l0.id] = 0
                rem -= q0
            else:
                COVER[l0.id] = q0 - rem
                rem = 0
    ARR = arr_records(120)
    ARRW = {}
    for r in ARR:
        ARRW.setdefault(r['wid'], []).append(r)
    PBASE = [('picking_type_code', '=', 'incoming'), ('purchase_id', '!=', False)]
    ev = collect([('x_done', '=', False), ('x_date', '!=', False)],
                 PBASE + [('state', 'not in', ['done', 'cancel', 'draft'])],
                 PBASE + [('state', '=', 'done'), ('date_done', '>=', datetime.datetime.combine(gstart, datetime.time(0, 0))), ('date_done', '<', datetime.datetime.combine(gend + datetime.timedelta(days=1), datetime.time(0, 0)))])

    # 20.11.: reported arrivals (not booked yet) as own entries – amber "angekommen", red "ohne Bestellung"
    for r in ARR:
        dd = arr_date(r['ts'])
        if dd < gstart or dd > gend:
            continue
        if r['pick'] and Pick.browse(r['pick']).exists().state == 'done':
            continue
        cd = WE.browse(r['wid']).exists()
        if not cd:
            continue
        pz = cd.x_studio_purchase_order
        ev.append({'d': dd, 'sup': (pz.partner_id.commercial_partner_id.name if pz else (cd.x_studio_supplier.commercial_partner_id.name or '')) or '', 'prod': r['prod'], 'names': [r['prod']],
                   'ship': ('angekommen' if de else 'arrived') + ' · ' + r['who'] + ((' · ' + (str(r['cnt']) + ' gezählt' if de else str(r['cnt']) + ' counted')) if r['cnt'] else ''),
                   'qty': r['cnt'] or r['ls'], 'ref': pz.name if pz else ('ohne Bestellung' if de else 'no PO'), 'kind': 'arr' if pz else 'nopo', 'poid': pz.id if pz else 0, 'wid': cd.id})
    ev = sorted(ev, key=lambda e: e['d'])

    # search (PO, supplier, product, order no., delivery note)
    q = (params.get('q') or '').strip()
    found = []
    if len(q) >= 2:
        lq = ['|', '|', '|', '|', ('x_product_text', 'ilike', q), ('x_supplier_ref', 'ilike', q), ('x_shipment', 'ilike', q),
              ('x_partner_id.name', 'ilike', q), ('x_wareneingang_id.x_studio_purchase_order.name', 'ilike', q)]
        pq = ['|', '|', '|', '|', ('purchase_id.name', 'ilike', q), ('purchase_id.partner_ref', 'ilike', q), ('partner_id.name', 'ilike', q),
              ('move_ids.product_id.name', 'ilike', q), ('origin', 'ilike', q)]
        found = collect([('x_done', '=', False), ('x_date', '!=', False)] + lq,
                        PBASE + [('state', 'not in', ['done', 'cancel', 'draft'])] + pq,
                        PBASE + [('state', '=', 'done')] + pq)
        found = sorted(found, key=lambda e: e['d'], reverse=True)[:60]

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
        od = ' dlv' if e['kind'] == 'done' else (' arr' if e['kind'] == 'arr' else (' nopo' if e['kind'] == 'nopo' else (' od' if d < today else '')))
        inner = ('<div class="ev' + od + '" style="border-left-color:' + col(e['sup']) + '" title="' + esc(e['sup'] + ' · ' + e['prod']) + (' – Wareneingang öffnen' if ev_url(e) else '') + '">'
                 + '<b>' + num(e['qty']) + '</b> ' + esc(e['prod']) + '<span>' + esc(e['sup']) + (' · ' + esc(e['ship']) if e['ship'] else '')
                 + (' · ' + esc(e['ref']) if e['ref'] else '') + '</span></div>')
        edt = ''
        if ADM and e.get('lids'):
            for lid in e['lids']:
                edt += '<a class="edt" href="' + base.replace('&', '&amp;') + '&amp;plan=' + str(lid) + '">✎ ' + ('Bearbeiten' if de else 'Edit') + (' ' + str(e['lids'].index(lid) + 1) if len(e['lids']) > 1 else '') + '</a>'
        if e['kind'] in ('plan', 'po') and d <= today + datetime.timedelta(days=3):
            au = ('&arr=1&lid=' + str(e['lids'][0]) + (('&po=' + str(e['poid'])) if e.get('poid') else '')) if e.get('lids') else (('&arr=1&po=' + str(e['poid'])) if e.get('poid') else (('&arr=1&wid=' + str(e['wid'])) if e.get('wid') else ''))
            if au:
                edt += '<a class="arrl" href="' + base.replace('&', '&amp;') + au.replace('&', '&amp;') + '">' + ICB + ('Angekommen?' if de else 'Arrived?') + '</a>'
        return (('<a class="evl" href="' + ev_url(e) + '" target="_blank">' + inner + '</a>') if ev_url(e) else inner) + edt

    def abhtml(d):
        out = ''
        if d.weekday() < 5:
            for a in sorted(absn, key=lambda a: a['p']):
                if a['a'] <= d <= a['b']:
                    out += ('<div class="ab pend" title="' + L['pend_t'] + '">' + av(a) + esc(a['n']) + ' ?</div>') if a['p'] else ('<div class="ab">' + av(a) + esc(a['n']) + '</div>')
        return out

    # KPIs
    tday = [x for x in ev if x['d'] == today and x['kind'] in ('plan', 'po')]
    mev = [x for x in ev if first <= x['d'] <= last]
    mdone = [x for x in mev if x['kind'] == 'done']
    odl = [x for x in ev if x['d'] < today and x['kind'] in ('plan', 'po')]
    absnow = [a for a in absn if a['a'] <= today <= a['b'] and today.weekday() < 5 and not a['p']]
    k = ['<div class="kpis">',
         '<div class="kpi"><small>' + L['k_today'] + '</small><b>' + (num(sum(x['qty'] for x in tday)) + ' ' + L['pcs'] if tday else L['none_today']) + '</b><span>' + str(len(tday)) + ' ' + (L['deliv1'] if len(tday) == 1 else L['deliv']) + '</span></div>',
         '<div class="kpi"><small>' + L['k_month'] + ' · ' + MONTHS[m - 1] + '</small><b>' + num(sum(x['qty'] for x in mev)) + ' ' + L['pcs'] + '</b><span>' + str(len(mev)) + ' ' + (L['deliv1'] if len(mev) == 1 else L['deliv']) + ((' · <b style="display:inline;font-size:12.5px;color:#16a34a">' + num(sum(x['qty'] for x in mdone)) + ' ' + L['done_s'] + '</b>') if mdone else '') + '</span></div>',
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
        g.append('<div class="' + cls + '"><div class="dn">' + str(d.day) + '</div>' + (('<a class="addd" title="' + ('Lieferung eintragen' if de else 'Add delivery') + '" href="' + base.replace('&', '&amp;') + '&amp;plan=new&amp;d=' + d.strftime('%Y-%m-%d') + '">+</a>') if ADM else '') + abhtml(d))
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
            ag.append('<div class="d' + (' today' if d == today else '') + '"><h4>' + LDAYS[d.weekday()] + ', ' + d.strftime('%d.%m.') + (' <span class="tag">' + L['today'] + '</span>' if d == today else '') + (('<a class="addd" href="' + base.replace('&', '&amp;') + '&amp;plan=new&amp;d=' + d.strftime('%Y-%m-%d') + '">+</a>') if ADM else '') + '</h4>'
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
    nopos = []
    for r in ARR:
        cd = WE.browse(r['wid']).exists()
        if cd and not cd.x_studio_purchase_order and cd.id not in [x[0].id for x in nopos]:
            nopos.append([cd, r])
    if nopos:
        s.append('<div class="box red" id="nopo"><h3>' + ICW + ('Angekommen ohne Bestellung' if de else 'Arrived without purchase order') + ' (' + str(len(nopos)) + ')</h3>')
        for cr in nopos:
            u = ev_url({'wid': cr[0].id})
            s.append('<a class="rowl" href="' + u + '" target="_blank"><div class="row"><span>' + arr_date(cr[1]['ts']).strftime('%d.%m.') + ' ' + esc(cr[1]['prod']) + '<small>' + esc(cr[0].x_studio_supplier.name or '')
                     + (' · LS ' + esc(cr[1]['lsno']) if cr[1]['lsno'] else '') + ' · ' + esc(cr[1]['who']) + '</small></span><b>' + num(cr[1]['cnt'] or cr[1]['ls']) + '</b></div></a>')
        s.append('<p class="mut" style="margin:6px 0 0;font-size:12px">' + ('Bestellung in Odoo anlegen – Lieferantenreferenz = Lieferschein-Nr., dann wird sie automatisch mit dem Wareneingang verknüpft.' if de else
                 'Create the purchase order in Odoo – vendor reference = delivery note no., then it is linked to the goods receipt automatically.') + '</p></div>')
    if odl:
        s.append('<div class="box red"><h3>' + L['overdue'] + '</h3>')
        for e in odl:
            s.append(('<a class="rowl" href="' + ev_url(e) + '" target="_blank">' if ev_url(e) else '') + '<div class="row"><span>' + e['d'].strftime('%d.%m.') + ' ' + esc(e['prod']) + '<small>' + esc(e['sup']) + (' · ' + esc(e['ref']) if e['ref'] else '') + '</small></span><b>' + num(e['qty']) + '</b></div>' + ('</a>' if ev_url(e) else ''))
        s.append('</div>')
    s.append('<div class="box"><h3>' + L['month_list'] + MONTHS[m - 1] + '</h3>')
    if not mev:
        s.append('<p class="mut" style="margin:0">' + L['nodel'] + '</p>')
    for e in mev:
        tag = L['done'] if e['kind'] == 'done' else (L['po'] if e['kind'] == 'po' else (('Angekommen' if de else 'Arrived') if e['kind'] == 'arr' else (('ohne Bestellung' if de else 'no PO') if e['kind'] == 'nopo' else L['plan'])))
        s.append(('<a class="rowl" href="' + ev_url(e) + '" target="_blank">' if ev_url(e) else '') + '<div class="row"><span><i class="dot" style="background:' + col(e['sup']) + '"></i>' + e['d'].strftime('%d.%m.') + ' ' + esc(e['prod'])
                 + '<small>' + esc(e['sup']) + (' · ' + esc(e['ship']) if e['ship'] else '') + ' · ' + tag + (' ' + esc(e['ref']) if e['ref'] else '') + '</small></span><b>' + num(e['qty']) + '</b></div>' + ('</a>' if ev_url(e) else ''))
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

    srch_html = ('<form class="srch" method="get" action=""><input type="hidden" name="key" value="' + KEY + '">' + ('' if de else '<input type="hidden" name="lang" value="en">')
                 + '<input type="search" name="q" value="' + esc(q) + '" placeholder="' + L['srch'] + '"><button>' + L['go'] + '</button>'
                 + ('<a class="x" href="' + link(first) + '">' + L['clear'] + '</a>' if q else '') + '</form>')
    if len(q) >= 2:
        rr = ''
        for e in found:
            if e['kind'] == 'done':
                st = '<span class="s s-dn">✓ ' + L['done'] + '</span>'
            elif e['d'] < today:
                st = '<span class="s s-od">' + L['k_od'] + '</span>'
            else:
                st = '<span class="s s-ex">' + L['expected'] + '</span>'
            rr += ('<tr><td>' + e['d'].strftime('%d.%m.%Y') + '</td><td>' + st + '</td><td>' + esc(e['prod']) + '<br><span class="mut" style="font-size:12px">' + esc(e['sup'])
                   + (' · ' + esc(e['ship']) if e['ship'] else '') + (' · ' + (('<a href="' + ev_url(e) + '" target="_blank">' + esc(e['ref']) + ' ↗</a>') if ev_url(e) else esc(e['ref'])) if e['ref'] else '') + '</span></td><td class="r"><b>' + num(e['qty']) + '</b></td>'
                   + '<td class="r"><a href="' + link(e['d']) + '">' + L['show'] + '</a></td></tr>')
        srch_html += ('<div class="box res"><h3>' + L['res'] + ': „' + esc(q) + '“</h3>' + ('<table><tr><th>' + L['date'] + '</th><th>' + L['status'] + '</th><th>' + L['what'] + '</th><th class="r">' + L['qty'] + '</th><th></th></tr>' + rr + '</table>' if rr else '<p class="mut" style="margin:0">' + L['nores'] + '</p>') + '</div>')
    langlink = ('?key=' + KEY + '&amp;m=' + first.strftime('%Y-%m') + '&amp;lang=en') if de else ('?key=' + KEY + '&amp;m=' + first.strftime('%Y-%m'))
    html = (page_head(TITLE) + '<meta http-equiv="refresh" content="600"></head><body>'
            + '<div class="top"><div class="in"><div class="brand"><img src="' + LOGO + '" alt="IQ Dogsport"><div><h1>' + TITLE + '</h1><p>' + L['sub'] + '</p></div></div>'
            + '<nav class="cnav"><a class="nm" href="' + link(prv) + '">&larr;</a><b>' + MONTHS[m - 1] + ' ' + str(y) + '</b><a class="nm" href="' + link(nxt) + '">&rarr;</a>'
            + '<a class="nt" href="' + link(today) + '">' + L['today'] + '</a>'
            + '<span class="nbtn"><a class="na arrb" href="' + base.replace('&', '&amp;') + '&amp;arr=1">' + ICB + ('Ware angekommen' if de else 'Goods arrived') + '</a>'
            + '<a class="na" href="' + base.replace('&', '&amp;') + '&amp;plan=new" style="background:#16a34a;border-color:#16a34a">+ ' + ('Lieferung eintragen' if de else 'Add delivery') + '</a><a class="na" href="/website/action/iq-qc?key=' + KEY + '&amp;view=dash" style="background:#151515;border-color:#fff">QC Dashboard</a><a class="na me" href="?key=' + KEY + '&amp;view=me' + ('' if de else '&amp;lang=en') + '" style="background:#a51d1b;border-color:#a51d1b">' + ('Meine Stunden &amp; Urlaub' if de else 'My hours &amp; vacation') + '</a><a class="nl" href="' + langlink + '">' + ('EN' if de else 'DE') + '</a></span></nav><script>(function(){var n=document.querySelector(".nbtn");if(!n)return;function f(){n.classList.toggle("more",n.scrollWidth>n.clientWidth+2)}f();addEventListener("resize",f)})()</script></div></div>'
            + '<div class="wrap">' + ''.join(k) + srch_html + '<main><div>' + ''.join(g) + ''.join(ag) + '</div>' + ''.join(s) + '</main></div>'
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
AMc = env['account.move'].sudo().search_count([('move_type', '=', 'out_invoice'), ('state', '=', 'posted'), ('payment_state', 'in', ['not_paid', 'partial'])])
RMc = env['mail.message'].sudo().search_count([('model', '=', 'account.move'), ('body', 'ilike', 'IQ-REMINDER-3')])
log('IQ calendar 23.11 arrival simple + scanner + to-do + header right + time off request v2 installed | IQ calendar 20.11d booked = not overdue + goods arrival + icons installed | IQ calendar 20.11b goods arrival installed | IQ calendar 20.11 QC link installed | IQ calendar 19.11 add deliveries installed | IQ calendar 17.11 goods-receipt links installed | Goods Receipts action: ' + str(env['ir.actions.act_window'].sudo().search([('res_model', '=', 'x_wareneingang')], order='id', limit=1).id or 'NOT FOUND') + ' | invoices with IQ-REMINDER-3 note: ' + str(RMc) + ' | ' + 'IQ calendar 13.11c reminders installed | unpaid customer invoices: ' + str(AMc) + ' | manager PIN: ' + ('OK' if len(mp) >= 8 else ('TOO SHORT – needs 8+ digits' if mp else 'NOT SET – add system parameter iq.delivery_calendar_manager_pin'))
    + ' | overtime model: ' + OTM + ' / field: ' + dfield + ' / status filter: ' + ('yes' if 'status' in fg else 'no')
    + ' | overtime time-off types: ' + (', '.join(ot_types) or 'none')
    + ' | employees with PIN: ' + str(pins) + ' | without PIN: ' + (', '.join(nopin) or 'none'))
