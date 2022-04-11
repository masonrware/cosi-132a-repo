#!/bin/sh

./scripts/elastic.sh
./scripts/sbert.sh
./scripts/fastText.sh

# bash -e ../elasticsearch-7.10.2/bin/elasticsearch &
# bash -e python3.9 -m embedding_service.server --embedding fasttext  --model pa5_data/wiki-news-300d-1M-subword.vec &
# bash -e python3.9 -m embedding_service.server --embedding sbert  --model msmarco-distilbert-base-v3 &
# python3.9 load_es_index.py --index_name wapo_docs_50k --wapo_path pa5_data/subset_wapo_50k_sbert_ft_filtered.jl

#SBATCH -N 9
#SBATCH -t 0:15:00

# srun --hint=nomultithread -N 2 --ntasks=64 --ntasks-per-node=32 --ntasks-per-socket=16 ./elastic.sh
# srun --hint=nomultithread –N 3 --ntasks=96 --ntasks-per-node=32 --ntasks-per-socket=16 ./fastText.sh
# srun --hint=nomultithread -N 4 --ntasks=128 --ntasks-per-node=32 --ntasks-per-socket=16 ./sbert.sh