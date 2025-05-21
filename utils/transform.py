# src/transform.py

import pandas as pd
import numpy as np
from datetime import datetime

# bagian ini digunakan untuk mendefinisikan beberapa variabel yang digunakan dalam transformasi data
# Variabel ini digunakan untuk menyimpan ukuran dan jenis kelamin yang valid
# yang akan digunakan dalam proses transformasi data
VALID_SIZES = {'S', 'M', 'L', 'XL', 'XXL'}
VALID_GENDERS = {'men', 'woman', 'unisex'}

# Fungsi ini digunakan untuk membersihkan dan memproses data produk
class DataTransformer:
    def __init__(self, products):
        self.products = products

    def transform(self):
        df = pd.DataFrame(self.products)

        # Filter invalid title
        df = df[df['title'].str.lower() != 'unknown product']
        df['title'] = df['title'].astype('object')

        # Clean price dan konversi ke float
        df['price'] = df['price'].replace(r'[^\d.]', '', regex=True)
        df['price'] = pd.to_numeric(df['price'], errors='coerce') * 16000
        df['price'] = df['price'].astype('float64')
        df.dropna(subset=['price'], inplace=True)

        # Clean rating
        df['rating'] = df['rating'].replace(r'[^\d.]', '', regex=True)
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce').astype('float64')
        df.dropna(subset=['rating', 'colors'], inplace=True)

        # Normalisasi color
        df['colors'] = df['colors'].str.extract(r'(\d+)').astype('Int64')

        # Normalisasi size
        df['size'] = df['size'].str.replace('Size: ', '', regex=False).str.upper()
        df = df[df['size'].isin(VALID_SIZES)]
        df['size'] = df['size'].astype('object')

        # Normalisasi gender
        df['gender'] = df['gender'].str.replace('Gender: ', '', regex=False).str.lower()
        df['gender'] = df['gender'].where(df['gender'].isin(VALID_GENDERS))
        df.dropna(subset=['gender'], inplace=True)
        df['gender'] = df['gender'].astype('object')

        # tambahan untuk timestamp
        df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Remove duplikat data
        df.drop_duplicates(inplace=True)

        return df

# Fungsi untuk membersihkan dan menggabungkan dua DataFrame
def clean_and_merge(df1, df2):
    for df in [df1, df2]:
        df['price'] = df['price'].replace(r'[^\d.]', '', regex=True)
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
    merged = pd.concat([df1, df2], ignore_index=True).drop_duplicates()
    return merged
