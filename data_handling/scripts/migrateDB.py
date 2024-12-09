#Name of artifact: migrateDB
#THis is a script that migrates the SQL database to the Firebase database
#Programmer: Harrison Reed
#Date: 12/7/2024
#Last Revision: 12/7
#Preconditions: Authentication to the Firebase database is required, and a valid SQL database is required 
#Postconditions: The SQL database is migrated to the Firebase database

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pymysql
import json
import sys

#open firebase database
try:
    cred = credentials.Certificate(r"firebaseauth.json")
except:
    print("Error loading firebaseauth.json\nPlease make sure the file exists\nCheck out this video if your having trouble: https://www.youtube.com/watch?v=qsFYq_1BQdk\nExiting...")
    sys.exit(1)
firebase_admin.initialize_app(cred)

fireDB = firestore.client()
#open the SQL database
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

#get limit from command line
if(len(sys.argv) < 2):
    print("Usage python migrateDB.py <limit>")
    sys.exit(1)
limit = sys.argv[1]
print(f"Limit: {limit}")



with connection.cursor() as cursor:
    #Get all the tracks from the database
    if(int(limit) == 0):
        print("Getting all tracks")
        sql = "SELECT * FROM Tracks"
    else:
        sql = f"SELECT * FROM Tracks LIMIT {limit}"
    cursor.execute(sql)
    result = cursor.fetchall()
    for track in result:
        #Add the track to the firebase database
        print(track['Title'])
        if(fireDB.collection('Tracks').where('Title', '==', track['Title']).get()):
            print(f"Track: {track['Title']} already exists in Firebase")
            continue
        fireDB.collection('Tracks').add(track)
        print(f"Added Track: {track['Title']} to Firebase")
        
    #Get all the artists from the database
    sql = "SELECT * FROM Artists"
    cursor.execute(sql)
    result = cursor.fetchall()
    for artist in result:
        #Add the artist to the firebase database
        print(artist['Name'])
        if(fireDB.collection('Artists').where('Name', '==', artist['Name']).get()):
            print(f"Artist: {artist['Name']} already exists in Firebase")
            continue
        fireDB.collection('Artists').add(artist)
        print(f"Added Artist: {artist['Name']} to Firebase")
    
    #Get all the albums from the database
    sql = "SELECT * FROM Albums"
    cursor.execute(sql)
    result = cursor.fetchall()
    for album in result:
        #Add the album to the firebase database
        print(album['Title'])
        # print(album)
        if(fireDB.collection('Albums').where('Title', '==', album['Title']).get()):
            print(f"Album: {album['Title']} already exists in Firebase")
            continue
        result = {
            'Title': album['Title'],
            'ArtistID': album['ArtistID'],
            'ReleaseDate': album['ReleaseDate'].strftime('%Y-%m-%d'),
            'AlbumID': album['AlbumID'],
            'Description': album['blurb'],
            'CreatedAt': album['CreatedAt'],
            'UpdatedAt': album['UpdatedAt'],
            "Recommended": album['recommended'],
        }
        fireDB.collection('Albums').add(result)
        print(f"Added Album: {album['Title']} to Firebase")
    
    #Get all the genres from the database
    sql = "SELECT * FROM Genres"
    cursor.execute(sql)
    result = cursor.fetchall()
    for genre in result:
        #Add the genre to the firebase database
        print(genre['Name'])
        print(genre)
        if(fireDB.collection('Genres').where('Name', '==', genre['Name']).get()):
            print(f"Genre: {genre['Name']} already exists in Firebase")
            continue
        fireDB.collection('Genres').add(genre)
        print(f"Added Genre: {genre['Name']} to Firebase")
    
    #Get all the playlists from the database
    sql = "SELECT * FROM Playlists"
    cursor.execute(sql)
    result = cursor.fetchall()
    for playlist in result:
        #Add the playlist to the firebase database
        print(playlist['Name'])
        if(fireDB.collection('Playlists').where('Name', '==', playlist['Name']).get()):
            print(f"Playlist: {playlist['Name']} already exists in Firebase")
            continue
        fireDB.collection('Playlists').add(playlist)
        print(f"Added Playlist: {playlist['Name']} to Firebase")
    
    #get all the users from the database
    sql = "SELECT * FROM Users"
    cursor.execute(sql)
    result = cursor.fetchall()
    for user in result:
        #Add the user to the firebase database
        print(user['Username'])
        if(fireDB.collection('Users').where('Username', '==', user['Username']).get()):
            print(f"User: {user['Username']} already exists in Firebase")
            continue
        fireDB.collection('Users').add(user)
        print(f"Added User: {user['Username']} to Firebase")
    
    #get all the DJmixes from the database
    sql = "SELECT * FROM DJMixes"
    cursor.execute(sql)
    result = cursor.fetchall()
    for mix in result:
        #Add the mix to the firebase database
        print(mix['Name'])
        if(fireDB.collection('DJMixes').where('Name', '==', mix['Name']).get()):
            print(f"DJMix: {mix['Name']} already exists in Firebase")
            continue
        fireDB.collection('DJMixes').add(mix)
        print(f"Added DJMix: {mix['Name']} to Firebase")
    
    #get all the follows in the database
    sql = "SELECT * FROM Follows"
    cursor.execute(sql)
    result = cursor.fetchall()
    for follow in result:
        #Add the follow to the firebase database
        print(follow['UserID'])
        if(fireDB.collection('Follows').where('UserID', '==', follow['UserID']).get()):
            print(f"Follow: {follow['UserID']} already exists in Firebase")
            continue
        fireDB.collection('Follows').add(follow)
        print(f"Added Follow: {follow['UserID']} to Firebase")
    
    #get all the lables in the database
    sql = "SELECT * FROM Labels"
    cursor.execute(sql)
    result = cursor.fetchall()
    for label in result:
        #Add the label to the firebase database
        print(label['Name'])
        if(fireDB.collection('Labels').where('Name', '==', label['Name']).get()):
            print(f"Label: {label['Name']} already exists in Firebase")
            continue
        fireDB.collection('Labels').add(label)
        print(f"Added Label: {label['Name']} to Firebase")
   
    #get all the subgenres in the database
    sql = "SELECT * FROM Subgenres"
    cursor.execute(sql)
    result = cursor.fetchall()
    for subgenre in result:
        #Add the subgenre to the firebase database
        print(subgenre['SubgenreName'])
        if(fireDB.collection('Subgenres').where('Name', '==', subgenre['SubgenreName']).get()):
            print(f"Subgenre: {subgenre['SubgenreName']} already exists in Firebase")
            continue
        fireDB.collection('Subgenres').add(subgenre)
        print(f"Added Subgenre: {subgenre['SubgenreName']} to Firebase")
    pass