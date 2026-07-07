#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate 14 fintech demo pages with code examples and SEO metadata."""

import os
import re

# ── Shared configuration ────────────────────────────────────────────────
CONFIG = {
    "company": {
        "name": "AXIIOM",
        "nameRu": "ООО Аксиома",
        "shortName": "Аксиома",
        "domain": "axiiom.ru",
        "siteUrl": "https://axiiom.ru/",
        "ogImage": "https://axiiom.ru/og-image.png",
        "copyrightStart": 2024,
    },
    "contact": {
        "email": "hello@axiiom.ru",
        "phone": "+7 (812) 928-74-78",
        "phoneLink": "+78129287478",
        "telegram": "https://t.me/axiiom",
    },
    "analytics": {
        "yandexMetrika": "109391253",
        "googleAnalytics": "G-HFS4BDGTV4",
    },
}
# ─────────────────────────────────────────────────────────────────────────

DEMOS = [
    {
        "slug": "payment-gateway",
        "title": "Платёжный шлюз",
        "desc": "Универсальный платёжный шлюз с поддержкой мультиэквайринга, сплитования платежей и escrow-счетов. Соответствие 161-ФЗ и PCI DSS.",
        "meta_desc": "Демо платёжного шлюза: приём платежей по картам, SBP, токенизация, сплитование. Соответствие 161-ФЗ и PCI DSS. Примеры кода интеграции.",
        "code": """// Инициализация платёжного шлюза
const gateway = new PaymentGateway({
  apiKey: 'your_api_key',
  merchantId: 'merchant_123',
  environment: 'sandbox' // sandbox | production
});

// Создание платежа
const payment = await gateway.createPayment({
  amount: 1500.00,
  currency: 'RUB',
  description: 'Заказ №4281',
  split: [
    { merchant: 'submerchant_1', amount: 1200.00 },
    { merchant: 'submerchant_2', amount: 300.00 }
  ],
  escrow: { holdPeriod: 3 } // дней
});

// Перенаправление на платёжную страницу
window.location.href = payment.paymentUrl;""",
        "features": ["Мультиэквайринг (Visa, MC, Мир, SBP)", "Сплитование платежей и escrow", "Токенизация карт (PCI DSS)", "Холдирование и возвраты", "Webhook-уведомления", "Личный кабинет мерчанта"],
        "tags": ["PHP", "Go", "Node.js", "PostgreSQL", "PCI DSS"],
        "gradient": "#6c5ce7,#a29bfe",
        "widget_html": """<div class="pg-card">
  <div class="pg-header">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--clr-accent)" stroke-width="1.8"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/><line x1="7" y1="15" x2="11" y2="15"/></svg>
    <span>Оплата картой</span>
  </div>
  <div class="pg-body">
    <div class="pg-fld">
      <label class="pg-lbl">Номер карты</label>
      <div class="pg-inp-wrap">
        <input class="pg-inp" id="w1n" placeholder="0000 0000 0000 0000" maxlength="19">
        <svg class="pg-card-icon" width="22" height="16" viewBox="0 0 24 16" fill="none">
          <rect x="1" y="1" width="22" height="14" rx="2" stroke="var(--clr-faint)" stroke-width="1.2" fill="none"/>
          <line x1="1" y1="6" x2="23" y2="6" stroke="var(--clr-faint)" stroke-width="1.2"/>
          <circle cx="9" cy="10" r="2.5" stroke="var(--clr-accent)" stroke-width="1.2" fill="none" opacity=".5"/>
          <circle cx="15" cy="10" r="2.5" stroke="var(--clr-accent)" stroke-width="1.2" fill="none" opacity=".5"/>
        </svg>
      </div>
    </div>
    <div class="pg-row">
      <div class="pg-fld">
        <label class="pg-lbl">Срок действия</label>
        <input class="pg-inp" id="w1e" placeholder="MM / YY" maxlength="7">
      </div>
      <div class="pg-fld">
        <label class="pg-lbl">CVV</label>
        <div class="pg-inp-wrap">
          <input class="pg-inp" id="w1c" placeholder="•••" maxlength="4" type="password">
          <svg class="pg-cvv-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--clr-faint)" stroke-width="1.5"><rect x="3" y="7" width="18" height="12" rx="1.5"/><line x1="7" y1="11" x2="9" y2="11"/><line x1="7" y1="14" x2="11" y2="14"/></svg>
        </div>
      </div>
      <div class="pg-fld">
        <label class="pg-lbl">Сумма</label>
        <div class="pg-inp-wrap">
          <span class="pg-currency">₽</span>
          <input class="pg-inp pg-inp-amt" id="w1a" type="number" value="1500">
        </div>
      </div>
    </div>
    <button class="pg-btn" id="w1b">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="10" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/><circle cx="12" cy="16" r="1"/></svg>
      Оплатить 1 500 ₽
    </button>
    <div class="pg-secure">
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="var(--clr-faint)" stroke-width="2"><rect x="3" y="11" width="18" height="10" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
      Защищено PCI DSS
    </div>
    <div class="pg-result" id="w1x">
      <div class="pg-spinner" id="w1sp"></div>
      <div class="pg-success" id="w1ok">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#00b894" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="16 8 10 16 7 12"/></svg>
        <span class="pg-success-t">Платёж выполнен</span>
        <span class="pg-success-sub">Спасибо! Ваш платёж прошёл успешно.</span>
      </div>
    </div>
  </div>
</div>
<style>
.pg-card{margin:12px 0;background:var(--clr-surface);border:1px solid var(--clr-border);border-radius:20px;overflow:hidden}
.pg-header{display:flex;align-items:center;gap:10px;padding:18px 24px 0;font-size:15px;font-weight:600;color:var(--clr-heading)}
.pg-body{display:flex;flex-direction:column;gap:18px;padding:20px 24px 24px}
.pg-fld{display:flex;flex-direction:column;gap:5px}
.pg-lbl{font-size:12px;color:var(--clr-faint);font-weight:500;letter-spacing:.3px;text-transform:uppercase}
.pg-inp-wrap{position:relative;display:flex;align-items:center}
.pg-inp{width:100%;padding:12px 14px;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:12px;color:var(--clr-text);font-size:15px;font-family:'SF Mono','Fira Code',monospace;box-sizing:border-box;transition:border-color .25s,box-shadow .25s;letter-spacing:.5px}
.pg-inp:focus{outline:none;border-color:var(--clr-accent);box-shadow:0 0 0 3px color-mix(in srgb,var(--clr-accent) 18%,transparent)}
.pg-inp::placeholder{color:var(--clr-faint);opacity:.5;letter-spacing:0}
.pg-card-icon{position:absolute;right:12px;pointer-events:none;opacity:.6}
.pg-cvv-icon{position:absolute;right:12px;pointer-events:none;opacity:.5}
.pg-currency{position:absolute;left:14px;color:var(--clr-faint);font-size:14px;font-weight:500;pointer-events:none}
.pg-inp-amt{padding-left:28px}
.pg-row{display:grid;grid-template-columns:1fr 80px 1fr;gap:12px}
.pg-btn{display:flex;align-items:center;justify-content:center;gap:10px;padding:14px;background:var(--clr-accent);border:none;border-radius:14px;color:#fff;font-size:16px;font-weight:600;cursor:pointer;transition:opacity .25s,transform .15s;font-family:inherit}
.pg-btn:hover{opacity:.9;transform:translateY(-1px)}
.pg-btn:active{transform:translateY(0)}
.pg-secure{display:flex;align-items:center;justify-content:center;gap:6px;font-size:11px;color:var(--clr-faint);opacity:.6}
.pg-result{text-align:center;padding:8px 0 0}
.pg-spinner{display:none;width:32px;height:32px;border:2px solid var(--clr-border);border-top-color:var(--clr-accent);border-radius:50%;animation:pgs .7s linear infinite;margin:0 auto}
.pg-success{display:none;flex-direction:column;align-items:center;gap:4px;padding:8px 0}
.pg-success-t{color:#00b894;font-weight:600;font-size:15px}
.pg-success-sub{color:var(--clr-faint);font-size:12px;opacity:.6}
@keyframes pgs{to{transform:rotate(360deg)}}
@media (min-width:768px){.pg-card{max-width:460px;margin-left:auto;margin-right:auto}}
@media (max-width:500px){.pg-row{grid-template-columns:1fr 1fr}.pg-row .pg-fld:last-child{grid-column:1/-1}}
</style>
<script>(function(){
function fm(id,fn){var el=document.getElementById('w1'+id);if(el)el.addEventListener('input',fn)}
fm('n',function(e){e.target.value=e.target.value.replace(/\\D/g,'').replace(/(.{4})/g,'$1 ').trim()});
fm('e',function(e){var v=e.target.value.replace(/[^\\d\\/]/g,'');if(v.length===2&&!v.includes('/'))v=v+' / ';e.target.value=v});
fm('c',function(e){e.target.value=e.target.value.replace(/\\D/g,'')});
document.getElementById('w1b').addEventListener('click',function(){var b=this,x=document.getElementById('w1x'),sp=document.getElementById('w1sp'),ok=document.getElementById('w1ok');b.style.display='none';x.style.display='block';sp.style.display='block';ok.style.display='none';setTimeout(function(){sp.style.display='none';ok.style.display='flex'},1800)});
})();</script>""",
        "widget_css": "",
        "widget_js": ""
    },
    {
        "slug": "loyalty-program",
        "title": "Программа лояльности",
        "desc": "White-label платформа лояльности LOVII: баллы, уровни, кэшбэк, промокоды и геймификация. Готовая экосистема для любого бизнеса.",
        "meta_desc": "Демо white-label платформы лояльности: балльная система, уровни, кэшбэк, промокоды, push-уведомления. Интеграция с iiko и r_keeper.",
        "code": """// Начисление баллов
await loyalty.accruePoints({
  userId: 'user_456',
  amount: 350,
  source: 'purchase',
  orderId: 'ORD-2024-8912'
});

// Проверка уровня пользователя
const level = await loyalty.getUserLevel('user_456');
// { level: 'gold', multiplier: 1.5, benefits: [...] }

// Активация промокода
const promo = await loyalty.applyPromo({
  code: 'WELCOME25',
  userId: 'user_456'
});""",
        "features": ["Балльно-бонусная система с уровнями", "Промокоды и персональные офферы", "Push и Email-уведомления", "Интеграция с iiko, r_keeper, 1С", "Аналитика LTV и когорт", "White Label под ваш бренд"],
        "tags": ["React", "Node.js", "PostgreSQL", "Redis", "Kafka"],
        "gradient": "#fd79a8,#e84393",
        "widget_html": """<div class="dw">
  <h3 class="dw-t">🏆 Программа лояльности</h3>
  <div style="display:flex;gap:8px;margin-bottom:14px">
    <div class="loy-t" data-l="silver"><div style="font-size:20px">🥈</div><div style="font-size:12px;font-weight:600;color:var(--clr-heading);margin-top:2px">Silver</div><div style="font-size:10px;color:var(--clr-muted)">0 баллов</div></div>
    <div class="loy-t" data-l="gold"><div style="font-size:20px">🥇</div><div style="font-size:12px;font-weight:600;color:var(--clr-heading);margin-top:2px">Gold</div><div style="font-size:10px;color:var(--clr-muted)">от 1 000</div></div>
    <div class="loy-t" data-l="platinum"><div style="font-size:20px">💎</div><div style="font-size:12px;font-weight:600;color:var(--clr-heading);margin-top:2px">Platinum</div><div style="font-size:10px;color:var(--clr-muted)">от 3 000</div></div>
  </div>
  <div style="padding:14px;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:12px;margin-bottom:12px">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
      <span style="font-size:13px;font-weight:500;color:var(--clr-text)">👤 Клиент: <span id="loy-name">Анна С.</span></span>
      <span id="loy-bal" style="font-size:24px;font-weight:700;color:var(--clr-heading);font-variant-numeric:tabular-nums">2 450</span>
    </div>
    <div style="height:6px;background:var(--clr-surface);border-radius:3px;overflow:hidden;margin-bottom:4px"><div id="loy-bar" style="height:100%;width:45%;background:linear-gradient(90deg,var(--clr-accent),#f6d365);border-radius:3px;transition:width .5s"></div></div>
    <div style="display:flex;justify-content:space-between;font-size:11px;color:var(--clr-muted)"><span id="loy-level">Gold</span><span id="loy-next"></span></div>
  </div>
  <div id="loy-b" style="display:flex;flex-direction:column;gap:5px;margin-bottom:12px"></div>
  <div style="display:flex;gap:6px;margin-bottom:12px">
    <button class="dw-btn" id="loy-earn">💳 Покупка 5 000 ₽</button>
    <button class="dw-btn dw-btn-o" id="loy-redeem">🎁 Списать</button>
  </div>
  <div id="loy-r" style="display:none;margin-bottom:12px"><div style="font-size:13px;font-weight:600;color:var(--clr-heading);margin-bottom:8px">Выберите вознаграждение:</div><div id="loy-shop" style="display:flex;flex-direction:column;gap:6px"></div></div>
  <div style="margin-bottom:12px"><div style="font-size:13px;font-weight:600;color:var(--clr-heading);margin-bottom:8px">📊 Статистика программы</div><div style="display:flex;gap:8px"><div style="flex:1;text-align:center;padding:10px 6px;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:10px"><div id="loy-mem" style="font-size:20px;font-weight:700;color:var(--clr-heading)">256</div><div style="font-size:10px;color:var(--clr-muted)">участников</div></div><div style="flex:1;text-align:center;padding:10px 6px;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:10px"><div id="loy-pts" style="font-size:20px;font-weight:700;color:var(--clr-heading)">15.4K</div><div style="font-size:10px;color:var(--clr-muted)">баллов выдано</div></div><div style="flex:1;text-align:center;padding:10px 6px;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:10px"><div id="loy-red" style="font-size:20px;font-weight:700;color:var(--clr-heading)">89</div><div style="font-size:10px;color:var(--clr-muted)">списаний</div></div></div></div>
  <div><div style="font-size:13px;font-weight:600;color:var(--clr-heading);margin-bottom:8px">📢 Активные кампании</div><div id="loy-camps" style="display:flex;flex-direction:column;gap:6px;margin-bottom:8px"><div class="loy-camp"><span style="font-size:16px">🔥</span><span style="flex:1;font-size:13px;color:var(--clr-text)">Двойные баллы на всё</span><span style="font-size:11px;color:var(--clr-accent);font-weight:600">до 30 июня</span></div></div><button class="dw-btn-sm" id="loy-add">+ Создать кампанию</button></div>
  <div id="loy-msg" style="display:none;margin-top:12px;padding:10px 14px;border-radius:10px;font-size:13px;font-weight:500"></div>
</div>
<style>.dw{margin:12px 0;background:var(--clr-surface);border:1px solid var(--clr-border);border-radius:16px;padding:24px}.dw-t{font-size:16px;font-weight:600;margin:0 0 16px;color:var(--clr-heading)}.dw-btn{padding:10px;border:none;border-radius:10px;font-size:13px;font-weight:600;cursor:pointer;transition:opacity .2s;flex:1}.dw-btn:hover{opacity:.85}.dw-btn-o{background:var(--clr-bg);border:1px solid var(--clr-border);color:var(--clr-text)}.dw-btn-sm{padding:8px 14px;background:none;border:1px dashed var(--clr-border);border-radius:8px;color:var(--clr-text);font-size:12px;font-weight:500;cursor:pointer;transition:all .2s;width:100%}.dw-btn-sm:hover{border-color:var(--clr-accent);color:var(--clr-accent)}.loy-t{flex:1;text-align:center;padding:8px 4px;border:2px solid var(--clr-border);border-radius:12px;transition:all .4s;cursor:default}.loy-t.active{background:var(--clr-accent)12;border-color:var(--clr-accent)}.loy-camp{display:flex;align-items:center;gap:8px;padding:8px 12px;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:8px}.loy-shop-item{display:flex;align-items:center;gap:10px;padding:10px 12px;background:var(--clr-surface);border:1px solid var(--clr-border);border-radius:8px;cursor:pointer;transition:all .15s}.loy-shop-item:hover{border-color:var(--clr-accent);background:var(--clr-accent)06}.loy-shop-item:active{transform:scale(.98)}@keyframes fIn{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:translateY(0)}}@media(min-width:768px){.dw{max-width:480px;margin-left:auto;margin-right:auto}}</style>
<script>(function(){var bal=2450,mem=256,pts=15400,red=89,balEl=document.getElementById('loy-bal'),bar=document.getElementById('loy-bar'),levelEl=document.getElementById('loy-level'),nextEl=document.getElementById('loy-next'),bEl=document.getElementById('loy-b'),msg=document.getElementById('loy-msg'),rEl=document.getElementById('loy-r'),shop=document.getElementById('loy-shop'),memEl=document.getElementById('loy-mem'),ptsEl=document.getElementById('loy-pts'),redEl=document.getElementById('loy-red'),campEl=document.getElementById('loy-camps'),cards=document.querySelectorAll('.loy-t'),lvls=[{n:'Silver',m:0,b:[{i:'🎁',t:'Приветственный бонус 100 баллов'}]},{n:'Gold',m:1000,b:[{i:'💰',t:'Кешбэк 5% баллами'},{i:'🚚',t:'Бесплатная доставка'}]},{n:'Platinum',m:3000,b:[{i:'💰',t:'Кешбэк 10% баллами'},{i:'🚚',t:'Бесплатная доставка'},{i:'🎂',t:'Бонус в день рождения 500 баллов'},{i:'⭐',t:'Персональный менеджер'}]}],rw=[{e:'Скидка 10%',p:500,i:'🏷️'},{e:'Бесплатная доставка',p:300,i:'🚚'},{e:'Подарок при заказе',p:800,i:'🎁'}],camps=['Двойные баллы на всё'];function fmt(n){return n.toLocaleString('ru')}function upd(){var cu=lvls.filter(function(l){return bal>=l.m}),cl=cu[cu.length-1];cards.forEach(function(c){c.classList.toggle('active',c.dataset.l===cl.n.toLowerCase())});levelEl.textContent=cl.n;var nx=lvls.filter(function(l){return l.m>bal});if(nx.length){nextEl.textContent=nx[0].n+' ('+fmt(nx[0].m-bal)+' баллов)'}else{nextEl.textContent='Максимальный уровень'}bar.style.width=Math.min(100,(bal-(cl.m||0))/((nx.length?nx[0].m:bal)-cl.m)*100)+'%';bEl.innerHTML='';cl.b.forEach(function(b){var e=document.createElement('div');e.style.cssText='display:flex;align-items:center;gap:8px;padding:7px 10px;background:var(--clr-surface);border:1px solid var(--clr-border);border-radius:8px;font-size:12px;color:var(--clr-text);animation:fIn .25s';e.innerHTML='<span>'+b.i+'</span><span>'+b.t+'</span>';bEl.appendChild(e)});memEl.textContent=fmt(mem);ptsEl.textContent=pts>=1000?fmt(Math.round(pts/100)/10)+'K':fmt(pts);redEl.textContent=fmt(red)}function rebuildShop(){shop.innerHTML='';rw.forEach(function(r,i){var e=document.createElement('div');e.className='loy-shop-item';e.innerHTML='<span style="font-size:18px">'+r.i+'</span><span style="flex:1;font-size:13px;color:var(--clr-text)">'+r.e+'</span><span style="font-size:12px;font-weight:600;color:var(--clr-muted)">'+fmt(r.p)+' баллов</span>';e.addEventListener('click',function(){if(bal<r.p){msg.style.display='block';msg.style.background='#e1705514';msg.style.border='1px solid #e1705544';msg.style.color='#e17055';msg.textContent='Недостаточно баллов';return}bal-=r.p;red++;balEl.textContent=fmt(bal);redEl.textContent=fmt(red);upd();rEl.style.display='none';msg.style.display='block';msg.style.background='#00b89414';msg.style.border='1px solid #00b89444';msg.style.color='#00b894';msg.textContent='🎉 '+r.e+' — баллы списаны'});shop.appendChild(e)})}document.getElementById('loy-earn').addEventListener('click',function(){msg.style.display='none';bal+=100;pts+=100;balEl.textContent=fmt(bal);ptsEl.textContent=pts>=1000?fmt(Math.round(pts/100)/10)+'K':fmt(pts);upd();msg.style.display='block';msg.style.background='#00b89414';msg.style.border='1px solid #00b89444';msg.style.color='#00b894';msg.textContent='+100 баллов за покупку 5 000 ₽'});document.getElementById('loy-redeem').addEventListener('click',function(){rebuildShop();rEl.style.display=rEl.style.display==='none'?'block':'none'});document.getElementById('loy-add').addEventListener('click',function(){var names=['🔥 Кешбэк удвоен','🎂 День рождения — баллы x3','⚡ Flash sale: +200 баллов','💎 Platinum early access','🏆 Конкурс: 2x баллы'];var n=names[Math.floor(Math.random()*names.length)];if(camps.indexOf(n)>-1)names=n;var el=document.createElement('div');el.className='loy-camp';el.style.animation='fIn .3s';el.innerHTML='<span style="font-size:16px">'+n.split(' ')[0]+'</span><span style="flex:1;font-size:13px;color:var(--clr-text)">'+n.split(' ').slice(1).join(' ')+'</span><span style="font-size:11px;color:var(--clr-accent);font-weight:600">с '+new Date().toLocaleDateString('ru-RU',{day:'numeric',month:'long'})+'</span>';campEl.appendChild(el);camps.push(n);mem++;memEl.textContent=fmt(mem)});upd()})();</script>""",
        "widget_css": "",
        "widget_js": ""
    },
    {
        "slug": "credit-conveyor",
        "title": "Кредитный конвейер",
        "desc": "Автоматизированный кредитный конвейер: скоринг, принятие решений, выдача. Интеграция с БКИ и банковскими системами.",
        "meta_desc": "Демо кредитного конвейера: скоринг-модели, ML-принятие решений, интеграция с БКИ. От заявки до выдачи за 5 минут.",
        "code": """// Создание заявки на кредит
const application = await credit.createApplication({
  client: {
    firstName: 'Иван',
    lastName: 'Петров',
    passport: '4010 123456',
    income: 120000
  },
  product: 'consumer_loan',
  amount: 500000,
  term: 12
});

// Запуск скоринга
const decision = await credit.score(application.id);
// { status: 'approved', rate: 15.9, limit: 500000 }

// Выдача
await credit.issue(application.id);""",
        "features": ["Скоринг-модели (ML + правила)", "Интеграция с 4+ БКИ", "Андеррайтинг в реальном времени", "Конвейерная обработка заявок", "Личный кабинет заёмщика", "Соответствие 161-ФЗ, 152-ФЗ"],
        "tags": ["Python", "ML", "PostgreSQL", "Kubernetes", "161-ФЗ"],
        "gradient": "#00b894,#55efc4",
        "widget_html": """<div class="dw">
  <h3 class="dw-t">📊 Кредитный калькулятор</h3>
  <div class="dw-b">
    <div class="dw-f"><label class="dw-l">Сумма кредита: <strong id="cc-a">500 000</strong> ₽</label><input class="dw-i" id="cc-as" type="range" min="100000" max="5000000" step="10000" value="500000" style="accent-color:var(--clr-accent);width:100%"></div>
    <div class="dw-f"><label class="dw-l">Срок: <strong id="cc-t">12</strong> мес.</label><input class="dw-i" id="cc-ts" type="range" min="3" max="24" step="1" value="12" style="accent-color:var(--clr-accent);width:100%"></div>
    <div style="padding:16px;background:var(--clr-bg);border-radius:12px;margin:8px 0;text-align:center">
      <div style="font-size:12px;color:var(--clr-muted)">Ежемесячный платёж</div>
      <div id="cc-pm" style="font-size:28px;font-weight:700;color:var(--clr-heading);font-variant-numeric:tabular-nums">43 124 ₽</div>
      <div style="font-size:12px;color:var(--clr-muted);margin-top:4px">Ставка: 12.9% годовых</div>
    </div>
    <div style="display:flex;align-items:center;justify-content:center;gap:8px;color:#00b894;font-weight:600;font-size:14px"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#00b894" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> Предварительное одобрение</div>
  </div>
</div>
<style>.dw{margin:12px 0;background:var(--clr-surface);border:1px solid var(--clr-border);border-radius:16px;padding:24px}.dw-t{font-size:16px;font-weight:600;margin:0 0 16px;color:var(--clr-heading)}.dw-b{display:flex;flex-direction:column;gap:10px}.dw-f{display:flex;flex-direction:column;gap:3px}.dw-l{font-size:13px;color:var(--clr-text);font-weight:500}.dw-i{background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:10px;color:var(--clr-text);font-size:14px;box-sizing:border-box}.dw-i[type=range]{border:none;background:none;padding:4px 0}@media(min-width:768px){.dw{max-width:520px;margin-left:auto;margin-right:auto}}</style>
<script>(function(){var as=document.getElementById('cc-as'),ts=document.getElementById('cc-ts'),pm=document.getElementById('cc-pm'),ae=document.getElementById('cc-a'),te=document.getElementById('cc-t');function calc(){var a=parseFloat(as.value),t=parseInt(ts.value),r=0.129/12;if(r===0){pm.textContent=Math.round(a/t).toLocaleString('ru')+' ₽'}else{var mp=a*r*Math.pow(1+r,t)/(Math.pow(1+r,t)-1);pm.textContent=Math.round(mp).toLocaleString('ru')+' ₽'}ae.textContent=Math.round(a).toLocaleString('ru');te.textContent=t}as.addEventListener('input',calc);ts.addEventListener('input',calc);calc()})();</script>""",
        "widget_css": "",
        "widget_js": ""
    },
    {
        "slug": "marketplace",
        "title": "Маркетплейс",
        "desc": "Готовая платформа маркетплейса: каталог, корзина, оплата, доставка, отзывы и личный кабинет продавца.",
        "meta_desc": "Демо маркетплейс-платформы: каталог товаров, корзина, мультиэквайринг, доставка, личный кабинет продавца. Full-stack решение.",
        "widget_html": """<div class="dw">
  <h3 class="dw-t" style="display:flex;justify-content:space-between;align-items:center">🛒 Маркетплейс <span id="mp-cnt-badge" style="background:var(--clr-accent);color:#fff;font-size:11px;font-weight:600;min-width:20px;height:20px;border-radius:10px;display:none;align-items:center;justify-content:center">0</span></h3>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:10px">
    <div class="mp-c"><div class="mp-img" style="background:linear-gradient(135deg,#6c5ce7,#a29bfe)">📱</div><div class="mp-n">Phone X Pro</div><div class="mp-p">79 990 ₽</div><button class="dw-btn mp-b" data-n="Phone X Pro" data-p="79990">В корзину</button></div>
    <div class="mp-c"><div class="mp-img" style="background:linear-gradient(135deg,#00b894,#55efc4)">💻</div><div class="mp-n">NoteBook Air</div><div class="mp-p">129 990 ₽</div><button class="dw-btn mp-b" data-n="NoteBook Air" data-p="129990">В корзину</button></div>
    <div class="mp-c"><div class="mp-img" style="background:linear-gradient(135deg,#fd79a8,#e84393)">🎧</div><div class="mp-n">Headphones Pro</div><div class="mp-p">14 990 ₽</div><button class="dw-btn mp-b" data-n="Headphones Pro" data-p="14990">В корзину</button></div>
    <div class="mp-c"><div class="mp-img" style="background:linear-gradient(135deg,#fdcb6e,#f39c12)">⌚</div><div class="mp-n">Watch Ultra</div><div class="mp-p">49 990 ₽</div><button class="dw-btn mp-b" data-n="Watch Ultra" data-p="49990">В корзину</button></div>
  </div>
  <div id="mp-cart" style="display:none;margin-top:16px;padding:16px;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:12px">
    <div style="font-size:14px;font-weight:600;color:var(--clr-heading);margin-bottom:8px">Корзина</div>
    <div id="mp-items"></div>
    <div style="display:flex;justify-content:space-between;padding-top:8px;border-top:1px solid var(--clr-border);margin-top:8px;font-weight:700;color:var(--clr-heading)"><span>Итого:</span><span id="mp-total">0 ₽</span></div>
    <button class="dw-btn" id="mp-checkout-btn" style="margin-top:12px;width:100%">Оформить заказ</button>
  </div>
</div>
<div id="mp-modal" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.7);z-index:99999;align-items:center;justify-content:center">
  <div style="background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:16px;padding:32px;max-width:400px;width:90%;text-align:center">
    <h3 style="color:var(--clr-heading);margin-bottom:16px">Оформление заказа</h3>
    <div id="mp-modal-items" style="font-size:13px;color:var(--clr-muted);margin-bottom:16px;text-align:left"></div>
    <div id="mp-modal-total" style="font-size:18px;font-weight:700;color:var(--clr-heading);margin-bottom:20px"></div>
    <button class="dw-btn" id="mp-confirm" style="width:100%;margin-bottom:8px">Подтвердить заказ</button>
    <button class="dw-btn" id="mp-cancel" style="background:transparent;border:1px solid var(--clr-border);color:var(--clr-muted)">Отмена</button>
    <div id="mp-success" style="display:none;padding:20px"><svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00b894" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg><h3 style="color:#00b894;margin-top:12px">Заказ оформлен!</h3><p style="font-size:13px;color:var(--clr-muted);margin-top:4px">Номер: MK-<span id="mp-order-year"></span>-<span id="mp-order-num"></span></p></div>
  </div>
</div>
<style>.dw{margin:12px 0;background:var(--clr-surface);border:1px solid var(--clr-border);border-radius:16px;padding:24px}.dw-t{font-size:16px;font-weight:600;margin:0 0 16px;color:var(--clr-heading)}.dw-btn{padding:8px 12px;background:var(--clr-accent);border:none;border-radius:8px;color:#fff;font-size:13px;font-weight:600;cursor:pointer;transition:opacity .2s;width:100%}.dw-btn:hover{opacity:.85}.mp-c{background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:12px;padding:12px;text-align:center}.mp-img{width:100%;height:80px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:32px;margin-bottom:8px}.mp-n{font-size:13px;font-weight:500;color:var(--clr-text);margin-bottom:4px}.mp-p{font-size:15px;font-weight:700;color:var(--clr-heading);margin-bottom:8px}.mp-ci{display:flex;justify-content:space-between;padding:4px 0;font-size:13px;color:var(--clr-text)}.mp-ci button{background:none;border:none;color:var(--clr-muted);cursor:pointer;font-size:11px;text-decoration:underline;padding:0}@media(min-width:768px){.dw{max-width:640px;margin-left:auto;margin-right:auto}}</style>
<script>(function(){
var items={},badge=document.getElementById('mp-cnt-badge'),cart=document.getElementById('mp-cart'),list=document.getElementById('mp-items'),total=document.getElementById('mp-total'),modal=document.getElementById('mp-modal'),mItems=document.getElementById('mp-modal-items'),mTotal=document.getElementById('mp-modal-total');
function render(){var html='',t=0,c=0;for(var k in items){var it=items[k];html+='<div class="mp-ci"><span>'+it.n+' × '+it.q+'</span><span>'+((it.p*it.q).toLocaleString('ru'))+' ₽ <button class="mp-rm" data-k="'+k+'">✕</button></span></div>';t+=it.p*it.q;c+=it.q}list.innerHTML=html;total.textContent=t.toLocaleString('ru')+' ₽';badge.textContent=c;badge.style.display=c?'flex':'none';cart.style.display=c?'block':'none';Array.from(list.querySelectorAll('.mp-rm')).forEach(function(b){b.addEventListener('click',function(){var k=this.dataset.k;delete items[k];render()})})};
document.querySelectorAll('.mp-b').forEach(function(b){b.addEventListener('click',function(){var n=this.dataset.n,p=parseInt(this.dataset.p);if(!items[n])items[n]={n:n,p:p,q:0};items[n].q++;render();this.textContent='✓ '+n;var t=this;setTimeout(function(){t.textContent='В корзину'},800)})});
document.getElementById('mp-checkout-btn').addEventListener('click',function(){var h='';for(var k in items){h+='<div style="display:flex;justify-content:space-between;padding:2px 0"><span>'+items[k].n+' × '+items[k].q+'</span><span>'+((items[k].p*items[k].q).toLocaleString('ru'))+' ₽</span></div>'}mItems.innerHTML=h;var t=0;for(var k in items)t+=items[k].p*items[k].q;mTotal.textContent='Итого: '+t.toLocaleString('ru')+' ₽';modal.style.display='flex'});
document.getElementById('mp-confirm').addEventListener('click',function(){var s=document.getElementById('mp-success');s.style.display='block';s.querySelector('h3').textContent='Заказ оформлен!';document.getElementById('mp-order-year').textContent=new Date().getFullYear();document.getElementById('mp-order-num').textContent=Math.floor(100000+Math.random()*900000);document.querySelector('#mp-modal > div > h3').style.display='none';document.getElementById('mp-modal-items').style.display='none';document.getElementById('mp-modal-total').style.display='none';this.style.display='none';document.getElementById('mp-cancel').style.display='none';items={};render();setTimeout(function(){modal.style.display='none';location.reload()},2500)});
document.getElementById('mp-cancel').addEventListener('click',function(){modal.style.display='none'});
modal.addEventListener('click',function(e){if(e.target===modal)modal.style.display='none'});
})();</script>""",
        "code": """// Добавление товара продавцом
await marketplace.addProduct({
  sellerId: 'seller_789',
  name: 'Смартфон X Pro',
  price: 79990,
  category: 'electronics',
  stock: 50
});

// Оформление заказа покупателем
const order = await marketplace.checkout({
  items: [
    { productId: 'prod_123', quantity: 1 },
    { productId: 'prod_456', quantity: 2 }
  ],
  delivery: 'cdek',
  paymentMethod: 'card'
});

// Сплитование выплаты продавцу
await marketplace.settle(order.id);""",
        "features": ["Каталог с фильтрацией и поиском", "Мультиэквайринг и сплитование", "Личный кабинет продавца", "Интеграция с СДЭК, Почтой России", "Система отзывов и рейтингов", "Аналитика продаж"],
        "tags": ["Vue.js", "Node.js", "PostgreSQL", "Elasticsearch", "Redis"],
        "gradient": "#0984e3,#74b9ff"
    },
    {
        "slug": "payment-terminal",
        "title": "Платёжный терминал",
        "desc": "POS-терминал для приёма платежей: карты, NFC, QR-коды, SBP. Работает на Android и iOS.",
        "meta_desc": "Демо мобильного POS-терминала: приём платежей по картам, NFC, SBP, QR. Соответствие PCI DSS. Примеры интеграции.",
        "code": """// Инициализация терминала
const terminal = new PaymentTerminal({
  merchantId: 'merchant_456',
  terminalId: 'T-001',
  apiKey: 'sk_live_***'
});

// Приём платежа по карте
const payment = await terminal.processCard({
  amount: 3500.00,
  currency: 'RUB',
  cardPresent: true // чип/NFC
});

// Оплата по QR (SBP)
const qrPayment = await terminal.processSBP({
  amount: 1299.00,
  bank: 'sbp'
});

// Печать чека
await terminal.printReceipt(payment.id);""",
        "features": ["Приём карт, NFC, QR, SBP", "Онлайн-касса (ФНС/ККТ)", "Печать чеков (Bluetooth)", "Возвраты и отмены", "Офлайн-режим", "Аналитика и отчёты"],
        "tags": ["Swift", "Kotlin", "Flutter", "PCI DSS", "54-ФЗ"],
        "gradient": "#fdcb6e,#f39c12",
        "widget_html": """<div class="dw">
  <h3 class="dw-t">💳 POS-терминал</h3>
  <div style="display:flex;flex-direction:column;align-items:center;gap:12px">
    <div style="background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:12px;padding:16px;width:100%;text-align:center">
      <div style="font-size:12px;color:var(--clr-muted);margin-bottom:4px">Сумма к оплате</div>
      <div id="pt-amt" style="font-size:36px;font-weight:700;color:var(--clr-heading);font-variant-numeric:tabular-nums;min-height:44px">0 ₽</div>
    </div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;width:100%;max-width:280px">
      <button class="pt-k" data-v="1">1</button><button class="pt-k" data-v="2">2</button><button class="pt-k" data-v="3">3</button>
      <button class="pt-k" data-v="4">4</button><button class="pt-k" data-v="5">5</button><button class="pt-k" data-v="6">6</button>
      <button class="pt-k" data-v="7">7</button><button class="pt-k" data-v="8">8</button><button class="pt-k" data-v="9">9</button>
      <button class="pt-k" data-v="00">00</button><button class="pt-k" data-v="0">0</button><button class="pt-k pt-clr" id="pt-clr">C</button>
    </div>
    <button class="dw-btn" id="pt-pay" style="width:100%;max-width:280px">Оплатить</button>
    <div id="pt-st" style="display:none;text-align:center;padding:12px">
      <div class="dw-sp" id="pt-sp"></div>
      <div id="pt-ok" style="display:none;color:#00b894;font-weight:600;font-size:15px">✅ Оплата принята</div>
      <button id="pt-reset" style="display:none;margin-top:12px;padding:8px 16px;background:none;border:1px solid var(--clr-border);border-radius:8px;color:var(--clr-muted);font-size:12px;cursor:pointer;transition:all .2s">⟳ Новый платёж</button>
    </div>
  </div>
</div>
<style>.dw{margin:12px 0;background:var(--clr-surface);border:1px solid var(--clr-border);border-radius:16px;padding:24px}.dw-t{font-size:16px;font-weight:600;margin:0 0 16px;color:var(--clr-heading)}.dw-btn{padding:12px;background:var(--clr-accent);border:none;border-radius:10px;color:#fff;font-size:15px;font-weight:600;cursor:pointer;transition:opacity .2s}.dw-btn:hover{opacity:.85}.dw-sp{width:28px;height:28px;border:2px solid var(--clr-border);border-top-color:var(--clr-accent);border-radius:50%;animation:dws .7s linear infinite;margin:0 auto}.pt-k{padding:14px;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:10px;color:var(--clr-text);font-size:20px;font-weight:600;cursor:pointer;transition:all .15s;text-align:center}.pt-k:hover{background:var(--clr-surface);border-color:var(--clr-accent)}.pt-k:active{transform:scale(.95)}.pt-clr{color:#e17055;border-color:#e1705544}#pt-reset:hover{border-color:var(--clr-accent);color:var(--clr-accent)}@keyframes dws{to{transform:rotate(360deg)}}@media(min-width:768px){.dw{max-width:400px;margin-left:auto;margin-right:auto}}</style>
<script>(function(){var amt=0,e=document.getElementById('pt-amt'),b=document.getElementById('pt-pay'),st=document.getElementById('pt-st'),sp=document.getElementById('pt-sp'),ok=document.getElementById('pt-ok'),rs=document.getElementById('pt-reset');document.querySelectorAll('.pt-k').forEach(function(k){k.addEventListener('click',function(){if(this.id==='pt-clr'){amt=0}else{var v=this.dataset.v;amt=amt*100+parseInt(v)}e.textContent=Math.round(amt).toLocaleString('ru')+' ₽'});});b.addEventListener('click',function(){if(amt<=0)return;b.style.display='none';st.style.display='block';sp.style.display='block';ok.style.display='none';rs.style.display='none';setTimeout(function(){sp.style.display='none';ok.style.display='block';rs.style.display='inline-block'},1500);});rs.addEventListener('click',function(){amt=0;e.textContent='0 ₽';b.style.display='block';st.style.display='none';sp.style.display='none';ok.style.display='none';rs.style.display='none';});})();</script>""",
        "widget_css": "",
        "widget_js": ""
    },
    {
        "slug": "chatbot-support",
        "title": "Чат-бот техподдержки",
        "desc": "AI-чат-бот техподдержки с NLP: ответы на вопросы, создание тикетов, эскалация на оператора. Интеграция с Telegram, WhatsApp, VK.",
        "meta_desc": "Демо AI-чат-бота техподдержки: NLP, создание тикетов, эскалация, интеграция с Telegram/WhatsApp/VK. Примеры кода.",
        "code": """// Обработка входящего сообщения
const response = await chatbot.handleMessage({
  channel: 'telegram',
  userId: 'tg_123456',
  text: 'Как пополнить баланс?'
});

// Ответ бота
// { type: 'text', text: 'Пополнить баланс можно...' }

// Создание тикета (эскалация)
const ticket = await chatbot.createTicket({
  userId: 'tg_123456',
  reason: 'Не прошёл платёж',
  priority: 'high',
  assignTo: 'support_team'
});

// Отправка уведомления оператору
await chatbot.notifyOperator(ticket.id);""",
        "features": ["NLP-движок с кастомизацией", "Интеграция с Telegram, WhatsApp, VK", "Создание и эскалация тикетов", "База знаний (FAQ)", "Аналитика диалогов", "Передача оператору с контекстом"],
        "tags": ["Python", "Node.js", "NLP/LLM", "Redis", "WebSocket"],
        "gradient": "#e17055,#fab1a0",
        "widget_html": """<div class="dw">
  <h3 class="dw-t">💬 Чат техподдержки</h3>
  <div style="border:1px solid var(--clr-border);border-radius:12px;overflow:hidden;background:var(--clr-bg)">
    <div id="ch-msgs" style="height:220px;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:8px">
      <div style="align-self:flex-start;background:var(--clr-surface);padding:10px 14px;border-radius:12px 12px 12px 4px;max-width:80%;font-size:14px;color:var(--clr-text);border:1px solid var(--clr-border)">Здравствуйте! Чем могу помочь?</div>
    </div>
    <div style="display:flex;gap:8px;padding:10px 12px;border-top:1px solid var(--clr-border)">
      <input id="ch-inp" placeholder="Напишите сообщение..." class="dw-i" style="flex:1" onkeydown="if(event.key==='Enter')chSend()">
      <button class="dw-btn" id="ch-btn" style="padding:10px 16px;font-size:13px" onclick="chSend()">→</button>
    </div>
  </div>
  <div style="margin-top:10px;display:flex;flex-wrap:wrap;gap:6px">
    <button class="dw-btn ch-q" style="padding:6px 12px;font-size:12px" data-q="Привет">Привет</button>
    <button class="dw-btn ch-q" style="padding:6px 12px;font-size:12px" data-q="Как пополнить?">Как пополнить?</button>
    <button class="dw-btn ch-q" style="padding:6px 12px;font-size:12px" data-q="Проблема с платежом">Проблема с платежом</button>
  </div>
</div>
<style>.dw{margin:12px 0;background:var(--clr-surface);border:1px solid var(--clr-border);border-radius:16px;padding:24px}.dw-t{font-size:16px;font-weight:600;margin:0 0 16px;color:var(--clr-heading)}.dw-i{width:100%;padding:10px 14px;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:10px;color:var(--clr-text);font-size:14px;box-sizing:border-box}.dw-i:focus{outline:none;border-color:var(--clr-accent)}.dw-btn{padding:12px;background:var(--clr-accent);border:none;border-radius:10px;color:#fff;font-size:15px;font-weight:600;cursor:pointer;transition:opacity .2s}.dw-btn:hover{opacity:.85}@media(min-width:768px){.dw{max-width:520px;margin-left:auto;margin-right:auto}}</style>
<script>var chMsgs=document.getElementById('ch-msgs'),chInp=document.getElementById('ch-inp');var chRes={'привет':'Привет! Чем могу помочь?','как пополнить':'Пополнить баланс можно через личный кабинет или приложение. Выберите способ: карта, SBP или кошелёк.','проблема с платежом':'Опишите проблему подробнее. Возможно, потребуется проверить статус транзакции. Напишите номер операции.','по умолчанию':'Передаю ваш вопрос специалисту. Пожалуйста, ожидайте.'};function chAdd(m,u){var d=document.createElement('div');d.style.cssText='align-self:'+(u?'flex-end':'flex-start')+';background:'+(u?'var(--clr-accent)':'var(--clr-surface)')+';padding:10px 14px;border-radius:'+(u?'4px 12px 12px 12px':'12px 12px 12px 4px')+';max-width:80%;font-size:14px;color:'+(u?'#fff':'var(--clr-text)')+';'+(u?'':'border:1px solid var(--clr-border)');d.textContent=m;chMsgs.appendChild(d);chMsgs.scrollTop=chMsgs.scrollHeight}function chSend(){var t=chInp.value.trim();if(!t)return;chAdd(t,1);chInp.value='';var r=t.toLowerCase();var a=chRes[r]||Object.keys(chRes).filter(function(k){return r.includes(k)}).map(function(k){return chRes[k]})[0]||chRes['по умолчанию'];setTimeout(function(){chAdd(a,0)},500)}document.querySelectorAll('.ch-q').forEach(function(b){b.addEventListener('click',function(){chInp.value=this.dataset.q;chSend()})});</script>""",
        "widget_css": "",
        "widget_js": ""
    },
    {
        "slug": "analytics-dashboard",
        "title": "Аналитическая панель",
        "desc": "Real-time дашборд с метриками бизнеса: DAU/MAU, LTV, конверсии, когортный анализ, funnel report.",
        "meta_desc": "Демо аналитической панели: real-time метрики, когорты, воронки, LTV. Примеры кода построения дашбордов и API.",
        "code": """// Получение метрик за период
const metrics = await analytics.getMetrics({
  period: 'last_30_days',
  metrics: ['dau', 'mau', 'conversion', 'ltv'],
  groupBy: 'day'
});

// Построение воронки
const funnel = await analytics.buildFunnel({
  steps: ['visit', 'register', 'deposit', 'purchase'],
  startDate: '2024-01-01',
  endDate: '2024-06-30'
});

// Когортный анализ
const cohorts = await analytics.cohortAnalysis({
  period: 'monthly',
  metric: 'retention'
});""",
        "features": ["Real-time метрики (WebSocket)", "Когортный анализ", "Воронки конверсий", "Custom report builder", "Экспорт в PDF/Excel", "Alerting и аномалии"],
        "tags": ["React", "D3.js", "ClickHouse", "Go", "Kafka"],
        "gradient": "#74b9ff,#0984e3",
        "widget_html": """<div class="dw">
  <h3 class="dw-t">📈 Аналитическая панель</h3>
  <p style="font-size:13px;color:var(--clr-muted);margin:-8px 0 14px">Кликните по метрике для детализации</p>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px">
    <div class="ad-k" data-i="0"><div style="display:flex;justify-content:space-between;align-items:flex-start"><span style="font-size:11px;color:var(--clr-muted)">DAU</span><span style="font-size:10px;color:#00b894;font-weight:600">+8.2%</span></div><div style="font-size:22px;font-weight:700;color:var(--clr-heading);font-variant-numeric:tabular-nums" id="ad-dau">0</div><div class="ad-sp" style="background:linear-gradient(90deg,#6c5ce7,transparent)"></div></div>
    <div class="ad-k" data-i="1"><div style="display:flex;justify-content:space-between;align-items:flex-start"><span style="font-size:11px;color:var(--clr-muted)">MAU</span><span style="font-size:10px;color:#00b894;font-weight:600">+12.1%</span></div><div style="font-size:22px;font-weight:700;color:var(--clr-heading);font-variant-numeric:tabular-nums" id="ad-mau">0</div><div class="ad-sp" style="background:linear-gradient(90deg,#0984e3,transparent)"></div></div>
    <div class="ad-k" data-i="2"><div style="display:flex;justify-content:space-between;align-items:flex-start"><span style="font-size:11px;color:var(--clr-muted)">LTV</span><span style="font-size:10px;color:#00b894;font-weight:600">+5.4%</span></div><div style="font-size:22px;font-weight:700;color:var(--clr-heading);font-variant-numeric:tabular-nums" id="ad-ltv">0</div><div class="ad-sp" style="background:linear-gradient(90deg,#00b894,transparent)"></div></div>
    <div class="ad-k" data-i="3"><div style="display:flex;justify-content:space-between;align-items:flex-start"><span style="font-size:11px;color:var(--clr-muted)">Конверсия</span><span style="font-size:10px;color:#e17055;font-weight:600">-0.3%</span></div><div style="font-size:22px;font-weight:700;color:var(--clr-heading);font-variant-numeric:tabular-nums" id="ad-conv">0</div><div class="ad-sp" style="background:linear-gradient(90deg,#e17055,transparent)"></div></div>
  </div>
  <div id="ad-detail" style="display:none;padding:10px 12px;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:8px;margin-bottom:12px;font-size:13px;color:var(--clr-text);line-height:1.6"></div>
  <div style="font-size:13px;font-weight:600;color:var(--clr-heading);margin-bottom:8px">Воронка конверсии <span style="font-weight:400;font-size:11px;color:var(--clr-muted)">(кликните по шагу)</span></div>
  <div style="display:flex;flex-direction:column;gap:5px;margin-bottom:14px">
    <div class="ad-f" data-i="0" style="width:100%"><span>Визит</span><span class="ad-fv">12 450</span></div>
    <div class="ad-f" data-i="1" style="width:78%"><span>Регистрация</span><span class="ad-fv">9 711</span></div>
    <div class="ad-f" data-i="2" style="width:52%"><span>Депозит</span><span class="ad-fv">6 474</span></div>
    <div class="ad-f" data-i="3" style="width:31%"><span>Покупка</span><span class="ad-fv">3 860</span></div>
  </div>
  <div id="ad-funnel-info" style="display:none;padding:8px 12px;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:8px;margin-bottom:14px;font-size:13px;color:var(--clr-text)"></div>
  <div style="font-size:13px;font-weight:600;color:var(--clr-heading);margin-bottom:4px">DAU за 2 недели</div>
  <div style="position:relative">
    <svg viewBox="0 0 280 80" style="width:100%;height:68px;display:block" id="ad-chart">
      <polyline id="ad-line" fill="none" stroke="var(--clr-accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      <polyline id="ad-fill" fill="url(#ad-grad)" stroke="none"/>
      <defs><linearGradient id="ad-grad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="var(--clr-accent)" stop-opacity=".25"/><stop offset="100%" stop-color="var(--clr-accent)" stop-opacity="0"/></linearGradient></defs>
    </svg>
    <div id="ad-tip" style="display:none;position:absolute;bottom:100%;left:0;transform:translateX(-50%);padding:3px 8px;background:var(--clr-heading);color:var(--clr-bg);border-radius:5px;font-size:11px;font-weight:600;white-space:nowrap;pointer-events:none"></div>
  </div>
  <div style="display:flex;justify-content:space-between;font-size:10px;color:var(--clr-muted);margin-top:2px"><span>1 нед</span><span>2 нед</span></div>
</div>
<style>.dw{margin:12px 0;background:var(--clr-surface);border:1px solid var(--clr-border);border-radius:16px;padding:24px}.dw-t{font-size:16px;font-weight:600;margin:0 0 16px;color:var(--clr-heading)}.ad-k{padding:12px;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:10px;cursor:pointer;transition:all .2s}.ad-k:hover{border-color:var(--clr-accent)}.ad-k.ad-sel{border-color:var(--clr-accent);box-shadow:0 0 0 2px var(--clr-accent)22}.ad-sp{height:2px;margin-top:6px;border-radius:2px;opacity:.4}.ad-f{display:flex;justify-content:space-between;align-items:center;padding:8px 12px;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:6px;font-size:13px;color:var(--clr-text);box-sizing:border-box;transition:width .8s;cursor:pointer}.ad-f:hover{border-color:var(--clr-accent)}.ad-f.ad-f-sel{border-color:var(--clr-accent);background:var(--clr-accent)0a}.ad-fv{font-weight:600;font-variant-numeric:tabular-nums;font-size:12px;color:var(--clr-muted)}@media(min-width:768px){.dw{max-width:560px;margin-left:auto;margin-right:auto}}</style>
<script>(function(){var data=[9600,10200,11800,12400,13100,12800,13500,14200,13800,14500,15100,14800,15600,16200];var padX=8,padY=4,w=280,h=80,iw=w-padX*2,ih=h-padY*2;var mx=Math.max.apply(null,data);var pts=data.map(function(v,i){return(i/(data.length-1)*iw+padX)+','+(ih-(v/mx*ih)+padY)}).join(' ');var fillPts='0,'+h+' '+pts+' '+iw+','+h;document.getElementById('ad-line').setAttribute('points',pts);document.getElementById('ad-fill').setAttribute('points',fillPts);var svg=document.getElementById('ad-chart'),tip=document.getElementById('ad-tip');data.forEach(function(v,i){var cx=i/(data.length-1)*iw+padX,cy=ih-(v/mx*ih)+padY;var c=document.createElementNS('http://www.w3.org/2000/svg','circle');c.setAttribute('cx',cx);c.setAttribute('cy',cy);c.setAttribute('r','4');c.setAttribute('fill','var(--clr-accent)');c.setAttribute('stroke','var(--clr-surface)');c.setAttribute('stroke-width','2');c.style.cursor='pointer';c.addEventListener('mouseenter',function(){tip.style.display='block';tip.textContent=v.toLocaleString('ru-RU');c.setAttribute('r','6')});c.addEventListener('mouseleave',function(){tip.style.display='none';c.setAttribute('r','4')});svg.appendChild(c)});function ct(el,v,s){var c=0,e=document.getElementById(el),i=setInterval(function(){c++;var d=Math.round(v*c/60);e.textContent=d.toLocaleString('ru-RU')+s;if(c>=60){clearInterval(i);e.textContent=v.toLocaleString('ru-RU')+s}},20)}ct('ad-dau',12450,'');ct('ad-mau',45200,'');ct('ad-ltv',12500,' ₽');setTimeout(function(){var el=document.getElementById('ad-conv'),c=0,i=setInterval(function(){c++;var d=Math.round(3.2*c/60*10)/10;el.textContent=d.toLocaleString('ru-RU')+'%';if(c>=60){clearInterval(i);el.textContent='3,2%'}},20)},200);var kpis=document.querySelectorAll('.ad-k'),detail=document.getElementById('ad-detail'),detailData=[['Пн: 11 200','Вт: 11 800','Ср: 12 400','Чт: 12 100','Пт: 13 000','Сб: 11 500','Вс: 10 800'],['1 нед: 41 200','2 нед: 43 800','3 нед: 44 100','4 нед: 45 200'],['30 д: 8 200 ₽','60 д: 11 300 ₽','90 д: 12 500 ₽'],['Organic 4.1%','Social 2.8%','Email 5.2%','Paid 1.9%']];kpis.forEach(function(k,i){k.addEventListener('click',function(){var isSel=k.classList.contains('ad-sel');kpis.forEach(function(x){x.classList.remove('ad-sel')});if(isSel){detail.style.display='none';return}k.classList.add('ad-sel');detail.style.display='block';detail.innerHTML=detailData[i].map(function(d){return'<span style="display:inline-block;margin:0 8px 4px 0;padding:4px 10px;background:var(--clr-surface);border:1px solid var(--clr-border);border-radius:6px;font-size:12px">'+d+'</span>'}).join('')})});var funnelSteps=document.querySelectorAll('.ad-f'),funnelInfo=document.getElementById('ad-funnel-info'),funnelLabels=['','Визит → Регистрация','Регистрация → Депозит','Депозит → Покупка'],funnelDrop=['','-22% потеря','-33% потеря','-40% потеря'],funnelVals=[12450,9711,6474,3860];funnelSteps.forEach(function(f,i){f.addEventListener('click',function(){if(i===0){funnelInfo.style.display='none';return}var isSel=f.classList.contains('ad-f-sel');funnelSteps.forEach(function(x){x.classList.remove('ad-f-sel')});if(isSel){funnelInfo.style.display='none';return}f.classList.add('ad-f-sel');funnelInfo.style.display='block';var prev=funnelVals[i-1],cur=funnelVals[i];funnelInfo.innerHTML='<strong>'+funnelLabels[i]+'</strong>: '+funnelDrop[i]+' ('+prev.toLocaleString('ru-RU')+' → '+cur.toLocaleString('ru-RU')+')'})})})();</script>""",
        "widget_css": "",
        "widget_js": ""
    },
    {
        "slug": "incident-monitoring",
        "title": "Мониторинг инцидентов",
        "desc": "Система мониторинга и оповещения: сбор метрик, алерты, on-call, postmortem, SLA-дашборд.",
        "meta_desc": "Демо системы мониторинга инцидентов: сбор метрик, алерты, on-call, postmortem, SLA-дашборд. Примеры кода интеграции.",
        "code": """// Создание алерта
await monitoring.createAlert({
  name: 'High CPU Usage',
  metric: 'cpu_usage',
  condition: '> 90',
  duration: '5m',
  severity: 'critical',
  channels: ['telegram', 'email', 'sms']
});

// Регистрация инцидента
const incident = await monitoring.incident({
  alertId: 'alert_789',
  status: 'firing',
  value: 94.5,
  threshold: 90
});

// Аcknowledge
await monitoring.acknowledge(incident.id, {
  assignee: 'devops_team',
  note: 'Начинаем диагностику' 
});""",
        "features": ["Сбор метрик (Prometheus/StatsD)", "Гибкие алерты с эскалацией", "On-call scheduling", "Postmortem и RCA", "SLA/SLO дашборд", "Интеграция с PagerDuty, Telegram"],
        "tags": ["Go", "Prometheus", "Grafana", "Kubernetes", "ClickHouse"],
        "gradient": "#2d3436,#636e72",
        "widget_html": """<div class="dw">
  <h3 class="dw-t">🔍 Мониторинг сервисов</h3>
  <div style="display:flex;flex-direction:column;gap:8px">
    <div class="im-r" data-s="ok"><span class="im-d im-g"></span><span class="im-n">API Gateway</span><span class="im-s">Operational</span></div>
    <div class="im-r" data-s="ok"><span class="im-d im-g"></span><span class="im-n">Database</span><span class="im-s">Operational</span></div>
    <div class="im-r" data-s="warn"><span class="im-d im-y"></span><span class="im-n">Cache (Redis)</span><span class="im-s">Degraded</span></div>
    <div class="im-r" data-s="ok"><span class="im-d im-g"></span><span class="im-n">Message Queue</span><span class="im-s">Operational</span></div>
    <div class="im-r" data-s="ok"><span class="im-d im-g"></span><span class="im-n">Frontend CDN</span><span class="im-s">Operational</span></div>
  </div>
  <div id="im-alert" style="display:none;margin-top:10px;padding:10px 14px;background:#e1705522;border:1px solid #e1705544;border-radius:10px;color:#e17055;font-size:13px;font-weight:500">⚠️ Инцидент: сервис недоступен</div>
  <div style="margin-top:10px;font-size:11px;color:var(--clr-muted)">Нажмите на сервис, чтобы переключить статус</div>
</div>
<style>.dw{margin:12px 0;background:var(--clr-surface);border:1px solid var(--clr-border);border-radius:16px;padding:24px}.dw-t{font-size:16px;font-weight:600;margin:0 0 16px;color:var(--clr-heading)}.im-r{display:flex;align-items:center;gap:10px;padding:10px 14px;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:10px;cursor:pointer;transition:all .2s}.im-r:hover{border-color:var(--clr-accent)}.im-d{width:10px;height:10px;border-radius:50%;flex-shrink:0}.im-g{background:#00b894;box-shadow:0 0 6px #00b89466}.im-y{background:#fdcb6e;box-shadow:0 0 6px #fdcb6e66}.im-red{background:#e17055;box-shadow:0 0 6px #e1705566}.im-n{flex:1;font-size:14px;font-weight:500;color:var(--clr-text)}.im-s{font-size:12px;color:var(--clr-muted)}@media(min-width:768px){.dw{max-width:640px;margin-left:auto;margin-right:auto}}</style>
<script>(function(){var st={0:'ok',1:'ok',2:'warn',3:'ok',4:'ok'},al=document.getElementById('im-alert');document.querySelectorAll('.im-r').forEach(function(r,i){r.addEventListener('click',function(){var sts=['ok','warn','down'];var ci=sts.indexOf(st[i]);st[i]=sts[(ci+1)%3];var d=r.querySelector('.im-d');d.className='im-d';if(st[i]==='ok'){d.classList.add('im-g');r.querySelector('.im-s').textContent='Operational'}else if(st[i]==='warn'){d.classList.add('im-y');r.querySelector('.im-s').textContent='Degraded'}else{d.classList.add('im-red');r.querySelector('.im-s').textContent='Down'}var hasDown=Object.values(st).some(function(s){return s==='down'});al.style.display=hasDown?'block':'none';al.textContent=hasDown?'⚠️ Инцидент: требуется внимание':'✅ Все сервисы работают';al.style.color=hasDown?'#e17055':'#00b894'});});})();</script>""",
        "widget_css": "",
        "widget_js": ""
    },
    {
        "slug": "user-onboarding",
        "title": "Онбординг пользователей",
        "desc": "White-label решение для онбординга: KYC, верификация, скоринг, интеграция с госуслугами и БКИ.",
        "meta_desc": "Демо системы онбординга: KYC, верификация документов, биометрия, интеграция с Госуслугами. Соответствие 115-ФЗ и 161-ФЗ.",
        "code": """// Начало онбординга
const session = await onboarding.createSession({
  userId: 'user_789',
  steps: ['passport', 'selfie', 'phone', 'address']
});

// Верификация паспорта
const passport = await onboarding.verifyPassport({
  sessionId: session.id,
  series: '4010',
  number: '123456',
  issuedBy: 'УФМС...'
});

// Биометрическая верификация
const biometric = await onboarding.verifyBiometric({
  sessionId: session.id,
  selfie: fileBuffer,
  passportPhoto: fileBuffer
});""",
        "features": ["KYC и AML-проверки", "Верификация документов (AI)", "Биометрия (liveness detection)", "Интеграция с Госуслугами", "Скоринг и фрод-мониторинг", "Соответствие 115-ФЗ, 161-ФЗ"],
        "tags": ["Python", "React", "PostgreSQL", "ML/AI", "115-ФЗ"],
        "gradient": "#a29bfe,#6c5ce7",
        "widget_html": """<div class="dw">
  <h3 class="dw-t"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="var(--clr-heading)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-3px;margin-right:6px"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><polyline points="17 11 19 13 23 9"/></svg>Онбординг пользователя</h3>
  <div style="display:flex;gap:6px;margin-bottom:18px;background:var(--clr-surface);border:1px solid var(--clr-border);border-radius:10px;padding:4px;font-size:12px;font-weight:500" id="ub-lvl">
    <div class="ub-lvl s" data-l="0" tabindex="0" role="button">Простой</div>
    <div class="ub-lvl" data-l="1" tabindex="0" role="button">Средний</div>
    <div class="ub-lvl" data-l="2" tabindex="0" role="button">Сложный</div>
    <div class="ub-lvl" data-l="3" tabindex="0" role="button">Мега + Госуслуги</div>
  </div>
  <div id="ub-progress" style="display:flex;align-items:center;gap:6px;margin-bottom:18px"></div>
  <div id="ub-c" style="padding:18px;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:12px;min-height:110px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;transition:all .3s;position:relative;overflow:hidden">
    <div id="ub-content"></div>
  </div>
  <button class="dw-btn" id="ub-btn" style="margin-top:12px;width:100%">Далее</button>
  <button id="ub-reset" style="margin-top:8px;width:100%;padding:8px;background:none;border:1px solid var(--clr-border);border-radius:10px;color:var(--clr-muted);font-size:12px;cursor:pointer;transition:all .2s">⟳ Сбросить</button>
</div>
<style>.dw{margin:12px 0;background:var(--clr-surface);border:1px solid var(--clr-border);border-radius:16px;padding:24px}.dw-t{font-size:16px;font-weight:600;margin:0 0 16px;color:var(--clr-heading)}.dw-btn{padding:12px;background:var(--clr-accent);border:none;border-radius:10px;color:#fff;font-size:15px;font-weight:600;cursor:pointer;transition:opacity .2s;width:100%}.dw-btn:hover{opacity:.85}.dw-btn:disabled{opacity:.35;cursor:default}.ub-lvl{flex:1;text-align:center;padding:8px 4px;border-radius:8px;cursor:pointer;color:var(--clr-muted);transition:all .2s;font-size:11px;user-select:none}.ub-lvl:hover{color:var(--clr-text)}.ub-lvl.s{background:var(--clr-accent);color:#fff;font-weight:600}#ub-reset:hover{border-color:var(--clr-accent);color:var(--clr-accent)}.ub-progress{display:flex;align-items:center;gap:6px;margin-bottom:18px}.ub-s{display:flex;flex-direction:column;align-items:center;gap:3px;flex:1;cursor:pointer;min-width:0}.ub-s:hover .ub-sn{border-color:var(--clr-accent)}.ub-sn{width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;background:var(--clr-bg);border:2px solid var(--clr-border);color:var(--clr-muted);transition:all .3s;flex-shrink:0}.ub-s.s .ub-sn{background:var(--clr-accent);border-color:var(--clr-accent);color:#fff}.ub-s.d .ub-sn{background:var(--clr-accent);border-color:var(--clr-accent);color:#fff;opacity:.5}.ub-sl{font-size:9px;color:var(--clr-muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}.ub-s.s .ub-sl{color:var(--clr-accent);font-weight:600}.ub-line{height:2px;flex:1;background:var(--clr-border);margin-bottom:18px;min-width:4px}.dw-i{background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:10px;color:var(--clr-text);box-sizing:border-box;width:100%;padding:10px 14px;font-size:13px}.dw-i:focus{outline:none;border-color:var(--clr-accent)}.ub-z{display:flex;flex-direction:column;align-items:center;gap:8px;padding:22px 14px;border:2px dashed var(--clr-border);border-radius:12px;cursor:pointer;transition:all .2s;text-align:center;width:100%;max-width:260px;box-sizing:border-box}.ub-z:hover{border-color:var(--clr-accent);background:rgba(108,92,231,.04)}.ub-z span{font-size:12px;color:var(--clr-muted)}.ub-cam{padding:10px 22px;background:var(--clr-accent);border:none;border-radius:10px;color:#fff;font-size:13px;font-weight:600;cursor:pointer;transition:opacity .2s}.ub-cam:hover{opacity:.85}.ub-cam:disabled{opacity:.35;cursor:default}.ub-gos{display:flex;flex-direction:column;align-items:center;gap:12px;width:100%;max-width:260px}.ub-gos-btn{display:flex;align-items:center;gap:10px;padding:12px 24px;background:#00247d;border:none;border-radius:10px;color:#fff;font-size:14px;font-weight:600;cursor:pointer;transition:opacity .2s;width:100%;justify-content:center}.ub-gos-btn:hover{opacity:.9}.ub-gos-btn:disabled{opacity:.5;cursor:default}.ub-spin{width:18px;height:18px;border:2px solid rgba(255,255,255,.3);border-top-color:#fff;border-radius:50%;animation:ubSpin .6s linear infinite;display:inline-block}@keyframes ubSpin{to{transform:rotate(360deg)}}.ub-auto{display:flex;flex-direction:column;gap:6px;width:100%;max-width:260px}.ub-auto .dw-i{opacity:.8;background:var(--clr-surface)}.ub-auto .dw-i:disabled{opacity:.6}.ub-tag{display:inline-block;padding:2px 8px;border-radius:4px;font-size:10px;font-weight:600;margin-left:6px}.ub-tag-esia{background:#00247d;color:#fff}.ub-tag-ok{background:#00b894;color:#fff}.ub-approved{display:flex;align-items:center;gap:8px;padding:8px 12px;background:var(--clr-surface);border:1px solid #00b894;border-radius:10px;color:#00b894;font-size:12px;width:100%;max-width:260px;box-sizing:border-box}@media(min-width:768px){.dw{max-width:520px;margin-left:auto;margin-right:auto}}</style>
<script>(function(){var l=0,s=1,btn=document.getElementById('ub-btn'),prog=document.getElementById('ub-progress'),cnt=document.getElementById('ub-content');var levels=[{steps:['Данные','Готово'],labels:['Введите имя и телефон',''],cont:['form','done'],form:true,docs:false,bio:false,esia:false,auto:false},{steps:['Данные','Паспорт','Готово'],labels:['Введите имя и телефон','Укажите серию и номер',''],cont:['form','passport','done'],form:true,docs:true,bio:false,esia:false,auto:false},{steps:['Данные','Паспорт (AI)','Биометрия','Готово'],labels:['Введите имя и телефон','Загрузите скан','Подтвердите селфи',''],cont:['form','passport','bio','done'],form:true,docs:true,bio:true,esia:false,auto:false},{steps:['Госуслуги','Данные (авто)','Паспорт','Биометрия','Готово'],labels:['Войдите через ЕСИА','Данные из ЕСИА','Загрузите скан','Подтвердите селфи',''],cont:['esia','form','passport','bio','done'],form:true,docs:true,bio:true,esia:true,auto:true}];var state={esiaDone:false,docLoaded:false,bioDone:false};function t(txt){return document.createTextNode(txt)}function el(tag,attr,children){var e=document.createElement(tag);if(attr)Object.keys(attr).forEach(function(k){e.setAttribute(k,attr[k])});if(children)children.forEach(function(c){if(typeof c==='string')e.appendChild(t(c));else e.appendChild(c)});return e}function html(str){var d=document.createElement('div');d.innerHTML=str;return d.firstElementChild}function buildProgress(){prog.innerHTML='';var lv=levels[l];lv.steps.forEach(function(label,i){var step=el('div',{class:'ub-s'+(i+1===s?' s':i+1<s?' d':'')});var num=el('div',{class:'ub-sn'},[t(''+(i+1))]);var lb=el('div',{class:'ub-sl'},[t(label)]);step.appendChild(num);step.appendChild(lb);(function(idx){step.addEventListener('click',function(){go(idx+1)});step.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();go(idx+1)}})})(i);prog.appendChild(step);if(i<lv.steps.length-1){var line=el('div',{class:'ub-line'});prog.appendChild(line)}})}function render(){var lv=levels[l];buildProgress();cnt.innerHTML='';var stepIdx=s-1;var stepType=lv.cont[stepIdx];if(stepType==='done'){cnt.appendChild(html('<div style=\"display:flex;flex-direction:column;align-items:center;gap:6px\"><svg viewBox=\"0 0 24 24\" width=\"44\" height=\"44\" fill=\"none\" stroke=\"#00b894\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M22 11.08V12a10 10 0 1 1-5.93-9.14\"/><polyline points=\"22 4 12 14.01 9 11.01\"/></svg><div style=\"font-size:16px;font-weight:600;color:#00b894\">Регистрация завершена!</div><div style=\"font-size:12px;color:var(--clr-muted);text-align:center\">'+(l===3?'Лицевой счёт открыт, карта выпущена<br>Уведомление отправлено в Госуслуги':l===2?'Лицевой счёт открыт, карта заказана':'Аккаунт создан')+'</div></div>'));btn.style.display='none';return}btn.style.display='block';if(stepType==='form'){cnt.appendChild(html('<div style=\"display:flex;flex-direction:column;gap:8px;width:100%;max-width:260px;animation:ubFade .25s\">'+(l===3?'<div style=\"font-size:11px;color:var(--clr-muted);margin-bottom:2px\">Данные получены из ЕСИА, проверьте:</div>':'<div style=\"font-size:13px;color:var(--clr-text);font-weight:500;text-align:center;margin-bottom:2px\">'+lv.labels[stepIdx]+'</div>')+'<input class=\"dw-i\" placeholder=\"Имя\" value=\"'+(l===3?'Иван Петров':'Иван')+'\"'+(l===3?' disabled':'')+'><input class=\"dw-i\" placeholder=\"Телефон\" value=\"'+(l===3?'+7 (916) 555-12-34':'+7 (999) 123-45-67')+'\"'+(l===3?' disabled':'')+'><input class=\"dw-i\" placeholder=\"Email\" value=\"'+(l===3?'ivan@example.ru':'')+'\"'+(l===3?' disabled':'')+'>'+(l===3?'<div style=\"display:flex;justify-content:space-between;font-size:11px;color:var(--clr-muted);padding:6px 0\"><span>Дата рождения: 15.03.1985 <span class=\"ub-tag ub-tag-ok\">совпадает</span></span></div>':'')+'</div>'));btn.textContent='Далее';btn.disabled=false}else if(stepType==='passport'){cnt.appendChild(html('<div style=\"display:flex;flex-direction:column;align-items:center;gap:8px;width:100%;animation:ubFade .25s\">'+(l===2||l===3?'<div style=\"font-size:12px;color:var(--clr-muted);text-align:center\">'+(l===3?'Загрузите скан паспорта<br>AI-верификация выполнится автоматически':'Загрузите скан паспорта для AI-верификации')+'</div>':'<div style=\"font-size:12px;color:var(--clr-muted);text-align:center\">Укажите серию и номер паспорта</div>')+(state.docLoaded?'<div class=\"ub-approved\"><svg viewBox=\"0 0 24 24\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"#00b894\" stroke-width=\"2.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><polyline points=\"20 6 9 17 4 12\"/></svg>'+(l>=2?'Паспорт проверен AI (достоверность 98.7%)':'Серия 4010, номер 123456 подтверждён')+'</div>':'<div class=\"ub-z\" id=\"ub-upload-btn\" tabindex=\"0\"><svg viewBox=\"0 0 24 24\" width=\"22\" height=\"22\" fill=\"none\" stroke=\"var(--clr-muted)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4\"/><polyline points=\"17 8 12 3 7 8\"/><line x1=\"12\" y1=\"3\" x2=\"12\" y2=\"15\"/></svg><span>Нажмите для загрузки</span></div>')+'</div>'));btn.textContent=s===lv.steps.length?'Завершить':'Далее';btn.disabled=!state.docLoaded}else if(stepType==='bio'){cnt.appendChild(html('<div style=\"display:flex;flex-direction:column;align-items:center;gap:10px;animation:ubFade .25s\"><div style=\"width:72px;height:72px;border-radius:50%;background:var(--clr-surface);border:2px solid '+(state.bioDone?'#00b894':'var(--clr-border)')+';display:flex;align-items:center;justify-content:center;overflow:hidden\">'+(state.bioDone?'<svg viewBox=\"0 0 24 24\" width=\"32\" height=\"32\" fill=\"none\" stroke=\"#00b894\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2\"/><circle cx=\"12\" cy=\"7\" r=\"4\"/></svg>':'<svg viewBox=\"0 0 24 24\" width=\"32\" height=\"32\" fill=\"none\" stroke=\"var(--clr-muted)\" stroke-width=\"1.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2\"/><circle cx=\"12\" cy=\"7\" r=\"4\"/></svg>')+'</div>'+(state.bioDone?'<div style=\"font-size:12px;color:#00b894;font-weight:600\">Liveness подтверждён</div>':'<button class=\"ub-cam\" id=\"ub-bio-btn\"><svg viewBox=\"0 0 24 24\" width=\"14\" height=\"14\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" style=\"vertical-align:-2px;margin-right:4px\"><path d=\"M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z\"/><circle cx=\"12\" cy=\"13\" r=\"4\"/></svg>Сделать селфи</button>')+'</div>'));btn.textContent='Завершить';btn.disabled=!state.bioDone}else if(stepType==='esia'){cnt.appendChild(html('<div class=\"ub-gos\" style=\"animation:ubFade .25s\">'+(state.esiaDone?'<div class=\"ub-approved\"><svg viewBox=\"0 0 24 24\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"#00b894\" stroke-width=\"2.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><polyline points=\"20 6 9 17 4 12\"/></svg>Подтверждено через ЕСИА</div><div style=\"font-size:11px;color:var(--clr-muted);text-align:center\">Персональные данные получены из Госуслуг</div>':'<div style=\"font-size:13px;color:var(--clr-text);text-align:center;font-weight:500;line-height:1.5\">Подключитесь к Госуслугам<br>для автоматического заполнения</div><button class=\"ub-gos-btn\" id=\"ub-esia-btn\"><svg viewBox=\"0 0 24 24\" width=\"18\" height=\"18\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><rect x=\"3\" y=\"11\" width=\"18\" height=\"11\" rx=\"2\" ry=\"2\"/><path d=\"M7 11V7a5 5 0 0 1 10 0v4\"/></svg>Войти через Госуслуги</button><div style=\"font-size:10px;color:var(--clr-muted);text-align:center\">ЕСИА · 115-ФЗ · Усиленная аутентификация</div>')+'</div>'));btn.textContent='Далее';btn.disabled=!state.esiaDone}requestAnimationFrame(function(){var up=document.getElementById('ub-upload-btn');if(up){up.addEventListener('click',function(){state.docLoaded=true;render()});up.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();state.docLoaded=true;render()}})}var bioBtn=document.getElementById('ub-bio-btn');if(bioBtn){bioBtn.addEventListener('click',function(){state.bioDone=true;render()})}var esiaBtn=document.getElementById('ub-esia-btn');if(esiaBtn){esiaBtn.addEventListener('click',function(){var self=this;self.disabled=true;self.innerHTML='<span class=\"ub-spin\"></span> Подключение...';setTimeout(function(){state.esiaDone=true;render()},1200)})}})}function go(n){var lv=levels[l];if(n<1||n>lv.steps.length||n===s)return;if(n>s){if(s===2&&lv.cont[s-1]==='esia'&&!state.esiaDone)return;if(s===2&&lv.cont[s-1]==='passport'&&!state.docLoaded)return;if(s===3&&lv.cont[s-1]==='passport'&&!state.docLoaded)return;if(s===3&&lv.cont[s-1]==='bio'&&!state.bioDone)return;if(s===4&&lv.cont[s-1]==='bio'&&!state.bioDone)return}s=n;render()}function setLevel(n){if(n===l)return;l=n;s=1;state={esiaDone:false,docLoaded:false,bioDone:false};document.querySelectorAll('.ub-lvl').forEach(function(el,i){el.classList.toggle('s',i===n)});render()}document.querySelectorAll('.ub-lvl').forEach(function(el,i){el.addEventListener('click',function(){setLevel(i)});el.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();setLevel(i)}})});btn.addEventListener('click',function(){var lv=levels[l];if(s<lv.steps.length){go(s+1)}else{render()}});document.getElementById('ub-reset').addEventListener('click',function(){l=0;s=1;state={esiaDone:false,docLoaded:false,bioDone:false};document.querySelectorAll('.ub-lvl').forEach(function(el,i){el.classList.toggle('s',i===0)});render()});render()})();</script>""",
        "widget_css": "",
        "widget_js": ""
    },
    {
        "slug": "telegram-storefront",
        "title": "Витрина в Telegram",
        "desc": "Telegram Mini App — витрина товаров/услуг с оплатой прямо в мессенджере. Каталог, корзина, платежи, уведомления.",
        "meta_desc": "Демо Telegram Mini App: витрина товаров с оплатой внутри Telegram, каталог, корзина, уведомления. Примеры кода создания Mini App.",
        "code": """// Инициализация Telegram Mini App
const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

// Получение данных пользователя
const user = tg.initDataUnsafe.user;
// { id: 123456, first_name: 'Иван', ... }

// Загрузка каталога товаров
const products = await store.getProducts({
  category: 'electronics',
  page: 1,
  limit: 20
});

// Оформление заказа
const order = await store.createOrder({
  userId: user.id,
  items: cart,
  delivery: 'pickup'
});

// Закрытие Mini App
tg.close();""",
        "features": ["Telegram Mini App (TWA)", "Каталог с поиском и фильтрацией", "Оплата через Telegram Stars", "Push-уведомления через бота", "История заказов", "Аналитика продаж"],
        "tags": ["React", "Node.js", "Telegram API", "PostgreSQL"],
        "gradient": "#55efc4,#00b894",
        "widget_html": """<div class="dw">
  <h3 class="dw-t"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="var(--clr-heading)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-3px;margin-right:6px"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><line x1="21.17" y1="8" x2="12" y2="8"/><line x1="3.95" y1="6.06" x2="8.54" y2="14"/><line x1="10.88" y1="21.94" x2="15.46" y2="14"/></svg>Telegram Shop</h3>
  <div style="border:2px solid var(--clr-border);border-radius:20px;padding:0;max-width:340px;margin:0 auto;position:relative;overflow:hidden;background:var(--clr-bg)">
    <div style="height:22px;width:130px;background:var(--clr-bg);border-radius:0 0 10px 10px;margin:0 auto;border:1px solid var(--clr-border);border-top:none;position:relative;z-index:2"></div>
    <div id="ts-shop" style="padding:10px 12px 12px">
      <div style="display:flex;flex-direction:column;gap:8px;margin-bottom:10px">
        <div class="ts-c"><div style="background:linear-gradient(135deg,#6c5ce7,#a29bfe);width:36px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12" y2="18"/></svg></div><div style="flex:1;min-width:0"><div style="font-size:13px;font-weight:600;color:var(--clr-text)">Phone X</div><div style="font-size:13px;font-weight:700;color:var(--clr-heading);margin-top:1px">79 990 ₽</div></div><button class="ts-b" data-i="0" data-p="79990">Купить</button></div>
        <div class="ts-c"><div style="background:linear-gradient(135deg,#00b894,#55efc4);width:36px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg></div><div style="flex:1;min-width:0"><div style="font-size:13px;font-weight:600;color:var(--clr-text)">Buds Pro</div><div style="font-size:13px;font-weight:700;color:var(--clr-heading);margin-top:1px">14 990 ₽</div></div><button class="ts-b" data-i="1" data-p="14990">Купить</button></div>
        <div class="ts-c"><div style="background:linear-gradient(135deg,#fdcb6e,#f39c12);width:36px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="7"/><polyline points="12 9 12 12 13.5 13.5"/><path d="M16.51 17.35l-.35 3.83a2 2 0 0 1-2 1.82H9.83a2 2 0 0 1-2-1.82l-.35-3.83"/></svg></div><div style="flex:1;min-width:0"><div style="font-size:13px;font-weight:600;color:var(--clr-text)">Watch</div><div style="font-size:13px;font-weight:700;color:var(--clr-heading);margin-top:1px">49 990 ₽</div></div><button class="ts-b" data-i="2" data-p="49990">Купить</button></div>
      </div>
      <div id="ts-cart" style="display:none;flex-direction:column;gap:4px;padding:8px 0;border-top:1px solid var(--clr-border);margin-top:2px"></div>
      <div style="display:flex;justify-content:space-between;align-items:center;padding:6px 0 0;border-top:1px solid var(--clr-border)">
        <span style="font-size:12px;color:var(--clr-muted)">Товаров: <strong id="ts-cnt" style="color:var(--clr-heading)">0</strong></span>
        <span style="font-size:15px;font-weight:700;color:var(--clr-heading)" id="ts-tot">0 ₽</span>
        <button class="ts-pay" id="ts-pay">Оплатить</button>
      </div>
      <button id="ts-reset" style="margin-top:8px;width:100%;padding:6px;background:none;border:1px solid var(--clr-border);border-radius:8px;color:var(--clr-muted);font-size:11px;cursor:pointer;transition:all .2s">⟳ Сбросить корзину</button>
    </div>
    <div id="ts-chat" style="display:none;flex-direction:column;height:340px;background:var(--clr-bg)">
      <div style="display:flex;align-items:center;gap:8px;padding:8px 12px;background:var(--clr-accent);color:#fff">
        <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><line x1="21.17" y1="8" x2="12" y2="8"/><line x1="3.95" y1="6.06" x2="8.54" y2="14"/><line x1="10.88" y1="21.94" x2="15.46" y2="14"/></svg>
        <div><div style="font-size:13px;font-weight:600">AXIIOM Shop Bot</div><div style="font-size:10px;opacity:.8">онлайн</div></div>
        <div style="margin-left:auto;display:flex;gap:4px">
          <button class="ts-chat-btn" id="ts-back" style="font-size:11px">⟳ Магазин</button>
        </div>
      </div>
      <div id="ts-msgs" style="flex:1;overflow-y:auto;padding:8px 12px;display:flex;flex-direction:column;gap:6px;background:var(--clr-surface)"></div>
      <div style="display:flex;gap:6px;padding:8px 10px;border-top:1px solid var(--clr-border);background:var(--clr-bg)">
        <input id="ts-input" style="flex:1;padding:8px 12px;border:1px solid var(--clr-border);border-radius:20px;background:var(--clr-surface);color:var(--clr-text);font-size:12px;outline:none" placeholder="Написать..." maxlength="50">
        <button id="ts-send" style="width:34px;height:34px;border-radius:50%;background:var(--clr-accent);border:none;color:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer;flex-shrink:0"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg></button>
      </div>
    </div>
  </div>
</div>
<style>.dw{margin:12px 0;background:var(--clr-surface);border:1px solid var(--clr-border);border-radius:16px;padding:24px}.dw-t{font-size:16px;font-weight:600;margin:0 0 16px;color:var(--clr-heading)}.ts-c{display:flex;align-items:center;gap:10px;padding:8px 10px;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:10px}.ts-b{padding:6px 14px;background:var(--clr-accent);border:none;border-radius:8px;color:#fff;font-size:11px;font-weight:600;cursor:pointer;transition:all .2s;white-space:nowrap}.ts-b:hover{opacity:.85}.ts-b.added{background:var(--clr-muted)}.ts-pay{padding:8px 16px;background:var(--clr-accent);border:none;border-radius:10px;color:#fff;font-size:12px;font-weight:600;cursor:pointer;transition:all .2s;white-space:nowrap}.ts-pay:hover{opacity:.85}.ts-pay:disabled{opacity:.35;cursor:default}.ts-msg{max-width:80%;padding:8px 12px;border-radius:12px;font-size:12px;line-height:1.4;animation:tsIn .2s ease}.ts-msg.bot{align-self:flex-start;background:var(--clr-bg);border:1px solid var(--clr-border);border-bottom-left-radius:4px;color:var(--clr-text)}.ts-msg.user{align-self:flex-end;background:var(--clr-accent);color:#fff;border-bottom-right-radius:4px}.ts-chat-btn{background:none;border:1px solid rgba(255,255,255,.3);border-radius:6px;color:#fff;padding:4px 8px;cursor:pointer;font-size:11px;transition:opacity .2s}.ts-chat-btn:hover{opacity:.8}#ts-reset:hover{border-color:var(--clr-accent);color:var(--clr-accent)}@keyframes tsIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}@media(min-width:768px){.dw{max-width:420px;margin-left:auto;margin-right:auto}}</style>
<script>(function(){var cart={},total=0,count=0,orderId='MK-'+Math.floor(100000+Math.random()*900000);var names=['Phone X','Buds Pro','Watch'],prices=[79990,14990,49990];function up(){var cEl=document.getElementById('ts-cnt'),tEl=document.getElementById('ts-tot'),pEl=document.getElementById('ts-pay');cEl.textContent=count;tEl.textContent=total.toLocaleString('ru')+' ₽';pEl.disabled=count===0;document.querySelectorAll('.ts-b').forEach(function(b){var i=parseInt(b.dataset.i);b.classList.toggle('added',cart[i]);b.textContent=cart[i]?'✓ '+cart[i]:'Купить'});var cartEl=document.getElementById('ts-cart');cartEl.innerHTML='';if(count>0){cartEl.style.display='flex';Object.keys(cart).forEach(function(i){var item=document.createElement('div');item.style.cssText='display:flex;align-items:center;gap:6px;padding:4px 6px;background:var(--clr-surface);border-radius:6px;font-size:11px';item.innerHTML='<span style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1;color:var(--clr-text)">'+names[i]+'</span><span style="color:var(--clr-muted)">×'+cart[i]+'</span><span style="font-weight:600;color:var(--clr-heading)">'+(prices[i]*cart[i]).toLocaleString('ru')+' ₽</span><button class="ts-rm" data-i="'+i+'" style="background:none;border:none;color:var(--clr-muted);cursor:pointer;font-size:14px;padding:0 2px;line-height:1">×</button>';cartEl.appendChild(item)});document.querySelectorAll('.ts-rm').forEach(function(b){b.addEventListener('click',function(e){e.stopPropagation();var i=this.dataset.i;total-=prices[i]*cart[i];count-=cart[i];delete cart[i];up()})})}else{cartEl.style.display='none'}}document.querySelectorAll('.ts-b').forEach(function(b){b.addEventListener('click',function(){var i=parseInt(this.dataset.i),p=parseInt(this.dataset.p);if(!cart[i]){cart[i]=1;total+=p;count++}else{cart[i]++;total+=p;count++}up()})});document.getElementById('ts-pay').addEventListener('click',function(){var pay=this;pay.disabled=true;pay.textContent='⏳ Оплата...';setTimeout(function(){pay.textContent='✅ Оплачено';var shop=document.getElementById('ts-shop'),chat=document.getElementById('ts-chat'),msgs=document.getElementById('ts-msgs');shop.style.display='none';chat.style.display='flex';var items=Object.keys(cart).map(function(i){return names[i]+' x'+cart[i]}).join(', ');var t=total.toLocaleString('ru');var ms=[{t:'bot',m:'✅ Заказ <b>№'+orderId+'</b> оформлен'},{t:'bot',m:'🛒 <b>'+items+'</b>'},{t:'bot',m:'💳 Оплачено <b>'+t+' ₽</b> через Telegram Stars'},{t:'bot',m:'📦 Трек-номер: <b>TG-'+orderId+'</b>'},{t:'bot',m:'Спасибо за покупку! 🎉\\n\\n<i>Доступные команды:</i>\\n• <b>статус</b> — проверить доставку\\n• <b>отмена</b> — отменить заказ\\n• <b>помощь</b> — поддержка'}];function addMsg(i){if(i>=ms.length)return;var d=document.createElement('div');d.className='ts-msg '+(ms[i].t==='bot'?'bot':'user');d.innerHTML=ms[i].m;msgs.appendChild(d);msgs.scrollTop=msgs.scrollHeight;setTimeout(function(){addMsg(i+1)},i%2===0?500:300)}addMsg(0)},1500)});document.getElementById('ts-send').addEventListener('click',function(){var inp=document.getElementById('ts-input'),txt=inp.value.trim();if(!txt)return;inp.value='';var msgs=document.getElementById('ts-msgs');var ud=document.createElement('div');ud.className='ts-msg user';ud.textContent=txt;msgs.appendChild(ud);msgs.scrollTop=msgs.scrollHeight;setTimeout(function(){var bd=document.createElement('div');bd.className='ts-msg bot';var low=txt.toLowerCase();if(low.indexOf('статус')>=0||low.indexOf('трек')>=0||low.indexOf('где')>=0){bd.innerHTML='📦 Заказ <b>'+orderId+'</b> в пути.<br>📍 Текущий статус: <b>Сортировка</b><br>🚚 Ожидаемая дата: <b>20 июня</b>'}else if(low.indexOf('отмен')>=0||low.indexOf('верн')>=0){bd.innerHTML='❌ Отмена невозможна — заказ уже передан в доставку.<br>Свяжитесь с поддержкой: @axiiom_support'}else if(low.indexOf('помощ')>=0||low.indexOf('support')>=0||low.indexOf('поддерж')>=0){bd.innerHTML='👋 Напишите @axiiom_support<br>Время ответа: ~5 минут'}else{bd.innerHTML='❓ Команда не распознана.<br><i>Доступно: статус, отмена, помощь</i>'}msgs.appendChild(bd);msgs.scrollTop=msgs.scrollHeight},600)});document.getElementById('ts-input').addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();document.getElementById('ts-send').click()}});document.getElementById('ts-back').addEventListener('click',function(){document.getElementById('ts-chat').style.display='none';document.getElementById('ts-shop').style.display='block';document.getElementById('ts-pay').textContent='Оплатить';document.getElementById('ts-pay').disabled=false;document.getElementById('ts-msgs').innerHTML=''});document.getElementById('ts-reset').addEventListener('click',function(){cart={};total=0;count=0;document.getElementById('ts-msgs').innerHTML='';document.getElementById('ts-chat').style.display='none';document.getElementById('ts-shop').style.display='block';document.getElementById('ts-pay').textContent='Оплатить';document.getElementById('ts-pay').disabled=false;up()});up()})();</script>""",
        "widget_css": "",
        "widget_js": ""
    },
    {
        "slug": "loyalty-system",
        "title": "Система лояльности",
        "desc": "Гибкая система лояльности с правилами, сегментацией, A/B-тестами и аналитикой в реальном времени.",
        "meta_desc": "Демо конструктора систем лояльности: правила, сегментация, A/B-тесты, аналитика. Гибкая настройка под любой бизнес.",
        "code": """// Создание правила лояльности
const rule = await loyalty.createRule({
  name: '3+1 бесплатно',
  trigger: 'purchase',
  condition: {
    category: 'coffee',
    minItems: 3
  },
  reward: {
    type: 'free_product',
    productId: 'coffee_any'
  }
});

// Сегментация пользователей
const segment = await loyalty.createSegment({
  name: 'VIP осень 2024',
  filters: [
    { spent: { gt: 50000 } },
    { visits: { gt: 10 } }
  ]
});

// Запуск A/B-теста
const ab = await loyalty.startABTest({
  name: 'Кешбэк 5% vs 10%',
  segments: ['A', 'B'],
  duration: 14
});""",
        "features": ["Конструктор правил и триггеров", "Сегментация аудитории", "A/B-тестирование механик", "Real-time аналитика", "Персонализированные офферы", "API для внешних систем"],
        "tags": ["Node.js", "React", "PostgreSQL", "Redis", "Kafka"],
        "gradient": "#e84393,#fd79a8",
        "widget_html": """<div class="dw">
  <h3 class="dw-t">⚙️ Система лояльности</h3>
  <p style="font-size:13px;color:var(--clr-muted);margin:-8px 0 14px">Rules Engine — управляйте правилами, сегментами и аналитикой</p>
  <div style="display:flex;gap:8px;margin-bottom:14px">
    <button class="ls-tab ls-tab-a" id="ls-t-r" style="flex:1">📋 Правила</button>
    <button class="ls-tab" id="ls-t-s" style="flex:1">👥 Сегменты</button>
    <button class="ls-tab" id="ls-t-a" style="flex:1">📊 Аналитика</button>
  </div>
  <div id="ls-rules">
    <div class="ls-r" data-on="1"><div style="display:flex;align-items:center;gap:8px;flex:1"><span style="font-size:18px">🎁</span><div><div style="font-size:13px;font-weight:600;color:var(--clr-heading)">3+1 бесплатно</div><div style="font-size:11px;color:var(--clr-muted)">Триггер: покупка кофе | Награда: бесплатный напиток</div></div></div><div class="ls-tog" style="background:var(--clr-accent)"><div class="ls-tog-k" style="transform:translateX(14px)"></div></div></div>
    <div class="ls-r" data-on="1"><div style="display:flex;align-items:center;gap:8px;flex:1"><span style="font-size:18px">💰</span><div><div style="font-size:13px;font-weight:600;color:var(--clr-heading)">Кешбэк 5%</div><div style="font-size:11px;color:var(--clr-muted)">Триггер: любой платёж | Награда: 5% баллами</div></div></div><div class="ls-tog" style="background:var(--clr-accent)"><div class="ls-tog-k" style="transform:translateX(14px)"></div></div></div>
    <div class="ls-r" data-on="0"><div style="display:flex;align-items:center;gap:8px;flex:1"><span style="font-size:18px">🔥</span><div><div style="font-size:13px;font-weight:600;color:var(--clr-heading)">Двойные баллы на выходные</div><div style="font-size:11px;color:var(--clr-muted)">Триггер: покупка сб-вс | Награда: x2 баллов</div></div></div><div class="ls-tog" style="background:var(--clr-border)"><div class="ls-tog-k"></div></div></div>
  </div>
  <div id="ls-segments" style="display:none">
    <div style="display:flex;flex-direction:column;gap:6px">
      <div class="ls-s"><div style="display:flex;align-items:center;gap:8px;flex:1"><span style="font-size:16px">👑</span><div><div style="font-size:13px;font-weight:600;color:var(--clr-heading)">VIP</div><div style="font-size:11px;color:var(--clr-muted)">Потратили >50 000 ₽</div></div></div><span style="font-size:15px;font-weight:700;color:var(--clr-heading)">2 450</span></div>
      <div class="ls-s"><div style="display:flex;align-items:center;gap:8px;flex:1"><span style="font-size:16px">🌟</span><div><div style="font-size:13px;font-weight:600;color:var(--clr-heading)">Активные</div><div style="font-size:11px;color:var(--clr-muted)">Покупка за последние 30 дней</div></div></div><span style="font-size:15px;font-weight:700;color:var(--clr-heading)">8 310</span></div>
      <div class="ls-s"><div style="display:flex;align-items:center;gap:8px;flex:1"><span style="font-size:16px">🌱</span><div><div style="font-size:13px;font-weight:600;color:var(--clr-heading)">Новые</div><div style="font-size:11px;color:var(--clr-muted)">Регистрация до 14 дней</div></div></div><span style="font-size:15px;font-weight:700;color:var(--clr-heading)">1 205</span></div>
      <div class="ls-s"><div style="display:flex;align-items:center;gap:8px;flex:1"><span style="font-size:16px">⚠️</span><div><div style="font-size:13px;font-weight:600;color:var(--clr-heading)">Отток</div><div style="font-size:11px;color:var(--clr-muted)">Не было покупок >60 дней</div></div></div><span style="font-size:15px;font-weight:700;color:var(--clr-heading)">643</span></div>
    </div>
  </div>
  <div id="ls-analytics" style="display:none">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
      <div class="ls-k"><div style="font-size:11px;color:var(--clr-muted)">Участников</div><div style="font-size:20px;font-weight:700;color:var(--clr-heading)">12 450</div><div style="font-size:11px;color:#00b894">+12% за месяц</div></div>
      <div class="ls-k"><div style="font-size:11px;color:var(--clr-muted)">Средний чек</div><div style="font-size:20px;font-weight:700;color:var(--clr-heading)">+23%</div><div style="font-size:11px;color:#00b894">участники vs неучастники</div></div>
      <div class="ls-k"><div style="font-size:11px;color:var(--clr-muted)">Удержание</div><div style="font-size:20px;font-weight:700;color:var(--clr-heading)">78%</div><div style="font-size:11px;color:#00b894">+5% за квартал</div></div>
      <div class="ls-k"><div style="font-size:11px;color:var(--clr-muted)">Акций запущено</div><div style="font-size:20px;font-weight:700;color:var(--clr-heading)">6</div><div style="font-size:11px;color:var(--clr-muted)">в этом месяце</div></div>
    </div>
  </div>
</div>
<style>.dw{margin:12px 0;background:var(--clr-surface);border:1px solid var(--clr-border);border-radius:16px;padding:24px}.dw-t{font-size:16px;font-weight:600;margin:0 0 16px;color:var(--clr-heading)}.ls-tab{padding:8px;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:8px;font-size:13px;font-weight:500;color:var(--clr-text);cursor:pointer;transition:all .2s}.ls-tab:hover{border-color:var(--clr-accent)}.ls-tab-a{background:var(--clr-accent);border-color:var(--clr-accent);color:#fff}.ls-r,.ls-s{display:flex;align-items:center;gap:8px;padding:10px 12px;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:8px;margin-bottom:6px}.ls-tog{width:32px;height:18px;border-radius:10px;padding:2px;cursor:pointer;transition:background .2s;flex-shrink:0}.ls-tog-k{width:14px;height:14px;background:#fff;border-radius:50%;transition:transform .2s}.ls-k{padding:12px;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:10px;text-align:center}@media(min-width:768px){.dw{max-width:520px;margin-left:auto;margin-right:auto}}</style>
<script>(function(){var tabs=[document.getElementById('ls-t-r'),document.getElementById('ls-t-s'),document.getElementById('ls-t-a')],panels=[document.getElementById('ls-rules'),document.getElementById('ls-segments'),document.getElementById('ls-analytics')];function show(i){tabs.forEach(function(t,j){t.classList.toggle('ls-tab-a',j===i)});panels.forEach(function(p,j){p.style.display=j===i?'block':'none'})}tabs[0].addEventListener('click',function(){show(0)});tabs[1].addEventListener('click',function(){show(1)});tabs[2].addEventListener('click',function(){show(2)});document.querySelectorAll('.ls-r').forEach(function(r){r.addEventListener('click',function(e){if(e.target.closest('.ls-tog')){var on=r.dataset.on==='1'?'0':'1';r.dataset.on=on;var tog=r.querySelector('.ls-tog');var k=r.querySelector('.ls-tog-k');if(on==='1'){tog.style.background='var(--clr-accent)';k.style.transform='translateX(14px)'}else{tog.style.background='var(--clr-border)';k.style.transform='translateX(0)'}}})})})();</script>""",
        "widget_css": "",
        "widget_js": ""
    },
    {
        "slug": "fintech-constructor",
        "title": "Финтех-конструктор",
        "desc": "Low-code конструктор финтех-продуктов: собирайте платёжные сценарии, rules-engine, workflow из готовых блоков.",
        "meta_desc": "Демо low-code конструктора финтех-продуктов: визуальный редактор сценариев, rules-engine, workflow. API-first архитектура.",
        "code": """// Создание платёжного сценария
const scenario = await constructor.createScenario({
  name: 'Пополнение+P2P-перевод',
  blocks: [
    { type: 'payment_method', params: { methods: ['card', 'sbp'] } },
    { type: 'commission', params: { percent: 0.5, min: 10 } },
    { type: 'split', params: { receivers: ['merchant', 'partner'] } },
    { type: 'notification', params: { channels: ['sms', 'push'] } }
  ]
});

// Деплой сценария
await constructor.deploy(scenario.id, 'production');

// Тестирование
const test = await constructor.testScenario(scenario.id, {
  amount: 1000,
  method: 'card'
});""",
        "features": ["Drag-and-drop редактор сценариев", "Rules-engine с версионированием", "API-first архитектура", "Песочница для тестирования", "Audit log всех изменений", "Готовые шаблоны"],
        "tags": ["React", "Node.js", "GraphQL", "Docker", "PostgreSQL"],
        "gradient": "#8B5CF6,#c4b5fd",
        "widget_html": """<div class="dw">
  <h3 class="dw-t">🧩 Финтех-конструктор</h3>
  <p style="font-size:13px;color:var(--clr-muted);margin:-8px 0 14px">Сценарий: «Пополнение + P2P перевод» — настройте блоки и запустите</p>
  <div style="display:flex;flex-direction:column;gap:6px;margin-bottom:14px" id="fc-blocks">
    <div class="fc-b" data-i="0"><div style="display:flex;align-items:center;gap:8px;flex:1"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="var(--clr-text)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/><line x1="5" y1="15" x2="9" y2="15"/></svg><div><div style="font-size:13px;font-weight:600;color:var(--clr-heading)">Приём платежа</div><div style="font-size:11px;color:var(--clr-muted)" id="fc-pm">Метод: Visa, MC</div></div></div><div style="display:flex;align-items:center;gap:4px"><span style="font-size:10px;color:var(--clr-muted);background:var(--clr-surface);padding:2px 6px;border-radius:4px">нажмите</span><span style="font-size:16px;cursor:pointer;opacity:.5" id="fc-tog0">↻</span></div></div>
    <div style="text-align:center;font-size:16px;color:var(--clr-border);line-height:1">↓</div>
    <div class="fc-b" data-i="1"><div style="display:flex;align-items:center;gap:8px;flex:1"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="var(--clr-text)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v12"/><path d="M8.5 9.5h4a2 2 0 0 1 0 4h-4"/></svg><div><div style="font-size:13px;font-weight:600;color:var(--clr-heading)">Комиссия</div><div style="font-size:11px;color:var(--clr-muted)" id="fc-cm">Тип: 0.5% + 10 ₽</div></div></div><span style="font-size:16px;cursor:pointer;opacity:.5" id="fc-tog1">↻</span></div>
    <div style="text-align:center;font-size:16px;color:var(--clr-border);line-height:1">↓</div>
    <div class="fc-b" data-i="2"><div style="display:flex;align-items:center;gap:8px;flex:1"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="var(--clr-text)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18"/><path d="M19 9l-7-6-7 6"/><path d="M5 15l7 6 7-6"/></svg><div><div style="font-size:13px;font-weight:600;color:var(--clr-heading)">Сплит</div><div style="font-size:11px;color:var(--clr-muted)" id="fc-sp">Магазин: 97% | Партнёр: 3%</div></div></div><span style="font-size:16px;cursor:pointer;opacity:.5" id="fc-tog2">↻</span></div>
    <div style="text-align:center;font-size:16px;color:var(--clr-border);line-height:1">↓</div>
    <div class="fc-b" data-i="3"><div style="display:flex;align-items:center;gap:8px;flex:1"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="var(--clr-text)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg><div><div style="font-size:13px;font-weight:600;color:var(--clr-heading)">Уведомление</div><div style="font-size:11px;color:var(--clr-muted)" id="fc-nt">Каналы: SMS, Push</div></div></div><span style="font-size:16px;cursor:pointer;opacity:.5" id="fc-tog3">↻</span></div>
  </div>
  <div style="display:flex;gap:6px;margin-bottom:14px">
    <div style="flex:1;position:relative">
      <input type="text" id="fc-amount" value="1 000" style="width:100%;padding:8px 30px 8px 12px;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:8px;color:var(--clr-heading);font-size:16px;font-weight:600;box-sizing:border-box;text-align:right">
      <span style="position:absolute;right:10px;top:50%;transform:translateY(-50%);font-size:12px;color:var(--clr-muted);pointer-events:none">₽</span>
    </div>
    <button class="dw-btn" id="fc-run" style="padding:8px 16px;font-size:13px">Запустить</button>
  </div>
  <div id="fc-result" style="display:none;flex-direction:column;gap:6px;padding:12px 14px;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:10px">
    <div style="display:flex;justify-content:space-between;font-size:12px;color:var(--clr-muted)"><span>Прошло платежей</span><span id="fc-r-pm">1 × 975 ₽ (после комиссии)</span></div>
    <div style="display:flex;justify-content:space-between;font-size:12px;color:var(--clr-muted)"><span>Комиссия</span><span id="fc-r-cm">−15 ₽</span></div>
    <div style="display:flex;justify-content:space-between;font-size:12px;color:var(--clr-muted)"><span>Сплит</span><span id="fc-r-sp">931 / 29 ₽</span></div>
    <div style="display:flex;justify-content:space-between;font-size:12px;color:var(--clr-muted)"><span>Уведомления</span><span id="fc-r-nt">SMS, Push → отправлены</span></div>
    <div style="border-top:1px solid var(--clr-border);padding-top:8px;display:flex;justify-content:space-between">
      <span style="font-size:14px;font-weight:600;color:var(--clr-heading)">Магазин получит</span>
      <span style="font-size:20px;font-weight:700;color:var(--clr-accent)" id="fc-payout">931 ₽</span>
    </div>
  </div>
</div>
<style>.dw{margin:12px 0;background:var(--clr-surface);border:1px solid var(--clr-border);border-radius:16px;padding:24px}.dw-t{font-size:16px;font-weight:600;margin:0 0 16px;color:var(--clr-heading)}.dw-btn{padding:10px 20px;background:var(--clr-accent);border:none;border-radius:10px;color:#fff;font-size:14px;font-weight:600;cursor:pointer;transition:opacity .2s}.dw-btn:hover{opacity:.85}.fc-b{display:flex;align-items:center;gap:8px;padding:10px 12px;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:8px;transition:all .2s;cursor:pointer}.fc-b:hover{border-color:var(--clr-accent)}.fc-b.hl{border-color:var(--clr-accent);box-shadow:0 0 0 2px var(--clr-accent)22}@media(min-width:768px){.dw{max-width:520px;margin-left:auto;margin-right:auto}}</style>
<script>(function(){var amount=document.getElementById('fc-amount'),run=document.getElementById('fc-run'),result=document.getElementById('fc-result'),blocks=document.querySelectorAll('.fc-b');var pm=0,cm=0,sp=0,nt=0;var pmOpts=['Visa, MC','Visa, MC, Мир, SBP','Только SBP'];var cmOpts=['0.5% + 10 ₽','1.5%','2% (без фикс)'];var spOpts=['Магазин: 97% | Партнёр: 3%','Магазин: 100%','Магазин: 50% | Партнёр: 50%'];var ntOpts=['SMS, Push','Email, Push','SMS, Email, Push'];function up(v,el,opts){var idx=v%opts.length;document.getElementById(el).textContent=opts[idx]}blocks[0].addEventListener('click',function(){pm++;up(pm,'fc-pm',pmOpts)});blocks[1].addEventListener('click',function(){cm++;up(cm,'fc-cm',cmOpts)});blocks[2].addEventListener('click',function(){sp++;up(sp,'fc-sp',spOpts)});blocks[3].addEventListener('click',function(){nt++;up(nt,'fc-nt',ntOpts)});run.addEventListener('click',function(){var raw=amount.value.replace(/[\\s,]/g,'');var val=parseFloat(raw);if(isNaN(val)||val<1)val=1000;amount.value=Math.round(val).toLocaleString('ru-RU');var pmi=document.getElementById('fc-pm'),cmi=document.getElementById('fc-cm'),spi=document.getElementById('fc-sp'),nti=document.getElementById('fc-nt');blocks.forEach(function(b,i){b.classList.remove('hl')});var fee=0;if(cmi.textContent.indexOf('0.5%')>=0){fee=Math.round(val*0.5/100)+10}else if(cmi.textContent.indexOf('1.5%')>=0){fee=Math.round(val*1.5/100)}else{fee=Math.round(val*2/100)}var afterAcq=Math.round(val*0.975);var afterFee=afterAcq-fee;var ms=afterFee,pn=0;if(spi.textContent.indexOf('97%')>=0){ms=Math.round(afterFee*0.97);pn=afterFee-ms}else if(spi.textContent.indexOf('50%')>=0){ms=Math.round(afterFee*0.5);pn=afterFee-ms}else{ms=afterFee;pn=0}document.getElementById('fc-r-pm').textContent='1 x '+afterAcq.toLocaleString('ru-RU')+' ₽';document.getElementById('fc-r-cm').textContent='−'+fee.toLocaleString('ru-RU')+' ₽';document.getElementById('fc-r-sp').textContent=ms.toLocaleString('ru-RU')+(pn>0?' / '+pn.toLocaleString('ru-RU'):' 0')+' ₽';document.getElementById('fc-r-nt').textContent=nti.textContent+' → отправлены';document.getElementById('fc-payout').textContent=ms.toLocaleString('ru-RU')+' ₽';result.style.display='flex';result.style.animation='none';result.offsetHeight;result.style.animation='fIn .3s';var i=0;var t=setInterval(function(){if(i>=4){clearInterval(t);return}blocks[i].classList.add('hl');i++},300)});amount.addEventListener('keydown',function(e){if(e.key==='Enter')run.click()})})();</script>""",
        "widget_css": "",
        "widget_js": ""
    },
    {
        "slug": "project-portfolio",
        "title": "Портфель проектов",
        "desc": "Dashboard управления портфелем IT-проектов: сроки, ресурсы, бюджеты, риски. Иерархия: портфель → программа → проект.",
        "meta_desc": "Демо системы управления портфелем проектов: dashboard, Gantt, ресурсы, бюджеты, риски. PMO-инструмент для IT-компаний.",
        "code": """// Создание портфеля проектов
const portfolio = await pmo.createPortfolio({
  name: 'Финтех-направление 2024',
  budget: 50000000,
  strategicGoal: 'Рост доли финтех-продуктов'
});

// Добавление проекта
const project = await pmo.addProject({
  portfolioId: portfolio.id,
  name: 'Маркетплейс V2',
  type: 'product',
  startDate: '2024-09-01',
  endDate: '2025-03-01',
  budget: 15000000,
  resources: [
    { role: 'backend', count: 3 },
    { role: 'frontend', count: 2 }
  ]
});

// Оценка рисков
const risk = await pmo.assessRisk(project.id, {
  type: 'technical',
  probability: 0.3,
  impact: 'high',
  mitigation: 'Proof of Concept'
});""",
        "features": ["Иерархия: портфель → программа → проект", "Gantt-диаграммы и вехи", "Управление ресурсами", "Бюджетный контроль", "Риск-менеджмент", "Power BI-отчёты"],
        "tags": ["React", "Python", "PostgreSQL", "D3.js", "Docker"],
        "gradient": "#D4A574,#8b5e3c",
        "widget_html": """<div class="dw">
  <h3 class="dw-t"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="var(--clr-heading)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-3px;margin-right:6px"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/><line x1="15" y1="21" x2="15" y2="9"/></svg>Портфель проектов</h3>
  <div style="display:flex;flex-direction:column;gap:8px">
    <div class="pp-p expanded" data-i="0">
      <div class="pp-hdr" tabindex="0" role="button" aria-expanded="true">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="var(--clr-text)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
        <div style="flex:1;min-width:0"><div style="font-size:14px;font-weight:600;color:var(--clr-heading)">Маркетплейс V2</div><div style="font-size:11px;color:var(--clr-muted)">Сен 2024 — Мар 2025 · 5 чел.</div></div>
        <div style="text-align:right"><div style="font-size:13px;font-weight:600;color:var(--clr-accent)">70%</div><div style="font-size:10px;color:var(--clr-muted)">активно</div></div>
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="var(--clr-muted)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="pp-arr" style="flex-shrink:0;transition:transform .25s"><polyline points="6 9 12 15 18 9"/></svg>
      </div>
      <div class="pp-body">
        <div class="pp-progress"><span>Прогресс</span><span>70%</span></div>
        <div style="height:6px;background:var(--clr-surface);border-radius:3px;overflow:hidden;margin-bottom:10px"><div style="height:100%;width:70%;background:linear-gradient(90deg,#6c5ce7,#a29bfe);border-radius:3px"></div></div>
        <div class="pp-grid">
          <div class="pp-m"><span>Бюджет</span><strong>15 млн</strong><small style="color:#00b894">10.5 млн потрачено</small></div>
          <div class="pp-m"><span>Команда</span><strong>5 чел.</strong><small>бэк 3 · фронт 2</small></div>
          <div class="pp-m"><span>Риски</span><strong style="color:#00b894"><svg viewBox="0 0 10 10" width="10" height="10" style="vertical-align:-1px;margin-right:3px"><circle cx="5" cy="5" r="4" fill="#00b894"/></svg>Низкие</strong><small>митигированы</small></div>
          <div class="pp-m"><span>След. веха</span><strong>MVP</strong><small>Дек 2024</small></div>
        </div>
      </div>
    </div>
    <div class="pp-p" data-i="1">
      <div class="pp-hdr" tabindex="0" role="button" aria-expanded="false">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="var(--clr-text)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
        <div style="flex:1;min-width:0"><div style="font-size:14px;font-weight:600;color:var(--clr-heading)">Кредитный конвейер</div><div style="font-size:11px;color:var(--clr-muted)">Янв 2025 — Июн 2025 · 4 чел.</div></div>
        <div style="text-align:right"><div style="font-size:13px;font-weight:600;color:#f39c12">35%</div><div style="font-size:10px;color:var(--clr-muted)">в работе</div></div>
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="var(--clr-muted)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="pp-arr" style="flex-shrink:0;transition:transform .25s"><polyline points="6 9 12 15 18 9"/></svg>
      </div>
      <div class="pp-body">
        <div class="pp-progress"><span>Прогресс</span><span>35%</span></div>
        <div style="height:6px;background:var(--clr-surface);border-radius:3px;overflow:hidden;margin-bottom:10px"><div style="height:100%;width:35%;background:linear-gradient(90deg,#00b894,#55efc4);border-radius:3px"></div></div>
        <div class="pp-grid">
          <div class="pp-m"><span>Бюджет</span><strong>8 млн</strong><small style="color:#f39c12">2.8 млн потрачено</small></div>
          <div class="pp-m"><span>Команда</span><strong>4 чел.</strong><small>бэк 2 · фронт 1 · ML 1</small></div>
          <div class="pp-m"><span>Риски</span><strong style="color:#f39c12"><svg viewBox="0 0 10 10" width="10" height="10" style="vertical-align:-1px;margin-right:3px"><circle cx="5" cy="5" r="4" fill="#f39c12"/></svg>Средние</strong><small>интеграция БКИ</small></div>
          <div class="pp-m"><span>След. веха</span><strong>Скоринг</strong><small>Апр 2025</small></div>
        </div>
      </div>
    </div>
    <div class="pp-p" data-i="2">
      <div class="pp-hdr" tabindex="0" role="button" aria-expanded="false">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="var(--clr-text)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12" y2="18"/></svg>
        <div style="flex:1;min-width:0"><div style="font-size:14px;font-weight:600;color:var(--clr-heading)">Mobile App</div><div style="font-size:11px;color:var(--clr-muted)">Май 2025 — Авг 2025 · 3 чел.</div></div>
        <div style="text-align:right"><div style="font-size:13px;font-weight:600;color:#e17055">15%</div><div style="font-size:10px;color:var(--clr-muted)">планир.</div></div>
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="var(--clr-muted)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="pp-arr" style="flex-shrink:0;transition:transform .25s"><polyline points="6 9 12 15 18 9"/></svg>
      </div>
      <div class="pp-body">
        <div class="pp-progress"><span>Прогресс</span><span>15%</span></div>
        <div style="height:6px;background:var(--clr-surface);border-radius:3px;overflow:hidden;margin-bottom:10px"><div style="height:100%;width:15%;background:linear-gradient(90deg,#fdcb6e,#f39c12);border-radius:3px"></div></div>
        <div class="pp-grid">
          <div class="pp-m"><span>Бюджет</span><strong>6 млн</strong><small style="color:#00b894">0.9 млн потрачено</small></div>
          <div class="pp-m"><span>Команда</span><strong>3 чел.</strong><small>iOS · Android · PM</small></div>
          <div class="pp-m"><span>Риски</span><strong style="color:#e17055"><svg viewBox="0 0 10 10" width="10" height="10" style="vertical-align:-1px;margin-right:3px"><circle cx="5" cy="5" r="4" fill="#e17055"/></svg>Высокие</strong><small>сроки, найм</small></div>
          <div class="pp-m"><span>След. веха</span><strong>Дизайн</strong><small>Июн 2025</small></div>
        </div>
      </div>
    </div>
  </div>
</div>
<style>.dw{margin:12px 0;background:var(--clr-surface);border:1px solid var(--clr-border);border-radius:16px;padding:24px}.dw-t{font-size:16px;font-weight:600;margin:0 0 16px;color:var(--clr-heading)}.pp-p{display:flex;flex-direction:column;padding:0;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:10px;overflow:hidden;transition:border-color .2s}.pp-p:hover{border-color:var(--clr-accent)}.pp-p.expanded{border-color:var(--clr-accent)}.pp-hdr{display:flex;align-items:center;gap:12px;cursor:pointer;width:100%;padding:12px 14px;box-sizing:border-box;transition:background .2s;border-left:3px solid transparent}.pp-hdr:hover{background:rgba(108,92,231,.06)}.pp-p.expanded .pp-hdr{border-left-color:var(--clr-accent);background:rgba(108,92,231,.04)}.pp-body{display:none;padding:0 14px 12px;font-size:13px;color:var(--clr-text);animation:fadeIn .25s ease}.pp-p.expanded .pp-body{display:block}.pp-p.expanded .pp-arr{transform:rotate(180deg)}.pp-progress{display:flex;justify-content:space-between;font-size:11px;color:var(--clr-muted);margin-bottom:2px}.pp-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px}.pp-m{display:flex;flex-direction:column;gap:1px;padding:8px 10px;background:var(--clr-surface);border:1px solid var(--clr-border);border-radius:6px;line-height:1.4}.pp-m span{font-size:10px;color:var(--clr-muted);text-transform:uppercase;letter-spacing:.3px}.pp-m strong{font-size:13px;font-weight:600;color:var(--clr-heading)}.pp-m small{font-size:10px;color:var(--clr-muted)}@keyframes fadeIn{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:translateY(0)}}@media(min-width:768px){.dw{max-width:600px;margin-left:auto;margin-right:auto}}</style>
<script>(function(){document.querySelectorAll('.pp-p').forEach(function(p){var hdr=p.querySelector('.pp-hdr');hdr.addEventListener('click',function(){var was=p.classList.contains('expanded');document.querySelectorAll('.pp-p.expanded').forEach(function(x){x.classList.remove('expanded');x.setAttribute('aria-expanded','false')});if(!was){p.classList.add('expanded');p.setAttribute('aria-expanded','true')}});hdr.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();hdr.click()}})})})();</script>""",
        "widget_css": "",
        "widget_js": ""
    },
    {
        "slug": "payment-page",
        "title": "Платёжная страница",
        "desc": "Кастомизируемая платёжная страница (Checkout Page) с мультиэквайрингом, скинами под бренд и умной маршрутизацией.",
        "meta_desc": "Демо платёжной страницы: кастомизируемый checkout, мультиэквайринг, скины, умная маршрутизация. Примеры кода встраивания.",
        "code": """// Встраивание платёжной страницы
&lt;iframe src="https://pay.axiiom.ru/checkout/{session_id}" 
        width="100%" height="600" frameborder="0"&gt;
&lt;/iframe&gt;

// Создание сессии checkout
const session = await checkout.createSession({
  merchantId: 'merchant_789',
  amount: 5499.00,
  currency: 'RUB',
  skin: 'dark_theme',
  methods: ['card', 'sbp', 'wallet'],
  successUrl: 'https://example.com/success',
  failUrl: 'https://example.com/fail'
});

// Умная маршрутизация
const route = await checkout.smartRoute({
  sessionId: session.id,
  amount: 5499.00,
  method: 'card',
  bin: '4276******1234'
});
// Выбирает оптимальный эквайринг""",
        "features": ["Кастомизация под бренд (скины)", "Умная маршрутизация платежей", "Мультиэквайринг на одной странице", "Invoice-ссылки", "Антифрод (3DS 2.0)", "Аналитика конверсий"],
        "tags": ["React", "Node.js", "PCI DSS", "3DS 2.0", "PostgreSQL"],
        "gradient": "#0984e3,#74b9ff",
        "widget_html": """<div class="pc-card">
  <div class="pc-head">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--clr-accent)" stroke-width="1.8"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/><line x1="6" y1="15" x2="10" y2="15"/></svg>
    <span>Checkout Page</span>
  </div>
  <div class="pc-body">
    <div class="pc-grid">
      <div class="pc-form">
        <div class="pc-fld">
          <label class="pc-lbl">Email</label>
          <input class="pc-inp" id="pp-email" value="user@example.com">
        </div>
        <div class="pc-fld">
          <label class="pc-lbl">Номер карты</label>
          <div class="pc-iw">
            <input class="pc-inp pc-mono" id="pp-card" placeholder="0000 0000 0000 0000" maxlength="19">
            <svg class="pc-ci" width="22" height="16" viewBox="0 0 24 16"><rect x="1" y="1" width="22" height="14" rx="2" stroke="var(--clr-faint)" stroke-width="1.2" fill="none"/><line x1="1" y1="6" x2="23" y2="6" stroke="var(--clr-faint)" stroke-width="1.2"/><circle cx="9" cy="10" r="2.5" stroke="var(--clr-accent)" stroke-width="1.2" fill="none" opacity=".5"/><circle cx="15" cy="10" r="2.5" stroke="var(--clr-accent)" stroke-width="1.2" fill="none" opacity=".5"/></svg>
          </div>
        </div>
        <div class="pc-fld">
          <label class="pc-lbl">Имя на карте</label>
          <input class="pc-inp pc-mono" id="pp-name" value="IVAN PETROV">
        </div>
        <button class="pc-btn" id="pp-btn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="10" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
          Оплатить 5 499 ₽
        </button>
      </div>
      <div class="pc-order">
        <div class="pc-order-hdr">Ваш заказ</div>
        <div class="pc-order-row"><span>Смартфон X Pro × 1</span><span>79 990 ₽</span></div>
        <div class="pc-order-row"><span>Страховка +1 год</span><span>3 990 ₽</span></div>
        <div class="pc-order-row"><span>Доставка</span><span class="pc-free">Бесплатно</span></div>
        <div class="pc-order-row pc-order-total"><span>Итого</span><span>83 980 ₽</span></div>
        <div class="pc-order-badge">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="10" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
          Безопасная оплата
        </div>
      </div>
    </div>
    <div class="pc-3ds" id="pp-modal">
      <div class="pc-3ds-box">
        <div class="pc-3ds-icon">🔐</div>
        <div class="pc-3ds-t">3D Secure</div>
        <div class="pc-3ds-sub">Подтвердите оплату через ваш банк</div>
        <div class="pc-3ds-actions">
          <button class="pc-btn pc-btn-sm" id="pp-confirm">Подтвердить</button>
          <button class="pc-btn pc-btn-sm pc-btn-ghost" id="pp-cancel">Отмена</button>
        </div>
      </div>
    </div>
    <div class="pc-ok" id="pp-ok">
      <svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#00b894" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="16 8 10 16 7 12"/></svg>
      <div class="pc-ok-t">Оплата подтверждена</div>
      <div class="pc-ok-sub">Спасибо! Ваш платёж прошёл успешно.</div>
    </div>
  </div>
</div>
<style>
.pc-card{margin:12px 0;background:var(--clr-surface);border:1px solid var(--clr-border);border-radius:20px;overflow:hidden}
.pc-head{display:flex;align-items:center;gap:10px;padding:20px 24px 0;font-size:15px;font-weight:600;color:var(--clr-heading)}
.pc-body{padding:20px 24px 24px;display:flex;flex-direction:column;gap:0}
.pc-grid{display:flex;flex-direction:column;gap:18px}
.pc-order{margin-top:0}
.pc-form{display:flex;flex-direction:column;gap:14px}
.pc-fld{display:flex;flex-direction:column;gap:5px}
.pc-lbl{font-size:11px;color:var(--clr-faint);font-weight:500;letter-spacing:.4px;text-transform:uppercase}
.pc-iw{position:relative;display:flex;align-items:center}
.pc-inp{width:100%;padding:12px 14px;background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:12px;color:var(--clr-text);font-size:14px;box-sizing:border-box;transition:border-color .25s,box-shadow .25s}
.pc-inp:focus{outline:none;border-color:var(--clr-accent);box-shadow:0 0 0 3px color-mix(in srgb,var(--clr-accent) 18%,transparent)}
.pc-mono{font-family:'SF Mono','Fira Code',monospace;letter-spacing:.5px}
.pc-mono::placeholder{color:var(--clr-faint);opacity:.4;letter-spacing:0}
.pc-ci{position:absolute;right:12px;pointer-events:none;opacity:.6}
.pc-btn{display:flex;align-items:center;justify-content:center;gap:10px;padding:14px;background:var(--clr-accent);border:none;border-radius:14px;color:#fff;font-size:15px;font-weight:600;cursor:pointer;transition:opacity .25s,transform .15s;font-family:inherit;width:100%;margin-top:2px}
.pc-btn:hover{opacity:.9;transform:translateY(-1px)}
.pc-btn:active{transform:translateY(0)}
.pc-btn-sm{padding:12px 20px;width:auto;font-size:13px}
.pc-btn-ghost{background:var(--clr-bg);color:var(--clr-text);border:1px solid var(--clr-border)}
.pc-order{background:var(--clr-bg);border:1px solid var(--clr-border);border-radius:14px;padding:16px}
.pc-order-hdr{font-size:13px;font-weight:600;color:var(--clr-heading);margin-bottom:12px}
.pc-order-row{display:flex;justify-content:space-between;font-size:13px;color:var(--clr-text);padding:5px 0;border-bottom:1px solid var(--clr-border)}
.pc-order-row:last-of-type{border-bottom:none}
.pc-order-total{font-weight:700;color:var(--clr-heading);padding-top:8px!important;font-size:14px;border-top:1px solid var(--clr-border)!important;margin-top:4px}
.pc-free{color:#00b894;font-weight:500}
.pc-order-badge{display:flex;align-items:center;justify-content:center;gap:5px;font-size:10px;color:var(--clr-faint);opacity:.6;margin-top:12px;padding-top:8px;border-top:1px solid var(--clr-border)}
.pc-3ds{display:none;position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:99999;align-items:center;justify-content:center}
.pc-3ds-box{background:var(--clr-surface);border:1px solid var(--clr-border);border-radius:20px;padding:32px;text-align:center;max-width:340px;width:90%;animation:pcf .3s ease}
.pc-3ds-icon{font-size:36px;margin-bottom:12px}
.pc-3ds-t{font-size:16px;font-weight:600;color:var(--clr-heading);margin-bottom:6px}
.pc-3ds-sub{font-size:13px;color:var(--clr-muted);margin-bottom:18px}
.pc-3ds-actions{display:flex;gap:10px;justify-content:center}
.pc-ok{display:none;flex-direction:column;align-items:center;gap:6px;padding:20px 0 8px;text-align:center}
.pc-ok-t{color:#00b894;font-weight:600;font-size:16px;margin-top:4px}
.pc-ok-sub{color:var(--clr-faint);font-size:12px;opacity:.6}
@keyframes pcf{from{opacity:0;transform:scale(.95)}to{opacity:1;transform:scale(1)}}
@media (min-width:768px){.pc-card{max-width:520px;margin-left:auto;margin-right:auto}}
@media (max-width:640px){.pc-head{padding:16px 18px 0}.pc-body{padding:16px 18px 20px}.pc-order{padding:14px}}
</style>
<script>
(function(){
document.getElementById('pp-card').addEventListener('input',function(e){e.target.value=e.target.value.replace(/\\D/g,'').replace(/(.{4})/g,'$1 ').trim();});
document.getElementById('pp-btn').addEventListener('click',function(){document.getElementById('pp-modal').style.display='flex';});
document.getElementById('pp-confirm').addEventListener('click',function(){document.getElementById('pp-modal').style.display='none';document.getElementById('pp-ok').style.display='flex';var b=document.getElementById('pp-btn');b.textContent='✓ Оплачено';b.disabled=1;b.style.cursor='default';b.style.transform='none'});
document.getElementById('pp-cancel').addEventListener('click',function(){document.getElementById('pp-modal').style.display='none';});
document.getElementById('pp-modal').addEventListener('click',function(e){if(e.target===this)this.style.display='none';});
})();</script>""",
        "widget_css": "",
        "widget_js": ""
    }
]

