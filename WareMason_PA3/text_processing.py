import re
from typing import Set, Any, List

from nltk.tokenize import word_tokenize  # type: ignore
from nltk.stem.porter import PorterStemmer  # type: ignore
from nltk.corpus import stopwords  # type: ignore

stop_words = set(stopwords.words('english'))

class TextProcessing:
    def __init__(self, stemmer, stop_words, *args):
        """
        class TextProcessing is used to tokenize and normalize tokens that will be further used to build inverted index.
        :param stemmer:
        :param stop_words:
        :param args:
        """
        self.stemmer = stemmer
        self.STOP_WORDS = stop_words

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
        """
        normalize the token based on:
        1. make all characters in the token to lower case
        2. remove any characters from the token other than alphanumeric characters and dash ("-")
        3. after step 1, if the processed token appears in the stop words list or its length is 1, return an empty string
        4. after step 1, if the processed token is NOT in the stop words list and its length is greater than 1, return the stem of the token
        :param token:
        :return:
        """
        token = token.lower()
        token = re.sub('[^a-zA-Z0-9 -]', '', token)
        if token in stop_words or len(token)==1:
            return ''
        elif token not in stop_words and len(token)>1:
            return self.stemmer.stem(token)


    def get_normalized_tokens(self, title: str, content: str) -> Set[str]:
        """
        pass in the title and content_str of each document, and return a set of normalized tokens (exclude the empty string)
        you may want to apply word_tokenize first to get un-normalized tokens first
        :param title:
        :param content:
        :return:
        """
        token_title = word_tokenize(title)
        token_content = word_tokenize(content)
        ##call normalize on each term of each

        # TODO:
        raise NotImplementedError


if __name__ == "__main__":
    pass
