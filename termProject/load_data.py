from typing import Dict, Union, Generator, Iterable
import functools
import os
import json
from logistic_regression import LogisticRegression
from mongo_db import insert_sents

movie_path = 'data/final_movies.json'

def build_index(docs: Iterable) -> None:
    lr = LogisticRegression(n_features=4)
    lr.train('data/IR_Final_LR/movie_reviews/train', batch_size=3, n_epochs=10, eta=0.1)
    results = lr.test('data/IR_Final_LR/movie_reviews/dev')
    lr.evaluate(results)
    overall_sentiments = {}
    i=0
    for x in docs :
        i+=1
        sentiments = {'sentiment': [], 'title': x['title']}
        for review in x['reviews'] :
            if review is not None:
                if review['review'] is not None:
                    sentiments['sentiment'].append(lr.classify(review['review']))


        #docs['overall_classification'] = sum(sentiments)/len(sentiments)
        overall_sentiments[x['title']] = sentiments

    insert_sents(overall_sentiments)
    
    
if __name__ == "__main__":
    pass
