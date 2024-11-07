
import requests
from sclib import SoundcloudAPI, Track, Playlist
import pymysql
import json

urls =[ 'https://soundcloud.com/music-charts-us/sets/new-hot','https://soundcloud.com/music-charts-us/sets/hip-hop','https://soundcloud.com/music-charts-us/sets/country',
       'https://soundcloud.com/music-charts-us/sets/pop','https://soundcloud.com/music-charts-us/sets/rock', 'https://soundcloud.com/music-charts-us/sets/electronic', 
       'https://soundcloud.com/music-charts-us/sets/r-b', 'https://soundcloud.com/music-charts-us/sets/next-pro']

with open('../../../config.JSON') as f:
    config = json.load(f)
    

connection = pymysql.connect(
    host=config['host'],
    user=config['user'],
    password=config['password'],
    database=config['database'],
    port=config['port'],
    cursorclass=pymysql.cursors.DictCursor
)

def insert_track(arr):
    
    #insert track into database
    #check if track exists
    track = "SELECT TrackID FROM Tracks WHERE Title = %s"
    artist = "SELECT ArtistID FROM Artists WHERE Name = %s"
    with connection.cursor() as cursor:
        cursor.execute(track, (arr[0],))
        trackResult = cursor.fetchone()
        cursor.execute(artist, (arr[1],))
        artistResult = cursor.fetchone()
        if trackResult is None:
            #insert track
            
            #insert when artist does not exist
            if artistResult is None:
                artist_sql = "INSERT INTO Artists (Name) VALUES (%s)"
                cursor.execute(artist_sql, (arr[1],))
                artist_id = cursor.lastrowid
                track_sql = "INSERT INTO Tracks (Title, ArtistID, Duration) VALUES (%s, %s, %s)"
                cursor.execute(track_sql, (arr[0], artist_id, arr[3]))
                track_id = cursor.lastrowid
                print(f"Inserted Track: {arr[0]} with ID: {track_id}")
            #insert when artist exists
            else:
                track_sql = "INSERT INTO Tracks (Title, ArtistID, Duration) VALUES (%s, %s, %s)"
                cursor.execute(track_sql, (arr[0], artistResult['ArtistID'], arr[3]))
                track_id = cursor.lastrowid
                print(f"Inserted Track: {arr[0]} with ID: {track_id}")
        else:
            track_id = trackResult['TrackID']
            print(f"Found Existing Track: {arr[0]} with ID: {track_id}")
    pass

if __name__ == "__main__":
    scraped = []
    api = SoundcloudAPI()
    for url in urls:
        playlist = api.resolve(url)
        assert type(playlist) is Playlist
        for track in playlist.tracks:
            temp = [track.title, track.artist, track.permalink_url, track.duration,track.genre]
            #scraped.append(temp)
            insert_track(temp)
            #[title, aritist, url, duration, genre]
    print(scraped)
    pass