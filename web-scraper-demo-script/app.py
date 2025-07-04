import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse

options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_argument("--start-maximized")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.set_page_load_timeout(20)

urls = [
    "https://www.moodys.com/web/en/us/insights/data-stories/apac-power-carbon-transition.html",
    "https://www.ft.com/",
    "https://www.scribd.com/",
    "https://www.moodys.com/",
    "https://www.netflix.com/"
]

output_folder = "./web-scraper-demo/scraped_pages"
os.makedirs(output_folder, exist_ok=True)

try:
    for url in urls:
        print(f"Fetching {url} with standard Selenium...")
        try:
            driver.get(url)

            time.sleep(2)

            full_html = driver.page_source

            parsed_url = urlparse(url)
            website_name = parsed_url.netloc.split('.')[-2]
            filename = f"{website_name}_full.html"
            full_path = os.path.join(output_folder, filename)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(full_html)

            print(f"✅ Full HTML saved to {full_path}")

        except TimeoutException:
            print(f"❌ Timed out loading {url}. Moving to the next one.")

finally:
    driver.quit()
    print(f"\nAll tasks complete. Files saved in '{output_folder}' folder.")