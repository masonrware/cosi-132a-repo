#!usr/bin/python3.9

#evaluate.py
#Version 1.0.0
#3-30-22

#Written By: Mason Ware


import argparse
import json
from typing import Any, Sequence

from example_query import generate_script_score_query, search, rescore_search
from embedding_service.client import EmbeddingClient
from utils import timer
from user_search import rank, re_rank                           # used to actually recieve relevance scores
from metrics import ndcg

from elasticsearch_dsl.query import MatchAll, Match, Query      # type: ignore
from elasticsearch_dsl.connections import connections           # type: ignore
import nltk                                                     # type: ignore
from nltk.corpus import wordnet                                 # type: ignore

nltk.download('wordnet', quiet=True)

class Evaluate:
    ''' A class to represent an individual evaluation run. '''
    def __init__(self, index: str, topic: int, query_type: str, search_type: str,
                 eng_ana: bool, vector_name: str, top_k: int = 20) -> None:
        self.index: str = index
        self.topic: int= topic
        self.query_type: str = query_type
        self.search_type: str = search_type
        self.eng_ana: bool = eng_ana
        self.vector_name: str = vector_name
        self.top_k: int = top_k
        
        self.topic_dict: dict()
        self.ideal_rel_scores: Sequence[int]
        self.rel_scores: Sequence[int]          #! needs filling
        
        self.match_all_query: Query = MatchAll()
        self.raw_query: str
        self.vector_query: Any
        self.basic_query: Any     
        self.better_query: Any  
        
        self.ndcg: float
        
    def __str__(self) -> None:
        return (f'index: {self.index}\ntopic: {self.topic}\nquery type: {self.query_type}\nsearch type: {self.search_type}\nUsing Eng. Analyzer? {self.eng_ana}\nK: {self.top_k}\n')
         
    def process_topic(self) -> None:
        ''' Method to analyze the query and embed it. '''
        with open("pa5_data/pa5_queries.json", 'r') as f:
            data = json.load(f)['pa5_queries']
        self.topic_dict = [topic_dict for topic_dict in data if int(topic_dict['topic'])==self.topic][0] 
        self.raw_query = self.topic_dict[self.query_type]
        with open("pa5_data/ideal_relevance.json", 'r') as f:
            data = json.load(f)
        self.ideal_rel_scores = data[f'{self.topic}']
    
    def eval_search(self) -> None:
        ''' Method to perform searching for an evaluation. '''
        parse_query: list = self.raw_query.split(' ')
        synonyms: list = list()
        for term in parse_query:
            synset = wordnet.synsets(term)
            synonyms += [lemma.name() for lemma in synset[0].lemmas()] if len(synset)>0 else ''
        if self.eng_ana:
            self.basic_query = Match(stemmed_content = {"query": self.raw_query + ' ' + ' '.join(synonyms)})
            self.better_query = Match(stemmed_content = {"query": self.raw_query + ' ' + ' '.join(synonyms)})
        else:
            self.basic_query = Match(content = {"query": self.raw_query + ' ' + ' '.join(synonyms)})
            self.better_query = Match(content = {"query": self.raw_query + ' ' + ' '.join(synonyms)})
        
        QUERY = self.better_query   # here is where you can select which query to use
        
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
            
        # search and retrieve
        if not self.search_type:
            #* bm25 w/ either analyzer
            # print(f'\nBM25 Ranking\n\n')
            # p_rank(QUERY, self.top_k)                                   # comment out to not have search results printed
            self.rel_scores = rank(self.index, QUERY, self.top_k)
        if self.search_type == 'vector':
            #* sbert with either embed (default of sbert)
            # print(f'\nVector Ranking\n\n')
            # p_rank(QUERY, self.top_k)                                   # comment out to not have search results printed
            self.rel_scores = rank(self.index, QUERY, self.top_k)
        elif self.search_type == 'rerank':
            #* rerank with either embed (default of sbert)
            # print(f'\nVector RERanking\n\n')
            # p_re_rank(QUERY, self.vector_query, self.top_k)             # comment out to not have search results printed
            self.rel_scores = re_rank(self.index, QUERY, self.vector_query, self.top_k)
        
    def score(self) -> None:
        ''' Method to get the relevance scores of every evaluation
            and then score the evaluation based on metrics and ideal
            data. '''
        parsed_scores = list()
        for score in self.rel_scores:
            if not score['annotation'].split('-')[0]=='':
                parsed_scores.append(int((score['annotation'].split('-'))[1]))
            else:
                parsed_scores.append(0)
        self.rel_scores = parsed_scores
        # print(self.rel_scores)
        self.ndcg = ndcg(self.rel_scores, self.ideal_rel_scores, k=self.top_k)
        # print(f'NDCG20 SCORE: {self.ndcg}')



def p_rank(query: Query, top_k: int) -> None:
    ''' Function to search for and rank documents using the standard bm25 [PRINT]. '''
    print('Results:\n')
    search("wapo_docs_50k", query=query, top_k=top_k)
    print('\n')
    
def p_re_rank(query: Query, vector: Query, top_k: int) -> None:
    ''' Function to rerank documents using embeddings (fasttext and sbert) [PRINT]. '''
    print('Results:\n')
    rescore_search("wapo_docs_50k", query=query, rescore_query=vector, top_k=top_k)
    print('\n')

class Client:
    ''' Class to run single/many evaluations of the SE. '''
    def __init__(self, index: str, topic: int, query_type: str, search_type: str,
                 eng_ana: bool, vector_name: str, top_k: int = 20) -> None:
        self.index: str = index
        self.topic: int= topic
        self.query_type: str = query_type
        self.search_type: str = search_type
        self.eng_ana: bool = eng_ana
        self.vector_name: str = vector_name
        self.top_k: int = top_k
        
    def __str__(self) -> None:
        return (f'index: {self.index}\ntopic: {self.topic}\nquery type: {self.query_type}\nsearch type: {self.search_type}\nUsing Eng. Analyzer? {self.eng_ana}\nK: {self.top_k}\n')
     
    # @timer
    def run(self) -> float:
        eval = Evaluate(index=self.index, topic=self.topic, query_type=self.query_type, 
                    search_type=self.search_type, eng_ana=self.eng_ana, 
                    vector_name=self.vector_name, top_k=self.top_k)
        eval.process_topic()    # get correct topic and ideal scores
        eval.eval_search()      # perform search and get relevance scores
        eval.score()            # generate a score for SE run
        print(eval.ndcg)

def main():
    parser = argparse.ArgumentParser()
    connections.create_connection(hosts=["localhost"], timeout=100, alias="default")

    # search_type: str = 'vector'
    vector_name: str = 'sbert_vector'
    
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
    
    client = Client(index=args.index_name, topic=args.topic_id, query_type=args.query_type, search_type=args.search_type, 
                    eng_ana=args.use_english_analyzer or True if args.search_type=='rerank' else args.use_english_analyzer, 
                    vector_name= args.vector_name if args.vector_name else vector_name, top_k=args.top_k)
    
    # driver
    line: str = '=' * 50
    # print(f'\n\n{line}\n\nRUNNING ELASTICSEARCH WITH THE FOLLOWING SPECS:\n\n{client}\n{line}\n')
    client.run()


# For each query, you should produce a table with 1 row per search type and 
# 1 column per query type. The value of each cell is the NDCG@20 value. 
# Include your results tables along with a short paragraph of analysis 
# of each table in the report. If you do the extra credit (below), 
# include results in the table(s) as additional query types and discuss 
# your interpretations here.


if __name__ == "__main__":
    main()
