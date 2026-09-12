#!/usr/bin/env python3
"""
AXIIOM — Генерация отраслевых лендингов v3 — максимально конверсионная, анти-дорвей
30 страниц, каждая уникальна:
- категория-бейдж + share
- hero с ценой-якорем MVP от / сроки, 2 CTA с ?industry=slug
- траст 50+ проектов / 99.99% / 161-ФЗ
- уникальные SVG-иконки по категории в hero
- блок автора/даты (E-E-A-T)
- боли 3 карточки уникальные
- модули 10, flow, стек, интеграции
- proof: логотипы клиентов + скриншот-заглушка
- кейсы 2 с цифрами + ссылки на портфолио/демо
- FAQ 5 вопросов под поисковые запросы + FAQPage JSON-LD
- related 3
- sticky CTA (появляется после 600px)
- CTA с калькулятором
- JSON-LD: WebPage + BreadcrumbList + Service(Offer) + FAQPage
"""

from string import Template
from datetime import datetime

CATEGORY_MAP = {
    'avtomatizaciya-restoranov': 'HoReCa & Retail',
    'dostavka-edy': 'HoReCa & Retail',
    'fitness-apps': 'HoReCa & Retail',
    'bronirovanie-gostinits': 'HoReCa & Retail',
    'kiberbezopasnost': 'Security & Fintech',
    'kyc-onboarding': 'Fintech',
    'multi-currency-wallet': 'Fintech',
    'p2p-marketplace': 'Fintech',
    'trading-engine': 'Fintech',
    'investment-crm': 'Fintech',
    'real-time-analytics': 'Fintech',
    'asset-tokenization': 'Fintech',
    'kraudfanding': 'Fintech',
    'crm-medcentry': 'B2B & Enterprise',
    'crm-nedvizhimost': 'B2B & Enterprise',
    'po-stroitelnye-kompanii': 'B2B & Enterprise',
    'erp-proizvodstvo': 'B2B & Enterprise',
    'sistemy-logistika': 'B2B & Enterprise',
    'upravlenie-cepochkami': 'B2B & Enterprise',
    'pravovie-firmu': 'B2B & Enterprise',
    'avtoservice': 'B2B & Enterprise',
    'hr-podbor-personala': 'B2B & Enterprise',
    'selskokhozyaystvo': 'B2B & Enterprise',
    'saas-startupy': 'SaaS & Digital',
    'online-obuchenie': 'SaaS & Digital',
    'platforma-frilans': 'SaaS & Digital',
    'iot-umnyy-dom': 'SaaS & Digital',
    'marketing-analitika': 'SaaS & Digital',
    'upravlenie-proektami': 'SaaS & Digital',
    'udalennaya-rabota': 'SaaS & Digital',
}

CATEGORY_ICONS = {
    'Fintech': '<svg width="400" height="400" viewBox="0 0 400 400" fill="none"><rect x="100" y="80" width="200" height="140" rx="16" stroke="currentColor" stroke-width="2" opacity=".15"/><rect x="120" y="100" width="60" height="12" rx="6" fill="currentColor" opacity=".12"/><rect x="120" y="130" width="100" height="8" rx="4" fill="currentColor" opacity=".08"/><circle cx="260" cy="140" r="24" stroke="currentColor" stroke-width="2" opacity=".15"/><path d="M250 140 L255 145 L270 130" stroke="currentColor" stroke-width="2" opacity=".15"/><rect x="140" y="260" width="120" height="80" rx="12" stroke="currentColor" stroke-width="2" opacity=".1"/><path d="M160 280 h80 M160 300 h60" stroke="currentColor" stroke-width="2" opacity=".1"/></svg>',
    'HoReCa & Retail': '<svg width="400" height="400" viewBox="0 0 400 400" fill="none"><circle cx="200" cy="180" r="80" stroke="currentColor" stroke-width="2" opacity=".12"/><path d="M160 160 L200 120 L240 160 L200 240 Z" stroke="currentColor" stroke-width="2" opacity=".12"/><rect x="140" y="260" width="120" height="60" rx="12" stroke="currentColor" stroke-width="2" opacity=".1"/><circle cx="170" cy="290" r="8" fill="currentColor" opacity=".1"/><circle cx="230" cy="290" r="8" fill="currentColor" opacity=".1"/></svg>',
    'B2B & Enterprise': '<svg width="400" height="400" viewBox="0 0 400 400" fill="none"><rect x="80" y="80" width="240" height="160" rx="12" stroke="currentColor" stroke-width="2" opacity=".12"/><line x1="80" y1="120" x2="320" y2="120" stroke="currentColor" stroke-width="2" opacity=".08"/><rect x="100" y="140" width="60" height="60" rx="8" stroke="currentColor" stroke-width="2" opacity=".1"/><rect x="180" y="140" width="60" height="60" rx="8" stroke="currentColor" stroke-width="2" opacity=".1"/><rect x="100" y="260" width="200" height="40" rx="8" stroke="currentColor" stroke-width="2" opacity=".08"/></svg>',
    'SaaS & Digital': '<svg width="400" height="400" viewBox="0 0 400 400" fill="none"><rect x="80" y="100" width="240" height="160" rx="16" stroke="currentColor" stroke-width="2" opacity=".12"/><circle cx="120" cy="130" r="6" fill="currentColor" opacity=".15"/><circle cx="140" cy="130" r="6" fill="currentColor" opacity=".12"/><circle cx="160" cy="130" r="6" fill="currentColor" opacity=".09"/><path d="M100 160 L300 160 M100 180 L250 180 M100 200 L280 200" stroke="currentColor" stroke-width="2" opacity=".08"/><rect x="120" y="280" width="160" height="60" rx="30" stroke="currentColor" stroke-width="2" opacity=".1"/></svg>',
    'Security & Fintech': '<svg width="400" height="400" viewBox="0 0 400 400" fill="none"><path d="M200 60 L300 100 L300 200 C300 260 250 310 200 340 C150 310 100 260 100 200 L100 100 Z" stroke="currentColor" stroke-width="2" opacity=".12"/><circle cx="200" cy="190" r="40" stroke="currentColor" stroke-width="2" opacity=".12"/><path d="M180 190 L195 205 L220 175" stroke="currentColor" stroke-width="2" opacity=".15"/></svg>',
}

PRICE_MAP = {
    'Fintech': ('от 2 млн ₽', '3 месяца', 'Discovery бесплатно'),
    'HoReCa & Retail': ('от 400к ₽', '6 недель', 'Аудит процессов бесплатно'),
    'B2B & Enterprise': ('от 800к ₽', '2 месяца', 'Аудит и ТЗ бесплатно'),
    'SaaS & Digital': ('от 600к ₽', '2 месяца', 'Консультация бесплатно'),
    'Security & Fintech': ('от 500к ₽', '1 месяц', 'Аудит безопасности бесплатно'),
}

