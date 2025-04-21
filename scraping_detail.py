import requests
from bs4 import BeautifulSoup
import json
import time

def parse_version_data(versions):
    if not versions:
        return []
        
    # Ambil header dari baris pertama
    headers = versions[0].split('|')
    headers = [h.strip() for h in headers]
    
    result = []
    # Mulai dari baris kedua (skip header)
    for version in versions[1:]:
        values = version.split('|')
        values = [v.strip() for v in values]
        
        # Buat dictionary dengan menggabungkan header dan value
        version_dict = {}
        for i, value in enumerate(values):
            if i < len(headers):  # Pastikan tidak melebihi jumlah header
                key = headers[i] if headers[i] else f"Column_{i}"  # Gunakan Column_X jika header kosong
                version_dict[key] = value
        
        result.append(version_dict)
    
    return result

def parse_version_data(versions):
    if not versions:
        return []
        
    # Ambil header dari baris pertama
    headers = versions[0].split('|')
    headers = [h.strip() for h in headers]
    
    result = []
    # Mulai dari baris kedua (skip header)
    for version in versions[1:]:
        values = version.split('|')
        values = [v.strip() for v in values]
        
        # Buat dictionary dengan menggabungkan header dan value
        version_dict = {}
        for i, value in enumerate(values):
            if i < len(headers):  # Pastikan tidak melebihi jumlah header
                key = headers[i] if headers[i] else f"Column_{i}"  # Gunakan Column_X jika header kosong
                version_dict[key] = value
        
        result.append(version_dict)
    
    return result

def get_detail_info(detail_url, serial_number):
    detail_data = {
        "Description": None,
        "Versions": [],
        "Gallery Images": []
    }
    try:
        res = requests.get(detail_url)
        detail_soup = BeautifulSoup(res.content, 'html.parser')

        content = detail_soup.find('div', class_='mw-parser-output')

        # --- Description ---
        if content:
            # Ambil semua <p> sampai ketemu <h2> (section berikutnya)
            paragraphs = []
            for elem in content.find_all(['p', 'h2'], recursive=False):
                if elem.name == 'h2':
                    break
                if elem.name == 'p':
                    text = elem.get_text(strip=True)
                    if text and not text.lower().startswith("this article is"):  # filter filler text
                        paragraphs.append(text)
            detail_data["Description"] = "\n\n".join(paragraphs)

        # --- Versions ---
        versions_section = None
        for header in content.find_all(['h2', 'h3']):
            span = header.find('span', class_='mw-headline')
            if span and 'Versions' in span.text:
                versions_section = header
                break

        if versions_section:
            # cari elemen berikutnya hingga ketemu <ul> atau <table>
            next_elem = versions_section.find_next_sibling()
            while next_elem:
                if next_elem.name == 'ul':
                    detail_data["Versions"] = [li.get_text(strip=True) for li in next_elem.find_all('li')]
                    break
                elif next_elem.name == 'table':
                    rows = next_elem.find_all('tr')
                    detail_data["Versions"] = [" | ".join(td.get_text(strip=True) for td in row.find_all(['td', 'th'])) for row in rows]
                    break
                next_elem = next_elem.find_next_sibling()

        # --- Gallery Images ---
        gallery_imgs = detail_soup.select('.wikia-gallery-item img, .gallerybox img')
        detail_data["Gallery Images"] = [img['src'] for img in gallery_imgs if img.get('src')]
        detail_data["Versions"] = parse_version_data(detail_data["Versions"])
        
        for version in detail_data["Versions"]:
            if version["Toy #"] == serial_number:
                for key in version.keys():
                    detail_data[key] = version[key]

    except Exception as e:
        print(f"Gagal memuat detail {detail_url}: {e}")

    return detail_data

if __name__ == "__main__":
    # custom here
    url = "https://hotwheels.fandom.com/wiki/%2768_Dodge_Dart"
    tagUUID = "045BC2EA067380"
    database = "database.json"
    serial_number = "HCW96"
    # end
    
    filename = url.split('/')[:-1]
    data = get_detail_info(url, serial_number=serial_number)
    data["TagUUID"] = tagUUID

    # load previous database data
    all_data = []
    with open(database, "r") as f:
        all_data = json.loads(f.read())
    all_data.append(data)

    with open(database, "w") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
