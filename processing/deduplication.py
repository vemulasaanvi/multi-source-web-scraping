import hashlib

from processing.cleaning import clean_text


def create_fingerprint(record):
    source = record.get("source", "")

    if source == "books_to_scrape":
        title = clean_text(
            record.get("name_or_title", "")
        ).lower()

        fingerprint_text = f"{source}|{title}"

    elif source == "quotes_to_scrape":
        author = clean_text(
            record.get("author", "")
        ).lower()

        quote = clean_text(
            record.get("name_or_title", "")
        ).lower()

        fingerprint_text = (
            f"{source}|{author}|{quote[:50]}"
        )

    else:
        fingerprint_text = str(record)

    return hashlib.sha256(
        fingerprint_text.encode("utf-8")
    ).hexdigest()


def remove_duplicates(records):
    unique_records = []
    seen_fingerprints = set()
    duplicate_count = 0

    for record in records:
        fingerprint = create_fingerprint(record)

        if fingerprint in seen_fingerprints:
            duplicate_count += 1
            continue

        seen_fingerprints.add(fingerprint)
        unique_records.append(record)

    return unique_records, duplicate_count