PROBLEMS = {
    'avtomatizaciya-restoranov': [("Заказы теряются между агрегаторами и кухней", "Решение: единое окно POS + CRM, все каналы в одном месте, печать чек-листов и KDS."),("Нет данных о гостях и LTV", "Решение: CRM с историей, сегментация, персональные предложения и кэшбэк LOVII."),("Кухня не успевает в пик", "Решение: KDS, тайминг блюд, тепловая карта загрузки, стоп-лист в реальном времени.")],
    'dostavka-edy': [("Курьеры опаздывают, клиент не видит статус", "Решение: трекинг в реальном времени, маршрутизация с учётом пробок, push-статусы."),("Заказы из разных источников не сводятся", "Решение: единый диспетчер — сайт, приложение, агрегаторы в одном окне."),("Нет аналитики по районам и курьерам", "Решение: дашборды по времени доставки, марже, конверсии, тепловой карте спроса.")],
    'fitness-apps': [("Низкая вовлечённость после первой недели", "Решение: геймификация, челленджи, уровни, push-триггеры и социальная лента."),("Нет персонализации", "Решение: AI-планы под цель — похудение, масса, выносливость, интеграция с wearables."),("Сложно монетизировать", "Решение: подписки, продажа программ, партнёрки с брендами питания и экипировки.")],
    'bronirovanie-gostinits': [("Простой номеров из-за ручного управления каналами", "Решение: Channel Manager — синхрон цен и наличия с Booking, Airbnb, Ostrovok в реальном времени."),("Нет динамического ценообразования", "Решение: Dynamic Pricing по загрузке, сезону, событиям — рост RevPAR на 18%."),("Теряете постоянных гостей", "Решение: CRM с историей, днём рождения, персональными предложениями и рассылками.")],
    'kiberbezopasnost': [("Нет видимости угроз", "Решение: SIEM, EDR, корреляция событий, real-time алерты и расследование инцидентов."),("Сотрудники кликают на фишинг", "Решение: обучение с фишинговыми симуляциями, тестами и сертификацией."),("Не проходите аудит 152-ФЗ/PCI DSS", "Решение: шифрование, DLP, backup 3-2-1, VPN с MFA, готовим к сертификации.")],
    'kyc-onboarding': [("Банк отказывает в интеграции из-за 161-ФЗ", "Решение: проходим аудит, готовим документы, есть опыт с 3 банками и PCI DSS."),("Высокий фрод и ручная проверка", "Решение: скоринг, биометрия, liveness, проверка по санкционным базам, ML."),("Длинный онбординг, отток 60%", "Решение: сокращаем до 2 минут, UX-тесты, автозаполнение, подсказки по камере.")],
    'multi-currency-wallet': [("Мультивалютность и потери на конвертации", "Решение: мульти-кошелёк с холдированием курса, сплит, escrow, netting."),("Нет PCI DSS и токенизации", "Решение: Vault, токенизация карт, подготовка к сертификации, KMS."),("Нет SBP/QR/NFC", "Решение: подключаем SBP, QR, NFC, Apple/Google Pay за 2 недели, 3D Secure.")],
    'p2p-marketplace': [("Нет доверия между сторонами", "Решение: escrow, рейтинги, KYC, модерация, арбитраж с доказательствами."),("Сложный сплит и комиссии", "Решение: гибкий сплит, холдирование, мультиэквайринг, автовыплаты."),("Падает в пик торгов", "Решение: микросервисы, Kafka, Kubernetes, 99.99% uptime, горизонтальное масштабирование.")],
    'trading-engine': [("Задержки и проскальзывания", "Решение: low-latency engine на Go, 100k+ RPS, in-memory orderbook, FIX API."),("Нет KYC/AML и логов для регулятора", "Решение: KYC, AML, 161-ФЗ, неизменяемый аудит-лог, отчёты."),("Нет интеграции с банками/ликвидностью", "Решение: банковские шлюзы, криптобиржи, провайдеры ликвидности.")],
    'investment-crm': [("Лиды теряются, нет воронки", "Решение: CRM с воронкой, автоназначение, напоминания, интеграция с сайтом и телефонией."),("Нет онбординга инвестора", "Решение: KYC, скоринг, личные кабинеты, портфель, документы и ЭДО."),("Нет аналитики по менеджерам", "Решение: дашборды — конверсия, средний чек, LTV, источники лидов.")],
    'real-time-analytics': [("Отчёты строятся часами", "Решение: ClickHouse, Kafka, real-time витрины, дашборды за секунды."),("Данные разрознены", "Решение: ETL из CRM, сайта, рекламы, 1С в единое хранилище."),("Нет прогноза", "Решение: ML-прогноз спроса, аномалий, оттока, рекомендации по бюджету.")],
    'asset-tokenization': [("Нет юридической обвязки токенов", "Решение: проспект, KYC, реестр, ЭДО, интеграция с депозитарием."),("Сложный выпуск и учёт", "Решение: движок токенизации, смарт-контракты, кошелёк, вторичный рынок."),("Нет доверия инвесторов", "Решение: аудит смарт-контрактов, escrow, прозрачные отчёты и дашборды.")],
    'kraudfanding': [("Низкая конверсия кампаний", "Решение: визуальный редактор, видео, stretch-goals, соцдоказательства."),("Нет платежей и возвратов", "Решение: эквайринг, SBP, PayPal, crypto, pledge-менеджмент и автовозвраты."),("Нет модерации", "Решение: верификация авторов, антифрод, правила, ручная модерация.")],
    'crm-medcentry': [("Пациенты не доходят, забывают", "Решение: онлайн-запись, напоминания SMS/push, лист ожидания, телемедицина."),("Нет ЕМК и интеграции с лабораториями", "Решение: ЕМК с МКБ-10, интеграция с KDL, Invitro, Гемотест, ЛИС."),("Нет аналитики загрузки врачей", "Решение: дашборды — загрузка, выручка по услугам, конверсия, отток.")],
    'crm-nedvizhimost': [("Объекты устаревают, цены неактуальны", "Решение: автообновление из ЦИАН/Авито/ДомКлик, парсинг, уведомления."),("Сделки ведут в Excel", "Решение: воронка, документы, ЭЦП, ДКП, проверка ЕГРН и обременений."),("Нет ипотеки", "Решение: калькулятор, ставки банков-партнёров, онлайн-заявка на одобрение.")],
    'po-stroitelnye-kompanii': [("Сметы не сходятся с фактом", "Решение: сметное ПО, ресурсный метод, актуализация цен, план-факт."),("Нет BIM и исполнительной", "Решение: интеграция Revit/ArchiCAD, исполнительная, фотофиксация."),("Подрядчики срывают сроки", "Решение: графики Ганта, наряды-допуски, табели, контроль качества.")],
    'erp-proizvodstvo': [("Нет планирования MRP", "Решение: MRP по заказам, прогноз спроса, графики, загрузка цехов."),("Нет учёта себестоимости", "Решение: плановая/фактическая себестоимость, распределение расходов, дашборды."),("Станки не интегрированы", "Решение: MES, OPC UA, диспетчеризация, маршрутные карты.")],
    'sistemy-logistika': [("Заявки теряются, нет трекинга", "Решение: CRM, личный кабинет, GPS-трекинг, ЭДО, мобильное приложение водителя."),("Маршруты неоптимальны", "Решение: оптимизация с учётом пробок, габаритов, времени, геозоны."),("Нет таможни", "Решение: декларации, ТН ВЭД, интеграция с ФТС и брокерами.")],
    'upravlenie-cepochkami': [("Запасы то избыточны, то дефицит", "Решение: прогнозирование спроса ML, WMS, RFQ, ABC-анализ."),("Нет видимости цепочки", "Решение: OTIF, сквозные KPI, дашборды для директора по логистике."),("Поставщики срывают", "Решение: реестр с рейтингом, аудиты, план B для критичных позиций.")],
    'pravovie-firmu': [("Сроки горят, дела теряются", "Решение: электронные карточки, авто-расчёт процессуальных сроков, календарь."),("Нет биллинга по часам", "Решение: тайм-трекинг, инвойсы, контроль дебиторки."),("Нет интеграции с судами", "Решение: ГАС Правосудие, картотека арбитража, импорт определений.")],
    'avtoservice': [("Запись в тетради, клиенты не возвращаются", "Решение: онлайн-запись, история по VIN, напоминания о ТО, кэшбэк."),("Нет учёта запчастей", "Решение: склад, автозаказ при min, учёт шин на хранении."),("Нет работы со страховыми", "Решение: заявки, фото до/после, расчёт по нормативам, ЭЦП.")],
    'hr-podbor-personala': [("Резюме в почте, нет базы", "Решение: парсинг с HH/SuperJob/LinkedIn, нормализация, дедупликация, семантический поиск."),("Долгий найм", "Решение: ATS-воронка, автопостинг вакансий, AI-скрининг, календарь интервью."),("Нет аналитики найма", "Решение: стоимость найма, время закрытия, конверсия, источники, retention.")],
    'selskokhozyaystvo': [("Нет карт полей и истории", "Решение: цифровые карты, севооборот, история обработок, урожайность."),("Техника не контролируется", "Решение: GPS, расход топлива, ТО, маршруты."),("Отчётность для Минсельхоза вручную", "Решение: шаблоны 1-СХ, 2-СХ, гранты, субсидии, агрострахование.")],
    'saas-startupy': [("Архитектура не держит рост", "Решение: мультитенантность, микросервисы, Kubernetes, автоскейлинг."),("Нет биллинга", "Решение: подписки, usage-based, купоны, dunning, инвойсы."),("Нет API для клиентов", "Решение: REST/GraphQL/Webhooks, OpenAPI, SDK.")],
    'online-obuchenie': [("Студенты бросают курсы", "Решение: геймификация, баллы, уровни, push-напоминания, мобильное приложение."),("Нет проверки домашки", "Решение: автопроверка тестов, ручная проверка с комментариями, сертификаты с QR."),("Нет вебинаров", "Решение: встроенная видеоконференция на 1000+, чат, опросы, запись.")],
    'platforma-frilans': [("Нет доверия и безопасных сделок", "Решение: escrow, верификация, рейтинги, арбитраж с доказательствами."),("Выплаты вручную", "Решение: автовыплаты на карты/кошельки/crypto, удержание комиссии и налогов."),("Нет поиска", "Решение: умный поиск с фильтрами, ML-рекомендации, чаты.")],
    'iot-umnyy-dom': [("Устройства не дружат", "Решение: Zigbee, Z-Wave, Wi-Fi, BLE, 50+ брендов — Xiaomi, Aqara, Hue."),("Нет сценариев", "Решение: if-this-then-that, геолокация, голос — Алиса, Маруся, Siri."),("Высокое потребление", "Решение: мониторинг энергии, рекомендации, авто-оптимизация графиков.")],
    'marketing-analitika': [("Данные в разных кабинетах", "Решение: ETL из CRM, сайта, соцсетей, рекламы в единое хранилище."),("Нет атрибуции", "Решение: multi-touch, ROI, CAC/LTV, воронки, когорты."),("Отчёты вручную", "Решение: real-time дашборды, автопочта PDF, тепловые карты, A/B тесты.")],
    'upravlenie-proektami': [("Сроки срываются", "Решение: Гант, критический путь, ресурсы, риски, портфель проектов."),("Нет учёта времени", "Решение: таймер, план/факт, EAC/ETC, отчёты для заказчика."),("Нет Agile", "Решение: Scrum/Kanban, WIP-лимиты, velocity, интеграции с CRM.")],
    'udalennaya-rabota': [("Нет контроля продуктивности", "Решение: трекер, тайм-трекинг, дашборды загрузки, выгорания."),("Небезопасный доступ", "Решение: VPN с MFA, SSO, ZTNA, шифрование, аудит."),("Звонки в Zoom без фиксации", "Решение: встроенные видеоконференции, транскрипция, задачи из встреч.")],
}
DEFAULT_PROBLEMS = [("Разработчики обещали, но проект застрял", "Решение: фиксируем scope, бюджет и сроки на Discovery, спринты по 2 недели с демо."),("Нет интеграции с нужными сервисами", "Решение: делаем API-first, есть опыт с банками, 1С, iiko, СДЭК, Яндекс."),("Сервис падает в пиковые нагрузки", "Решение: highload-архитектура, Kubernetes, горизонтальное масштабирование, 99.99%.")]

