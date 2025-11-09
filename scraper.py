import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_book_data(book_url: str) -> dict:
    r = requests.get(book_url, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.select_one("div.product_main > h1").get_text(strip=True)
    price = soup.select_one("p.price_color").get_text(strip=True)
    rating_cls = soup.select_one("p.star-rating")["class"]
    rating = next((c for c in rating_cls if c != "star-rating"), None)
    availability = soup.select_one("p.instock.availability").get_text(strip=True)
    desc_head = soup.find(id="product_description")
    description = ""
    if desc_head:
        nxt = desc_head.find_next("p")
        if nxt:
            description = nxt.get_text(strip=True)
    data = {"url": book_url, "title": title, "price": price, "rating": rating, "availability": availability, "description": description}
    table = soup.select_one("table.table.table-striped")
    if table:
        for row in table.select("tr"):
            key = row.th.get_text(strip=True)
            val = row.td.get_text(strip=True)
            data[key.lower().replace(" ", "_").replace("(", "").replace(")", "")] = val
    return data

def scrape_books(base_url: str = "http://books.toscrape.com", is_save: bool = False, save_path: str = "books_data.txt", max_pages: int | None = None):
    url = urljoin(base_url, "/catalogue/page-1.html")
    all_books = []
    page = 1
    while True:
        if max_pages is not None and page > max_pages:
            break
        resp = requests.get(url, timeout=20)
        if resp.status_code != 200:
            break
        soup = BeautifulSoup(resp.text, "html.parser")
        links = [urljoin(url, a.get("href")) for a in soup.select("article.product_pod h3 a")]
        for href in links:
            book_url = href if href.endswith("/index.html") else href.replace("../../../", "http://books.toscrape.com/catalogue/")
            all_books.append(get_book_data(book_url))
        page += 1
        url = urljoin(base_url, f"/catalogue/page-{page}.html")
    if is_save:
        with open(save_path, "w", encoding="utf-8") as f:
            for item in all_books:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
    return all_books

if __name__ == "__main__":
    scrape_books(is_save=True, save_path="artifacts/books_data.txt")
