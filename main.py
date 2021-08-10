import os
import re
from tkinter import filedialog, Text
import logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def authenticate():
    try:
        clientId = open(os.path.join(os.getcwd)+'client_id', 'r')
        clientSecret = open(os.path.join(os.getcwd)+'client_secret', 'r')
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


def convert():
    fileToParse = selectFile()
    urls = []
    try:
        with open(fileToParse, 'r', encoding='utf8') as textFile:
            for line in textFile:
                if re.search(r"""https://open.spotify.com/track/""", line):
                    words = line.split()
                    for word in words:
                        if re.search(r"""^(https)""", word):
                            urls.append('spotify:track:' + word[31:53])
        if len(words) >= 1:
            print(urls)
            return words
        else:
            logging.error('No Track IDs found')
            return None
    except:
        logging.exception('Read file failed')

convert()
