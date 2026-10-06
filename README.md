# Multi-Source Web Scraping & Data Consolidation

## Overview

This project implements a Python-based web scraping pipeline that collects public data from multiple websites, cleans and validates the collected records, detects duplicates, and generates consolidated CSV and JSON outputs.

The project scrapes data from:

- Books to Scrape
- Quotes to Scrape

The pipeline is designed with pagination support, request retries, error handling, data cleaning, validation, deduplication, logging, testing, and structured output generation.

---

## Sources

### Books to Scrape

https://books.toscrape.com/

The scraper collects approximately 1,000 book records across 50 pages.

### Quotes to Scrape

https://quotes.toscrape.com/

The scraper collects approximately 100 quote records across 10 pages.

Only publicly available information is accessed. No authentication, CAPTCHA bypass, or restricted information is used.

---

## Features

- Multi-source web scraping
- Dynamic pagination handling
- HTTP request retries
- Request timeout handling
- Reasonable delay between requests
- Source-level error handling
- Common data schema
- Text cleaning and normalization
- Price conversion to numeric values
- Rating standardization
- Tag normalization
- URL validation
- Record validation
- Duplicate detection using SHA-256 fingerprints
- CSV output
- JSON summary report
- Logging
- Unit tests using pytest

---

## Technologies Used

- Python 3.13
- Requests
- BeautifulSoup4
- pytest
- Python standard library

---

## Project Structure

```text
scraping-assignment/
│
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py
│   ├── books_scraper.py
│   └── quotes_scraper.py
│
├── processing/
│   ├── __init__.py
│   ├── cleaning.py
│   ├── validation.py
│   └── deduplication.py
│
├── tests/
│   ├── test_cleaning.py
│   ├── test_validation.py
│   └── test_deduplication.py
│
├── output/
│   ├── final_dataset.csv
│   └── summary_report.json
│
├── logs/
│   └── scraper.log
│
├── main.py
├── requirements.txt
├── pytest.ini
├── README.md
└── AI_USAGE.md


## Installation

### 1. Clone or download the project

Open the project directory in a terminal.

### 2. Create a virtual environment

```bash
python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt


```markdown
## Running the Scraper

Run:

```bash
python main.py