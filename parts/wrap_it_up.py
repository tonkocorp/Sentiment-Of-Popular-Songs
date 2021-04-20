#topSongs = self.get_names_and_artists(playlist_id)
# take in the topSongs, and the Sentiment
def wrap_it_up(topSongs,Sentiment,audio_features):

    endpoint = f"{self.base_URL}audio-features?ids={track_ids}"
    audio_features = self.make_request(endpoint)
        

    track_names, artist_names = zip(*topSongs)

    energy = []
    danceability = []
    tempo = []
    key = []
    loudness = []
    mode = []
    speechiness = []
    acousticness = []
    instumentalness = []
    liveness = []
    duration_ms = []
    time_signature = []

    for x in audio_features['audio_features']:
        energy.append(x['energy'])
        danceability.append(x['danceability'])
        tempo.append(x['tempo'])
        key.append(x['key']) 
        loudness.append(x['loudness'])
        mode.append(x['mode'])
        speechiness.append(x['speechiness'])
        acousticness.append(x['acousticness'])
        instumentalness.append(x['instrumentalness'])
        liveness.append(x['liveness'])
        duration_ms.append(x['duration_ms'])
        time_signature.append(x['time_signature'])
            
        df = pd.DataFrame(list(zip(track_names,artist_names, energy, danceability, tempo, 
                                  key, loudness, mode, speechiness,acousticness,
                                  instumentalness, liveness, duration_ms, time_signature)), 
                         
        columns =['Track-Name','Artist','Energy', 'danceability','tempo', 
                         'key', 'loudness', 'mode', 'speechiness', 'acousticness', 
                         'instrumentalness', 'liveness', 'duration_ms', 'time_signature'])

        
        
    return df


  