#Name of artifact: Scraper
#This is a scraper that grabs tracks from SoundCloud 
# and inserts them into the SQL database
#Programmer: Harrison Reed
#Date: 11/5/2024
#Last Revision: 11/24/2024 - Added file writing for testing
#Preconditions: A valid Soundcloud url is required for input, 
# if the user chooses to input a url
#Postconditions: The tracks from the Soundcloud url are inserted into the database,
#, and a file is created with the insertions for testing


import requests
from sclib import SoundcloudAPI, Track, Playlist
import pymysql
import json
import sys
import datetime
from datetime import timezone

#Base urls for regular checks on SoundCloud
urls =[ 'https://soundcloud.com/music-charts-us/sets/new-hot','https://soundcloud.com/music-charts-us/sets/hip-hop','https://soundcloud.com/music-charts-us/sets/country',
       'https://soundcloud.com/music-charts-us/sets/pop','https://soundcloud.com/music-charts-us/sets/rock', 'https://soundcloud.com/music-charts-us/sets/electronic', 
       'https://soundcloud.com/music-charts-us/sets/r-b', 'https://soundcloud.com/music-charts-us/sets/next-pro']

#Grab the config
with open('../config.JSON') as f:
    config = json.load(f)
    
#Connect to the database
connection = pymysql.connect(
    host=config['host'],
    user=config['user'],
    password=config['password'],
    database=config['database'],
    port=config['port'],
    cursorclass=pymysql.cursors.DictCursor
)

#Insert track inserts new tracks into the database
def insert_track(arr):

    #Grab the track and artist, this is to check if the track already exists
    track = "SELECT * FROM Tracks WHERE Title = %s"
    artist = "SELECT ArtistID FROM Artists WHERE Name = %s"
    
    with open('../data_handling/scripts/soundcloud/resultTrack.txt', 'w') as f:
        f.close()
    
    #Go through the database
    with connection.cursor() as cursor:
        cursor.execute(track, (arr[0],))
        trackResult = cursor.fetchone()
        cursor.execute(artist, (arr[1],))
        artistResult = cursor.fetchone()
        #checking if the track exists
        if trackResult is None:
            #insert when artist does not exist
            if artistResult is None:
                artist_sql = "INSERT INTO Artists (Name) VALUES (%s)"
                cursor.execute(artist_sql, (arr[1],))
                artist_id = cursor.lastrowid
                track_sql = "INSERT INTO Tracks (Title, ArtistID, Duration) VALUES (%s, %s, %s)"
                cursor.execute(track_sql, (arr[0], artist_id, arr[3]))
                track_id = cursor.lastrowid
                #Commit new tracks
                connection.commit()
                print(f"Inserted Track: {arr[0]} with ID: {track_id}")
                
                #Testing purposes
                #get the current date and time
                date = datetime.datetime.now(timezone.utc)
                #write the track to a file
                with open('../data_handling/scripts/soundcloud/resultTrack.txt', 'a') as f:
                    f.write(f"\n[{{'TrackID': {track_id}, 'Title': '{arr[0]}', 'Duration': {arr[3]}, 'AlbumID': None, 'ArtistID': {artist_id}, 'CreatedAt': datetime.datetime({date.year}, {date.month}, {date.day}, {date.hour}, {date.minute}, {date.second}), 'UpdatedAt': datetime.datetime({date.year}, {date.month}, {date.day}, {date.hour}, {date.minute}, {date.second}), 'GenreID': None}}]")
            #insert when artist exists
            else:
                track_sql = "INSERT INTO Tracks (Title, ArtistID, Duration) VALUES (%s, %s, %s)"
                cursor.execute(track_sql, (arr[0], artistResult['ArtistID'], arr[3]))
                track_id = cursor.lastrowid
                print(f"Inserted Track: {arr[0]} with ID: {track_id}")
                #commit the new track
                connection.commit()
                #Testing purposes
                #get the current date and time
                date = datetime.datetime.now(timezone.utc)
                #write the track to a file
                with open('../data_handling/scripts/soundcloud/resultTrack.txt', 'a') as f:
                    f.write(f"\n[{{'TrackID': {track_id}, 'Title': '{arr[0]}', 'Duration': {arr[3]}, 'AlbumID': None, 'ArtistID': {artistResult['ArtistID']}, 'CreatedAt': datetime.datetime({date.year}, {date.month}, {date.day}, {date.hour}, {date.minute}, {date.second}), 'UpdatedAt': datetime.datetime({date.year}, {date.month}, {date.day}, {date.hour}, {date.minute}, {date.second}), 'GenreID': None}}]")
        else:
            #track already exists, so nothing happens
            track_id = trackResult['TrackID']
            print(f"Found Existing Track: {arr[0]} with ID: {track_id}")
            
            thisDate1 = trackResult['CreatedAt']
            thisDate2 = trackResult['UpdatedAt']
            #Add the track to the file for testing
            with open('../data_handling/scripts/soundcloud/resultTrack.txt', 'a') as f:
                   f.write(f"\n[{{'TrackID': {track_id}, 'Title': '{arr[0]}', 'Duration': {arr[3]}, 'AlbumID': None, 'ArtistID': {artistResult['ArtistID']}, 'CreatedAt': datetime.datetime({thisDate1.year}, {thisDate1.month}, {thisDate1.day}, {thisDate1.hour}, {thisDate1.minute}, {thisDate1.second}), 'UpdatedAt': datetime.datetime({thisDate2.year}, {thisDate2.month}, {thisDate2.day}, {thisDate2.hour}, {thisDate2.minute}, {thisDate2.second}), 'GenreID': None}}]")
    pass


#main checks for input of in urls
if __name__ == "__main__":
    api = SoundcloudAPI()
    #if no input, check all urls
    if(len(sys.argv) < 2):
        for url in urls:
            playlist = api.resolve(url)
            assert type(playlist) is Playlist
            for track in playlist.tracks:
                temp = [track.title, track.artist, track.permalink_url, track.duration,track.genre]
                insert_track(temp)
                #[title, aritist, url, duration, genre]
    else:
        #check the input url
        playlist = api.resolve(sys.argv[1])
        assert type(playlist) is Playlist
        for track in playlist.tracks:
            temp = [track.title, track.artist, track.permalink_url, track.duration,track.genre]
            insert_track(temp)
    
    pass