from typing import List, Tuple, Iterable
import re

from utils import timer
from text_processing import TextProcessing

from mongo_db import insert_db_index, query_db_index


text_processor = TextProcessing()


class InvertedIndex:
    """Inverted Index class."""

    def __init__(self):
        self.index = []
        self.appearances_dict = dict()
        
    def index_document(self, document: dict) -> None:
        """Process a given document and update the index."""
        terms = text_processor.get_normalized_tokens(document['title'], document['content_str'])
        for term in terms:
            if term in self.appearances_dict:
                self.appearances_dict[term].append(document['id'])
            else:
                self.appearances_dict[term] = [document['id']]
    
    def load_index_postings_list(self) -> None:
        for term in self.appearances_dict:
            self.index.append({
                'token': term,
                'doc_ids': self.appearances_dict[term]
            })

    def get_index(self) -> List:
        return self.index


@timer
def build_inverted_index(wapo_docs: Iterable) -> None:
    """
    load wapo_pa3.jl to build the inverted index and insert the index by using mongo_db.insert_db_index method
    :param wapo_docs:
    :return:
    """
    inv_ind = InvertedIndex()
    for doc_image in wapo_docs:
        inv_ind.index_document(doc_image)
    inv_ind.load_index_postings_list()
    insert_db_index(sorted(inv_ind.get_index(), key = lambda i:len(i['doc_ids']), reverse=True)) #gets inserted into the db largest->smallest


def intersection(posting_lists: List[List[int]]) -> List[int]:
    """
    implementation of the intersection of a list of posting lists that have been ordered from the shortest to the longest
    """
    return list(set.intersection(*[set(x) for x in posting_lists])) if posting_lists else []


def query_inverted_index(query: str) -> Tuple[List[int], List[str], List[str]]:
    """
    conjunctive query over the built index by using mongo_db.query_db_index method
    return a list of matched document ids, a list of stop words and a list of unknown words separately
    """
    normalized_query = text_processor.get_normalized_tokens(query)
    query_list = query.split(' ')
    query_list = re.findall(r"[\w']+|[.,!?;]", query)
    
    stop_words = {token for token in query_list if not text_processor.normalize(token) in normalized_query}
    unknown_words = {token for token in query_list if isinstance(query_db_index(text_processor.normalize(token)), type(None)) and not token in stop_words}

    posting_lists = []
    for token in normalized_query:
        if not token in unknown_words:
            posting_lists.append(query_db_index(token)['doc_ids'])
    intersect_posting_lists = intersection(posting_lists)
    return (intersect_posting_lists, stop_words, unknown_words)
