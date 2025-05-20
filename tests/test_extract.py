import pytest
from utils.extract import scrape_main

@pytest.mark.parametrize("url", [
    "https://fashion-studio.dicoding.dev/",
])
def test_scrape_main_success(url):
    products = scrape_main(url)
    assert isinstance(products, list)
    assert len(products) > 0
    for p in products:
        assert 'title' in p
        assert 'price' in p
        assert 'rating' in p
        assert 'colors' in p
        assert 'size' in p
        assert 'gender' in p
