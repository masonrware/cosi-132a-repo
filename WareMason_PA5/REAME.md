    

PA5
===

COSI 132A -- Brandeis University
================================

##### Professor Peter Anick

###### Date: 04/11/22

* * *

### Description

This program interacts with two services, located at `embedding_service` and `es_service`, respectively. The first serves to provide both fastText and sBERT word embeddings
and the second works to host an elasticsearch server on your local instance. The heart of the program lies in `evaluate.py`/`user_search.py` and `hw5.py`. The reason for the
forward slash between `evaluate.py` and `user_search.py` is because for all intents and purposes these are the same module - they both serve to search any kind of retrieved
query against the elasticsearch instance. The difference between the two is that the first is geared towards the evaluation of the engine and SEO and the second is actually
used to produce search results for the flask app. As such, `evaluate` has a client in it as well and outputs its results differently. Due to the fact that `evaluate` is geared towards generating tabulated and recorded results, it is not perfectly indicative of the actual inner-workings of the searching done in this program. Therefore, I will be discussing only the code found in `user_search.py` when discussing the program's interaction with elasticsearch.

The following are the main components of the program:

### `hw5.py`

`hw5.py` implements a flask app so that it can obtain a raw query string and some specifications about which retrieval method to use. Once these attributes are recorded, that are
used to instantiate the Engine class present in `user_search.py` with the specified arguments. This is then searched upon and it's retrieved, ranked documents are returned and
rendered in the html files located in the `templates/` subdir, per Flask standards.

### Querying

* `user_search.py`

As stated earlier, almost all the aspect of `user_search`'s searching and interacting with the elasticsearch instance to retrieve results discussed in the following description holds for `evaluate.py`. The difference comes in output.

In `user_search`, an Engine instance is created to represent one search instance. Using the kwargs provided, the program runs the `search` method which first generates queries based on the original user query and some enhancements
depending on the analyzer they chose. After this is done, one query is chosen and that query is used for searching the index. Next, embeddings are created regardless of the retrieval method depending on the type of vector name provided
(default is sbert). 

Then, if the user specified a search type, it will be chosen via some logic gates and once that is done, the `rank` or `re_rank` methods are called, depending on the retrieval method.
  
* `rank` & `re_rank`

The functions `rank` and `re_rank` are both present in the global space of `user_search.py`. They make use of the `Search()` method provided by the elasticsearch API. Retrieving a full
response from the es instance, these methods either return it, in the case of `rank`, or they use the `.extra()` modifier to rescore the results according to a provided vector. 


### Dependencies

1. elasticsearch==7.17.1
2. elasticsearch_dsl==7.4.0
3. Flask==2.0.2
4. nltk==3.5
5. numpy==1.22.3
6. pyzmq==22.3.0
7. sentence_transformers==2.2.0
8. tqdm==4.61.2

All dependencies can be found in the `./requirements.txt` file. Moreover, they can be automatically installed using the shell command: `pip install -r requirements.txt` and the most up to date versions of the dependencies can be installed using the shell command: `pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U` .


* * *

Build & Run
-----------

### Build Instructions

[!DEPRECATED]In order to build the index and start the services required for interacting with the program, run the command `python3.9 hw5.py --build` while located in the root directory of the project. 

Alternatively, you can navigate to the file: `scripts.sh` to refer to some boilerplate scripts that start the service's required build.

### Run Instructions

In order to run the search engine, enter the command `python3.9 hw5.py --run`. This will start a flask server on you localhost, so check your browser.

* * *

### Testing

To test this program, I wrote unit tests for each major class and utility in the program aside from the database methods (as I am not sure how to test the pymongo methods). These tests are stored in the file: `test_hw5.py` and can be run from the terminal using the command: `python3.9 test_hw5.py`. This will prompt the test suite to run, running all the tests in multiple `unittest.TestCase` instances. If any fail, they will be conveniently displayed in the terminal with the initial exact difference marked.

Alternatively, this program is designed to be able to be controlled entirely from within `hw5.py`. Therefore, one can enter the command `python3.9 hw5.py --test` to run the test suite as well.

_© 2022 MASON WARE_