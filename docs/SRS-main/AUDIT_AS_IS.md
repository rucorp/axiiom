# Текущее состояние системы (AS IS)

**Источник:** §9.5 SRS-v2.md. Данные получены из `rewiew/schema.rb`, `rewiew/structure.sql` (PostgreSQL 16.6), `rewiew/swagger.json` (API V10), `references/github/` и опроса команды.

## 1. База данных

### Общая характеристика

| Параметр | Значение |
|---|---|
| **СУБД** | PostgreSQL 16.6 |
| **Количество таблиц** | 178 |
| **Количество enum-типов** | 51 |
| **Количество aasm_state (статусные машины)** | 25 (orders, items, payment_states, returned_orders, employees и др.) |
| **Аудит изменений** | logidze (триггеры) + PaperTrail (таблица `versions`) |
| **Расширения PG** | `btree_gin`, `citext`, `hstore`, `intarray`, `ltree`, `pg_trgm`, `pgcrypto`, `plpgsql`, `pageinspect`, `pg_stat_statements` |
| **Geo-данные** | Нет PostGIS (координаты хранятся как `float latitude`/`float longitude`) |
| **Метод миграций** | Rails schema.rb + structure.sql (логический дамп) |
| **Схема** | Единая БД (public), монолит |

### Архитектура каталога

Трёхуровневая модель с STI:

**brands** → **models** (type: 'piece'/'weight'/…) → **products** (shop_id + model_id + price)

```ruby
# Бренд (производитель)
brands: id, name, slug

# Товарная позиция (абстрактная)
models: id, category_id, type (STI: piece/weight/…), name, weight, volume,
        calories, proteins, fats, carbohydrates, composition, manufacturer, expire_at

# Товар в конкретном магазине
products: id, shop_id, model_id, category_id, price, price_per_kg, vat,
          available, sale, hidden, missing_count, orders_count
```

### Магазины

```ruby
shops: id, name, street, building, latitude, longitude, phone, inn, okved, okpo, kpp,
       bank_name, current_account, account_number, bik, ogrn, open_hour, closing_hour,
       day_and_night, open
```

Сети магазинов — поле `shop_group` (enum `shop_group_enum`):

`metro`, `lenta`, `karusel`, `prisma`, `spar`, `babylon`, `land`, `vkusvill`, `globus`, `selgros`, `magnit`, `azbukavkusa`, `auchan`, `okmarket`, `billa`, `dona`

### Заказы

```ruby
orders: id, shop_id, user_id, place_id, deliver_at, phone, payment_type,
        change_from, behavior (enum), aasm_state, picker_id, picker_cell,
        courier_id, courier_returning, delivery_price, user_email, inviter_id,
        filled_at
```

Статусы заказа (aasm_state, 25+ переходов): через `logidze` логируется вся история.

### Позиции заказа

```ruby
items: id, order_id, product_id, category_id, root_category_id, replacement_id,
       amount, aasm_state, added_at, missing_at, replacement_at
```

### Пользователи

```ruby
users: id, first_name, last_name, patronymic, email (citext),
       encrypted_password, reset_password_token, confirmation_token, phone,
       unconfirmed_phone, confirmation_code, behavior (enum), failed_attempts,
       locked_at, unlock_token, sign_in_count, remember_created_at, ...
```

**Аутентификация:** Sorcery (Rails gem). Поля: `encrypted_password`, `confirmation_token`, `reset_password_token`, `failed_attempts`, `locked_at`. RBAC: access-granted.

Типы пользователей (enum `user_type_enum`):

`User`, `JoomUser`, `AliexpressUser`, `ExternalUser`, `KomusUser`

### Платежи

Платёжные провайдеры (enum `order_payment_provider`):

`tinkoff`, `pskb`, `joom`, `cloud_payments`, `aliexpress`, `yandex_eda`

```ruby
payment_states: id, order_id, bank_card_id, aasm_state, custom_data (JSONB)
```

Apple Pay / Google Pay — через CloudPayments (таблица `cloud_payments`).

```ruby
cloud_payments: id, order_id (используется для ApplePay и GooglePay)
bank_cards: id, user_id, provider (enum: tinkoff/cloud_payments), token
billing_transactions: id, order_id, type, amount, provider
```

### Возвраты

