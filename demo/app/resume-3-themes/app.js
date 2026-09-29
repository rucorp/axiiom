/* kuzyukov resume: themes (deck/brief/terminal), lang (ru/en), cli, counters. 0 deps. */
(function () {
"use strict";
var $ = function (s, r) { return (r || document).querySelector(s); };
var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
var root = document.documentElement;

function store(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
function read(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
function lang() { return root.dataset.lang === "en" ? "en" : "ru"; }

/* ---------- toast ---------- */
var toastEl = $("#toast"), toastT;
function toast(msg) {
  if (!toastEl) return;
  toastEl.textContent = msg;
  toastEl.classList.add("show");
  clearTimeout(toastT);
  toastT = setTimeout(function () { toastEl.classList.remove("show"); }, 1800);
}

/* ---------- url params ---------- */
function getParams() {
  try { return new URLSearchParams(location.search); } catch (e) { return { get: function () { return null; } }; }
}
function syncURL() {
  try {
    var u = new URL(location.href);
    u.searchParams.set("theme", root.dataset.theme);
    u.searchParams.set("lang", lang());
    history.replaceState(null, "", u.toString());
  } catch (e) {}
}

/* ---------- i18n chrome ---------- */
var TITLES = {
  ru: "Сергей Кузюков — CDTO · Трансформация с P&L-ответственностью",
  en: "Sergey Kuzyukov — CDTO · Transformation with P&L accountability"
};
var DESCS = {
  ru: "CDTO: legacy и регуляторика → выручка. 500K+ пользователей, 5→45 команда, 3× Сбер 2,8–4,1 млрд ₽, вуз 12 000+ студентов за 2 месяца. Финтех, БПА/ЦБ, highload, AI.",
  en: "CDTO: legacy & regulation → revenue. 500K+ users, 5→45 team, 3× Sberbank approvals up to ₽4.1B, 12,000+ student university in 2 months. Fintech, compliance, highload, AI."
};

/* ---------- theme ---------- */
var THEMES = ["deck", "brief", "terminal"];
var cliBooted = false;
function setTheme(t) {
  if (THEMES.indexOf(t) < 0) t = "deck";
  root.dataset.theme = t;
  var r = document.querySelector('input[name="theme"][value="' + t + '"]');
  if (r) r.checked = true;
  $$('label[for^="t-"]').forEach(function (el) {
    el.setAttribute("data-active", el.getAttribute("for") === "t-" + t ? "true" : "false");
  });
  store("kz-theme", t);
  var cli = $("#cli");
  if (cli) { if (t === "terminal") cli.removeAttribute("hidden"); else cli.setAttribute("hidden", ""); }
  if (t === "terminal") {
    window.scrollTo(0, 0);
    bootCli();
    setTimeout(function () { var i = $("#cli-in"); if (i) i.focus(); }, 60);
  }
  syncURL();
}

/* ---------- lang ---------- */
function setLang(l) {
  if (l !== "en") l = "ru";
  root.dataset.lang = l;
  root.setAttribute("lang", l);
  document.title = TITLES[l];
  var m = document.querySelector('meta[name="description"]');
  if (m) m.setAttribute("content", DESCS[l]);
  var r = document.querySelector('input[name="lang"][value="' + l + '"]');
  if (r) r.checked = true;
  $$('label[for^="l-"]').forEach(function (el) {
    el.setAttribute("data-active", el.getAttribute("for") === "l-" + l ? "true" : "false");
  });
  store("kz-lang", l);
  syncURL();
  if (cliBooted && root.dataset.theme === "terminal") cliPrint("d", l === "ru" ? "— язык: русский" : "— language: english");
}

/* ---------- init from ?theme=&lang= → localStorage → default ---------- */
(function init() {
  var p = getParams();
  var y = $("#y");
  if (y) y.textContent = String(new Date().getFullYear());
  var jf = $("#js-flag");
  if (jf) jf.textContent = "js: on";
  setLang(p.get("lang") || read("kz-lang") || "ru");
  setTheme(p.get("theme") || read("kz-theme") || "deck");
})();

$$('input[name="theme"]').forEach(function (r) { r.addEventListener("change", function () { setTheme(r.value); }); });
$$('input[name="lang"]').forEach(function (r) { r.addEventListener("change", function () { setLang(r.value); }); });

/* keyboard: ` → terminal, Esc → deck */
document.addEventListener("keydown", function (e) {
  var tag = (e.target && e.target.tagName) || "";
  if (tag === "INPUT" || tag === "TEXTAREA") return;
  if (e.key === "`" || e.key === "ё" || e.key === "Ё") {
    e.preventDefault();
    setTheme(root.dataset.theme === "terminal" ? "deck" : "terminal");
  } else if (e.key === "Escape" && root.dataset.theme === "terminal") {
    setTheme("deck");
  }
});

/* ---------- typed ---------- */
(function typed() {
  var el = $("#typed");
  if (!el) return;
  var s = "> open_to_offer --role CDTO --domain fintech/retail/edu --effect P&L";
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) { el.textContent = s; return; }
  var i = 0;
  (function tick() { if (i <= s.length) { el.textContent = s.slice(0, i++); setTimeout(tick, 26); } })();
})();

/* ---------- count-up ---------- */
function countUp(b) {
  var target = parseFloat(b.dataset.count), dec = parseInt(b.dataset.dec || "0", 10);
  var l = lang();
  var suf = b.dataset["suffix" + (l === "ru" ? "Ru" : "En")] || b.dataset.suffix || "";
  if (isNaN(target)) return;
  var t0 = null, dur = 1200;
  function frame(ts) {
    if (!t0) t0 = ts;
    var p = Math.min((ts - t0) / dur, 1), e = 1 - Math.pow(1 - p, 3);
    var v = (target * e).toFixed(dec);
    if (l === "ru" && dec > 0) v = v.replace(".", ",");
    else if (dec === 0) v = String(Math.round(target * e));
    b.textContent = v + suf;
    if (p < 1) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}
(function observeCounts() {
  var els = $$("[data-count]");
  if (!els.length || !("IntersectionObserver" in window)) { els.forEach(countUp); return; }
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (en) { if (en.isIntersecting) { countUp(en.target); io.unobserve(en.target); } });
  }, { threshold: 0.4 });
  els.forEach(function (b) { io.observe(b); });
})();

/* ---------- reveal ---------- */
(function reveal() {
  root.classList.add("js");
  var els = $$(".reveal");
  if (!els.length || !("IntersectionObserver" in window)) { els.forEach(function (n) { n.classList.add("on"); }); return; }
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("on"); io.unobserve(en.target); } });
  }, { threshold: 0.1 });
  els.forEach(function (n) { io.observe(n); });
})();

