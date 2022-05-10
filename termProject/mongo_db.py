from typing import Dict, List, Iterable

import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client["ir_2022_final"]


def insert_sents(docs: Iterable) -> None:
    """
    - create a collection called "movie_reviews"
    - add a unique ascending index on the key "id"
    - insert documents into the "movie_reviews" collection
    :param docs: movie reviews iterator (utils.load_reviews(...))
    :return:
    """
    mrv = db['movie_reviews']
    mrv.create_index([('title', pymongo.ASCENDING)], unique=True)
    for doc in docs:
        db["movie_reviews"].insert_one(docs[doc])



def query_sents_index(term: str) -> Dict:
    """
    query the vs_index collection by term
    :param term:
    :return:
    """
    posting_list = db["movie_reviews"].find_one({'title': term})
    return posting_list



if __name__ == "__main__":
    pass
