import requests
from bs4 import BeautifulSoup

# fungsi ini digunakan untuk mengambil data dari website fashion-studio.dicoding.dev
def scrape_main(url):

    # bagian ini digunakan untuk mengakses URL dan menangani kesalahan
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Gagal mengakses URL: {url}. Detail: {e}")

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []

        # bagian ini digunakan untuk mencari elemen-elemen yang ada di dalam halaman
        element_selectors = {
            'title': {'tag': 'h3', 'class': 'product-title', 'default': 'Unknown Title'},
            'price': {'tag': 'div', 'class': 'price-container', 'default': 'Price Unavailable'},
            'rating': {'tag': 'p', 'string_contains': 'Rating', 'default': 'No Rating'},
            'colors': {'tag': 'p', 'string_contains': 'Colors', 'default': 'No Color Info'},
            'size': {'tag': 'p', 'string_contains': 'Size', 'default': 'No Size Info'},
            'gender': {'tag': 'p', 'string_contains': 'Gender', 'default': 'No Gender Info'}
        }

        # bagian ini digunakan untuk mencari elemen-elemen yang ada di dalam halaman
        for card in soup.find_all('div', class_='collection-card'):
            product_data = {}

            for key, selector in element_selectors.items():
                element = None
                if 'class' in selector:
                    element = card.find(selector['tag'], class_=selector['class'])
                elif 'string_contains' in selector:
                    element = card.find(selector['tag'], string=lambda text: text and selector['string_contains'] in text)
                product_data[key] = element.get_text(strip=True) if element else selector['default']

            products.append(product_data)

        if not products:
            raise Exception("Tidak ada produk yang ditemukan pada halaman ini.")

        return products

    # bagian ini digunakan untuk menangani kesalahan saat parsing HTML
    except Exception as e:
        raise Exception(f"Gagal melakukan parsing HTML. Detail: {e}")


