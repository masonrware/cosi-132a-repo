#!usr/bin/python3.9

#evaluate.py
#Version 1.0.0
#3-30-22

#Written By: Mason Ware


import argparse
from concurrent.futures import process
import json
from typing import Any, Sequence

from example_query import generate_script_score_query
from embedding_service.client import EmbeddingClient
from utils import timer

from elasticsearch_dsl import Search                            # type: ignore
from elasticsearch_dsl.query import MatchAll, Match, Query      # type: ignore
from elasticsearch_dsl.connections import connections           # type: ignore
from sklearn.feature_extraction.text import TfidfVectorizer     # type: ignore
import nltk                                                     # type: ignore
from nltk.corpus import wordnet                                 # type: ignore
nltk.download('wordnet')

connections.create_connection(hosts=["localhost"], timeout=100, alias="default")


class Engine:
    ''' A class to represent an SE user query. '''
    def __init__(self, index: str, raw_query: str, eng_ana: bool, 
                 vector_name: str = 'sbert_vector', search_type: str = '', 
                 top_k: int = 20) -> None:
        #TODO
        #change defaults so that user can customize their search
        
        self.index: str = index
        self.search_type: str = search_type
        self.eng_ana: bool = eng_ana
        self.vector_name: str = vector_name
        self.top_k: int = top_k
        self.raw_query: str = raw_query
        
        self.results: list()
        
        self.match_all_query: Query = MatchAll()
        self.vector_query: Any
        self.basic_query: Any     
        self.better_query: Any       
    
    @timer
    def search(self) -> list():
        ''' Method to perform searching '''
        parse_query: list = self.raw_query.split(' ')
        # definitions: list = list()
        # examples: list = list()
        synonyms: list = list()
        for term in parse_query:
            synset = wordnet.synsets(term)
            # definitions.append(synset[0].definition()) if len(synset)>0 else ''
            # examples.append(str(synset[0].examples()) if len(synset)>0 else '')
            synonyms += [lemma.name() for lemma in synset[0].lemmas()] if len(synset)>0 else ''
        if self.eng_ana:
            self.basic_query = Match(stemmed_content = {"query": self.raw_query + ' ' + ' '.join(synonyms)})        #vectorizer_basic.get_feature_names_out()
            self.better_query = Match(stemmed_content = {"query": self.raw_query + ' ' + ' '.join(synonyms)})
        else:
            self.basic_query = Match(content = {"query": self.raw_query + ' ' + ' '.join(synonyms)})
            self.better_query = Match(content = {"query": self.raw_query + ' ' + ' '.join(synonyms)})
        
        QUERY = self.better_query   # select which query to use
        
        # do embedding
        #* embed with ft
        if self.vector_name == 'ft_vector':
            encoder = EmbeddingClient(host="localhost", embedding_type="fasttext")
            self.vector_query = encoder.encode([QUERY.stemmed_content['query'] if self.eng_ana else QUERY.content['query']], pooling="mean").tolist()[0]    # get the query embedding and convert it to a list
            self.vector_query = generate_script_score_query(self.vector_query, "ft_vector")
        #* embed with sbert
        elif self.vector_name == 'sbert_vector':
            encoder = EmbeddingClient(host="localhost", embedding_type="sbert")
            self.vector_query = encoder.encode([QUERY.stemmed_content['query'] if self.eng_ana else QUERY.content['query']], pooling="mean").tolist()[0]    # get the query embedding and convert it to a list
            self.vector_query = generate_script_score_query(self.vector_query, "sbert_vector")
            
        # search
        #! might need to change logic gate bc search_type is an empty str default
        if not self.search_type:
            #* bm25 w/ either analyzer
            self.results = rank(self.index, QUERY, self.top_k)
        if self.search_type == 'vector':
            #* sbert with either embed (default of sbert)
            self.results = rank(self.index, self.vector_query, self.top_k)
        elif self.search_type == 'rerank':
            #* rerank with either embed (default of sbert)
            self.results = re_rank(QUERY, self.vector_query, self.top_k)
            
        return self.results
    
    
def rank(index: str, query: Query, top_k: int) -> list():
    ''' Function to rank documents given a query. '''
    s = Search(using="default", index=index).query(query)[
        :top_k
    ]  # initialize a query and return top five results
    response = s.execute()
    return response
        
    
def re_rank(index: str, query: Query, rescore_query: Query, top_k: int) -> list():
    ''' Function to rank and rerank documents given a query. '''
    s = Search(using="default", index=index).query(query)[
        :top_k
    ]  # initialize a query and return top five results
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
