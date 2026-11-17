# Automated Cryptocurrency CDC Data Pipeline

An automated ETL pipeline that extracts live cryptocurrency market data, stores it in AWS S3 as Parquet, and performs Change Data Capture (CDC / Upsert) in Snowflake.

### Architecture Flow
`CoinGecko REST API` -> `Python (In-Memory Parquet)` -> `AWS S3` -> `Snowflake (COPY INTO & MERGE INTO)`

### Tech Stack
* **Python:** `requests`, `pandas`, `io.BytesIO`, `boto3`, `python-dotenv`
* **Cloud & Warehouse:** AWS S3, Snowflake SQL

### Project Files
* `extract.py` - Fetches top 50 live cryptocurrency records from CoinGecko API.
* `transform.py` - Filters key financial columns and formats timestamps.
* `load_aws.py` - Converts data into Apache Parquet in RAM and uploads to AWS S3.
* `load_snowflake.py` - Loads data into staging using `COPY INTO` and performs atomic Upsert (`MERGE INTO`) on `coin_id` to prevent duplicate data.
* `main.py` - Orchestrates the complete pipeline execution.
