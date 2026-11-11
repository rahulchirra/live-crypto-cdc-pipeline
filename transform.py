import pandas as pd
from extract import extract_data

def clean_crypto_data(raw_data):
    df =pd.DataFrame(raw_data)

    columns =['id', 'symbol', 'name', 'current_price', 'market_cap', 'last_updated']
    df=df[columns]

    df=df.rename(columns={'id':'coin_id','name':'coin_name'})

    df=df.dropna()

    return df 
