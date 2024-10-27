import requests
import json

URL = 'https://ra.co/graphql'
HEADERS = {
    'Content-Type': 'application/json',
    'Referer': 'https://ra.co',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
}

class NewsContainerFetcher:
    """
    A class to fetch and print various types of news articles based on filters.
    """

    def __init__(self, types, date_from, date_to, area_id, page_size=20, page=1):
        self.payload = self.load_and_generate_payload(types, date_from, date_to, area_id, page_size, page)

    def load_and_generate_payload(self, types, date_from, date_to, area_id, page_size, page):
        """
        Load the GraphQL query from a file and generate the payload with dynamic values.

        :return: The generated payload.
        """
        with open("mix_fetcher_template.json", "r") as file:
            payload = json.load(file)
            payload["variables"]["types"] = types
            payload["variables"]["dateFrom"] = date_from
            payload["variables"]["dateTo"] = date_to
            payload["variables"]["areaId"] = area_id
            payload["variables"]["pageSize"] = page_size
            payload["variables"]["page"] = page
            return payload

    def fetch_news(self):
        """
        Fetch news based on the set filters and return them.

        :return: A dictionary containing various sets of news data.
        """
        response = requests.post(URL, headers=HEADERS, json=self.payload)

        try:
            response.raise_for_status()
            data = response.json()
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Error: {str(e)}")
            return {}

        if 'data' not in data:
            print(f"Error in response data: {data}")
            return {}

        return data["data"]

    def print_news_details(self, news_data):
        """
        Print details of news articles from different categories.

        :param news_data: A dictionary containing various sets of news data.
        """
        for category in ['headlineNews', 'latestNews', 'popularNews']:
            print(f"--- {category.upper()} ---")
            for news in news_data.get(category, []):
                print(f"Title: {news['title']}")
                print(f"Date: {news['date']}")
                print(f"Blurb: {news['blurb']}")
                print(f"Type: {news['type']}")
                print(f"Content URL: {news['contentUrl']}")
                print("-" * 80)

# Example Usage
if __name__ == "__main__":
    news_fetcher = NewsContainerFetcher(
        types=["MIXOFTHEDAY"], 
        date_from="2024-01-01", 
        date_to="2024-01-31", 
        area_id="359"
    )
    news_data = news_fetcher.fetch_news()
    if news_data:
        news_fetcher.print_news_details(news_data)