TECH_STACK = {
    'Fintech': {'Backend': 'Go, PHP, Node.js, Python, PostgreSQL, Redis, Kafka, ClickHouse','Frontend': 'React, Next.js, TypeScript, Tailwind','Mobile': 'Swift, Kotlin, NFC/QR/SBP, 3D Secure, Biometry','Infra': 'Kubernetes, Vault, PCI DSS, 161-ФЗ, 152-ФЗ, HSM'},
    'HoReCa & Retail': {'Backend': 'Node.js, PHP, Python, PostgreSQL, Redis','Frontend': 'React, Vue, Next.js, PWA','Mobile': 'React Native, Flutter, Push, QR, SBP','Infra': 'Docker, Yandex Cloud, 54-ФЗ, iiko/r_keeper API'},
    'B2B & Enterprise': {'Backend': 'Go, PHP, Python, 1C API, PostgreSQL, Redis','Frontend': 'React, Vue, TypeScript','Mobile': 'React Native, Flutter','Infra': 'Kubernetes, Docker, ЭДО, BIM, WMS, OPC UA'},
    'SaaS & Digital': {'Backend': 'Node.js, Go, Python, PostgreSQL, Redis, Kafka, ClickHouse','Frontend': 'React, Next.js, Vue, Tailwind','Mobile': 'React Native, Flutter, PWA','Infra': 'Kubernetes, Yandex Cloud, Terraform, S3, CDN'},
    'Security & Fintech': {'Backend': 'Go, Python, Vault, SonarQube, SAST/DAST, EDR','Frontend': 'React, TypeScript','Mobile': 'Kotlin, Swift, Biometry, Root detection','Infra': 'WAF, SIEM, PCI DSS, 152-ФЗ, 161-ФЗ, 3-2-1 Backup'},
}
INTEGRATIONS = {
    'Fintech': ['Сбербанк', 'Альфа-Банк', 'Тинькофф', 'ЮMoney', 'SBP', 'PCI DSS', '161-ФЗ', 'SumSub'],
    'HoReCa & Retail': ['iiko', 'r_keeper', 'Яндекс.Еда', 'СДЭК', '1С', '54-ФЗ', 'LOVII'],
    'B2B & Enterprise': ['1С', 'BIM (Revit)', 'WMS', 'СДЭК', 'ЭДО', 'Диадок', 'OPC UA'],
    'SaaS & Digital': ['Stripe', 'Yandex Cloud', 'S3', 'Kafka', 'Elasticsearch', 'Telegram', 'Amplitude'],
    'Security & Fintech': ['Vault', 'SonarQube', 'WAF', 'PCI DSS', '152-ФЗ', '161-ФЗ', 'EDR'],
}

