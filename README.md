# DataStore360 — Retail Data Pipeline

## Overview

DataStore360 is a retail data engineering project designed to simulate the industrialization of a complete data pipeline.

The objective is to build a simple, reliable, secure, and reproducible data system that allows the data team to audit, clean, protect, structure, load, and analyze sales data related to orders, customers, and products.

The project applies key data engineering principles, including:

- Data exploration and profiling
- Data quality control
- GDPR compliance
- Customer data pseudonymization
- Staging/core data architecture
- PostgreSQL relational modeling
- Automated ETL pipeline
- Apache Airflow orchestration
- Idempotent and reproducible processing

---

## Project Context

The retail company **DataStore360** wants to improve the reliability and security of its sales data exploitation.

The company needs a complete data pipeline capable of processing raw sales data, identifying quality issues, cleaning anomalies, protecting personal information, and loading normalized data into a PostgreSQL database.

The final system must make the data exploitable for analytics while respecting data quality and GDPR requirements.

---

## Main Objectives

The project has three main objectives:

### 1. Data Exploration and Audit

The first step consists of understanding the source dataset and evaluating its quality.

This includes:

- Exploring the dataset structure
- Analyzing column types and distributions
- Detecting missing values
- Detecting duplicated records
- Identifying invalid dates
- Identifying inconsistent business values
- Detecting outliers
- Analyzing trends by category, region, and customer segment
- Generating a data profiling report

### 2. GDPR Compliance and Data Cleaning

The second step consists of cleaning the data and protecting personal information.

This includes:

- Identifying personal data in the dataset
- Pseudonymizing `Customer Name`
- Applying SHA-256 hashing
- Treating missing values
- Removing duplicates
- Handling invalid discounts
- Handling negative quantities
- Handling invalid delivery dates
- Creating derived business variables such as:

  - `delivery_time`
  - `profit_margin`

### 3. Structuring and Orchestration

The final step consists of storing and orchestrating the data pipeline.

This includes:

- Designing a PostgreSQL database with two layers:

  - `staging`
  - `core`

- Loading raw data into the staging layer
- Transforming and cleaning data
- Loading normalized data into the core layer
- Automating the pipeline with Apache Airflow
- Ensuring idempotent execution
- Validating the quality of loaded data

---

## Business Rules

The project follows these business rules:

- Each order is linked to one unique customer.
- Each order is linked to one unique product.
- A customer can place multiple orders.
- A product can appear in multiple orders.
- `Customer Name` must never appear in clear text in the `core` layer.
- The `staging` layer receives raw data exactly as it appears in the source CSV file.
- A discount greater than 100% is considered invalid.
- A negative quantity is considered invalid.
- A ship date earlier than the order date is considered invalid.
- Missing values, duplicates, invalid date formats, and values outside logical ranges must be detected and treated.

---

## Technical Stack

### Data Processing

- Python
- Pandas
- NumPy

### Data Visualization

- Matplotlib
- Seaborn

### Data Profiling

- ydata-profiling

### GDPR Compliance

- hashlib
- SHA-256 hashing

### Database

- PostgreSQL
- pgAdmin
- SQLAlchemy
- psycopg2

### Orchestration

- Apache Airflow
- TaskFlow API
- PostgresHook

### Project Management and Versioning

- Jira
- Git
- GitHub
- uv

---

## Project Architecture

```txt
datastore360-pipeline/
│
├── dags/
│   └── datastore360_pipeline.py
│
├── data/
│   ├── raw/
│   │   └── superstore.csv
│   ├── processed/
│   │   └── superstore_cleaned.csv
│   └── profiling/
│       └── profiling_report.html
│
├── notebooks/
│   └── 01_exploration_audit.ipynb
│
├── sql/
│   ├── 01_create_schemas.sql
│   ├── 02_create_staging_tables.sql
│   ├── 03_create_core_tables.sql
│   └── 04_quality_checks.sql
│
├── src/
│   └── datastore360/
│       ├── config/
│       │   └── settings.py
│       ├── extraction/
│       │   └── extract.py
│       ├── loading/
│       │   └── load.py
│       ├── transformation/
│       │   └── transform.py
│       ├── validation/
│       │   └── quality_checks.py
│       └── utils/
│           └── hashing.py
│
├── reports/
│   └── final_report.md
│
├── tests/
│
├── pyproject.toml
├── uv.lock
├── .env.example
├── .gitignore
└── README.md
```

