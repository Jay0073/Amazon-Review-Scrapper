import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.driver_setup import get_driver
from utils.file_utils import save_asins_to_csv

def get_asins_and_review_links(search_url):
    """
    Scrapes all product ASINs and their review links from a search results page,
    handling pagination.
    """
    driver = get_driver()
    all_asins = set()
    review_links = []
    current_url = search_url

    try:
        while True:
            print(f"Fetching: {current_url}")
            driver.get(current_url)
            time.sleep(2)  # Wait for the page to load

            # Wait for search results to be present
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-asin]")))

            products = driver.find_elements(By.CSS_SELECTOR, "div[data-asin]")
            for product in products:
                asin = product.get_attribute("data-asin")
                if asin and len(asin.strip()) > 5:
                    all_asins.add(asin)

            # Find and click the next page button
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "a.s-pagination-next")
                if "s-pagination-disabled" in next_button.get_attribute("class"):
                    break  # No more pages
                current_url = next_button.get_attribute("href")
            except NoSuchElementException:
                break # No next button found

    except TimeoutException:
        print("Timeout while waiting for search results. Ending pagination.")
    finally:
        driver.quit()

    for asin in all_asins:
        link = f"https://www.amazon.in/product-reviews/{asin}/ref=cm_cr_arp_d_paging_btm_next_1?ie=UTF8&reviewerType=all_reviews&pageNumber=1"
        review_links.append(link)

    return list(all_asins), review_links


# for testing
if __name__ == "__main__":
    search_url = "https://www.amazon.in/s?k=laptops+under+50k"
    asins, review_urls = get_asins_and_review_links(search_url, max_pages=2)
    save_asins_to_csv(asins, review_urls)
