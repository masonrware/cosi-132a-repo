#!/usr/bin/python3

# mongo_db.py
# Version 2.0.0
# 3/14/2022

from operator import index
from turtle import pos
from typing import Dict, List, Iterable

import pymongo
from utils import timer

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
    wapo_docs.insert_many(docs)


def insert_vs_index(index_list: List[Dict]) -> None:
    """A term to doc-tf pair index is inseted into the db"""
    vs_index = db.vs_index
    vs_index.insert_many(index_list)


def insert_doc_len_index(index_list: List[Dict]) -> None:
    """A doc-cosine-normalized-length index is inserted into the db"""
    doc_len_index = db.doc_len_index
    doc_len_index.insert_many(index_list)
    
    
def insert_test_db_index(index_list: List[Dict]) -> None:
    """A test version of the vs_index collection is added to the db"""
    inverted_index = db.test_db_index
    inverted_index.insert_many(index_list)
    
    
def query_doc(doc_id: int) -> Dict:
    """A single document is queried from the db"""
    return db.wapo_docs.find_one({'id': doc_id})


def query_vs_index(term: str) -> Dict:
    """A single postings list is queried from the db"""
    return db.vs_index.find_one({'token': term})

def query_doc_len_index(doc_id: int) -> Dict:
    """A single document length is queried from the db"""
    return db.doc_len_index.find_one({'id': doc_id})


if __name__ == "__main__":
    pass
