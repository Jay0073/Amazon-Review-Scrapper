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
    # input("--> SCRIPT PAUSED: If needed, log in. Then, press Enter here to start scraping...")

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
                reviewer = review.find_element(By.CSS_SELECTOR, ".a-profile-name").text.strip()
                rating = review.find_element(By.CSS_SELECTOR, '[data-hook="review-star-rating"] span').get_attribute("innerHTML").strip().split(" ")[0]
                date = review.find_element(By.CSS_SELECTOR, '[data-hook="review-date"]').text.strip().replace("Reviewed in India on ", "")
                title = review.find_element(By.CSS_SELECTOR, '[data-hook="review-title"] span').get_attribute("innerHTML").strip().replace("<br>", "\n")
                reviews.append({"reviewer": reviewer, "rating": rating, "date": date, "title": title})
                print(f"Scraped review: {rating} stars on {date}")
            except Exception as e:
                print(f"Skipping review due to error: {e}")
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
        
    print(f"Total reviews scraped: {len(reviews)}")

    driver.quit()
    return reviews


# for testing
if __name__ == "__main__":
    asin = "B0B1PXM75C"
    reviews = get_reviews(asin)
    save_reviews_to_csv(reviews, f"data/amazon_reviews_{asin}.csv")
