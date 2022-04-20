#!usr/bin/python3

# flask_app.py
# Version 2.0.0  (?)
# 4/20/22

# Written By: Sarah Kosowsky


## This module implements a Flask Application that supports user queries about movies. Using elastic search
## and Mongo DB, this application returns relevant movie reviews back to the user.


from pathlib import Path
import argparse
from flask import Flask, render_template, request

app = Flask(__name__)

doc_results = []  # list that will contain all relevant docs for a certain query


@app.route("/")
def home():
    """
    This is the home page for the website, which has the functionality for searching Washington Post articles.
    @return: renders the html template for the home page, which creates the search box and submit button.
    """
    return render_template("home.html")


# result page
@app.route("/results", methods=["POST"])
def results():
    global doc_results
    query = request.form["query"]
    doc_results = []  # query index based on query, save result ids in doc_results for next page queries

    return render_template("results.html")


@app.route("/results/<int:page_id>, query", methods=["POST"])
def next_page(page_id):
    global doc_results

    offset = 10 * (page_id - 1)  # calculate offset for current page
    docs = doc_results[offset: min(offset + 10, len(doc_results))]  # get next ten result ids

    # get info about the next 10 ideas

    return render_template("results.html")


@app.route("/review_data/<int:review_id>")
def review_data(review_id):
    doc = 0  # query database using review id

    # go through data retrieved and get info to show to user

    return render_template("doc.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MovieRealView system")

    # parser.add_argument("--build", action="store_true")  # are we building index here?
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()

    # if args.build:
        # build inverted index here
    if args.run:
        app.run(debug=True, port=5000)
