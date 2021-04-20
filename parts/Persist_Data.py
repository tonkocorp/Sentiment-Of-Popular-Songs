import sqlite3
from datetime import date


t#test = [('Hold On', 'Justin Bieber', 0.056319565217391294), ('What’s Next', 'Drake', 0.09372375000000002), ('Selfish Love (with Selena Gomez)', 'DJ Snake', 0.2365323529411765), ('Save Your Tears', 'The Weeknd', 0.06771944444444444), ("We're Good", 'Dua Lipa', 0.31093)]

conn = sqlite3.connect('songs.db')
c = conn.cursor()

'''
c.execute("""CREATE TABLE TopSongs(
    Date text,
    Position integer,
    SongName text,
    Artist text,
    SentimentScore integer
    Energy integer
    Danceability integer
    Tempo integer
    Key integer
    Loudness integer
    Mode integer
    Speechiness integer
    Acousticness integer
    Instrumentalness integer
    Liveness integer
    Duration_ms integer
    Time_Signature  integer
)""")
'''



today = date.today()
today = today.strftime("%m/%d/%y")
def InsertIntoTable(list):
    position = 1
    
    for entry in list:
       c.execute("INSERT INTO TopSongs VALUES (:Date, :Position, :SongName, :Artist, :SentimentScore)",
       {'Date': today,'Position': position, 'SongName': entry[0], 'Artist': entry[1], 'SentimentScore': entry[2]
       'Energy': entry[3], 'Danceability':entry[4], 'Tempo':entry[5],
       'Key':entry[6], 'Loudness':entry[7], 'Mode': entry[8], 
       'Speechiness':entry[9], 'Acousticness':entry[10], 'Instrumentalness':entry[11],
       'Liveness':entry[11], 'Duration_ms': entry[12], 'Time_Signature':entry[13]})
       conn.commit()
       position+=1

    

#InsertIntoTable(test)

c.execute("SELECT * FROM TopSongs WHERE SentimentScore > 0.3 ")
#print(c.fetchall())

c.execute("SELECT * FROM TopSongs WHERE SentimentScore > 0.2 ")
#print(c.fetchall())

