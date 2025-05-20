import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine

class DataSaver:
    """Kelas untuk menangani penyimpanan data ke berbagai tempat."""

    def __init__(self, data):
        """Inisialisasi dengan data yang telah diproses."""
        self.data = data

    def save_to_csv(self, filename="products.csv"):
        """Simpan data ke CSV."""
        if self.data.empty:
            print("Dataframe kosong, tidak ada data yang disimpan.")
            return
        self.data.to_csv(filename, index=False)
        print(f"Data berhasil disimpan ke {filename}.")

    def save_to_google_sheets(self, spreadsheet_id, range_name):
        """Simpan data ke Google Sheets."""
        if self.data.empty:
            print("Dataframe kosong, tidak ada data yang disimpan ke Google Sheets.")
            return
        
        creds = Credentials.from_service_account_file('google-sheets-api.json')
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        values = self.data.values.tolist()
        body = {
            'values': values
        }
        
        try:
            sheet.values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            print(f"Data berhasil disimpan ke Google Sheets dengan ID {spreadsheet_id}.")
        except Exception as e:
            print(f"Gagal menyimpan ke Google Sheets: {e}")

    def save_to_postgresql(self, table_name='products'):
        """Simpan data ke PostgreSQL."""
        if self.data.empty:
            print("Dataframe kosong, tidak ada data yang disimpan ke PostgreSQL.")
            return
        
        try:
            username = 'postgres'
            password = '12345678'
            host = 'localhost'
            port = '5432'
            database = 'etl_db'

            engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')
            self.data.to_sql(table_name, engine, if_exists='replace', index=False)
            print(f"Data berhasil disimpan ke PostgreSQL table '{table_name}'.")
        except Exception as e:
            print(f"Gagal menyimpan ke PostgreSQL: {e}")

    def save_all(self):
        """Menyimpan data ke CSV, PostgreSQL, dan Google Sheets."""
        self.save_to_csv()
        self.save_to_postgresql()
        self.save_to_google_sheets(
            '1dNIljp-oy8RAklZUykFTaomnIA7b-mhXAGS3ul_Zg6A',
            'Sheet1!A2'
        )