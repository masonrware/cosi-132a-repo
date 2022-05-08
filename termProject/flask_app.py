#!usr/bin/python3

# flask_app.py
# Version 2.0.0  (?)
# 4/20/22

# Written By: Sarah Kosowsky


## This module implements a Flask Application that supports user queries about movies. Using elastic search
## and Mongo DB, this application returns relevant movie reviews back to the user.


from pathlib import Path
from query import Engine
from elasticsearch_dsl.connections import connections
import argparse
from flask import Flask, render_template, request

app = Flask(__name__)

connections.create_connection(hosts=["localhost"], timeout=100, alias="default")  # create connection

doc_results = []  # list that will contain all relevant docs for a certain query


@app.route("/")
def home():
    """
    This is the home page for the website, which has the functionality for searching Washington Post articles.
    @return: renders the html template for the home page, which creates the search box and submit button.
    """
    return render_template("home.html")


# result page
@app.route("/results", methods=["POST"])  # put back after testing
def results():
    global doc_results
    query = request.form["query"]
    print(query)
    #doc_results = []  # query index based on query, save result ids in doc_results for next page queries

    engine = Engine("wapo_docs_50k", query, 60)
    response = engine.search()
    print(response)
    temp_data = ["What is a movie?", """The moving images of a film are created by photographing actual scenes with a motion-picture camera, by photographing drawings or miniature models using traditional animation techniques, by means of CGI and computer animation, or by a combination of some or all of these techniques, and other visual effects.
                Before the introduction of digital production, series of still images were recorded on a strip of chemically sensitized celluloid (photographic film stock), usually at the rate of 24 frames per second. The images are transmitted through a movie projector at the same rate as they were recorded, with a Geneva drive ensuring that each frame remains still during its short projection time. A rotating shutter causes stroboscopic intervals of darkness, but the viewer does not notice the interruptions due to flicker fusion. The apparent motion on the screen is the result of the fact that the visual sense cannot discern the individual images at high speeds, so the impressions of the images blend with the dark intervals and are thus linked together to produce the illusion of one moving image. An analogous optical soundtrack (a graphic recording of the spoken words, music and other sounds) runs along a portion of the film exclusively reserved for it, and was not projected.
                Contemporary"""[:250] + "..."]
    for i in range(10):
        temp = [i]
        temp.extend(temp_data)
        doc_results.append(temp)
    #print(doc_results)

    return render_template("results.html", page=2, num_res=100, doc_results=doc_results)


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
    content = """The moving images of a film are created by photographing actual scenes with a motion-picture camera, by photographing drawings or miniature models using traditional animation techniques, by means of CGI and computer animation, or by a combination of some or all of these techniques, and other visual effects.
                Before the introduction of digital production, series of still images were recorded on a strip of chemically sensitized celluloid (photographic film stock), usually at the rate of 24 frames per second. The images are transmitted through a movie projector at the same rate as they were recorded, with a Geneva drive ensuring that each frame remains still during its short projection time. A rotating shutter causes stroboscopic intervals of darkness, but the viewer does not notice the interruptions due to flicker fusion. The apparent motion on the screen is the result of the fact that the visual sense cannot discern the individual images at high speeds, so the impressions of the images blend with the dark intervals and are thus linked together to produce the illusion of one moving image. An analogous optical soundtrack (a graphic recording of the spoken words, music and other sounds) runs along a portion of the film exclusively reserved for it, and was not projected.
                Contemporary films are usually fully digital through the entire process of production, distribution, and exhibition."""
    author = "Wiki Pedia"
    date = "05/05/2022"
    title = "What is a movie?"  # title of movie or of review
    page_id = 2
    # actors? directors?
    return render_template("review.html", content=content, date=date, author=author, title=title, page_id=page_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MovieRealView system")

    # parser.add_argument("--build", action="store_true")  # are we building index here?
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()

    # if args.build:
        # build inverted index here
    if args.run:
        app.run(debug=True, port=5000)
