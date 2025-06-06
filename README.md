# ETL Pipeline - simpancloud

## Deskripsi  
Pipeline ETL ini terdiri dari tiga tahapan utama: **Extract**, **Transform**, dan **Load**.  
Setiap tahapan dikelola dalam file Python terpisah untuk memudahkan modularitas dan unit testing.  
File utama (`main.py`) akan mengorkestrasi keseluruhan proses ETL.

## Struktur Proyek  
📂 etl_pipeline
├── main.py       # Orkestrasi utama ETL
├── requirements.txt  # Daftar dependency
├── tests/        # Unit test untuk setiap tahap
├── utils/        # Unit fitur utama ETL


## Menjalankan ETL  
Pastikan Anda telah menginstal **Python 3.8+** dan memiliki akun Google yang memiliki akses ke **Google Sheets API**.  

### Instal dependency  
Instal `pipreqs` untuk mengelola dependency: 

atau 

pip install pipreqs

atau

pip install -r requirements.txt 

## Menjalankan ETL

python main.py  

## Menjalankan Unit Test

python -m pytest tests