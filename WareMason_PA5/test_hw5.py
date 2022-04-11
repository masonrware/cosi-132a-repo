#!/usr/bin/python3.9

# test_hw5.py
# Version 1.0.0
# 4/11/2022

import unittest

from example_query import generate_script_score_query
from evaluate import Evaluate, Client
from user_search import rank, re_rank       # the Engine class from user_search is 
                                            # similar to the Evaluate class, so it
                                            # won't be tested

from elasticsearch_dsl.query import Match, MatchAll, Ids
from embedding_service.client import EmbeddingClient


encoder = EmbeddingClient(host="localhost", embedding_type="sbert")
                                

class TestEvaluation(unittest.TestCase):
    ''' These are tests for the Evaluation class located in evaluate.py. '''
    def setUp(self) -> None:
        self.base_bm25_eval = Evaluate(index='wapo_docs_50k',
                                  topic=363,
                                  query_type='nl',
                                  search_type='',
                                  eng_ana='',
                                  vector_name='sbert_vector',
                                  top_k=20)
        self.base_bm25eng_eval = Evaluate(index='wapo_docs_50k',
                                  topic=363,
                                  query_type='nl',
                                  search_type='',
                                  eng_ana='True',
                                  vector_name='sbert_vector',
                                  top_k=20)
        self.base_vec_eval = Evaluate(index='wapo_docs_50k',
                                  topic=363,
                                  query_type='nl',
                                  search_type='vector',
                                  eng_ana='',
                                  vector_name='sbert_vector',
                                  top_k=20)
        self.base_resbert_eval = Evaluate(index='wapo_docs_50k',
                                  topic=363,
                                  query_type='nl',
                                  search_type='rerank',
                                  eng_ana='',
                                  vector_name='sbert_vector',
                                  top_k=20)
        self.base_resbert_eval = Evaluate(index='wapo_docs_50k',    #! fastText issue persisting
                                  topic=363,
                                  query_type='nl',
                                  search_type='rerank',
                                  eng_ana='',
                                  vector_name='ft_vector',
                                  top_k=20)
        return super().setUp()
    
    def test_process_topic(self):
        ''' Eval class processes a topic from the TREC document correctly:
            [ ] The topic dict is populated correctly
            [ ] The correct query is retained '''
        self.base_bm25_eval.process_topic()
        message = f'bm25 evaluation does not process a given topic ({self.base_bm25_eval.topic}) correctly'
        self.assertEqual(self.base_bm25_eval.topic_dict, {'kw': 'tunnel injury disaster', 
                                                          'nl': 'tunnel disaster resulting from fire earthquake, flood, or explosion',
                                                          'topic': '363'}, message)    
        self.assertEqual(self.base_bm25_eval.raw_query, 'tunnel disaster resulting from fire earthquake, flood, or explosion', message)
        
    def test_eval_search(self):
        ''' Eval class searches for documents correctly:
            [ ] better_query is constructed properly
            [ ] correct relevance scores are retrieved '''
        self.base_bm25_eval.process_topic()
        self.base_bm25_eval.eval_search()
        message=f'bm25 evaluation search does not construct proper queries or does not return proper relevance scores'
        self.assertEqual(self.base_bm25_eval.better_query, Match(content={'query': 'tunnel disaster resulting from fire earthquake, flood, or explosion tunnel catastrophe disaster result ensue fire Oregon Beaver_State OR explosion detonation blowup'}), message)
        self.assertEqual(int((self.base_bm25_eval.rel_scores[0]['annotation'].split('-'))[1]), 2, message)
        
        self.base_bm25eng_eval.process_topic()
        self.base_bm25eng_eval.eval_search()
        message=f'bm25 w/ english analyzer evaluation search does not construct proper queries or does not return proper relevance scores'
        self.assertEqual(int((self.base_bm25eng_eval.rel_scores[0]['annotation'].split('-'))[1]), 0, message)
        
        self.base_vec_eval.process_topic()
        self.base_vec_eval.eval_search()
        message=f'vector space evaluation search does not construct proper queries or does not return proper relevance scores'
        self.assertEqual(int((self.base_vec_eval.rel_scores[0]['annotation'].split('-'))[1]), 0, message)
        
        self.base_resbert_eval.process_topic()
        self.base_vec_eval.eval_search()
        message=f'vector space evaluation search does not construct proper queries or does not return proper relevance scores'
        self.assertEqual(int((self.base_vec_eval.rel_scores[0]['annotation'].split('-'))[1]), 0, message)
        
        self.base_vec_eval.process_topic()
        self.base_vec_eval.eval_search()
        message=f'vector space evaluation search does not construct proper queries or does not return proper relevance scores'
        self.assertEqual(int((self.base_vec_eval.rel_scores[0]['annotation'].split('-'))[1]), 0, message)
    
    def test_score(self):
        ''' Eval class scores it's run via NDCG20 correctly. '''
        # understood that if one works, it is mathematically impossible 
        # for others to fail due to issues with the coee
        self.base_bm25_eval.process_topic()
        self.base_bm25_eval.eval_search()
        self.base_bm25_eval.score()
        message=f'an evaluation is not scored properly.'
        self.assertEqual(float(self.base_bm25_eval.ndcg), 0.7774395736906036, message)


class TestClient(unittest.TestCase):
    ''' These are tests for the Client class used to execute an evaluation in evaluate.py '''
    def setUp(self) -> None:
        self.base_client = Client(index='wapo_docs_50k',
                            topic=363,
                            query_type='nl',
                            search_type='',
                            eng_ana='',
                            vector_name='sbert_vector',
                            top_k=20)
        return super().setUp()
    
    def test_run(self) -> None:
        ''' the client executes an evaluation (okami bm25 w/out eng. ana.) correctly
            and recieves the correct results. '''
        res = self.base_client.run()
        message = f'the client does not run an eval properly'
        self.assertEqual(res, 0.7774395736906036, message)


class TestRanking(unittest.TestCase):
    ''' these are the tests for the ranking functions located in user_search.py. '''
    def setUp(self) -> None:
        self.match_all_query = MatchAll()
        self.match_id_query = Ids(values=[1])
        query_embedding = encoder.encode(['testing out a query'], pooling="mean").tolist()[0] 
        self.query_vector = generate_script_score_query(query_embedding, "sbert_vector") 
        return super().setUp()
    
    def test_rank(self):
        ''' Ranking function returns the correct relevance scores. '''
        res = rank('wapo_docs_50k', self.match_all_query, 10)
        message = 'ranking function does not return the correct relevancy scores.'
        self.assertEqual(res[0]['title'], 'Many Iowans still don’t know who they will caucus for', message)
        
    def test_rerank(self):
        ''' Re-Ranking function returns the correct relevance scores. '''
        res = re_rank('wapo_docs_50k', self.match_all_query, self.query_vector, 10)
        message = 're-ranking function does not return the correct relevancy scores.'
        self.assertEqual(res[0]['title'], 'Iran claims nuclear fuel advance, test-fires missile in gulf', message)


if __name__ == '__main__':
    unittest.main()
