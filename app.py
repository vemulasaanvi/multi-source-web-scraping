from fastapi import FastAPI

from main import scrape_all_sources
from main import process_records
from main import deduplicate_records


app = FastAPI(
    title="Multi-Source Web Scraping API",
    description="API for the web scraping assignment",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Multi-Source Web Scraping API is running"
    }


@app.get("/scrape")
def scrape():
    raw_records, raw_counts, start_time, end_time, duration = (
        scrape_all_sources()
    )

    cleaned_records, rejected_records, rejection_counts = (
        process_records(raw_records)
    )

    final_records, duplicate_count = (
        deduplicate_records(cleaned_records)
    )

    return {
        "raw_records": len(raw_records),
        "raw_records_by_source": raw_counts,
        "valid_records": len(cleaned_records),
        "rejected_records": len(rejected_records),
        "rejection_counts": rejection_counts,
        "duplicates_removed": duplicate_count,
        "final_records": len(final_records),
        "duration_seconds": duration
    }