import pandas as pd
import os

def save_asins_to_csv(asins, review_links, filename="data/amazon_asins.csv"):
    """Saves a list of ASINs and their review links to a CSV file."""
    if not os.path.exists('data'):
        os.makedirs('data')
    df = pd.DataFrame({"ASIN": asins, "Review_Link": review_links})
    df.to_csv(filename, index=False)
    print(f"ASINs saved to {filename}")

def save_reviews_to_csv(reviews, filename="data/all_amazon_reviews.csv"):
    """
    Appends a list of review dictionaries to a single CSV file.
    If the file doesn't exist, it creates it with headers.
    """
    if not os.path.exists('data'):
        os.makedirs('data')
    
    df = pd.DataFrame(reviews)
    
    # Check if file exists to determine if we need to write the header
    file_exists = os.path.isfile(filename)
    
    # Use append mode ('a') and write header only if the file is new
    df.to_csv(filename, mode='a', header=not file_exists, index=False)
    print(f"Reviews appended to {filename}")