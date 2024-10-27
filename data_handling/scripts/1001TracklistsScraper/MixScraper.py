from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def scrape_tracklist_data(url):
    # Selenium setup: specify the path to chromedriver.
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    service = Service(executable_path='C:/Webdrivers/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        time.sleep(5)  # Let JavaScript load before scraping

        # Obtain page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract title if available
        title = soup.find("h1", class_="trackTitle").get_text(strip=True) if soup.find("h1", class_="trackTitle") else "Not Found"

        # Extract other details based on provided structure
        tl_date = soup.find(lambda tag: tag.name == "div" and "TL date" in tag.text)
        tl_date = tl_date.find_next_sibling("div").text if tl_date else "Not Found"

        posted_by = soup.find(lambda tag: tag.name == "div" and "Posted by" in tag.text)
        posted_by = posted_by.find_next_sibling("div").text if posted_by else "Not Found"

        posted_at = soup.find(lambda tag: tag.name == "div" and "Posted at" in tag.text)
        posted_at = posted_at.find_next_sibling("div").text if posted_at else "Not Found"

        views = soup.find(lambda tag: tag.name == "div" and "Views" in tag.text)
        views = views.find_next_sibling("div").text if views else "Not Found"

        likes = soup.find(lambda tag: tag.name == "div" and "Likes" in tag.text)
        likes = likes.find_next_sibling("div").text if likes else "Not Found"

        ided = soup.find(lambda tag: tag.name == "div" and "IDed" in tag.text)
        ided = ided.find_next_sibling("div").text if ided else "Not Found"

        duration = soup.find(lambda tag: tag.name == "div" and "Duration" in tag.text)
        duration = duration.find_next_sibling("div").text if duration else "Not Found"

        genres = soup.find(lambda tag: tag.name == "div" and "Genres" in tag.text)
        genres = genres.find_next_sibling("div").text if genres else "Not Found"

        # Extract track information
        tracks = soup.find_all("div", class_="track")
        track_list = [track.text.strip() for track in tracks]

        print(f"Title: {title}")
        print(f"TL Date: {tl_date}")
        print(f"Posted By: {posted_by}")
        print(f"Posted At: {posted_at}")
        print(f"Views: {views}")
        print(f"Likes: {likes}")
        print(f"IDed: {ided}")
        print(f"Duration: {duration}")
        print(f"Genres: {genres}")
        print("Tracks:")
        for track in track_list:
            print(track)

    except Exception as e:
        print(f"Error accessing page: {e}")
    finally:
        driver.quit()

# URL to scrape
url = "https://www.1001tracklists.com/tracklist/2sxtl0r1/ben-klock-bassiani-invites-podcast-200-2024-02-13.html"
scrape_tracklist_data(url)
