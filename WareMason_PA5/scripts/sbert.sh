#!/bin/sh

python3.9 -m embedding_service.server --embedding sbert  --model msmarco-distilbert-base-v3
