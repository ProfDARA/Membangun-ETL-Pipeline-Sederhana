import pandas as pd
from utils.transform import clean_and_merge

def test_clean_and_merge():
    df1 = pd.DataFrame({"id": [1], "price": ["1,000"]})
    df2 = pd.DataFrame({"id": [1], "price": ["1,000"]})
    result = clean_and_merge(df1, df2)
    assert result.shape[0] == 1
    assert result["price"].iloc[0] == 1000.0