import pymysql
import json

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

with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM Tracks")
    result = cursor.fetchall()
    cursor.execute("SELECT * FROM Artists")
    result2 = cursor.fetchall()
    for track in result:
        print(track)
    for artist in result2:
        print(artist)
    pass