from pathlib import Path
import argparse
from flask import Flask, render_template, request
from utils import load_wapo
from inverted_index import build_inverted_index, query_inverted_index
from mongo_db import db, insert_docs, query_doc

app = Flask(__name__)

pages = {}
PAGE_NUM, TOTAL_PAGES = 1, 0

data_dir = Path(__file__).parent.joinpath("pa3_data")
wapo_path = data_dir.joinpath("wapo_pa3.jl")

if not "wapo_docs" in db.list_collection_names():
    insert_docs(load_wapo(wapo_path))


# home page
@app.route("/")
def home():
    """
    home page
    :return:
    """
    return render_template("home.html")


# result page
@app.route("/results", methods=["POST"])
def results():
    """
    result page
    :return:
    """
    query_text = request.form["query"]  # Get the raw user query from home page
    res = [0]
    dict_ind = 1
    for document_image in wapo_docs.values():
        if u.title_match(query_text, document_image['title']):
            if len(res)>0 and res[0]==0:
                res = []
            item_dict = {
                'title': document_image['title'],
                'content': limit_content(document_image['content_str']),
                'id': document_image['id']
            }
            res.append(item_dict)
            if len(res) == 8:
                pages[dict_ind] = res
                res = []
                dict_ind += 1
    TOTAL_PAGES = dict_ind
    if len(res) != 0:
        pages[dict_ind] = res
    print(query_text, len(pages))
    if res[0] == 0:
        return render_template("errorResults.html", PAGE_NUM=PAGE_NUM, TOTAL_PAGES=TOTAL_PAGES)  # add variables as you wish
    else:
        return render_template("results.html", query=pages[1], PAGE_NUM=PAGE_NUM, TOTAL_PAGES=TOTAL_PAGES)  # add variables as you wish

@app.route("/results/<int:page_id>/<int:total_pages>", methods=["GET", "POST"])
def prev_page(page_id: int, total_pages: int) -> str:
    """
    "previous page" to show more results
    :param page_id:
    :param total_pages:
    :return:
    """
    PAGE_NUM = page_id
    TOTAL_PAGES = total_pages
    return render_template("results.html", query=pages[PAGE_NUM], PAGE_NUM=PAGE_NUM,
                           TOTAL_PAGES=TOTAL_PAGES)  # add variables as you wish


# "next page" to show more results
@app.route("/results/<int:page_id>", methods=["POST"])
def next_page(page_id):
    """
    "next page" to show more results
    :param page_id:
    :param total_pages:
    :return:
    """
    PAGE_NUM = page_id
    TOTAL_PAGES = total_pages
    pages = pages
    return render_template("results.html", query=pages[PAGE_NUM], PAGE_NUM=PAGE_NUM,
                           TOTAL_PAGES=TOTAL_PAGES)  # add variables as you wish



# document page
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
