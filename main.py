from scrapers.product_ids import get_asins_and_review_links
from scrapers.product_reviews import get_reviews
from utils.file_utils import save_asins_to_csv, save_reviews_to_csv

if __name__ == "__main__":
    # Step 1: Scrape ASINs + review links
    search_url = "https://www.amazon.in/s?k=laptops+under+50k"
    asins, review_links = get_asins_and_review_links(search_url, max_pages=1)
    save_asins_to_csv(asins, review_links)

    # Step 2: Scrape reviews for first ASIN (as example)
    if asins:
        reviews = get_reviews(asins[0])
        save_reviews_to_csv(reviews, f"data/amazon_reviews_{asins[0]}.csv")