/* ---------- hero particle field ---------- */
(function particleField() {
  var canvas = $("[data-particle-field]");
  if (!canvas || !canvas.getContext) return;
  var hero = canvas.parentNode, ctx = canvas.getContext("2d");
  if (!ctx) return;
  var width = 0, height = 0, dpr = 1, particles = [], frame = 0, visible = true;
  var resizeObserver = null, intersectionObserver = null, themeObserver = null;
  var color = { r: 140, g: 169, b: 199 };
  var motion = window.matchMedia("(prefers-reduced-motion: reduce)");
  var linkRange = 148;

  function readColor() {
    var value = window.getComputedStyle(root).getPropertyValue("--signal").trim();
    var match = value.match(/^#([0-9a-f]{6})$/i);
    if (!match) return;
    color = {
      r: parseInt(match[1].slice(0, 2), 16),
      g: parseInt(match[1].slice(2, 4), 16),
      b: parseInt(match[1].slice(4, 6), 16)
    };
  }

  function seed() {
    var count = Math.max(14, Math.min(48, Math.round(width * height / 15000)));
    particles = [];
    for (var i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.28,
        vy: (Math.random() - 0.5) * 0.28,
        r: 0.8 + Math.random() * 1.3,
        alpha: 0.35 + Math.random() * 0.35
      });
    }
    linkRange = Math.max(108, Math.min(158, width * 0.14));
  }

  function render(advance) {
    if (!width || !height) return;
    ctx.clearRect(0, 0, width, height);
    if (advance) {
      particles.forEach(function (p) {
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > width) p.vx *= -1;
        if (p.y < 0 || p.y > height) p.vy *= -1;
        p.x = Math.max(0, Math.min(width, p.x));
        p.y = Math.max(0, Math.min(height, p.y));
      });
    }
    for (var i = 0; i < particles.length; i++) {
      for (var j = i + 1; j < particles.length; j++) {
        var a = particles[i], b = particles[j];
        var dx = a.x - b.x, dy = a.y - b.y, distance = Math.sqrt(dx * dx + dy * dy);
        if (distance < linkRange) {
          var opacity = (1 - distance / linkRange) * 0.16;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y);
          ctx.strokeStyle = "rgba(" + color.r + "," + color.g + "," + color.b + "," + opacity.toFixed(3) + ")";
          ctx.lineWidth = 0.7;
          ctx.stroke();
        }
      }
    }
    particles.forEach(function (p) {
      ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(" + color.r + "," + color.g + "," + color.b + "," + p.alpha.toFixed(2) + ")";
      ctx.fill();
    });
  }

  function canAnimate() {
    return visible && !document.hidden && root.dataset.theme !== "terminal" && !motion.matches;
  }
  function stop() {
    if (frame) { cancelAnimationFrame(frame); frame = 0; }
  }
  function tick() {
    frame = 0;
    if (!canAnimate()) return;
    render(true);
    frame = requestAnimationFrame(tick);
  }
  function start() {
    if (!width || !height) return;
    if (motion.matches) { stop(); render(false); return; }
    if (!visible || document.hidden || root.dataset.theme === "terminal") { stop(); return; }
    if (!frame) frame = requestAnimationFrame(tick);
  }
  function resize() {
    var rect = hero.getBoundingClientRect();
    if (!rect.width || !rect.height) return;
    width = rect.width; height = rect.height;
    dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    canvas.width = Math.round(width * dpr);
    canvas.height = Math.round(height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    seed(); render(false); start();
  }
  function themeChanged() {
    readColor();
    if (root.dataset.theme === "terminal") stop();
    else resize();
  }
  function motionChanged() {
    stop();
    if (motion.matches) render(false);
    else start();
  }

  readColor();
  if ("ResizeObserver" in window) {
    resizeObserver = new ResizeObserver(resize);
    resizeObserver.observe(hero);
  } else window.addEventListener("resize", resize);
  if ("IntersectionObserver" in window) {
    intersectionObserver = new IntersectionObserver(function (entries) {
      visible = entries[0].isIntersecting;
      if (visible) start(); else stop();
    });
    intersectionObserver.observe(hero);
  }
  if ("MutationObserver" in window) {
    themeObserver = new MutationObserver(themeChanged);
    themeObserver.observe(root, { attributes: true, attributeFilter: ["data-theme"] });
  } else {
    $$('input[name="theme"]').forEach(function (input) { input.addEventListener("change", themeChanged); });
  }
  document.addEventListener("visibilitychange", function () { if (document.hidden) stop(); else start(); });
  if (motion.addEventListener) motion.addEventListener("change", motionChanged);
  else if (motion.addListener) motion.addListener(motionChanged);
  resize();
})();

