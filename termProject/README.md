    

PA5
===

COSI 132A -- Brandeis University
================================

##### Professor Peter Anick

###### Date: 05/09/22

* * *

### Description

*RealView Movie Search Engine*

This project is intended to serve as a complex movie search engine. It works by hosting a flask app front end and an elasticsearch backend. Utilizing indexed documents and their vectors, the engine is able to compare the user's query against movie reviews from sources across the internet.

### Engine

* `flask_app.py`

`flask_app.py` implements a flask app so that it can obtain a raw query string that is
used to instantiate the Engine class present in `query.py` with the specified arguments. This is then searched upon and it's results are retrieved. Using Okami BM25 and reranking based on document sbert vectors, ranked documents are returned and rendered in the html files located in the `templates/` subdir, per Flask standards.

### Querying

* `query.py`

In `query.py`, an Engine instance is created to represent one search instance. Using the kwargs provided, the program runs the `search` method which first generates queries based on the original user query and some enhancements. After this is done, one query is chosen and that query is used for searching against the es-index. Next, sbert embeddings are created and used in rerank.

* `re_rank`

The function `re_rank` is present in the global space of `query.py`. It makes use of the `Search()` method provided by the elasticsearch API. Retrieving a full response from the es instance, this method uses the `.extra()` modifier to rescore the results according to a provided vector. 


### Dependencies

* elasticsearch==7.17.2
* elasticsearch_dsl==7.4.0
* googletrans==3.1.0a0
* nltk==3.7
* numpy==1.22.3
* pandas==1.4.1
* pyenchant==3.2.2
* pynytimes==0.8.0
* python-dotenv==0.20.0
* pyzmq==22.3.0
* requests==2.25.1
* sentence_transformers==2.2.0
* tqdm==4.61.2


All dependencies can be found in the `./requirements.txt` file. Moreover, they can be automatically installed using the shell command: `pip install -r requirements.txt` and the most up to date versions of the dependencies can be installed using the shell command: `pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U` .


* * *

Build & Run
-----------

### Build Instructions

Navigate to the file: `start.sh` to refer to some boilerplate scripts that start the service's required build.

There are multiple services that need localhosting including the flask app itself as well as some sample queries.

### Run Instructions

In order to run the search engine, enter the command `python3.9 flask_app.py --run`. This will start a flask server on you localhost, so check your browser.

* * *

### Testing

In order to test this program, we ran random queries against our test set of documents present at `data/sample_data`. These queries included:

* Life Love Happiness
* Epic Hero Explosions
* Pretty animation
* War hardship
  
These queries highlight the strengths and weeknesses of our engine, reflected in the idea that there are not a lot of source documents to begin with.

* * *

_© 2022 MASON WARE_

