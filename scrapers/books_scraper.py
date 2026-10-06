import time

from urllib.parse import urljoin

from bs4 import BeautifulSoup

from scrapers.base_scraper import create_session, fetch_page


BOOKS_HOME = "https://books.toscrape.com/"


class BooksScraper:

    def __init__(self):
        self.session = create_session()
        self.delay=0.5

    def get_book_details(self, book_url):
        response = fetch_page(self.session, book_url)
        time.sleep(self.delay)

        soup = BeautifulSoup(response.text, "html.parser")

        category_element = soup.select_one(
            "ul.breadcrumb li:nth-of-type(3)"
        )

        rating_element = soup.select_one(
            "p.star-rating"
        )

        description_element = soup.select_one(
            "#product_description + p"
        )

        rating = None

        if rating_element:
            rating_classes = rating_element.get("class", [])

            rating_words = {
                "One": 1,
                "Two": 2,
                "Three": 3,
                "Four": 4,
                "Five": 5
            }

            for word, value in rating_words.items():
                if word in rating_classes:
                    rating = value
                    break

        return {
            "category": (
                category_element.get_text(strip=True)
                if category_element
                else None
            ),
            "rating": rating,
            "description": (
                description_element.get_text(strip=True)
                if description_element
                else None
            )
        }

    def scrape(self):
        records = []
        current_url = BOOKS_HOME

        while current_url:
            print("Scraping:", current_url)

            response = fetch_page(
                self.session,
                current_url
            )

            time.sleep(self.delay)

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            books = soup.select(
                "article.product_pod"
            )

            for book in books:
                title_element = book.select_one(
                    "h3 a"
                )

                price_element = book.select_one(
                    "p.price_color"
                )

                availability_element = book.select_one(
                    "p.instock.availability"
                )

                book_link_element = book.select_one(
                    "h3 a"
                )

                if not title_element:
                    continue

                book_url = None

                if book_link_element:
                    book_url = urljoin(
                        current_url,
                        book_link_element.get("href")
                    )

                details = {
                    "category": None,
                    "rating": None,
                    "description": None
                }

                if book_url:
                    try:
                        details = self.get_book_details(
                            book_url
                        )
                    except Exception as error:
                        print(
                            f"Could not get details for "
                            f"{book_url}: {error}"
                        )

                record = {
                    "source": "books_to_scrape",

                    "source_url": book_url,

                    "name_or_title": (
                        title_element.get("title")
                    ),

                    "category": details["category"],

                    "price": (
                        price_element.get_text(strip=True)
                        if price_element
                        else None
                    ),

                    "rating": details["rating"],

                    "author": None,

                    "tags": None,

                    "description": details["description"],

                    "availability": (
                        availability_element.get_text(
                            strip=True
                        )
                        if availability_element
                        else None
                    ),

                    "scraped_at": None,
                }

                records.append(record)

            next_link = soup.select_one(
                "li.next a"
            )

            if next_link:
                current_url = urljoin(
                    current_url,
                    next_link.get("href")
                )
            else:
                current_url = None

        return records