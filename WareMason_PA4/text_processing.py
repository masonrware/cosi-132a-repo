#!/usr/bin/env python3

# text_processing.py
# Version 1.0
# 2/23/2022

import math
import re
from typing import Any, List, Set

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

    @classmethod
    def from_nltk(cls, stemmer: Any = PorterStemmer().stem, stop_words: List[str] = stopwords.words("english")) -> "TextProcessing":
        """
        initialize from nltk
        :param stemmer:
        :param stop_words:
        :return:
        """
        return cls(stemmer, set(stop_words))

    def normalize(self, token: str) -> str:
        """normalize the token based on:
        1. make all characters in the token to lower case
        2. remove any characters from the token other than alphanumeric characters and dash ("-")
        3. after step 1, if the processed token appears in the stop words list or its length is 1, return an empty
           string
        4. after step 1, if the processed token is NOT in the stop words list and its length is greater than 1, return
           the stem of the token """
        token = token.lower()
        token = re.sub(r'[^a-zA-Z0-9 -]', '', token)
        if token in stop_words or len(token) <= 1:
            return ''
        elif token not in stop_words and len(token) > 1:
            return self.stemmer.stem(token)

    def get_normalized_tokens(self, title_: str = " ", content_: str = " ") -> Set[str]:
        """pass in the title and content_str of each document, and return a set of normalized tokens (exclude the
        empty string) you may want to apply word_tokenize first to get un-normalized tokens first """
        tokenized_words = []
        token_title = word_tokenize(title_)
        token_content = word_tokenize(content_)
        for token in token_title:
            if self.normalize(token) != '':
                tokenized_words.append(self.normalize(token))
        for token in token_content:
            if self.normalize(token) != '':
                tokenized_words.append(self.normalize(token))
        return tokenized_words

    @staticmethod
    def idf(N: int, df: int) -> float:
        """
        compute the logarithmic (base 2) idf score
        :param N: document count N
        :param df: document frequency
        :return:
        """
        if N > 0.0 and df > 0.0:
            return float(math.log2(N/df))
        else:
            return 0.0

    @staticmethod
    def tf(freq: int) -> float:
        """
        compute the logarithmic tf (base 2) score
        :param freq: raw term frequency
        :return:
        """
        if freq>0:
            return float(1 + math.log2(freq))
        else:
            return 0.0


if __name__ == "__main__":
    tpObj = TextProcessing(PorterStemmer(), stop_words)
    title = ''
    content = ''
    print(tpObj.get_normalized_tokens(title, content))
