    

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

*THERE ARE NEEDED DOCUMENTS BELOW*

Some documents are too large to push to github (elasticsearch and our final jl data). You can find these documents for download here: (https://drive.google.com/drive/folders/1IenUta2TFhF8Brb_rkYoIzzeAdy1nWsr?usp=sharing)

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
* Flask==2.0.2
* googletrans==3.1.0a0
* nltk==3.7
* numpy==1.22.3
* pandas==1.4.1
* pyenchant==3.2.2
* pynytimes==0.8.0
* python-dotenv==0.20.0
* pyzmq==22.3.0
* requests==2.25.1
* scipy==1.8.0
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

In order to run the search engine, enter the command `python3.9 flask_app.py --run`. This will start a flask server on you localhost, so check your browser (http://127.0.0.1:5000).
The home page allows the user to search for keywords that they would like to see in a movie review. If users do not provide keywords to the system, then upon pressing the submit button, the system will alert the user to fill out the search box. On the home page, the user could also use the navbar, but it is not as useful on the home page since both the logo and 'home' link to the home page. Search is done by querying the ES index using reranking with sbert embeddings and the standard analyzer.

After searching for keywords, the system returns a result page to the user. Ten results are shown at a time because we did not want a user to have to scroll so much but we also did not want them to have to go through tons of pages. Each result shows the title of the movie review and 250 characters of the review content, so that the user could get a sense of the review before clicking on it. If the user wants to read more about the review, they could click on the title or content to go to the review page. If the user wants to look at more reviews, they could use the 'next' button, which is enabled when there are more results available. After navigating to another page, the user could use the 'prev' button to navigate to the previous page. In total 60 results are retrieved because we do not expect that users would look through more than that many reviews. The user could also use the navbar to naviagte home.

If the user click on a review, they will be directed to the review page, which displays the title, sentiment score, and full content of the review. The sentiment score represents the sentiment of all reviews documented for a movie in our corpus. It is on a scale from 0 to 1. The higher the score is, the higher people's opinion on the movie is. Users can hover over their mouse 'sentiment score' to learn more about what it means. From the review page, users can use the 'back to results' button to navigate back to the results page. They can also use the navbar to navigate back home.

The navbar also has an option to navigate to 'sentimovie', which is a page that we hope to work on in the future. For now, it has a template of the page, with a banner indicating that the feature is coming soon.


* * *

### Testing

In order to test this program, we ran random queries against our test set of documents present at `data/sample_data`. These queries included:

* Life Love Happiness
* Epic Hero Explosions
* Pretty animation
* War hardship
  
These queries highlight the strengths and weeknesses of our engine, reflected in the idea that there are not a lot of source documents to begin with.

We also carefully tested our system by ensuring that our features worked properly. We ensured that the navbar linked to the correct pages and that the search bar in the navbar was functional. We also tested to ensure that users could not search without input. We also made sure that the reviews themselves were clickable and that they brought the user to the correct review. Lastly we checked that the "prev" and "next" buttons were enabled when there were prev/next pages and disabled when there were not.

* * *

### Examples of queries/interactions that work over the test subset:

* buddy adventure comedy
* heartwarming and uplifiting
* great car chase (sentiment)
* spy thrillers

* * *

### Code submitted by:
Mason Ware

* * *

Team Member Contributions:
-----------

### Drew Gottlieb

### Jordan Blatter

### Mason Ware
I was responsible for sourcing our data. This included not only collecting data from api calls but also generating the final json data that our es-index is built upon. In addition to the data itself, I was responsible for designing and implementing the entire data pipeline, from source file, to jl file, to es-index. This required me include elasticsearch services tailored to our final movie data. Outside of these tasks, I aided in project management - often setting deadlines and motivating team members. Lastly, I helped maintain any and all documentation for this project including the dependencies and inline code comments.

### Sarah Kosowsky

 I was primarily responsible for the user interface. I made the flask application to handle user queries. I also edited the query.py code to use reranking with sbert embeddings for querying the ES index. In addition to making the flask routes, I also made all of the html files and spent lots of time trying to make the user experience as seamless as possible. I made “prev” and “next” buttons so that users could go back and forth between the result pages. I also added a navigation bar so that users could easily access the home page. On the review page I added a hover feature for the sentiment score, so that users could hover over the text to learn more about the meaning of a sentiment score. In addition to the html itself, I also used a lot of inline css coding. I also tested the system many times by testing both edge cases and simple queries. I also worked on demo-ing the system for the final presentation. Lastly, I created and designed our team’s logo and I made all of the presentation skeletons.

* * *

_© 2022 MASON WARE_