TEMPLATE = """<!doctype html>
<html lang="ru" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <meta name="theme-color" content="#0A0A0F">
  <title>{TITLE} — Демо-версия | AXIIOM</title>
  <meta name="description" content="{META_DESC}">
  <link rel="canonical" href="https://axiiom.ru/demo/app/{SLUG}/">

  <meta property="og:type" content="website">
  <meta property="og:url" content="https://axiiom.ru/demo/app/{SLUG}/">
  <meta property="og:title" content="{TITLE} — Демо | AXIIOM">
  <meta property="og:description" content="{META_DESC}">
  <meta property="og:image" content="https://axiiom.ru/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="ru_RU">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:url" content="https://axiiom.ru/demo/app/{SLUG}/">
  <meta name="twitter:title" content="{TITLE} — Демо | AXIIOM">
  <meta name="twitter:description" content="{META_DESC}">
  <meta name="twitter:image" content="https://axiiom.ru/og-image.png">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "{TITLE} — AXIIOM Demo",
    "description": "{META_DESC}",
    "url": "https://axiiom.ru/demo/app/{SLUG}/",
    "applicationCategory": "BusinessApplication",
    "operatingSystem": "Web",
    "author": {{
      "@type": "Organization",
      "name": "AXIIOM"
    }},
    "offers": {{
      "@type": "Offer",
      "price": "0",
      "priceCurrency": "RUB"
    }}
  }}
  </script>

  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path fill='%23{COLOR}' d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z'/></svg>" type="image/svg+xml">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" as="style">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">
  <link rel="stylesheet" href="/preloader.css">
  <style>
    .demo-page-hero {{
      min-height: 60vh; display: flex; align-items: center; justify-content: center;
      text-align: center; position: relative; overflow: hidden; padding-top: 100px;
      background: radial-gradient(ellipse 60% 40% at 30% 20%, rgba({R},{G},{B},.12), transparent),
                  radial-gradient(ellipse 50% 35% at 70% 80%, rgba({R},{G},{B},.05), transparent),
                  var(--clr-bg);
    }}
    .hero-bg-svg {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); width: 100%; max-width: 800px; opacity: .5; pointer-events: none; animation: rotateSlow 60s linear infinite; }}
    @keyframes rotateSlow {{ to {{ transform: translate(-50%,-50%) rotate(360deg); }} }}
    .code-block {{
      background: rgba(255,255,255,.03); border: 1px solid var(--clr-border);
      border-radius: 16px; padding: 24px; overflow-x: auto; margin: 20px 0;
      font-family: 'SF Mono','Fira Code','Consolas',monospace; font-size: 13px; line-height: 1.7;
    }}
    .code-block code {{ white-space: pre; }}
    .feature-grid {{
      display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
      gap: 16px; margin: 32px 0;
    }}
    .feature-item {{
      display: flex; align-items: center; gap: 12px; padding: 16px 20px;
      background: rgba(255,255,255,.02); border: 1px solid var(--clr-border);
      border-radius: 12px; font-size: 14px; color: var(--clr-text);
    }}
    .feature-item svg {{ flex-shrink: 0; width: 20px; height: 20px; }}
    .tag-list {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }}
    .tag-item {{
      display: inline-block; padding: 4px 14px; border: 1px solid var(--clr-border);
      border-radius: 20px; font-size: 12px; color: var(--clr-muted);
    }}
    .demo-nav-back {{
      position: fixed; top: 12px; left: 16px; z-index: 99999;
      display: inline-flex; align-items: center; gap: 6px;
      padding: 8px 16px; background: rgba(10,10,15,.9);
      color: #C7C7CC; border: 1px solid rgba(255,255,255,.08);
      border-radius: 20px; text-decoration: none;
      font-family: Inter,sans-serif; font-size: 13px; transition: all .2s;
    }}
    .demo-nav-back:hover {{ background: rgba(10,10,15,1); color: #F5F5F7; }}
    @media (max-width: 768px) {{
      .demo-page-hero {{ min-height: 50vh; padding-top: 80px; }}
      .feature-grid {{ grid-template-columns: 1fr; }}
      .hero-bg-svg {{ max-width: 500px; }}
    }}
  </style>
</head>
<body>
<div id="preloader">
<script>(function(){{var p=document.getElementById('preloader');if(!p)return;if(sessionStorage.getItem('_seen')){{p.style.display='none';return}}sessionStorage.setItem('_seen','1');var t=Date.now();p._start=t;setTimeout(function(){{p.classList.add('_rdy')}},500);window.addEventListener('load',function(){{var e=Date.now()-t;if(e<2000){{setTimeout(function(){{p.classList.add('hidden');setTimeout(function(){{p.classList.add('hidden-done')}},500)}},2000-e)}}else{{p.classList.add('hidden');setTimeout(function(){{p.classList.add('hidden-done')}},500)}}}})}})()</script>
  <svg class="preloader-svg" viewBox="0 0 36 36" width="80" height="80">
    <rect class="pr1" x="2" y="2" width="14" height="14" rx="2"/>
    <rect class="pr2" x="20" y="2" width="14" height="14" rx="2"/>
    <rect class="pr3" x="2" y="20" width="14" height="14" rx="2"/>
    <rect class="pr4" x="20" y="20" width="14" height="14" rx="2"/>
    <circle class="pc" cx="27" cy="27" r="3"/>
  </svg>
</div>

<div class="noise"></div>
<div class="grid-overlay"></div>

<header class="header" id="header">
  <div class="container">
    <nav class="nav">
      <a href="/" class="logo">
        <svg width="30" height="30" viewBox="0 0 36 36" fill="none">
          <rect x="2" y="2" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5" opacity=".4"/>
          <rect x="20" y="2" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5" opacity=".4"/>
          <rect x="2" y="20" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5" opacity=".4"/>
          <rect x="20" y="20" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5"/>
          <circle cx="27" cy="27" r="3" fill="currentColor" opacity=".8"/>
        </svg>
        <span>AXIIOM</span>
      </a>
      <ul class="nav-links nav-links--desktop" id="desktopNav"></ul>
      <div class="nav-actions">
        <a href="/#contact" class="btn btn-nav">Обсудить проект</a>
        <button class="theme-btn" id="themeToggle" aria-label="Сменить тему">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg>
        </button>
        <button class="nav-toggle" id="navToggle" aria-label="Меню"><span></span><span></span><span></span></button>
      </div>
    </nav>
  </div>
</header>

<div class="nav-overlay" id="navOverlay"><ul class="nav-links" id="mobileNav"></ul></div>
<nav class="breadcrumbs" id="breadcrumbs" aria-label="Breadcrumb"><div class="container"></div></nav>

<a href="/demo/app/" class="demo-nav-back">← Все демо AXIIOM</a>

<section class="demo-page-hero">
  <div class="hero-bg-svg" aria-hidden="true"><svg width="800" height="600" viewBox="0 0 800 600" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="400" cy="300" r="280" stroke="rgba(255,255,255,0.05)" stroke-width="2"/><circle cx="400" cy="300" r="200" stroke="rgba(255,255,255,0.06)" stroke-width="2"/><circle cx="400" cy="300" r="120" stroke="rgba(255,255,255,0.08)" stroke-width="2"/><line x1="50" y1="300" x2="750" y2="300" stroke="rgba(255,255,255,0.05)" stroke-width="2"/><line x1="400" y1="20" x2="400" y2="580" stroke="rgba(255,255,255,0.05)" stroke-width="2"/><path d="M200 300 L400 100 L600 300 L400 500 Z" stroke="rgba(255,255,255,0.06)" stroke-width="2" fill="none"/><circle cx="400" cy="300" r="4" fill="rgba(255,255,255,0.15)"/></svg></div>
  <div class="container">
    <div class="hero-content">
      <p class="badge">AXIIOM Demo</p>
      <h1>{TITLE}</h1>
      <p class="hero-desc">{DESC}</p>
      <div class="tag-list" style="justify-content:center;">
{TAGS}
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <p class="label">Интерактивное демо</p>
    <h2>Попробуйте прямо сейчас</h2>
    {DEMO_WIDGET}
  </div>
</section>

<section class="section">
  <div class="container">
    <p class="label">Пример кода</p>
    <h2>Интеграция за 5 минут</h2>
    <div class="code-block"><code>{CODE}</code></div>
  </div>
</section>

<section class="section dark">
  <div class="container">
    <p class="label">Возможности</p>
    <h2>Ключевые функции</h2>
    <div class="feature-grid">
{FEATURES}
    </div>
  </div>
</section>

<section class="section cta-section">
  <div class="container">
    <div class="glass-card" style="padding:48px 32px;text-align:center;border-radius:24px;">
      <h2 style="margin-bottom:16px;">Хотите такое решение?</h2>
      <p style="color:var(--clr-text);margin-bottom:24px;max-width:480px;margin-left:auto;margin-right:auto;">Обсудим ваш проект, покажем демо и рассчитаем стоимость.</p>
      <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;">
        <a href="mailto:{CONTACT_EMAIL}" class="btn">{CONTACT_EMAIL}</a>
        <a href="tel:{CONTACT_PHONE_LINK}" class="btn btn-outline">{CONTACT_PHONE}</a>
      </div>
    </div>
  </div>
</section>

<footer class="footer">
  <div class="container">
    <div id="footerCopy"></div>
  </div>
</footer>

<script>
var header = document.getElementById('header');
window.addEventListener('scroll', function() {{
  header.classList.toggle('scrolled', window.scrollY > 40);
}}, {{ passive: true }});

var reveals = document.querySelectorAll('.reveal');
var ro = new IntersectionObserver(function(e) {{
  e.forEach(function(entry) {{
    if (entry.isIntersecting) entry.target.classList.add('visible');
  }});
}}, {{ threshold: 0.15 }});
reveals.forEach(function(r) {{ ro.observe(r); }});
</script>

<script src="/config.js"></script>
<script src="/nav.js"></script>
<script>Nav.init({{ cta: true, breadcrumbs: true }});</script>
<script src="/theme.js"></script>
<script src="/preloader.js"></script>

<script>
(function() {{
  var t = document.getElementById('navToggle');
  var o = document.getElementById('navOverlay');
  if (!t || !o) return;
  t.addEventListener('click', function(e) {{
    e.stopPropagation();
    o.classList.toggle('open');
    t.classList.toggle('active');
    document.body.style.overflow = o.classList.contains('open') ? 'hidden' : '';
  }});
}})();
</script>

<!-- Yandex.Metrika counter -->
<script type="text/javascript">(function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){{if(document.scripts[j].src===r){{return}}}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)}})(window,document,"script","https://mc.yandex.ru/metrika/tag.js?id={YM_ID}","ym");ym({YM_ID},"init",{{clickmap:true,trackLinks:true,accurateTrackBounce:true}});</script>
<noscript><div><img src="https://mc.yandex.ru/watch/{YM_ID}" style="position:absolute;left:-9999px" alt=""></div></noscript>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
</body>
</html>"""


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    elif len(hex_color) == 3:
        r, g, b = int(hex_color[0]*2, 16), int(hex_color[1]*2, 16), int(hex_color[2]*2, 16)
    else:
        return 100, 80, 220
    return r, g, b


