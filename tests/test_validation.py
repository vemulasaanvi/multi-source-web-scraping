from processing.validation import validate_record


def test_valid_book_record():
    record = {
        "source": "books_to_scrape",
        "source_url": "https://books.toscrape.com/book.html",
        "name_or_title": "A Light in the Attic",
        "price": 51.77,
        "rating": 3,
    }

    assert validate_record(record) == []


def test_missing_title():
    record = {
        "source": "books_to_scrape",
        "source_url": "https://books.toscrape.com/book.html",
        "name_or_title": "",
        "price": 51.77,
        "rating": 3,
    }

    assert "missing_name_or_title" in validate_record(record)


def test_invalid_url():
    record = {
        "source": "books_to_scrape",
        "source_url": "books.toscrape.com/book.html",
        "name_or_title": "Test Book",
        "price": 10.0,
        "rating": 3,
    }

    assert "invalid_source_url" in validate_record(record)


def test_invalid_price():
    record = {
        "source": "books_to_scrape",
        "source_url": "https://books.toscrape.com/book.html",
        "name_or_title": "Test Book",
        "price": -10,
        "rating": 3,
    }

    assert "invalid_price" in validate_record(record)


def test_invalid_rating():
    record = {
        "source": "books_to_scrape",
        "source_url": "https://books.toscrape.com/book.html",
        "name_or_title": "Test Book",
        "price": 10.0,
        "rating": 6,
    }

    assert "invalid_rating" in validate_record(record)