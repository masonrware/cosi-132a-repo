    

PA4
===

COSI 132A -- Brandeis University
================================

##### Professor Peter Anick

###### Date: 02/26/22

* * *

### Description

This program is a search engine that uses Washington Post articles stored in `pa4_data/wapo_pa4.jl`. Utilizing a Flask backend, the engine takes a user query, normalizes, stems, and tokenizes the text and then compares the set of words against an inverted index. Before the application can be deployable and runnable, a database containing collections of documents and the inverted index itself must be made in order for the user to be able to continually search. The program does this with the `--build` option command. 

Once that command is run, the program will construct an inverted index with keys of every stemmed and normalized term in the corpora and values of lists
of tuples of every document that term appears in and the tf of that term in the document. This will be inserted into a local db under the alias vs_index
alongside another index titled doc_length_index. This collection, as can probably be deduced, has keys of doc ids and values of cosine-normalized lengths of each document.

###   Term Processing

The program has one class for term processing:

###   `term_processing.py`

This class houses the following methods:

*   `def normalize(self, token: str) -> str:`

This method takes a token representing an individual word and normalizes it. It does so by first lower casing the token, then it removes all non alpha-numeric and non dash characters using the regex expression: `'[^a-zA-Z0-9 -]'`. Lastly, it checks the token's length and whether or not the token is in a list of stopwords (Stop words in `text_processing.py` are imported from the natural language toolkit module). Should the token be of length 1 or be a stop word, then the string `''` is returned.

*   `def get_normalized_tokens(self, title_: str = " ", content_: str = " ") -> Set[str]:`

This method takes both a title and content str of an article as arguments and normalizes all of the tokens in each string. Notice that the arguments are given default values of empty strings as there are instances where the same code is used to normalize, for instance, the user query and therefore, any insufficient positional argument errors are avoided. This method first uses the nltk `word_tokenizer` class to tokenize the two strings. Next, each token in both sets are normalized and added to a set representing the desired output: a set of all normalized words in both the title and content.
  
This class also houses two static methods: `def idf() and def tf()`. These methods are used to find the inverse document frequency and the term frequency, respectively. They are smoothed values, found using a logarithm base 2.
  
###   Inverted Index

The program builds an inverted index and uses it to implement to db collections, vs_index and doc_len_index, using the class housed in `inverted_index.py`.

*   `inverted_index.py`

This file contains a class of the same name: `InvertedIndex` that represents the data structure itself. The class contains the following methods:

*   `def index_document(self, document: dict) -> None:`

This method is used to insert a document and all of its terms into the inverted index. Using the dictionary representing the document, the method utilizes the method `get_normalized_tokens()` from the `text_processing.py` file in order to normalize the title and content of the document. Then, iterating over the returned set of words, the program either adds an unseen token to the internal data structure: `appearances_dict`, as a key along with a value of a list containing tuples of the document ids and tfs of the term currently being looked at.

*   `def load_index_postings_list(self) -> None:`

This method is used to load the index into a format that is required by the rest of the program. Specifically, when inserting the index into a database, the easiest way to do so is to group all of the items in appearances dict separately and append them to a list. That way all of the contents of the index are accessible in an iterable object.

Outside of the class, there exist the following methods for interacting with the data structure:

*   `def build_inverted_index(wapo_docs: Iterable) -> None:`

This method is used to construct an inverted index and insert it into the database. Using the iterable argument that represents each individual document, the program indexes each document in the collection. After this is done, the method `insert_vs_index()` is used to insert the index into a mongo database. The list discussed earlier is used to represent the index and it is passed as a descendingly sorted index.

*   `def parse_query(query: str) -> Tuple[List[str], List[str], List[str]]:`

This method parses a query by utilizing the text processor built off of the TextProcessor class housed in `text_processing.py`. It also finds the stop words and unknown words and returns all three: the query, stop words, and unknown words. It retains a list of stop words by comparing the tokens in the normalized query to the normalized tokens in the non normalized query. It retains a list of unknown words by comparing the tokens in the normalized query with the index's keys.

*   `def top_k_docs(doc_scores: Dict[int, float], k: int) -> List[Tuple[float, int]]:`

This method implements a heapq on a list using the python package heapq. First, the method build the heap, then it heapifys it, and lastly it extracts the k largest documents, provided as an argument.

*   `def query_inverted_index(query: str) -> Tuple[List[int], List[str], List[str]]:`

