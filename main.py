from scrapers.product_ids import get_asins_and_review_links
from scrapers.product_reviews import get_reviews
from utils.file_utils import save_asins_to_csv, save_reviews_to_csv
import time

if __name__ == "__main__":
    # Define the single CSV file for all reviews
    all_reviews_filename = "data/all_amazon_reviews.csv"
    
    # Step 1: Scrape ASINs + review links from all search result pages
    search_url = "https://www.amazon.in/s?k=paddle&crid=17RGU0LOFJERO&sprefix=paddl%2Caps%2C288&ref=nb_sb_noss_2"
    print("Starting ASIN scraping...")
    asins, review_links = get_asins_and_review_links(search_url)
    save_asins_to_csv(asins, review_links)
    print(f"Found {len(asins)} ASINs. Saved to CSV.")

    # Step 2: Scrape reviews for all ASINs and save to a single file
    if asins:
        for i, asin in enumerate(asins):
            print(f"\nScraping reviews for ASIN {i+1}/{len(asins)}: {asin}")
            try:
                reviews = get_reviews(asin)
                if reviews:
                    save_reviews_to_csv(reviews, all_reviews_filename)
                    print(f"Saved {len(reviews)} reviews for {asin}.")
                else:
                    print(f"No reviews found for {asin}.")
            except Exception as e:
                print(f"An error occurred while scraping reviews for {asin}: {e}")
            time.sleep(5)  # Add a delay to avoid getting blocked