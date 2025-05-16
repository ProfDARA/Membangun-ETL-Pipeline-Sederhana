from utils.extract import scrape_main
from utils.transform import clean_data
from utils.load import load_to_csv, load_to_google_sheets

OUTPUT_PATH = "output.csv"
GOOGLE_CRED_PATH = "simpancloud-074f2cfa2617.json"
GOOGLE_SHEET_NAME = "FashionData"

def main():
    raw_data = scrape_main()
    transformed_data = clean_data(raw_data)
    load_to_csv(transformed_data, OUTPUT_PATH)
    load_to_google_sheets(transformed_data, GOOGLE_CRED_PATH, GOOGLE_SHEET_NAME)

if __name__ == "__main__":
    main()