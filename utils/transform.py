# transform.py
import pandas as pd
import numpy as np
from datetime import datetime

class DataTransformer:
    def __init__(self, products):
        self.products = products

    def transform(self):
        df = pd.DataFrame(self.products)

        df = df[df['title'].str.lower() != 'unknown product']
        df['price'] = df['price'].replace(r'[^\d.]', '', regex=True)
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df.dropna(subset=['price'], inplace=True)

        if not df['price'].empty:
            df['price'] = df['price'] * 16410  # Kurs IDR/USD sekarang

        df['rating'] = df['rating'].replace(r'[^0-9.]', '', regex=True)
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

        df.dropna(subset=['rating', 'colors'], inplace=True)
        df.drop_duplicates(inplace=True)

        df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return df


def clean_and_merge(df1, df2):
    df1['price'] = df1['price'].replace(r'[^\d.]', '', regex=True).astype(float)
    df2['price'] = df2['price'].replace(r'[^\d.]', '', regex=True).astype(float)
    merged = pd.concat([df1, df2]).drop_duplicates()
    return merged