Finally, this method is the powerhouse of the engine. It queries the database for document information and returns all of the relevant documents as well as a list of stop words and unknown words. Using the user's query, the method normalizes its tokens and finds all alphanumeric and dash characters using the method parse_query, discussed above. It then iterates over each term in the normalized query, querying its postings list from the db in the collection vs_index. Using this list of tuples of doc ids and tf scores, the method then calculates the idf of the respective document and term relationship. The tf-idf score is calculated by first multiplying the tf score of the given posting with the idf of entire data set and the length of the individual postings list. Next, a helper method `cosine_sim()` is used to calculate the cosine similarity of a document to the query. It does so by taking the previously calculated tf-idf score and the tf score of the document and divides their product by the product of the query length and the document length. Finally, it adds this calculated value to a dictionary called `doc_scores` where the keys are doc ids and values are cosine similarity scores. This dictionary gets passed to `top_k_scores` and then a reutrnable product is sent to `hw4.py` in order for the flask backend to render the results.


###   Mongo Database

The program necessitates persistent storage so that a user may load the application, exit, and reload and still be able to access the same data. In order to do so with the most ease and transparency, we use mongoDB's service. The methods related to building and querying from the database are housed in the file `mongo_db.py`.

The following are it's methods:

*   `def insert_docs(docs: Iterable) -> None:`

This method is used to construct the collection of the database representing all of the documents. This, in turn, allows us to access a document's data in constant time. It works by taking advantage of the pymongo class and creates a new db collection entitled `wapo_docs`. Iterating through the passed iterable of documents, it adds each sequentially in linear time - it takes around 9 minutes for me to index 27,000 documents on a MacBook Pro (13-inch, 2020, 1.4 GHz Quad-Core Intel Core i5, 16 GB 2133 MHz LPDDR3 RAM).

*   `def insert_vs_index(index_list: List[Dict]) -> None:`

This method does the same as above but it inserts each index to postings list/tf scores pairing of the inverted index into the database. It creates a new collection entitled: `inverted_index` and fills that with the items of the iterable argument.

*   `def insert_doc_len_index(index_list: List[Dict]) -> None:`

This method is used to insert the document cosine-normalized scores into a db collection. 


*   `def query_doc_len_index(doc_id: int) -> Dict:`

This method querys the database for an float representing the cosine-normalized length of a document. It queries by document id.

*   `def query_doc(doc_id: int) -> Dict:`

This method queries the database for a document using its unique id. It returns null if no document is found.

*   `def query_vs_index(token: str) -> Dict:`

This method queries the database for a postings list via a token

  

### Dependencies

1.  `Flask==2.0.2`
2.  `pymongo`
3.  `nltk==3.5`

All dependencies can be found in the `./requirements.txt` file. Moreover, they can be automatically installed using the shell command: `pip install -r requirements.txt` and the most up to date versions of the dependencies can be installed using the shell command: `pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U` .

  

* * *

Build & Run
-----------

### Build Instructions

In order to build the database collections with the data contained in `pa3_data/wapo_pa3.jl`, one must navigate to the root directory of this project and run the command: `python3 hw3.py --build`. This will create an inverted index. Once that is finished, you can move onto running the program and deploying the Flask application.

### Run Instructions

In order to run the app in your browser locally, enter the command: `python3 hw3.py --run`. This will start the Flask app at your localhost on port 5000, if it is free, in debug mode. However, before that happens, if it hasn't already, the collection for the documents is created. Once a collection named `wapo_docs` is present in the database, the flask app will start.

* * *

### Testing

To test this program, I wrote unit tests for each major class and utility in the program aside from the database methods (as I am not sure how to test the pymongo methods). These tests are stored in the file: `test_hw3.py` and can be run from the terminal using the command: `python3 test_hw3.py`. This will prompt the test suite to run, running 7 total tests in multiple `unittest.TestCase` instances. If any fail, they will be conveniently displayed in the terminal with the initial exact difference marked. For example, if one were to change the assertion statement on line `32` of the file to this: `self.assertDictEqual(invidx.appearances_dict, {'bodi': [1], 'titl': [1], 'sampl': [2]}, message)`, and ran the test suites, one would get the following response from the tests:  
`$ python3 test_hw3.py   ..F....   ======================================================================   FAIL: test_index_document (__main__.TestInvertedIndex)   A document is indexed into the appearances dictionary correctly.   ----------------------------------------------------------------------   Traceback (most recent call last):   File "test_hw3.py", line 32, in test_index_document   self.assertDictEqual(invidx.appearances_dict, {'bodi': [1], 'titl': [1], 'sampl': [2]}, message)   AssertionError: {'titl': [1], 'bodi': [1], 'sampl': [1]} != {'bodi': [1], 'titl': [1], 'sampl': [2]}   - {'bodi': [1], 'sampl': [1], 'titl': [1]}   ? ^      + {'bodi': [1], 'sampl': [2], 'titl': [1]}   ? ^   : Inverted Index DS does not load appearances dict correctly      ----------------------------------------------------------------------   Ran 7 tests in 0.023s      FAILED (failures=1)   `

_© 2022 MASON WARE_