---

## Database Architecture

The database is organized into two schemas:

---

## 1. Staging Layer

The staging layer stores the raw source data without transformation.

### Table: `staging.superstore_raw`

This table is a raw mirror of the original CSV file.

It contains all columns from the source dataset without constraints, cleaning, transformation, or anonymization.

Purpose:

- Keep the original data traceable
- Separate raw data from cleaned data
- Allow auditing and reproducibility
- Preserve the source format before transformation

---

## 2. Core Layer

The core layer stores cleaned, normalized, and GDPR-compliant data.

### Table: `core.customers`

Stores customer-related information.

Columns:

- `customer_id`
- `customer_name`
- `segment`
- `country`
- `city`
- `state`
- `postal_code`
- `region`

Important rule:

`customer_name` is pseudonymized using SHA-256 hashing and must not contain the original customer name.

---

### Table: `core.products`

Stores product-related information.

Columns:

- `product_id`
- `category`
- `sub_category`
- `product_name`

---

### Table: `core.orders`

Stores order-related information.

Columns:

- `row_id`
- `order_id`
- `customer_id`
- `product_id`
- `order_date`
- `ship_date`
- `ship_mode`
- `sales`
- `quantity`
- `discount`
- `profit`
- `delivery_time`
- `profit_margin`

Relationships:

- `orders.customer_id` references `customers.customer_id`
- `orders.product_id` references `products.product_id`

---

## ETL Pipeline Workflow

The pipeline follows this workflow:

```txt
CSV Source
   ↓
Extract raw data
   ↓
Load into staging.superstore_raw
   ↓
Audit and profile data
   ↓
Clean and transform data
   ↓
Pseudonymize personal data
   ↓
Create derived variables
   ↓
Load customers, products, and orders into core
   ↓
Run data quality checks
   ↓
Generate final statistics and report
```

---

## Airflow DAG

The ETL pipeline is orchestrated using Apache Airflow with the TaskFlow API.

Main DAG tasks:

1. `extract_data`
2. `load_to_staging`
3. `transform_data`
4. `load_customers`
5. `load_products`
6. `load_orders`
7. `validate_data_quality`
8. `generate_summary_report`

The DAG ensures that the pipeline can be executed automatically and reproduced safely.

---

## Idempotence Strategy

The pipeline is designed to be idempotent.

This means that running the pipeline multiple times should not create duplicate records or inconsistent results.

Idempotence is handled through:

- Stable primary keys
- Truncate/reload strategy for staging
- Upsert logic for core tables
- Duplicate checks before insertion
- Data quality validation after loading
- Clear separation between raw and transformed data

---

## GDPR Compliance

The dataset contains personal information through the `Customer Name` column.

To protect customer privacy, the project applies pseudonymization using SHA-256 hashing.

Example:

```python
import hashlib

def hash_customer_name(customer_name: str) -> str:
    return hashlib.sha256(customer_name.encode("utf-8")).hexdigest()
```

The raw customer name is allowed only in the staging layer because staging represents the original source data.

The core layer must never expose the customer name in clear text.

---

## Data Quality Rules

The pipeline checks and treats the following anomalies:

| Rule                        | Expected Treatment                              |
| --------------------------- | ----------------------------------------------- |
| Missing values              | Detect and clean depending on column importance |
| Duplicates                  | Remove duplicated records                       |
| Invalid date format         | Convert or reject invalid dates                 |
| Discount greater than 100%  | Mark as invalid and treat                       |
| Negative quantity           | Mark as invalid and treat                       |
| Ship date before order date | Mark as invalid and treat                       |
| Clear customer name in core | Not allowed                                     |
| Null primary key            | Not allowed                                     |
| Broken foreign key          | Not allowed                                     |

---

## Derived Business Variables

### `delivery_time`

Represents the number of days between the shipping date and the order date.

Formula:

```txt
delivery_time = ship_date - order_date
```

### `profit_margin`

Represents the profit ratio compared to sales.

Formula:

```txt
profit_margin = profit / sales
```

If sales equals zero, the value must be handled safely to avoid division errors.

---

## Final Statistics

The project provides the following final indicators:

