-- order indexes
CREATE INDEX IF NOT EXISTS idx_orders_order_id
ON core.orders (order_id);
CREATE INDEX IF NOT EXISTS idx_orders_customer_id
ON core.orders (customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_product_id
ON core.orders (product_id);
CREATE INDEX IF NOT EXISTS idx_orders_order_date
ON core.orders (order_date); 

-- product indexes
CREATE INDEX IF NOT EXISTS idx_category
ON core.product (category)
CREATE INDEX IF NOT EXISTS idx_sub_category 
ON core.product (sub_category)

-- custommer indexes
CREATE INDEX IF NOT EXISTS idx_segment
ON core.custommer (segment)
CREATE INDEX IF NOT EXISTS idx_country 
ON core.custommer (country)

