import os
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

def merge_to_snowflake():
    # 1. Snowflake database login 
    conn = snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse='COMPUTE_WH',
        database='CDC_DB',
        schema='USERS_SCHEMA'
    )
    cursor = conn.cursor()

    # 2. Temporary Table create 
    cursor.execute("""
        CREATE OR REPLACE TEMPORARY TABLE temp_crypto_data 
        LIKE crypto_market_data;
    """)

    # 3. S3 Stage to  Parquet file  Temp Table  COPY 
    cursor.execute("""
        COPY INTO temp_crypto_data
        FROM @cdc_s3_stage/cdc_data/crypto_market.parquet
        FILE_FORMAT = (TYPE = PARQUET)
        MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
    """)

    # 4. Temp Table  Main Table  MERGE (Upsert) 
    cursor.execute("""
        MERGE INTO crypto_market_data AS target
        USING temp_crypto_data AS source
        ON target.coin_id = source.coin_id
        WHEN MATCHED THEN 
            UPDATE SET 
                target.symbol = source.symbol,
                target.coin_name = source.coin_name,
                target.current_price = source.current_price,
                target.market_cap = source.market_cap,
                target.last_updated = source.last_updated
        WHEN NOT MATCHED THEN 
            INSERT (coin_id, symbol, coin_name, current_price, market_cap, last_updated)
            VALUES (source.coin_id, source.symbol, source.coin_name, source.current_price, source.market_cap, source.last_updated);
    """)

    print("Success: Data merged into Snowflake table!")

    # 5. Changes save  connection close 
    conn.commit()
    cursor.close()
    conn.close()
    return True
