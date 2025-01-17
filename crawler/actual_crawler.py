import logging
from crawler.tasks import process_listing
from crawler.utils import fetch_listing_urls
import time

logging.basicConfig(level=logging.INFO)

def live_crawler(period=30):
    seen_urls = set()
    while True:
        logging.info("Fetching URLs...")
        urls = fetch_listing_urls()
        new_urls = [url for url in urls if url not in seen_urls]
        for url in new_urls:
            process_listing.delay(url)  # Queue the task
            logging.info(f"Queued new URL: {url}")
            seen_urls.add(url)
        logging.info(f"Sleeping for {period} seconds...")
        time.sleep(period)

if __name__ == "__main__":
    logging.info("Starting the live crawler...")
    live_crawler()
