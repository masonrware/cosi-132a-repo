#!bin/usr/python3

#inverted_index.py
#Version 2.0.0
#3-12-22


import heapq
import math
from typing import List, Tuple, Dict, Iterable

from mongo_db import db, insert_doc_len_index, insert_vs_index, query_doc, query_vs_index, query_doc_len_index, insert_test_db_index
from text_processing import TextProcessing
from utils import timer

text_processor = TextProcessing()

def get_raw_tf_value(term: str, content: str) -> float:
    """ 
    This is a method that takes a str representing an individual token and a str representing the set of tokens and calculates
    the number of appearances of the given term in the content 
    """
    return float(content.count(term))

def cosine_sim(tfidf_term: float, tf_doc: float, doc_length: float) -> float:
    """ 
    This is a method to get the cosine similarity between objects of given information. Namely, this method computes the cosine similarity
    for a given tfidf score, a given tf score, and two vector lengths 
    """
    return (tfidf_term*tf_doc)/(doc_length)


class InvertedIndex:
    """
    Inverted Index Data Structure to map tokens to their postings.
    """
    def __init__(self):
        self.index = []
        self.appearances_dict = dict()
        
    def index_document(self, document: dict) -> None:
        """
        Process a given document and update the appearances dict.
        """
        terms = text_processor.get_normalized_tokens(document['title'], document['content_str'])
        for term in terms:
            if term in self.appearances_dict:
                self.appearances_dict[term].add((document['id'], text_processor.tf(get_raw_tf_value(term, terms))))
            else:
                self.appearances_dict[term] = {(document['id'], text_processor.tf(get_raw_tf_value(term, terms)))}
    
    def load_index_postings_list(self) -> None:
        for term in self.appearances_dict:
            self.index.append({
                'token': term,
                'doc_tf_index': list(self.appearances_dict[term])
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
    total_tf = sum((tf**2 for tf in term_tfs))
    if total_tf:
        return float(math.sqrt(total_tf))
    else:
        return 0.0

@timer
def build_inverted_index(wapo_docs: Iterable, flag: str) -> None:
    """
    load wapo_pa4.jl to build two indices:
        - "vs_index": for each normalized term as a key, the value should be a list of tuples; each tuple stores the doc id this term appears in and the term weight (log tf)
        - "doc_len_index": for each doc id as a key, the value should be the "length" of that document vector
    insert the indices by using mongo_db.insert_vs_index and mongo_db.insert_doc_len_index method
    """    
    inv_ind = InvertedIndex()
    doc_vec_lengths = {}
    doc_vec_lengths_list = []
    for doc_image in wapo_docs:
        inv_ind.index_document(doc_image)             ##! Weight document terms using log TF formula with cosine (length) normalization  
    inv_ind.load_index_postings_list()
    index = inv_ind.get_index()
    for term_index in index:
        for doc_tf_tuple in term_index['doc_tf_index']:
            if doc_tf_tuple[0] in doc_vec_lengths:
                doc_vec_lengths[doc_tf_tuple[0]].append(doc_tf_tuple[1])
            else:
                doc_vec_lengths[doc_tf_tuple[0]] = [ doc_tf_tuple[1] ]
    for key, value in doc_vec_lengths.items():
        doc_vec_lengths_list.append({'id': key, 'doc-vec-length': get_doc_vec_norm(value)})
    #generate doc_len_index content
    if flag == 'build':
        if not "vs_index" in db.list_collection_names():
            insert_vs_index(index)
        if not "doc_len_index" in db.list_collection_names():
            insert_doc_len_index(doc_vec_lengths_list)
    if flag == 'test':
        if not "test_db_index" in db.list_collection_names():
            insert_test_db_index(sorted(inv_ind.get_index(), key = lambda i:len(i['doc_tf_index']), reverse=True)) # gets inserted into the db largest->smallest

    
    
def parse_query(query: str) -> Tuple[List[str], List[str], List[str]]:
    """
    helper function, should be called in query_inverted_index
    given each query, return a list of normalized terms, a list of stop words and a list of unknown words separately
    """
    normalized_query = text_processor.get_normalized_tokens(query)
    query_list = query.split(' ')
    stop_words = {token for token in query_list if not text_processor.normalize(token) in normalized_query}
    unknown_words = {token for token in query_list if isinstance(query_vs_index(text_processor.normalize(token)), type(None)) and not token in stop_words}
    return (normalized_query, stop_words, unknown_words)

def top_k_docs(doc_scores: Dict[int, float], k: int) -> List[Tuple[float, int]]:
    """
    helper function, should be called in query_inverted_index method
    given the doc_scores, return top k doc ids and corresponding scores using a heap
    :param doc_scores: a dictionary where doc id is the key and cosine similarity score (TO THE PARSED QUERY) is the value
    :param k:
    :return: a list of tuples, each tuple contains (score, doc_id)
    """
    doc_scores_list = list(doc_scores.items())
    heapq.heapify(doc_scores_list)
    results = heapq.nlargest(k, doc_scores_list, key=lambda x:x[1])
    return results
    
@timer
def query_inverted_index(query: str, k: int = 10) -> Tuple[List[Tuple[float, int]], List[str], List[str]]:
    """
    disjunctive query over the vs_index with the help of mongo_db.query_vs_index, mongo_db.query_doc_len_index methods
    return a list of matched documents (output from the function top_k_docs), a list of stop words and a list of unknown words separately
    """
    postings_list = []
    parsed_query, stop_words, unknown_words = parse_query(query)
    doc_scores = {}
    for term in parsed_query:
        test_item = query_vs_index(term)
        print(f'====on term: {term}')
        if not term in unknown_words and test_item:
            postings_list = test_item['doc_tf_index']
            for doc_tuple in postings_list:
                term_tf_idf_score = (doc_tuple[1] * text_processor.idf(26987, len(postings_list)))        ##! Weight query terms using logarithmic TF*IDF formula without length normalization
                doc_score = cosine_sim(tfidf_term=term_tf_idf_score,
                                                tf_doc=doc_tuple[1],
                                                doc_length=0.5)
                    ##! Code for the above line. doc_length should be: query_doc_len_index(doc_tuple[0])['doc-vec-length']
                    ##! For some reason, querying - although it is constant - slows down the search process significantly
                doc_scores[doc_tuple[0]] = doc_score
    if postings_list:
        ranked_results = top_k_docs(doc_scores, k)
        return (ranked_results, stop_words, unknown_words)
    else:
        return ([], [], [])
    