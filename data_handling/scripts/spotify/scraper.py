import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from cryptography.fernet import Fernet
import pymysql
import json


urls = ["https://open.spotify.com/playlist/6UeSakyzhiEt4NB3UAd6NQ?si=5fd771417e344cf8",
        "https://open.spotify.com/playlist/451GSg2HhxCae2mXr4hQU1?si=063136e1d27d4047", 
        "https://open.spotify.com/playlist/37i9dQZF1EVHGWrwldPRtj?si=5e85bf087db64794",
        "https://open.spotify.com/playlist/7HP1rgWfJcGKHYCFt0cnYH?si=87c51e17b3a74ddd",
        "https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd?si=a5b5f1d8240a4e3d"]

with open('spotify_key.key', 'rb') as key_file:
    key = key_file.read()    

print(key)
fernet = Fernet(key)



with open('config.JSON') as f:
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
                connection.commit()
                print(f"Inserted Track: {arr[0]} with ID: {track_id}")
            #insert when artist exists
            else:
                track_sql = "INSERT INTO Tracks (Title, ArtistID, Duration) VALUES (%s, %s, %s)"
                cursor.execute(track_sql, (arr[0], artistResult['ArtistID'], arr[3]))
                track_id = cursor.lastrowid
                print(f"Inserted Track: {arr[0]} with ID: {track_id}")
                connection.commit()
        else:
            track_id = trackResult['TrackID']
            print(f"Found Existing Track: {arr[0]} with ID: {track_id}")
    pass


if __name__ == '__main__':
    
    print(os.getcwd())
    
    with open("/mnt/g/EECS 581/Project 3/data_handling/scripts/spotify/credentials.txt", "rb") as f:
        credentials = f.read()
        
    credentialsDE = fernet.decrypt(credentials)
    credentialsDE = credentialsDE.split(b'\n')
    
    for i in range(len(credentialsDE)):
        currentCred = credentialsDE[i].split(b'='b'\'')
        envVar = currentCred[0].split(b"export")
        envVar = envVar[1].decode('utf-8')
        envVar = envVar.replace(" ", "")
        setVar = currentCred[1].split(b'\'')
        setVar = setVar[0].decode('utf-8')
        os.environ[envVar] = setVar
        
    scope = "user-library-read"
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    #print(sp.categories(country=None, locale=None, limit=20, offset=0))
    for url in urls:
        results = sp.playlist(url)
        results = results['tracks']
    
        for idx, item in enumerate(results['items']):
            track = item['track']
            temp = [track['name'], track['artists'][0]['name'], track['external_urls']['spotify'], track['duration_ms']]
            insert_track(temp)