# review_details.py
import requests
import json
import re

# Constants
URL = 'https://ra.co/graphql'
HEADERS = {
    'Content-Type': 'application/json',
    'Referer': 'https://ra.co',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
}

def fetch_album_details(review_id):
    with open('album_detail_template.json', 'r') as file:
        payload = json.load(file)
        payload['variables']['id'] = review_id

    response = requests.post(URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return extract_specific_details(response.json())
    else:
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")

def extract_specific_details(data):
    try:
        review = data['data']['review']
        
        # Safe extraction of genres
        genres = [{'name': g['name']} for g in review.get('genres', [])]

        # Safe extraction of labels
        labels = [{'name': l['name']} for l in review.get('labels', [])]

        # Safe extraction of artists
        artists = [{'name': a['name']} for a in review.get('artist', [])]

        # Advanced extraction of tracklist
        tracklist = review.get('tracklist', '').split('\n')
        cleaned_tracklist = []
        for line in tracklist:
            if re.search('[a-zA-Z]', line):  # Check if the line contains any letters
                # Remove non-letter characters before the first letter if the line starts with a non-letter
                if re.match('[^a-zA-Z]+', line):
                    # Remove all non-letter characters before the first letter
                    cleaned_line = re.sub('^[^a-zA-Z]+', '', line)
                    cleaned_tracklist.append(cleaned_line)
                else:
                    cleaned_tracklist.append(line.strip())
            else:
                # If no letters are present, keep the line as is
                cleaned_tracklist.append(line)

    except KeyError as e:
        # Handle cases where expected keys are missing in the JSON data
        print(f"Key error occurred: {e}")
        return {'error': f"Missing data for key: {e}"}
    except Exception as e:
        # Handle other unforeseen errors that may occur
        print(f"An error occurred: {e}")
        return {'error': str(e)}

    return {
        'genres': genres,
        'labels': labels,
        'tracklist': cleaned_tracklist,
        'artists': artists
    }
