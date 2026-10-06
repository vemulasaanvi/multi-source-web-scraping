from processing.deduplication import (
    create_fingerprint,
    remove_duplicates,
)


def test_same_book_has_same_fingerprint():
    record1 = {
        "source": "books_to_scrape",
        "name_or_title": "A Light in the Attic",
    }

    record2 = {
        "source": "books_to_scrape",
        "name_or_title": " A Light in the Attic ",
    }

    assert create_fingerprint(record1) == create_fingerprint(record2)


def test_remove_duplicate_books():
    record1 = {
        "source": "books_to_scrape",
        "name_or_title": "A Light in the Attic",
    }

    record2 = {
        "source": "books_to_scrape",
        "name_or_title": "A Light in the Attic",
    }

    unique_records, duplicate_count = remove_duplicates(
        [record1, record2]
    )

    assert len(unique_records) == 1
    assert duplicate_count == 1


def test_unique_books_are_kept():
    record1 = {
        "source": "books_to_scrape",
        "name_or_title": "Book One",
    }

    record2 = {
        "source": "books_to_scrape",
        "name_or_title": "Book Two",
    }

    unique_records, duplicate_count = remove_duplicates(
        [record1, record2]
    )

    assert len(unique_records) == 2
    assert duplicate_count == 0


def test_duplicate_quotes():
    record1 = {
        "source": "quotes_to_scrape",
        "author": "Albert Einstein",
        "name_or_title": (
            "The world as we have created it is a process "
            "of our thinking."
        ),
    }

    record2 = {
        "source": "quotes_to_scrape",
        "author": "Albert Einstein",
        "name_or_title": (
            "The world as we have created it is a process "
            "of our thinking."
        ),
    }

    unique_records, duplicate_count = remove_duplicates(
        [record1, record2]
    )

    assert len(unique_records) == 1
    assert duplicate_count == 1