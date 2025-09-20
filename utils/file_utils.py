import csv

def save_asins_to_csv(asins, links, filename="data/asins_links.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ASIN", "Review_Link"])
        for asin, link in zip(asins, links):
            writer.writerow([asin, link])
    print(f"✅ Saved {len(asins)} ASINs & links to {filename}")


def save_reviews_to_csv(reviews, filename):
    if not reviews:
        print("⚠️ No reviews to save.")
        return
    fieldnames = ["rating", "date", "body"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(reviews)
    print(f"✅ Saved {len(reviews)} reviews to {filename}")
