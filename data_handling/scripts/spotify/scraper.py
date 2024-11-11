import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from cryptography.fernet import Fernet


with open('spotify_key.key', 'rb') as key_file:
    key = key_file.read()    

print(key)
fernet = Fernet(key)

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
    print(sp.categories(country=None, locale=None, limit=20, offset=0))
    results = sp.current_user_saved_tracks()
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])