import logging
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib.parse
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver(relative_download_dir):
    logging.info("Setting up Firefox web driver.")
    try:
        options = FirefoxOptions()
        options.add_argument("--headless")  # Uncomment if you want the browser to be invisible
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", os.path.abspath(relative_download_dir))
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

        driver = webdriver.Firefox(options=options)
        return driver
    except Exception as e:
        logging.error(f"Error initializing WebDriver: {e}")

def search_mix(driver, mix_name):
    logging.info(f"Searching for mix: {mix_name}")
    encoded_mix_name = urllib.parse.quote(mix_name)
    search_url = f"https://trackid.net/audiostreams?keywords={encoded_mix_name}"
    logging.info(search_url)
    driver.get(search_url)
    time.sleep(2)

def select_top_result(driver):
    logging.info("Selecting mix\n")
    """ Select the top result from the search results by clicking the 'View' button in the first row of the table. """
    try:
        # Wait until the table of results is visible and then click the 'View' button in the first row
        view_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.MuiDataGrid-cellWithRenderer button[type='button']"))
        )
        view_button.click()
        logging.info("Navigating to the detailed mix page...")
        time.sleep(2)  # Wait for the detailed page to load
    except Exception as e:
        logging.info(f"Failed to select top result: {str(e)}")
        return None


def download_tracklist(driver):
    logging.info("Attempting to download the tracklist.")
    try:
        download_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "CSV"))
        )
        download_button.click()
        logging.info("Tracklist downloaded.")
    except Exception as e:
        logging.error(f"Download button not found: {str(e)}")

def main(mix_name, download_dir):
    driver = setup_driver(download_dir)
    search_mix(driver, mix_name)
    if select_top_result(driver):
        download_tracklist(driver)
    driver.quit()

if __name__ == "__main__":
    mix_name = "SonarMix 036"
    download_dir = "../../raw_data/Tracklists-CSV"
    main(mix_name, download_dir)
