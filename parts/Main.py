import spotify as sp
import Genius
import Sentiment_Analysis as SA
import Persist_Data

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


if __name__ == '__main__':
    playlist_Id = '37i9dQZF1DXcBWIGoYBM5M'
    spotify = sp.SpotifyAPI(sp.client_id, sp.client_secret)
    #this is also fed into the extract features
    #keep in mind that both names and ids call on get_playlist

    playlist = spotify.get_playlist(playlist_Id, limit=5)
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

    print(final_list)
    
    
    #here need to zip all the functions

    #get track features
    '''
    here it might be better if the extract features
    took in song_artist and sentiment list.

    It might also be better to have extract features 
    be its own thing again.

    So there is function that takes in the lists.
    -songartist
    -sentiment_list
    -featues list

    This way the spotify API servers two purposes it grabs the 
    songs and also extracts their features.


    '''
 
    
    SQL = Persist_Data.c
    addData = Persist_Data.InsertIntoTable
    #addData(sentiment_list)

    

    CertianScore = SQL.execute("SELECT * FROM TopSongs WHERE SentimentScore > 0.1 ")
    #print(SQL.fetchall())

    



#print(info(feedTheGenius))

#import json

#my_details = info(feedTheGenius)
 

#with open('sentiment_scores.json', 'w') as json_file:
#    json.dump(my_details, json_file)

  





#feedTheGenius= list(feedTheGenius)# [('Calling My Phone', 'Lil Tjay'), ('Goosebumps - Remix', 'Travis Scott'), ("We're Good", 'Dua Lipa')
#lyric_list = getLyrics(feedTheGenius) # returns a list of the lyrics

#print(lyric_list)