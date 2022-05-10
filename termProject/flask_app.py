#!usr/bin/python3

# flask_app.py
# Version 2.0.0  (?)
# 4/20/22

# Written By: Sarah Kosowsky


## This module implements a Flask Application that supports user queries about movies. Using elastic search
## and Mongo DB, this application returns relevant movie reviews back to the user.


from pathlib import Path
from query import Engine
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.query import Match
from flask import Flask, render_template, request
from nltk.tokenize import word_tokenize
import argparse
import math

from logistic_regression import LogisticRegression

app = Flask(__name__)

connections.create_connection(hosts=["localhost"], timeout=100, alias="default")  # create connection


pages = {}  # dictionary to hold pages of results
engine = None
NUM_PER_PAGE = 10  # number of results displayed per page to use
num_res, page, query = 0, 1, ""

@app.route("/")
def home():
    """
    This is the home page for the website, which has the functionality for searching movie reviews.
    @return: renders the html template for the home page, which creates the search box and submit button.
    """
    return render_template("home.html")


# result page
@app.route("/results", methods=["POST"])
def results():
    """
    The result page shows up to ten results of the search results of the input query. When applicable, users can use the
    next and prev buttons to look through result pages. The page also includes the functionality to search again. Users
    can click on the reviews to read more about them.
    @return: renders the html results template, which displays the title and the first 250 chars of the content for
    each search match.
    """
    global pages, engine, num_res, query, page

    query = request.form["query"]  # get user query

    engine = Engine("movie_reviews", query, 60)
    response = engine.search()  # query ES index

    pages = {}
    page = 1
    num_res = len(response)
    num_pages = math.ceil(num_res/ NUM_PER_PAGE)  # determine total number of pages

    for i in range(num_pages):  # store 10 reviews per page
        pages[i + 1] = [[hit.doc_id, hit.title, hit.review[:250] + "..."] for hit in
                        response[i * NUM_PER_PAGE: min(num_res, (i * NUM_PER_PAGE) + NUM_PER_PAGE)]]

    curr_page = pages[1] if len(pages) > 0 else []  # set doc_results to empty list if no results found

    return render_template("results.html", page=page, num_res=num_res, doc_results=curr_page, query=query)


@app.route("/results/<int:page_id>, query", methods=["POST"])
def next_page(page_id):
    """
    "next page" gets and displays the doc info for up to 10 more search results to the user.
    @param page_id: page_id is the number of the next page. If it's the second page of results, page_id=2.
    @return: renders the results html, with up to 10 more reviews. Page number is incremented while next_page
    is called in results.html.
    """
    global pages, num_res, page, query
    page = page_id  # set page number globally

    return render_template("results.html", page=page, num_res=num_res, doc_results=pages[page_id], query=query)


@app.route("/review_data/<int:review_id>")
def review_data(review_id):
    """
    The review page for the website, which shows a movie review's full content (title, content, and sentiment score).
    @param doc_id: The document id of the review the user wants to see
    @return: renders the template for the doc html file, which displays the document, with the searched keywords
    highlighted, and the review's sentiment score to the user.
    """
    global engine, page

    response = engine.general_search(Match(doc_id={"query": review_id})).hits[0]  # look up info about review
    title, content = response.title, response.review

    # split content and word_queries , so that highlighting could be done for keywords
    content = word_tokenize(content)
    word_queries = word_tokenize(query)
    word_queries = [word.lower() for word in word_queries]
    
    content = " ".join(["<mark>" + word + "</mark>" if word.lower() in word_queries else word for word in content])

    # lr_model = LogisticRegression(n_features=4) # ? not sure what num to put here
    # sentiment = lr_model.classify(title + " " + content)  # change when mongodb is set up
    sentiment = 9 # arbitrary
    return render_template("review.html", content=content, title=title, page_id=page, sentiment=sentiment)

@app.route("/sentimovie")
def sentimovie():
    """
    This is the home page for the sentimove feature of the website, which will have the functionality to find movies
    similar in sentiment to inputted movies. This feature is part of our next steps.
    @return: renders the html template for the sentimovie page, which is "coming soon".
    """
    return render_template("sentimovie.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MovieRealView system")

    # parser.add_argument("--build", action="store_true")  # are we building index here?
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()

    # if args.build:
    # build inverted index here
    if args.run:
        app.run(debug=True, port=5000)
