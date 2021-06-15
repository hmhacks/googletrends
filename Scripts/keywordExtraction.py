"""
This script parses text and generates a list of most frequent keywords.

Henry Manley - hjm67@cornell.edu -  Last Modified 5/25/2021
"""
from collections import Counter
import PyPDF2
import os

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

try:
    os.remove("../Data/fed2021.txt")
except Exception as e:
    print(e)
    pass


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

    stop = stopwords.words('english') + [',','.', '?', ':', ';', "'"] + ['doth', 'hath', 'thou', 'thy', 'thee', 'yet', 'thine']

    for i in stop:
        try:
            text_tokens = list(filter((i).__ne__, text_tokens))
        except:
            pass

    filtered = (" ").join(text_tokens)
    split_it = filtered.split()
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
        pageobj = pdfreader.getPage(page)
        text=pageobj.extractText()
        file=open(outfile,'w')
        file.writelines(text)

if __name__ == "__main__":
    parsePDF('../Data/fomc2021.pdf', "../Data/fed2021.txt")
    # fed = getKeywords("../Data/fed2021.txt", 20)
    shakespeare =getKeywords('../Data/shakespeare.txt', 20)
    # print(fed)
    print(shakespeare)
