import pandas as pd
from utils.load import DataSaver
from unittest.mock import patch, MagicMock

# bagian ini digunakan untuk menguji fungsi penyimpanan data ke dalam file csv, google sheets, dan postgresql
@patch("utils.load.create_engine")
def test_save_to_postgresql(mock_engine):
    df = pd.DataFrame({"title": ["Test"], "price": [1000], "rating": [4.5], "colors": ["Red"]})
    saver = DataSaver(df)
    saver.save_to_postgresql(table_name="test_table")
    mock_engine.assert_called()

# fungsi ini digunakan untuk menguji fungsi penyimpanan data ke dalam google sheets
@patch("utils.load.Credentials.from_service_account_file")
@patch("utils.load.build")
def test_save_to_google_sheets(mock_build, mock_credentials):
    df = pd.DataFrame({"title": ["Test"], "price": [1000], "rating": [4.5], "colors": ["Red"]})
    saver = DataSaver(df)
    mock_service = MagicMock()
    mock_build.return_value.spreadsheets.return_value = mock_service
    saver.save_to_google_sheets("fake_id", "Sheet1!A1")
    mock_service.values().update.assert_called()

# fungsi ini digunakan untuk menguji fungsi penyimpanan data ke dalam file csv
def test_save_to_csv(tmp_path):
    df = pd.DataFrame({"title": ["Test"], "price": [1000], "rating": [4.5], "colors": ["Red"]})
    saver = DataSaver(df)
    file_path = tmp_path / "test_products.csv"
    saver.save_to_csv(filename=str(file_path))
    saved_df = pd.read_csv(file_path)
    assert not saved_df.empty