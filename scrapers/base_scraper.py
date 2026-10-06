import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def create_session():
    session = requests.Session()

    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/154.0.0.0 Safari/537.36"
        )
    })

    retry_strategy = Retry(
        total=3,
        connect=3,
        read=3,
        status=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
        respect_retry_after_header=True
    )

    adapter = HTTPAdapter(
        max_retries=retry_strategy
    )

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session

def fetch_page(session, url, timeout=20, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        try:
            response = session.get(
                url,
                timeout=timeout
            )

            response.raise_for_status()
            response.encoding = "utf-8"

            return response

        except requests.RequestException as error:
            print(
                f"Request failed "
                f"(attempt {attempt}/{max_attempts}): {url}"
            )

            if attempt == max_attempts:
                raise

            wait_time = 2 ** (attempt - 1)

            print(
                f"Retrying in {wait_time} seconds..."
            )

            import time
            time.sleep(wait_time)