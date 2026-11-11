import warnings
from extract import extract_data
from transform import clean_crypto_data
from load_aws import upload_to_s3
from load_snowflake import merge_to_snowflake

# Snowflake iche FutureWarnings ni silent cheyadaniki
warnings.filterwarnings("ignore")

def run_pipeline():
    print("--- STARTING LIVE CRYPTO CDC PIPELINE ---")
    
    # Step 1: CoinGecko API nunchi live data theeskura
    raw_data = extract_data()
    print("Step 1 Done: Extracted 50 live coins from API.")
    
    # Step 2: Pandas tho data clean cheyi
    clean_df = clean_crypto_data(raw_data)
    print("Step 2 Done: Data cleaned and formatted in Pandas.")
    
    # Step 3: AWS S3 loki Parquet file upload cheyi
    upload_to_s3(clean_df)
    print("Step 3 Done: Uploaded Parquet file to AWS S3.")
    
    # Step 4: Snowflake loki MERGE (Upsert) cheyi
    merge_to_snowflake()
    print("Step 4 Done: Merged latest prices into Snowflake!")
    
    print("--- PIPELINE COMPLETED SUCCESSFULLY ---")

# Pipeline ni trigger cheyadam
run_pipeline()