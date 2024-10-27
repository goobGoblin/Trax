import requests
from fake_headers import Headers
from bs4 import BeautifulSoup

def get_soup(url):
    """ Retrieve HTML and return a BeautifulSoup object """
    try:
        response = requests.get(url, headers=Headers().generate())
        response.raise_for_status()  # This will raise an exception for HTTP error codes
        soup = BeautifulSoup(response.text, "html.parser")
        if "Error 403" in soup.title.text:
            raise Exception("Error 403: Captcha or Forbidden access encountered: https://www.1001tracklists.com/")
        return soup
    except requests.RequestException as e:
        raise Exception(f"Failed to retrieve data from {url}. Reason: {str(e)}")

def get_json(url):
    """ Retrieve JSON from a URL """
    try:
        response = requests.get(url, headers=Headers().generate())
        response.raise_for_status()  # Checks if the request returned an HTTP error
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"Failed to retrieve JSON from {url}. Reason: {str(e)}")
