import re
from typing import Set
#TODO: move below imports to where they will be called for both the index terms loading and for the query normalization
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

class TextProcessing:
    """
    Class to process text
    """

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
    def from_nltk(self, cls, stemmer: Any = PorterStemmer().stem, stop_words: List[str] = stopwords.words("english")) -> "TextProcessing":
        """
        initialize from nltk
        :param stemmer:
        :param stop_words:
        :return:
        """
        return cls(self, stemmer, stop_words)

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
        if token in stop_words or len(token)<=1:
            return ''
        elif token not in stop_words and len(token)>1:
            return self.stemmer.stem(token)

    def get_normalized_tokens(self, title: str = '', content: str = '') -> Set[str]:
        """
        pass in the title and content_str of each document, and return a set of normalized tokens (exclude the empty string)
        you may want to apply word_tokenize first to get un-normalized tokens first
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
    tpObj = TextProcessing(PorterStemmer(), stop_words)
    title = ''
    content = ''
    print(tpObj.get_normalized_tokens(title, content))
