import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def extract_from_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def extract_from_google_sheets(json_credential_path: str, sheet_name: str, worksheet_index: int = 0) -> pd.DataFrame:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_credential_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name)
    worksheet = sheet.get_worksheet(worksheet_index)
    data = worksheet.get_all_records()
    return pd.DataFrame(data)