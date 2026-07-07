# ARBAT 38 - API Documentation

## Base URL
```
https://api.arbat38.ru/v1
```

## Authentication
- **JWT Token** для сотрудников и менеджеров
- **Phone Session** для пассажиров

---

## 🔐 AUTHENTICATION

### POST /auth/login
Вход для сотрудников/менеджеров/админов

**Request:**
```json
{
  "email": "staff@airport.ru",
  "password": "password123",
  "role": "airport_staff"  // airport_staff, restaurant_manager, admin
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "uuid",
    "email": "staff@airport.ru",
    "first_name": "Иван",
    "last_name": "Иванов",
    "role": "staff",
    "airport_id": "uuid"
  }
}
```

### POST /auth/passenger/login
Вход пассажира по номеру телефона

**Request:**
```json
{
  "phone": "+79991234567"
}
```

**Response:**
```json
{
  "session_id": "uuid",
  "message": "SMS code sent"
}
```

### POST /auth/passenger/verify
Подтверждение SMS кода

**Request:**
```json
{
  "phone": "+79991234567",
  "code": "123456"
}
```

**Response:**
```json
{
  "session_token": "uuid",
  "passenger": {
    "id": "uuid",
    "phone": "+79991234567",
    "first_name": "Михаил",
    "bonus_balance": 3723,
    "loyalty_level": "gastrosset"
  }
}
```

---

## 🎫 VOUCHERS (Ваучеры)

### POST /vouchers/create
Создать ваучеры для рейса (только airport_staff)

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "flight_number": "SU 1234",
  "destination": "Санкт-Петербург",
  "passengers_count": 180,
  "voucher_type": "food",  // water, food
  "amount": 500,
  "valid_hours": 24
}
```

**Response:**
```json
{
  "delay_id": "uuid",
  "vouchers_created": 180,
  "qr_code_url": "https://api.arbat38.ru/qr/delay-uuid",
  "message": "Vouchers created successfully"
}
```

### GET /vouchers/:voucher_code
Получить информацию о ваучере

**Response:**
```json
{
  "voucher_code": "VCH-123456789",
  "type": "food",
  "amount": 500,
  "status": "active",  // active, redeemed, expired
  "flight_number": "SU 1234",
  "passenger_last_name": "Иванов",
  "valid_until": "2026-04-16T23:59:59Z",
  "airport_code": "SVO"
}
```

### POST /vouchers/:voucher_code/redeem
Погасить ваучер (только restaurant_manager)

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "message": "Voucher redeemed successfully",
  "amount": 500,
  "redeemed_at": "2026-04-15T14:30:00Z"
}
```

### GET /vouchers/passenger/:phone
Получить активные ваучеры пассажира

**Response:**
```json
{
  "vouchers": [
    {
      "voucher_code": "VCH-123456789",
      "type": "food",
      "amount": 500,
      "status": "active",
      "flight_number": "SU 1234",
      "valid_until": "2026-04-16T23:59:59Z"
    }
  ]
}
```

---

## ✈️ FLIGHTS (Рейсы)

### GET /flights/delays/active
Получить активные задержки рейсов

**Query Parameters:**
- `airport_code` (optional): SVO, VKO, DME
- `status` (optional): active, completed

**Response:**
```json
{
  "delays": [
    {
      "id": "uuid",
      "flight_number": "SU 1234",
      "destination": "Санкт-Петербург",
      "delay_hours": 4.5,
      "passengers_count": 180,
      "vouchers_issued": 145,
      "vouchers_redeemed": 98,
      "status": "active"
    }
  ]
}
```

### POST /flights/delays
Создать запись о задержке

**Request:**
```json
{
  "airport_id": "uuid",
  "flight_number": "SU 1234",
  "destination": "Санкт-Петербург",
  "scheduled_departure": "2026-04-15T10:00:00Z",
  "delay_hours": 4.5,
  "passengers_count": 180
}
```

---

## 🍽️ RESTAURANTS (Рестораны)

### GET /restaurants
Получить список ресторанов

