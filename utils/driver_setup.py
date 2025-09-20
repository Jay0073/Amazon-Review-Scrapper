from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument(r"--user-data-dir=C:\chrome-profile")
    driver_path = r"C:\webdriver\chromedriver.exe"
    service = Service(executable_path=driver_path)
    return webdriver.Chrome(service=service, options=chrome_options)
