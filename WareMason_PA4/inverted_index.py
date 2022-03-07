from pydoc import doc
from typing import List, Tuple, Dict, Iterable
from utils import timer

from text_processing import TextProcessing
from mongo_db import db, insert_doc_len_index

from scipy import spatial

text_processor = TextProcessing.from_nltk()

## TODO: NEED TO REWRITE BELOW
class InvertedIndex:
    """Inverted Index Data Structure to map tokens to their postings."""
    def __init__(self, n: int):
        self.index = []
        self.appearances_dict = dict()
        self.N = n
        
    def index_document(self, document: dict) -> None:
        """Process a given document and update the appearances dict."""
        terms = text_processor.get_normalized_tokens(document['title'], document['content_str'])
        for term in terms:
            if term in self.appearances_dict:
                self.appearances_dict[term].append((document['id'], text_processor.tf(len([token for token in document['content_str'] if token == term]))))
            else:
                self.appearances_dict[term] = [(document['id'], text_processor.tf(len([token for token in document['content_str'] if token == term])))]
    
    def load_index_postings_list(self) -> None:
        for term in self.appearances_dict:
            self.index.append({
                'token': term,
                'doc_tf_index': self.appearances_dict[term]
            })

    def get_index(self) -> List:
        return self.index


def get_doc_vec_norm(term_tfs: List[float]) -> float:
    """
    helper function, should be called in build_inverted_index
    compute the length of a document vector
    :param term_tfs: a list of term weights (log tf) for one document
    :return:
    """
    pass
    

@timer
def build_inverted_index(wapo_docs: Iterable) -> None:
    """
    load wapo_pa4.jl to build two indices:
        - "vs_index": for each normalized term as a key, the value should be a list of tuples; each tuple stores the doc id this term appears in and the term weight (log tf) == THIS IS EVERY INDEX OF THE INV INDEX
        - "doc_len_index": for each doc id as a key, the value should be the "length" of that document vector
    insert the indices by using mongo_db.insert_vs_index and mongo_db.insert_doc_len_index method
    """
    inv_ind = InvertedIndex(len(wapo_docs))
    for doc_image in wapo_docs:

        ##! Weight document terms using log TF formula with cosine (length) normalization
        
        insert_doc_len_index({'doc_id': doc_image['doc_id'], 'length': get_doc_vec_norm([text_processor.tf(term) for term in doc_image['content_str']])})
        inv_ind.index_document(doc_image)
    inv_ind.load_index_postings_list()
    # insert_db_index(sorted(inv_ind.get_index(), key = lambda i:len(i['doc_ids']), reverse=True)) # gets inserted into the db largest->smallest



def parse_query(query: str) -> Tuple[List[str], List[str], List[str]]:
    """
    helper function, should be called in query_inverted_index
    given each query, return a list of normalized terms, a list of stop words and a list of unknown words separately
    """
    ##! Weight query terms using logarithmic TF*IDF formula without length normalization
    pass


def top_k_docs(doc_scores: Dict[int, float], k: int) -> List[Tuple[float, int]]:
    """
    helper function, should be called in query_inverted_index method
    given the doc_scores, return top k doc ids and corresponding scores using a heap
    :param doc_scores: a dictionary where doc id is the key and cosine similarity score (TO THE PARSED QUERY) is the value
    :param k:
    :return: a list of tuples, each tuple contains (score, doc_id)
    """
    ##? HERE IS MY BIG QUESTION
    ##? how am I getting the param for this method, is it the doc_len_index? - where is the method for cosine similarity/length normalization supposed to go?
    pass


def query_inverted_index(query: str, k: int) -> Tuple[List[Tuple[float, int]], List[str], List[str]]:
    """
    disjunctive query over the vs_index with the help of mongo_db.query_vs_index, mongo_db.query_doc_len_index methods
    return a list of matched documents (output from the function top_k_docs), a list of stop words and a list of unknown words separately
    """
    #call parse_query = unknown and stop


    # result = 1 - spatial.distance.cosine(dataSetI, dataSetII)

    #call top_k_docs = matched documents
    pass


if __name__ == "__main__":
    pass
