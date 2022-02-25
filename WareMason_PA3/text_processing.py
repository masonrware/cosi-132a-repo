#!/usr/bin/env python3

# text_processing.py
# Version 1.0
# 2/23/2022

import re
from typing import Set

from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
unkown_words = set()


class TextProcessing:
    """Class to process text"""

    def __init__(self, stemmer=PorterStemmer(), stop_words_=None, *args):
        """class TextProcessing is used to tokenize and normalize tokens that will be further used to build inverted
        index."""
        if stop_words_ is None:
            stop_words_ = stop_words
        self.stemmer = stemmer
        self.STOP_WORDS = stop_words_

    def normalize(self, token: str) -> str:
        """normalize the token based on:
        1. make all characters in the token to lower case
        2. remove any characters from the token other than alphanumeric characters and dash ("-")
        3. after step 1, if the processed token appears in the stop words list or its length is 1, return an empty
           string
        4. after step 1, if the processed token is NOT in the stop words list and its length is greater than 1, return
           the stem of the token """
        token = token.lower()
        token = re.sub('[^a-zA-Z0-9 -]', '', token)
        if token in stop_words or len(token) <= 1:
            return ''
        elif token not in stop_words and len(token) > 1:
            return self.stemmer.stem(token)

    def get_normalized_tokens(self, title_: str = " ", content_: str = " ") -> Set[str]:
        """pass in the title and content_str of each document, and return a set of normalized tokens (exclude the
        empty string) you may want to apply word_tokenize first to get un-normalized tokens first """
        tokenized_words = set()
        token_title = word_tokenize(title_)
        token_content = word_tokenize(content_)
        for token in token_title:
            if self.normalize(token) != '':
                tokenized_words.add(self.normalize(token))
        for token in token_content:
            if self.normalize(token) != '':
                tokenized_words.add(self.normalize(token))
        return tokenized_words


if __name__ == "__main__":
    tpObj = TextProcessing(PorterStemmer(), stop_words)
    title = ''
    content = ''
    print(tpObj.get_normalized_tokens(title, content))
