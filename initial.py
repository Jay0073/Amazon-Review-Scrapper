import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_reviews(product_id):
    """
    Scrapes all reviews for a given Amazon product ID using Selenium,
    based on the confirmed HTML structure.
    """
    chrome_options = Options()
    # Uses the dedicated profile so you don't need to close your main browser.
    chrome_options.add_argument(r"--user-data-dir=C:\chrome-profile")
    driver_path = r"C:\webdriver\chromedriver.exe"
    service = Service(executable_path=driver_path)

    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return []

    reviews = []
    page_number = 1
    start_url = f"https://www.amazon.in/product-reviews/{product_id}/ref=cm_cr_arp_d_paging_btm_next_1?ieUTF8&reviewerType=all_reviews&pageNumber=1"
    
    driver.get(start_url)
    
    # You can comment out the input() line after the first successful run.
    input("--> SCRIPT PAUSED: If needed, log in. Then, press Enter here to start scraping...")

    while True:
        print(f"Scraping page: {page_number}...")
        wait = WebDriverWait(driver, 10)

        try:
            # CORRECTED WAIT: We now wait for any element with data-hook="review", which matches the <li> tag.
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-hook="review"]')))
            review_elements = driver.find_elements(By.CSS_SELECTOR, '[data-hook="review"]')
            print(f"Found {len(review_elements)} reviews on page {page_number}.")
        except TimeoutException:
            print("Timed out waiting for reviews to load. Assuming end of reviews.")
            break
        
        for review in review_elements:
            try:
                rating = review.find_element(By.CSS_SELECTOR, '[data-hook="review-star-rating"] span').get_attribute('innerHTML').strip().split(' ')[0]
                date = review.find_element(By.CSS_SELECTOR, '[data-hook="review-date"]').text.strip().replace('Reviewed in India on ', '')
                body = review.find_element(By.CSS_SELECTOR, '[data-hook="review-body"] span').get_attribute('innerHTML').strip().replace('<br>', '\n')

                reviews.append({'rating': rating, 'date': date, 'body': body})
            except NoSuchElementException:
                # This can happen if a review is structured differently (e.g., just a rating)
                print("Skipping a review with missing parts.")
                continue
            except Exception as e:
                print(f"An error occurred while parsing a review: {e}")
                continue
        
        # Pagination Logic
        try:
            # The 'Next page' button is in a list item with class 'a-last'
            next_page_li = driver.find_element(By.CSS_SELECTOR, 'ul.a-pagination li.a-last')
            # If the list item has the 'a-disabled' class, it's the last page.
            if 'a-disabled' in next_page_li.get_attribute('class'):
                print("Next page button is disabled. Reached the end of reviews.")
                break
            
            # Otherwise, find the link inside and click it.
            next_page_li.find_element(By.TAG_NAME, 'a').click()
            page_number += 1
            # Give the next page a moment to start loading
            time.sleep(2) 
        except NoSuchElementException:
            print("No 'Next page' button found. Reached the end of reviews.")
            break

    driver.quit()
    return reviews

def save_to_csv(reviews, filename):
    if not reviews:
        print("No reviews to save.")
        return
    fieldnames = ['rating', 'date', 'body']
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(reviews)
    print(f"\nSuccessfully saved {len(reviews)} reviews to {filename}")


if __name__ == "__main__":
    product_id_to_scrape = 'B0B1PXM75C' 
    scraped_reviews = get_reviews(product_id_to_scrape)
    
    if scraped_reviews:
        print("\n--- Sample of Scraped Reviews ---")
        for rev in scraped_reviews[:3]:
            print(rev)
            print("-" * 20)
        output_filename = f'amazon_reviews_{product_id_to_scrape}.csv'
        save_to_csv(scraped_reviews, output_filename)
