"""
This script parses text and generates a list of most frequent keywords.

Henry Manley - hjm67@cornell.edu -  Last Modified 5/25/2021
"""
from collections import Counter
import urllib.request
import PyPDF2
import os
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def getKeywords(file, num):
    """
    Returns a list of sorted num keywords from file.

    @param file is a .txt to extract keywords from.
    @param num is the number of keywords to return
    """

    with open(file, 'r') as file:
        text = file.read().replace('\n', '')

    text_tokens = word_tokenize(text)
    text_tokens = [x.lower() for x in text_tokens]

    stop = stopwords.words('english') + [',','.', '?', ':', ';', "'", ')', '(', '$', '']
    stop = stop + ['doth', 'hath', 'thou', 'thy', 'thee', 'yet', 'thine']

    for i in stop:
        try:
            text_tokens = list(filter((i).__ne__, text_tokens))
        except:
            pass

    filtered = (" ").join(text_tokens)
    split_it = filtered.split()
    split_it = [word for word in split_it if len(word) > 2]
    split_it = [word for word in split_it if re.match(r'^-?\d+(?:\.\d+)$', word) is None]

    count = Counter(split_it)
    most_occur = count.most_common(num)
    most_occur = [x[0] for x in most_occur]
    return most_occur


def parsePDF(infile, outfile):
    """
    Procedure that parses a pdf file and creates a .txt file
    from it.

    @param infile is the PDF path to parse.
    @param outfile is the .txt path to write to
    """
    pdf=open(infile,'rb')
    pdfreader=PyPDF2.PdfFileReader(pdf)
    numPages = pdfreader.numPages

    if pdfreader.isEncrypted:
        pdfreader.decrypt('')

    for page in range(numPages):
        print(page)
        pageobj = pdfreader.getPage(page)
        text=pageobj.extractText()
        with open(outfile,'a') as file:
            file.write(text)



def getTexts(url, outfile):
    """
    Downloads file from specified url to local memory.

    @param url is the url to download data from.
    @param outfile is the path to write to. Extension must match file type.
    """
    urllib.request.urlretrieve(url, outfile)


if __name__ == "__main__":
    parsePDF('../Data/FOMC20210127.pdf', "../Data/fed2021.txt")
    fedTest = getKeywords('../Data/fed2021.txt', 20)
    print(fedTest)
    os.remove('../Data/fed2021.txt')
