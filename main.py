import os
import re
from tkinter import filedialog, Text
import logging


def selectFile():
    try:
        fileName = filedialog.askopenfilename(initialdir='/',
                title='Select chatlog text file',
                filetypes=(('Text File', '*.txt'), ))
        return fileName
    except:
        logging.exception('Failed to select file')


def convert():
    folderPath = ''
    fileToConvert = selectFile()
    urls = []
    try:
        with open(fileToConvert, 'r', encoding='utf8') as textFile:
            for line in textFile:
                if re.search(r"""https://open.spotify.com/track/""", line):
                    words = line.split()
                    for word in words:
                        if re.search(r"""^(https)""", word):
                            urls.append(word[31:53])
                            print("Found match")
        print(urls)
    except:
        logging.exception('Read file failed')

convert()
