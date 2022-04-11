#!/bin/sh

python3.9 -m embedding_service.server --embedding fasttext  --model pa5_data/wiki-news-300d-1M-subword.vec
