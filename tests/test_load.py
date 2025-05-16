import pandas as pd
import os
from utils.load import load_to_csv

def test_load_to_csv(tmp_path):
    df = pd.DataFrame({"id": [1], "price": [1000.0]})
    output_file = tmp_path / "test_output.csv"
    load_to_csv(df, output_file)
    assert os.path.exists(output_file)
    loaded = pd.read_csv(output_file)
    assert loaded.equals(df)