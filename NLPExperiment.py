import os, json
import lyricsgenius
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#Genius accces token: cQ15SgX_iCubNYTUW2pivTNrZbHmUIBHlzUHg2GEbDbrFUmzEVaRFE9BPvefe2io

#set GENIUS_ACCESS_TOKEN=cQ15SgX_iCubNYTUW2pivTNrZbHmUIBHlzUHg2GEbDbrFUmzEVaRFE9BPvefe2io
analyser = SentimentIntensityAnalyzer()

genius_access_token = os.environ['GENIUS_ACCESS_TOKEN']
geniusObject = lyricsgenius.Genius(genius_access_token)

song = geniusObject.search_song(title='Unbelievers', artist='Vampire Weekend')
print(song.lyrics)
annotations = geniusObject.song_annotations(song.id)
#print(json.dumps(annotations, sort_keys=True, indent=4))
#print(annotations)

sentiment_list = []
sentiment_score_list = []
print()
# for x in annotations:
#     sentiment_score = analyser.polarity_scores(x[0])
#     print('Lyric:', x[0], 'Score:', sentiment_score)


sentiment_score = analyser.polarity_scores(song.to_text())
print('Score:', sentiment_score)
