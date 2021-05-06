import spotify as sp
import Genius
import Sentiment_Analysis as SA
import Persist_Data

import pandas as pd


def wrap_it_up(songs_and_artists, sentiment_list, song_features):
    
    print(len(sentiment_list))
    
    #print(list(song_features))
    #song_features = song_features

    song, artist = zip(*songs_and_artists)
    #print(list(song))
    print(len(song))
    


    (energy, danceability, tempo, 
    key, loudness, mode, 
    speechiness,acousticness,instumentalness, 
    liveness, duration_ms, time_signature) = zip(*song_features)

    music_list=  zip(song, artist, sentiment_list, 
    energy, danceability, tempo, 
    key, loudness, mode, 
    speechiness,acousticness,
    instumentalness, liveness, duration_ms, 
    time_signature)

    return list(music_list)

def main():
    playlist_Id = '37i9dQZF1DXcBWIGoYBM5M'
    spotify = sp.SpotifyAPI(sp.client_id, sp.client_secret)
    #this is also fed into the extract features
    #keep in mind that both names and ids call on get_playlist

    playlist = spotify.get_playlist(playlist_Id, limit=10)
    #print(playlist)
    songs_and_artists1 = spotify.get_names_and_artists(playlist)
    songs_and_artists2 = spotify.get_names_and_artists(playlist)
    #print(list(songs_and_artists))
    track_ids = spotify.get_track_IDs(playlist)
    
    song_features = spotify.extract_track_features(track_ids)
    


    #get song lyrics
    song_lyrics = Genius.get_lyrics(songs_and_artists2)
    #feed lyrics into Sentiment list
    song_sentiment = SA.sentiment(song_lyrics)

    #print(list(songs_and_artists2))
    #print(list(song_features))

    final_list = wrap_it_up(songs_and_artists1, song_sentiment, song_features)

    #-----------------------------------------------------------
    #DATABASE
    #print(final_list)
  
    addData = Persist_Data.InsertIntoTable(final_list)

    conn = Persist_Data.conn
    c = Persist_Data.c

    #check for duplicates

    duplicates = pd.read_sql_query("SELECT SongName, Date, COUNT(*) as Count FROM TopSongs GROUP BY SongName, Date HAVING COUNT(*) > 1",conn)
    print(duplicates)


    df = pd.read_sql_query("SELECT * FROM TopSongs", conn)
    print(df)

import time
one_minute = 86400

if __name__ == '__main__':
    
    while True:
        start = time.time()
        main()
        stop = time.time()
        elapsed = stop - start
        time.sleep(one_minute - elapsed)
    



    

    
    # get SQLite to output a pandas dataframe.
    #CertianScore = SQL.execute("SELECT * FROM TopSongs WHERE SentimentScore > 0.1 ")
    #print(SQL.fetchall())

    