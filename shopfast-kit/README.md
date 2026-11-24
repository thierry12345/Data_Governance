# ShopFast kit — Data Governance for Engineers

ShopFast is a fictional French e-commerce company. This kit holds its raw data and a local PostgreSQL database.
All people in the data are fake (generated). The data is dirty **on purpose**: you will find and fix the problems in the labs.

| File | What it is |
|---|---|
| `data/customers.csv` | Customers (personal data!) |
| `data/products.csv` | Product catalogue |
| `data/orders.csv`, `data/order_items.csv` | Orders and order lines |
| `data/payments.csv` | Payments (amount in EUR) |
| `data/support_tickets.csv` | Customer-service tickets (free text) |
| `data/marketing_campaign_export.csv` | An export someone made for a marketing campaign |
| `docker-compose.yml`, `init/` | Starts PostgreSQL 16 and loads the CSVs into schema `raw` |
| `requirements.txt` | Python packages for the course |
| `check_setup.py` | Self-test: run it before the CM 2 lab (24 Nov) |

Start: `docker compose up -d` · Stop: `docker compose stop` · Reset: `docker compose down -v && docker compose up -d`

Database login (local training only): host `localhost`, port `5432`, db `shopfast`, user `shopfast_admin`, password `shopfast_admin`.
