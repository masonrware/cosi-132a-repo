from typing import Union, List, Tuple, Iterable

from utils import timer
from text_processing import TextProcessing
from mongo_db import insert_db_index, query_db_index

text_processor = TextProcessing.from_nltk()


# include your customized text processing class


@timer
def build_inverted_index(wapo_docs: Iterable) -> None:
    """
    load wapo_pa3.jl to build the inverted index and insert the index by using mongo_db.insert_docs method
    :param wapo_docs:
    :return:
    """
    # TODO:
    raise NotImplementedError


def intersection(posting_lists: List[List[int]]) -> List[int]:
    """
    implementation of the intersection of a list of posting lists that have been ordered from the shortest to the longest
    :param posting_lists:
    :return:
    """
    # TODO:
    raise NotImplementedError


def query_inverted_index(query: str) -> Tuple[List[int], List[str], List[str]]:
    """
    conjunctive query over the built index by using mongo_db.query_db_index method
    return a list of matched document ids, a list of stop words and a list of unknown words separately
    :param query: user input query
    :return:
    """
    # TODO:
    raise NotImplementedError
