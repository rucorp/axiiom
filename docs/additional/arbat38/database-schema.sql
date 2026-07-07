-- ============================================
-- ARBAT 38 - DATABASE SCHEMA
-- Система электронных ваучеров и ресторанный маркетплейс
-- PostgreSQL
-- ============================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- 1. AIRPORTS (Аэропорты)
-- ============================================
CREATE TABLE airports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(10) UNIQUE NOT NULL,           -- SVO, VKO, DME
    name VARCHAR(100) NOT NULL,                 -- Шереметьево
    city VARCHAR(100) NOT NULL,                 -- Москва
    latitude DECIMAL(10, 8),                    -- Геолокация
    longitude DECIMAL(11, 8),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 2. TERMINALS (Терминалы)
-- ============================================
CREATE TABLE terminals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    airport_id UUID REFERENCES airports(id) ON DELETE CASCADE,
    code VARCHAR(10) NOT NULL,                  -- B, C, A
    name VARCHAR(100),                          -- Терминал B
    UNIQUE(airport_id, code)
);

-- ============================================
-- 3. AIRPORT_STAFF (Сотрудники аэропорта)
-- ============================================
CREATE TABLE airport_staff (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    airport_id UUID REFERENCES airports(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(50) DEFAULT 'staff',          -- staff, supervisor
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 4. RESTAURANTS (Рестораны)
-- ============================================
CREATE TABLE restaurants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    terminal_id UUID REFERENCES terminals(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    brand_name VARCHAR(100),                    -- BLACK STAR BURGER
    cuisine_type VARCHAR(100),                  -- Бургеры, Паб
    description TEXT,
    phone VARCHAR(20),
    email VARCHAR(255),
    rating DECIMAL(3, 2) DEFAULT 0,
    avg_delivery_time INTEGER,                  --分钟
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 5. RESTAURANT_MANAGERS (Менеджеры ресторанов)
-- ============================================
CREATE TABLE restaurant_managers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    restaurant_id UUID REFERENCES restaurants(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 6. MENU_CATEGORIES (Категории меню)
-- ============================================
CREATE TABLE menu_categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    restaurant_id UUID REFERENCES restaurants(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,                 -- Бургеры, Напитки
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 7. MENU_ITEMS (Позиции меню)
-- ============================================
CREATE TABLE menu_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    category_id UUID REFERENCES menu_categories(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    image_url VARCHAR(500),
    is_available BOOLEAN DEFAULT true,
    is_alcohol BOOLEAN DEFAULT false,           -- Для правил ваучеров
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 8. DELAYS (Задержки рейсов)
-- ============================================
CREATE TABLE flight_delays (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    airport_id UUID REFERENCES airports(id),
    flight_number VARCHAR(20) NOT NULL,         -- SU 1234
    destination VARCHAR(100),                   -- Санкт-Петербург
    scheduled_departure TIMESTAMP NOT NULL,
    actual_departure TIMESTAMP,
    delay_hours DECIMAL(4, 2),                  -- 4.5 часов
    passengers_count INTEGER,
    status VARCHAR(50) DEFAULT 'active',       -- active, completed, cancelled
    created_by UUID REFERENCES airport_staff(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 9. VOUCHERS (Ваучеры)
-- ============================================
CREATE TABLE vouchers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    delay_id UUID REFERENCES flight_delays(id) ON DELETE CASCADE,
    voucher_code VARCHAR(50) UNIQUE NOT NULL,   -- VCH-123456789
    passenger_flight_number VARCHAR(20),        -- SU 1234
    passenger_boarding_pass VARCHAR(20),        -- 12A
    passenger_last_name VARCHAR(100),
    voucher_type VARCHAR(50) NOT NULL,          -- water, food
    amount DECIMAL(10, 2) NOT NULL,             -- 500.00
    valid_from TIMESTAMP DEFAULT NOW(),
    valid_until TIMESTAMP NOT NULL,
    status VARCHAR(50) DEFAULT 'active',       -- active, redeemed, expired, cancelled
    redeemed_at TIMESTAMP,
    redeemed_by UUID REFERENCES restaurant_managers(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Index for quick voucher lookup
CREATE INDEX idx_vouchers_code ON vouchers(voucher_code);
CREATE INDEX idx_vouchers_status ON vouchers(status);
CREATE INDEX idx_vouchers_delay ON vouchers(delay_id);

-- ============================================
-- 10. PASSENGERS (Пассажиры)
-- ============================================
CREATE TABLE passengers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone VARCHAR(20) UNIQUE,                   -- Для авторизации
    email VARCHAR(255) UNIQUE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    bonus_balance INTEGER DEFAULT 0,            -- Бонусные баллы
    loyalty_level VARCHAR(50) DEFAULT 'basic', -- basic, gastrosset, vip
    accrual_rate DECIMAL(5, 2) DEFAULT 7.00,    -- 7% начисление
    redemption_rate DECIMAL(5, 2) DEFAULT 50.00,-- 50% списание
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 11. ORDERS (Заказы)
-- ============================================
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    passenger_id UUID REFERENCES passengers(id),
    restaurant_id UUID REFERENCES restaurants(id),
    order_number VARCHAR(20) UNIQUE NOT NULL,   -- ORD-001
    status VARCHAR(50) DEFAULT 'new',          -- new, accepted, preparing, ready, completed, cancelled
    total_amount DECIMAL(10, 2) NOT NULL,
    voucher_discount DECIMAL(10, 2) DEFAULT 0,
    bonus_discount DECIMAL(10, 2) DEFAULT 0,
    final_amount DECIMAL(10, 2) NOT NULL,       -- Итого к оплате
    payment_method VARCHAR(50),                -- card, apple_pay, google_pay
    payment_status VARCHAR(50) DEFAULT 'pending',-- pending, paid, refunded
    pickup_time TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 12. ORDER_ITEMS (Позиции заказа)
-- ============================================
CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    menu_item_id UUID REFERENCES menu_items(id),
    item_name VARCHAR(150) NOT NULL,            -- Snapshot
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,              -- Price at order time
    total DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 13. VOUCHER_USAGE (Использование ваучеров в заказах)
-- ============================================
CREATE TABLE voucher_usage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    voucher_id UUID REFERENCES vouchers(id) ON DELETE CASCADE,
    amount_used DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 14. BONUS_TRANSACTIONS (Транзакции бонусов)
-- ============================================
CREATE TABLE bonus_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    passenger_id UUID REFERENCES passengers(id),
    order_id UUID REFERENCES orders(id),
    transaction_type VARCHAR(50) NOT NULL,      -- earned, spent, expired, adjusted
    amount INTEGER NOT NULL,                    -- +100 or -50
    balance_after INTEGER NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 15. FAVORITES (Избранные рестораны)
-- ============================================
CREATE TABLE passenger_favorites (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    passenger_id UUID REFERENCES passengers(id) ON DELETE CASCADE,
    restaurant_id UUID REFERENCES restaurants(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(passenger_id, restaurant_id)
);

-- ============================================
-- 16. SYSTEM_SETTINGS (Настройки системы)
-- ============================================
CREATE TABLE system_settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    description TEXT,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Default settings
INSERT INTO system_settings (setting_key, setting_value, description) VALUES
('delay_hours_for_water', '2', 'Минимальная задержка для выдачи воды (часы)'),
('delay_hours_for_food', '4', 'Минимальная задержка для выдачи горячего питания (часы)'),
('voucher_amount_water', '150', 'Сумма ваучера на воду (₽)'),
('voucher_amount_food', '500', 'Сумма ваучера на горячее питание (₽)'),
('voucher_valid_hours', '24', 'Срок действия ваучера (часы)'),
('bonus_accrual_rate', '7', 'Процент начисления бонусов'),
('bonus_redemption_rate', '50', 'Процент списания бонусов');

-- ============================================
-- 17. ADMIN_USERS (Суперадминистраторы)
-- ============================================
CREATE TABLE admin_users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(50) DEFAULT 'admin',          -- admin, superadmin
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================
CREATE INDEX idx_delays_flight ON flight_delays(flight_number);
CREATE INDEX idx_delays_status ON flight_delays(status);
CREATE INDEX idx_orders_passenger ON orders(passenger_id);
CREATE INDEX idx_orders_restaurant ON orders(restaurant_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_menu_items_category ON menu_items(category_id);
CREATE INDEX idx_bonus_transactions_passenger ON bonus_transactions(passenger_id);

-- ============================================
-- VIEWS FOR REPORTING
-- ============================================

-- Active vouchers view
CREATE VIEW active_vouchers AS
SELECT 
    v.*,
    d.flight_number,
    d.destination,
    a.code as airport_code,
    a.name as airport_name
FROM vouchers v
JOIN flight_delays d ON v.delay_id = d.id
JOIN airports a ON d.airport_id = a.id
WHERE v.status = 'active' AND v.valid_until > NOW();

-- Order statistics view
CREATE VIEW order_statistics AS
SELECT 
    r.id as restaurant_id,
    r.name as restaurant_name,
    a.code as airport_code,
    COUNT(o.id) as total_orders,
    SUM(o.final_amount) as total_revenue,
    AVG(o.final_amount) as avg_order_value,
    COUNT(CASE WHEN o.status = 'completed' THEN 1 END) as completed_orders
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.id
JOIN terminals t ON r.terminal_id = t.id
JOIN airports a ON t.airport_id = a.id
WHERE o.payment_status = 'paid'
GROUP BY r.id, r.name, a.code;

-- ============================================
-- TRIGGERS FOR UPDATED_AT
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_airports_updated_at BEFORE UPDATE ON airports
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_restaurants_updated_at BEFORE UPDATE ON restaurants
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_menu_items_updated_at BEFORE UPDATE ON menu_items
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_vouchers_updated_at BEFORE UPDATE ON vouchers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- SAMPLE DATA
-- ============================================

-- Airports
INSERT INTO airports (code, name, city) VALUES
('SVO', 'Шереметьево', 'Москва'),
('VKO', 'Внуково', 'Москва'),
('DME', 'Домодедово', 'Москва');

-- Terminals
INSERT INTO terminals (airport_id, code, name) VALUES
((SELECT id FROM airports WHERE code = 'SVO'), 'B', 'Терминал B'),
((SELECT id FROM airports WHERE code = 'SVO'), 'C', 'Терминал C'),
((SELECT id FROM airports WHERE code = 'VKO'), 'A', 'Терминал A');

-- Restaurants
INSERT INTO restaurants (terminal_id, name, brand_name, cuisine_type) VALUES
((SELECT id FROM terminals WHERE code = 'B' LIMIT 1), 'BLACK STAR BURGER', 'BLACK STAR BURGER', 'Бургеры'),
((SELECT id FROM terminals WHERE code = 'C' LIMIT 1), 'MO!BAR', 'MO!BAR', 'Бар'),
((SELECT id FROM terminals WHERE code = 'A' LIMIT 1), 'THE IRISH BAR', 'THE IRISH BAR', 'Паб');

-- ============================================
-- COMMENTS
-- ============================================
COMMENT ON TABLE airports IS 'Аэропорты, где работают рестораны Arbat 38';
COMMENT ON TABLE vouchers IS 'Электронные ваучеры для пассажиров при задержках';
COMMENT ON TABLE orders IS 'Заказы на предзаказ еды из ресторанов';
COMMENT ON TABLE bonus_transactions IS 'История начислений и списаний бонусов';
