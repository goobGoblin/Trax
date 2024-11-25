#Name of artifact: Testing
#This is a testing script that gets equivalent data from recently 
# inserted tracks in the database
#Programmer: Harrison Reed
#Date: 11/24/2024
#Last Revision: 11/24/2024
#Preconditions: A argument is required to run the script,
#This is so the tester can choose to test either the spotify or soundcloud scraper
#Postconditions: The tracks from the database are written to a file for testing


import requests
from sclib import SoundcloudAPI, Track, Playlist
import pymysql
import json
import sys
import re

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

if __name__ == "__main__":
    
    #Clear the result file, incase we need new songs to check
    open('../data_handling/scripts/soundcloud/resultTrack2.txt', 'w').close()
    
    with connection.cursor() as cursor:
        #read the file and get the track id, to grab the track from the database
        with open('../data_handling/scripts/soundcloud/resultTrack.txt', 'r') as f:
            currentTrack = f.readlines()
            for line in currentTrack:
                thisLine = re.findall(r'\d+', line)
                if(len(thisLine) != 0):
                    cursor.execute("SELECT * FROM Tracks WHERE TrackID = %s", (thisLine[0]))
                    result = cursor.fetchall()
                    #write the result to a file
                    with open('../data_handling/scripts/soundcloud/resultTrack2.txt', 'a') as f:
                        f.write('\n' + str(result))
        pass