import os
import re
from tkinter import filedialog, Text
import logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

playlist_id = "playlist_id_goes_here"
getUrl = "/v1/playlists/{playlist_id}/tracks"
postUrl = "	/v1/playlists/{playlist_id}/tracks"
sp

def authenticate():
    try:
        clientId = open(os.path.join(os.getcwd)+'client_id', 'r')
        clientSecret = open(os.path.join(os.getcwd)+'client_secret', 'r')
        global sp
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=clientId, client_secret=clientSecret))
    except:
        logging.exception('Failed to authenticate')

def selectFile():
    try:
        fileName = filedialog.askopenfilename(initialdir='/',
                title='Select chatlog text file',
                filetypes=(('Text File', '*.txt'), ))
        return fileName
    except:
        logging.exception('Failed to select file')

def getExistingUris():
    try:
        return sp.playlist_tracks(playlist_id)
    except:
        logging.exception('Get request failed')

def updatePlaylist(newUris):
    try:
        sp.playlist_add_items(playlist_id, newUris, "end")
    except:
        logging.exception('Post request failed')

def findNewUris(fileToParse, existingUris):
    newUris = []
    try:
        with open(fileToParse, 'r', encoding='utf8') as textFile:
            for line in textFile:
                if re.search(r"""https://open.spotify.com/track/""", line):
                    words = line.split()
                    for word in words:
                        if re.search(r"""^(https)""", word):
                            uri = 'spotify:track:' + word[31:53]
                            if (uri not in existingUris):
                                newUris.append(uri)
    except:
        logging.exception('Read file failed')

def run():
    authenticate()
    fileToParse = selectFile()
    existingUris = getExistingUris()
    newUris = findNewUris(fileToParse, existingUris)
    if len(newUris) >= 1:
        print(newUris)
        updatePlaylist(newUris)
    else:
        logging.error('No new Track IDs found')
        return None

run()
 