from typing import Set
import pandas as pd
import re

#using the feauture_extraction package from sklearn, I import the TfidVectorizer
#using this, I can get a list of stopwords and can create a vecotrizer to give me the 
#informative ratings of any words input
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer

stop_words = text.ENGLISH_STOP_WORDS.union(["book"])
vectorizer = TfidfVectorizer(ngram_range=(1,1), stop_words=stop_words)


##use case
X = vectorizer.fit_transform(["this is an apple.","this is a book."])
idf_values = dict(zip(vectorizer.get_feature_names(), vectorizer.idf_))


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

    @classmethod
    def from_customized(cls, *args, **kwargs) -> "CustomizedTextProcessing":
        """
        You don't necessarily need to implement a class method, but if you do, please use this boilerplate.
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError

    def normalize(self, token: str) -> str:
        """
        your approach to normalize a token. You can still adopt the criterion and methods from TextProcessing along with your own approaches
        :param token:
        :return:
        """
        token = token.lower()
        # remove numbers
        no_number_string = re.sub(r'\d+','',token)
        # remove all punctuation except words and space
        no_punc_string = re.sub(r'[^\w\s]','', no_number_string)
        # remove white spaces
        no_wspace_string = no_punc_string.strip()
        lst_string = [no_wspace_string][0].split()
        no_stpwords_string=''
        for i in lst_string:
            if not i in stop_words:
                no_stpwords_string += i+' '
        # removing last space
        no_stpwords_string = no_stpwords_string[:-1]
        return no_stpwords_string


    def get_normalized_tokens(self, title: str, content: str) -> Set[str]:
        """
        pass in the title and content_str of each document, and return a set of normalized tokens (exclude the empty string)
        :param title:
        :param content:
        :return:
        """

        # TODO:
        raise NotImplementedError


if __name__ == "__main__":
    pass