# FAQ под поисковые запросы (5 вопросов)
FAQ_MAP = {
    'kyc-onboarding': [
        ("Сколько стоит KYC под ключ по 161-ФЗ?", "MVP от 2 млн ₽, полный цикл с биометрией и AML — от 4 млн ₽. Входит: eKYC, liveness, санкционные списки, аудит-лог, интеграция с 3 банками. Discovery бесплатно."),
        ("Проходите ли аудит 161-ФЗ и 152-ФЗ?", "Да, готовим пакет документов, шифрование, KMS, аудит-лог, DLP. Есть опыт с 3 банками, чек-лист для ЦБ."),
        ("Сколько занимает онбординг пользователя?", "Цель — 2 минуты: документ → селфи → liveness → решение. Без ручной проверки, автозаполнение, подсказки по камере."),
        ("SumSub vs самописный KYC — что выбрать?", "SumSub — быстро, но дорого и данные за рубежом. Самописный — контроль, хранение в РФ, кастомизация под 161-ФЗ, дешевле на масштабе."),
        ("Какой стек используете?", "Go/Python + React, Vault/HSM, Kafka, Postgres, ClickHouse. Разворачиваем в Yandex Cloud или on-premise."),
    ],
    'trading-engine': [
        ("Сколько стоит разработка криптобиржи / трейдинг-платформы?", "MVP от 3 млн ₽, биржа с кошельками и KYC — от 7 млн ₽. Matching engine на Go, 100k RPS, FIX API, листинги."),
        ("Какая задержка у matching engine?", "In-memory orderbook на Go, <10ms на матч, 100k+ RPS, WebSocket + FIX. Нагрузочные тесты Grafana."),
        ("Как с ликвидностью и банками?", "Подключаем провайдеров ликвидности, криптобиржи, банковские шлюзы, SBP, эквайринг. Агрегация стакана."),
        ("Есть ли KYC/AML и отчёты для регулятора?", "Да, KYC, AML, 161-ФЗ, аудит-лог, отчёты, лимиты, риск-контроль."),
        ("Даёте демо?", "Да, sandbox с ордербуком, API-доки OpenAPI, нагрузочные отчёты за 24 часа."),
    ],
    'multi-currency-wallet': [
        ("Разработка мультивалютного кошелька — цена?", "MVP от 2 млн ₽, с SBP/QR/NFC/PCI DSS — от 4 млн ₽. Мультивалютные счета, холдирование курса, escrow."),
        ("Поддерживаете SBP, QR, NFC, Apple Pay?", "Да, SBP, QR, NFC, Apple/Google Pay, 3D Secure 2.0, токенизация через Vault/HSM."),
        ("Как с PCI DSS и 161-ФЗ?", "Токенизация, HSM, KMS, аудит-лог, готовим к сертификации, чек-лист ЦБ."),
        ("Можно escrow и сплит?", "Да, escrow, сплит, netting, холдирование, автовыплаты, мультиэквайринг."),
        ("Есть ли мобильное приложение?", "Да, iOS/Android, Face ID, QR-сканер, push, офлайн-баланс, виджеты."),
    ],
    'avtomatizaciya-restoranov': [
        ("Сколько стоит автоматизация ресторана / кафе?", "MVP от 400к ₽, полный цикл с CRM, KDS, приложением — от 1.2 млн ₽. Запуск 6–8 недель, iiko/r_keeper."),
        ("Интегрируетесь с iiko, r_keeper, Яндекс.Еда?", "Да, готовые коннекторы: iiko, r_keeper, Яндекс.Еда, Delivery Club, СДЭК, 1С, LOVII лояльность."),
        ("Делаете приложение для гостей?", "Да, бронирование столиков, меню, кэшбэк, push, QR-оплата, отзывы, чат с админом."),
        ("Как с 54-ФЗ и кассами?", "Подключаем любые кассы, 54-ФЗ, эквайринг, ОФД, печать чеков, маркировка."),
        ("Что с аналитикой?", "Дашборды: выручка, прибыль блюд, загрузка зала, LTV, конверсия, отчёты для ФНС."),
    ],
}

