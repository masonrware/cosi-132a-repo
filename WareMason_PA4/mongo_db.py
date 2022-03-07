from operator import index
from turtle import pos
from typing import Dict, List, Iterable

import pymongo
import pprint

client = pymongo.MongoClient("localhost", 27017)
db = client["ir_2022_wapo"]


def insert_docs(docs: Iterable) -> None:
    """
    - create a collection called "wapo_docs"
    - add a unique ascending index on the key "id"
    - insert documents into the "wapo_docs" collection
    :param docs: WAPO docs iterator (utils.load_wapo(...))
    :return:
    """
    wapo_docs = db.wapo_docs
    for doc in docs:
        wapo_docs.insert_one(doc)
        pprint.pprint('DOC---added ' + (doc['title'] if doc['title'] is not None else 'null title') + ' to the DB')


def insert_vs_index(index_list: List[Dict]) -> None:
    """
    - create a collection called "vs_index"
    - add a unique ascending index on the key "term"
    - insert posting lists (index_list) into the "inverted_index" collection
    :param index_list: posting lists in the format of [{"term": "earlier", "term_tf": [[0, 1], [4, 1], ...]}, ...]
    :return:
    """
    vs_index = db.vs_index
    for postings_list in index_list:
        vs_index.insert_one(postings_list)
        pprint.pprint('PL---added the postings list for the term ' + postings_list['term'])


def insert_doc_len_index(index_list: List[Dict]) -> None:
    """
    - create a collection called "doc_len_index"
    - add a unique ascending index on the key "doc_id"
    - insert list of document vector length (index_list) into the "doc_len_index" collection
    :param index_list: document vector length list in the format of [{"doc_id": 0, "length": 39.53}, ...]
    :return:
    """
    doc_len_index = db.doc_len_index
    for doc_vector_image in index_list:
        doc_len_index.insert_one(doc_vector_image)
        pprint.pprint('DL---added doc length for doc #' + doc_vector_image['doc_id'])


def query_doc(doc_id: int) -> Dict:
    """
    query the document from "wapo_docs" collection based on the doc_id
    :param doc_id:
    :return:
    """
    return db.wapo_docs.find_one({'id': doc_id})


def query_vs_index(term: str) -> Dict:
    """
    query the vs_index collection by term
    :param term:
    :return:
    """
    return db.wapo_docs.find_one({'term': term})


def query_doc_len_index(doc_id: int) -> Dict:
    """
    query the doc_len_index by doc_id
    :param doc_id:
    :return:
    """
    return db.wapo_docs.find_one({'doc_id': doc_id})


if __name__ == "__main__":
    pass
