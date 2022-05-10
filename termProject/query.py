#!usr/bin/python3.9

#evaluate.py
#Version 1.0.0
#3-30-22

#Written By: Mason Ware


## This module has methods to use for querying the ES index. The retrieval method used is reranking with
## sentence BERT embeddings + standard analyzer


import argparse
from ast import List
from concurrent.futures import process
from flask import flash
import json
from typing import Any, Tuple

from embedding_service.client import EmbeddingClient
from utils.utils import timer

from elasticsearch_dsl import Search                                            # type: ignore
from elasticsearch_dsl.query import MatchAll, Match, Query, ScriptScore         # type: ignore
from elasticsearch_dsl.connections import connections                           # type: ignore
import nltk                                                                     # type: ignore
from nltk.corpus import wordnet                                                 # type: ignore

nltk.download('wordnet', quiet=True)

connections.create_connection(hosts=["localhost"], timeout=100, alias="default")


def generate_script_score_query(query_vector) -> Query:  #took out vector_name param
    """
    generate an ES query that match all documents based on the cosine similarity
    :param query_vector: query embedding from the encoder
    :param vector_name: embedding type, should match the field name defined in BaseDoc ("ft_vector" or "sbert_vector")
    :return: an query object
    """
    q_script = ScriptScore(
        query={"match_all": {}},  # use a match-all query
        script={  # script your scoring function
            "source": f"cosineSimilarity(params.query_vector, 'sbert_vector') + 1.0",  # hard coded sbert_vector
            # add 1.0 to avoid negative score
            "params": {"query_vector": query_vector},
        },
    )
    return q_script
   
# removed define_search method        
        
class Engine:
    ''' A class to represent an SE user query. '''
    def __init__(self, index: str, raw_query: str, top_k: int = 50) -> None:
        self.index: str = index
        self.search_type: str = 'rerank'  # can be taken out
        self.vector_name: str = 'sbert_vector'
        self.top_k: int = top_k
        self.raw_query: str = raw_query
        
        self.results: list()
        
        self.match_all_query: Query = MatchAll()
        self.vector_query: Any
        self.basic_query: Any     
        self.better_query: Any       
    
    # @timer
    def search(self) -> list():
        ''' Method to perform searching '''
        parse_query: list = self.raw_query.split(' ')
        synonyms: list = list()
        for term in parse_query:
            synset = wordnet.synsets(term)
            synonyms += [lemma.name() for lemma in synset[0].lemmas()] if len(synset)>0 else ''

        self.basic_query = Match(review = {"query": self.raw_query + ' ' + ' '.join(synonyms)})
        self.better_query = Match(review = {"query": self.raw_query + ' ' + ' '.join(synonyms)})
        
        QUERY = self.better_query   # select which query to use
        
        # embed with sbert
        encoder = EmbeddingClient(host="localhost", embedding_type="sbert")
        self.vector_query = encoder.encode([QUERY.review['query']], pooling="mean").tolist()[0]    # get the query embedding and convert it to a list
        self.vector_query = generate_script_score_query(self.vector_query)
            
        # rerank with sbert
        self.results = re_rank(self.index, QUERY, self.vector_query, self.top_k)

        return self.results

    def general_search(self, query: Query):
        """
        Searches index based on query
        @param query: Any user Query object
        @return a response object of the matches from the index based on the query
        """
        # initialize a query and return top result
        s = Search(using="default", index=self.index).query(query)[:1]
        response = s.execute()

        return response

        
def re_rank(index: str, query: Query, rescore_query: Query, top_k: int) -> list():
    ''' Function to rank and rerank documents given a query. '''
    s = Search(using="default", index=index).query(query)[
        :top_k
    ]
    s = s.extra(
        rescore={
            "window_size": top_k,
            "query": {
                "rescore_query": rescore_query,
                "query_weight": 0,
                "rescore_query_weight": 1,
            },
        }
    )
    response = s.execute()
    return response
    
    
def main():
    # driver
    connections.create_connection(hosts=["localhost"], timeout=100, alias="default")
    

if __name__ == "__main__":
    main()
