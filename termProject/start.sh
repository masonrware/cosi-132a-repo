pip3 install -r requirements.txt
# python3 main.py

# load fasttext embeddings that are trained on wiki news. Each embedding has 300 dimensions
python3.9 -m embedding_service.server --embedding fasttext  --model data/wiki-news-300d-1M-subword.vec

# load sentence BERT embeddings that are trained on msmarco. Each embedding has 768 dimensions
python3.9 -m embedding_service.server --embedding sbert  --model msmarco-distilbert-base-v3

# load wapo docs into the index called "wapo_docs_50k"
python3.9 load_es_index.py --index_name wapo_docs_50k --path data/final_unique_movie_data.jl

# use keyword from topic 363 as the query; search over the stemmed_content field from index "wapo_docs_50k" based on BM25 and compute NDCG@20
python3.9 evaluate.py --index_name wapo_docs_50k --topic_id 363 --query_type kw --use_english_analyzer --top_k 20

# use natural language from topic 363 as the query; search over the stemmed_content field from index "wapo_docs_50k" based on sentence BERT embedding reranking query and compute NDCG@20
python3.9 evaluate.py --index_name wapo_docs_50k --topic_id 363 --query_type nl --vector_name sbert_vector  --top_k 20  --search_type rerank
