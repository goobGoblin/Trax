from bs4 import BeautifulSoup
import requests
from sclib import SoundcloudAPI, Track, Playlist

urls =[ 'https://soundcloud.com/music-charts-us/sets/new-hot','https://soundcloud.com/music-charts-us/sets/hip-hop','https://soundcloud.com/music-charts-us/sets/country',
       'https://soundcloud.com/music-charts-us/sets/pop','https://soundcloud.com/music-charts-us/sets/rock', 'https://soundcloud.com/music-charts-us/sets/electronic', 
       'https://soundcloud.com/music-charts-us/sets/r-b', 'https://soundcloud.com/music-charts-us/sets/next-pro']

if __name__ == "__main__":
    scraped = []
    api = SoundcloudAPI()
    for url in urls:
        playlist = api.resolve(url)
        assert type(playlist) is Playlist
        for track in playlist.tracks:
            temp = [track.title, track.artist, track.permalink_url, track.duration,track.genre]
            scraped.append(temp)
            #[title, aritist, url, duration, genre]
    print(scraped)
    pass