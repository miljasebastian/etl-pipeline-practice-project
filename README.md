# ETL Pipeline Practice Project

## Project Overview

This project demonstrates an end-to-end **ETL pipeline** using **Python**, **AWS S3**, **Lambda**, and **Amazon Redshift**.  
The pipeline simulates real-world workflows: ingesting raw data, transforming it, and loading it into a data warehouse for analytics.

---

## Architecture
S3 raw/ → Lambda (transform) → S3 processed/ → Redshift (orders table)

### Components

1. **S3 (Data Lake)**
   - `raw/` layer stores unprocessed CSV files
   - `processed/` layer stores cleaned and transformed CSV files
   - Enables reproducibility and versioning of raw data

2. **AWS Lambda (Transformation)**
   - Triggered automatically when a file is uploaded to `raw/`
   - Reads raw CSV using `boto3`
   - Cleans and transforms data:
     - Fills missing numeric values with defaults (`0` or `0.0`)
     - Normalizes dates to a uniform format
     - Computes `total_amount = quantity * price`
   - Writes cleaned data to `processed/`

3. **Amazon Redshift (Data Warehouse)**
   - Stores transformed order data for analytics
   - Table schema:
        ```sql
        CREATE TABLE IF NOT EXISTS orders (
            order_id        VARCHAR(50),
            order_date      DATE,
            quantity        INTEGER,
            price           DECIMAL(10,2),
            total_amount    DECIMAL(12,2)
        );
        -- Data is loaded from S3 using Redshift COPY command:
        COPY orders
        FROM 's3://<bucket-name>/processed/processed_orders.csv'
        IAM_ROLE 'arn:aws:iam::<AWS_ACCOUNT_ID>:role/<redshift-s3-access-role>'
        CSV
        IGNOREHEADER 1;
        ```

## Project Highlights
- Event-driven ETL using AWS Lambda
- Data cleaning, type conversion, and derived column computation
- Proper S3 data lake structure (raw/ vs processed/)
- Redshift table design and COPY data loading
- Demonstrates cloud ETL practices suitable for analytics pipelines

## Repository Structure
etl-pipeline-practice-project/
├── data/
│   └── raw_orders.csv         # Sample raw dataset
├── lambda/
│   └── transform.py           # ETL transformation logic
├── sql/
│   └── redshift_tables.sql    # Table schema and COPY command for Redshift
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
