import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def load_to_csv(df: pd.DataFrame, output_path: str) -> None:
    try:
        df.to_csv(output_path, index=False)
    except Exception as e:
        print(f"Failed to save CSV: {e}")

def load_to_google_sheets(df: pd.DataFrame, json_credential_path: str, sheet_name: str):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_credential_path, scope)
        client = gspread.authorize(creds)
        sheet = client.open(sheet_name)
        worksheet = sheet.sheet1
        worksheet.clear()
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    except Exception as e:
        print(f"Failed to load to Google Sheets: {e}")
