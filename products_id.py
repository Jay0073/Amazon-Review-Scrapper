import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_asins_and_review_links(search_url, max_pages=1):
    """
    Scrapes product ASINs from Amazon search results and builds review page links.
    :param search_url: Amazon search or category page URL
    :param max_pages: Number of search result pages to scrape
    """
    chrome_options = Options()
    chrome_options.add_argument(r"--user-data-dir=C:\chrome-profile")
    driver_path = r"C:\webdriver\chromedriver.exe"
    service = Service(executable_path=driver_path)

    driver = webdriver.Chrome(service=service, options=chrome_options)

    all_asins = set()
    review_links = []

    for page in range(1, max_pages + 1):
        url = f"{search_url}&page={page}"
        print(f"Fetching: {url}")
        driver.get(url)

        time.sleep(2)  # wait for page to load fully

        # Get all product containers with data-asin
        products = driver.find_elements(By.CSS_SELECTOR, "div[data-asin]")
        for product in products:
            asin = product.get_attribute("data-asin")
            if asin and len(asin.strip()) > 5:  # valid ASIN
                all_asins.add(asin)

    driver.quit()

    # Build review links
    for asin in all_asins:
        link = f"https://www.amazon.in/product-reviews/{asin}/ref=cm_cr_arp_d_paging_btm_next_1?ie=UTF8&reviewerType=all_reviews&pageNumber=1"
        review_links.append(link)

    return list(all_asins), review_links


if __name__ == "__main__":
    # Example: search for "laptops"
    search_url = "https://www.amazon.in/s?k=laptops+under+50k"
    asins, review_urls = get_asins_and_review_links(search_url, max_pages=2)

    print("\nASINs Found:")
    print(asins)

    print("\nReview Page Links:")
    for link in review_urls[:10]:  # show first 10
        print(link)

    print(f"\nTotal ASINs collected: {len(asins)}")
