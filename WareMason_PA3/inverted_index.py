from typing import Union, List, Tuple, Iterable

from utils import timer, load_wapo
from text_processing import TextProcessing
from mongo_db import insert_db_index, query_db_index

text_processor = TextProcessing.from_nltk()

#!!! Sort listings (i.e. values of index) by size shortest->longest


@timer
def build_inverted_index(wapo_docs: Iterable) -> None:
    """
    load wapo_pa3.jl to build the inverted index and insert the index by using mongo_db.insert_db_index method
    :param wapo_docs:
    :return:
    """
    # TODO: reload the wapo_docs with load_wapo to get a list back and then ...
    # TODO: call insert_db_index and put the documents into the database as a dictionary with ids?? idk yet

def intersection(posting_lists: List[List[int]]) -> List[int]:
    """
    implementation of the intersection of a list of posting lists that have been ordered from the shortest to the longest
    :param posting_lists:
    :return:
    """
    # TODO: get all documents for a given term set's list of posting lists
    raise NotImplementedError


def query_inverted_index(query: str) -> Tuple[List[int], List[str], List[str]]:
    """
    conjunctive query over the built index by using mongo_db.query_db_index method
    return a list of matched document ids, a list of stop words and a list of unknown words separately
    :param query: user input query
    :return:
    """
    # TODO: search based on a query
    #! maybe also normalize query text - alr have the text processor
    raise NotImplementedError