**Query Parameters:**
- `airport_code`: SVO (required)
- `terminal_code`: B, C (optional)
- `cuisine_type`: Бургеры, Паб (optional)

**Response:**
```json
{
  "restaurants": [
    {
      "id": "uuid",
      "name": "BLACK STAR BURGER",
      "brand_name": "BLACK STAR BURGER",
      "cuisine_type": "Бургеры",
      "rating": 4.5,
      "avg_delivery_time": 20,
      "terminal": "B",
      "airport": "SVO"
    }
  ]
}
```

### GET /restaurants/:id
Информация о ресторане

**Response:**
```json
{
  "id": "uuid",
  "name": "BLACK STAR BURGER",
  "description": "...",
  "phone": "+7 (495) 123-45-67",
  "rating": 4.5,
  "avg_delivery_time": 20,
  "terminal": {
    "code": "B",
    "name": "Терминал B"
  },
  "airport": {
    "code": "SVO",
    "name": "Шереметьево"
  }
}
```

---

## 📋 MENU (Меню)

### GET /restaurants/:id/menu
Получить меню ресторана

**Response:**
```json
{
  "restaurant_id": "uuid",
  "categories": [
    {
      "id": "uuid",
      "name": "Бургеры",
      "items": [
        {
          "id": "uuid",
          "name": "Classic Burger",
          "description": "Говядина, чеддер, салат, томат",
          "price": 690,
          "image_url": "https://...",
          "is_available": true,
          "is_alcohol": false
        }
      ]
    }
  ]
}
```

### POST /menu/items
Добавить позицию в меню (restaurant_manager)

**Request:**
```json
{
  "category_id": "uuid",
  "name": "New Burger",
  "description": "Описание",
  "price": 790,
  "image_url": "https://...",
  "is_alcohol": false
}
```

### PUT /menu/items/:id
Обновить позицию меню

### DELETE /menu/items/:id
Удалить позицию меню

---

## 🛒 ORDERS (Заказы)

### POST /orders
Создать заказ

**Headers:**
```
X-Session-Token: <passenger_session>
```

**Request:**
```json
{
  "restaurant_id": "uuid",
  "items": [
    {
      "menu_item_id": "uuid",
      "quantity": 2
    },
    {
      "menu_item_id": "uuid",
      "quantity": 1
    }
  ],
  "pickup_time": "2026-04-15T15:00:00Z",
  "voucher_code": "VCH-123456789",  // optional
  "use_bonuses": true,  // optional
  "payment_method": "card"
}
```

**Response:**
```json
{
  "order_id": "uuid",
  "order_number": "ORD-001",
  "total_amount": 1960,
  "voucher_discount": 500,
  "bonus_discount": 100,
  "final_amount": 1360,
  "payment_url": "https://yookassa.ru/pay/...",
  "status": "pending_payment"
}
```

### GET /orders
Получить заказы пассажира

**Response:**
```json
{
  "orders": [
    {
      "id": "uuid",
      "order_number": "ORD-001",
      "restaurant_name": "BLACK STAR BURGER",
      "status": "preparing",  // new, accepted, preparing, ready, completed
      "total_amount": 1960,
      "final_amount": 1360,
      "pickup_time": "2026-04-15T15:00:00Z",
      "created_at": "2026-04-15T14:30:00Z"
    }
  ]
}
```

### GET /orders/:id
Детали заказа

**Response:**
```json
{
  "id": "uuid",
  "order_number": "ORD-001",
  "restaurant": {
    "name": "BLACK STAR BURGER",
    "terminal": "B"
  },
  "items": [
    {
      "name": "Classic Burger",
      "quantity": 2,
      "price": 690,
      "total": 1380
    }
  ],
  "total_amount": 1960,
  "voucher_discount": 500,
  "bonus_discount": 100,
  "final_amount": 1360,
  "status": "preparing",
  "pickup_time": "2026-04-15T15:00:00Z"
}
```

### PUT /orders/:id/status
Обновить статус заказа (restaurant_manager)

**Request:**
```json
{
  "status": "preparing"  // accepted, preparing, ready, completed
}
```

