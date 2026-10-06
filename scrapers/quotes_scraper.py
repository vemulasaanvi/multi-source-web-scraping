import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from scrapers.base_scraper import create_session, fetch_page


QUOTES_HOME = "https://quotes.toscrape.com/"


class QuotesScraper:

    def __init__(self):
        self.session = create_session()
        self.delay = 0.5

    def scrape(self):
        records = []
        current_url = QUOTES_HOME

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

            quotes = soup.select("div.quote")

            for quote in quotes:
                text_element = quote.select_one(
                    "span.text"
                )

                author_element = quote.select_one(
                    "small.author"
                )

                tags = quote.select(
                    "div.tags a.tag"
                )

                next_link = None

                record = {
                    "source": "quotes_to_scrape",
                    "source_url": current_url,
                    "name_or_title": (
                        text_element.get_text()
                        if text_element
                        else None
                    ),
                    "category": None,
                    "price": None,
                    "rating": None,
                    "author": (
                        author_element.get_text(strip=True)
                        if author_element
                        else None
                    ),
                    "tags": (
                        [
                            tag.get_text(strip=True)
                            for tag in tags
                        ]
                        if tags
                        else []
                    ),
                    "description": None,
                    "availability": None,
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