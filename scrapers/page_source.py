from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_page_source(product_id):
    """
    Opens the Amazon reviews page, waits for user input, and then saves
    the complete page source HTML to a file for manual inspection.
    """
    chrome_options = Options()
    chrome_options.add_argument(r"--user-data-dir=C:\chrome-profile")
    driver_path = r"C:\webdriver\chromedriver.exe"
    service = Service(executable_path=driver_path)

    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return

    start_url = "https://www.amazon.in/s?k=laptops+under+50k"
    
    print("Attempting to navigate to the URL...")
    driver.get(start_url)
    print("Navigation command sent. The page should now be loading.")
    
    input("--> SCRIPT PAUSED: Wait for the review page to fully load in the browser, then press Enter here to save the HTML...")

    # --- SAVE THE FULL PAGE SOURCE ---
    print("Saving the page source...")
    page_source = driver.page_source
    with open("data/amazon_page_source.html", "w", encoding="utf-8") as f:
        f.write(page_source)

    print("\nSuccessfully saved the complete HTML to 'data/amazon_page_source.html'.")
    print("You can now close the script.")
    
    driver.quit()


if __name__ == "__main__":
    product_id_to_scrape = 'B0F3NQFQTY' 
    get_page_source(product_id_to_scrape)

