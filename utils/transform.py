import pandas as pd
import numpy as np
from datetime import datetime

# modul ini digunakan untuk membersihkan dan mengubah data produk
# dari website fashion-studio.dicoding.dev
class DataTransformer:
    def __init__(self, products):
        self.products = products

    # Fungsi ini digunakan untuk membersihkan dan mengubah data produk
    # dari website fashion-studio.dicoding.dev
    # Fungsi ini akan menghapus produk yang tidak valid, mengubah harga
    # dan rating menjadi tipe data numerik, serta menambahkan timestamp
    # ke dalam dataframe
    def transform(self):
        df = pd.DataFrame(self.products)

        #  bagian ini digunakan untuk membersihkan data produk
        df = df[df['title'].str.lower() != 'unknown product']
        df['price'] = df['price'].replace(r'[^\d.]', '', regex=True)
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df.dropna(subset=['price'], inplace=True)

        # bagian ini digunakan untuk mengubah harga menjadi tipe data numerik
        if not df['price'].empty:
            df['price'] = df['price'] * 16410 # Kurs idr usd Sekarang 16410 per dolar

        # bagian ini digunakan untuk membersihkan data produk
        df['rating'] = df['rating'].replace(r'[^0-9.]', '', regex=True)
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

        df.dropna(subset=['rating', 'colors'], inplace=True)
        df.drop_duplicates(inplace=True)

        df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return df