DEFAULT_FAQ = [
    ("Сколько стоит разработка?", "MVP — от 2 млн ₽ для финтеха, от 400к ₽ для HoReCa. Точная смета после бесплатной Discovery 1–2 недели. Есть калькулятор /calculator/?industry=${slug}"),
    ("Какие сроки запуска?", "Discovery 1–2 недели, MVP 2–4 месяца, релиз с SLA 24/7, мониторинг, алерты в Telegram."),
    ("Даёте демо и архитектурную схему?", "Да, sandbox, схема архитектуры, смета за 24 часа. Портфолио /projects/ и демо /demo/app/ — смотрите."),
    ("Как с интеграциями — банки, 1С, iiko, СДЭК?", "API-first, готовые коннекторы: Сбер, Альфа, Тинькофф, SBP, 1С, iiko/r_keeper, СДЭК, Яндекс.Еда."),
    ("Это не дорвей? Уникальный ли контент?", "Нет. Каждая страница — уникальный лендинг с болями, модулями, стеком, кейсами, FAQ, авторством. 50+ проектов, 99.99% uptime."),
]

MODULES_TMPL = Template('''
<section class="section">
<div class="container">
<p class="label reveal">Модули</p>
<h2 class="reveal">Что входит в решение</h2>
<div class="tools-grid">
${items}
</div>
</div>
</section>''')
MODULE_ITEM = '''
<div class="card reveal">
<div class="card-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 6L9 17l-5-5"/></svg></div>
<h3>${name}</h3>
<p>${desc}</p>
</div>'''
CTA_TMPL = Template('''
<section class="section cta-section">
<div class="container">
<div class="glass-card cta-card reveal">
<h2>${title}</h2>
<p>${text}</p>
<div class="cta-contacts">
<a href="/#contact" class="btn">Обсудить проект</a>
<a href="/calculator/?industry=${slug}" class="btn btn-outline">Рассчитать в калькуляторе</a>
</div>
<p style="margin-top:16px;font-size:.85rem;color:var(--clr-muted)">Или посмотрите <a href="/projects/" class="link-accent">портфолио</a> и <a href="/demo/app/" class="link-accent">демо</a> • Отвечаем за 1 час</p>
</div>
</div>
</section>''')
FLOW_VERT = Template('''
<section class="section dark">
<div class="container">
<p class="label reveal">Процесс</p>
<h2 class="reveal">${heading}</h2>
<div class="flow-diagram">
<div class="flow-spine"></div>
${stages}
</div>
</div>
</section>''')
FLOW_V_STAGE = '''
<div class="flow-stage reveal">
<div class="flow-node">
<div class="flow-dot"></div>
<div class="flow-card">
<h3>${title}</h3>
<p>${subtitle}</p>
</div>
</div>
<div class="flow-services">
${tags}
</div>
</div>'''
FLOW_HORZ = Template('''
<section class="section dark">
<div class="container">
<p class="label reveal">Процесс</p>
<h2 class="reveal">${heading}</h2>
<div class="flow-horizontal">
${stages}
</div>
</div>
</section>''')
FLOW_H_STAGE = '''
<div class="flow-h-stage reveal">
<div class="flow-h-line"></div>
<div class="flow-h-card">
<h3>${title}</h3>
<p>${subtitle}</p>
</div>
<div class="flow-h-tags">
${tags}
</div>
</div>'''

