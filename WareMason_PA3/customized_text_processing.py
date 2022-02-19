from typing import Set
import pandas as pd
import re

# #using the feauture_extraction package from sklearn, I import the TfidVectorizer
# #using this, I can get a list of stopwords and can create a vecotrizer to give me the 
# #informative ratings of any words input
from sklearn.feature_extraction import text
from nltk.tokenize import word_tokenize
# from sklearn.feature_extraction.text import TfidfVectorizer

stop_words = text.ENGLISH_STOP_WORDS.union(["book"])
# vectorizer = TfidfVectorizer(ngram_range=(1,1), stop_words=stop_words)


# ##use case
# X = vectorizer.fit_transform(["this is an apple.","this is a book."])
# idf_values = dict(zip(vectorizer.get_feature_names(), vectorizer.idf_))

import spacy
nlp = spacy.load('en_core_web_sm')


doc = nlp(Example_Sentence)


class CustomizedTextProcessing:
    def __init__(self, *args, **kwargs):
        """
        the default TextProcessing class uses Porter stemmer and stopwords list from nltk to process tokens.
        in the Python class, please include at least one other approach for each of the following:
        - to identify a list of terms that should also be ignored along with stopwords
        - to normalize tokens other than stemming and lemmatization

        Your implementation should be in this class. Create more helper functions as you needed. Your approaches could
        be based on heuristics, the usage of a tool from nltk or some new feature you implemented using Python. Be creative!

        # TODO:
        :param args:
        :param kwargs:
        """
        pass

    @classmethod
    def from_customized(cls, *args, **kwargs) -> "CustomizedTextProcessing":
        """
        You don't necessarily need to implement a class method, but if you do, please use this boilerplate.
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def normalize(self, token: str) -> str:
        """
        your approach to normalize a token. You can still adopt the criterion and methods from TextProcessing along with your own approaches
        :param token:
        :return:
        """
        token = token.lower()
        no_number_token = re.sub('\d+','',token)
        no_punc_token = re.sub('[^\w\s]','', no_number_token)
        no_wspace_token = no_punc_token.strip()
        if not no_wspace_token in stop_words:
            return ''
        else:
            return no_wspace_token
        ## alt to stem or lem


    def get_normalized_tokens(self, title: str, content: str) -> Set[str]:
        """
        pass in the title and content_str of each document, and return a set of normalized tokens (exclude the empty string)
        :param title:
        :param content:
        :return:
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
        return tokenized_words


if __name__ == "__main__":
    pass