/* ---------- copy ---------- */
function copyText(v, okMsg) {
  function done() { toast(okMsg); }
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(v).then(done, function () { fallback(); });
  } else { fallback(); }
  function fallback() {
    try {
      var ta = document.createElement("textarea");
      ta.value = v; ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      document.execCommand("copy"); document.body.removeChild(ta); done();
    } catch (e) { toast(v); }
  }
}
$$("[data-copy]").forEach(function (btn) {
  btn.addEventListener("click", function () {
    var v = btn.dataset.copy;
    copyText(v, (lang() === "ru" ? "скопировано: " : "copied: ") + v);
  });
});
$$("[data-employer-link]").forEach(function (btn) {
  btn.addEventListener("click", function () {
    var url;
    try {
      var u = new URL(location.href);
      u.searchParams.set("theme", root.dataset.theme === "terminal" ? "deck" : root.dataset.theme);
      u.searchParams.set("lang", lang());
      u.hash = "#top";
      url = u.toString();
    } catch (e) { url = location.href; }
    copyText(url, lang() === "ru" ? "ссылка скопирована — отправьте работодателю" : "link copied — send it to the employer");
  });
});
$$("[data-print]").forEach(function (btn) { btn.addEventListener("click", function () { window.print(); }); });

/* ================= CLI ================= */
var cliOut = $("#cli-out"), cliForm = $("#cli-form"), cliIn = $("#cli-in");
var hist = [], histI = 0;
function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
function cliPrint(cls, html) {
  if (!cliOut) return;
  var d = document.createElement("div");
  if (cls) d.className = cls;
  d.innerHTML = html;
  cliOut.appendChild(d);
  cliOut.scrollTop = cliOut.scrollHeight;
}
var LINKS = {
  telegram: "https://t.me/bestdeejay", github: "https://github.com/bestdeejay-design/resume",
  univerid: "https://univerid.ru", axiiom: "https://axiiom.ru",
  linkedin: "https://www.linkedin.com/in/bestdeejay", mobtop: "https://mobtop.ru",
  mail: "mailto:bestdeejay@ya.ru"
};
function linkLine(k, desc) { return '<span class="p">' + k + "</span>  " + desc + '  <a href="' + LINKS[k] + '">' + LINKS[k].replace("https://", "") + "</a>"; }

