#!/bin/sh

#bm25 w/out eng ana
python3.9 evaluate.py --index_name wapo_docs_50k --topic_id 336 --query_type kw --top_k 20
python3.9 evaluate.py --index_name wapo_docs_50k --topic_id 336 --query_type nl --top_k 20

#bm25 w/ eng ana
python3.9 evaluate.py --index_name wapo_docs_50k --topic_id 336 --query_type kw --top_k 20 --use_english_analyzer
python3.9 evaluate.py --index_name wapo_docs_50k --topic_id 336 --query_type nl --top_k 20 --use_english_analyzer

#vector with sbert
python3.9 evaluate.py --index_name wapo_docs_50k --topic_id 336 --query_type kw --top_k 20 --search_type vector --vector_name sbert_vector
python3.9 evaluate.py --index_name wapo_docs_50k --topic_id 336 --query_type nl --top_k 20 --search_type vector --vector_name sbert_vector

#rerank w/ sbert (uses eng ana by default)
python3.9 evaluate.py --index_name wapo_docs_50k --topic_id 336 --query_type kw --top_k 20 --search_type rerank --vector_name sbert_vector
python3.9 evaluate.py --index_name wapo_docs_50k --topic_id 336 --query_type nl --top_k 20 --search_type rerank --vector_name sbert_vector

#rerank w/ fastText (uses eng ana by default)
python3.9 evaluate.py --index_name wapo_docs_50k --topic_id 336 --query_type kw --top_k 20 --search_type rerank --vector_name ft_vector
python3.9 evaluate.py --index_name wapo_docs_50k --topic_id 336 --query_type nl --top_k 20 --search_type rerank --vector_name ft_vector
