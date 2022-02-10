from pathlib import Path
from flask import Flask, render_template, request
import math
import utils as u

app = Flask(__name__)


def limit_content(content: str) -> str:
    return content[:150] if len(content) > 150 else content


pages = {int: [{}]}
PAGE_NUM, TOTAL_PAGES = 1, 0

DATA_DIR = Path(__file__).parent.joinpath("pa2_data")
wapo_path = DATA_DIR.joinpath("wapo_pa2.jl")
wapo_docs = u.load_wapo(wapo_path)  # load and process WAPO documents


@app.route("/")
def home() -> str:
    """
    home page
    :return:
    """
    return render_template("home.html")


@app.route("/results", methods=["POST"])
def results() -> str:
    """
    result page
    :return:
    """
    query_text = request.form["query"]  # Get the raw user query from home page
    res = []
    dict_ind = 1
    for document_image in wapo_docs.values():
        if u.title_match(query_text, document_image['title']):
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
    if len(list(pages.keys())) != 1:
        return render_template("results.html", query=pages[1], PAGE_NUM=PAGE_NUM, TOTAL_PAGES=TOTAL_PAGES)  # add variables as you wish
    else:
        return render_template("errorResults.html", PAGE_NUM=PAGE_NUM, TOTAL_PAGES=TOTAL_PAGES)  # add variables as you wish


# CUSTOM ADDED METHOD
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


@app.route("/results/<int:page_id>/<int:total_pages>", methods=["GET", "POST"])
def next_page(page_id: int, total_pages: int) -> str:
    """
    "next page" to show more results
    :param page_id:
    :param total_pages:
    :return:
    """
    PAGE_NUM = page_id
    TOTAL_PAGES = total_pages
    return render_template("results.html", query=pages[PAGE_NUM], PAGE_NUM=PAGE_NUM,
                           TOTAL_PAGES=TOTAL_PAGES)  # add variables as you wish


@app.route("/doc_data/<doc_id>")
def doc_data(doc_id: int) -> str:
    """
    document page
    :param doc_id:
    :return:
    """
    doc_dict = u.look_up_by_id(doc_id)
    # TODO:
    # maybe get a bootswatch background
    return render_template("doc.html", here=doc_dict)  # add variables as you wish


if __name__ == "__main__":
    app.run(debug=True, port=2400)
