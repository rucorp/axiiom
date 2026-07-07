# Интеграция с ВкусВилл (Vkusvill API)

> **Источник:** [openapi_universal_integration.yaml.yaml](../../rewiew/openapi_universal_integration.yaml.yaml) — OpenAPI 3.0.0 спецификация

## Общие сведения

| Параметр | Значение |
|----------|----------|
| **Версия API** | 1.0.6 |
| **Формат** | OpenAPI 3.0.0 |
| **Базовый URL** | `/{partner_name}` |
| **Аутентификация** | Bearer Token (предоставляется по запросу) |
| **Модель** | Pull-модель: партнер запрашивает/обновляет ресурсы |

> Каталог торговых точек актуализируется 1 раз в сутки. Для получения полного каталога используйте `store_id = 0`.

## Эндпоинты

### Торговые точки (Stores)

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/v1/{partner_name}/stores/list` | Список ТТ с адресами |
| GET | `/v1/{partner_name}/stores/geo` | Список ТТ с геозонами (полигоны) |
| GET | `/v2/{partner_name}/stores/geo` | Список ТТ с геозонами v2 (с дырками на полигоне) |
| POST | `/v1/{partner_name}/stores/check-store` | Проверка ТТ по координатам |
| POST | `/v1/{partner_name}/stores/get-store` | Определение ТТ по координатам |
| POST | `/v2/{partner_name}/stores/get-store` | Определение ТТ по координатам v2 |

**Geo v2:** поддерживает полигоны с "дырками" (holes). Формат GeoJSON Feature/Polygon. Каждая зона содержит: area_id, feature (geometry), time_slot, delivery_fee_thresholds, is_express, sla.

**Store data:** store_id, title, address, city, priority, areas[], time_slot, delivery_fee_thresholds (minimal_order_amount, delivery_fee).

### Номенклатура (Nomenclature)

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/v1/{partner_name}/nomenclature/{store_id}/catalog` | Актуальный каталог товаров |
| GET | `/v1/{partner_name}/nomenclature/{store_id}/stocks` | Остатки товаров |
| GET | `/v1/{partner_name}/nomenclature/{store_id}/stocks_tomorrow` | Остатки на завтра |
| GET | `/v1/{partner_name}/nomenclature/{store_id}/price` | Стоимость товаров |

**Catalog:** категории (id, parent_id, name, sort_order, images) + товары.

**Товар (item):** id, vendor_code, categories[], name, description (general, composition, nutritional_value, purpose, storage_requirements, expires_in, vendor_country, package_info), price, loyalty_price, vat, measure (value, quantum, unit — MLT/GRM), is_catch_weight, is_express, is_excise, is_hot, is_freeze, images (hash, url), rating, replacement_items[].

**Остатки:** список {id, stock} — при 0 товар пропадает из выдачи.

**Параметр night_zeroing** — ночное зануление остатков (0 — не занулять).

### Заказы (Orders)

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/v1/{partner_name}/orders/create` | Создание заказа |
| POST | `/v1/{partner_name}/orders/cancellation` | Отмена заказа |
| POST | `/v1/{partner_name}/orders/confirm-delivery` | Подтверждение доставки |
| POST | `/v1/{partner_name}/orders/status` | Получение статуса |
| POST | `/v1/{partner_name}/orders/show` | Информация о заказе (корзина) |

**Две схемы заказа:**

| Тип | discriminator | Доставка |
|-----|---------------|----------|
| VkusvillOrder | `vkusvill` | Силами ВВ |
| MarketplaceOrder | `marketplace` | Силами партнера |

**Создание заказа:** original_order_id, store_id, customer (name, phone), payment (total_price, payment_type: CARD/CASH), items[] (id, name, quantity, price), delivery (coordinates, address, time_slot), comment.

**Для весовых товаров:** quantity — вес в кг, кратный quantum. price — цена за 1 кг. Для штучных: quantity — количество штук, price — цена за штуку.

**Статусы заказа:** NEW → ACCEPTED → COLLECTING → READY → IN_DELIVERY → DELIVERED. Из любого статуса → CANCELLED.

### Сервисы (Services)

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/v1/{partner_name}/services/client-check` | Проверка карты клиента по телефону |
| POST | `/v1/{partner_name}/services/create-card` | Создание карты клиента ВВ |
| POST | `/v1/{partner_name}/services/lp-list` | Скидки на ЛП по нескольким клиентам |
| POST | `/v1/{partner_name}/services/lp` | Скидка на ЛП по одному клиенту |

**Любимые продукты (LP):** id товара, dsc_value (процент скидки), date_from, date_to.

## Формат ответов

```json
{
  "status": "success" | "error",
  "message": "Сообщение",
  "data": { ... }
}
```

## Типы ошибок

| HTTP | Описание |
|------|----------|
| 401 | Unauthorized |
| 422 | Ошибка валидации (с указанием полей) |
| 500 | Внутренняя ошибка сервера |

## Особенности для реализации

- Каталог общий для всех ТТ, обновляется 1 раз в сутки
- Для получения каталога использовать `store_id = 0`
- Цены получать отдельно в разрезе каждой ТТ
- `night_zeroing` — ночное обнуление остатков (по умолчанию — зануляются)
- quantum — минимальный шаг заказа для весового товара
- Товары с нулевой ценой отбрасываются
- Маркировка Честный знак: `data_matrix[]` в информации о заказе
- Для экспресс-доставки: `is_express` на уровне зоны и товара
