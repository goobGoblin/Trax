#Name of artifact: fireBaseUpdateLinks
#This is a script that updates the links(i.e. the references to other documents in the database) in the firebase database
#Programmer: Harrison Reed
#Date: 12/7/2024
#Last Revision: 12/7/2024
#Preconditions: A valid firebase database/auth.json file is required
#Postconditions: The links in the database are updated

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pymysql
import json

#open firebase database
cred = credentials.Certificate(r"firebaseauth.json")
firebase_admin.initialize_app(cred)

fireDB = firestore.client()

tracks = fireDB.collection('Tracks').stream()


#Update the tracks in the database
for track in tracks:
    trackID = track.id
    track = track.to_dict()
    print(trackID)
    try:
        #Update the ArtistID
        if "ArtistID" in track:
            artistResult = fireDB.collection('Artists').where('ArtistID', '==', track['ArtistID']).get()
            if(artistResult):
                #grab the reference to the artist
                artistResult = fireDB.collection('Artists').document(artistResult[0].id)
                track['ArtistID'] = artistResult
                print(track)
                fireDB.collection('Tracks').document(trackID).set(track)
                print(f"Updated Track: {track['Title']}")
        
        #Update the LabelID        
        if track["AlbumID"] is not None:
            albumResult = fireDB.collection('Albums').where('AlbumID', '==', track['AlbumID']).get()
            if(albumResult):
                #grab the reference to the album
                albumResult = fireDB.collection('Albums').document(albumResult[0].id)
                track['AlbumID'] = albumResult
                print(track)
                fireDB.collection('Tracks').document(trackID).set(track)
                print(f"Updated Track: {track['Title']}")
        
        #Update the GenreID    
        if track["GenreID"] is not None:
            genreResult = fireDB.collection('Genres').where('GenreID', '==', track['GenreID']).get()
            if(genreResult):
                #grab the reference to the genre
                genreResult = fireDB.collection('Genres').document(genreResult[0].id)
                track['GenreID'] = genreResult
                print(track)
                fireDB.collection('Tracks').document(trackID).set(track)
                print(f"Updated Track: {track['Title']}")
    except:
        print(f"Error updating Track: {track['Title']}")

DJMixes = fireDB.collection('DJMixes').stream()            
#Update DJMixes in the database            
for mix in DJMixes:
    mixID = mix.id
    mix = mix.to_dict()
    print(mixID)
    try:
        #Update the ArtistID
        if "ArtistID" in mix:
            artistResult = fireDB.collection('Artists').where('ArtistID', '==', mix['ArtistID']).get()
            if(artistResult):
                #grab the reference to the artist
                artistResult = fireDB.collection('Artists').document(artistResult[0].id)
                mix['ArtistID'] = artistResult
                print(mix)
                fireDB.collection('DJMixes').document(mixID).set(mix)
                print(f"Updated DJMix: {mix['Title']}")
        
        #Update the LabelID
        if mix["LabelID"] is not None:
            labelResult = fireDB.collection('Labels').where('LabelID', '==', mix['LabelID']).get()
            if(labelResult):
                #grab the reference to the label
                labelResult = fireDB.collection('Labels').document(labelResult[0].id)
                mix['LabelID'] = labelResult
                print(mix)
                fireDB.collection('DJMixes').document(mixID).set(mix)
                print(f"Updated DJMix: {mix['Title']}")
        
        #Update the GenreID        
        if mix["GenreID"] is not None:
            genreResult = fireDB.collection('Genres').where('GenreID', '==', mix['GenreID']).get()
            if(genreResult):
                #grab the reference to the genre
                genreResult = fireDB.collection('Genres').document(genreResult[0].id)
                mix['GenreID'] = genreResult
                print(mix)
                fireDB.collection('DJMixes').document(mixID).set(mix)
                print(f"Updated DJMix: {mix['Title']}")
    except:
        print(f"Error updating DJMix: {mix['Title']}")
            
albums = fireDB.collection('Albums').stream()
#Update Albums in the database
for album in albums:
    albumID = album.id
    album = album.to_dict()
    try:
        #Update the ArtistID
        if album["LabelID"] is not None:
            labelResult = fireDB.collection('Labels').where('LabelID', '==', album['LabelID']).get()
            if(labelResult):
                #grab the reference to the label
                labelResult = fireDB.collection('Labels').document(labelResult[0].id)
                album['LabelID'] = labelResult
                print(album)
                fireDB.collection('Albums').document(albumID).set(album)
                print(f"Updated Album: {album['Title']}")
        #Update the GenreID        
        if album["GenreID"] is not None:
            genreResult = fireDB.collection('Genres').where('GenreID', '==', album['GenreID']).get()
            if(genreResult):
                #grab the reference to the genre
                genreResult = fireDB.collection('Genres').document(genreResult[0].id)
                album['GenreID'] = genreResult
                print(album)
                fireDB.collection('Albums').document(albumID).set(album)
                print(f"Updated Album: {album['Title']}")
    except:
        print(f"Error updating Album: {album['Title']}")

pass