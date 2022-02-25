#!/usr/bin/env python3

# hw3.py
# Version 1.0
# 2/23/2022

from pathlib import Path
import argparse

from flask import Flask, render_template, request

from utils import load_wapo
from inverted_index import build_inverted_index, query_inverted_index
from mongo_db import db, insert_docs, query_doc

app = Flask(__name__)

data_dir = Path(__file__).parent.joinpath("pa3_data")
wapo_path = data_dir.joinpath("wapo_pa3.jl")

pages = {}
PAGE_NUM, TOTAL_PAGES = 1, 0

if "wapo_docs" not in db.list_collection_names():
    insert_docs(load_wapo(wapo_path))


def limit_content(content: str) -> str:
    return content[:150] if len(content) > 150 else content


class FlaskApp:
    """Backend Flask App. """

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

        postings_list, stop_words, unknown_words = query_inverted_index(query_text)

        if len(postings_list) != 0:
            for posting in postings_list:
                document = query_doc(posting)
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
            return render_template("errorResults.html", PAGE_NUM=PAGE_NUM, TOTAL_PAGES=PAGE_NUM)  # render error page

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
    parser = argparse.ArgumentParser(description="Boolean IR system")
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()

    if args.build:
        build_inverted_index(load_wapo(wapo_path))
    if args.run:
        app.run(debug=True, port=5000)
