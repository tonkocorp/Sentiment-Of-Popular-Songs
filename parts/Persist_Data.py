import sqlite3
from datetime import date

test = [('Hold On', 'Justin Bieber', 0.056319565217391294), ('What’s Next', 'Drake', 0.09372375000000002), ('Selfish Love (with Selena Gomez)', 'DJ Snake', 0.2365323529411765), ('Save Your Tears', 'The Weeknd', 0.06771944444444444), ("We're Good", 'Dua Lipa', 0.31093)]

conn = sqlite3.connect('songs.db')
c = conn.cursor()

'''
c.execute("""CREATE TABLE TopSongs(
    Date text,
    Position integer,
    SongName text,
    Artist text,
    SentimentScore integer
)""")
'''



today = date.today()
today = today.strftime("%m/%d/%y")
def InsertIntoTable(list):
    position = 1
    
    for entry in list:
       c.execute("INSERT INTO TopSongs VALUES (:Date, :Position, :SongName, :Artist, :SentimentScore)",
       {'Date': today,'Position': position, 'SongName': entry[0], 'Artist': entry[1], 'SentimentScore': entry[2]})
       conn.commit()
       position+=1

    

#InsertIntoTable(test)

c.execute("SELECT * FROM TopSongs WHERE SentimentScore > 0.3 ")
#print(c.fetchall())

c.execute("SELECT * FROM TopSongs WHERE SentimentScore > 0.2 ")
#print(c.fetchall())

