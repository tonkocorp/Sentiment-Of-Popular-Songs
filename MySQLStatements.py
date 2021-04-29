
selectAll = "SELECT * FROM TopSongs"

averageSentiment = "SELECT AVG(SentimentScore) FROM TopSongs GROUP BY Day "

tempoVersus = "SELECT DISTINCT SongName, Artist, Tempo ,SentimentScore FROM TopSongs "