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