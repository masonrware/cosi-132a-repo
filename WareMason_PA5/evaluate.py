#!usr/bin/python3.9

#evaluate.py
#Version 1.0.0
#3-30-22

#Written By: Mason Ware


import argparse
import json
from typing import Any

from example_query import generate_script_score_query, search, rescore_search
from embedding_service.client import EmbeddingClient

from elasticsearch_dsl.query import MatchAll, Match, Query      # type: ignore
from elasticsearch_dsl.connections import connections           # type: ignore
from sklearn.feature_extraction.text import TfidfVectorizer     # type: ignore


class Evaluate:
    ''' A class to represent an individual evaluation run. '''
    def __init__(self, index: str, topic: int, query_type: str, search_type: str,
                 eng_ana: bool, vector_name: str, top_k: int = 20) -> None:
        self.index = index
        self.topic = topic
        self.query_type = query_type
        self.search_type = search_type
        self.eng_ana = eng_ana
        self.vector_name = vector_name
        self.top_k = top_k
        
        self.topic_dict: dict()
        
        self.match_all_query = MatchAll()
        self.raw_query: Any
        self.vector_query: Any
        self.basic_query: Any
        
    def __str__(self) -> None:
        return (f'index: {self.index}\ntopic: {self.topic}\nquery type: {self.query_type}\nsearch type: {self.search_type}\nUsing Eng. Analyzer? {self.eng_ana}\nK: {self.top_k}\n')
        
    def process_topic(self) -> None:
        ''' Method to analyze the query and embed it. '''
        # process the topic
        with open("pa5_data/pa5_queries.json", 'r') as f:
            data = json.load(f)['pa5_queries']
        self.topic_dict = [topic_dict for topic_dict in data if int(topic_dict['topic'])==self.topic][0] 
    
    def search(self) -> None:
        ''' Method to perform searching. '''
        
        # find the most informative words in query and
        # create a basic query (one for english analyzer
        # and one for std analyzer)
        # also save the raw query as a str for encoding
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform([self.topic_dict[self.query_type]]) 
        if self.eng_ana:
            #? Better way to do this?
            self.basic_query = Match(stemmed_content = {"query": vectorizer.get_feature_names_out()[0]})
            self.raw_query = self.topic_dict[self.query_type]
        else:
            self.basic_query = Match(content = {"query": vectorizer.get_feature_names_out()[0]})
            self.raw_query = self.topic_dict[self.query_type]
            
        #! HOW TO RANK W/ SBERT? - thought I can only rank with standard bm25 (bc sbert requires embedding...)
        #* embed with ft
        if self.vector_name == 'ft_vector':
            encoder = EmbeddingClient(host="localhost", embedding_type="fasttext")
            self.vector_query = encoder.encode([self.raw_query], pooling="mean").tolist()[0]  # get the query embedding and convert it to a list
            self.vector_query = generate_script_score_query(self.vector_query, "ft_vector")
        #* embed with sbert
        elif self.vector_name == 'sbert_vector':
            encoder = EmbeddingClient(host="localhost", embedding_type="sbert")
            self.vector_query = encoder.encode([self.raw_query], pooling="mean").tolist()[0]  # get the query embedding and convert it to a list
            self.vector_query = generate_script_score_query(self.vector_query, "sbert_vector")
            
        if self.search_type == 'vector':
            #* bm25 w/ either analyzer
            rank_results(self.basic_query, self.top_k)
            #somehow also search sbert - no way to differentiate?
        elif self.search_type == 'rerank':
            #* rerank with either embed
            re_rank_results(self.basic_query, self.vector_query, self.top_k)
        


def rank_results(query: Query, top_k: int) -> None:
    ''' Function to search for and rank documents using the standard bm25. '''
    search("wapo_docs_50k", query, top_k)
    print('\n')
    
def re_rank_results(query: Query, vector: Query, top_k: int) -> None:
    ''' Function to rerank documents using embeddings (fasttext and sbert). '''
    rescore_search("wapo_docs_50k", query, vector, top_k)
    print('\n')

# For each query, you should produce a table with 1 row per search type and 
# 1 column per query type. The value of each cell is the NDCG@20 value. 
# Include your results tables along with a short paragraph of analysis 
# of each table in the report. If you do the extra credit (below), 
# include results in the table(s) as additional query types and discuss 
# your interpretations here.


def main():
    parser = argparse.ArgumentParser()
    connections.create_connection(hosts=["localhost"], timeout=100, alias="default")

    search_type = 'vector'
    vector_name = 'ft_vector'
    
    parser.add_argument("--index_name", 
                        metavar='{wapo_docs_50k}', 
                        required=True,
                        type=str, 
                        help="name of the ES index")
    parser.add_argument("--topic_id", 
                        required=True, 
                        type=int, 
                        help="topic id number")
    parser.add_argument("--query_type", 
                        metavar='{kw,nl}', 
                        required=True, 
                        type=str,
                        help="use keyword or natural language query")
    parser.add_argument("--search_type", 
                        metavar='{vector,rerank}', 
                        required=False,
                        type=str, 
                        help="reranking or ranking with vector only")
    parser.add_argument("--use_english_analyzer", 
                        required=False,
                        action='store_true', 
                        help="use english analyzer for BM25 search")
    parser.add_argument("--vector_name", 
                        metavar='{ft_vector,sbert_vector}',
                        required=False, 
                        type=str, 
                        help="use fasttext or sbert embedding")
    parser.add_argument("--top_k", 
                        required=False, 
                        type=int,
                        help="evaluate on top K ranked documents")   
    args = parser.parse_args()
    
    eval = Evaluate(index=args.index_name, topic=args.topic_id, query_type=args.query_type, 
                    search_type=args.search_type if args.search_type else search_type, eng_ana=args.use_english_analyzer, 
                    vector_name= args.vector_name if args.vector_name else vector_name, top_k=args.top_k)
    print('='*50, '\nRUNNING ELASTICSEARCH WITH THE FOLLOWING SPECS:\n', eval, '='*50, '\n')
    eval.process_topic()
    eval.search()       #run
    

if __name__ == "__main__":
    main()