var CMD = {
  help: {
    ru: 'команды: <span class="a">whoami summary cases track ventures stack ai compliance proof hire project contact open lang theme clear exit</span>\nпример: <span class="p">cases</span> · <span class="p">open telegram</span> · <span class="p">theme brief</span> · <span class="p">lang en</span>',
    en: 'commands: <span class="a">whoami summary cases track ventures stack ai compliance proof hire project contact open lang theme clear exit</span>\ntry: <span class="p">cases</span> · <span class="p">open telegram</span> · <span class="p">theme brief</span> · <span class="p">lang ru</span>'
  },
  whoami: {
    ru: 'Сергей Кузюков · <span class="a">CDTO</span> (цель) / CTO / CPO · СПб\n17 лет 10 мес. в IT непрерывно, с 11.2008: разработчик → CEO/CTO/CPO\nфинтех с compliance · highload · AI · команды до 80',
    en: 'Sergey Kuzyukov · <span class="a">CDTO</span> (target) / CTO / CPO · Saint Petersburg\n17y 10m in IT continuous, since 11.2008: developer → CEO/CTO/CPO\nregulated fintech · highload · AI · teams up to 80'
  },
  summary: {
    ru: '<span class="a">EXEC:</span> legacy и регуляторика → выручка.\n· ИТ-Парк: 5→45, 500K+/30K+, −20% OPEX, ~1 млрд ₽/год\n· UniverID: 12 000+ студентов, демо за 2 месяца\n· Сбер: 3× проектное финансирование 2,8–4,1 млрд ₽ (2023–2025)\n· метод: ТЗ как контракт; слабые гипотезы закрываются быстро',
    en: '<span class="a">EXEC:</span> legacy & regulation → revenue.\n· IT-Park: 5→45, 500K+/30K+, −20% OPEX, ~₽1B/year\n· UniverID: 12,000+ students, demo in 2 months\n· Sberbank: 3× project finance ₽2.8–4.1B (2023–2025)\n· method: spec-as-contract; weak hypotheses die fast'
  },
  cases: {
    ru: '<span class="a">1. ИТ-Парк (2018–2024):</span> 5 разрабов → 45 + 8 менеджеров → 500K+/30K+, −20% OPEX, ~1 млрд ₽/год\n<span class="a">2. UniverID (2026):</span> бумага → 20 модулей, 6 ролей, AI-куратор → демо 12K+ за 2 мес\n<span class="a">3. Сбер (2023–2025):</span> архитектура + compliance + C-level → 3× 2,8–4,1 млрд ₽',
    en: '<span class="a">1. IT-Park (2018–2024):</span> 5 devs → 45 + 8 managers → 500K+/30K+, −20% OPEX, ~₽1B/year\n<span class="a">2. UniverID (2026):</span> paper → 20 modules, 6 roles, AI curator → 12K+ demo in 2 mo\n<span class="a">3. Sberbank (2023–2025):</span> architecture + compliance + C-level → 3× ₽2.8–4.1B'
  },
  track: {
    ru: '2024–now <span class="p">Axiiom</span> CEO/Architect · 2024–25 <span class="p">Bank</span> ABS/DBO · 2018–24 <span class="p">IT-Park</span> CEO\n2012–21 <span class="p">MOBIAP</span> CEO ∥ · 2016–17 <span class="p">Meevu CY</span> CTO · 2013–15 <span class="p">ZED</span> HoP 150K+\n2015 <span class="p">Ready4Sky</span> CMO · 2008–12 <span class="p">MOBIADS</span> → exit (Runet Prize nominee)',
    en: '2024–now <span class="p">Axiiom</span> CEO/Architect · 2024–25 <span class="p">Bank</span> core/digital · 2018–24 <span class="p">IT-Park</span> CEO\n2012–21 <span class="p">MOBIAP</span> CEO ∥ · 2016–17 <span class="p">Meevu CY</span> CTO · 2013–15 <span class="p">ZED</span> HoP 150K+\n2015 <span class="p">Ready4Sky</span> CMO · 2008–12 <span class="p">MOBIADS</span> → exit (Runet Prize nominee)'
  },
  ventures: {
    ru: '<span class="a">LOVII</span> (09.2025–now): white-label маркетплейсы, Т-Банк подключён, мини-пилот ОК.\nстатус: <span class="a">предрелиз, транзакций нет</span> — честно, отдельный P&L.\n<span class="a">CPA-сеть</span> (2024): гипотеза закрыта, задел переиспользован.',
    en: '<span class="a">LOVII</span> (09.2025–now): white-label marketplaces, T-Bank live, mini-pilot OK.\nstatus: <span class="a">pre-release, no transactions yet</span> — honestly, separate P&L.\n<span class="a">CPA network</span> (2024): invalidated fast, assets reused.'
  },
  stack: {
    ru: 'arch: микросервисы · event-driven · Kafka · K8s · PostgreSQL · Go/Node/Python\ninfra: Linux KVM · Linstor · cloud · CI/CD · мониторинг · 3-контурная ИБ (RBAC/LDAP/Harbor)\ncompliance: БПА · ЦБ · 161/115/54/152-ФЗ · СБП · ККТ/ОФД · УКЭП · ФНС(НПД) · 1С',
    en: 'arch: microservices · event-driven · Kafka · K8s · PostgreSQL · Go/Node/Python\ninfra: Linux KVM · Linstor · cloud · CI/CD · monitoring · 3-zone security (RBAC/LDAP/Harbor)\ncompliance: BPA · Central Bank · 161/115/54/152-FZ · SBP · fiscal · e-sign · 1C'
  },
  ai: {
    ru: '· agent-skills: 59 скиллов, v1.0, прод — автор\n· PMOS: 17 сервисов, AI OpenAPI, 89+168 тестов — архитектор\n· RAG с цитированием (zero-infra) · Whisper+RAG без платных ключей\n· handbook 108 глав EN+RU · 200+ LLM проверено · 2 MCP · GITVERSE 91 репо',
    en: '· agent-skills: 59 skills, v1.0, prod — author\n· PMOS: 17 services, AI OpenAPI, 89+168 tests — architect\n· cited RAG (zero-infra) · Whisper+RAG, zero paid keys\n· 108-ch handbook EN+RU · 200+ LLMs verified · 2 MCP servers · GITVERSE 91 repos'
  },
  compliance: {
    ru: 'БПА — легальные финпотоки · ЦБ/Росфинмониторинг — согласования\n161-ФЗ платежи · 115-ФЗ AML/CFT · 54-ФЗ фискализация · 152-ФЗ ПДн\nСБП/QR · ФНС НПД · эквайринг Т-Банк · УКЭП/КЭП',
    en: 'BPA — legal money flows · Central Bank approvals\n161-FZ payments · 115-FZ AML/CFT · 54-FZ fiscal · 152-FZ data privacy\nSBP/QR · NPD tax · T-Bank acquiring · e-signature'
  },
  proof: { ru: "__LINKS__", en: "__LINKS__" },
  hire: {
    ru: '<span class="a">Трек 1 — найм:</span> CDTO/CTO/CPO · полная занятость · гибрид/удалённо/офис\nпереезд внутри РФ · интро 20 мин + 1-page PDF · решение за недели\n→ <span class="p">open mail-hire</span> · <span class="p">open telegram</span>',
    en: '<span class="a">Track 1 — employment:</span> CDTO/CTO/CPO · full-time · hybrid/remote/on-site\nrelocation within Russia · 20-min intro + 1-page PDF · decision in weeks\n→ <span class="p">open mail-hire</span> · <span class="p">open telegram</span>'
  },
  project: {
    ru: '<span class="a">Трек 2 — проект:</span> команда Axiiom · аудиты с планом · MVP zero-to-one\nБПА/ЦБ · Реестр ПО 65 раб. дней · SOW+NDA · приёмка по документу\n→ <span class="p">open mail-project</span> · <span class="p">open telegram</span>',
    en: '<span class="a">Track 2 — project:</span> Axiiom team · audits with plan · zero-to-one MVP\nBPA/CB · SW Register 65 workdays · SOW+NDA · spec acceptance\n→ <span class="p">open mail-project</span> · <span class="p">open telegram</span>'
  },
  contact: {
    ru: 'telegram: <a href="https://t.me/bestdeejay">t.me/bestdeejay</a> (primary, отвечаю за день)\nтел: +7 (911) 928-74-78 · mail: bestdeejay@ya.ru · <a href="https://www.linkedin.com/in/bestdeejay">linkedin</a>\nусловия: от 400 000 ₽ на руки · обсуждаются · СПб · GMT+3',
    en: 'telegram: <a href="https://t.me/bestdeejay">t.me/bestdeejay</a> (primary, replies in a day)\nphone: +7 (911) 928-74-78 · mail: bestdeejay@ya.ru · <a href="https://www.linkedin.com/in/bestdeejay">linkedin</a>\nterms: from ₽400K net · negotiable · Saint Petersburg · GMT+3'
  }
};
LINKS["mail-hire"] = "mailto:bestdeejay@ya.ru?subject=CDTO%2FCTO%20%E2%80%94%20intro%20(employment)";
LINKS["mail-project"] = "mailto:bestdeejay@ya.ru?subject=Project%20with%20Axiiom%20%E2%80%94%20scope";