```ruby
returned_orders: id, order_id, aasm_state (returned_order_state_enum),
                 moderated_at, moderated_employee_id, comment,
                 returned_real_price_kop, box_number
returned_receipts: id, returned_order_id, photo, total
returned_items: id, returned_order_id, item_id, amount, aasm_state (returned_item_state_enum)
```

Статусы возврата (`returned_order_state_enum`): `created`, `on_moderation`, `on_picker`, `on_courier`, `closed`, `waiting_for_picker`

### Внешние интеграции

```ruby
external_meta: id, source_id, source_type (enum: Order/Item/Product/Shop/Category/Model),
               provider (enum: metro/aloe/yandex_eda/komus/vkusvill), payload (JSONB)
```

Розничные агрегаторы (enum `external_retailer_enum`): `aloe`

Источники внешних пользователей (enum `external_user_source_enum`): `yandex_eda`

### Доставка

```ruby
delivery_zones: id, shop_id, name, polygon (не GEOGRAPHY — текстовое или JSON)
delivery_plans: id, provider (enum: vee_route/simple/yandex/manual), shop_id,
                calculation_id, is_finished, plan_data (JSONB)
delivery_routes: id, delivery_plan_id, courier_id, route_data (JSONB)
delivery_eta_requests: id, order_id, eta_seconds, requested_at
courier_locations: id, order_id, latitude, longitude, distance
```

Провайдеры планирования доставки (`delivery_planning_providers_enum`):

`vee_route`, `simple`, `yandex`, `manual`

### Сотрудники (пикеры/курьеры)

```ruby
employees: id, user_id, first_name, last_name, role (enum: courier/picker),
           gender (enum), position_id
employee_positions: id, name, responsibilities
employee_payments: id, employee_id, amount, provider (enum: manual/rocketwork/tinkoff)
employee_contacts: id, employee_id, phone, email
employee_notifications: id, employee_id, domain (enum: delivery/collect), title, body
breaks: id, employee_id, start_at, stop_at
hours: id, employee_id, start_at, stop_at, comment
```

### Честный знак (маркировка)

```ruby
honest_label_types: id, name
honest_labels: id, model_id, honest_label_type_id, shop_group (enum)
```

### Прочие значимые таблицы

| Таблица | Назначение |
|---|---|
| `carts` | Корзины пользователей |
| `coupons`, `coupon_redemptions` | Промокоды и их активации |
| `accruals`, `accrual_types` | Баллы лояльности |
| `claims`, `claim_sources`, `claim_pictures` | Претензии/споры |
| `feedbacks`, `desktop_feedbacks` | Обратная связь |
| `favorite_models` | Избранные товары |
| `ab_tests`, `ab_test_participations`, `ab_test_orders_histories` | A/B тестирование |
| `blacklisted_phones` | Заблокированные номера |
| `callback_requests` | Запросы обратного звонка |
| `aliexpress_users` | Пользователи с Aliexpress |
| `external_users` | Внешние пользователи (Yandex.Eda и др.) |
| `events` | Логи событий |

## 2. API

| Параметр | Значение |
|---|---|
| **Тип** | Монолит Rails, REST JSON API |
| **Версия** | V10 (`/api/v10/`) |
| **Эндпоинтов** | 100 |
| **Формат** | JSON |
| **Swagger** | `rewiew/swagger.json` (OpenAPI 3.0.3) |
| **Servers** | `http://igooods.test` (dev), `https://master.jira.igooods.ru` (staging) |
| **Аутентификация** | Не видна из swagger (вероятно, cookie + Sorcery session) |

### Разделы API

| Эндпоинтов | Раздел |
|---|---|
| 21 | Заказы (orders) |
| 10 | Корзина (cart) |
| 10 | Каталог (catalog/shops) |
| 10 | Пользователи (users) |
| 9 | Подборки товаров |
| 7 | Общая корзина |
| 7 | Магазины |
| 5 | Карты (банковские) |
| 5 | Товары в заказе |
| 5 | Наборы товаров |
| 4 | Города |
| 4 | Адреса |
| 3 | Избранные товары |
| 2 | A/B тестирование |
| 2 | Обратная связь |
| 2 | Регистрация |
| 1 | Рефералы, Лендинги, Логирование, Метакаталог, Мобильные сборки, Новостные баннеры |

## 3. Технологический стек

