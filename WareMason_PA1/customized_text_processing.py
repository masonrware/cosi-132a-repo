from typing import Set


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
        # TODO:
        raise NotImplementedError

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
