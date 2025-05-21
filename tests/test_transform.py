import pandas as pd
from utils.transform import DataTransformer, clean_and_merge

def test_transform_valid_data():
    sample_data = [{
        'title': 'Shirt',
        'price': 'Rp 150.000',
        'rating': 'Rating: 4.5',
        'colors': 'Colors: Red',
        'size': 'Size: M',
        'gender': 'Gender: Male'
    }]
    transformer = DataTransformer(sample_data)
    df = transformer.transform()
    assert not df.empty
    assert 'price' in df.columns
    assert df['price'].dtype == 'float64'
    assert df['rating'].dtype == 'float64'

def test_clean_and_merge():
    df1 = pd.DataFrame({"id": [1], "price": ["1,000"]})
    df2 = pd.DataFrame({"id": [1], "price": ["1,000"]})
    result = clean_and_merge(df1, df2)
    assert result.shape[0] == 1
    assert result["price"].iloc[0] == 1000.0