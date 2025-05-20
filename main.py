from colorama import init, Fore, Back, Style
from utils.extract import scrape_main
from utils.transform import DataTransformer
from utils.load import DataSaver

# Inisialisasi colorama untuk kompatibilitas Windows
init(autoreset=True)

class Scraper:
    """Kelas untuk menangani proses scraping dan pengolahan data."""

    def __init__(self, base_url, pages=50):
        """Inisialisasi dengan URL dasar dan jumlah halaman yang akan di-scrape."""
        self.base_url = base_url
        self.pages = pages
        self.all_products = []

    def scrape_page(self, url, page_number=None):
        """Mencoba untuk meng-scrape halaman dan menambahkan hasilnya ke all_products."""
        label = f"Halaman {page_number}" if page_number else "Halaman Utama"
        print(f"{Fore.GREEN}{Style.BRIGHT}🔎  {label:<10}: Scraping {url}{Style.RESET_ALL}")
        try:
            products = scrape_main(url)
            self.all_products.extend(products)
        except Exception as e:
            print(f"{Fore.RED}{Style.BRIGHT}❌  Gagal scraping {url}: {e}{Style.RESET_ALL}")

    def scrape_all(self):
        """Scrape halaman utama dan halaman lainnya dari 2 hingga halaman ke-N."""
        # Halaman utama
        self.scrape_page(self.base_url, page_number=1)

        # Halaman 2 sampai N
        for page in range(2, self.pages + 1):
            url = f"{self.base_url}page{page}"
            self.scrape_page(url, page)

        return self.all_products


class DataProcessor:
    """Kelas untuk menangani proses transformasi data."""

    def __init__(self, products):
        """Inisialisasi dengan data produk yang akan diproses."""
        self.transformer = DataTransformer(products)

    def process(self):
        """Melakukan transformasi pada data produk."""
        return self.transformer.transform()


def main():
    base_url = 'https://fashion-studio.dicoding.dev/'

    # Scraping data produk
    scraper = Scraper(base_url)
    all_products = scraper.scrape_all()

    if all_products:
        # Proses transformasi data
        processor = DataProcessor(all_products)
        transformed_data = processor.process()

        # Simpan data ke berbagai tempat
        saver = DataSaver(transformed_data)
        saver.save_all()
    else:
        print(f"{Fore.YELLOW}{Style.BRIGHT}⚠️  Tidak ada produk yang ditemukan.{Style.RESET_ALL}")


if __name__ == '__main__':
    main()