import re
from scraper import get_book_data, scrape_books

def test_get_book_data_keys():
    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    data = get_book_data(url)
    assert isinstance(data, dict)
    for k in ["title", "price", "rating", "availability"]:
        assert k in data

def test_get_book_title_known():
    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    data = get_book_data(url)
    assert "Light" in data["title"]

def test_scrape_one_page_count():
    res = scrape_books(is_save=False, max_pages=1)
    assert isinstance(res, list)
    assert len(res) == 20
