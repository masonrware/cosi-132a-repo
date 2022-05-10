#############################
##  The following are some 
##  commands that need to be 
##  run before interaction.
#############################

# ALL CMDS ARE ASSUMING YOU ARE 
# IN THE ROOT DIR OF THE PROJECT


# To install all requirements:
pip3 install -r requirements.txt

# To host the sbert embedding service locally
python3.9 -m embedding_service.server --embedding sbert  --model msmarco-distilbert-base-v3

# To start a local server instance of elasticsearch
./elasticsearch-7.10.2/bin/elasticsearch

# ONLY ONE OF BELOW TWO:
    # To build an es index named movie_reviews based on final_movies.jl (needs to be downloaded see README.md)
    python3.9 load_es_index.py --index_name movie_reviews --path data/final_movies.jl

    # To build a test es-index for purpose of demoing
    python3.9 load_es_index.py --index_name movie_reviews --path data/sample_data/movies.jl

# To start and host the flask app
python3.9 flask_app.py --run