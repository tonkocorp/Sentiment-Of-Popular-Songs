import spotify as sp
import Genius
import Sentiment_Analysis as SA
import Persist_Data

def info(song_artists):
    lyric_list = Genius.getLyrics(feedTheGenius)  
    sentiment_list = SA.sentiment(lyric_list) 

    song,artist = zip(*feedTheGenius)

    music_list=  zip(song, artist, sentiment_list)

    return list(music_list)


if __name__ == '__main__':
    playlist_Id = '37i9dQZF1DXcBWIGoYBM5M'
    #get
    spotify = sp.SpotifyAPI(sp.client_id, sp.client_secret)

    songs_artist = spotify.get_names_and_artists(playlist_Id)
    feedTheGenius = list(songs_artist)

    sentiment_list = info(feedTheGenius)
    #print features
    track_features = spotify.extract_track_features(playlist_Id)
    print(track_features)
    SQL = Persist_Data.c
    addData = Persist_Data.InsertIntoTable
    addData(sentiment_list)

    

    CertianScore = SQL.execute("SELECT * FROM TopSongs WHERE SentimentScore > 0.1 ")
    print(SQL.fetchall())

    



#print(info(feedTheGenius))

#import json

#my_details = info(feedTheGenius)
 

#with open('sentiment_scores.json', 'w') as json_file:
#    json.dump(my_details, json_file)

  





#feedTheGenius= list(feedTheGenius)# [('Calling My Phone', 'Lil Tjay'), ('Goosebumps - Remix', 'Travis Scott'), ("We're Good", 'Dua Lipa')
#lyric_list = getLyrics(feedTheGenius) # returns a list of the lyrics

#print(lyric_list)