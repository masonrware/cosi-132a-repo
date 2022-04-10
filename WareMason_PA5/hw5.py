#!/usr/bin/python3.9

# hw5.py
# Version 1.0.0
# 4/3/2022

import argparse
from pydoc import doc
import unittest
import os

from user_search import Engine
from embedding_service.text_processing import TextProcessing

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
        return render_template("home.html")

    # results page
    @app.route("/results", methods=["POST"])
    def results():
        # persisting data
        global postings_list
        global stop_words
        global unknown_words
        global query_text
        
        query_text = request.form["query"]  # Get the raw user query from home page
        if request.method == 'POST':
            retr_methods = request.form.getlist('retr_methods')
        
        #TODO
        #still need to undo the search_type param default - i.e. add the checkbox for vector
        
        #defaults:
        seng = Engine(index='wapo_docs_50k', raw_query=query_text,
                      vector_name='sbert_vector', search_type=retr_methods,
                      eng_ana=False, top_k=20)
        res = seng.search()
        
        dict_ind = 1
        for document in res:
            document = document.to_dict()
            document['content'] = limit_content(document['content'])     
        if len(res) == 8:  # limit page length to 8 results
            pages[dict_ind] = res
            res = []
            dict_ind += 1
        else:
            while len(res) > 8:
                pages[dict_ind] = res[:8]
                res = res[8:]
                dict_ind += 1
            pages[dict_ind] = res
        TOTAL_PAGES = dict_ind
        if len(res) != 0:
            return render_template("results.html", response=pages[1], query=query_text, 
                                    PAGE_NUM=PAGE_NUM, TOTAL_PAGES=TOTAL_PAGES)  # render results on results page
        else:
            return render_template("errorResults.html", query=query_text,
                                    PAGE_NUM=1, TOTAL_PAGES=1)  # render error page

    # previous page
    @app.route("/results/<int:page_id>/prev", methods=["GET", "POST"])
    def prev_page(page_id: int) -> str:
        """previous page to show more results"""
        PAGE_NUM = page_id
        return render_template("results.html", response=pages[PAGE_NUM], query=query_text,
                               PAGE_NUM=PAGE_NUM, TOTAL_PAGES=len(pages))  # render results page with persisting data

    # next page
    @app.route("/results/<int:page_id>/next", methods=["GET", "POST"])
    def next_page(page_id: int) -> str:
        """next page to show more results"""
        PAGE_NUM = page_id
        return render_template("results.html", response=pages[PAGE_NUM], query=query_text,
                               PAGE_NUM=PAGE_NUM, TOTAL_PAGES=len(pages))  # render results page with persisting data

    # get a single doc based on it's id
    @app.route("/doc_data/<int:doc_id>")
    def doc_data(doc_id):
        """individual document page"""
        result_doc = search_client.search(index="wapo_docs_50k", body={"query": {"terms": { "_id": [ doc_id ]}}})
        result_doc = (result_doc['hits']['hits'][0]['_source'])
        return render_template("doc.html", document=result_doc)  # render a document page


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VS IR system")
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    if args.build:
        if not search_client.indices.exists(index="wapo_docs_50k"):
            os.system('python3.9 load_es_index.py --index_name wapo_docs_50k --wapo_path pa5_data/subset_wapo_50k_sbert_ft_filtered.jl')    # pa5 data is saved locally due to size issues so this will not work
    if args.test:
        # write test suite and switch below
        
        print(f'-'*60,f'\nRunning Test Suite...\n\n', f'-'*60)
        suite = unittest.TestLoader().loadTestsFromModule(test_hw4)
        unittest.TextTestRunner(verbosity=3).run(suite)
        
        app.run(port=5001)
    if args.run:
        app.run(debug=True, port=5000)
