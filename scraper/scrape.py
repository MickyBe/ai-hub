import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup 
import time

def scrape_website(url):
    print("Launching Chrome browser...")
    chrome_driver_path = "scraper/chromedriver"
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless=new')  # Run headless for performance
    # options.add_argument('--disable-gpu')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(url)
        print("Page requested, waiting for DOM...")
        # Wait for the body tag to be present as a sign the page is loaded
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("Body loaded.")
        except Exception as e:
            print(f"Timeout waiting for page body: {e}")
        html = driver.page_source
        return html
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""
def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script","style"]):
        script_or_style.extract()
    
    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content

def split_dom_content(dom_content, max_line=6000):
    """
    Splits the dom_content string into chunks, each with at most max_line characters.
    Returns a list of string chunks.
    """
    return [dom_content[i:i+max_line] for i in range(0, len(dom_content), max_line)]
