# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[7.0].define(version: 2025_12_23_100049) do
  # These are extensions that must be enabled in order to support this database
  enable_extension "btree_gin"
  enable_extension "citext"
  enable_extension "hstore"
  enable_extension "intarray"
  enable_extension "ltree"
  enable_extension "pageinspect"
  enable_extension "pg_stat_statements"
  enable_extension "pg_trgm"
  enable_extension "pgcrypto"
  enable_extension "plpgsql"

  # Custom types defined in this database.
  # Note that some types may not work with other database engines. Be careful if changing database.
  create_enum "apps_flyers_platform_enum", ["ios", "android", "web"]
  create_enum "bank_card_provider", ["tinkoff", "cloud_payments"]
  create_enum "behavior_enum", ["call_or_trust", "call_or_hide", "trust", "hide"]
  create_enum "claims_employee_role_enum", ["courier", "picker"]
  create_enum "cloud_payment_state_enum", ["pay_waiting", "pay_accepted", "pay_declined"]
  create_enum "coupon_marketing_type", ["marketing", "loyalty", "points_to_order", "points_to_user"]
  create_enum "coupons_discount_method", ["absolute", "percent"]
  create_enum "coupons_user_type", ["individual", "legal_entity", "any"]
  create_enum "courier_delivery_state", ["loading", "started", "returning", "finished"]
  create_enum "delivery_planning_providers_enum", ["vee_route", "simple", "yandex", "manual"]
  create_enum "employee_gender_enum", ["male", "female", "unknown"]
  create_enum "employee_notifications_domain_enum", ["delivery", "collect"]
  create_enum "employee_payment_providers", ["manual", "rocketwork", "tinkoff"]
  create_enum "external_meta_provider", ["metro", "aloe", "yandex_eda", "komus", "vkusvill"]
  create_enum "external_meta_source_type", ["Order", "Item", "Product", "Shop", "Category", "Model"]
  create_enum "external_retailer_enum", ["aloe"]
  create_enum "external_user_source_enum", ["yandex_eda"]
  create_enum "fields_seo_text_type_enum", ["none", "seo_text", "category_and_seo_text"]
  create_enum "google_analytics_apps_platform_enum", ["ios", "android", "web"]
  create_enum "invoice_report_status_enum", ["started", "completed", "no_orders", "fail"]
  create_enum "komus_accounts_type_enum", ["credit"]
  create_enum "label_type_enum", ["novelty", "hit", "promo"]
  create_enum "mobile_builds_domain_enum", ["clients", "delivery"]
  create_enum "mobile_builds_platform_type_enum", ["android", "ios", "huawei"]
  create_enum "model_limit_unit", ["gram", "piece"]
  create_enum "news_banner_kind", ["redirect", "text"]
  create_enum "notification_devices_platform_enum", ["android", "ios", "huawei"]
  create_enum "notification_devices_push_token_provider_enum", ["fcm", "onesignal"]
  create_enum "operator_payment_provider", ["tinkoff", "cloud_payments"]
  create_enum "order_payment_provider", ["tinkoff", "pskb", "joom", "cloud_payments", "aliexpress", "yandex_eda"]
  create_enum "order_user_permission_access_level", ["owner", "guest"]
  create_enum "partner_configurations_partner_identifier", ["komus"]
  create_enum "payment_events_kind", ["api", "callback"]
  create_enum "phone_devices_kind_enum", ["common", "couriers", "pickers"]
  create_enum "price_file_state_enum", ["wait", "shops_missing", "started", "completed", "fatal", "interrupted"]
  create_enum "product_prices_source_type", ["Employee", "PriceFile"]
  create_enum "product_set_platform_enum", ["any", "web", "mobile"]
  create_enum "returned_item_state_enum", ["created", "returned_to_shop", "someone_take", "utilisation", "employee_take"]
  create_enum "returned_order_assignment_status", ["pending", "active", "finished", "unassigned"]
  create_enum "returned_order_assignment_type", ["picker", "courier"]
  create_enum "returned_order_state_enum", ["created", "on_moderation", "on_picker", "on_courier", "closed", "waiting_for_picker"]
  create_enum "shop_brand_label", ["utkonos"]
  create_enum "shop_group_enum", ["metro", "lenta", "karusel", "prisma", "spar", "babylon", "land", "vkusvill", "globus", "selgros", "magnit", "azbukavkusa", "auchan", "okmarket", "billa", "dona"]
  create_enum "shop_orders_sort_type", ["by_readiness", "by_start_packing_deadline"]
  create_enum "tinkoff_terminal_transactions_type_enum", ["debit", "credit", "other"]
  create_enum "transaction_direction_enum", ["income", "outcome"]
  create_enum "trip_states_enum", ["created", "waiting_bank_confirmation", "confirmed", "waiting_bank_completion", "completed", "declined", "waiting_bank_payment", "paying_failed", "paid"]
  create_enum "user_comments_type", ["picker", "courier", "admin"]
  create_enum "user_deletion_request_status_enum", ["created", "cancelled", "cancelled_by_user", "executed"]
  create_enum "user_platform_selection_enum", ["any", "web", "mobile"]
  create_enum "user_type_enum", ["User", "JoomUser", "AliexpressUser", "ExternalUser", "KomusUser"]

  create_table "ab_test_orders_histories", force: :cascade do |t|
    t.bigint "ab_test_id", null: false
    t.bigint "user_id", null: false
    t.bigint "order_id", null: false
    t.bigint "shop_id", null: false
    t.string "group"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["user_id", "ab_test_id", "order_id"], name: "i_user_test_order_on_ab_test_orders_histories", unique: true
  end

  create_table "ab_test_participations", id: :serial, force: :cascade do |t|
    t.boolean "participating", default: false, null: false
    t.string "group"
    t.integer "ab_test_id"
    t.integer "user_id"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["ab_test_id", "user_id"], name: "index_ab_test_participations_on_ab_test_id_and_user_id", unique: true
    t.index ["user_id"], name: "index_ab_test_participations_on_user_id"
  end

  create_table "ab_tests", id: :serial, force: :cascade do |t|
    t.string "name"
    t.boolean "active", default: false, null: false
    t.string "groups", default: [], null: false, array: true
    t.index ["name"], name: "index_ab_tests_on_name", unique: true
  end

  create_table "ab_tests_cities_relations", id: false, force: :cascade do |t|
    t.integer "ab_test_id", null: false
    t.integer "city_id", null: false
    t.index ["ab_test_id", "city_id"], name: "index_ab_tests_cities_relations_on_ab_test_id_and_city_id", unique: true
  end

  create_table "accounts", id: :serial, force: :cascade do |t|
    t.integer "user_id", null: false
    t.integer "operator_id", null: false
    t.integer "balance", default: 0, null: false
    t.string "type", null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.date "expire_at"
    t.integer "expire_points_amount", default: 0
    t.integer "non_expire_points_amount", default: 0
    t.index ["operator_id"], name: "index_accounts_on_operator_id"
    t.index ["user_id", "operator_id", "type", "expire_at"], name: "index_accounts_on_uniq_check", unique: true
  end

  create_table "accrual_types", id: :serial, force: :cascade do |t|
    t.string "title", null: false
    t.text "description"
    t.string "kind", null: false
    t.boolean "enabled", default: false, null: false
    t.datetime "created_at", precision: nil
    t.datetime "updated_at", precision: nil
  end

  create_table "accruals", id: :serial, force: :cascade do |t|
    t.integer "employee_id", null: false
    t.integer "author_id", null: false
    t.integer "accrual_type_id", null: false
    t.datetime "accrual_at", precision: nil, null: false
    t.decimal "amount", precision: 10, scale: 2, null: false
    t.text "description"
    t.datetime "created_at", precision: nil
    t.datetime "updated_at", precision: nil
    t.uuid "public_id", default: -> { "public.gen_random_uuid()" }
    t.index ["accrual_type_id"], name: "index_accruals_on_accrual_type_id"
    t.index ["author_id"], name: "index_accruals_on_author_id"
    t.index ["employee_id"], name: "index_accruals_on_employee_id"
    t.index ["public_id"], name: "index_accruals_on_public_id", unique: true
  end

  create_table "aliexpress_users", id: :serial, force: :cascade do |t|
    t.string "first_name"
    t.string "last_name"
    t.string "patronymic"
    t.string "phone"
    t.integer "orders_count", default: 0
    t.string "comment", default: "", null: false
    t.string "kind", default: "mobile", null: false
    t.boolean "blocked"
    t.string "blocked_comment"
    t.datetime "blocked_at", precision: nil
    t.integer "blocked_employee_id"
    t.boolean "as_entity", default: false, null: false
    t.enum "behavior", enum_type: "behavior_enum"
    t.datetime "last_order_at", precision: nil
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["phone"], name: "index_aliexpress_users_on_phone", unique: true
  end

  create_table "areas", id: :serial, force: :cascade do |t|
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.polygon "polygon"
  end

  create_table "bank_cards", id: :serial, force: :cascade do |t|
    t.integer "user_id", null: false
    t.enum "bank", null: false, enum_type: "bank_card_provider"
    t.string "external_card_id"
    t.string "rebill_id"
    t.string "pan", null: false
    t.date "expire"
    t.boolean "enabled", default: true, null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.enum "user_type", default: "User", null: false, enum_type: "user_type_enum"
    t.index ["user_type", "user_id", "bank", "pan", "expire"], name: "index_bank_cards_on_most_fields", unique: true
  end

  create_table "billing_transactions", force: :cascade do |t|
    t.uuid "public_id", null: false
    t.bigint "employee_id", null: false
    t.string "franchisee_name"
    t.string "role"
    t.integer "debit", null: false
    t.integer "credit", null: false
    t.string "wallet_type"
    t.string "operation_type"
    t.boolean "is_fine", default: false
    t.string "status"
    t.text "description"
    t.jsonb "payload", default: {}, null: false
    t.string "provider"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["employee_id"], name: "index_billing_transactions_on_employee_id"
    t.index ["public_id"], name: "index_billing_transactions_on_public_id", unique: true
  end

  create_table "bills", force: :cascade do |t|
    t.integer "amount"
    t.bigint "entity_id"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["entity_id"], name: "index_bills_on_entity_id"
  end

  create_table "blacklisted_phones", force: :cascade do |t|
    t.string "msisdn", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["msisdn"], name: "index_blacklisted_phones_on_msisdn", unique: true
  end

  create_table "brands", id: :serial, force: :cascade do |t|
    t.string "name"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.string "slug"
    t.index ["slug"], name: "index_brands_on_slug"
  end

  create_table "breaks", id: :serial, force: :cascade do |t|
    t.integer "employee_id"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.boolean "active", default: true
    t.index ["employee_id", "created_at"], name: "index_breaks_on_employee_id_and_created_at"
  end

  create_table "cachboxes", id: :serial, force: :cascade do |t|
    t.string "cachbox_provider", null: false
    t.string "api_login", null: false
    t.string "api_key", null: false
    t.string "category", null: false
    t.integer "operator_id"
    t.datetime "created_at", precision: nil
    t.datetime "updated_at", precision: nil
    t.string "receipt_format", default: "ffd_1_05", null: false
    t.index ["operator_id"], name: "index_cachboxes_on_operator_id"
  end

  create_table "callback_requests", id: :serial, force: :cascade do |t|
    t.string "name"
    t.string "address"
    t.citext "email"
    t.string "phone_number"
    t.string "city_subdomain"
    t.datetime "created_at", precision: nil
    t.datetime "updated_at", precision: nil
  end

  create_table "carts", id: :serial, force: :cascade do |t|
    t.integer "user_id"
    t.integer "order_id", null: false
    t.integer "shop_id", null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.integer "delivery_zone_id"
    t.enum "user_type", default: "User", null: false, enum_type: "user_type_enum"
    t.index ["order_id"], name: "index_carts_on_order_id"
    t.index ["user_type", "user_id"], name: "index_carts_on_user_type_and_user_id"
  end

  create_table "categories", id: :serial, force: :cascade do |t|
    t.string "name"
    t.string "ancestry"
    t.integer "children_count", default: 0, null: false
    t.boolean "returnable", default: true, null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.boolean "adult"
    t.integer "position"
    t.boolean "novelty"
    t.boolean "xml_group", default: true, null: false
    t.string "image"
    t.boolean "block", default: false, null: false
    t.integer "low_cost_count"
    t.string "web_image"
    t.boolean "frost", default: false
    t.string "big_image"
    t.string "bg_web_image"
    t.boolean "check_passport", default: false, null: false
    t.jsonb "name_cases", default: {}, null: false
    t.boolean "hide_price_per_kg", default: false, null: false
    t.boolean "pharmacy_shop", default: false, null: false
    t.string "about_seller"
    t.boolean "can_use_for_checkout", default: false, null: false
    t.enum "external_retailer", enum_type: "external_retailer_enum"
    t.integer "min_piece_stock", default: 1
    t.integer "min_weight_stock", default: 1
    t.string "slug"
    t.bigint "category_group_id"
    t.float "weight_markup_percent", default: 0.0, null: false
    t.index ["ancestry"], name: "index_categories_on_ancestry"
    t.index ["category_group_id"], name: "index_categories_on_category_group_id"
    t.index ["position"], name: "index_categories_on_position"
    t.index ["slug"], name: "index_categories_on_slug"
    t.index ["updated_at"], name: "index_categories_on_updated_at"
  end

  create_table "categories_product_line_campaigns", id: false, force: :cascade do |t|
    t.integer "category_id"
    t.integer "product_line_campaign_id"
  end

  create_table "category_groups", force: :cascade do |t|
    t.string "name", null: false
    t.integer "position", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "cities", id: :serial, force: :cascade do |t|
    t.string "name", null: false
    t.string "country", null: false
    t.string "subdomain", null: false
    t.boolean "enabled", default: false, null: false
    t.float "latitude", null: false
    t.float "longitude", null: false
    t.text "city_kladr"
    t.text "region_kladr"
    t.integer "display_order", null: false
    t.datetime "created_at", precision: nil
    t.datetime "updated_at", precision: nil
    t.string "region_name"
    t.string "phone"
    t.integer "area_id"
    t.string "time_zone", null: false
    t.jsonb "social_networks", default: {"facebook"=>nil, "instagram"=>nil, "vkontakte"=>nil}
    t.uuid "fias_id"
    t.uuid "region_fias_id"
    t.integer "min_order_price", comment: "Minimal order price, if not set then used hardcode value, usually its 500 roubles"
    t.index ["name"], name: "index_cities_on_name"
    t.index ["subdomain"], name: "index_cities_on_subdomain", unique: true
  end

  create_table "claim_pictures", id: :serial, force: :cascade do |t|
    t.integer "claim_id"
    t.string "picture"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["claim_id"], name: "index_claim_pictures_on_claim_id"
  end

  create_table "claim_sources", force: :cascade do |t|
    t.string "name", null: false
  end

  create_table "claims", id: :serial, force: :cascade do |t|
    t.string "aasm_state", default: "opened"
    t.string "comment"
    t.integer "points", default: 0
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.integer "order_id"
    t.integer "product_ids", default: [], array: true
    t.string "kind"
    t.datetime "changed_state_at", precision: nil
    t.integer "changed_state_employee_id"
    t.string "types", default: [], array: true
    t.integer "claim_source_id", default: 1, null: false
    t.integer "creator_employee_id"
    t.string "employee_comment"
    t.datetime "closed_at", precision: nil
    t.string "solution_type"
    t.boolean "auto_created", default: false, null: false
    t.bigint "score_id"
    t.float "progress_time_in_seconds", default: 0.0
    t.datetime "reopened_at", precision: nil
    t.enum "employee_role", enum_type: "claims_employee_role_enum"
    t.integer "operator_id"
    t.integer "shop_id"
    t.index ["order_id"], name: "index_claims_on_order_id"
    t.index ["score_id"], name: "index_claims_on_score_id"
  end

  create_table "cloud_payments", id: :serial, comment: "ApplePay and GooglePay via CloudPayments", force: :cascade do |t|
    t.integer "order_id", null: false
    t.enum "aasm_state", null: false, enum_type: "cloud_payment_state_enum"
    t.string "message"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["order_id"], name: "index_cloud_payments_on_order_id"
  end

  create_table "coupon_redemptions", id: :serial, force: :cascade do |t|
    t.integer "coupon_id"
    t.integer "user_id"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.integer "cart_id"
    t.index ["cart_id"], name: "index_coupon_redemptions_on_cart_id"
    t.index ["coupon_id"], name: "index_coupon_redemptions_on_coupon_id"
    t.index ["user_id"], name: "index_coupon_redemptions_on_user_id"
  end

  create_table "coupons", id: :serial, force: :cascade do |t|
    t.citext "code", null: false
    t.string "prefix"
    t.boolean "multiple", default: true
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.integer "shipping_cost", default: 0
    t.date "start_at"
    t.date "expire_at"
    t.string "purpose"
    t.string "uuid"
    t.string "coverage"
    t.boolean "is_deleted", default: false
    t.integer "min_sum_order"
    t.integer "user_ids", default: [], array: true
    t.integer "city_id"
    t.integer "user_idle_days"
    t.text "description"
    t.integer "multiple_use_amount", default: 1
    t.enum "marketing_type", null: false, enum_type: "coupon_marketing_type"
    t.integer "operator_id", null: false
    t.integer "sum_points", default: 0
    t.integer "category_ids", default: [], null: false, array: true
    t.integer "min_sum_products"
    t.boolean "excludes_users", default: false
    t.enum "discount_method", enum_type: "coupons_discount_method"
    t.integer "shop_ids", default: [], array: true
    t.string "shop_groups", default: [], array: true
    t.boolean "show_in_cart_for_all", default: false, null: false
    t.enum "user_type", default: "individual", null: false, enum_type: "coupons_user_type"
    t.boolean "birthday", default: false
    t.index ["city_id"], name: "index_coupons_on_city_id"
    t.index ["code"], name: "index_coupons_on_code", unique: true
  end

  create_table "courier_locations", force: :cascade do |t|
    t.bigint "order_id", null: false
    t.float "latitude"
    t.float "longitude"
    t.float "distance"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["order_id"], name: "index_courier_locations_on_order_id"
  end

  create_table "courier_rate_resets", id: :serial, force: :cascade do |t|
    t.integer "shift_id", null: false
    t.string "reason", null: false
    t.boolean "enabled", null: false
    t.boolean "applicable", null: false
    t.integer "placed_orders_count", null: false
    t.integer "courier_orders", null: false
    t.datetime "created_at", precision: nil, default: -> { "now()" }, null: false
    t.datetime "updated_at", precision: nil, default: -> { "now()" }, null: false
    t.index ["shift_id"], name: "index_courier_rate_resets_on_shift_id"
  end

  create_table "day_schedule_presets", id: :serial, force: :cascade do |t|
    t.string "name"
    t.string "kind"
    t.integer "shop_id"
    t.datetime "time", precision: nil
    t.date "date"
    t.integer "duration"
    t.integer "position"
    t.string "color", default: "#919090"
    t.integer "order_count"
    t.integer "delivery_zone_id"
    t.integer "pre_period", default: 0
    t.integer "post_period", default: 0
    t.integer "action_period", default: 0
    t.boolean "archive", default: false
    t.datetime "created_at"
    t.datetime "updated_at"
    t.index ["name", "shop_id", "date", "position"], name: "line_uniquiness", unique: true
    t.index ["shop_id"], name: "index_day_schedule_presets_on_shop_id"
  end

  create_table "day_schedules", id: :serial, force: :cascade do |t|
    t.string "kind"
    t.integer "shop_id"
    t.datetime "time", precision: nil
    t.date "date"
    t.integer "duration"
    t.integer "position"
    t.integer "line"
    t.boolean "enabled", default: true
    t.string "color"
    t.integer "order_count"
    t.integer "delivery_zone_id"
    t.integer "pre_period", default: 0
    t.integer "post_period", default: 0
    t.integer "action_period", default: 0
    t.string "name"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.index ["date"], name: "index_day_schedules_on_date"
    t.index ["delivery_zone_id", "date", "time"], name: "index_day_schedules_on_delivery_zone_id_and_date_and_time"
    t.index ["shop_id", "date", "line", "position"], name: "index_day_schedules_on_shop_id_and_date_and_line_and_position", unique: true
  end

  create_table "delivery_eta_requests", force: :cascade do |t|
    t.string "calculation_id"
    t.boolean "is_finished", default: false, null: false
    t.bigint "delivery_route_id", null: false
    t.bigint "order_id", null: false
    t.datetime "time_from", precision: nil
    t.datetime "time_to", precision: nil
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["delivery_route_id"], name: "index_delivery_eta_requests_on_delivery_route_id"
    t.index ["order_id"], name: "index_delivery_eta_requests_on_order_id"
  end

  create_table "delivery_features", force: :cascade do |t|
    t.string "key", null: false
    t.boolean "value", default: true, null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
  end

  create_table "delivery_plan_extras", force: :cascade do |t|
    t.bigint "delivery_plan_id"
    t.datetime "historical_run_date", precision: nil
    t.index ["delivery_plan_id"], name: "index_delivery_plan_extras_on_delivery_plan_id"
  end

  create_table "delivery_plans", id: :serial, force: :cascade do |t|
    t.enum "provider", null: false, enum_type: "delivery_planning_providers_enum"
    t.integer "shop_id", null: false
    t.string "calculation_id"
    t.datetime "created_at", precision: nil
    t.datetime "updated_at", precision: nil
    t.boolean "is_finished", default: false, null: false
    t.jsonb "plan_data"
    t.index ["calculation_id"], name: "index_delivery_plans_on_calculation_id"
    t.index ["shop_id"], name: "index_delivery_plans_on_shop_id"
  end

  create_table "delivery_routes", id: :serial, force: :cascade do |t|
    t.integer "delivery_plan_id", null: false
    t.integer "courier_id", null: false
    t.enum "provider", null: false, enum_type: "delivery_planning_providers_enum"
    t.jsonb "route_data"
    t.datetime "created_at", precision: nil
    t.datetime "updated_at", precision: nil
    t.datetime "time_from", precision: nil, null: false
    t.datetime "time_to", precision: nil, null: false
    t.enum "delivery_state", default: "loading", null: false, enum_type: "courier_delivery_state"
    t.datetime "estimated_return_at", precision: nil
    t.integer "shift_id", null: false
    t.datetime "started_at", precision: nil
    t.datetime "finished_at", precision: nil
    t.index ["courier_id"], name: "index_delivery_routes_on_courier_id"
    t.index ["delivery_plan_id"], name: "index_delivery_routes_on_delivery_plan_id"
    t.index ["delivery_state"], name: "index_delivery_routes_on_delivery_state"
    t.index ["shift_id"], name: "index_delivery_routes_on_shift_id"
  end

  create_table "delivery_zones", id: :serial, force: :cascade do |t|
    t.integer "shop_id"
    t.integer "area_id"
    t.string "kind"
    t.integer "price"
    t.integer "time"
    t.string "name"
    t.boolean "deleted", default: false
    t.boolean "include_availability_stat", default: true
    t.integer "yandex_eda_price", default: 0, null: false
    t.integer "min_order_price"
    t.index ["area_id"], name: "index_delivery_zones_on_area_id"
    t.index ["kind"], name: "index_delivery_zones_on_kind"
    t.index ["shop_id"], name: "index_delivery_zones_on_shop_id"
  end

  create_table "desktop_feedbacks", id: :serial, force: :cascade do |t|
    t.citext "email"
    t.string "comment"
    t.integer "points", null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
  end

  create_table "employee_additional_acts", force: :cascade do |t|
    t.bigint "employee_id"
    t.bigint "hour_id"
    t.integer "amount", null: false
    t.boolean "signed", default: false
    t.datetime "signed_at", precision: nil
    t.uuid "manual_payment_public_id", null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.string "pdf_file"
    t.string "signed_with_code"
    t.index ["employee_id"], name: "index_employee_additional_acts_on_employee_id"
    t.index ["hour_id", "manual_payment_public_id"], name: "idx_additional_acts_on_shift_and_manual_payment", unique: true
  end

  create_table "employee_contacts", id: :serial, force: :cascade do |t|
    t.integer "employee_id", null: false
    t.string "telegram_id", default: "", null: false
    t.string "telegram_username", default: "", null: false
    t.index ["employee_id"], name: "index_employee_contacts_on_employee_id"
  end

  create_table "employee_flashes", id: :serial, force: :cascade do |t|
    t.integer "employee_id"
    t.text "text"
    t.string "state"
    t.index ["employee_id"], name: "index_employee_flashes_on_employee_id"
  end

  create_table "employee_notification_devices", force: :cascade do |t|
    t.bigint "employee_id", null: false
    t.string "push_token", null: false
    t.string "device_uid", null: false
    t.enum "platform", enum_type: "notification_devices_platform_enum"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.enum "push_token_provider", null: false, enum_type: "notification_devices_push_token_provider_enum"
    t.string "platform_version"
    t.index ["employee_id", "device_uid"], name: "index_notification_devices_on_employee_id_and_device_uid", unique: true
  end

  create_table "employee_notification_reads", force: :cascade do |t|
    t.bigint "employee_id", null: false
    t.bigint "employee_notification_id", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["employee_id", "employee_notification_id"], name: "index_uniq_notification_reads_on_employee_and_notification", unique: true
  end

  create_table "employee_notifications", force: :cascade do |t|
    t.string "title", null: false
    t.string "body", null: false
    t.string "summary", limit: 170, null: false
    t.string "link"
    t.datetime "pinned_at", precision: nil
    t.datetime "hidden_at", precision: nil
    t.enum "domain", null: false, enum_type: "employee_notifications_domain_enum"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.integer "receiver_ids", default: [], null: false, array: true
    t.index ["receiver_ids"], name: "index_employee_notifications_on_receiver_ids", using: :gin
  end

  create_table "employee_payments", id: :serial, force: :cascade do |t|
    t.integer "employee_id", null: false
    t.datetime "payment_at", precision: nil
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["employee_id"], name: "index_employee_payments_on_employee_id"
  end

  create_table "employee_positions", id: :serial, force: :cascade do |t|
    t.integer "employee_id"
    t.integer "shop_id"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.string "aasm_state"
    t.integer "hour_id"
    t.datetime "start_at", precision: nil
    t.datetime "packing_started_at", precision: nil
    t.index ["aasm_state"], name: "index_employee_positions_on_aasm_state", where: "((aasm_state)::text <> 'finished'::text)"
    t.index ["employee_id"], name: "index_employee_positions_on_employee_id"
    t.index ["hour_id"], name: "index_employee_positions_on_hour_id"
    t.index ["shop_id"], name: "index_employee_positions_on_shop_id"
  end

  create_table "employee_want_bonus", id: :serial, force: :cascade do |t|
    t.integer "employee_id"
    t.integer "order_id"
    t.string "reason", null: false
    t.text "comment"
    t.string "image"
    t.string "aasm_state"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["employee_id"], name: "index_employee_want_bonus_on_employee_id"
    t.index ["order_id"], name: "index_employee_want_bonus_on_order_id"
  end

  create_table "employees", id: :serial, force: :cascade do |t|
    t.string "role", null: false
    t.string "first_name"
    t.string "last_name"
    t.string "patronymic"
    t.string "phone"
    t.citext "login", default: "", null: false
    t.string "encrypted_password", default: "", null: false
    t.integer "sign_in_count", default: 0, null: false
    t.datetime "current_sign_in_at", precision: nil
    t.datetime "last_sign_in_at", precision: nil
    t.inet "current_sign_in_ip"
    t.inet "last_sign_in_ip"
    t.integer "failed_attempts", default: 0, null: false
    t.string "unlock_token"
    t.datetime "locked_at", precision: nil
    t.boolean "planned_break"
    t.datetime "created_at", precision: nil
    t.datetime "updated_at", precision: nil
    t.boolean "planned_lunch"
    t.string "photo"
    t.string "authentication_token", limit: 30
    t.integer "operator_id"
    t.boolean "closed_shops", default: false
    t.string "models_count", default: [], array: true
    t.date "contract_date"
    t.string "contract_number"
    t.string "cloud_tips_url"
    t.integer "vehicle_specs_id"
    t.boolean "self_employed", default: false
    t.string "passport_series"
    t.string "passport_number"
    t.string "passport_date"
    t.string "passport_code"
    t.string "passport_address"
    t.string "inn"
    t.string "bank_account"
    t.string "bank_ks"
    t.string "bank_bik"
    t.string "bank_name"
    t.string "ufms"
    t.datetime "fired_at", precision: nil
    t.boolean "self_employed_confirmed"
    t.uuid "public_id", default: -> { "public.gen_random_uuid()" }
    t.integer "tax_rate", limit: 2
    t.enum "payment_provider", enum_type: "employee_payment_providers"
    t.boolean "shop_transfer_available", default: false, null: false
    t.enum "gender", enum_type: "employee_gender_enum"
    t.jsonb "log_data"
    t.integer "automatical_wallet_balance", default: 0
    t.integer "manual_wallet_balance", default: 0
    t.boolean "employed_by_hour"
    t.index ["authentication_token"], name: "index_employees_on_authentication_token", unique: true
    t.index ["cloud_tips_url"], name: "index_employees_on_cloud_tips_url"
    t.index ["fired_at"], name: "index_employees_on_fired_at"
    t.index ["login"], name: "index_employees_on_login", unique: true
    t.index ["operator_id"], name: "index_employees_on_operator_id"
    t.index ["public_id"], name: "index_employees_on_public_id", unique: true
    t.index ["unlock_token"], name: "index_employees_on_unlock_token", unique: true
    t.check_constraint "tax_rate >= 0 AND tax_rate <= 99", name: "check_tax_rate"
  end

  create_table "entities", id: :serial, force: :cascade do |t|
    t.integer "user_id"
    t.string "name"
    t.string "inn"
    t.string "address"
    t.string "checking_account"
    t.string "bank_name"
    t.string "bik"
    t.string "correspondent_account"
    t.text "reason"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.boolean "as_consignee", default: false
    t.string "aasm_state", default: "unfilled", null: false
    t.string "opf_short"
    t.string "opf_full"
    t.string "management_name"
    t.string "kpp"
    t.string "ogrn"
    t.string "authority_type"
    t.string "authority_number"
    t.date "authority_date"
    t.string "name_full"
  end

  create_table "entity_documents", force: :cascade do |t|
    t.bigint "entity_id"
    t.string "document"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["entity_id"], name: "index_entity_documents_on_entity_id"
  end

  create_table "events", id: :serial, force: :cascade do |t|
    t.integer "order_id"
    t.string "name"
    t.string "item_name"
    t.string "replacement_name"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.decimal "price", precision: 10, scale: 2
    t.integer "product_id"
    t.integer "replacement_id"
    t.index ["order_id"], name: "index_events_on_order_id"
    t.index ["product_id"], name: "index_events_on_product_id"
  end

  create_table "external_altcrafts", force: :cascade do |t|
    t.bigint "user_id", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.boolean "excluded", default: false, null: false
    t.index ["user_id"], name: "index_external_altcrafts_on_user_id", unique: true
  end

  create_table "external_meta", force: :cascade do |t|
    t.jsonb "payload", default: {}
    t.bigint "source_id", null: false
    t.enum "source_type", null: false, enum_type: "external_meta_source_type"
    t.enum "provider", null: false, enum_type: "external_meta_provider"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index "((payload ->> 'model_id'::text))", name: "index_external_meta_on_payload_model_id", unique: true
    t.index "date(created_at)", name: "index_external_meta_on_date_created_at"
    t.index ["source_id", "source_type", "provider"], name: "index_external_meta_on_source_id_and_source_type_and_provider", unique: true
  end

  create_table "external_retailer_cloud_receipts", force: :cascade do |t|
    t.bigint "order_id", null: false
    t.enum "external_retailer", null: false, enum_type: "external_retailer_enum"
    t.jsonb "external_receipt_json"
    t.string "external_receipt_url"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["order_id", "external_retailer"], name: "order_id_and_external_retailer_unique", unique: true
  end

  create_table "external_users", force: :cascade do |t|
    t.enum "user_source", null: false, enum_type: "external_user_source_enum"
    t.string "first_name", null: false
    t.string "last_name"
    t.string "patronymic"
    t.string "phone"
    t.integer "orders_count", default: 0
    t.string "comment", default: "", null: false
    t.string "kind", default: "mobile", null: false
    t.boolean "blocked", default: false, null: false
    t.string "blocked_comment"
    t.datetime "blocked_at", precision: nil
    t.integer "blocked_employee_id"
    t.boolean "as_entity", default: false, null: false
    t.enum "behavior", enum_type: "behavior_enum"
    t.datetime "last_order_at", precision: nil
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "favorite_models", id: :serial, force: :cascade do |t|
    t.integer "model_id", null: false
    t.integer "user_id", null: false
    t.integer "count", default: 0, null: false
    t.boolean "hidden", default: false, null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.boolean "marked", default: false, null: false
    t.boolean "paid", default: false, null: false
    t.enum "user_type", default: "User", null: false, enum_type: "user_type_enum"
    t.index ["model_id"], name: "index_favorite_models_on_model_id"
    t.index ["user_id", "user_type", "model_id"], name: "index_favorite_models_on_user_id_and_user_type_and_model_id", unique: true
  end

  create_table "feedbacks", id: :serial, force: :cascade do |t|
    t.string "name"
    t.string "email"
    t.text "text"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.text "error_types", array: true
    t.integer "user_id"
    t.integer "product_id"
    t.string "aasm_state"
    t.string "from", default: "web", null: false
    t.integer "shop_id"
    t.integer "model_id"
    t.index ["model_id"], name: "index_feedbacks_on_model_id"
    t.index ["shop_id"], name: "index_feedbacks_on_shop_id"
  end

  create_table "field_values", id: :serial, force: :cascade do |t|
    t.integer "field_id", null: false
    t.text "name"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.string "slug"
    t.text "seo_text"
    t.index ["field_id"], name: "index_field_values_on_field_id"
    t.index ["slug"], name: "index_field_values_on_slug"
  end

  create_table "fields", id: :serial, force: :cascade do |t|
    t.integer "category_id", null: false
    t.text "name"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.string "slug"
    t.enum "seo_text_type", default: "none", null: false, enum_type: "fields_seo_text_type_enum"
    t.index ["category_id"], name: "index_fields_on_category_id"
    t.index ["slug"], name: "index_fields_on_slug"
  end

  create_table "franchisees", id: :serial, force: :cascade do |t|
    t.string "name"
    t.string "city"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.string "offer_image"
    t.string "pscb_merchant_id"
    t.string "tinkoff_terminal_id"
    t.string "tinkoff_terminal_pass"
    t.string "stamp_image"
    t.string "faximile_image"
    t.string "cloud_payments_public_id"
    t.string "cloud_payments_secret"
  end

  create_table "geo_ips", id: :serial, force: :cascade do |t|
    t.inet "addr"
    t.string "country_code"
    t.string "country"
    t.string "city"
    t.float "lat"
    t.float "lng"
    t.index ["addr"], name: "index_geo_ips_on_addr", opclass: :inet_ops, using: :gist
  end

  create_table "google_analytics_apps", comment: "For tracking app_instance_id (Firebase) / client_id (gtag) for analytics", force: :cascade do |t|
    t.bigint "user_id", null: false
    t.string "instance_id", null: false
    t.enum "platform", null: false, enum_type: "google_analytics_apps_platform_enum"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["user_id"], name: "index_google_analytics_apps_on_user_id"
  end

  create_table "gooodwin_user_bot_sessions", force: :cascade do |t|
    t.bigint "user_id"
    t.string "chat_id", null: false
    t.string "state", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.integer "command_shown_product_ids", default: [], array: true
    t.integer "feed_shown_product_ids", default: [], array: true
    t.datetime "command_shown_products_at", precision: nil
    t.datetime "feed_shown_products_at", precision: nil
    t.datetime "last_message_at", precision: nil
    t.index ["user_id"], name: "index_gooodwin_user_bot_sessions_on_user_id"
  end

  create_table "honest_label_types", force: :cascade do |t|
    t.string "name", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "honest_labels", force: :cascade do |t|
    t.bigint "model_id", null: false
    t.bigint "honest_label_type_id"
    t.enum "shop_group", null: false, enum_type: "shop_group_enum"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["honest_label_type_id"], name: "index_honest_labels_on_honest_label_type_id"
    t.index ["shop_group", "model_id"], name: "index_unique_by_shop_group_and_model_id", unique: true
  end

  create_table "hours", id: :serial, force: :cascade do |t|
    t.datetime "start_at", precision: nil
    t.datetime "stop_at", precision: nil
    t.integer "employee_id", null: false
    t.text "comment"
    t.boolean "standards"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.integer "exchange", default: 0
    t.integer "encashment", default: 0
    t.integer "phone_device_id"
    t.string "phone", limit: 20, default: "", null: false
    t.integer "shop_ids", default: [], null: false, array: true
    t.string "num_terminal", limit: 20
    t.string "type"
    t.integer "min_rate", default: 0
    t.float "rub_per_km", default: 0.0
    t.integer "distance", default: 0
    t.integer "employee_payment_id"
    t.boolean "accounting_checked", default: false, null: false
    t.integer "terminal_id"
    t.integer "picker_hour_rate"
    t.integer "picker_half_hour_rate"
    t.integer "payment_card_id"
    t.datetime "deleted_at", precision: nil
    t.integer "transport_expenses"
    t.integer "stationery_expenses"
    t.integer "misc_expenses"
    t.text "misc_expenses_comment"
    t.string "selfie"
    t.boolean "hold", default: false, null: false
    t.uuid "public_id", default: -> { "public.gen_random_uuid()" }
    t.integer "minimal_amount_to_pay"
    t.integer "earned_amount_to_pay"
    t.integer "amount_to_pay"
    t.integer "half_shift_min_rate"
    t.integer "courier_rate_for_employment_by_hour"
    t.integer "picker_rate_for_employment_by_hour"
    t.integer "picker_time_bonus"
    t.index "date(start_at), employee_id", name: "index_hours_on_start_at_for_courier_per_day", unique: true, where: "((stop_at IS NULL) AND ((type)::text = 'courier_car'::text) AND (deleted_at IS NULL))"
    t.index "lower((num_terminal)::text)", name: "index_hours_on_lower_terminal_num"
    t.index ["employee_id"], name: "index_hours_on_employee_id"
    t.index ["employee_payment_id"], name: "index_hours_on_employee_payment_id"
    t.index ["payment_card_id"], name: "index_hours_on_payment_card_id"
    t.index ["public_id"], name: "index_hours_on_public_id", unique: true
    t.index ["start_at"], name: "index_hours_on_start_at"
    t.index ["terminal_id", "stop_at"], name: "index_hours_on_terminal_id_and_stop_at"
    t.index ["terminal_id"], name: "index_hours_on_terminal_id", where: "(((type)::text = 'courier_scooter'::text) OR ((type)::text = 'courier_car'::text))"
  end

  create_table "invalid_events", force: :cascade do |t|
    t.jsonb "event", default: {}, null: false
    t.jsonb "error", default: []
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
  end

  create_table "invoice_reports", force: :cascade do |t|
    t.bigint "operator_id", null: false
    t.date "min_date", null: false
    t.date "max_date", null: false
    t.enum "aasm_state", null: false, enum_type: "invoice_report_status_enum"
    t.string "invoice_report_file"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["operator_id"], name: "index_invoice_reports_on_operator_id"
  end

  create_table "item_honest_labels", force: :cascade do |t|
    t.bigint "item_id", null: false
    t.string "picker_labels", default: [], array: true
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["item_id"], name: "index_item_honest_labels_on_item_id"
  end

  create_table "item_original_prices", force: :cascade do |t|
    t.bigint "item_id", null: false
    t.decimal "price", precision: 10, scale: 2, null: false
    t.decimal "price_per_kg", precision: 10, scale: 2, null: false
    t.decimal "price_for_receipt", precision: 10, scale: 2
    t.decimal "price_per_kg_for_receipt", precision: 10, scale: 2
    t.index ["item_id"], name: "index_item_original_prices_on_item_id"
  end

  create_table "item_picker_declines", force: :cascade do |t|
    t.bigint "item_id"
    t.string "reason", null: false
    t.string "comment"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["item_id"], name: "index_item_picker_declines_on_item_id"
  end

  create_table "item_replacement_original_prices", force: :cascade do |t|
    t.bigint "item_replacement_id", null: false
    t.decimal "price", precision: 10, scale: 2, null: false
    t.decimal "price_per_kg", precision: 10, scale: 2, null: false
    t.index ["item_replacement_id"], name: "index_item_replacement_original_prices_on_item_replacement_id"
  end

  create_table "item_replacements", id: :serial, force: :cascade do |t|
    t.integer "product_id"
    t.integer "amount"
    t.integer "item_id"
    t.decimal "price"
    t.decimal "price_per_kg"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.integer "weight"
    t.boolean "sale", default: false
    t.integer "user_amount"
    t.string "model_type"
    t.string "picker_reason"
    t.decimal "original_price", precision: 10, scale: 2
    t.decimal "original_price_per_kg", precision: 10, scale: 2
    t.index ["item_id"], name: "index_item_replacements_on_item_id"
  end

  create_table "item_unconfirmed_replacements", force: :cascade do |t|
    t.bigint "item_id"
    t.bigint "product_id"
    t.string "reason"
    t.integer "amount"
    t.integer "weight"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["item_id"], name: "index_item_unconfirmed_replacements_on_item_id"
  end

  create_table "items", id: :serial, force: :cascade do |t|
    t.integer "order_id", null: false
    t.integer "product_id", null: false
    t.integer "category_id", null: false
    t.integer "root_category_id", null: false
    t.integer "replacement_id"
    t.integer "amount", default: 0
    t.string "aasm_state"
    t.datetime "added_at", precision: nil
    t.datetime "missing_at", precision: nil
    t.datetime "replacement_at", precision: nil
    t.datetime "cancelled_at", precision: nil
    t.integer "picker_amount"
    t.integer "picker_replacement_id"
    t.integer "courier_amount"
    t.string "courier_reason"
    t.string "courier_comment"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.integer "picker_weights", default: [], array: true
    t.integer "weight", default: 0
    t.integer "courier_weights", default: [], array: true
    t.integer "picker_replacement_amount"
    t.decimal "price", precision: 10, scale: 2
    t.decimal "price_per_kg", precision: 10, scale: 2
    t.text "comment"
    t.integer "picker_replacement_weight"
    t.boolean "sale", default: false
    t.integer "user_amount"
    t.string "model_type"
    t.string "platform", limit: 20, default: "web", null: false
    t.decimal "price_when_filled", precision: 10, scale: 2
    t.decimal "price_per_kg_when_filled", precision: 10, scale: 2
    t.string "picker_reason"
    t.string "picker_code"
    t.boolean "added_by_picker", default: false, null: false
    t.integer "delivered_amount"
    t.integer "delivered_weights", default: [], array: true
    t.jsonb "log_data"
    t.decimal "original_price", precision: 10, scale: 2
    t.decimal "original_price_per_kg", precision: 10, scale: 2
    t.decimal "original_price_for_receipt", precision: 10, scale: 2
    t.decimal "original_price_per_kg_for_receipt", precision: 10, scale: 2
    t.index ["order_id"], name: "index_items_on_order_id"
    t.index ["product_id", "order_id"], name: "index_items_on_product_id_and_order_id"
    t.index ["product_id"], name: "index_items_on_product_id"
  end

  create_table "joom_users", id: :serial, force: :cascade do |t|
    t.string "first_name"
    t.string "last_name"
    t.string "patronymic"
    t.string "phone"
    t.integer "orders_count", default: 0
    t.string "comment", default: "", null: false
    t.string "kind", default: "mobile", null: false
    t.boolean "blocked", default: false
    t.string "blocked_comment"
    t.datetime "blocked_at", precision: nil
    t.integer "blocked_employee_id"
    t.boolean "as_entity", default: false, null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.enum "behavior", enum_type: "behavior_enum"
    t.datetime "last_order_at", precision: nil
    t.index ["phone"], name: "index_joom_users_on_phone", unique: true
  end

  create_table "komus_account_transactions", force: :cascade do |t|
    t.bigint "komus_account_id", null: false
    t.bigint "order_id", null: false
    t.decimal "amount", precision: 10, scale: 2, null: false
    t.enum "direction", null: false, enum_type: "transaction_direction_enum"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "komus_employee_id"
    t.index ["komus_account_id"], name: "index_komus_account_transactions_on_komus_account_id"
    t.index ["komus_employee_id"], name: "index_komus_account_transactions_on_komus_employee_id"
    t.index ["order_id"], name: "index_komus_account_transactions_on_order_id"
  end

  create_table "komus_accounts", force: :cascade do |t|
    t.bigint "komus_user_id", null: false
    t.decimal "balance", precision: 10, scale: 2, null: false
    t.enum "type", null: false, enum_type: "komus_accounts_type_enum"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["komus_user_id"], name: "index_komus_accounts_on_komus_user_id"
  end

  create_table "komus_employees", force: :cascade do |t|
    t.string "full_name", null: false
    t.string "role", null: false
    t.datetime "fired_at", precision: nil
    t.citext "login", null: false
    t.string "encrypted_password"
    t.integer "sign_in_count", default: 0, null: false
    t.datetime "current_sign_in_at", precision: nil
    t.datetime "last_sign_in_at", precision: nil
    t.inet "current_sign_in_ip"
    t.inet "last_sign_in_ip"
    t.integer "failed_attempts", default: 0, null: false
    t.datetime "locked_at", precision: nil
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["login"], name: "index_komus_employees_on_login", unique: true
  end

  create_table "komus_users", force: :cascade do |t|
    t.string "name"
    t.string "phone"
    t.string "unconfirmed_phone"
    t.string "phone_confirmation_code"
    t.datetime "phone_confirmation_code_sent_at", precision: nil
    t.citext "email"
    t.citext "unconfirmed_email"
    t.string "email_confirmation_code"
    t.datetime "email_confirmation_code_sent_at", precision: nil
    t.string "authentication_token", null: false
    t.inet "current_sign_in_ip"
    t.inet "last_sign_in_ip"
    t.datetime "current_sign_in_at", precision: nil
    t.datetime "last_sign_in_at", precision: nil
    t.enum "behavior", null: false, enum_type: "behavior_enum"
    t.integer "orders_count", default: 0, null: false
    t.datetime "last_order_at", precision: nil
    t.string "kind", null: false
    t.string "comment"
    t.boolean "as_entity", default: false, null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.datetime "phone_confirmed_at", precision: nil
    t.datetime "registered_at", precision: nil
    t.boolean "blocked"
    t.datetime "blocked_at", precision: nil
    t.string "blocked_comment"
    t.string "blocked_by_type"
    t.bigint "blocked_by_id"
    t.string "partner_code"
    t.string "entity_name"
    t.string "entity_name_full"
    t.string "address"
    t.string "inn"
    t.string "kpp"
    t.string "ogrn"
    t.boolean "confirmed", default: false, null: false
    t.boolean "shipment_on_credit", default: false, null: false
    t.string "avatar"
    t.string "checking_account"
    t.string "bank_name"
    t.string "bik"
    t.string "correspondent_account"
    t.string "payment_type", default: "online"
    t.index ["blocked_by_type", "blocked_by_id"], name: "index_komus_users_on_blocked_by"
    t.index ["email_confirmation_code"], name: "index_komus_users_on_email_confirmation_code", unique: true
    t.index ["inn"], name: "index_komus_users_on_inn"
    t.index ["partner_code"], name: "index_komus_users_on_partner_code"
    t.index ["phone"], name: "index_komus_users_on_phone", unique: true
    t.index ["unconfirmed_phone"], name: "index_komus_users_on_unconfirmed_phone"
  end

  create_table "landing_banners", id: :serial, force: :cascade do |t|
    t.integer "landing_id"
    t.string "image", null: false
    t.integer "serial_number", null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["landing_id"], name: "index_landing_banners_on_landing_id"
  end

  create_table "landing_link_attributes", id: :serial, force: :cascade do |t|
    t.integer "landing_id"
    t.string "category", null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.string "element"
    t.index ["landing_id"], name: "index_landing_link_attributes_on_landing_id"
  end

  create_table "landings", id: :serial, force: :cascade do |t|
    t.string "name", null: false
    t.string "url", null: false
    t.string "landing_title", null: false
    t.string "meta_title", default: "iGooods", null: false
    t.string "meta_description", default: "iGooods", null: false
    t.string "meta_keywords", default: "iGooods", null: false
    t.string "banner_title", null: false
    t.text "banner_text", null: false
    t.string "promotional_products_title", null: false
    t.text "promotional_products_text", null: false
    t.string "promotional_products_strategy", null: false
    t.string "promotional_products_ids"
    t.integer "promotional_products_category_id"
    t.string "promotional_products_shop_group"
    t.boolean "redirect_to_sa_for_authorized", default: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.text "seo_text"
    t.integer "city_id", null: false
    t.string "shop_group"
    t.datetime "deleted_at", precision: nil
    t.string "how_it_works_subtitle", default: "Как работает igooods", null: false
    t.string "redirect_to"
    t.index ["promotional_products_category_id"], name: "index_landings_on_promotional_products_category_id"
    t.index ["url", "city_id"], name: "index_landings_on_url_and_city_id", unique: true
  end

  create_table "lenta_prices", force: :cascade do |t|
    t.date "perform_date", null: false
    t.boolean "performed", default: false, null: false
    t.datetime "performed_at", precision: nil
    t.integer "shop_id", null: false
    t.string "action_type", null: false
    t.decimal "price", precision: 10, scale: 2
    t.decimal "promo_price", precision: 10, scale: 2
    t.date "from"
    t.date "to"
    t.string "name"
    t.datetime "created_at", precision: nil
    t.datetime "updated_at", precision: nil
    t.bigint "price_file_id"
    t.string "sap_code"
    t.index ["price_file_id"], name: "index_lenta_prices_on_price_file_id"
    t.index ["shop_id", "perform_date"], name: "index_lenta_prices_on_shop_id_and_perform_date"
  end

  create_table "life_pay_notifications", id: :serial, force: :cascade do |t|
    t.integer "order_id", null: false
    t.jsonb "delivery"
    t.jsonb "goods"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.jsonb "combined"
    t.jsonb "combined_receipt", default: {}, null: false
    t.jsonb "goods_receipt", default: {}, null: false
    t.jsonb "delivery_receipt", default: {}, null: false
    t.jsonb "advance"
    t.jsonb "advance_receipt", default: {}, null: false
    t.index ["order_id"], name: "index_life_pay_notifications_on_order_id"
  end

  create_table "lunches", id: :serial, force: :cascade do |t|
    t.integer "employee_id"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.boolean "active", default: true
    t.index ["employee_id"], name: "index_lunches_on_employee_id"
  end

  create_table "manual_receipts", force: :cascade do |t|
    t.bigint "order_id", null: false
    t.decimal "total_sum", precision: 10, scale: 2, null: false
    t.string "photo", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["order_id"], name: "index_manual_receipts_on_order_id"
  end

  create_table "members_delivery_zones", id: :serial, force: :cascade do |t|
    t.integer "member_id", null: false
    t.integer "delivery_zone_id", null: false
    t.index ["member_id", "delivery_zone_id"], name: "index_members_delivery_zones_on_member_id_and_delivery_zone_id", unique: true
  end

  create_table "members_shops", id: :serial, force: :cascade do |t|
    t.integer "member_id", null: false
    t.integer "shop_id", null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["member_id", "shop_id"], name: "index_members_shops_on_member_id_and_shop_id"
  end

  create_table "mobile_builds", id: :serial, force: :cascade do |t|
    t.enum "platform_type", null: false, enum_type: "mobile_builds_platform_type_enum"
    t.string "min_support_version", null: false
    t.string "blacklist", default: [], null: false, array: true
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.enum "domain", null: false, enum_type: "mobile_builds_domain_enum"
  end

  create_table "model_limits", force: :cascade do |t|
    t.string "name", null: false
    t.enum "shop_group", null: false, enum_type: "shop_group_enum"
    t.integer "shop_ids", default: [], null: false, array: true
    t.integer "model_ids", default: [], null: false, array: true
    t.integer "limit", null: false
    t.enum "unit", null: false, enum_type: "model_limit_unit"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["model_ids"], name: "index_model_limits_on_model_ids", using: :gin
    t.index ["shop_ids"], name: "index_model_limits_on_shop_ids", using: :gin
  end

  create_table "model_metadata", force: :cascade do |t|
    t.integer "department"
    t.bigint "model_id"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["model_id"], name: "index_model_metadata_on_model_id"
  end

  create_table "models", id: :serial, force: :cascade do |t|
    t.integer "category_id", null: false
    t.string "type", default: "piece", null: false
    t.string "name"
    t.integer "weight"
    t.integer "volume"
    t.integer "calories"
    t.float "proteins"
    t.float "fats"
    t.float "carbohydrates"
    t.string "composition"
    t.string "manufacturer"
    t.string "info"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.integer "expire_at"
    t.boolean "group_pack"
    t.text "code", default: [], null: false, array: true
    t.integer "group_quantity"
    t.boolean "hidden", default: false, null: false
    t.boolean "local", default: false, null: false
    t.enum "shop_group", enum_type: "shop_group_enum"
    t.integer "brand_id"
    t.string "tag_context"
    t.integer "weight_brutto"
    t.boolean "our_product", default: false, null: false
    t.text "indications_for_use"
    t.text "active_substance"
    t.text "form_of_issue"
    t.text "contraindications"
    t.text "instruction"
    t.text "expiration_date"
    t.index ["brand_id"], name: "index_models_on_brand_id"
    t.index ["category_id"], name: "index_models_on_category_id"
    t.index ["code"], name: "index_models_on_code", using: :gin
  end

  create_table "models_field_values", id: :serial, force: :cascade do |t|
    t.integer "model_id"
    t.integer "field_id", null: false
    t.integer "field_value_id", null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["model_id"], name: "index_models_field_values_on_model_id"
  end

  create_table "news_banners", force: :cascade do |t|
    t.integer "position", default: 0, null: false
    t.string "title", null: false
    t.enum "kind", default: "text", null: false, enum_type: "news_banner_kind"
    t.string "content", null: false
    t.boolean "hidden", default: false, null: false
    t.enum "platform", default: "any", null: false, enum_type: "user_platform_selection_enum"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "notification_devices", id: :serial, force: :cascade do |t|
    t.integer "user_id", null: false
    t.string "push_token"
    t.string "device_uid"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.enum "platform", enum_type: "notification_devices_platform_enum"
    t.string "version"
    t.enum "push_token_provider", default: "onesignal", null: false, enum_type: "notification_devices_push_token_provider_enum"
    t.index ["push_token", "push_token_provider"], name: "push_token_and_provider_uniq", unique: true
    t.index ["user_id"], name: "index_notification_devices_on_user_id"
  end

  create_table "operators", id: :serial, force: :cascade do |t|
    t.integer "franchisee_id"
    t.boolean "franchisor", default: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.string "inn"
    t.string "phone"
    t.boolean "use_igooods_cachboxes", default: false, null: false
    t.string "legal_address"
    t.string "kpp"
    t.string "ogrn"
    t.string "bank_name"
    t.string "bik"
    t.string "correspondent_account"
    t.string "current_account"
    t.string "rocketwork_token"
    t.boolean "active", default: true, null: false
    t.enum "payment_provider", null: false, enum_type: "operator_payment_provider"
    t.uuid "public_id", default: -> { "public.gen_random_uuid()" }, null: false
    t.boolean "can_edit_self_employed", default: false
    t.string "contract_number"
    t.date "contract_date"
    t.string "contract_number_dkk"
    t.date "contract_date_dkk"
    t.index ["franchisee_id"], name: "index_operators_on_franchisee_id", unique: true
    t.index ["public_id"], name: "index_operators_on_public_id", unique: true
  end

  create_table "order_courier_payments", id: :serial, force: :cascade do |t|
    t.integer "order_id"
    t.integer "rate", default: 0, null: false
    t.integer "boxes_bonus", default: 0, null: false
    t.integer "harm", default: 0, null: false
    t.text "comment"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.integer "hour_id"
    t.decimal "weight_bonus", precision: 10, scale: 2, default: "0.0", null: false
    t.index ["hour_id"], name: "index_order_courier_payments_on_hour_id"
    t.index ["order_id"], name: "index_order_courier_payments_on_order_id"
  end

  create_table "order_picker_declines", id: :serial, force: :cascade do |t|
    t.integer "order_id"
    t.string "reason", null: false
    t.text "comment"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.integer "product_id"
    t.index ["order_id"], name: "index_order_picker_declines_on_order_id"
    t.index ["product_id"], name: "index_order_picker_declines_on_product_id"
  end

  create_table "order_picker_payments", id: :serial, force: :cascade do |t|
    t.integer "order_id"
    t.integer "time_bonus", default: 0
    t.integer "items_bonus", default: 0
    t.integer "harm", default: 0
    t.text "comment"
    t.integer "packing_time", default: 0
    t.integer "adding_time", default: 0
    t.integer "hour_id"
    t.integer "employee_position_id"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["employee_position_id"], name: "index_order_picker_payments_on_employee_position_id"
    t.index ["hour_id"], name: "index_order_picker_payments_on_hour_id"
    t.index ["order_id"], name: "index_order_picker_payments_on_order_id"
  end

  create_table "order_shop_brand_labels", force: :cascade do |t|
    t.bigint "order_id", null: false
    t.enum "brand_label", null: false, enum_type: "shop_brand_label"
    t.index ["order_id"], name: "index_order_shop_brand_labels_on_order_id"
  end

  create_table "order_user_permissions", force: :cascade do |t|
    t.bigint "order_id", null: false
    t.bigint "user_id", null: false
    t.enum "access_level", null: false, enum_type: "order_user_permission_access_level"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["order_id"], name: "index_order_user_permissions_on_order_id"
    t.index ["user_id"], name: "index_order_user_permissions_on_user_id"
  end

  create_table "orders", id: :serial, force: :cascade do |t|
    t.integer "shop_id", null: false
    t.integer "user_id"
    t.integer "place_id"
    t.datetime "deliver_at", precision: nil
    t.string "phone"
    t.string "payment_type"
    t.string "change_from"
    t.enum "behavior", enum_type: "behavior_enum"
    t.string "aasm_state"
    t.integer "picker_id"
    t.integer "picker_cell"
    t.integer "courier_id"
    t.boolean "courier_returning", default: false, null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.string "picker_invoice_number"
    t.datetime "filled_at", precision: nil
    t.integer "delivery_price"
    t.string "user_email"
    t.integer "inviter_id"
    t.integer "discount", default: 0
    t.text "comment"
    t.string "picker_invoice_number_adult"
    t.integer "picker_real_adult_price_rub"
    t.integer "picker_real_adult_price_kop"
    t.boolean "early", default: false, null: false
    t.integer "picker_boxes"
    t.string "type", default: "delivery", null: false
    t.string "picker_boxes_type", default: [], array: true
    t.integer "packet_price"
    t.string "kind"
    t.boolean "first", default: false
    t.datetime "block_slot", precision: nil
    t.integer "trailer_id"
    t.datetime "start_delivering_at", precision: nil
    t.integer "delivery_zone_id"
    t.integer "priority", default: 0
    t.datetime "ready_at", precision: nil
    t.integer "operator_id"
    t.integer "day_schedule_id"
    t.integer "total_sum_user"
    t.integer "total_sum_picker"
    t.integer "total_sum_courier"
    t.integer "adult_extra_charge_user"
    t.integer "adult_extra_charge_picker"
    t.integer "adult_extra_charge_courier"
    t.datetime "first_item_at", precision: nil
    t.integer "assembly_price"
    t.enum "payment_provider", null: false, enum_type: "order_payment_provider"
    t.integer "payment_card_id"
    t.integer "picker_calc_real_price"
    t.integer "picker_real_price_rub"
    t.integer "picker_real_price_kop"
    t.boolean "evaluated", default: false, null: false
    t.enum "user_type", enum_type: "user_type_enum"
    t.integer "delivery_route_id"
    t.datetime "time_from", precision: nil
    t.datetime "time_to", precision: nil
    t.datetime "planning_started_at", precision: nil
    t.integer "courier_trip_id"
    t.integer "initial_weight_bonus"
    t.datetime "start_packing_at", precision: nil
    t.integer "picker_trip_id"
    t.string "cloud_payment_token"
    t.boolean "confirmed", default: false
    t.integer "route_sheet_id"
    t.boolean "fewer_plastic_bags", default: false, null: false
    t.boolean "payment_card_limit", default: false, null: false
    t.datetime "updated_by_admin_at", precision: nil
    t.boolean "available_to_edit_by_picker", default: false, null: false
    t.boolean "regular_items_packed", default: false, null: false
    t.integer "total_sum_courier_original_price"
    t.datetime "payment_card_limit_at", precision: nil
    t.integer "total_sum_courier_our_products_prime_price_costs"
    t.string "invoice_pdf_file"
    t.integer "total_sum_courier_pharmacy"
    t.decimal "service_fee", precision: 10, scale: 2, default: "0.0", null: false
    t.boolean "post_pay", default: false
    t.string "multi_user_token"
    t.string "soft_receipt_guids", array: true
    t.bigint "partner_configuration_id"
    t.bigint "cross_sell_main_order_id"
    t.boolean "has_cross_sell", default: false, null: false
    t.index "date(created_at)", name: "index_orders_on_date_created_at"
    t.index "date(deliver_at)", name: "index_orders_on_date_deliver_at", where: "(deliver_at IS NOT NULL)"
    t.index ["aasm_state"], name: "index_orders_on_aasm_state"
    t.index ["block_slot"], name: "index_orders_on_block_slot", where: "(block_slot IS NOT NULL)"
    t.index ["courier_id"], name: "index_orders_on_courier_id"
    t.index ["courier_trip_id"], name: "index_orders_on_courier_trip_id"
    t.index ["cross_sell_main_order_id"], name: "index_orders_on_cross_sell_main_order_id"
    t.index ["day_schedule_id"], name: "index_orders_on_day_schedule_id", where: "(day_schedule_id IS NOT NULL)"
    t.index ["deliver_at", "aasm_state", "shop_id"], name: "index_orders_on_deliver_at_and_aasm_state_and_shop_id"
    t.index ["deliver_at", "id"], name: "index_orders_on_deliver_at_and_id", order: { deliver_at: :desc }, where: "((aasm_state)::text = ANY (ARRAY[('filled'::character varying)::text, ('packing'::character varying)::text, ('packed'::character varying)::text, ('delivering'::character varying)::text, ('declined'::character varying)::text, ('returned'::character varying)::text, ('paid'::character varying)::text]))"
    t.index ["deliver_at", "shop_id"], name: "index_orders_on_deliver_at_and_shop_id"
    t.index ["delivery_route_id"], name: "index_orders_on_delivery_route_id"
    t.index ["id", "aasm_state", "shop_id"], name: "index_orders_on_id_and_aasm_state_and_shop_id"
    t.index ["operator_id", "aasm_state"], name: "index_orders_on_operator_id_and_aasm_state"
    t.index ["operator_id", "user_type", "user_id"], name: "index_orders_on_operator_id_and_user_type_and_user_id"
    t.index ["partner_configuration_id"], name: "index_orders_on_partner_configuration_id"
    t.index ["payment_provider", "updated_at"], name: "index_orders_on_payment_provider_and_updated_at"
    t.index ["phone"], name: "index_orders_on_phone"
    t.index ["picker_id"], name: "index_orders_on_picker_id"
    t.index ["place_id"], name: "index_orders_on_place_id"
    t.index ["route_sheet_id"], name: "index_orders_on_route_sheet_id"
    t.index ["shop_id", "user_type", "user_id"], name: "index_orders_on_shop_id_and_user_type_and_user_id"
    t.index ["updated_at"], name: "index_orders_on_updated_at"
    t.index ["user_email"], name: "index_orders_on_user_email"
    t.index ["user_type", "user_id"], name: "index_orders_on_user_type_and_user_id"
  end

  create_table "pages", id: :serial, force: :cascade do |t|
    t.string "title"
    t.string "permalink"
    t.text "content"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
  end

  create_table "partner_configurations", force: :cascade do |t|
    t.enum "partner_identifier", null: false, enum_type: "partner_configurations_partner_identifier"
    t.jsonb "configuration", default: {}, null: false
    t.datetime "start_at", precision: nil
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["start_at"], name: "index_partner_configurations_on_start_at", unique: true, order: :desc
  end

  create_table "payment_cards", id: :serial, force: :cascade do |t|
    t.integer "shop_id", null: false
    t.string "pan", null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.boolean "active", default: true, null: false
    t.bigint "tinkoff_ucid"
    t.datetime "deleted_at", precision: nil
    t.index ["shop_id"], name: "index_payment_cards_on_shop_id"
  end

  create_table "payment_cards_journal", id: :serial, force: :cascade do |t|
    t.integer "payment_card_id", null: false
    t.integer "hour_id", null: false
    t.datetime "start_use_at", precision: nil, null: false
    t.datetime "stop_use_at", precision: nil
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["hour_id"], name: "index_payment_cards_journal_on_hour_id"
    t.index ["payment_card_id"], name: "index_payment_cards_journal_on_payment_card_id"
  end

  create_table "payment_events", id: :serial, force: :cascade do |t|
    t.enum "kind", null: false, enum_type: "payment_events_kind"
    t.integer "user_id"
    t.integer "order_id"
    t.integer "bank_card_id"
    t.integer "duration_ms"
    t.string "address"
    t.string "request"
    t.string "response"
    t.string "exception"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.enum "user_type", default: "User", null: false, enum_type: "user_type_enum"
    t.index ["order_id"], name: "index_payment_events_on_order_id", where: "(order_id IS NOT NULL)"
    t.index ["user_type", "user_id"], name: "index_payment_events_on_user_type_and_user_id"
  end

  create_table "payment_states", id: :serial, force: :cascade do |t|
    t.integer "order_id", null: false
    t.integer "bank_card_id"
    t.string "aasm_state", null: false
    t.jsonb "custom_data", default: {}, null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["bank_card_id"], name: "index_payment_states_on_bank_card_id"
    t.index ["order_id"], name: "index_payment_states_on_order_id"
  end

  create_table "pharmacy_payment_states", force: :cascade do |t|
    t.bigint "order_id", null: false
    t.bigint "bank_card_id"
    t.string "aasm_state", null: false
    t.jsonb "custom_data", default: {}, null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["bank_card_id"], name: "index_pharmacy_payment_states_on_bank_card_id"
    t.index ["order_id"], name: "index_pharmacy_payment_states_on_order_id"
  end

  create_table "phone_devices", id: :serial, force: :cascade do |t|
    t.boolean "active", default: true, null: false
    t.integer "shop_id", null: false
    t.string "code", null: false
    t.string "number", limit: 20, null: false
    t.string "comment", default: "", null: false
    t.enum "kind", default: "common", null: false, enum_type: "phone_devices_kind_enum"
    t.index ["code"], name: "index_phone_devices_on_code", unique: true
    t.index ["number", "shop_id"], name: "index_phone_devices_on_number_and_shop_id", unique: true
  end

  create_table "pictures", id: :serial, force: :cascade do |t|
    t.integer "model_id"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.boolean "main"
    t.string "picture"
    t.string "source"
    t.integer "priority", default: 0, null: false
    t.index ["model_id"], name: "index_pictures_on_model_id"
  end

  create_table "places", id: :serial, force: :cascade do |t|
    t.integer "user_id", null: false
    t.string "city"
    t.string "street"
    t.string "building"
    t.string "apartment"
    t.string "name"
    t.string "wing"
    t.string "unit"
    t.string "porch"
    t.string "stage"
    t.string "note"
    t.float "latitude"
    t.float "longitude"
    t.boolean "main"
    t.integer "near_shop_ids", default: [], array: true
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.string "entrance"
    t.boolean "deleted", default: false
    t.text "payload"
    t.string "digest"
    t.enum "user_type", enum_type: "user_type_enum"
    t.integer "regional_center_id"
    t.boolean "elevator"
    t.string "geo_grinder_address_id"
    t.index "to_tsvector('russian'::regconfig, (street)::text)", name: "index_places_on_fulltext_street_search", using: :gin
    t.index ["apartment"], name: "index_places_on_pgtrgm_apartment", opclass: :gin_trgm_ops, using: :gin
    t.index ["building"], name: "index_places_on_pgtrgm_building", opclass: :gin_trgm_ops, using: :gin
    t.index ["digest", "apartment"], name: "index_places_on_digest_and_apartment", where: "(digest IS NOT NULL)", comment: "Index for checking orders on same place exists \"Order#orders_on_same_place_exist?\""
    t.index ["geo_grinder_address_id"], name: "index_places_on_geo_grinder_address_id"
    t.index ["user_type", "user_id", "apartment"], name: "index_places_on_user_type_and_user_id_and_apartment"
    t.index ["user_type", "user_id", "digest"], name: "index_places_on_user_type_and_user_id_and_digest"
  end

  create_table "points_flow", id: :serial, force: :cascade do |t|
    t.integer "account_id", null: false
    t.integer "user_id", null: false
    t.integer "operator_id", null: false
    t.integer "employee_id"
    t.integer "order_id"
    t.string "payment_order"
    t.date "payment_transfer_date"
    t.integer "invitee_id"
    t.integer "amount"
    t.integer "users_balance"
    t.string "type"
    t.string "direction"
    t.integer "order_operator_id"
    t.text "comment"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.bigint "claim_id"
    t.date "expiration_date"
    t.bigint "coupon_id"
    t.index ["account_id"], name: "index_points_flow_on_account_id"
    t.index ["claim_id"], name: "index_points_flow_on_claim_id"
    t.index ["coupon_id"], name: "index_points_flow_on_coupon_id", where: "(coupon_id IS NOT NULL)"
    t.index ["order_id"], name: "index_points_flow_on_order_id"
    t.index ["user_id"], name: "index_points_flow_on_user_id"
  end

  create_table "price_files", id: :serial, force: :cascade do |t|
    t.date "perform_date", null: false
    t.enum "aasm_state", null: false, enum_type: "price_file_state_enum"
    t.string "shop_group", null: false
    t.string "file_name", null: false
    t.datetime "started_at", precision: nil
    t.datetime "completed_at", precision: nil
    t.datetime "fatal_at", precision: nil
    t.datetime "created_at", precision: nil
    t.datetime "updated_at", precision: nil
    t.string "sha512_hash"
    t.string "kind"
    t.index ["file_name"], name: "index_price_files_on_file_name"
    t.index ["perform_date"], name: "index_price_files_on_perform_date"
    t.index ["sha512_hash"], name: "index_price_files_on_sha512_hash"
  end

  create_table "price_files_shops", id: false, force: :cascade do |t|
    t.integer "shop_id"
    t.integer "price_file_id"
    t.index ["price_file_id"], name: "index_price_files_shops_on_price_file_id"
    t.index ["shop_id"], name: "index_price_files_shops_on_shop_id"
  end

  create_table "product_expireds", id: :serial, force: :cascade do |t|
    t.string "code", null: false
    t.datetime "expired_at", precision: nil
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.integer "employee_id"
    t.integer "shop_id"
    t.string "image"
    t.index ["employee_id"], name: "index_product_expireds_on_employee_id"
    t.index ["shop_id"], name: "index_product_expireds_on_shop_id"
  end

  create_table "product_line_campaign_keyword_tokens", force: :cascade do |t|
    t.bigint "product_line_campaign_keyword_id", null: false
    t.text "tokens", default: [], null: false, array: true
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["product_line_campaign_keyword_id"], name: "i_product_line_campaign_keyword_token_id_on_campaign_tokens"
    t.index ["tokens"], name: "index_product_line_campaign_keyword_tokens_on_tokens", using: :gin
  end

  create_table "product_line_campaign_keywords", force: :cascade do |t|
    t.bigint "product_line_campaign_id", null: false
    t.string "phrase"
    t.integer "words_count"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["product_line_campaign_id"], name: "i_product_line_campaign_id_on_campaign_keywords"
  end

  create_table "product_line_campaigns", id: :serial, force: :cascade do |t|
    t.string "name", null: false
    t.string "comment"
    t.datetime "created_at", precision: nil
    t.datetime "updated_at", precision: nil
    t.string "client"
    t.date "start_at", default: -> { "now()" }, null: false
    t.date "expire_at"
    t.boolean "hidden", default: false, null: false
    t.string "kind", default: "boost_in_categories"
    t.text "keywords"
    t.enum "label", enum_type: "label_type_enum"
    t.integer "model_ids", default: [], null: false, array: true
    t.integer "reserved_model_ids", default: [], null: false, array: true
    t.decimal "cost_per_action", precision: 10, scale: 2
    t.boolean "without_sale", default: false, null: false
  end

  create_table "product_line_campaigns_sets", id: false, force: :cascade do |t|
    t.bigint "product_line_campaign_id", null: false
    t.bigint "product_set_id", null: false
    t.index ["product_line_campaign_id", "product_set_id"], name: "index_product_line_campaigns_sets"
  end

  create_table "product_line_campaigns_shops", id: false, force: :cascade do |t|
    t.integer "shop_id"
    t.integer "product_line_campaign_id"
    t.index ["product_line_campaign_id", "shop_id"], name: "product_line_campaigns_shops_uidx", unique: true
  end

  create_table "product_losts", id: :serial, force: :cascade do |t|
    t.integer "user_id"
    t.integer "shop_id"
    t.string "email"
    t.string "name"
    t.string "code"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.string "aasm_state"
    t.string "first_name"
    t.string "last_name"
    t.text "comment"
    t.string "kind", default: "web", null: false
    t.index ["shop_id"], name: "index_product_losts_on_shop_id"
    t.index ["user_id"], name: "index_product_losts_on_user_id"
  end

  create_table "product_price_costs", force: :cascade do |t|
    t.bigint "product_id"
    t.decimal "price_cost", precision: 10, scale: 2, null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["created_at"], name: "index_product_price_costs_on_created_at"
    t.index ["product_id"], name: "index_product_price_costs_on_product_id"
  end

  create_table "product_prices", id: :serial, force: :cascade do |t|
    t.integer "product_id", null: false
    t.decimal "price", precision: 10, scale: 2
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.boolean "sale"
    t.bigint "source_id"
    t.enum "source_type", enum_type: "product_prices_source_type"
    t.decimal "original_price", precision: 10, scale: 2
    t.index ["product_id", "price"], name: "index_product_prices_on_product_id_and_price"
    t.index ["source_type", "source_id"], name: "index_product_prices_on_source_type_and_source_id"
  end

  create_table "product_set_shop_groups", id: :serial, force: :cascade do |t|
    t.integer "product_set_id"
    t.string "group", null: false
  end

  create_table "product_set_shops", id: :serial, force: :cascade do |t|
    t.integer "shop_id", null: false
    t.integer "product_set_id", null: false
    t.datetime "created_at", precision: nil
    t.datetime "updated_at", precision: nil
    t.index ["product_set_id"], name: "index_product_set_shops_on_product_set_id"
    t.index ["shop_id"], name: "index_product_set_shops_on_shop_id"
  end

  create_table "product_sets", id: :serial, force: :cascade do |t|
    t.string "name", null: false
    t.string "kind", default: "shop_scope", null: false
    t.integer "position", default: 0, null: false
    t.integer "model_ids", default: [], array: true
    t.boolean "hidden", default: false, null: false
    t.integer "category_ids", default: [], array: true
    t.string "brands", default: [], array: true
    t.datetime "created_at", precision: nil
    t.datetime "updated_at", precision: nil
    t.text "main_banner_description"
    t.boolean "top_position", default: false
    t.string "main_banner"
    t.string "set_banner"
    t.string "set_description"
    t.boolean "all_shops", default: false
    t.string "text_color"
    t.string "head_color"
    t.string "mobile_banner"
    t.boolean "category_filter_enabled", default: false, null: false
    t.string "client"
    t.date "start_at", default: -> { "now()" }, null: false
    t.date "expire_at"
    t.string "codes", default: [], array: true
    t.string "product_picture"
    t.string "background_color"
    t.string "comment"
    t.integer "reserved_model_ids", default: [], null: false, array: true
    t.decimal "cost_per_action", precision: 10, scale: 2
    t.string "mobile_icon"
    t.boolean "show_in_sidebar", default: false, null: false
    t.boolean "show_in_main_page", default: false, null: false
    t.string "mobile_recommended_picture"
    t.enum "platform", default: "any", null: false, enum_type: "product_set_platform_enum"
    t.string "meta_title"
    t.string "meta_description"
  end

  create_table "product_suggestions", force: :cascade do |t|
    t.string "suggestion", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "products", id: :serial, force: :cascade do |t|
    t.integer "shop_id", null: false
    t.integer "model_id", null: false
    t.integer "category_id", null: false
    t.decimal "price", precision: 10, scale: 2
    t.decimal "price_per_kg", precision: 10, scale: 2
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.integer "vat"
    t.boolean "available", default: true, null: false
    t.boolean "sale", default: false
    t.boolean "hidden", default: false, null: false
    t.text "comment"
    t.integer "missing_count", default: 0
    t.integer "orders_count", default: 0
    t.datetime "hidden_from", precision: nil
    t.datetime "hidden_to", precision: nil
    t.boolean "attached", default: false, null: false
    t.datetime "sale_at", precision: nil
    t.integer "scales_button"
    t.datetime "last_parsed_at", precision: nil
    t.integer "root_category_id"
    t.string "raw_name"
    t.datetime "sale_from", precision: nil
    t.float "stock"
    t.decimal "original_price", precision: 10, scale: 2
    t.decimal "original_price_per_kg", precision: 10, scale: 2
    t.decimal "old_price", precision: 10, scale: 2
    t.decimal "old_original_price", precision: 10, scale: 2
    t.boolean "attached_stock", default: false, null: false
    t.index ["category_id", "shop_id", "available", "hidden"], name: "index_products_on_category_id_and_shop_id", where: "((available = true) AND (hidden = false))"
    t.index ["category_id"], name: "index_products_on_category_id"
    t.index ["last_parsed_at"], name: "index_products_on_last_parsed_at"
    t.index ["model_id"], name: "index_products_on_model_id"
    t.index ["shop_id", "category_id", "available", "sale", "hidden"], name: "index_products_for_product_set_sales", where: "((available = true) AND (sale = true) AND (hidden = false))", comment: "Index for get products from ProductSet type \"sale_products\""
    t.index ["shop_id", "model_id"], name: "index_products_on_shop_id_and_model_id", unique: true
    t.index ["updated_at", "shop_id"], name: "index_products_on_updated_at_and_shop_id"
  end

  create_table "providers", id: :serial, force: :cascade do |t|
    t.integer "user_id", null: false
    t.string "uid"
    t.string "name"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
  end

  create_table "rating_coefficients", force: :cascade do |t|
    t.bigint "shop_id", null: false
    t.jsonb "values", default: "[]", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["shop_id"], name: "index_rating_coefficients_on_shop_id", unique: true
  end

  create_table "receipt_items", force: :cascade do |t|
    t.bigint "receipt_id", null: false
    t.bigint "product_id"
    t.bigint "item_id"
    t.string "name", null: false
    t.integer "price_sum_kop", null: false
    t.integer "price_kop", null: false
    t.decimal "quantity", precision: 10, scale: 3
    t.integer "nds"
    t.integer "nds_sum"
    t.integer "payment_type"
    t.integer "product_type"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["item_id"], name: "index_receipt_items_on_item_id", where: "(item_id IS NOT NULL)"
    t.index ["name"], name: "index_receipt_items_on_name"
    t.index ["product_id"], name: "index_receipt_items_on_product_id", where: "(product_id IS NOT NULL)"
    t.index ["receipt_id"], name: "index_receipt_items_on_receipt_id"
  end

  create_table "receipts", id: :serial, force: :cascade do |t|
    t.integer "order_id", null: false
    t.datetime "payment_at", precision: nil, null: false
    t.decimal "total", precision: 10, scale: 2, null: false
    t.string "fn", null: false
    t.string "serial_number", null: false
    t.string "fp", null: false
    t.string "n", null: false
    t.datetime "created_at", precision: nil
    t.datetime "updated_at", precision: nil
    t.jsonb "fns_data", default: {}
    t.string "photo"
    t.index ["fn", "serial_number"], name: "FN_document_uniquiness", unique: true
    t.index ["order_id"], name: "index_receipts_on_order_id"
  end

  create_table "referral_filters", id: :serial, force: :cascade do |t|
    t.string "referral"
    t.boolean "active", default: true, null: false
    t.string "comment", default: "", null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.integer "referral_group_id"
    t.index "lower((referral)::text)", name: "index_referral_filters_on_lowercase_referral", unique: true
    t.index ["referral"], name: "index_referral_filters_on_referral"
    t.index ["referral_group_id"], name: "index_referral_filters_on_referral_group_id"
  end

  create_table "referral_groups", id: :serial, force: :cascade do |t|
    t.string "name", null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
  end

  create_table "referrals", id: :serial, force: :cascade do |t|
    t.string "referral"
    t.string "promocode"
    t.string "http_referrer"
    t.integer "users_count", default: 0, null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["promocode"], name: "index_referrals_on_promocode", unique: true, where: "(promocode IS NOT NULL)"
    t.index ["referral"], name: "index_referrals_on_referral", unique: true, where: "(referral IS NOT NULL)"
  end

  create_table "requisitions", id: :serial, force: :cascade do |t|
    t.string "email"
    t.string "first_name"
    t.string "last_name"
    t.string "city"
    t.string "street"
    t.float "latitude"
    t.float "longitude"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.string "building"
    t.string "phone"
    t.integer "city_id"
  end

  create_table "returned_items", force: :cascade do |t|
    t.bigint "item_id", null: false
    t.bigint "order_id", null: false
    t.bigint "returned_order_id", null: false
    t.enum "aasm_state", null: false, enum_type: "returned_item_state_enum"
    t.integer "quantity", null: false
    t.integer "real_price_kop"
    t.integer "user_price_kop"
    t.text "comment"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.integer "weights", default: [], array: true
    t.index ["item_id"], name: "index_returned_items_on_item_id"
    t.index ["order_id", "item_id"], name: "index_returned_items_on_order_id_and_item_id", unique: true
    t.index ["returned_order_id"], name: "index_returned_items_on_returned_order_id"
  end

  create_table "returned_order_assignments", force: :cascade do |t|
    t.bigint "returned_order_id", null: false
    t.bigint "employee_id", null: false
    t.enum "assignment_type", null: false, enum_type: "returned_order_assignment_type"
    t.enum "assignment_status", default: "pending", null: false, enum_type: "returned_order_assignment_status"
    t.bigint "telegram_id", null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["employee_id"], name: "index_returned_order_assignments_on_employee_id"
    t.index ["returned_order_id"], name: "index_active_returned_order_assignments_on_returned_order_id", unique: true, where: "(assignment_status = 'active'::returned_order_assignment_status)"
    t.index ["returned_order_id"], name: "index_returned_order_assignments_on_returned_order_id"
    t.index ["telegram_id", "assignment_type"], name: "idx_active_assignments_on_telegram_id_and_assignment_type", unique: true, where: "(assignment_status = 'active'::returned_order_assignment_status)"
  end

  create_table "returned_orders", force: :cascade do |t|
    t.bigint "order_id", null: false
    t.enum "aasm_state", null: false, enum_type: "returned_order_state_enum"
    t.datetime "moderated_at", precision: nil
    t.bigint "moderated_employee_id"
    t.text "comment"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.integer "returned_real_price_kop"
    t.integer "box_number"
    t.index ["aasm_state"], name: "index_returned_orders_on_aasm_state"
    t.index ["moderated_employee_id"], name: "index_returned_orders_on_moderated_employee_id"
    t.index ["order_id"], name: "index_returned_orders_on_order_id"
  end

  create_table "returned_receipts", force: :cascade do |t|
    t.bigint "returned_order_id", null: false
    t.string "photo"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.decimal "total", precision: 10, scale: 2
    t.string "fn"
    t.string "serial_number"
    t.string "fp"
    t.string "n"
    t.datetime "payment_at", precision: nil
    t.index ["fn", "serial_number"], name: "FN_document_uniqueness", unique: true
    t.index ["returned_order_id"], name: "index_returned_receipts_on_returned_order_id"
  end

  create_table "route_categories", id: :serial, force: :cascade do |t|
    t.integer "shop_id"
    t.integer "position", default: 0
    t.string "name"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.string "file"
    t.string "ean_codes", default: [], null: false, array: true
    t.index ["shop_id"], name: "index_route_categories_on_shop_id"
  end

  create_table "route_category_models", id: :serial, force: :cascade do |t|
    t.integer "route_category_id"
    t.integer "model_id"
    t.integer "position", default: 0
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["model_id"], name: "index_route_category_models_on_model_id"
    t.index ["route_category_id"], name: "index_route_category_models_on_route_category_id"
  end

  create_table "route_sheets", id: :serial, force: :cascade do |t|
    t.integer "trip_id", null: false
    t.string "pdf_file"
    t.string "contract_number", null: false
    t.string "city", null: false
    t.string "courier_full_name", null: false
    t.string "courier_passport_series", null: false
    t.string "courier_passport_number", null: false
    t.string "courier_passport_ufms", null: false
    t.string "courier_passport_date", null: false
    t.string "courier_passport_code", null: false
    t.string "courier_passport_address", null: false
    t.string "courier_inn", null: false
    t.string "courier_bank_account", null: false
    t.string "courier_bank_name", null: false
    t.string "courier_bank_ks", null: false
    t.string "courier_bank_bik", null: false
    t.string "operator_name", null: false
    t.string "operator_legal_address", null: false
    t.string "operator_inn", null: false
    t.string "operator_kpp"
    t.string "operator_ogrn", null: false
    t.string "operator_current_account", null: false
    t.string "operator_bank_name", null: false
    t.string "operator_bik", null: false
    t.string "operator_correspondent_account", null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.boolean "signed", default: false
    t.bigint "delivery_route_id"
    t.datetime "signed_at", precision: nil
    t.index ["delivery_route_id"], name: "index_route_sheets_on_delivery_route_id", unique: true
    t.index ["trip_id"], name: "index_route_sheets_on_trip_id"
  end

  create_table "sample_campaign_shops", force: :cascade do |t|
    t.bigint "sample_campaign_id"
    t.bigint "shop_id"
    t.integer "order_ids", default: [], null: false, array: true
    t.boolean "available", default: true, null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["order_ids"], name: "index_sample_campaign_shops_on_order_ids", using: :gin
    t.index ["sample_campaign_id", "shop_id"], name: "index_sample_campaign_shops_on_sample_campaign_id_and_shop_id", unique: true
    t.index ["shop_id"], name: "index_sample_campaign_shops_on_shop_id"
  end

  create_table "sample_campaigns", force: :cascade do |t|
    t.string "name", null: false
    t.string "client", null: false
    t.date "start_at", null: false
    t.date "expire_at"
    t.boolean "hidden", default: false, null: false
    t.integer "category_ids", default: [], null: false, array: true
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "sap_codes", id: :serial, force: :cascade do |t|
    t.integer "model_id", null: false
    t.enum "shop_group", null: false, enum_type: "shop_group_enum"
    t.string "sap_code", null: false
    t.datetime "created_at", precision: nil
    t.datetime "updated_at", precision: nil
    t.index ["model_id", "sap_code", "shop_group"], name: "index_sap_codes_on_model_id_and_sap_code_and_shop_group", unique: true
    t.index ["sap_code"], name: "index_sap_codes_on_sap_code"
  end

  create_table "scores", id: :serial, force: :cascade do |t|
    t.integer "order_id", null: false
    t.integer "user_id", null: false
    t.integer "worker_id", null: false
    t.float "points", default: 0.0
    t.text "comment"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.datetime "changed_state_at", precision: nil
    t.integer "changed_state_employee_id"
    t.boolean "is_moderated"
    t.enum "user_type", default: "User", null: false, enum_type: "user_type_enum"
    t.index ["order_id"], name: "index_scores_on_order_id"
    t.index ["user_type", "user_id"], name: "index_scores_on_user_type_and_user_id"
    t.index ["worker_id", "created_at"], name: "index_scores_on_worker_id_and_created_at"
  end

  create_table "self_employed_changes", force: :cascade do |t|
    t.bigint "employee_id", null: false
    t.bigint "set_by_employee_id", null: false
    t.datetime "applied_at", precision: nil
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["employee_id"], name: "index_self_employed_changes_on_employee_id", unique: true
  end

  create_table "shared_item_amounts", force: :cascade do |t|
    t.bigint "user_id"
    t.string "item_source_type"
    t.bigint "item_source_id"
    t.integer "amount"
    t.integer "weight"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["item_source_type", "item_source_id"], name: "index_shared_item_amounts_on_item_source"
    t.index ["user_id", "item_source_id", "item_source_type"], name: "index_shared_item_amounts_on_user_id_and_item_source"
    t.index ["user_id"], name: "index_shared_item_amounts_on_user_id"
  end

  create_table "shop_categories_payment_configurations", force: :cascade do |t|
    t.bigint "shop_id", null: false
    t.bigint "category_id", null: false
    t.string "cloud_payments_public_id", null: false
    t.string "cloud_payments_secret", null: false
    t.string "entity_name"
    t.string "tinkoff_terminal_id"
    t.string "tinkoff_terminal_pass"
    t.string "entity_inn"
    t.string "actual_address"
    t.string "entity_phone"
    t.string "public_offer_url"
    t.string "contract_number"
    t.date "contract_date"
    t.string "entity_address"
    t.index ["category_id"], name: "index_shop_categories_payment_configurations_on_category_id"
    t.index ["shop_id"], name: "index_shop_categories_payment_configurations_on_shop_id"
  end

  create_table "shop_external_catalog_settings", force: :cascade do |t|
    t.bigint "shop_id", null: false
    t.boolean "pharmacy_enabled", default: false, null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["shop_id"], name: "index_shop_external_catalog_settings_on_shop_id", unique: true
  end

  create_table "shop_external_integration_settings", force: :cascade do |t|
    t.bigint "shop_id"
    t.float "yandex_eda_markup_percent", default: 0.0, null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.boolean "yandex_eda_accepts_orders", default: false, null: false
    t.float "yandex_eda_royalty_percent", default: 0.0, null: false
  end

  create_table "shop_load_stats", id: :serial, force: :cascade do |t|
    t.integer "shop_id", null: false
    t.integer "delivery_zone_id", null: false
    t.string "kind", null: false
    t.integer "pickers_started", default: 0, null: false
    t.integer "couriers_started", default: 0, null: false
    t.integer "pickers_total", default: 0, null: false
    t.integer "couriers_total", default: 0, null: false
    t.integer "nearest_delivery_minutes_real", default: 0, null: false
    t.datetime "calculated_at", precision: nil, null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.integer "nearest_delivery_minutes_smoothed", default: 0, null: false
    t.boolean "smoothed", default: false, null: false
    t.datetime "smooth_slot_1", precision: nil
    t.datetime "smooth_slot_2", precision: nil
    t.index ["calculated_at", "shop_id", "delivery_zone_id"], name: "index_shop_load_stats_on_calc_shop_zone", unique: true
    t.index ["shop_id", "delivery_zone_id"], name: "index_shop_load_stats_on_shop_id_and_delivery_zone_id"
  end

  create_table "shop_logistics_settings", id: :serial, force: :cascade do |t|
    t.integer "shop_id", null: false
    t.enum "preferred_provider", default: "yandex", null: false, enum_type: "delivery_planning_providers_enum"
    t.integer "threshold", default: 0, null: false
    t.boolean "enabled", default: false, null: false
    t.boolean "hold", default: false, null: false
    t.boolean "zero_rate_kpi", default: false, null: false
    t.boolean "wiretap", default: false, null: false
    t.integer "loading_time", default: 20
    t.bigint "yandex_version_id", default: 1, null: false
    t.index ["shop_id"], name: "index_shop_logistics_settings_on_shop_id"
    t.index ["yandex_version_id"], name: "index_shop_logistics_settings_on_yandex_version_id"
  end

  create_table "shop_notification_settings", id: :serial, force: :cascade do |t|
    t.integer "shop_id", null: false
    t.integer "shift_notification_receivers", default: [], null: false, array: true
    t.integer "picker_order_receivers", default: [], null: false, array: true
    t.integer "shop_load_receivers", default: [], null: false, array: true
    t.integer "receipt_notification_receivers", default: [], array: true
    t.integer "filled_order_receivers", default: [], null: false, array: true
    t.index ["shop_id"], name: "index_shop_notification_settings_on_shop_id"
  end

  create_table "shop_payment_settings", id: :serial, force: :cascade do |t|
    t.integer "shop_id"
    t.jsonb "courier_payment_settings", default: {}
    t.jsonb "picker_payment_settings", default: {}
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["shop_id"], name: "index_shop_payment_settings_on_shop_id"
  end

  create_table "shops", id: :serial, force: :cascade do |t|
    t.string "name"
    t.string "legal_address"
    t.string "street"
    t.string "building"
    t.float "latitude"
    t.float "longitude"
    t.string "phone"
    t.string "inn"
    t.string "okved"
    t.string "okpo"
    t.string "kpp"
    t.string "bank_name"
    t.string "current_account"
    t.string "account_number"
    t.string "bik"
    t.string "ogrn"
    t.integer "open_hour"
    t.integer "closing_hour"
    t.boolean "day_and_night"
    t.boolean "open", default: false, null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.integer "time_step", default: 30
    t.integer "categories_order", array: true
    t.integer "inner_index"
    t.integer "picker_assign_interval", default: 3
    t.string "group"
    t.integer "time_before_slot", default: 80
    t.integer "base_shipping_price"
    t.integer "courier_rate", default: 0
    t.decimal "discount", precision: 10, scale: 2, default: "0.0", null: false
    t.decimal "discount_sale", precision: 10, scale: 2, default: "0.0", null: false
    t.integer "operator_id", null: false
    t.integer "city_id", null: false
    t.text "branding"
    t.integer "assembly_price", default: 99
    t.integer "lower_assembly_limit", default: 2000
    t.string "legal_name", default: "", null: false
    t.jsonb "payment_types"
    t.enum "orders_sort_type", default: "by_start_packing_deadline", null: false, enum_type: "shop_orders_sort_type"
    t.integer "first_shipping_price"
    t.integer "first_assembly_price"
    t.boolean "soft_receipts", default: false, null: false
    t.boolean "picker_assign_early", default: false, null: false
    t.decimal "service_fee", precision: 10, scale: 2, default: "0.0", null: false
    t.float "postpaid_comission", default: 0.0, null: false
    t.float "individual_comission", default: 0.0, null: false
    t.float "legal_entity_comission", default: 0.0, null: false
    t.float "catalog_markup_percent", default: 0.0, null: false
    t.enum "brand_label", enum_type: "shop_brand_label"
    t.decimal "subagent_reward_percent", precision: 5, scale: 2, default: "0.0", null: false
    t.float "entity_catalog_markup_percent", default: 0.0, null: false
    t.integer "entity_shipping_price", default: 0
    t.integer "in_stock_products_count", default: 0, null: false
    t.text "type", default: "Shop", null: false
    t.boolean "available_for_entity", default: true, null: false
    t.index ["open"], name: "index_open"
  end

  create_table "sms_deliveries", force: :cascade do |t|
    t.string "owner_type", null: false
    t.bigint "owner_id", null: false
    t.string "provider", null: false
    t.string "tx_id"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.jsonb "log_data"
    t.index ["owner_type", "owner_id"], name: "index_sms_deliveries_on_owner_type_and_owner_id"
  end

  create_table "terminals", id: :serial, force: :cascade do |t|
    t.boolean "active", default: true, null: false
    t.text "comment", default: "", null: false
    t.string "num_terminal", limit: 20, null: false
    t.integer "shop_id", null: false
    t.integer "exchange", default: 0, null: false
    t.integer "encashment", default: 0, null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.string "terminal_sn", default: "", null: false
    t.datetime "deleted_at", precision: nil
    t.index ["num_terminal"], name: "index_terminals_on_num_terminal", unique: true, where: "(deleted_at IS NULL)"
  end

  create_table "tinkoff_terminal_transactions", force: :cascade do |t|
    t.bigint "terminal_id", null: false
    t.string "bank_transaction_id", null: false, comment: "Bank transaction ID"
    t.datetime "transaction_at", precision: nil, null: false, comment: "Date and time of the transaction"
    t.integer "amount", null: false, comment: "Amount in russian rubles in 'копейка'."
    t.string "card_number", null: false, comment: "Card number, example: 999999xxxxxx9999"
    t.enum "transaction_type", null: false, comment: "Type of operation, enum: debit/credit/other", enum_type: "tinkoff_terminal_transactions_type_enum"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.bigint "hour_id", null: false
    t.index ["bank_transaction_id", "terminal_id", "hour_id", "amount", "card_number"], name: "index_tinkoff_terminal_transactions_unique", unique: true
    t.index ["hour_id"], name: "index_tinkoff_terminal_transactions_on_hour_id"
    t.index ["terminal_id"], name: "index_tinkoff_terminal_transactions_on_terminal_id"
  end

  create_table "trailers", id: :serial, force: :cascade do |t|
    t.string "city"
    t.string "street"
    t.string "wing"
    t.string "building"
    t.string "name"
    t.string "note"
    t.float "latitude"
    t.float "longitude"
    t.datetime "created_at", precision: nil
    t.datetime "updated_at", precision: nil
    t.string "gs_employee"
    t.string "photo"
    t.string "mapimage"
    t.string "maplink"
    t.string "gs_controller"
    t.boolean "enabled", default: true
    t.integer "shop_id"
    t.integer "price"
    t.text "payload"
    t.string "digest"
    t.index ["shop_id"], name: "index_trailers_on_shop_id"
  end

  create_table "trips", id: :serial, force: :cascade do |t|
    t.integer "employee_id", null: false
    t.integer "task_id"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.string "contract"
    t.string "fns_receipt_uri"
    t.string "code"
    t.datetime "code_send_at", precision: nil
    t.enum "aasm_state", default: "created", null: false, enum_type: "trip_states_enum"
    t.integer "fee"
    t.string "act"
    t.integer "hour_id"
    t.boolean "act_signed", default: false
    t.boolean "skipped", default: false, null: false
    t.datetime "act_generating_start_at", precision: nil
    t.boolean "contract_signed", default: false, null: false
    t.datetime "contract_signed_at", precision: nil
    t.string "contract_signed_with_code"
    t.datetime "act_signed_at", precision: nil
    t.string "act_signed_with_code"
    t.index ["employee_id"], name: "index_trips_on_employee_id"
    t.index ["hour_id"], name: "index_trips_on_hour_id"
  end

  create_table "unique_configurations", force: :cascade do |t|
    t.text "key", null: false
    t.text "schema", null: false
    t.jsonb "payload", default: "{}::jsonb", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.jsonb "log_data"
    t.index ["key"], name: "index_unique_configurations_on_key", unique: true
  end

  create_table "user_comments", id: :serial, force: :cascade do |t|
    t.integer "user_id", null: false
    t.integer "employee_id", null: false
    t.string "comment", null: false
    t.boolean "is_deleted", default: false, null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.enum "type", enum_type: "user_comments_type"
    t.enum "user_type", default: "User", null: false, enum_type: "user_type_enum"
    t.index ["employee_id"], name: "index_user_comments_on_employee_id"
    t.index ["user_type", "user_id"], name: "index_user_comments_on_user_type_and_user_id"
  end

  create_table "user_deletion_requests", force: :cascade do |t|
    t.bigint "user_id", null: false
    t.enum "aasm_state", default: "created", null: false, enum_type: "user_deletion_request_status_enum"
    t.text "reason"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["user_id", "aasm_state"], name: "index_user_deletion_requests_on_user_id_and_aasm_state"
  end

  create_table "user_notification_settings", force: :cascade do |t|
    t.bigint "user_id"
    t.boolean "order_status_push_enabled", default: true, null: false
    t.boolean "order_invoices_email_enabled", default: true, null: false
    t.boolean "sales_push_enabled", default: true, null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["user_id"], name: "index_user_notification_settings_on_user_id"
  end

  create_table "user_set_models", force: :cascade do |t|
    t.bigint "user_set_id", null: false
    t.bigint "model_id", null: false
    t.integer "weight"
    t.integer "amount"
    t.string "comment"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["model_id"], name: "index_user_set_models_on_model_id"
    t.index ["user_set_id"], name: "index_user_set_models_on_user_set_id"
  end

  create_table "user_sets", force: :cascade do |t|
    t.bigint "user_id"
    t.string "name", null: false
    t.string "description"
    t.string "color"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["user_id"], name: "index_user_sets_on_user_id"
  end

  create_table "users", id: :serial, force: :cascade do |t|
    t.string "first_name"
    t.string "last_name"
    t.string "patronymic"
    t.citext "email"
    t.string "encrypted_password", default: "", null: false
    t.string "reset_password_token"
    t.datetime "reset_password_sent_at", precision: nil
    t.datetime "remember_created_at", precision: nil
    t.integer "sign_in_count", default: 0, null: false
    t.datetime "current_sign_in_at", precision: nil
    t.datetime "last_sign_in_at", precision: nil
    t.string "current_sign_in_ip"
    t.string "last_sign_in_ip"
    t.string "confirmation_token"
    t.datetime "confirmed_at", precision: nil
    t.datetime "confirmation_sent_at", precision: nil
    t.citext "unconfirmed_email"
    t.integer "failed_attempts", default: 0, null: false
    t.string "unlock_token"
    t.datetime "locked_at", precision: nil
    t.string "phone"
    t.string "unconfirmed_phone"
    t.string "confirmation_code"
    t.enum "behavior", default: "call_or_hide", enum_type: "behavior_enum"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.boolean "as_entity", default: false
    t.datetime "confirmation_code_send_at", precision: nil
    t.boolean "as_consignee", default: false
    t.integer "inviter_id"
    t.text "comment"
    t.integer "orders_count", default: 0
    t.datetime "last_order_at", precision: nil
    t.string "authentication_token", limit: 30
    t.string "device_id"
    t.string "avatar"
    t.string "kind", default: "web", null: false
    t.string "payment_type", default: "cash"
    t.datetime "phone_confirmed_at", precision: nil
    t.integer "referral_id"
    t.string "session_key"
    t.boolean "blocked", default: false
    t.string "blocked_comment"
    t.datetime "blocked_at", precision: nil
    t.integer "blocked_employee_id"
    t.string "gender"
    t.uuid "public_id", default: -> { "public.gen_random_uuid()" }
    t.date "date_of_birth"
    t.datetime "registered_at", precision: nil
    t.text "authentication_tokens", default: [], null: false, array: true
    t.datetime "next_order_at", precision: nil
    t.index ["authentication_token"], name: "index_users_on_authentication_token", unique: true
    t.index ["confirmation_token"], name: "index_users_on_confirmation_token", unique: true
    t.index ["date_of_birth"], name: "index_users_on_date_of_birth"
    t.index ["device_id"], name: "index_users_on_device_id"
    t.index ["email"], name: "index_users_on_email"
    t.index ["inviter_id"], name: "index_users_on_inviter_id", where: "(inviter_id IS NOT NULL)"
    t.index ["phone"], name: "index_users_on_phone", unique: true
    t.index ["referral_id"], name: "index_users_on_referral_id", where: "(referral_id IS NOT NULL)"
    t.index ["reset_password_token"], name: "index_users_on_reset_password_token", unique: true
    t.index ["unconfirmed_phone"], name: "index_users_on_unconfirmed_phone"
    t.index ["unlock_token"], name: "index_users_on_unlock_token", unique: true
  end

  create_table "vehicle_specs", id: :serial, force: :cascade do |t|
    t.string "name"
    t.integer "capacity"
  end

  create_table "versions", id: :serial, force: :cascade do |t|
    t.string "item_type", null: false
    t.integer "item_id", null: false
    t.string "event", null: false
    t.string "whodunnit"
    t.jsonb "object"
    t.datetime "created_at", precision: nil
    t.jsonb "object_changes"
    t.string "whodunnit_type"
    t.index ["item_id"], name: "index_versions_on_item_id"
    t.index ["item_type", "item_id"], name: "index_versions_on_item_type_and_item_id"
  end

  create_table "vocabulary_product_synonyms", id: :serial, force: :cascade do |t|
    t.string "word", null: false
    t.string "nominative_case", null: false
    t.string "synonyms"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["word"], name: "index_vocabulary_product_synonyms_on_word", unique: true
  end

  create_table "vocabulary_stop_words", force: :cascade do |t|
    t.string "list"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "yandex_routing_penalties", force: :cascade do |t|
    t.bigint "version_id", null: false
    t.string "key"
    t.integer "value"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["version_id"], name: "index_yandex_routing_penalties_on_version_id"
  end

  create_table "yandex_routing_versions", force: :cascade do |t|
    t.string "name", null: false
    t.string "description"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
  end

  add_foreign_key "ab_test_orders_histories", "ab_tests"
  add_foreign_key "ab_test_orders_histories", "shops"
  add_foreign_key "ab_test_orders_histories", "users"
  add_foreign_key "ab_test_participations", "ab_tests"
  add_foreign_key "ab_test_participations", "users"
  add_foreign_key "ab_tests_cities_relations", "ab_tests"
  add_foreign_key "ab_tests_cities_relations", "cities"
  add_foreign_key "accruals", "accrual_types"
  add_foreign_key "accruals", "employees"
  add_foreign_key "accruals", "employees", column: "author_id"
  add_foreign_key "billing_transactions", "employees"
  add_foreign_key "bills", "entities"
  add_foreign_key "categories", "category_groups"
  add_foreign_key "courier_rate_resets", "hours", column: "shift_id"
  add_foreign_key "day_schedule_presets", "shops"
  add_foreign_key "day_schedules", "shops"
  add_foreign_key "delivery_eta_requests", "delivery_routes"
  add_foreign_key "delivery_plan_extras", "delivery_plans"
  add_foreign_key "delivery_plans", "shops"
  add_foreign_key "delivery_routes", "delivery_plans"
  add_foreign_key "delivery_routes", "employees", column: "courier_id"
  add_foreign_key "delivery_routes", "hours", column: "shift_id"
  add_foreign_key "delivery_zones", "areas"
  add_foreign_key "delivery_zones", "shops"
  add_foreign_key "employee_additional_acts", "employees"
  add_foreign_key "employee_additional_acts", "hours"
  add_foreign_key "employee_notification_devices", "employees"
  add_foreign_key "employee_payments", "employees"
  add_foreign_key "employee_positions", "employees"
  add_foreign_key "employee_positions", "hours"
  add_foreign_key "employee_positions", "shops"
  add_foreign_key "employee_want_bonus", "employees"
  add_foreign_key "employees", "operators"
  add_foreign_key "entity_documents", "entities"
  add_foreign_key "favorite_models", "models"
  add_foreign_key "feedbacks", "models"
  add_foreign_key "feedbacks", "products"
  add_foreign_key "feedbacks", "shops"
  add_foreign_key "feedbacks", "users"
  add_foreign_key "fields", "categories"
  add_foreign_key "honest_labels", "honest_label_types"
  add_foreign_key "honest_labels", "models"
  add_foreign_key "item_picker_declines", "items"
  add_foreign_key "item_unconfirmed_replacements", "items"
  add_foreign_key "item_unconfirmed_replacements", "products"
  add_foreign_key "lenta_prices", "price_files"
  add_foreign_key "models_field_values", "field_values"
  add_foreign_key "models_field_values", "fields"
  add_foreign_key "models_field_values", "models"
  add_foreign_key "notification_devices", "users"
  add_foreign_key "operators", "franchisees"
  add_foreign_key "order_picker_payments", "employee_positions"
  add_foreign_key "order_picker_payments", "hours"
  add_foreign_key "order_user_permissions", "users"
  add_foreign_key "orders", "operators"
  add_foreign_key "orders", "orders", column: "cross_sell_main_order_id"
  add_foreign_key "orders", "partner_configurations"
  add_foreign_key "orders", "route_sheets"
  add_foreign_key "orders", "trips", column: "courier_trip_id"
  add_foreign_key "orders", "trips", column: "picker_trip_id"
  add_foreign_key "places", "cities", column: "regional_center_id"
  add_foreign_key "points_flow", "coupons"
  add_foreign_key "product_line_campaign_keyword_tokens", "product_line_campaign_keywords"
  add_foreign_key "product_line_campaign_keywords", "product_line_campaigns"
  add_foreign_key "receipt_items", "items"
  add_foreign_key "receipt_items", "products"
  add_foreign_key "receipt_items", "receipts", on_update: :cascade, on_delete: :cascade
  add_foreign_key "returned_order_assignments", "employees"
  add_foreign_key "returned_order_assignments", "returned_orders"
  add_foreign_key "returned_orders", "employees", column: "moderated_employee_id"
  add_foreign_key "returned_receipts", "returned_orders"
  add_foreign_key "route_categories", "shops"
  add_foreign_key "route_category_models", "models"
  add_foreign_key "route_category_models", "route_categories"
  add_foreign_key "route_sheets", "delivery_routes"
  add_foreign_key "route_sheets", "trips"
  add_foreign_key "sample_campaign_shops", "sample_campaigns"
  add_foreign_key "sample_campaign_shops", "shops"
  add_foreign_key "self_employed_changes", "employees"
  add_foreign_key "self_employed_changes", "employees", column: "set_by_employee_id"
  add_foreign_key "shared_item_amounts", "users"
  add_foreign_key "shop_external_catalog_settings", "shops"
  add_foreign_key "shop_external_integration_settings", "shops"
  add_foreign_key "shop_logistics_settings", "yandex_routing_versions", column: "yandex_version_id"
  add_foreign_key "shop_payment_settings", "shops"
  add_foreign_key "tinkoff_terminal_transactions", "hours"
  add_foreign_key "tinkoff_terminal_transactions", "terminals"
  add_foreign_key "trailers", "shops"
  add_foreign_key "trips", "employees"
  add_foreign_key "user_deletion_requests", "users"
  add_foreign_key "user_notification_settings", "users"
  add_foreign_key "user_set_models", "models"
  add_foreign_key "user_set_models", "user_sets"
  add_foreign_key "user_sets", "users"
  add_foreign_key "users", "users", column: "inviter_id", on_delete: :restrict
  add_foreign_key "yandex_routing_penalties", "yandex_routing_versions", column: "version_id"
end
