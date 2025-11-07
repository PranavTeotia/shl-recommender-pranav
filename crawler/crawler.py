import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv, time, os

BASE = "https://www.shl.com/solutions/products/product-catalog/"

def extract_product_urls(base=BASE):
    r = requests.get(base, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    urls = set()
    for a in soup.select("a[href]"):
        href = a['href']
        if "/products/" in href and "product-catalog" not in href:
            urls.add(urljoin(base, href))
    return sorted(urls)

def parse_product_page(url):
    r = requests.get(url, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    name = (soup.select_one("h1") or soup.select_one("title")).get_text(strip=True)
    paragraphs = [p.get_text(separator=" ", strip=True) for p in soup.select("p")]
    desc = " ".join(paragraphs)
    test_type = None
    body = soup.get_text(" ", strip=True)
    if "personality" in body.lower(): test_type = "P"
    if "skills" in body.lower() or "knowledge" in body.lower():
        test_type = (test_type or "K")
    return {"assessment_name": name, "assessment_url": url, "test_type": test_type or "U", "short_description": desc[:2000], "full_text": name + " " + desc}

def crawl_and_save(out_path="data/shl_catalog.csv"):
    urls = extract_product_urls()
    items = []
    for u in urls:
        try:
            items.append(parse_product_page(u))
            time.sleep(0.5)
        except Exception as e:
            print("Error", u, e)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    keys = ["assessment_name","assessment_url","test_type","short_description","full_text"]
    with open(out_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(items)

if __name__ == "__main__":
    crawl_and_save()