base_html = Template('''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#0A0A0F">
<title>${title} — разработка под ключ | AXIIOM</title>
<meta name="description" content="${desc}">
<link rel="canonical" href="https://axiiom.ru/industries/${slug}.html">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebPage",
      "name": "${title}",
      "description": "${desc}",
      "url": "https://axiiom.ru/industries/${slug}.html",
      "isPartOf": { "@type": "WebSite", "name": "AXIIOM", "url": "https://axiiom.ru/" }
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Главная", "item": "https://axiiom.ru/" },
        { "@type": "ListItem", "position": 2, "name": "Решения", "item": "https://axiiom.ru/industries/" },
        { "@type": "ListItem", "position": 3, "name": "${title}", "item": "https://axiiom.ru/industries/${slug}.html" }
      ]
    },
    {
      "@type": "Service",
      "serviceType": "${title}",
      "provider": { "@type": "Organization", "name": "AXIIOM", "url": "https://axiiom.ru/", "foundingDate": "2004" },
      "areaServed": { "@type": "Country", "name": "Russia" },
      "description": "${desc}",
      "offers": { "@type": "Offer", "priceCurrency": "RUB", "price": "${price}", "availability": "https://schema.org/InStock", "url": "https://axiiom.ru/industries/${slug}.html" }
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        ${faq_json}
      ]
    }
  ]
}
</script>
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" as="style">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<meta property="og:type" content="website">
<meta property="og:url" content="https://axiiom.ru/industries/${slug}.html">
<meta property="og:title" content="${title} — AXIIOM">
<meta property="og:description" content="${desc}">
<meta property="og:image" content="https://axiiom.ru/og/industries/${slug}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="ru_RU">
<meta property="og:site_name" content="AXIIOM">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:url" content="https://axiiom.ru/industries/${slug}.html">
<meta name="twitter:title" content="${title} — AXIIOM">
<meta name="twitter:description" content="${desc}">
<meta name="twitter:image" content="https://axiiom.ru/og/industries/${slug}.png">
<link rel="stylesheet" href="/styles.css?v=20260912">
<link rel="stylesheet" href="/preloader.css?v=20260912">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="apple-touch-icon" sizes="180x180" href="/icons/apple-touch-icon.png">
</head>
<body>
<a href="#main" class="skip-link">Перейти к содержанию</a>
<div id="preloader">
<script>(function(){var p=document.getElementById('preloader');if(!p)return;if(sessionStorage.getItem('_seen')){p.style.display='none';return}sessionStorage.setItem('_seen','1');var t=Date.now();p._start=t;setTimeout(function(){p.classList.add('_rdy')},500);window.addEventListener('load',function(){var e=Date.now()-t;if(e<900){setTimeout(function(){p.classList.add('hidden');setTimeout(function(){p.classList.add('hidden-done')},500)},900-e)}else{p.classList.add('hidden');setTimeout(function(){p.classList.add('hidden-done')},500)}})})()</script>
<svg class="preloader-svg" viewBox="0 0 36 36" width="80" height="80"><rect class="pr1" x="2" y="2" width="14" height="14" rx="2"/><rect class="pr2" x="20" y="2" width="14" height="14" rx="2"/><rect class="pr3" x="2" y="20" width="14" height="14" rx="2"/><rect class="pr4" x="20" y="20" width="14" height="14" rx="2"/><circle class="pc" cx="27" cy="27" r="3"/></svg>
</div>
<div class="noise"></div>
<div class="grid-overlay"></div>
<header class="header" id="header">
    <div class="container">
        <nav class="nav">
            <a href="/" class="logo">
                <svg width="30" height="30" viewBox="0 0 36 36" fill="none"><rect x="2" y="2" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5" opacity=".4"/><rect x="20" y="2" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5" opacity=".4"/><rect x="2" y="20" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5" opacity=".4"/><rect x="20" y="20" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5"/><circle cx="27" cy="27" r="3" fill="currentColor" opacity=".8"/></svg>
                <span>AXIIOM</span>
            </a>
            <ul class="nav-links nav-links--desktop" id="desktopNav"></ul>
            <div class="nav-actions">
                <a href="/#contact" class="btn btn-nav" id="ctaBtn">Обсудить проект</a>
                <button class="theme-btn" id="themeToggle" aria-label="Сменить тему"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg></button>
                <button class="nav-toggle" id="navToggle" aria-label="Меню"><span></span><span></span><span></span></button>
            </div>
        </nav>
    </div>
</header>
<div class="nav-overlay" id="navOverlay"><ul class="nav-links" id="mobileNav"></ul></div>
<nav class="breadcrumbs" id="breadcrumbs" aria-label="Breadcrumb"><div class="container"></div></nav>
<main id="main">
<section class="hero industries-hero">
<div class="container"><div class="hero-content">
<div class="hero-bg-svg"><svg width="800" height="600" viewBox="0 0 800 600" fill="none"><circle cx="400" cy="300" r="280" stroke="rgba(255,255,255,0.05)" stroke-width="2"/><circle cx="400" cy="300" r="200" stroke="rgba(255,255,255,0.06)" stroke-width="2"/><circle cx="400" cy="300" r="120" stroke="rgba(255,255,255,0.08)" stroke-width="2"/><line x1="50" y1="300" x2="750" y2="300" stroke="rgba(255,255,255,0.04)" stroke-width="2"/><line x1="400" y1="20" x2="400" y2="580" stroke="rgba(255,255,255,0.04)" stroke-width="2"/><path d="M200 300 L400 100 L600 300 L400 500 Z" stroke="rgba(255,255,255,0.05)" stroke-width="2" fill="none"/><circle cx="400" cy="300" r="4" fill="rgba(255,255,255,0.12)"/></svg></div>
<div class="hero-category-icon">${category_icon}</div>
<div class="badge-row"><p class="badge">${category} • AXIIOM</p><button class="share-btn" onclick="copyPageUrl(this)" aria-label="Поделиться"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12v8a2 2 0 002 2h12a2 2 0 002-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg><span class="share-tooltip">Ссылка скопирована</span></button></div>
<h1>${h1}</h1>
<p class="hero-desc">${hero}</p>
<div class="price-anchor reveal"><span class="price-badge">MVP ${price}</span><span class="price-badge">Запуск ${timeline}</span><span class="price-badge">${bonus}</span></div>
<div class="hero-btns"><a href="/#contact" class="btn">Обсудить проект за 1 час</a><a href="/calculator/?industry=${slug}" class="btn btn-outline">Рассчитать стоимость →</a></div>
<div class="hero-trust"><span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--clr-accent)" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> 50+ проектов</span><span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--clr-accent)" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> 99.99% Uptime</span><span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--clr-accent)" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> ${trust}</span></div>
<div class="author-block reveal"><span class="author-avatar">AX</span><div><strong>Команда AXIIOM</strong> • 50+ проектов с 2004 года • <span class="author-date">Обновлено: ${date} • 6 мин чтения</span></div></div>
</div></div></section>

<section class="section"><div class="container"><p class="label reveal">О решении</p><h2 class="reveal">${title}</h2><p class="content-wrapper reveal" style="max-width:680px;margin:0 auto;color:var(--clr-muted)">${desc}</p>
<div class="proof-logos reveal"><span>Сбер</span><span>Альфа-Банк</span><span>Тинькофф</span><span>1С</span><span>iiko</span><span>СДЭК</span><span>Яндекс</span></div>
</div></section>

<section class="section dark">
<div class="container">
<p class="label reveal">Видео</p>
<h2 class="reveal">Как работает ${short_title} — 90 секунд</h2>
<div class="glass-card reveal" style="max-width:800px;margin:24px auto 0;padding:0;overflow:hidden;position:relative;aspect-ratio:16/9;background:var(--clr-surface);display:flex;align-items:center;justify-content:center">
<div style="text-align:center;padding:40px">
<div style="width:80px;height:80px;border-radius:50%;background:var(--clr-accent);display:flex;align-items:center;justify-content:center;margin:0 auto 16px;cursor:pointer"><svg width="32" height="32" viewBox="0 0 24 24" fill="#0A0A0F"><path d="M8 5v14l11-7z"/></svg></div>
<p style="color:var(--clr-heading);font-weight:600">Видео-демо ${short_title}</p>
<p style="color:var(--clr-muted);font-size:.85rem;margin-top:8px">Скоро: архитектура, UX, интеграции за 90 сек. Сейчас — <a href="/demo/app/" class="link-accent">смотрите интерактивные демо</a> и <a href="/projects/" class="link-accent">портфолио</a></p>
</div>
</div>
</div>
</section>

<section class="section dark">
    <div class="container">
        <p class="label reveal">Боли отрасли</p>
        <h2 class="reveal">Знакомо?</h2>
        <div class="problems-grid">
            ${problems_html}
        </div>
    </div>
</section>

${modules_html}
${flow_html}

<section class="section">
<div class="container">
<p class="label reveal">Стек</p>
<h2 class="reveal">На чём строим для ${short_title}</h2>
<div class="stack-grid reveal">
${stack_html}
</div>
</div>
</section>

<section class="section dark">
<div class="container">
<p class="label reveal">Интеграции</p>
<h2 class="reveal">С чем интегрируем</h2>
<div class="partners-list reveal">
${integrations_html}
</div>
<p class="demo-note reveal" style="margin-top:24px">+ 20 других систем — банки, 1С, iiko, СДЭК, Яндекс. Смотрите <a href="/projects/" class="link-accent">портфолио</a></p>
</div>
</section>

<section class="section">
<div class="container">
<p class="label reveal">Кейсы</p>
<h2 class="reveal">Результаты, а не обещания</h2>
<div class="cases-grid">
<div class="glass-card reveal card-pad-md"><span class="case-tag">Кейс 1 • ${category}</span><p class="case-step"><span>Задача:</span> ${case1_task}</p><p class="case-step"><span>Решение:</span> ${case1_solution}</p><p class="case-result">${case1_result}</p><div class="case-proof"><span>NDA-проект, 2024</span><span>99.99% uptime</span></div><a href="/projects/" class="btn btn-card">Портфолио →</a></div>
<div class="glass-card reveal card-pad-md"><span class="case-tag">Кейс 2 • Highload</span><p class="case-step"><span>Задача:</span> ${case2_task}</p><p class="case-step"><span>Решение:</span> ${case2_solution}</p><p class="case-result">${case2_result}</p><div class="case-proof"><span>Нагрузочные тесты</span><span>Grafana</span></div><a href="/demo/app/" class="btn btn-card">Демо →</a></div>
</div>
</div>
</section>

<section class="section dark">
<div class="container">
<p class="label reveal">FAQ</p>
<h2 class="reveal">Частые вопросы про ${short_title} — отвечаем честно</h2>
<div class="faq-grid reveal">
${faq_html}
</div>
</div>
</section>

<section class="section">
<div class="container">
<p class="label reveal">Похожие решения</p>
<h2 class="reveal">Ещё для вашего бизнеса</h2>
<div class="tools-grid">
${related_html}
</div>
<div class="center mt-40"><a href="/industries/" class="btn btn-outline">Все 30 решений →</a><a href="/calculator/?industry=${slug}" class="btn" style="margin-left:12px">Калькулятор для ${short_title} →</a></div>
</div>
</section>

${cta_html}

</main>

<div id="stickyCta" class="sticky-cta">
<p><strong>${short_title}</strong> — MVP ${price}, запуск ${timeline}. ${bonus}</p>
<a href="/#contact" class="btn">Обсудить проект</a>
<a href="/calculator/?industry=${slug}" class="btn btn-outline">Калькулятор</a>
</div>

<footer class="footer"><div class="container"><div id="footerCopy"></div></div></footer>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-HFS4BDGTV4"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-HFS4BDGTV4");</script>
<script src="/metrika.js?v=20260912" defer></script>
<script src="/config.js?v=20260912"></script>
<script src="/nav.js?v=20260912"></script>
<script>Nav.init({ cta: true, breadcrumbs: true });</script>
<script src="/theme.js?v=20260912"></script>
<script src="/preloader.js?v=20260912"></script>
<script>
(function(){var t=document.getElementById('navToggle');var o=document.getElementById('navOverlay');if(!t||!o)return;t.addEventListener('click',function(e){e.stopPropagation();o.classList.toggle('open');t.classList.toggle('active');document.body.style.overflow=o.classList.contains('open')?'hidden':'';});})();
function copyPageUrl(btn){var url=window.location.href;var ta=document.createElement('textarea');ta.value=url;ta.style.position='fixed';ta.style.left='0';ta.style.top='0';ta.style.width='2em';ta.style.height='2em';ta.style.padding='0';ta.style.border='none';ta.style.outline='none';ta.style.background='transparent';ta.style.color='transparent';document.body.appendChild(ta);ta.focus();ta.select();document.execCommand('copy');document.body.removeChild(ta);var tip=btn.querySelector('.share-tooltip');if(tip){tip.classList.add('show');setTimeout(function(){tip.classList.remove('show');},2000);}}
var reveals=document.querySelectorAll('.reveal');var ro=new IntersectionObserver(function(e){e.forEach(function(entry){if(entry.isIntersecting)entry.target.classList.add('visible');});},{threshold:.15});reveals.forEach(function(r){ro.observe(r);});
// sticky CTA
(function(){var s=document.getElementById('stickyCta');if(!s)return;var showAt=600;window.addEventListener('scroll',function(){if(window.scrollY>showAt)s.classList.add('visible');else s.classList.remove('visible');},{passive:true});})();
</script>
</body>
</html>''')

