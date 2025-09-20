import time
from selenium.webdriver.common.by import By
from utils.driver_setup import get_driver
from utils.file_utils import save_asins_to_csv

def get_asins_and_review_links(search_url, max_pages=1):
    driver = get_driver()
    all_asins = set()
    review_links = []

    for page in range(1, max_pages + 1):
        url = f"{search_url}&page={page}"
        print(f"Fetching: {url}")
        driver.get(url)
        time.sleep(2)

        products = driver.find_elements(By.CSS_SELECTOR, "div[data-asin]")
        for product in products:
            asin = product.get_attribute("data-asin")
            if asin and len(asin.strip()) > 5:
                all_asins.add(asin)

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
