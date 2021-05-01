
selectAll = "SELECT * FROM TopSongs"

averageSentiment = "SELECT AVG(SentimentScore), Date FROM TopSongs GROUP BY Date "

tempoVersus = "SELECT DISTINCT SongName, Artist, Tempo ,SentimentScore FROM TopSongs "