import pandas as pd
import numpy as np
from datetime import datetime

# bagian ini digunakan untuk mengubah data yang sudah diambil dari website fashion-studio.dicoding.dev
class DataTransformer:
    def __init__(self, products):
        self.products = products

    # fungsi ini digunakan untuk membersihkan dan mengubah data
    def transform(self):
        df = pd.DataFrame(self.products)
        
        # mengubah kolom 'price' menjadi float
        df = df[df['title'].str.lower() != 'unknown product']
        df['price'] = df['price'].replace(r'[^\d.]', '', regex=True)
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df.dropna(subset=['price'], inplace=True)

        if not df['price'].empty:
            df['price'] = df['price'] * 16000  # Kurs IDR/USD sekarang

        # mengubah kolom rating menjadi float
        df['rating'] = df['rating'].replace(r'[^0-9.]', '', regex=True)
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

        # mengubah kolom colors menjadi string
        df.dropna(subset=['rating', 'colors'], inplace=True)
        df.drop_duplicates(inplace=True)

        # filter size agar hanya 'S', 'M', 'L', 'XL', 'XXL'
        df['size'] = df['size'].str.replace('Size: ', '', regex=False).astype(str)


        # Filter gender agar hanya 'men' dan 'woman'
        df['gender'] = df['gender'].str.replace('Gender: ', '', regex=False).str.lower()
        df['gender'] = df['gender'].map(lambda x: 'men' if x == 'men' else 'woman' if x == 'woman' else 'unisex' if x == 'unisex' else np.nan)
        df.dropna(subset=['gender'], inplace=True)

        # mengubah kolom timestamp menjadi datetime
        df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return df

# fungsi ini digunakan untuk membersihkan dan menggabungkan dua dataframe
def clean_and_merge(df1, df2):
    df1['price'] = df1['price'].replace(r'[^\d.]', '', regex=True).astype(float)
    df2['price'] = df2['price'].replace(r'[^\d.]', '', regex=True).astype(float)
    merged = pd.concat([df1, df2]).drop_duplicates()
    return merged