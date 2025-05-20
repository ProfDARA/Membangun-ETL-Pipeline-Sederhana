import pandas as pd
import numpy as np
from datetime import datetime

class DataTransformer:
    """Kelas untuk melakukan transformasi data."""

    def __init__(self, products):
        """Inisialisasi dengan data produk yang akan diproses."""
        self.products = products

    def transform(self):
        """Melakukan transformasi pada data produk."""
        df = pd.DataFrame(self.products)

        print("Data awal:")
        print(df)
        
        # Menghapus produk yang title-nya 'unknown product'
        df = df[df['title'].str.lower() != 'unknown product']

        print("\nSetelah menghapus produk 'unknown product':")
        print(df)

        # Menghapus simbol 'Rp' dan titik pada harga, kemudian konversi menjadi float
        df['price'] = df['price'].replace(r'[^\d.]', '', regex=True)
        print("\nSetelah membersihkan simbol dari harga:")
        print(df['price'])

        # Konversi harga menjadi float
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        print("\nSetelah mengonversi harga menjadi angka:")
        print(df['price'])

        # Menghapus baris dengan harga yang NaN
        df.dropna(subset=['price'], inplace=True)
        print("\nSetelah menghapus baris dengan harga NaN:")
        print(df)

        if not df['price'].empty:
            df['price'] = df['price'] * 16000  # Mengonversi harga menjadi Rupiah

        print("\nSetelah mengonversi harga menjadi Rupiah:")
        print(df['price'])

        # Konversi rating menjadi float
        df['rating'] = df['rating'].replace(r'[^0-9.]', '', regex=True)
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        print("\nSetelah mengonversi rating menjadi angka:")
        print(df['rating'])

        # Bersihkan colors (biarkan saja atau hilangkan regex non-digit)
        # Jika ingin menjaga warna tetap sebagai teks, cukup hapus pembersihan berikut:
        # df['colors'] = df['colors'].replace(r'\D', '', regex=True)
        # df['colors'] = pd.to_numeric(df['colors'], errors='coerce')
        print("\nSetelah membersihkan kolom colors (tetap dalam bentuk teks):")
        print(df['colors'])

        # Drop NaN dari kolom penting dan baris duplikat
        df.dropna(subset=['rating', 'colors'], inplace=True)
        df.drop_duplicates(inplace=True)

        print("\nSetelah drop NaN dan duplikat:")
        print(df)

        # Tambahkan kolom timestamp
        df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print("\nData akhir setelah transformasi:")
        print(df)

        return df