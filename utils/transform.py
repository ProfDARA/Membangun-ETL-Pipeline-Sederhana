import pandas as pd
import re

def clean_and_merge(csv_df: pd.DataFrame, sheet_df: pd.DataFrame) -> pd.DataFrame:
    combined_df = pd.concat([csv_df, sheet_df], ignore_index=True)
    return clean_data(combined_df)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    df = df[~df['Title'].str.contains("Unknown Product", na=False)]

    df['Price'] = df['Price'].replace(r'\$|,', '', regex=True).astype(float) * 16000
    df['Rating'] = df['Rating'].replace(r'[^0-9\.]', '', regex=True).astype(float)
    df['Colors'] = df['Colors'].replace(r'[^0-9]', '', regex=True).astype(int)
    df['Size'] = df['Size'].str.replace("Size: ", "", regex=False)
    df['Gender'] = df['Gender'].str.replace("Gender: ", "", regex=False)

    return df