"""
This script parses text and generates a list of most frequent keywords.

Henry Manley - hjm67@cornell.edu -  Last Modified 5/25/2021
"""
from collections import Counter
import urllib.request
import PyPDF2
import os
import pickle
import re

from itertools import chain
import gensim
from gensim import corpora, models
from nltk.corpus import stopwords, wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer

def getKeywords(file, num, LDA=False):
    """
    Returns a list of sorted num keywords from file.

    @param file is a .txt to extract keywords from.
    @param num is the number of keywords to return
    @param LDA is True if this function is to return the preprocessed
    text, as opposed to the num most frequent keywords.
    """

    with open(file, 'r') as file:
        text = file.read().replace('\n', '')

    text_tokens = word_tokenize(text)
    text_tokens = [x.lower() for x in text_tokens]

    stop = stopwords.words('english') + [',','.', '?', ':', ';', "'", ')', '(', '$', '', '_']
    stop = stop + ['doth', 'hath', 'thou', 'thy', 'thee', 'yet', 'thine']

    for i in stop:
        try:
            text_tokens = list(filter((i).__ne__, text_tokens))
        except:
            pass

    filtered = (" ").join(text_tokens)
    split_it = filtered.split()
    split_it = [word for word in split_it if len(word) > 2]
    split_it = [word for word in split_it if not any(c.isdigit() for c in word)]
    split_it = [word for word in split_it if re.match(r'^-?\d+(?:\.\d+)$', word) is None]
    new = []
    [new.append(word) for word in split_it if word not in new]
    split_it = new
    split_it = [word.replace('-','') for word in split_it]

    if LDA:
        return split_it

    count = Counter(split_it)
    most_occur = count.most_common(num)
    most_occur = [x[0] for x in most_occur]
    return most_occur


def LDA(texts, topics, words):
    """
    Returns a list of words generated from topic modeling.

    Given tokenized and lemmatized text, return a parameterized number of LDA-based
    topics. From these topics, return n feature words.

    @param texts is a raw text file that gets tokenized and lemmatized via getKeywords()
    @param texts is the number of topics to return
    @param words is the number of words to return from each topic
    """
    data = getKeywords(texts, 0, LDA=True)
    data = [d.split() for d in data]
    dictionary = corpora.Dictionary(data)
    corpus = [dictionary.doc2bow(text) for text in data]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=topics, id2word = dictionary, passes=20)
    results = ldamodel.print_topics(num_topics=topics, num_words=words)

    results = [word[1] for word in results]

    new = []
    p = re.compile(r'"(.*?)"')
    for word in results:

        extract = p.findall(word)
        new.append(extract)

    results = list(chain.from_iterable(new))
    return results


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
    fedTest = LDA('../Data/fed2021.txt', 5, 5)
    print(fedTest)
    os.remove('../Data/fed2021.txt')
