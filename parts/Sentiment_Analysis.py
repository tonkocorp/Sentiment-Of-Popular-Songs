import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()   


# def sentiment(lyric_list): 
#     sentiment_list = [] 
#     for entry in lyric_list:
#         results = sia.polarity_scores(entry)["compound"]
#         sentiment_list.append(results)
#     return sentiment_list

# add something in here if did not return any lryics
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