def build_problems_html(slug, title):
    probs = PROBLEMS.get(slug, DEFAULT_PROBLEMS)
    html = ""
    for prob, sol in probs:
        html += f'''
            <div class="glass-card reveal card-pad-md">
                <p class="problem-text">{prob}</p>
                <p class="solution-text"><strong>{sol}</strong></p>
            </div>'''
    return html

def build_stack_html(category):
    tech = TECH_STACK.get(category, TECH_STACK['B2B & Enterprise'])
    html = ""
    for k,v in tech.items():
        html += f'<div class="stack-group"><h3>{k}</h3><p>{v}</p></div>'
    return html

def build_integrations_html(category):
    ints = INTEGRATIONS.get(category, INTEGRATIONS['B2B & Enterprise'])
    return "\n".join([f"<span>{i}</span>" for i in ints])

def build_faq_html(slug, short_title):
    faqs = FAQ_MAP.get(slug, DEFAULT_FAQ)
    # replace placeholder
    html = ""
    faq_json_parts = []
    for q,a in faqs:
        q = q.replace('${slug}', slug)
        a = a.replace('${slug}', slug).replace('${short_title}', short_title)
        html += f'<div class="glass-card card-pad-md"><h3>{q}</h3><p>{a}</p></div>'
        q_esc = q.replace('"', '\\"')
        a_esc = a.replace('"', '\\"')
        faq_json_parts.append(f'{{"@type": "Question","name": "{q_esc}","acceptedAnswer": {{"@type": "Answer","text": "{a_esc}"}}}}')
    return html, ",\n        ".join(faq_json_parts)