| Компонент | Текущая версия |
|---|---|
| **Backend** | Ruby on Rails 7.0 (монолит) |
| **Ruby** | 3.x (предположительно, по совместимости с Rails 7.0) |
| **База данных** | PostgreSQL 16.6 |
| **Очереди** | RabbitMQ |
| **Кэш** | Redis |
| **Frontend** | Next.js (версия неизвестна) |
| **Mobile** | Flutter (пикер/курьер), нативные? (клиент) |
| **Аутентификация** | Sorcery + access-granted (RBAC) |
| **Загрузка файлов** | Carrierwave + MiniMagick |
| **Аудит** | logidze (триггеры) + PaperTrail (таблица `versions`) |
| **Инфраструктура** | Docker Compose |
| **Хостинг** | Selectel |
| **CI/CD** | GitHub Actions |

## 4. Алгоритмы и бизнес-логика

### Назначение курьеров (Dispatch)

Курьеры закреплены за конкретным гипермаркетом и зоной доставки. Ручная переброска между зонами при высокой загрузке или невыходе на смену.

Планирование маршрутов: через `delivery_plans` с провайдерами `vee_route`, `simple`, `yandex` или `manual`.

Плановый dispatch engine (multi-objective optimization) — на V3.

### Расчёт ETA

`delivery_eta_requests` — таблица для запросов ETA.
`courier_locations` — трекинг в реальном времени (координаты, дистанция).

Согласно AUDIT: гибрид OSRM + XGBoost (13 признаков: погода, трафик, время суток, праздники, день недели, дистанция, кол-во стопов). Пересчёт каждые 5 мин.

### Обновление каталога и остатков

Два процесса:
1. **Обновление каталога** — загрузка ассортимента, цен, акций от сети через `external_meta` (provider: metro/aloe/yandex_eda/komus/vkusvill)
2. **Остатки в конкретном магазине** — запрос остатков по API магазина (если доступно), иначе сканер пикера на месте

### Замены товаров

Через `items.replacement_id` (ссылка на товар-замену). Пикер звонит клиенту (скрытый номер), предлагает альтернативы, клиент подтверждает устно, замена фиксируется.

Статусы `items.aasm_state`: `added` → `missing` (нет в наличии) → `replaced` (согласована замена).

### Честный знак

Маркированные товары имеют запись в `honest_labels` (model_id + shop_group + honest_label_type_id). Не все сети поддерживают. В MVP не доставляются.

## 5. Платежи

| Провайдер | Механизм |
|---|---|
| **Tinkoff** | `bank_cards` (provider: tinkoff), `payment_states` с aasm_state |
| **CloudPayments** | `cloud_payments` (ApplePay/GooglePay), `bank_cards` (provider: cloud_payments) |
| **PSKB** | `order_payment_provider` enum |
| **Joom** | `order_payment_provider` enum |
| **Aliexpress** | `order_payment_provider` enum, `aliexpress_users` |
| **Yandex.Eda** | `order_payment_provider` enum, `external_users` |

Двойная система: `payment_states` (aasm_state + custom_data JSONB) + `payment_events` (api/callback).

## 6. Состав команды

| Роль | Количество |
|---|---|
| Backend-разработчики | 2 |
| Frontend-разработчики | 2 |
| Mobile-разработчик | 1 |
| DevOps | 2 |
| QA | Нет выделенного (покрывается командой) |

## 7. Что требует уточнения

| Вопрос | Почему не удалось установить |
|---|---|
| Ruby версия | Нет Gemfile.lock, только Gemfile (Rails 5.1 из публичного репозитория). По Rails 7.0 — предполагается 3.x |
| Точные регионы покрытия | Нет данных о городах кроме очевидных (СПб, Мск по swagger) |
| Бизнес-метрики | Нет доступа к продакшену (заказов/день, выручка, средний чек) | ✅ Данные получены из CSV заказов за май 2026 — см. [business_model.md](business_model.md) |
| SLA | Нет документов |
| Инфраструктура (мощности серверов) | Нет данных |
| Версия Next.js / Flutter | В rewiew/ только бэкенд-файлы |
| Детали OSRM + XGBoost | Алгоритм описан со слов команды, код не представлен |
| Статус сетей selgros/magnit/azbukavkusa/auchan/okmarket/billa/dona | Есть в enum `shop_group_enum`, но неизвестно, активны ли интеграции |
