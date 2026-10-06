import csv
import json
import logging

from datetime import datetime, timezone

from scrapers.books_scraper import BooksScraper
from scrapers.quotes_scraper import QuotesScraper

from processing.cleaning import (
    clean_text,
    strip_quotes,
    clean_price,
    clean_rating,
    clean_tags,
    normalize_url,
)

from processing.validation import validate_record
from processing.deduplication import remove_duplicates


logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def clean_record(record):
    cleaned = record.copy()

    cleaned["source"] = clean_text(
        cleaned.get("source")
    )

    cleaned["source_url"] = normalize_url(
        cleaned.get("source_url")
    )

    cleaned["name_or_title"] = strip_quotes(
        cleaned.get("name_or_title")
    )

    cleaned["category"] = clean_text(
        cleaned.get("category")
    )

    cleaned["price"] = clean_price(
        cleaned.get("price")
    )

    cleaned["rating"] = clean_rating(
        cleaned.get("rating")
    )

    cleaned["author"] = clean_text(
        cleaned.get("author")
    )

    cleaned["tags"] = clean_tags(
        cleaned.get("tags")
    )

    cleaned["description"] = clean_text(
        cleaned.get("description")
    )

    cleaned["availability"] = clean_text(
        cleaned.get("availability")
    )

    if not cleaned.get("scraped_at"):
        cleaned["scraped_at"] = datetime.now(
            timezone.utc
        ).isoformat()

    return cleaned


def process_records(raw_records):
    cleaned_records = []
    rejected_records = []
    rejection_counts = {}

    for record in raw_records:
        try:
            cleaned = clean_record(record)

            problems = validate_record(cleaned)

            if problems:
                rejected_records.append({
                    "record": cleaned,
                    "problems": problems
                })

                for problem in problems:
                    rejection_counts[problem] = (
                        rejection_counts.get(problem, 0) + 1
                    )

                continue

            cleaned_records.append(cleaned)

        except Exception as error:
            rejected_records.append({
                "record": record,
                "problems": ["processing_error"]
            })

            rejection_counts["processing_error"] = (
                rejection_counts.get("processing_error", 0) + 1
            )

    return (
        cleaned_records,
        rejected_records,
        rejection_counts
    )


def scrape_all_sources():
    start_time = datetime.now(timezone.utc)

    all_raw_records = []
    raw_counts = {}

    try:
        books_scraper = BooksScraper()
        books_records = books_scraper.scrape()

        logger.info(
            f"Books scraping completed: {len(books_records)} records"
        )

        all_raw_records.extend(books_records)
        raw_counts["books_to_scrape"] = len(books_records)

    except Exception as error:
        logger.error(
            f"Books scraper failed: {error}"
        )
        raw_counts["books_to_scrape"] = 0

    try:
        quotes_scraper = QuotesScraper()
        quotes_records = quotes_scraper.scrape()

        logger.info(
            f"Quotes scraping completed: {len(quotes_records)} records"
        )

        all_raw_records.extend(quotes_records)
        raw_counts["quotes_to_scrape"] = len(quotes_records)

    except Exception as error:
        logger.error(
            f"Quotes scraper failed: {error}"
        )
        raw_counts["quotes_to_scrape"] = 0

    end_time = datetime.now(timezone.utc)

    duration = (
        end_time - start_time
    ).total_seconds()

    return (
        all_raw_records,
        raw_counts,
        start_time,
        end_time,
        duration
    )


def deduplicate_records(records):
    unique_records, duplicate_count = remove_duplicates(
        records
    )

    return unique_records, duplicate_count


def save_csv(records):
    output_file = "output/final_dataset.csv"

    fieldnames = [
        "source",
        "source_url",
        "name_or_title",
        "category",
        "price",
        "rating",
        "author",
        "tags",
        "description",
        "availability",
        "scraped_at",
    ]

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(records)

    print(
        f"CSV saved successfully: {output_file}"
    )


def save_summary_report(summary):
    output_file = "output/summary_report.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            summary,
            file,
            indent=4
        )

    print(
        f"Summary report saved successfully: {output_file}"
    )


if __name__ == "__main__":
    raw_records, raw_counts, start_time, end_time, duration = (
        scrape_all_sources()
    )

    print(
        f"\nTotal raw records: {len(raw_records)}"
    )

    cleaned_records, rejected_records, rejection_counts = (
        process_records(raw_records)
    )

    print(
        f"Valid records: {len(cleaned_records)}"
    )

    print(
        f"Rejected records: {len(rejected_records)}"
    )

    unique_records, duplicate_count = (
        deduplicate_records(cleaned_records)
    )

    print(
        f"Duplicates removed: {duplicate_count}"
    )

    print(
        f"Final records: {len(unique_records)}"
    )

    save_csv(unique_records)

    summary = {
        "run_started_at": start_time.isoformat(),
        "run_finished_at": end_time.isoformat(),
        "duration_seconds": duration,
        "raw_records": len(raw_records),
        "raw_records_by_source": raw_counts,
        "valid_records": len(cleaned_records),
        "rejected_records": len(rejected_records),
        "rejection_counts": rejection_counts,
        "duplicates_removed": duplicate_count,
        "final_records": len(unique_records),
    }

    save_summary_report(summary)