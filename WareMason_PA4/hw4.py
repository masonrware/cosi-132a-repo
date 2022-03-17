#!/usr/bin/python3

# hw4.py
# Version 2.0.0
# 3/14/2022

from pathlib import Path
import argparse
import time
import unittest
from flask import Flask, render_template, request
from utils import load_wapo
from inverted_index import build_inverted_index, query_inverted_index
from mongo_db import db, insert_docs, query_doc
import test_hw4


pages = {}
PAGE_NUM, TOTAL_PAGES = 1, 0

app = Flask(__name__)

data_dir = Path(__file__).parent.joinpath("pa4_data")
wapo_path = data_dir.joinpath("wapo_pa4.jl") ##!change file here

if not "wapo_docs" in db.list_collection_names():
    insert_docs(load_wapo(wapo_path))

def limit_content(content: str) -> str:
    return content[:150] if len(content) > 150 else content


class FlaskApp:
    """Backend Flask App """

    @app.route("/")
    def home():
        """home page"""
        return render_template("home.html")

    @app.route("/results", methods=["POST"])
    def results():
        """results page"""
        # persisting data
        global postings_list
        global stop_words
        global unknown_words
        global query_text

        query_text = request.form["query"]  # Get the raw user query from home page
        res = []
        dict_ind = 1

        postings_list, stop_words, unknown_words = query_inverted_index(query_text, 30) # k = 30

        if len(postings_list) != 0:
            for posting in postings_list:
                document = query_doc(posting[0])
                item_dict = {
                    'title': document['title'],
                    'published_date': document['published_date'],
                    'content': limit_content(document['content_str']) + '...',
                    'id': document['id']
                }
                res.append(item_dict)
                if len(res) == 8:  # limit page length to 8 results
                    pages[dict_ind] = res
                    res = []
                    dict_ind += 1
            TOTAL_PAGES = dict_ind
            if len(res) != 0:  # catch any overflow on last page
                pages[dict_ind] = res
            return render_template("results.html", response=pages[1], query=query_text, stop_words=stop_words,
                                   unknown_words=unknown_words,
                                   PAGE_NUM=PAGE_NUM, TOTAL_PAGES=TOTAL_PAGES)  # render results on results page
        else:
            return render_template("errorResults.html", query=query_text, stop_words=stop_words,
                                   unknown_words=unknown_words,
                                   PAGE_NUM=1, TOTAL_PAGES=1)  # render error page

    @app.route("/results/<int:page_id>/prev", methods=["GET", "POST"])
    def prev_page(page_id: int) -> str:
        """"previous page"to show more results"""
        PAGE_NUM = page_id
        return render_template("results.html", response=pages[PAGE_NUM], query=query_text, stop_words=stop_words,
                               unknown_words=unknown_words,
                               PAGE_NUM=PAGE_NUM, TOTAL_PAGES=len(pages))  # render results page with persisting data

    @app.route("/results/<int:page_id>/next", methods=["GET", "POST"])
    def next_page(page_id: int) -> str:
        """"next page" to show more results"""
        PAGE_NUM = page_id
        return render_template("results.html", response=pages[PAGE_NUM], query=query_text, stop_words=stop_words,
                               unknown_words=unknown_words,
                               PAGE_NUM=PAGE_NUM, TOTAL_PAGES=len(pages))  # render results page with persisting data

    @app.route("/doc_data/<int:doc_id>")
    def doc_data(doc_id):
        """individual document page"""
        doc_image = query_doc(doc_id)
        return render_template("doc.html", document=doc_image)  # render a document page


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VS IR system")
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    if args.build:
        build_inverted_index(load_wapo(wapo_path))
        print('\n'+'='*60+'\nbuild completed successfully :)\n'+'='*60)
    if args.test:
        print(f'-'*60,f'\nRunning Test Suite...\n\n', f'-'*60)
        suite = unittest.TestLoader().loadTestsFromModule(test_hw4)
        unittest.TextTestRunner(verbosity=3).run(suite)
        time.sleep(3)   # delay is to help visuals
        print(f'-'*60,f'\nstarting construction of test database...\n', f'-'*60)
        build_inverted_index(load_wapo('pa4_data/test_data_pa4.jl'), flag='test')
        print(f'-'*60,f'\ntest database contruction finished :)\n', f'-'*60)
        app.run(port=5001)
    if args.run:
        app.run(debug=True, port=5000)
