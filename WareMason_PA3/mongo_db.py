from typing import Dict, List, Iterable

import pymongo

client = pymongo.MongoClient(
    "localhost", 27017
)  # connect to the mongodb server running on your localhost
db = client["ir_2022_wapo"]  # create a new database called "ir_2022_wapo"


def insert_docs(docs: Iterable) -> None:
    """
    - create a collection called "wapo_docs"
    - add a unique ascending index on the key "id"
    - insert documents into the "wapo_docs" collection
    :param docs: WAPO docs iterator (utils.load_wapo(...))
    :return:
    """
    #? I think using utils?
    #! no^, the utils is called pre-pass
    # TODO: give all the docs to reference and render when I need to in hw3.py
    #iterate of the param
    raise NotImplementedError


def insert_db_index(index_list: List[Dict]) -> None:
    """
    - create a collection called "inverted_index"
    - add a unique ascending index on the key "token"
    - insert posting lists (index_list) into the "inverted_index" collection
    :param index_list: posting lists in the format of [{"token": "post", "doc_ids": [0, 3, 113, 444, ...]}, {...}, ...]
    :return:
    """
    #! param recieved from query_doc? - i.e. method called in query_doc
    raise NotImplementedError


def query_doc(doc_id: int) -> Dict:
    """
    query the document from "wapo_docs" collection based on the doc_id
    :param doc_id:
    :return:
    """
    # TODO: get a document by id
    raise NotImplementedError


def query_db_index(token: str) -> Dict:
    """
    query the posting list from "inverted_index" collection based on the token
    :param token:
    :return:
    """
    # TODO: get a list of documents based on a str
    raise NotImplementedError
