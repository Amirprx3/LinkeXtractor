import logging
import requests
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException, StaleElementReferenceException # madeBy: #Amirprx3

# logging settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Cache for fetched script content
script_cache = {}

def initialize_driver(browser='firefox'):
    # Initialize the WebDriver.
    if browser == 'firefox':
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        try:
            driver = webdriver.Firefox(options=options)
            return driver
        except Exception as e:
            logger.error(f"Error initializing Firefox WebDriver: {e}")
            return None
    elif browser == 'chrome':
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        try:
            driver = webdriver.Chrome(options=options)
            return driver
        except Exception as e:
            logger.error(f"Error initializing Chrome WebDriver: {e}")
            return None
    elif browser == 'edge':
        options = webdriver.EdgeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        try:
            driver = webdriver.Edge(options=options)
            return driver
        except Exception as e:
            logger.error(f"Error initializing Edge WebDriver: {e}") # madeBy: #Amirprx3
            return None
    else:
        logger.error(f"Unsupported browser: {browser}")
        return None

def Banner(text):
    # Display banner text with neon effect.
    neon_colors = ["\033[1;30;40m", "\033[1;34;40m"]
    for char in text:
        print(neon_colors[0] + char, end="", flush=True)
        neon_colors.append(neon_colors.pop(0))
        time.sleep(0.001)
    print('\033[0m')

Banner("""
██╗     ██╗███╗   ██╗██╗  ██╗███████╗██╗  ██╗████████╗██████╗  █████╗  ██████╗████████╗ ██████╗ ██████╗ 
██║     ██║████╗  ██║██║ ██╔╝██╔════╝╚██╗██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
██║     ██║██╔██╗ ██║█████╔╝ █████╗   ╚███╔╝    ██║   ██████╔╝███████║██║        ██║   ██║   ██║██████╔╝
██║     ██║██║╚██╗██║██╔═██╗ ██╔══╝   ██╔██╗    ██║   ██╔══██╗██╔══██║██║        ██║   ██║   ██║██╔══██╗
███████╗██║██║ ╚████║██║  ██╗███████╗██╔╝ ██╗   ██║   ██║  ██║██║  ██║╚██████╗   ██║   ╚██████╔╝██║  ██║
╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
Github: https://github.com/Amirprx3
made by: Amirprx3
""")

def fetch_script_content(src, retries=3):
    # Fetch script content from a URL with retries and caching.
    if src in script_cache:
        return script_cache[src]

    for attempt in range(retries):
        try:
            response = requests.get(src, timeout=5)
            response.raise_for_status()
            script_cache[src] = response.text
            return response.text
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error fetching {src}: {e} (attempt {attempt + 1})")
            if attempt == retries - 1:
                return ""
        except Exception as e:
            logger.error(f"Unexpected error fetching {src}: {e}")
            return ""

def extract_links(content, regex):
    # Extract links using regex.
    return set(match.group(0) for match in re.finditer(regex, content))

def collect_links(driver, url):
    # Collect links from a URL.
    try:
        # Load the page
        driver.get(url)

        # Extract scripts from the page
        scripts = driver.find_elements(By.TAG_NAME, 'script')
        regex = r'(?<=(["\'`]))((https?:\/\/|\/)[\w\-./?=&%#]+)(?=\1)'
        results = set()

        # Process the content of all scripts
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(fetch_script_content, s.get_attribute('src')): s for s in scripts if s.get_attribute('src')} # madeBy: #Amirprx3
            for future in as_completed(futures):
                script_content = future.result()
                if script_content:
                    results.update(extract_links(script_content, regex))

        # Extract links from the page content
        page_content = driver.page_source
        results.update(extract_links(page_content, regex))

        return results
    except TimeoutException:
        logger.error(f"Error processing {url}: Timeout")
        return set()
    except StaleElementReferenceException:
        logger.error(f"Error processing {url}: Stale element reference")
        return set()
    except WebDriverException as e:
        logger.error(f"Error processing {url}: {e}")
        return set()
    except Exception as e:
        logger.error(f"Unexpected error processing {url}: {e}")
        return set()

def process_urls(driver, urls):
    # Process all URLs and save results.
    for url in urls:
        results = collect_links(driver, url)
        if results:
            domain = url.replace('https://', '').replace('http://', '').split('/')[0]
            filename = f"{domain}.txt"
            with open(filename, 'w', encoding='utf-8') as file:
                file.write("\n".join(results))
            logger.info(f"\033[1;32;40m[✓] Results saved to {filename}\033[0m")
        else:
            logger.info(f"\033[1;31;40m[✕] No links found for {url}\033[0m")

def quit_driver(driver, retries=3):
    # Quit the WebDriver with retries.
    for attempt in range(retries):
        try:
            driver.quit()
            return
        except Exception as e:
            logger.error(f"Error quitting WebDriver: {e} (attempt {attempt + 1})")
            if attempt == retries - 1:
                logger.error("Failed to quit WebDriver after multiple attempts.")

# main function
if __name__ == "__main__":
    browser_choice = input("[*]Enter the browser to use (firefox, chrome, edge): ").strip().lower()
    driver = initialize_driver(browser_choice)
    if not driver:
        logger.error("Failed to initialize WebDriver. Exiting.")
        exit(1)

    urls = []
    try:
        while True:
            url = input("[+]Enter the website URL (or type 'exit' to quit): ")
            if url.lower() == 'exit':
                break
            urls.append(url)
        process_urls(driver, urls)
    except KeyboardInterrupt:
        logger.info("\n[!] Exiting :(")
    finally:
        if driver:
            quit_driver(driver)
# madeBy: #Amirprx3
