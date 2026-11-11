import warnings
from extract import extract_data
from transform import clean_crypto_data
from load_aws import upload_to_s3
from load_snowflake import merge_to_snowflake

warnings.filterwarnings("ignore")

def run_pipeline():
    print("--- STARTING LIVE CRYPTO CDC PIPELINE ---")
    
    # Step 1:
    raw_data = extract_data()
    print("Step 1 Done: Extracted 50 live coins from API.")
    
    # Step 2: 
    clean_df = clean_crypto_data(raw_data)
    print("Step 2 Done: Data cleaned and formatted in Pandas.")
    
    # Step 3: 
    upload_to_s3(clean_df)
    print("Step 3 Done: Uploaded Parquet file to AWS S3.")
    
    # Step 4: 
    merge_to_snowflake()
    print("Step 4 Done: Merged latest prices into Snowflake!")
    
    print("--- PIPELINE COMPLETED SUCCESSFULLY ---")

# Pipeline
run_pipeline()
