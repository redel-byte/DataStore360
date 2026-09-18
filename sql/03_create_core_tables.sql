CEATE TABLE IF NOT EXISTS core.customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(64) NOT NULL,
    segment VARCHAR(50),
    country VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    region VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS core.products (
    product_id VARCHAR(50) PRIMARY KEY,
    category VARCHAR(100),
    sub_category VARCHAR(100),
    product_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS core.orders (
    row_id INTEGER PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,

    customer_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,

    order_date DATE NOT NULL,
    ship_date DATE,
    ship_mode VARCHAR(50),

    sales NUMERIC(12, 2),
    quantity INTEGER,
    discount NUMERIC(5, 2),
    profit NUMERIC(12, 2),

    delivery_time INTEGER,
    profit_margin NUMERIC(10, 4),

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES core.customers(customer_id),

    CONSTRAINT fk_orders_product
        FOREIGN KEY (product_id)
        REFERENCES core.products(product_id)
);
