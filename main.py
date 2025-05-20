from colorama import init, Fore, Style
from utils.extract import scrape_main
from utils.transform import DataTransformer
from utils.load import DataSaver

init(autoreset=True)

class Scraper:
    def __init__(self, base_url, pages=50):
        self.base_url = base_url
        self.pages = pages
        self.all_products = []

    def scrape_page(self, url, page_number=None):
        label = f"Halaman {page_number}" if page_number else "Halaman Utama"
        print(f"{Fore.GREEN}{Style.BRIGHT}🔎  {label:<10}: Scraping {url}{Style.RESET_ALL}")
        try:
            products = scrape_main(url)
            self.all_products.extend(products)
        except Exception as e:
            print(f"{Fore.RED}{Style.BRIGHT}❌  Gagal scraping {url}: {e}{Style.RESET_ALL}")

    def scrape_all(self):
        self.scrape_page(self.base_url, page_number=1)
        for page in range(2, self.pages + 1):
            url = f"{self.base_url}page{page}"
            self.scrape_page(url, page)
        return self.all_products


class DataProcessor:
    def __init__(self, products):
        self.transformer = DataTransformer(products)

    def process(self):
        return self.transformer.transform()


def main():
    base_url = 'https://fashion-studio.dicoding.dev/'

    scraper = Scraper(base_url)
    all_products = scraper.scrape_all()

    if all_products:
        processor = DataProcessor(all_products)
        transformed_data = processor.process()

        saver = DataSaver(transformed_data)
        saver.save_all()
    else:
        print(f"{Fore.YELLOW}{Style.BRIGHT}⚠️  Tidak ada produk yang ditemukan.{Style.RESET_ALL}")


if __name__ == '__main__':
    main()