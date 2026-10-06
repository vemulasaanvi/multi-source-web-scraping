ALLOWED_SOURCES = {
    "books_to_scrape",
    "quotes_to_scrape"
}


def validate_record(record):
    problems = []

  
    if record.get("source") not in ALLOWED_SOURCES:
        problems.append("invalid_source")

    name_or_title = record.get("name_or_title")

    if not name_or_title or not str(name_or_title).strip():
        problems.append("missing_name_or_title")

  
    source_url = record.get("source_url")

    if not source_url or not (
        source_url.startswith("http://")
        or source_url.startswith("https://")
    ):
        problems.append("invalid_source_url")

    
    price = record.get("price")

    if price is not None:
        try:
            price_value = float(price)

            if price_value < 0:
                problems.append("invalid_price")

        except (TypeError, ValueError):
            problems.append("invalid_price")

    
    rating = record.get("rating")

    if rating is not None:
        try:
            rating_value = int(rating)

            if rating_value < 1 or rating_value > 5:
                problems.append("invalid_rating")

        except (TypeError, ValueError):
            problems.append("invalid_rating")

    return problems