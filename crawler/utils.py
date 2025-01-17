import json
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


BASE_URL = "https://www.bayut.com/for-sale/property/dubai/?sort=date_desc"

from tempfile import mkdtemp

def get_webdriver():
    """Initialize and return a Selenium WebDriver instance."""
    options = Options()
    options.add_argument("--headless")  # Comment this out for debugging
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")

    # Use a unique temporary directory for user data
    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={user_data_dir}")

    # Specify the ChromeDriver binary path
    service = Service("/usr/bin/chromedriver")
    print(f"Initializing WebDriver with user-data-dir: {user_data_dir}")

    return webdriver.Chrome(service=service, options=options)

def fetch_listing_urls():
    """Fetch listing URLs from the main page."""
    driver = get_webdriver()
    try:
        print("Initializing WebDriver...")
        print("Browser Version:", driver.capabilities["browserVersion"])
        print("Driver Version:", driver.capabilities["chrome"]["chromedriverVersion"])

        driver.get(BASE_URL)
        print("Page loaded successfully.")

        # Scroll to ensure all content loads
        for _ in range(5):
            driver.execute_script("window.scrollBy(0, 1000);")
            WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "body")))

        # Wait for elements with the correct class to load
        wait = WebDriverWait(driver, 15)
        listings = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.d40f2294")))

        # Extract and return URLs
        urls = [listing.get_attribute("href") for listing in listings if listing.get_attribute("href")]
        print(f"Found {len(urls)} listing URLs.")
        return urls

    except Exception as e:
        print(f"Error fetching listing URLs: {e}")
        return []

    finally:
        driver.quit()



def fetch_listing_details(listing_url):
    """Fetch property details for a given URL."""
    driver = get_webdriver()
    try:
        driver.get(listing_url)
        print(f"Fetching details for: {listing_url}")

        # Wait for content to load
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))

        # Extract property details
        try:
            region = driver.find_element(By.XPATH, "//script[contains(text(), 'addressLocality')]").get_attribute("innerHTML")
            region_start = region.find('"addressLocality":"') + len('"addressLocality":"')
            region_end = region.find('"', region_start)
            region = region[region_start:region_end] if region_start > 0 and region_end > 0 else "Unknown"
        except Exception as e:
            print(f"Error extracting region for {listing_url}: {e}")
            region = "Unknown"
        

        # try:
        #     trucheck_elements = driver.find_elements(By.XPATH, "//div[@aria-label='Property Verified Button']")
        #     for element in trucheck_elements:
        #         print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        #         ancestors = element.find_elements(By.XPATH, "./ancestor::*")
        #         print(f"Element: {element.get_attribute('outerHTML')}")
        #         for ancestor in ancestors:
        #             print("-----------------------------------------------------------------------")
        #             print(f"Ancestor: {ancestor.get_attribute('outerHTML')[:500]}")
        # except:
        #     print("exception")

        try:
            # Locate the TruCheck element outside of the recommended section
            trucheck_element = driver.find_element(
                By.XPATH,
                "//div[@aria-label='Property Verified Button' and not(ancestor::div[.//h2[contains(@class, '_19b9b537') and text()='Recommended for you']])]"
            )
            print(f"TruCheck element: {trucheck_element.get_attribute('outerHTML')}")
            trucheck = True
        except Exception as e:
            print(f"No TruCheck element found or error: {e}")
            trucheck = False


        details = {"url": listing_url, "region": region, "trucheck": trucheck}
        print(f"Fetched details: {details}")
        return details

    except Exception as e:
        print(f"Error fetching details for {listing_url}: {e}")
        return None

    finally:
        driver.quit()
