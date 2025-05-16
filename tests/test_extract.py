import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_main(base_url: str = "https://fashion-studio.dicoding.dev/", pages: int = 50) -> pd.DataFrame:
    all_data = []
    for page in range(1, pages + 1):
        try:
            response = requests.get(f"{base_url}?page={page}", timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            product_cards = soup.select(".product-card")
            for card in product_cards:
                try:
                    title = card.select_one(".product-title").get_text(strip=True)
                    price = card.select_one(".product-price").get_text(strip=True)
                    rating = card.select_one(".product-rating").get_text(strip=True)
                    colors = card.select_one(".product-colors").get_text(strip=True)
                    size = card.select_one(".product-size").get_text(strip=True)
                    gender = card.select_one(".product-gender").get_text(strip=True)
                    timestamp = datetime.now().isoformat()

                    all_data.append({
                        "Title": title,
                        "Price": price,
                        "Rating": rating,
                        "Colors": colors,
                        "Size": size,
                        "Gender": gender,
                        "Timestamp": timestamp
                    })
                except Exception as e:
                    print(f"Error parsing product card: {e}")
        except Exception as e:
            print(f"Failed to retrieve page {page}: {e}")
    return pd.DataFrame(all_data)