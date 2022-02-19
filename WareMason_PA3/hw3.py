from pathlib import Path
import argparse
from flask import Flask, render_template, request
from utils import load_wapo
from inverted_index import build_inverted_index, query_inverted_index
from mongo_db import db, insert_docs, query_doc

app = Flask(__name__)

data_dir = Path(__file__).parent.joinpath("pa3_data")
wapo_path = data_dir.joinpath("wapo_pa3.jl")

if not "wapo_docs" in db.list_collection_names():
    # if wapo_docs collection is not existed, create a new one and insert docs into it
    insert_docs(load_wapo(wapo_path))
    

# home page
@app.route("/")
def home():
    return render_template("home.html")


# result page
@app.route("/results", methods=["POST"])
def results():
    # TODO:
    raise NotImplementedError


# "next page" to show more results
@app.route("/results/<int:page_id>", methods=["POST"])
def next_page(page_id):
    # TODO:
    raise NotImplementedError


# document page
@app.route("/doc_data/<int:doc_id>")
def doc_data(doc_id):
    # TODO:
    raise NotImplementedError


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Boolean IR system")
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()

    if args.build:
        build_inverted_index(load_wapo(wapo_path))
    if args.run:
        app.run(debug=True, port=5000)
