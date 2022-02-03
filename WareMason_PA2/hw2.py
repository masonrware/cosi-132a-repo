from pathlib import Path
from flask import Flask, render_template, request

from utils import title_match, load_wapo

app = Flask(__name__)

DATA_DIR = Path(__file__).parent.joinpath("pa2_data")
wapo_path = DATA_DIR.joinpath("wapo_pa2.jl")
wapo_docs = load_wapo(wapo_path)  # load and process WAPO documents


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
    for document_image in wapo_docs.values():
        if title_match(query_text, document_image['title']):
            if len(res) >= 2:
                res.append('-------')
            res.append(document_image['title'])
            res.append(limit_content(document_image['content_str']))
    return render_template("results.html", query=res)  # add variables as you wish


def limit_content(content: str) -> str:
    return content[:150] if len(content) > 150 else content


@app.route("/results/<int:page_id>", methods=["POST"])
def next_page(page_id):
    """
    "next page" to show more results
    :param page_id:
    :return:
    """
    return render_template("results.html")  # add variables as you wish


@app.route("/doc_data/<doc_id>")
def doc_data(doc_id):
    """
    document page
    :param doc_id:
    :return:
    """
    return render_template("doc.html")  # add variables as you wish


if __name__ == "__main__":
    app.run(debug=True, port=5000)
