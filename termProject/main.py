#!/usr/bin/python3.9

# hw5.py
# Version 1.0.0
# 4/3/2022

import argparse
from pydoc import doc
import unittest
import subprocess

from user_search import Engine
from embedding_service.text_processing import TextProcessing
import test_hw5

from flask import Flask, render_template, request       # type: ignore
from elasticsearch import Elasticsearch                 # type: ignore

search_client = Elasticsearch()

pages = {}
PAGE_NUM, TOTAL_PAGES = 1, 0

app = Flask(__name__)
user_search: "Engine"
text_processor = TextProcessing.from_nltk()

def limit_content(content: str) -> str:
    return f'{content[:350] if len(content) > 350 else content} ...'


class FlaskApp:
    """Backend Flask App """
    # home page
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
    parser = argparse.ArgumentParser(description="VS IR system")
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    if args.build:
        subprocess.call('./build.sh', shell=False)
        
        print(('='*100)+'\n'+('='*100)+'\nES index constructed and all listeners ACTIVE :)\n'+('='*100)+'\n'+('='*100)+'\n\n\n\n....\n\n\n\n')
    if args.test:
        # write test suite and switch below
        
        print(f'-'*60,f'\nRunning Test Suite...\n\n', f'-'*60)
        suite = unittest.TestLoader().loadTestsFromModule(test_hw5)
        unittest.TextTestRunner(verbosity=3).run(suite)
        
    if args.run:
        
        app.run(debug=True, port=5000)
