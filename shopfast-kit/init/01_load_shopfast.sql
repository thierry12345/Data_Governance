-- Loads the raw ShopFast CSV files into the "raw" schema.
-- Raw = landing zone: every column is TEXT, exactly as the source sent it (dirty on purpose).
CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE raw.customers (customer_id TEXT, first_name TEXT, last_name TEXT, email TEXT, phone TEXT,
  birth_date TEXT, address TEXT, city TEXT, postal_code TEXT, country TEXT, signup_date TEXT,
  marketing_consent TEXT, loyalty_tier TEXT);
CREATE TABLE raw.products (product_id TEXT, sku TEXT, product_name TEXT, category TEXT, unit_price_eur TEXT,
  supplier TEXT, is_active TEXT);
CREATE TABLE raw.orders (order_id TEXT, customer_id TEXT, order_date TEXT, status TEXT, channel TEXT,
  shipping_country TEXT, total_amount_eur TEXT);
CREATE TABLE raw.order_items (order_item_id TEXT, order_id TEXT, product_id TEXT, quantity TEXT, unit_price_eur TEXT);
CREATE TABLE raw.payments (payment_id TEXT, order_id TEXT, payment_date TEXT, method TEXT, amount TEXT,
  currency TEXT, card_last4 TEXT, status TEXT);
CREATE TABLE raw.support_tickets (ticket_id TEXT, customer_id TEXT, created_at TEXT, channel TEXT, subject TEXT,
  message TEXT, agent_notes TEXT);
CREATE TABLE raw.marketing_campaign_export (customer_id TEXT, email TEXT, first_name TEXT, loyalty_tier TEXT, campaign TEXT);

COPY raw.customers FROM '/data/customers.csv' WITH (FORMAT csv, HEADER true);
COPY raw.products FROM '/data/products.csv' WITH (FORMAT csv, HEADER true);
COPY raw.orders FROM '/data/orders.csv' WITH (FORMAT csv, HEADER true);
COPY raw.order_items FROM '/data/order_items.csv' WITH (FORMAT csv, HEADER true);
COPY raw.payments FROM '/data/payments.csv' WITH (FORMAT csv, HEADER true);
COPY raw.support_tickets FROM '/data/support_tickets.csv' WITH (FORMAT csv, HEADER true);
COPY raw.marketing_campaign_export FROM '/data/marketing_campaign_export.csv' WITH (FORMAT csv, HEADER true);
