from pathlib import Path
from flask import Flask, render_template, request
import math
import utils as u

utils = u.Utils()
pages = {int: [{}]}
PAGE_NUM, TOTAL_PAGES = 1, 0

app = Flask(__name__)

DATA_DIR = Path(__file__).parent.joinpath("pa2_data")
wapo_path = DATA_DIR.joinpath("wapo_pa2.jl")
wapo_docs = utils.load_wapo(wapo_path)  # load and process WAPO documents


@app.route("/")
def home():
    """
    home page
    :return:
    """
    return render_template("home.html")


@app.route("/results", methods=["POST"])
def results():
    """
    result page
    :return:
    """
    query_text = request.form["query"]  # Get the raw user query from home page'
    res = []
    dict_ind = 1
    for document_image in wapo_docs.values():
        if utils.title_match(query_text, document_image['title']):
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
    if len(res) != 0:
        pages[dict_ind] = res

    print(pages.keys())

    TOTAL_PAGES = dict_ind
    return render_template("results.html", query=pages[1], PAGE_NUM=PAGE_NUM, TOTAL_PAGES=TOTAL_PAGES)  # add variables as you wish
    ##TODO:
    # pass a variable for page number and overall page number and then have if statement that checks if they're equal or
    # not and then render the new thing with page number


def limit_content(content: str) -> str:
    return content[:150] if len(content) > 150 else content


@app.route("/results/<int:page_id>/<int:total_pages>", methods=["GET", "POST"])
def next_page(page_id, total_pages):
    """
    "next page" to show more results
    :param page_id:
    :return:
    """
    PAGE_NUM = page_id
    TOTAL_PAGES = total_pages
    print(TOTAL_PAGES)

    return render_template("results.html", query=pages[PAGE_NUM], PAGE_NUM=PAGE_NUM, TOTAL_PAGES=TOTAL_PAGES)  # add variables as you wish


@app.route("/doc_data/<doc_id>")
def doc_data(doc_id):
    """
    document page
    :param doc_id:
    :return:
    """
    doc_dict = utils.look_up_by_id(doc_id)
    ##TODO:
    ##maybe get a bootswatch background
    return render_template("doc.html", here=doc_dict)  # add variables as you wish


if __name__ == "__main__":
    app.run(debug=True, port=5000)
