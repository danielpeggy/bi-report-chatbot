# BI Report Chatbot

An AI-powered business intelligence platform that combines interactive QuickSight dashboards with a natural language chatbot. Ask business questions in plain English and get instant SQL-backed answers with full end-to-end data lineage.

**Live Demo**: [https://d1k3nghlesd8gk.cloudfront.net](https://d1k3nghlesd8gk.cloudfront.net)

---

## What This Does

A restaurant chain (200 stores, 30 menu items, full year 2023) uses this platform to:

1. **View interactive dashboards** — 5 QuickSight dashboards covering Executive Summary, Sales & Menu, Operations, Customer Intelligence, and Financial Performance
2. **Ask questions in natural language** — "What is the total revenue by region?" or "Which menu items have the highest profit margin?"
3. **Get SQL-backed answers** — The chatbot generates SQL, queries Redshift, and returns results with timing
4. **Trace data lineage end-to-end** — Every answer shows: Source System → S3 Raw → Glue ETL → Redshift → Dashboard Aggregation

---

## Architecture

```
Source Systems (POS, HR, Inventory, CRM, Finance)
        │
        ▼
S3 Raw Landing Zone (CSV files, monthly/daily partitions)
        │
        ▼
AWS Glue PySpark ETL (3 jobs: dimensions, facts, metadata)
        │   JOINs, type casting, calculated fields
        ▼
Amazon Redshift Serverless (star schema: 7 dim + 8 fact tables, 27M+ rows)
        │
        ├──── Amazon Bedrock (Claude) ──── Text-to-SQL generation
        │         │
        │         └── Bedrock Knowledge Base ── Schema/lineage RAG
        │
        ▼
CloudFront → S3 (static frontend) + Lambda (API backend)
        │
        ▼
Browser: QuickSight Dashboards + GenBI Chatbot
```

See [`architecture-diagram.html`](architecture-diagram.html) for the detailed visual diagram.

---

## Technology Stack

| Layer | Service | Purpose |
|-------|---------|---------|
| **Frontend** | HTML5, CSS3, JavaScript, Chart.js | Dashboard UI, chat interface |
| **CDN** | Amazon CloudFront | Global content delivery, HTTPS |
| **Static Hosting** | Amazon S3 | HTML/JS/CSS files |
| **API Backend** | AWS Lambda + Function URL | Chat API, QuickSight embed URL generation |
| **AI/ML** | Amazon Bedrock (Claude) | Natural language → SQL generation |
| **Knowledge Base** | Amazon Bedrock KB | RAG retrieval for schema, lineage, SQL examples |
| **Data Warehouse** | Amazon Redshift Serverless | Star schema analytics (27M+ rows) |
| **ETL** | AWS Glue (PySpark) | S3 CSV → Redshift transformation |
| **Dashboards** | Amazon QuickSight | 5 embedded interactive dashboards |
| **Raw Storage** | Amazon S3 | CSV data files (POS, operations, financial, customer) |

---

## Project Structure

```
bi-report-chatbot/
├── embed/
│   └── index.html              # Main app — QuickSight dashboards + chat sidebar
├── genbi/
│   ├── api.py                  # Flask REST API (chat, QuickSight embed, health)
│   ├── agent.py                # AI agent: KB retrieval → SQL generation → Redshift query
│   ├── config.py               # Master config (stores, menu items, dates)
│   ├── etl/
│   │   ├── load_dimensions.py  # Glue job: S3 → Redshift dimension tables
│   │   ├── load_facts.py       # Glue job: S3 → Redshift fact tables
│   │   └── load_metadata.py    # Glue job: ETL registry, column lineage, data dictionary
│   ├── kb_docs/                # Knowledge base documents (indexed by Bedrock KB)
│   │   ├── 01_schema_overview.md
│   │   ├── 02_data_lineage.md
│   │   ├── 03_sql_examples.md
│   │   ├── 04_business_glossary.md
│   │   ├── 05_dashboard_catalog.md
│   │   └── 06_pipeline_lineage.md
│   ├── generate_*.py           # Synthetic data generators
│   └── raw/                    # Generated data (excluded from git, ~2.4 GB)
├── sql/
│   ├── 01_schema_and_dimensions.sql
│   ├── 02_orders_data.sql
│   ├── 03_order_items_data.sql
│   └── 04_dashboard_queries.sql
├── index.html                  # Simple Chart.js dashboard (standalone)
├── app.js                      # Chart rendering & data aggregation
├── chat.js                     # Chat interface controller
├── architecture-diagram.html   # Visual system architecture
├── documentation.html          # Detailed project documentation
└── README.md
```

---

## Data Model

### Star Schema (genbi_mart)

**Dimension Tables** (7):
- `dim_date` — 365 rows (2023 calendar with HK holidays)
- `dim_store` — 200 stores across HK Island, Kowloon, New Territories
- `dim_menu_item` — 30 items in 8 categories with COGS and food cost %
- `dim_channel` — 5 order channels (counter, kiosk, mobile, delivery, drive-thru)
- `dim_payment_method` — 7 payment types (cash, Octopus, Visa, etc.)
- `dim_promotion` — 12 promotions run throughout 2023
- `dim_customer` — 50,000 loyalty program members

**Fact Tables** (8):
- `fact_sales` — 17.5M rows — transaction line items (revenue, COGS, gross profit)
- `fact_inventory` — 2.19M rows — daily stock levels, waste tracking
- `fact_labor` — 665K rows — employee shifts, labor costs, productivity
- `fact_service_performance` — 1.75M rows — hourly service times by channel
- `fact_customer_feedback` — 28K rows — CSAT ratings, sentiment, NPS
- `fact_loyalty` — 2.49M rows — points earned/redeemed, order values
- `fact_equipment` — 10K rows — maintenance events, downtime, repair costs
- `fact_financial` — 2.4K rows — monthly store P&L statements

---

## GenBI Chatbot — How It Works

```
User: "What is the total revenue by region?"
                    │
                    ▼
        ┌─── Bedrock Knowledge Base ───┐
        │  Retrieve schema, lineage,   │
        │  SQL examples via RAG        │
        └──────────┬───────────────────┘
                   ▼
        ┌─── Amazon Bedrock (Claude) ──┐
        │  Generate SQL query from     │
        │  natural language + context  │
        └──────────┬───────────────────┘
                   ▼
        ┌─── Redshift Data API ────────┐
        │  Execute SQL, return results │
        └──────────┬───────────────────┘
                   ▼
        Response with:
        - Query results (table)
        - Explanation
        - End-to-end data lineage
        - Recommended dashboard
        - SQL (expandable)
```

### Data Lineage Example

For every answer, the chatbot traces the full pipeline:

> **Source System**: POS terminals (store registers) →
>
> **S3 Raw Landing**:
> s3://.../pos/transactions/ (monthly CSV with transaction headers) AND
> s3://.../pos/line_items/ (line-level details: item, quantity, price) →
>
> **Glue ETL** (load_fact_sales): Joins transactions + line_items ON transaction_id, calculates gross_profit = line_total - discount - COGS →
>
> **Redshift** genbi_mart.fact_sales:
> 17.5M rows, grain = one row per line item per transaction →
>
> **Dashboard Aggregation**:
> COUNT(DISTINCT transaction_id) to convert line-item grain to order count

### Topic Guardrails

The chatbot only responds to restaurant operations questions. Off-topic queries (politics, weather, coding, etc.) receive a polite redirect.

---

## QuickSight Dashboards

| Dashboard | Key Metrics | Data Sources |
|-----------|-------------|--------------|
| **Executive Summary** | Total revenue, orders, gross profit, regional breakdown, monthly trend | fact_sales + dim_date + dim_store |
| **Sales & Menu** | Revenue by category, top items, channel mix, payment methods, hourly pattern | fact_sales + dim_menu_item + dim_channel + dim_payment_method |
| **Operations** | Labor cost, staffing efficiency, shift productivity, hours/shift | fact_labor + dim_store + dim_date |
| **Customer Intelligence** | CSAT rating, NPS, sentiment, recommendation rate, by region | fact_customer_feedback + dim_store |
| **Financial Performance** | EBITDA, net profit, margins, cost breakdown, monthly P&L | fact_financial + dim_store + dim_date |

---

## Deployment

### Prerequisites
- AWS Account with Redshift Serverless, Bedrock, QuickSight, Glue enabled
- Python 3.9+
- AWS CLI configured

### Quick Start (Local Development)
```bash
# Clone the repo
git clone https://github.com/danielpeggy/bi-report-chatbot.git
cd bi-report-chatbot

# Generate synthetic data (optional — ~2.4 GB)
python3 generate_data.py
cd genbi && python3 generate_pos.py && python3 generate_operations.py && python3 generate_market_financial.py

# Start the API server
cd genbi
python3 api.py
# Server runs at http://localhost:5001

# Open dashboard in browser
open http://localhost:5001
```

### Production Deployment (AWS)
1. **Redshift**: Create serverless workgroup, run SQL scripts from `sql/`
2. **Glue**: Upload ETL scripts from `genbi/etl/`, create and run jobs
3. **Bedrock KB**: Create knowledge base, point to `kb_docs/` in S3
4. **QuickSight**: Create 5 dashboards, configure embedding
5. **Lambda**: Package `agent.py` + dependencies as Lambda function
6. **S3 + CloudFront**: Upload static files, configure distribution

See [`documentation.html`](documentation.html) for detailed step-by-step instructions.

---

## Data Generation

All data is synthetically generated with seed 42 (fully reproducible). Realistic patterns include:
- Seasonal variation (summer tourism, winter holidays, typhoon season)
- Geographic variation (income by district, foot traffic)
- Temporal patterns (lunch/dinner peaks, weekend spikes)
- Supply chain volatility (typhoon impact on reliability)
- Equipment failures (ice cream machines break more frequently)

---

## License

This project is provided as a reference implementation for AI-powered BI platforms on AWS.
