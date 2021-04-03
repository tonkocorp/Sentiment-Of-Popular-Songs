import json
import lyricsgenius 

import base64
import requests
import datetime
import pandas as pd
from urllib.parse import urlencode
import re

''' 
THIS IS CLASS IS USED TO CONNCECT TO THE SPOTIFY-API
 '''

client_id ='1512cb0502974d278f30521744cf497f'
client_secret ='00849c1a47724711ac3294baaf3e4f96'

class SpotifyAPI(object):
    access_token = None
    access_token_expiration = datetime.datetime.now()
    access_token_expired = True
    client_id = None
    client_secret = None
    token_url = 'https://accounts.spotify.com/api/token'
    #the following are new
    base_URL = "https://api.spotify.com/v1/"
    

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs) #can call any class that it is inherting itself
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        #takes in client_id and client secret and return a base 64 encoded string
        client_id = self.client_id
        client_secret = self.client_secret
        if client_id == None or client_secret == None: # watch out fo this
            raise Exception("you forgot your client id or client secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode()) # encode
        return client_creds_b64.decode()


    def get_token_header(self):
        client_creds_b64 = self.get_client_credentials()
        return { 
            "Authorization" : f"Basic {client_creds_b64}"
            } #Basic <base64 encoded client_id:client_secret>

    def get_token_data(self):
        return {"grant_type":"client_credentials"}
    
    def perform_authorization(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_header() #calls the get client credentials method
        request = requests.post(token_url, data=token_data, headers=token_headers)
        if request.status_code not in range(200, 299):
            raise Exception("Could not Authenticate client")
            return False
        
        response = request.json()
        access_token = response['access_token']
        now = datetime.datetime.now()
        expires_in = response['expires_in'] #3600 seconds
        expires = now + datetime.timedelta(seconds=expires_in)# current time + 1 hour
        self.access_token = access_token
        self.access_token_expiration = expires
        self.access_token_expired = expires < now # once the current time passes expires
        return True

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expiration
        now = datetime.datetime.now()
        if expires < now: # token has expired
            self.perform_authorization()
            return self.get_access_token()
        elif token == None: # token does not exist
            self.perform_authorization()
            return self.get_access_token()
        return token 

    def get_resource_header(self):
       access_token = self.get_access_token()
       headers = {"Authorization": f"Bearer {access_token}"}
       return headers

    def make_request(self, endpoint):
        header = self.get_resource_header()
        r = requests.get(endpoint, headers = header) # can have this be its own function.
        if r.status_code not in range(200, 299):
            {}
        return r.json() # requests
   
    def get_playlist(self, playlist_id, limit=10, offset=0): # HOT100! 37i9dQZF1DXcBWIGoYBM5M
        endpoint = f"{self.base_URL}playlists/{playlist_id}/tracks?offset={str(offset)}&limit={str(limit)}"
        playlist = self.make_request(endpoint)
        
        return playlist
    
           
    def get_track_IDs(self, playlist_id, limit = 10, offset= 0 ): # the feature to add more than one song needs to be added here.
        playlist = self.get_playlist(playlist_id, limit=limit, offset=offset)
        track_ids = []
       
        for x in playlist['items']:
            track_ids.append(x['track']['id'])
         
        #super_ID = ','.join(track_ids) #THIS Feature needs to be moved to its own function
        
        return track_ids #, artist_names

    def get_names_and_artists(self, playlist_id, limit = 5, offset= 0 ): 
        playlist = self.get_playlistpip3 freeze > requirements.txt(playlist_id, limit=limit, offset=offset)
        track_names = []
        artist_names = [] 
        for x in playlist['items']:
            track_names.append(x['track']['name'])
            artist_names.append(x['track']['artists'][0]['name'])
        
        return zip(track_names, artist_names) 

    
    def extract_track_features(self, playlist_id):
        #consider getting the playlist first then passing it to functions.
        track_names, artist_names = self.get_names_and_artists(playlist_id)
        track_ids = self.get_track_IDs(playlist_id)
        #get the audio features for the track_ids extracted.
        endpoint = f"{self.base_URL}audio-features?ids={track_ids}"
        audio_features = self.make_request(endpoint)
        
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
    
    #def extract_audio_features(self, playlist_id):


spotify = SpotifyAPI(client_id, client_secret)

feedTheGenius = spotify.get_names_and_artists('37i9dQZF1DXcBWIGoYBM5M')
feedTheGenius= list(feedTheGenius)

print(feedTheGenius)


genius = lyricsgenius.Genius('o7wQ-YJ6Oxrl7o7oqagI3MkrTgDvfMcg0JahQdZU_DlUJuKbiEm7EkYS_ORcSVkn',
skip_non_songs=True, excluded_terms=[ "(Live)"], remove_section_headers=True)


#takes in a list of the top 10 artists and their songs
# the key needs to be the song name
#TopSongs = {"MotorSport": "Migos", "Heart of Gold": "Neil Young" }

def getLyrics(TopSongs):

    lyricList = []
    #add a method to check whether the song is alreadt in the pipeline
    for song, artist in TopSongs:

        no_good = '('

        if no_good in song:
            song = re.sub(r"\([^()]*\)", "", song)

        search = genius.search_song(f"{song}, {artist}")
        
        try:
            lyrics = search.lyrics
            lyricList.append(lyrics)
        except:
            print("That song does not contain any lyrics")
            lyricList.append(f"{song} by {artist}  did not return any lyrics")

    return lyricList

#---------------------------------------------------------------------------------------
#SENTIMENT ANALYSIS
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()   


# def sentiment(lyric_list): 
#     sentiment_list = [] 
#     for entry in lyric_list:
#         results = sia.polarity_scores(entry)["compound"]
#         sentiment_list.append(results)
#     return sentiment_list


def sentiment(lyric_list):
    sentiment_list = []
    for entry in lyric_list:
        split_entry = entry.split("\n")
        split_list_results = []
        #sentiment_list.append(Average(split_list_results))
        for w in split_entry:
            if w == '':
                continue
            else:
                results = sia.polarity_scores(w)["compound"]
                split_list_results.append(results) # i need to sum up results
        Average = sum(split_list_results)/ len(split_list_results) #get the average score
        sentiment_list.append(Average)
    return sentiment_list

def info(song_artists):
    lyric_list = getLyrics(feedTheGenius)  
    sentiment_list = sentiment(lyric_list) 

    song,artist = zip(*feedTheGenius)

    music_list=  zip(song, artist, sentiment_list)

    return list(music_list)

print(info(feedTheGenius))

#import json

#my_details = info(feedTheGenius)
 

#with open('sentiment_scores.json', 'w') as json_file:
#    json.dump(my_details, json_file)

  





#feedTheGenius= list(feedTheGenius)# [('Calling My Phone', 'Lil Tjay'), ('Goosebumps - Remix', 'Travis Scott'), ("We're Good", 'Dua Lipa')
#lyric_list = getLyrics(feedTheGenius) # returns a list of the lyrics

#print(lyric_list)