---

## 💰 BONUSES (Бонусы)

### GET /passenger/bonuses
Получить баланс и историю бонусов

**Response:**
```json
{
  "balance": 3723,
  "loyalty_level": "gastrosset",
  "accrual_rate": 7,
  "redemption_rate": 50,
  "transactions": [
    {
      "id": "uuid",
      "type": "earned",  // earned, spent, expired
      "amount": 100,
      "balance_after": 3723,
      "description": "Начислено за заказ ORD-001",
      "created_at": "2026-04-15T14:30:00Z"
    }
  ]
}
```

---

## 👤 PASSENGERS (Пассажиры)

### GET /passenger/profile
Получить профиль пассажира

**Response:**
```json
{
  "id": "uuid",
  "phone": "+79991234567",
  "first_name": "Михаил",
  "last_name": "Иванов",
  "bonus_balance": 3723,
  "loyalty_level": "gastrosset",
  "orders_count": 4,
  "favorites_count": 12
}
```

### PUT /passenger/profile
Обновить профиль

### GET /passenger/favorites
Получить избранные рестораны

### POST /passenger/favorites/:restaurant_id
Добавить в избранное

### DELETE /passenger/favorites/:restaurant_id
Удалить из избранного

---

## 📊 STATISTICS (Статистика)

### GET /admin/statistics/vouchers
Статистика по ваучерам (admin)

**Query Parameters:**
- `from`: 2026-04-01
- `to`: 2026-04-30
- `airport_code`: SVO (optional)

**Response:**
```json
{
  "total_created": 2847,
  "total_redeemed": 1923,
  "redemption_rate": 67.5,
  "total_amount": 962000,
  "by_airport": [
    {
      "airport_code": "SVO",
      "created": 1234,
      "redeemed": 845,
      "amount": 422500
    }
  ],
  "by_day": [
    {
      "date": "2026-04-15",
      "created": 147,
      "redeemed": 98
    }
  ]
}
```

### GET /admin/statistics/orders
Статистика по заказам (admin)

### GET /admin/statistics/restaurants
Статистика по ресторанам

---

## 🔔 NOTIFICATIONS (Уведомления)

### POST /notifications/push
Отправить push-уведомление

**Request:**
```json
{
  "passenger_id": "uuid",
  "title": "Заказ готов",
  "body": "Ваш заказ ORD-001 готов к выдаче",
  "data": {
    "order_id": "uuid",
    "type": "order_ready"
  }
}
```

---

## ❌ ERROR RESPONSES

### 400 Bad Request
```json
{
  "error": "validation_error",
  "message": "Invalid phone number",
  "details": {
    "phone": "Must be in format +7XXXXXXXXXX"
  }
}
```

### 401 Unauthorized
```json
{
  "error": "unauthorized",
  "message": "Invalid token"
}
```

### 403 Forbidden
```json
{
  "error": "forbidden",
  "message": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "error": "not_found",
  "message": "Voucher not found"
}
```

### 422 Unprocessable Entity
```json
{
  "error": "unprocessable",
  "message": "Voucher already redeemed"
}
```

### 500 Internal Server Error
```json
{
  "error": "internal_error",
  "message": "Something went wrong"
}
```

---

## 🔒 RATE LIMITING

- **Public endpoints:** 100 requests per minute
- **Authenticated endpoints:** 500 requests per minute
- **Payment endpoints:** 10 requests per minute

---

## 📝 NOTES

1. **Voucher Rules:**
   - One voucher per flight per type per passenger
   - Cannot be used for alcohol
   - Valid for 24 hours or until flight departure
   - Airport-specific

2. **Bonus Rules:**
   - Earned only on card payment portion
   - 7% accrual rate
   - 50% redemption rate
   - Cannot be used to pay for vouchers

3. **Order Flow:**
   ```
   new → accepted → preparing → ready → completed
   ```

4. **Payment Integration:**
   - YooKassa or T-Bank
   - Support for Apple Pay, Google Pay
   - Webhook for payment confirmation