- Total number of orders loaded into the database
- Total number of customers loaded into the database
- Total number of products loaded into the database
- Sales distribution by category
- Sales distribution by region
- Sales distribution by customer segment
- Number of missing values before and after cleaning
- Number of duplicates removed
- Number of invalid records detected
- Data completeness rate
- GDPR technique applied

---

## How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/datastore360-pipeline.git
cd datastore360-pipeline
```

### 2. Create Environment File

```powershell
Copy-Item .env.example .env
```

On Linux or macOS, use `cp .env.example .env`. Configure the PostgreSQL connection and pseudonymization salt before processing real data.

### 3. Install Python Dependencies

```bash
uv sync --all-groups
```

### 4. Start PostgreSQL, pgAdmin, and Airflow

The Docker Compose stack is intended for local development. Docker Desktop should have at least 4 GB of memory available (8 GB is preferable for Airflow).

```bash
docker compose up --build -d
docker compose ps
```

The first command builds the project-specific Airflow image, initializes PostgreSQL and the Airflow metadata schema, creates the Airflow administrator, and starts all services.

| Service | Address | Credentials |
| --- | --- | --- |
| PostgreSQL | `localhost:5432` | `datastore_user` / value of `POSTGRES_PASSWORD` |
| pgAdmin | http://localhost:5050 | Values of `PGADMIN_DEFAULT_EMAIL` and `PGADMIN_DEFAULT_PASSWORD` |
| Airflow | http://localhost:8080 | Values of `AIRFLOW_ADMIN_USERNAME` and `AIRFLOW_ADMIN_PASSWORD` |

pgAdmin includes a pre-registered server named **DataStore360 PostgreSQL**. When it requests the database password, enter the value of `POSTGRES_PASSWORD`. From one container to another, the PostgreSQL host is `postgres`, not `localhost`.

Airflow receives a connection named `datastore360_postgres` through its environment. DAG code can use it as `conn_id="datastore360_postgres"`, including with `PostgresHook`.

Useful commands:

```bash
# Follow service logs
docker compose logs -f

# Stop services while preserving database data
docker compose down

# Delete all local PostgreSQL, pgAdmin, and Airflow state and start fresh
docker compose down --volumes --remove-orphans
```

PostgreSQL executes the files in `sql/` only when its data volume is created for the first time. After changing initialization SQL, either apply it manually or recreate the volumes with the last command above. That command permanently removes the local container data.

### 5. Run the Airflow DAG

Open Airflow, unpause the DAG, and trigger:

```txt
datastore360_pipeline
```

---

## Data Profiling

The project uses `ydata-profiling` to generate an automated data quality report.

The report includes:

- Column types
- Missing values
- Unique values
- Duplicates
- Correlations
- Distributions
- Potential anomalies

Generated report path:

```txt
data/profiling/profiling_report.html
```

---

## Example SQL Quality Checks

Check if clear customer names exist in core:

```sql
SELECT customer_name
FROM core.customers
WHERE customer_name IS NULL
   OR LENGTH(customer_name) <> 64;
```

Check invalid discounts:

```sql
SELECT *
FROM core.orders
WHERE discount < 0 OR discount > 1;
```

Check negative quantities:

```sql
SELECT *
FROM core.orders
WHERE quantity < 0;
```

Check invalid delivery dates:

```sql
SELECT *
FROM core.orders
WHERE ship_date < order_date;
```

Check loaded record counts:

```sql
SELECT COUNT(*) AS total_customers FROM core.customers;
SELECT COUNT(*) AS total_products FROM core.products;
SELECT COUNT(*) AS total_orders FROM core.orders;
```

---

## Expected Deliverables

The final project deliverables are:

- Exploratory data analysis notebook
- Data profiling report
- Cleaned dataset
- PostgreSQL staging/core database
- SQL schema scripts
- Airflow DAG
- ETL source code
- Data quality validation queries
- Final project report
- GitHub README documentation

---

## Project Status

Current status:

```txt
Planning phase
```

---

## Author

Created as part of a Data Engineering learning project.

**Project:** DataStore360 Retail Data Pipeline
**Role:** Data Engineer

## Github workflow

```
main
│
└── develop
    │
    ├── feature/project-setup
    ├── feature/data-exploration
    ├── feature/data-cleaning
    ├── feature/postgres-modeling
    ├── feature/etl-pipeline
    ├── feature/airflow-orchestration
    └── feature/data-quality-reporting
```
