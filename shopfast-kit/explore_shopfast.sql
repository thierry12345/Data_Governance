-- CM 2 lab (24 Nov) - Explore the ShopFast raw data
-- Run in psql:  docker exec -it shopfast-db psql -U shopfast_admin -d shopfast
-- (or any SQL client: host localhost, port 5432, db shopfast, user/password shopfast_admin)

-- 1. Which tables exist?
\dt raw.*

-- 2. How many rows per table?
SELECT 'customers' AS t, count(*) FROM raw.customers
UNION ALL SELECT 'products', count(*) FROM raw.products
UNION ALL SELECT 'orders', count(*) FROM raw.orders
UNION ALL SELECT 'order_items', count(*) FROM raw.order_items
UNION ALL SELECT 'payments', count(*) FROM raw.payments
UNION ALL SELECT 'support_tickets', count(*) FROM raw.support_tickets
UNION ALL SELECT 'marketing_campaign_export', count(*) FROM raw.marketing_campaign_export;

-- 3. Look at 10 rows of a table (change the name)
SELECT * FROM raw.customers LIMIT 10;

-- 4. How many distinct values does a column have? (good for spotting inconsistent codes)
SELECT country, count(*) FROM raw.customers GROUP BY country ORDER BY 2 DESC;

-- 5. How many empty values?
SELECT count(*) FILTER (WHERE email IS NULL OR email = '') AS empty_emails FROM raw.customers;

-- 6. Is the "id" really unique?
SELECT customer_id, count(*) FROM raw.customers GROUP BY customer_id HAVING count(*) > 1;

-- 7. Your own queries below: try orders.status, orders.order_date, products.category ...
