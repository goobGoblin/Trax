# Adds albums and tracks from resident advisor to database. 
import os
import json
import pymysql

# Load database configuration
with open('../../config.JSON') as f:
    config = json.load(f)

def connect_to_db():
    """ Connect to the MySQL database and return the connection and cursor. """
    connection = pymysql.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=config['database'],
        port=config['port'],
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

def process_json_files(directory):
    """ Process each JSON file in the specified directory. """
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as file:
                albums = json.load(file)
                for album in albums:
                    process_album_entry(album)

def process_album_entry(album):
    """ Process a single album entry and update the database as needed. """
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            # Check if the artist exists
            cursor.execute("SELECT ArtistID FROM Artists WHERE name = %s", (album['Artist'],))
            artist = cursor.fetchone()
            if not artist:
                # Insert the artist if not found
                cursor.execute("INSERT INTO Artists (name) VALUES (%s)", (album['Artist'],))
                connection.commit()
                artist_id = cursor.lastrowid
            else:
                artist_id = artist['ArtistID']

            # Handle genres and labels before inserting the album
            genre_ids = []
            subgenre_ids = []
            for genre in album['Genre']:
                cursor.execute("SELECT GenreID FROM Genres WHERE name = %s", (genre['name'],))
                genre_entry = cursor.fetchone()

                if genre_entry:
                    # If the genre exists, add its ID to the list
                    genre_ids.append(genre_entry['GenreID'])
                else:
                    # If the genre does not exist, check if it's a known subgenre in the Subgenres table
                    cursor.execute("SELECT SubgenreID FROM Subgenres WHERE SubgenreName = %s", (genre['name'],))
                    subgenre_entry = cursor.fetchone()

                    if subgenre_entry:
                        # If it is a subgenre, use the SubgenreID to find the parent GenreID
                        cursor.execute("SELECT GenreID FROM GenreSubgenre WHERE SubgenreID = %s", (subgenre_entry['SubgenreID'],))
                        parent_genre_entry = cursor.fetchone()
                        if parent_genre_entry:
                            genre_ids.append(parent_genre_entry['GenreID'])
                            subgenre_ids.append(subgenre_entry['SubgenreID'])
                        else:
                            print(f"Parent genre not found for subgenre: {genre['name']}")
                    else:
                        # If no record exists, create a new "Other" genre if it does not exist
                        cursor.execute("SELECT GenreID FROM Genres WHERE name = 'Other'")
                        other_genre = cursor.fetchone()
                        if not other_genre:
                            cursor.execute("INSERT INTO Genres (name) VALUES ('Other')")
                            connection.commit()
                            other_genre_id = cursor.lastrowid
                        else:
                            other_genre_id = other_genre['GenreID']
                            
                        # Create a new subgenre for the unrecognized genre name
                        cursor.execute("INSERT INTO Subgenres (SubgenreName) VALUES (%s)", (genre['name'],))
                        connection.commit()
                        new_subgenre_id = cursor.lastrowid
                        subgenre_ids.append(new_subgenre_id)
                        
                        # Link the new subgenre to the "Other" genre
                        cursor.execute("INSERT INTO GenreSubgenre (GenreID, SubgenreID) VALUES (%s, %s)", (other_genre_id, new_subgenre_id))
                        connection.commit()
                        genre_ids.append(other_genre_id)

            label_ids = []
            for label in album['Labels']:
                cursor.execute("SELECT LabelID FROM Labels WHERE name = %s", (label['name'],))
                label_entry = cursor.fetchone()
                if not label_entry:
                    cursor.execute("INSERT INTO Labels (name) VALUES (%s)", (label['name'],))
                    connection.commit()
                    label_ids.append(cursor.lastrowid)
                else:
                    label_ids.append(label_entry['LabelID'])

            # Check if the album exists
            cursor.execute("SELECT AlbumID FROM Albums WHERE title = %s AND ArtistID = %s", (album['Title'], artist_id))
            album_entry = cursor.fetchone()
            # Insert the album if not found
            if not album_entry:
                cursor.execute(
                    "INSERT INTO Albums (title, ReleaseDate, ArtistID, blurb, recommended) VALUES (%s, %s, %s, %s, %s)",
                    (album['Title'], album['Date'], artist_id, album.get('Blurb'), album['Recommended'])
                )
                connection.commit()
                album_id = cursor.lastrowid  # Retrieve the ID of the newly inserted album correctly here

                # Linking genres and subgenres to the album
                for genre_id, subgenre_id in zip(genre_ids, subgenre_ids):
                    # First, check if this combination of AlbumID and GenreID already exists in AlbumGenres
                    cursor.execute("SELECT 1 FROM AlbumGenres WHERE AlbumID = %s AND GenreID = %s", (album_id, genre_id))
                    if not cursor.fetchone():
                        cursor.execute(
                            "INSERT INTO AlbumGenres (AlbumID, GenreID, SubgenreID) VALUES (%s, %s, %s)",
                            (album_id, genre_id, subgenre_id if subgenre_id else None)
                        )
                        connection.commit()
                    else:
                        print(f"Skip inserting duplicate AlbumGenres entry for AlbumID {album_id} and GenreID {genre_id}")


                # Linking labels to the album
                for label_id in label_ids:
                    # Check if the link between the album and label already exists
                    cursor.execute(
                        "SELECT 1 FROM AlbumLabels WHERE AlbumID = %s AND LabelID = %s",
                        (album_id, label_id)
                    )
                    if cursor.fetchone() is None:
                        # Only insert if the link does not already exist to prevent duplicate key error
                        cursor.execute(
                            "INSERT INTO AlbumLabels (AlbumID, LabelID) VALUES (%s, %s)",
                            (album_id, label_id)
                        )
                        connection.commit()


                # Now move on to inserting tracks
                tracklist = album['Tracklist']
                count_dash = sum(1 for track in tracklist[:3] if '-' in track)  # Count dashes in the first three tracks

                for track in tracklist:
                    if len(tracklist) >= 3 and count_dash >= 2 and '-' in track:
                        track_artist, track_title = track.split('-', 1)
                        track_artist = track_artist.strip()
                        track_title = track_title.strip()
                    else:
                        track_artist = album['Artist']  # Use the album's artist as default
                        track_title = track.strip()

                    cursor.execute("INSERT INTO Tracks (AlbumID, ArtistID, title) VALUES (%s, %s, %s)",
                                (album_id, artist_id, track_title))
                    connection.commit()

    finally:
        connection.close()

if __name__ == '__main__':
    directory = 'raScraper/album_scraper/Genres/ALBUM'  # Set the path to your JSON files directory
    process_json_files(directory)
