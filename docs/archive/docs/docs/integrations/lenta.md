# Интеграция с Лентой (Lenta Pickup API)

> **Источник:** [lenta.pickup_11_04_2024.yml.yml](../../rewiew/lenta.pickup_11_04_2024.yml.yml) — OpenAPI 3.0.1 спецификация

## Общие сведения

| Параметр | Значение |
|----------|----------|
| **Версия API** | 1.1.0 |
| **Формат** | OpenAPI 3.0.1 |
| **Stage** | `https://partners-stage.dev.lenta.tech` |
| **Production** | `https://partners.api.lenta.com` |
| **Аутентификация** | OAuth2 Client Credentials |

## Аутентификация

`POST /v1/security/oauth/token`

Партнер отправляет `client_id`, `client_secret`, `grant_type`, `scope`. В ответ получает `access_token`, `expires_in`, `token_type`.

## Эндпоинты

### Каталог (Catalog)

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/v1/catalog/categories` | Список категорий |
| GET | `/v1/catalog/products` | Список продуктов (deprecated) |
| GET | `/v2/catalog/products` | Список продуктов v2 |
| GET | `/v1/catalog/products-full` | Полный список без фильтрации ассортимента |
| GET | `/v1/catalog/{storeId}/prices` | Цены продуктов указанного склада |

**Product v2:** id, posId, name, brand, images (detail/list), metadata (JSON), exciseValue (S/N/V/O), markType (TOBACCO/MILK/..., 13 типов).

**ProductData v2:** categories, product, vat, weight (net/gross), barcodes (value, type, weightEncoding), limits (maxSaleQuantity, minSaleQuantity, foldSaleQuantity), packageType (Piece/Weight).

**PriceData:** productId, price (копейки), discountPrice, pricePerKg, discountPricePerKg.

### Заказы (Order)

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/v1/order/get-time-slots` | Ближайшие слоты для корзины |
| POST | `/v1/order` | Создание неподтверждённого заказа |
| GET | `/v1/order/{extOrderId}/query` | Информация о заказе |
| DELETE | `/v1/order/{extOrderId}/cancel` | Отмена заказа |
| GET | `/order/{extOrderId}/status` | Актуальный статус заказа |
| PUT | `/order/{extOrderId}/courier` | Обновление информации о курьере |

**Статусы заказа:** Created → Accepted → Picking → ReadyToDelivery → InDelivery → Finished / Cancelled

**CreateOrderRequest:** customer (clientKey, city, mobile, name), timeSlotId, orderLines (productId, quantity, weight, packageType, price, discountPrice, totalPrice), originalOrderId, totalDiscountPrice, totalPrice, storeId, orderAdjustmentBehavior (Hide/CallOrTrust/CallOrHide/Trust).

**Время:** слоты передаются в RFC3339 формате (`2020-03-21T15:00:00.000+03:00`).

### Остатки (Stock)

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/v1/stores/{storeId}/stocks` | Остатки товаров склада |

### Склады (Store)

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/v1/stores/query` | Информация по всем складам |
| GET | `/v1/store/delivery` | Информация о доставке |

**Store:** storeId, name, type (HM — гипермаркет / SM — супермаркет), window (open/close — unix time), suspended, limits (maxOrderAmount, maxBasketWeight, minOrderPriceAmount).

## Типы ошибок

| Код | Описание |
|-----|----------|
| WrongTimeslot (3003) | Некорректное время доставки |
| TimeSlotReservationFailed (3034) | Ошибка резервирования слота |
| TimeSlotNotFound (3035) | Интервал недоступен |
| TimeslotExpired (3022) | Истёк срок жизни интервала |
| NotEnoughStock (3005/3017) | Товара нет в наличии |
| Overweight (3014) | Превышен максимальный вес |
| OrderNotFound (6030) | Заказ не найден |
| MaxSumLimit (3019) | Превышена макс. сумма заказа |

## Особенности для реализации

- Все цены в **копейках** (integer), не в рублях
- Вес товаров в **граммах**
- Тип товара: `Piece` (штучный) или `Weight` (весовой)
- `productId` — строка (SKU)
- Маркировка `Честный знак`: datamatrix доступен после сборки заказа
- Courier info: имя, тип (pedestrian/bicycle/vehicle/motorcycle/electric_bicycle/rover), телефон, статус (assigned/accepted_order/arrived_to_place/has_taken_order), maxPlaceArrivalTime
- Отмена заказа: можно передать reason и comment
