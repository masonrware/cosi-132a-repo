from pathlib import Path
import argparse
from typing import Tuple

from flask import Flask, render_template, request

from utils import load_wapo
from inverted_index import build_inverted_index, query_inverted_index
from mongo_db import db, insert_docs, query_doc

app = Flask(__name__)

data_dir = Path(__file__).parent.joinpath("pa3_data")
wapo_path = data_dir.joinpath("wapo_pa3.jl")

if not "wapo_docs" in db.list_collection_names():
    insert_docs(load_wapo(wapo_path))


pages = {}
PAGE_NUM, TOTAL_PAGES = 1, 0
stop_words, unknown_words = [], set()


# home page
@app.route("/")
def home():
    """
    home page
    :return:
    """
    return render_template("home.html")

def limit_content(content: str) -> str:
    return content[:150] if len(content) > 150 else content

# result page
@app.route("/results", methods=["POST"])
def results():
    """
    result page
    :return:
    """
    query_text = request.form["query"]  # Get the raw user query from home page
    res = []
    dict_ind = 1

    postings_list, stop_words, unknown_words = query_inverted_index(query_text)

    if len(postings_list) != 0:
        for posting in postings_list:
            document = query_doc(posting)
            item_dict = {
                'title': document['title'],
                'content': limit_content(document['content_str']) + '...',
                'id': document['id']
            }
            res.append(item_dict)
            if len(res) == 8:
                pages[dict_ind] = res
                res = []
                dict_ind += 1
        TOTAL_PAGES = dict_ind
        if len(res) != 0:
            pages[dict_ind] = res
        return render_template("results.html", response=pages[1], stop_words = stop_words, unknown_words = unknown_words, PAGE_NUM=PAGE_NUM, TOTAL_PAGES=TOTAL_PAGES)  # add variables as you wish
    else:
        return render_template("errorResults.html", PAGE_NUM=PAGE_NUM, TOTAL_PAGES=PAGE_NUM)  # add variables as you wish

        

@app.route("/results/<int:page_id>/prev", methods=["GET", "POST"])
def prev_page(page_id: int, passed_values: Tuple) -> str:
    """
    "previous page" to show more results
    :param page_id:
    :param total_pages:
    :return:
    """
    ##!need stop words and unkown words to persist
    PAGE_NUM = page_id
    stop_words = passed_values[0]
    unknown_words = passed_values[1]
    return render_template("results.html", response=pages[PAGE_NUM], stop_words = stop_words, unknown_words = unknown_words,
                            PAGE_NUM=PAGE_NUM, TOTAL_PAGES=len(pages))  # add variables as you wish


@app.route("/results/<int:page_id>/next", methods=["GET", "POST"])
def next_page(page_id: int, passed_values: Tuple) -> str:
    """
    "next page" to show more results
    :param page_id:
    :param total_pages:
    :return:
    """
    ##!need stop words and unkown words to persist
    PAGE_NUM = page_id
    stop_words = passed_values[0]
    unknown_words = passed_values[1]
    return render_template("results.html", response=pages[PAGE_NUM], stop_words = stop_words, unknown_words = unknown_words,
                            PAGE_NUM=PAGE_NUM, TOTAL_PAGES=len(pages))  # add variables as you wish


#! needs fixing
@app.route("/doc_data/<int:doc_id>")
def doc_data(doc_id):
    """
    document page
    :param doc_id:
    :return:
    """
    doc_dict = u.look_up_by_id(doc_id)
    return render_template("doc.html", here=doc_dict) 



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Boolean IR system")
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()

    if args.build:
        build_inverted_index(load_wapo(wapo_path))
    if args.run:
        app.run(debug=True, port=5000)