def make_tags(tags):
    return "\n".join(f'        <span class="tag-item">{t}</span>' for t in tags)


def make_features(features, color):
    rows = []
    for f in features:
        rows.append(f"""      <div class="feature-item">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#{color}" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
        <span>{f}</span>
      </div>""")
    return "\n".join(rows)


def main():
    base = os.path.dirname(os.path.abspath(__file__))

    for demo in DEMOS:
        slug = demo["slug"]
        color = demo["gradient"].split(",")[0].strip("#")
        r, g, b = hex_to_rgb(demo["gradient"].split(",")[0].strip())

        html = TEMPLATE.format(
            SLUG=slug,
            TITLE=demo["title"],
            DESC=demo["desc"],
            META_DESC=demo["meta_desc"],
            CODE=demo["code"],
            TAGS=make_tags(demo["tags"]),
            FEATURES=make_features(demo["features"], color),
            DEMO_WIDGET=demo.get("widget_html", ""),
            COLOR=color,
            R=r, G=g, B=b,
            CONTACT_EMAIL=CONFIG["contact"]["email"],
            CONTACT_PHONE=CONFIG["contact"]["phone"],
            CONTACT_PHONE_LINK=CONFIG["contact"]["phoneLink"],
            YM_ID=CONFIG["analytics"]["yandexMetrika"],
            GA_ID=CONFIG["analytics"]["googleAnalytics"],
        )

        dir_path = os.path.join(base, slug)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, "index.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✓ {slug}/index.html")

    print(f"\nВсего создано: {len(DEMOS)} страниц")


if __name__ == "__main__":
    main()
