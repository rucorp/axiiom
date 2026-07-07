# Интеграция с Globus (Globus API)

> **Источник:** `rewiew/api-docs-export/globus/index.html` — ReDoc документация, OpenAPI 3.0.3

## Общие сведения

| Параметр | Значение |
|----------|----------|
| **Версия API** | v1 |
| **Базовый URL** | `http://igooods.test/api/v8` (stage) / `https://master.jira.igooods.ru/api/v8` (prod) |
| **Формат** | OpenAPI 3.0.3 |
| **Аутентификация** | Внутренний API igooods (не внешний) |

Globus — внутренняя интеграция (igooods → Globus). API работает поверх основного API v8.

## Эндпоинты

| Метод | Путь | Описание | Параметры |
|-------|------|----------|-----------|
| GET | `/shops` | Список магазинов Globus по координатам | `group=globus`, `lat`, `lng` |
| GET | `/deep_link` | Deep link для выбора товара/магазина/адреса | `delivery_zone_id`, `shop_group`, `latitude`, `longitude`, опционально `sap_code` |

### GET /shops

Возвращает список магазинов Globus с зонами доставки, отсортированный по удалённости от указанных координат.

**Параметры:**
- `group` (string, required) — всегда `globus`
- `lat` (number, required) — широта
- `lng` (number, required) — долгота

**Ответ:**
```json
{
  "code": 0,
  "data": {
    "total": 1,
    "list": [
      {
        "id": 1,
        "name": "Globus",
        "group": "globus",
        "group_en": "globus",
        "color": "#d42b1c",
        "header_color": "#ffffff",
        "short_address": "ул. Примерная, 1",
        "logo": { "svg": "/logos/globus.svg", "png": "/logos/globus.png" },
        "brand_logo": { "svg": "/brand/globus.svg", "png": "/brand/globus.png" },
        "branding": { "mark": { "svg": "/brand/mark.svg" } },
        "payment_types": { "cash": true, "card": true, "online": false, "sbp": true, "apple_pay": true, "google_pay": false },
        "coordinate": { "longitude": 37.6173, "latitude": 55.7558 },
        "open": true,
        "zone": {
          "id": 1,
          "delivery_date": null,
          "service_info": [
            { "type": "assembly", "name": "Сборка", "price": 99, "real_price": 99, "threshold": 0, "next_price": 0 },
            { "type": "delivery", "name": "Доставка", "price": 199, "real_price": 199, "threshold": 1000, "next_price": 0 },
            { "type": "overweight", "name": "Перевес", "price": 0, "real_price": 0, "threshold": 80, "next_price": 50 }
          ]
        },
        "max_order_weight": 80,
        "branding": {}
      }
    ]
  }
}
```

### GET /deep_link

Генерирует ссылку для выбора товара, магазина и адреса доставки в приложении.

**Параметры:**
- `delivery_zone_id` (integer, required)
- `shop_group` (string, required)
- `latitude` (number, required)
- `longitude` (number, required)
- `sap_code` (string, optional) — код товара SAP

**Ответ:**
```json
{
  "deep_link": "igooods://?..."
}
```

## Особенности для реализации

- Globus — **внутренняя** интеграция (API хостится на стороне igooods, не на стороне сети)
- API минималистичный: всего 2 эндпоинта, весь каталог и заказы идут через общий API v8
- `service_info` — массив услуг со стоимостью сборки, доставки, перевеса
- `branding` — кастомизация интерфейса под бренд Globus (цвета, логотипы)
- `payment_types` — список доступных способов оплаты для конкретного магазина
- `max_order_weight` — ограничение веса заказа для магазина
