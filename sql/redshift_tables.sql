-- Redshift table schema for analytics
-- This table stores cleaned order data loaded from S3

CREATE TABLE IF NOT EXISTS orders (
    order_id        VARCHAR(50),
    order_date      DATE,
	customer_id		VARCHAR(5),
	product			VARCHAR(10),
    quantity        INTEGER,
    price           DECIMAL(10,2),
    total_amount    DECIMAL(12,2)
);



-- Command to LOAD data into Redshift table (orders) from cleaned CSV in S3
-- Executed via Redshift Query Editor or orchestration tool (e.g., Airflow)

-- COPY orders
-- FROM 's3://etl-practice-milja/processed/processed_orders.csv'
-- IAM_ROLE 'arn:aws:iam::<account-id>:role/<redshift-role>'
-- CSV
-- IGNOREHEADER 1;