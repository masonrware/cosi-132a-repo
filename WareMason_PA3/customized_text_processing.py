#!/usr/bin/env python3

# customized_text_processing.py
# Version 1.0
# 2/23/2022

from typing import Set
import re

from sklearn.feature_extraction import text
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


class CustomizedTextProcessing:
    def __init__(self, *args, **kwargs):
        """
        the default TextProcessing class uses Porter stemmer and stopwords list from nltk to process tokens.
        in the Python class, please include at least one other approach for each of the following:
        - to identify a list of terms that should also be ignored along with stopwords
        - to normalize tokens other than stemming and lemmatization

        Your implementation should be in this class. Create more helper functions as you needed. Your approaches could
        be based on heuristics, the usage of a tool from nltk or some new feature you implemented using Python. Be creative!
        """
        self.stop_words = text.ENGLISH_STOP_WORDS.union(["book"])
        self.vectorizer = TfidfVectorizer(ngram_range=(1,1), stop_words=self.stop_words)


    # @classmethod
    # def from_customized(cls, *args, **kwargs) -> "CustomizedTextProcessing":
    #     """
    #     You don't necessarily need to implement a class method, but if you do, please use this boilerplate.
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #     return cls(*args, **kwargs)


    def normalize(self, token: str) -> str:
        """
        your approach to normalize a token. You can still adopt the criterion and methods from TextProcessing along with your own approaches
        """
        token = token.lower()
        no_number_token = re.sub('\d+','',token)
        no_punc_token = re.sub('[^\w\s]','', no_number_token)
        no_wspace_token = no_punc_token.strip()
        if len(no_wspace_token)<=1:
            return ''
        else:
            return no_wspace_token


    def get_normalized_tokens(self, title: str, content: str) -> Set[str]:
        """
        pass in the title and content_str of each document, and return a set of normalized tokens (exclude the empty string)
        """
        tokenized_words = set()
        token_title = word_tokenize(title)
        token_content = word_tokenize(content)
        for token in token_title:
            token = str(token)
            if self.normalize(token) != '':
                tokenized_words.add(self.normalize(token))
        for token in token_content:
            token = str(token)
            if self.normalize(token) != '':
                tokenized_words.add(self.normalize(token))

        X = self.vectorizer.fit_transform(tokenized_words)
        idf_values = dict(zip(self.vectorizer.get_feature_names_out(), self.vectorizer.idf_)) 
        return [idf_values.keys()]


if __name__ == "__main__":
    pass
