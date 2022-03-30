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

from elasticsearch_dsl import analyzer, tokenizer               # type: ignore
from elasticsearch_dsl.query import MatchAll, Match             # type: ignore
from elasticsearch_dsl.connections import connections           # type: ignore
from sklearn.feature_extraction.text import TfidfVectorizer     # type: ignore



class Evaluate:
    ''' A class to represent an individual evaluation run. '''
    def __init__(self, index: str, topic: int, query_type: str, search_type: str,               # vec_name: str
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
        self.raw_query: list()
        self.vector_query: Any
        self.basic_query: Any
        
        
    def __str__(self) -> None:
        print(f'{self.index}\n{self.topic}\n{self.query_type}\n{self.search_type}\n{self.eng_ana}\n{self.top_k}')
        
    def process_topic(self) -> None:
        ''' Method to analyze the query and embed it. '''
        vectorizer = TfidfVectorizer()
        my_analyzer = analyzer(
            "my_analyzer1",
            tokenizer=tokenizer("trigram", "ngram", min_gram=3, max_gram=3),
            filter=["lowercase"],
        )
        
        with open("pa5_data/pa5_queries.json", 'r') as f:
            data = json.load(f)['pa5_queries']
        self.topic_dict = [topic_dict for topic_dict in data if int(topic_dict['topic'])==self.topic][0]
        
        ###????????? How to go from text to list to searching?
        
        
        if self.query_type=='kw':
            X = vectorizer.fit_transform([self.topic_dict['kw']])
            self.basic_query = Match(
                title={"query": vectorizer.get_feature_names_out()[0]}
            )
            
            response = my_analyzer.simulate(self.topic_dict['kw'])
            self.raw_query = [t.token for t in response.tokens]
            
        elif self.query_type=='nl':
            X = vectorizer.fit_transform([self.topic_dict['nl']])
            self.basic_query = Match(
                title={"query": vectorizer.get_feature_names_out()[0]}
            )
            
            response = my_analyzer.simulate(self.topic_dict['nl'])
            self.raw_query = [t.token for t in response.tokens]
        
        ###????????
        
        #embedding done here
        if self.vector_name == 'ft_vector':
            encoder = EmbeddingClient(host="localhost", embedding_type="fasttext")
            self.vector_query = encoder.encode(self.raw_query, pooling="mean").tolist()[0]  # get the query embedding and convert it to a list
            self.vector_query = generate_script_score_query(self.vector_query, "ft_vector")
        elif self.vector_name == 'sbert_vector':
            encoder = EmbeddingClient(host="localhost", embedding_type="sbert")
            self.vector_query = encoder.encode([self.raw_query], pooling="mean").tolist()[0]
            self.vector_query = generate_script_score_query(self.vector_query, "sbert_vector")


    def rank_results(self) -> None:
        ''' Method to search the db and return the specified-method-ranked results. '''
        search("wapo_docs_50k", self.raw_query)
        print('\n')
        rescore_search("wapo_docs_50k", self.basic_query, self.vector_query)
        
        ##??? NDCG20 ?
        



def main():
    parser = argparse.ArgumentParser()
    connections.create_connection(hosts=["localhost"], timeout=100, alias="default")

    
    parser.add_argument("--index_name", metavar='{wapo_docs_50k}', required=True,
                        type=str, help="name of the ES index")
    parser.add_argument("--topic_id", required=True, type=int, help="topic id number")
    parser.add_argument("--query_type", metavar='{kw,nl}', required=True, type=str,
                        help="use keyword or natural language query")
    parser.add_argument("--search_type", metavar='{vector,rerank}', required=True,
                        type=str, help="reranking or ranking with vector only")
    parser.add_argument("--use_english_analyzer", required=False,
                        action='store_true', help="use english analyzer for BM25 search")
    parser.add_argument("--vector_name", metavar='{ft_vector,sbert_vector}',
                        required=True, type=str, help="use fasttext or sbert embedding")
    parser.add_argument("--top_k", required=False, type=int,
                        help="evaluate on top K ranked documents")   
    args = parser.parse_args()
    
    if args.use_english_analyzer:
        eval = Evaluate(index=args.index_name, topic=args.topic_id,                                 # vec_name=args.vector_name
                    query_type=args.query_type, search_type=args.search_type,
                    eng_ana=True, vector_name=args.vector_name, top_k=args.top_k)
    else:
        eval = Evaluate(index=args.index_name, topic=args.topic_id,                                 # vec_name=args.vector_name
                    query_type=args.query_type, search_type=args.search_type,
                    eng_ana=False, vector_name=args.vector_name, top_k=args.top_k)
    
    # eval.__str__()
    eval.process_topic()
    eval.rank_results()
    
    

if __name__ == "__main__":
    main()
