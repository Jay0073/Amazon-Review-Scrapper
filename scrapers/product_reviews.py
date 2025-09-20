import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from utils.driver_setup import get_driver
from utils.file_utils import save_reviews_to_csv

def get_reviews(product_id):
    driver = get_driver()
    reviews = []
    page_number = 1
    start_url = f"https://www.amazon.in/product-reviews/{product_id}/ref=cm_cr_arp_d_paging_btm_next_1?ie=UTF8&reviewerType=all_reviews&pageNumber=1"
    
    driver.get(start_url)
    input("--> Log in if needed, then press Enter...")

    while True:
        print(f"Scraping page: {page_number}...")
        wait = WebDriverWait(driver, 10)

        try:
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-hook="review"]')))
            review_elements = driver.find_elements(By.CSS_SELECTOR, '[data-hook="review"]')
        except TimeoutException:
            print("No more reviews. Stopping.")
            break

        for review in review_elements:
            try:
                rating = review.find_element(By.CSS_SELECTOR, '[data-hook="review-star-rating"] span').text.split()[0]
                date = review.find_element(By.CSS_SELECTOR, '[data-hook="review-date"]').text.replace("Reviewed in India on ", "")
                body = review.find_element(By.CSS_SELECTOR, '[data-hook="review-body"] span').text
                reviews.append({"rating": rating, "date": date, "body": body})
            except Exception:
                continue

        try:
            next_page_li = driver.find_element(By.CSS_SELECTOR, "ul.a-pagination li.a-last")
            if "a-disabled" in next_page_li.get_attribute("class"):
                break
            next_page_li.find_element(By.TAG_NAME, "a").click()
            page_number += 1
            time.sleep(2)
        except NoSuchElementException:
            break

    driver.quit()
    return reviews


# for testing
if __name__ == "__main__":
    asin = "B0B1PXM75C"
    reviews = get_reviews(asin)
    save_reviews_to_csv(reviews, f"data/amazon_reviews_{asin}.csv")