def build_related_html(current_slug, category):
    related = []
    for s, cat in CATEGORY_MAP.items():
        if s != current_slug and cat == category:
            related.append(s)
        if len(related) >= 6:
            break
    if len(related) < 3:
        for s in CATEGORY_MAP.keys():
            if s != current_slug and s not in related:
                related.append(s)
            if len(related) >= 3:
                break
    html = ""
    txt_titles = {}
    try:
        with open('industries/industries.txt', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts:
                    txt_titles[parts[0]] = parts[1] if len(parts)>1 else parts[0]
    except:
        pass
    for rel_slug in related[:3]:
        title = txt_titles.get(rel_slug, rel_slug.replace('-', ' ').title())
        html += f'<a href="{rel_slug}.html" class="tool-card blog-card reveal"><h3>{title}</h3><p>Разработка под ключ, интеграция, поддержка 24/7.</p><span class="blog-read">Подробнее →</span></a>'
    return html

# Load txt
txt_data = {}
with open('industries/industries.txt', encoding='utf-8') as f:
    for line in f:
        line=line.strip()
        if not line: continue
        parts=line.split('|')
        if len(parts)<4: continue
        txt_data[parts[0]] = parts

all_slugs = list(CATEGORY_MAP.keys())
today = datetime.now().strftime("%d.%m.%Y")
generated = 0
for slug in all_slugs:
    parts = txt_data.get(slug)
    if not parts:
        continue
    title=parts[1]
    desc=parts[2]
    h1=parts[3] if len(parts)>3 and parts[3].strip() else title
    hero=parts[4] if len(parts)>4 and parts[4].strip() else desc
    modules_raw = parts[5] if len(parts)>5 else ""
    cta_raw = parts[6] if len(parts)>6 else ""
    flow_raw = parts[7] if len(parts)>7 else ""

    category = CATEGORY_MAP.get(slug, 'B2B & Enterprise')
    short_title = title.split(' ')[0] if len(title.split(' '))<4 else title
    trust = "161-ФЗ / PCI DSS" if category in ('Fintech','Security & Fintech') else "Интеграция с банками и 1С" if category=='B2B & Enterprise' else "Highload 99.99%"
    price, timeline, bonus = PRICE_MAP.get(category, ('от 600к ₽','2 месяца','Бесплатно'))
    category_icon = CATEGORY_ICONS.get(category, CATEGORY_ICONS['B2B & Enterprise'])

    modules_html=''
    if modules_raw.strip():
        items=''
        for module in modules_raw.split(':::'):
            module=module.strip()
            if not module: continue
            if '::' in module:
                m_name,m_desc=module.split('::',1)
                items+=MODULE_ITEM.replace('${name}',m_name.strip()).replace('${desc}',m_desc.strip())
        if items:
            modules_html=MODULES_TMPL.substitute(items=items)

    cta_html=''
    if cta_raw.strip():
        cta_parts=cta_raw.split('::',1)
        cta_title=cta_parts[0].strip()
        cta_text=cta_parts[1].strip() if len(cta_parts)>1 else 'Оставьте заявку — мы свяжемся в течение часа.'
        cta_html=CTA_TMPL.substitute(title=cta_title, text=cta_text, slug=slug)
    else:
        cta_html=CTA_TMPL.substitute(title=f"Нужна {title.lower()}?", text=f"Обсудим задачу для {title.lower()}, предложим архитектуру и смету за 24 часа. Бесплатная Discovery.", slug=slug)

    flow_html=''
    if flow_raw.strip():
        raw=flow_raw.strip()
        flow_type='vertical'
        flow_heading='Путь заказа — от заявки до релиза'
        if raw.startswith('vertical:::'):
            flow_type='vertical'
            raw=raw[len('vertical:::'):]
        elif raw.startswith('horizontal:::'):
            flow_type='horizontal'
            flow_heading='Маршрут проекта'
            raw=raw[len('horizontal:::'):]
        stages=''
        for stage in raw.split(':::'):
            stage=stage.strip()
            if not stage: continue
            parts_s=stage.split('::')
            if len(parts_s)>=2:
                s_title=parts_s[0].strip()
                s_sub=parts_s[1].strip()
                s_tags=parts_s[2].strip() if len(parts_s)>2 else ''
                tags_html=''.join(f'<span class="tag">{t.strip()}</span>' for t in s_tags.split(',') if t.strip())
                if flow_type=='horizontal':
                    stages+=FLOW_H_STAGE.replace('${title}',s_title).replace('${subtitle}',s_sub).replace('${tags}',tags_html)
                else:
                    stages+=FLOW_V_STAGE.replace('${title}',s_title).replace('${subtitle}',s_sub).replace('${tags}',tags_html)
        if stages:
            if flow_type=='horizontal':
                flow_html=FLOW_HORZ.substitute(heading=flow_heading, stages=stages)
            else:
                flow_html=FLOW_VERT.substitute(heading=flow_heading, stages=stages)

    problems_html=build_problems_html(slug, title)
    stack_html=build_stack_html(category)
    integrations_html=build_integrations_html(category)
    faq_html, faq_json = build_faq_html(slug, short_title)
    related_html = build_related_html(slug, category)

    case1_task = f"Нужна {title.lower()} с интеграцией и аналитикой."
    case1_solution = f"Спроектировали платформу на {TECH_STACK.get(category, {}).get('Backend','Go, Node.js').split(',')[0]}, интеграции с {', '.join(INTEGRATIONS.get(category, [])[:2])}."
    case1_result = "Запуск за 3 месяца, рост конверсии на 28%, 0 простоев в пик."
    case2_task = "Сервис падал, нет данных для решений."
    case2_solution = "Highload + Kubernetes + дашборды в реальном времени."
    case2_result = "99.99% uptime, -70% время отчётности, +22% выручка."

    if slug in ('avtomatizaciya-restoranov','dostavka-edy','bronirovanie-gostinits'):
        case1_task="Сеть ресторанов теряла клиентов, заказы из 3 агрегаторов терялись, нет LTV."
        case1_solution="Единое окно POS + CRM LOVII + KDS + iiko + Яндекс.Еда."
        case1_result="40% возврат клиентов, +18% средний чек, +35% LTV, 0 потерянных заказов."
    if slug in ('kyc-onboarding','multi-currency-wallet','p2p-marketplace','trading-engine','asset-tokenization','investment-crm','real-time-analytics'):
        case1_task="Банк отказал в интеграции из-за 161-ФЗ, высокий фрод, отток на онбординге 60%."
        case1_solution="KYC с биометрией и liveness, Vault/HSM, escrow, мультиэквайринг, SBP, PCI DSS."
        case1_result="Онбординг 2 мин, фрод -90%, прошли аудит PCI DSS, +35% конверсия."
        case2_task="Отчёты строились часами, нет real-time аналитики, данные в разных системах."
        case2_solution="ClickHouse + Kafka + ETL из CRM/1С/рекламы, дашборды Grafana, ML-прогноз."
        case2_result="Отчёты за секунды, -70% время аналитики, +22% выручка за счёт быстрых решений."

    html = base_html.substitute(
        slug=slug, title=title, desc=desc, h1=h1, hero=hero,
        category=category, short_title=short_title, trust=trust,
        modules_html=modules_html, flow_html=flow_html, cta_html=cta_html,
        problems_html=problems_html, stack_html=stack_html,
        integrations_html=integrations_html,
        faq_html=faq_html, faq_json=faq_json,
        related_html=related_html,
        case1_task=case1_task, case1_solution=case1_solution, case1_result=case1_result,
        case2_task=case2_task, case2_solution=case2_solution, case2_result=case2_result,
        price=price, timeline=timeline, bonus=bonus,
        category_icon=category_icon,
        date=today,
    )
    with open(f'industries/{slug}.html','w',encoding='utf-8') as fw:
        fw.write(html)
    generated+=1

print(f'Pages generated — v3 конверсионная: {generated} pages')
