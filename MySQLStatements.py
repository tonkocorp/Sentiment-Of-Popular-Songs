
selectAll = "SELECT * FROM TopSongs"

averageSentiment = "SELECT AVG(SentimentScore), Date FROM TopSongs GROUP BY Date "

tempoVersus = "SELECT DISTINCT SongName, Artist, Tempo ,SentimentScore FROM TopSongs "

intValues = ("SELECT Position, SentimentScore, Energy, Danceability, Tempo, Loudness, Mode, Speechiness,Acousticness, Instrumentalness ,Liveness ,Duration_ms ,Time_Signature FROM TopSongs")

position = "SELECT *FROM TopSongs ORDER BY DATE DESC LIMIT 10"

