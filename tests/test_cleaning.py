from processing.cleaning import (
    clean_text,
    strip_quotes,
    clean_price,
    clean_rating,
    clean_tags,
    normalize_url,
)


def test_clean_text():
    assert clean_text(" Hello \n world ") == "Hello world"


def test_strip_quotes():
    assert strip_quotes(
        "“Hello world”"
    ) == "Hello world"


def test_clean_price():
    assert clean_price("£51.77") == 51.77


def test_clean_rating():
    assert clean_rating("Three") == 3


def test_clean_tags():
    assert clean_tags(
        ["World", "thinking", "world"]
    ) == "thinking;world"


def test_normalize_url():
    assert normalize_url(
        "https://example.com"
    ) == "https://example.com"


def test_invalid_url():
    assert normalize_url(
        "example.com"
    ) is None