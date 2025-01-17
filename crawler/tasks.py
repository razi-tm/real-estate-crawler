from celery import Celery
from crawler.database import save_to_database
from crawler.utils import fetch_listing_details

# Correct the Celery app initialization to include the full module path
app = Celery("crawler.tasks", broker="redis://redis:6379/0")
app.conf.broker_connection_retry_on_startup = True

@app.task
def process_listing(listing_url):
    try:
        print(f"Processing listing: {listing_url}")
        details = fetch_listing_details(listing_url)
        if details:
            print(details)
            print(f"Fetched details: {details}")
            save_to_database(details)
            print(f"Task completed for {listing_url}")
        else:
            print(f"No details fetched for {listing_url}")
    except Exception as e:
        print(f"Error processing listing {listing_url}: {e}")
