# Hot Wheels Data Scraper

Aplikasi ini digunakan untuk mengambil data Hot Wheels dari website Fandom Hot Wheels.
Silakan kunjungi YouTube https://youtu.be/R6HiF4f-dCA untuk melihat demo.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/R6HiF4f-dCA/0.jpg)]([https://www.youtube.com/watch?v=YOUTUBE_VIDEO_ID_HERE](https://youtu.be/R6HiF4f-dCA))

## Persyaratan
- Python 3.7 atau lebih tinggi
- pip (Python package installer)

## Instalasi

1. Clone repository ini ke komputer Anda
2. Buka terminal dan masuk ke direktori project
3. Install dependencies yang diperlukan:
```bash
pip install -r requirements.txt
```

## Konfigurasi

Buka file `scraping_detail.py` dan sesuaikan variabel berikut sesuai kebutuhan Anda:

```python
url = "https://hotwheels.fandom.com/wiki/%2768_Dodge_Dart"  # URL Hot Wheels yang ingin di-scrape
tagUUID = "045BC2EA067380"                                  # Tag UUID untuk identifikasi
database = "database.json"                                  # Nama file database JSON
serial_number = "HCW96"                                    # Nomor seri Hot Wheels (lihat belakang blister Hotwheels)
```

### Penjelasan Variabel:
- `url`: URL halaman Hot Wheels di Fandom yang ingin Anda ambil datanya
- `tagUUID`: Kode unik untuk identifikasi item (dapat disesuaikan)
- `database`: Nama file JSON untuk menyimpan hasil scraping
- `serial_number`: Nomor seri Hot Wheels yang sedang di-scrape

## Cara Penggunaan

1. Sesuaikan konfigurasi seperti yang dijelaskan di atas
2. Jalankan script dengan perintah:
```bash
python scraping_detail.py
```

## Output

Data hasil scraping akan disimpan dalam file JSON sesuai dengan nama yang ditentukan di variabel `database`.

## Catatan Penting

- Pastikan Anda memiliki koneksi internet yang stabil saat menjalankan script
- Hormati Terms of Service dari website yang di-scrape
- Disarankan untuk memberikan jeda waktu yang cukup jika melakukan scraping multiple pages

## Troubleshooting

Jika mengalami masalah:
1. Pastikan semua dependencies terinstall dengan benar
2. Periksa koneksi internet Anda
3. Pastikan URL yang dimasukkan valid dan dapat diakses

## Kontribusi

Silakan buat pull request jika ingin berkontribusi pada project ini.
