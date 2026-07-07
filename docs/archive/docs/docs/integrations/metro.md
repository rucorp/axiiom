# Интеграция с METRO (METRO Cash & Carry)

> **Источники:**
> - `references/github/store-apis-research.md` — исследование API
> - `SRS/db/schema.rb` — `external_meta_provider: metro`, `shop_group_enum`

## Общие сведения

| Параметр | Значение |
|----------|----------|
| **Тип интеграции** | B2B (METRO Markets) + EDI (основной каталог) |
| **EDI-провайдер** | EDI Culture Center (edicult.ru) |
| **Developer Portal** | developer.metro-selleroffice.com (OpenAPI для B2B) |
| **Портал поставщика** | supplier-support.metro-cc.ru |
| **Формат данных** | EDI (ORDERS, DESADV, RECADV, INVOIC) + JSON (B2B) |

## Статус интеграции

METRO интегрирована в систему на уровне `external_meta`:
- `external_meta_provider` включает `metro`
- `shop_group_enum` включает `metro`
- Данные каталога, цен и остатков синхронизируются через внешний адаптер

## EDI протокол

METRO Russia использует электронный документооборот через EDI Culture Center:

| Документ | Описание | Направление |
|----------|----------|-------------|
| **ORDERS** | Заказ на поставку | igooods → METRO |
| **DESADV** | Уведомление об отгрузке | METRO → igooods |
| **RECADV** | Подтверждение приёмки | igooods → METRO |
| **INVOIC** | Счёт-фактура | METRO → igooods |

## Особенности для реализации

- METRO — **B2B-ориентированная** сеть (юридические лица, ИП)
- Для розничных заказов может потребоваться другой подход (парсинг сайта или альтернативный API)
- Адаптер METRO в коде: `external_meta` с `provider: "metro"`, данные хранятся в `JSONB payload`
- Каталог и цены синхронизируются через внешний адаптер в таблицу `external_meta` (source_type: Product/Shop/Category/Model)
- EDI-документы обрабатываются через выделенный сервис (или Sidekiq worker)
