# WordFilter.py
#
# Strip, Tokenize, Lemmatize, Remove non-alphabetical phrases
# and performs dictionary checks on input and returns an array of strings
#

from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from enchant import Dict

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class WordFilter():
    def __init__(self):
        self.stopWords = stopwords.words('english')
        self.stemmer = SnowballStemmer('english')
        self.spellcheck = Dict()

    def filterWords(self, words):
        output = []
        for w in word_tokenize(words.strip()):
            w = w.lower()
            if w not in self.stopWords and w.isalpha() and self.spellcheck.check(w):
                token = str(self.stemmer.stem(w))
                if token not in output:
                    output.append(token)
        return output
