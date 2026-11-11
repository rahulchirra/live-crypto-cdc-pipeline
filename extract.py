import requests
import pandas as pd

def extract_data():
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&per_page=50'
    response=requests.get(url)
    data = response.json()

    return data 
