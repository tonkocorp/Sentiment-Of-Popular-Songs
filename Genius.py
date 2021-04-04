
import lyricsgenius
import re 


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