function bootCli() {
  if (cliBooted || !cliOut) return;
  cliBooted = true;
  var fb = $("#cli-fallback");
  if (fb && fb.parentNode) fb.parentNode.removeChild(fb);
  var l = lang();
  cliPrint("d", l === "ru"
    ? "kuzyukov-cli v1.0 · факты из MASTER от 28.09.2026 · ничего не выдумано"
    : "kuzyukov-cli v1.0 · facts from MASTER of 28.09.2026 · nothing invented");
  cliPrint("", CMD.help[l]);
}

function runCmd(raw) {
  var l = lang();
  var parts = raw.trim().split(/\s+/);
  var c = (parts[0] || "").toLowerCase(), arg = (parts[1] || "").toLowerCase();
  if (!c) return;
  if (c === "clear") { cliOut.innerHTML = ""; return; }
  if (c === "exit") { setTheme("deck"); toast(l === "ru" ? "режим Deck" : "Deck mode"); return; }
  if (c === "sudo") { cliPrint("a", l === "ru" ? "дерзко. напишите мне в telegram — договоримся." : "bold. text me on telegram — we will talk."); return; }
  if (c === "echo") { cliPrint("", esc(parts.slice(1).join(" "))); return; }
  if (c === "theme") {
    if (THEMES.indexOf(arg) >= 0) { setTheme(arg); if (arg !== "terminal") toast("theme: " + arg); }
    else cliPrint("a", "usage: theme deck|brief|terminal");
    return;
  }
  if (c === "lang") {
    if (arg === "ru" || arg === "en") setLang(arg);
    else cliPrint("a", "usage: lang ru|en");
    return;
  }
  if (c === "open") {
    if (LINKS[arg]) {
      cliPrint("", '<span class="g">opening</span> ' + esc(LINKS[arg]));
      try { window.open(LINKS[arg], "_blank", "noopener"); } catch (e) {}
    } else cliPrint("a", "usage: open " + Object.keys(LINKS).join("|"));
    return;
  }
  if (c === "proof") {
    ["univerid", "axiiom", "github", "linkedin", "mobtop", "telegram"].forEach(function (k) {
      var d = { univerid: "univ portal", axiiom: "AI handbook", github: "resume as code", linkedin: "profile", mobtop: "Runet nominee", telegram: "direct" }[k];
      cliPrint("", linkLine(k, '<span class="d">' + d + "</span>"));
    });
    return;
  }
  if (CMD[c]) { cliPrint("", CMD[c][l]); return; }
  cliPrint("a", (l === "ru" ? "не знаю «" : "unknown command «") + esc(c) + (l === "ru" ? "». введите help" : "». type help"));
}

if (cliForm && cliIn) {
  cliForm.addEventListener("submit", function (e) {
    e.preventDefault();
    var v = cliIn.value;
    cliPrint("", '<span class="p">kuzyukov@cdto:~$</span> ' + esc(v));
    hist.push(v); histI = hist.length;
    cliIn.value = "";
    runCmd(v);
  });
  cliIn.addEventListener("keydown", function (e) {
    if (e.key === "ArrowUp") { e.preventDefault(); if (histI > 0) { histI--; cliIn.value = hist[histI] || ""; } }
    else if (e.key === "ArrowDown") { e.preventDefault(); if (histI < hist.length) { histI++; cliIn.value = hist[histI] || ""; } }
  });
}

/* deep-link ?theme=terminal: init ran before CLI refs existed — boot now */
if (root.dataset.theme === "terminal") bootCli();

/* console egg */
console.log("%c kuzyukov --help %c facts from MASTER, 0 invented ",
  "background:#F2F5F8;color:#071019;font-weight:bold", "color:#8CA9C7");
})();
