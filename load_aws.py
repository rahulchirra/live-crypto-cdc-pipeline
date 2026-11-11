import os 
import boto3
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

def upload_to_s3(df):
    parquet_buffer = BytesIO()
    df.to_parquet(parquet_buffer , index=False)

    s3_client=boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key =os.getenv('AWS_SECRET_KEY')
    )

    s3_client.put_object(
        Bucket=os.getenv('BUCKET'),
        Key ='cdc_data/crypto_market.parquet',
        Body=parquet_buffer.getvalue()
    )

    print('successfully stored data in s3 ')
    return True