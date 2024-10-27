# Adds Genres and Subgenres from JSON files to database
import os
import json
import pymysql

# Load database configuration
with open('../../config.JSON') as f:
    config = json.load(f)

# Connect to the database
connection = pymysql.connect(
    host=config['db_host'],
    user=config['db_user'],
    password=config['db_passwd'],
    database=config['db_database'],
    port=config['db_port'],
    cursorclass=pymysql.cursors.DictCursor
)

def handle_subgenre(cursor, subgenre, genre_id, parent_id=None):
    try:
        # Check if subgenre exists
        check_sql = "SELECT SubgenreID FROM Subgenres WHERE SubgenreName = %s"
        cursor.execute(check_sql, (subgenre['name'],))
        result = cursor.fetchone()

        if result is None:
            # Insert subgenre
            subgenre_sql = "INSERT INTO Subgenres (SubgenreName, Description) VALUES (%s, %s)"
            cursor.execute(subgenre_sql, (subgenre['name'], subgenre['description']))
            subgenre_id = cursor.lastrowid
            print(f"Inserted Subgenre: {subgenre['name']} with ID: {subgenre_id}")
        else:
            subgenre_id = result['SubgenreID']
            print(f"Found Existing Subgenre: {subgenre['name']} with ID: {subgenre_id}")

        # Link genre and subgenre
        link_sql = "INSERT INTO GenreSubgenre (GenreID, SubgenreID) VALUES (%s, %s)"
        cursor.execute(link_sql, (genre_id, subgenre_id))
        print(f"Linked Genre ID {genre_id} with Subgenre ID {subgenre_id}")

        connection.commit()

        # Handle nested subgenres
        if 'subgenres' in subgenre:
            for child in subgenre['subgenres']:
                handle_subgenre(cursor, child, genre_id, subgenre_id)

    except pymysql.err.IntegrityError as e:
        print(f"Database error during handling subgenre {subgenre['name']}: {str(e)}")
        connection.rollback()
    except Exception as e:
        print(f"An error occurred while handling subgenre {subgenre['name']}: {str(e)}")
        connection.rollback()

def main():
    directory_path = '../raw_data/Genres-JSON'  # Directory containing all JSON files
    json_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith('.json')]

    try:
        with connection.cursor() as cursor:
            for json_file in json_files:
                try:
                    with open(json_file, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        print(f"Processing file: {json_file}")

                        # Insert genre
                        genre_sql = "INSERT INTO Genres (Name, Description) VALUES (%s, %s)"
                        cursor.execute(genre_sql, (data['genre'], data['description']))
                        genre_id = cursor.lastrowid
                        connection.commit()
                        print(f"Inserted Genre: {data['genre']} with ID: {genre_id}")

                        # Process each subgenre
                        for subgenre in data['subgenres']:
                            handle_subgenre(cursor, subgenre, genre_id)

                except json.JSONDecodeError as e:
                    print(f"An error occurred processing file {json_file}: {e}")
                except Exception as e:
                    print(f"An error occurred: {str(e)}")
                    connection.rollback()

    finally:
        connection.close()

if __name__ == "__main__":
    main()
