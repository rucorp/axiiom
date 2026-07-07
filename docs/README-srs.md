# Документация продукта (SRS)

Software Requirements Specification — агрегатор доставки продуктов из супермаркетов.

- **Живой сайт:** https://bestdeejay-design.github.io/srs-docs/
- **Исходный SRS:** `SRS/SRS-v2.md` (v2.0, 4240+ строк, 2 тома, 14 BP, 7 ADR)

## Структура

```
├── SRS/
│   ├── SRS-v2.md                   # **Главный документ** — полная SRS v2.0
│   ├── SRS-pdf.md                  # PDF-версия (с Mermaid-диаграммами, HTML-таблицами)
│   ├── business_model.md           # Детальная юнит-экономика
│   ├── finops.md                   # FinOps / стоимость инфраструктуры
│   ├── ESTIMATION.md               # Оценка сроков разработки
│   ├── AUDIT_AS_IS.md              # Аудит текущего состояния
│   ├── OTP_VIA_MESSENGERS.md       # OTP доставка через мессенджеры
│   ├── feature-map.md              # Карта фич (mindmap)
│   ├── db/schema.rb                # Схема БД (Rails)
│   ├── migrations/*.sql            # SQL-миграции (каталог, пользователи, заказы и т.д.)
│   ├── integrations/*.md           # Детали интеграций с API магазинов
│   ├── roadmap/V3_FRANCHISE.md     # Франчайзинговая модель (V3)
│   └── references/README.md        # Индекс референсов по разделам
├── archive/                        # Устаревшие документы (сохранены для истории)
│   ├── SRS.md                      # Предыдущая версия SRS
│   ├── SRS_original.md             # Оригинальная SRS
│   ├── SRS.html                    # Предыдущая HTML-сборка
│   ├── ШАБЛОН_СПЕЦИФИКАЦИИ_ПРОДУКТА.md  # Шаблон SRS (черновик)
│   ├── ПЛАН_ОПТИМИЗАЦИИ.md         # План миграции на микросервисы
│   ├── Discovery-фаза.txt          # Описание Discovery-этапа
│   ├── Набор-промптов-для-доработки-SRS-документа.rtf
│   ├── docs/                       # Устаревшая MkDocs-сборка
│   └── exports/                    # Устаревшие экспорты HTML/PDF/diagrams
├── build-srs-html.py               # Сборка HTML — Pandoc → шаблон с TOC, поиском, темами
├── filter-pdf.py                   # Фильтр для удаления черновиков/заметок
├── prepare-pdf.py                  # Подготовка PDF
├── pdf-style.css                   # Стили для PDF-экспорта
├── puppeteer-config.json           # Конфиг Mermaid CLI для рендеринга диаграмм
├── references/
│   └── github/                     # Исследования и референсы
│       ├── README.md               # Индекс
│       ├── catalog-data.js         # Модель каталога товаров
│       ├── dependencies/           # Зависимости (frontend/backend)
│       ├── analysis.md             # Анализ сервиса-аналога
│       ├── research.md             # Исследование GitHub
│       ├── store-apis-research.md  # API супермаркетов
│       ├── open-source-references.md  # Каталог OS-референсов
│       └── repos/                  # Склонированные репозитории (12 шт)
└── mkdocs.yml                      # Конфиг MkDocs (deprecated)
```

## Сборка

```bash
# HTML-сайт
python3 build-srs-html.py
# → SRS/SRS-v2.md → exports/SRS.html (устаревший пайплайн)

# PDF
python3 prepare-pdf.py
# → exports/SRS.pdf (устаревший пайплайн)
```

## Пайплайн

`SRS/SRS-v2.md` → сборка HTML/PDF → деплой на GitHub Pages (`srs-docs` repo, `gh-pages` ветка).

**Ключевые зависимости:** Pandoc, Mermaid CLI (mmdc), Python 3.

## Важно

- `SRS/SRS-v2.md` — единственный актуальный источник.
- Название сервиса удалено из всех публичных артефактов.
- Содержимое ведётся на русском языке.
