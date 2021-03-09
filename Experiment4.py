import os, json
import lyricsgenius

#Genius accces token: cQ15SgX_iCubNYTUW2pivTNrZbHmUIBHlzUHg2GEbDbrFUmzEVaRFE9BPvefe2io

#set GENIUS_ACCESS_TOKEN=cQ15SgX_iCubNYTUW2pivTNrZbHmUIBHlzUHg2GEbDbrFUmzEVaRFE9BPvefe2io


genius_access_token = os.environ['GENIUS_ACCESS_TOKEN']
geniusObject = lyricsgenius.Genius(genius_access_token)

song = geniusObject.search_song(title='​we fell in love in october', artist='girl in red')
print(song.lyrics)
annotations = geniusObject.song_annotations(song.id)
#print(json.dumps(annotations, sort_keys=True, indent=4))
#print(annotations)
print()
for x in annotations:
    print(x[0], x[1])
