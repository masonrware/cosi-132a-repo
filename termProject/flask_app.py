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
import argparse
import math

app = Flask(__name__)

connections.create_connection(hosts=["localhost"], timeout=100, alias="default")  # create connection

pages = {}
engine = None
NUM_PER_PAGE = 10
num_res = 0
page = 1
query = ""

@app.route("/")
def home():
    """
    This is the home page for the website, which has the functionality for searching Washington Post articles.
    @return: renders the html template for the home page, which creates the search box and submit button.
    """
    return render_template("home.html")


# result page
@app.route("/results", methods=["POST"])  # put back after testing
def results():
    global pages, engine, num_res, query
    query = request.form["query"]
    print(query)

    engine = Engine("wapo_docs_50k", query, 60)
    response = engine.search()

    pages = {}
    num_res = len(response)
    num_pages = math.ceil(num_res/ NUM_PER_PAGE)

    for i in range(num_pages):
        pages[i + 1] = [[hit.doc_id, hit.title, hit.review[:250] + "..."] for hit in
                        response[i * NUM_PER_PAGE: min(num_res, (i * NUM_PER_PAGE) + NUM_PER_PAGE)]]

    curr_page = pages[1] if len(pages) > 0 else []

    return render_template("results.html", page=page, num_res=num_res, doc_results=curr_page)


@app.route("/results/<int:page_id>, query", methods=["POST"])
def next_page(page_id):
    global pages, num_res, page
    page = page_id
    return render_template("results.html", page=page, num_res=num_res, doc_results=pages[page_id])


@app.route("/review_data/<int:review_id>")
def review_data(review_id):
    global engine, page

    response = engine.general_search(Match(doc_id={"query": review_id})).hits[0]
    title, content = response.title, response.review

    # need better way to split words, also need better way to get stems of words
    content = content.split(" ")
    word_queries = query.split(" ")
    content = " ".join(["<mark>" + word + "</mark>" if word in word_queries else word for word in content])

    return render_template("review.html", content=content, title=title, page_id=page, sentiment=9)

@app.route("/sentimovie")
def sentimovie():
    """
    This is the home page for the website, which has the functionality for searching Washington Post articles.
    @return: renders the html template for the home page, which creates the search box and submit button.
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
