import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine

# bagian ini digunakan untuk menyimpan data yang sudah diproses ke dalam file csv, google sheets, dan postgresql
class DataSaver:
    def __init__(self, data):
        self.data = data

    # fungsi ini digunakan untuk menyimpan data ke dalam file csv
    def save_to_csv(self, filename="products.csv"):
        if self.data.empty:
            print("Dataframe kosong, tidak ada data yang disimpan.")
            return
        self.data.to_csv(filename, index=False)
        print(f"Data berhasil disimpan ke {filename}.")

    # fungsi ini digunakan untuk menyimpan data ke dalam google sheets
    def save_to_google_sheets(self, spreadsheet_id, range_name):
        if self.data.empty:
            print("Dataframe kosong, tidak ada data yang disimpan ke Google Sheets.")
            return

        creds = Credentials.from_service_account_file('google-sheets-api.json')
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        values = [self.data.columns.tolist()] + self.data.values.tolist()
        body = {'values': values}

        # Menggunakan try-except untuk menangani kesalahan saat menyimpan ke Google Sheets
        try:
            sheet.values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            print(f"Data berhasil disimpan di Google Sheets ID: {spreadsheet_id}.")
        except Exception as e:
            print(f"Gagal menyimpan ke Google Sheets: {e}")

    # fungsi ini digunakan untuk menyimpan data ke dalam postgresql
    def save_to_postgresql(self, table_name='products'):
        if self.data.empty:
            print("Dataframe kosong, tidak ada data yang disimpan ke PostgreSQL.")
            return
        
        # Menggunakan try-except untuk menangani kesalahan saat menyimpan ke PostgreSQL
        # bagian konfigurasi untuk menghubungkan ke database PostgreSQL sesuai server yang digunakan
        try:
            username = 'postgres'
            password = '12345678'
            host = 'localhost'
            port = '5433'
            database = 'etl'

            engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')
            self.data.to_sql(table_name, engine, if_exists='replace', index=False)
            print(f"Data berhasil disimpan ke PostgreSQL table '{table_name}'.")
        except Exception as e:
            print(f"Gagal menyimpan ke PostgreSQL: {e}")

    # fungsi ini digunakan untuk menyimpan data ke dalam semua tempat
    def save_all(self):
        self.save_to_csv()
        self.save_to_postgresql()
        self.save_to_google_sheets(
            '1qGvCVX2L7hl-dBdLgM0EEXYlimIfDcbowS7LFFUA0Fw',
            'Sheet1!A1'
        )