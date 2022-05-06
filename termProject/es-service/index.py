#!/usr/local/lib/python3.9

from typing import Iterator, Dict, Union, Sequence, Generator

from elasticsearch_dsl import Index
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk

from embedding_service.client import EmbeddingClient
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import analyzer, tokenizer, token_filter, char_filter


from doc_template import BaseDoc


class ESIndex(object):
    def __init__(
        self,
        index_name: str,
        docs: Union[Iterator[Dict], Sequence[Dict]],
    ):
        """
        ES index structure
        :param index_name: the name of your index
        :param docs: wapo docs to be loaded
        """
        # set an elasticsearch connection to your localhost
        connections.create_connection(hosts=["localhost"], timeout=100, alias="default")
        self.index = index_name
        es_index = Index(self.index)  # initialize the index

        # delete existing index that has the same name
        if es_index.exists():
            es_index.delete()

        es_index.document(BaseDoc)  # link document mapping to the index
        es_index.create()  # create the index
        if docs is not None:
            self.load(docs)


    # TODO
    # below needs to be rewritten in conjunction with doc_template.py
    
    @staticmethod
    def _populate_doc(
        docs: Union[Iterator[Dict], Sequence[Dict]]
    ) -> Generator[BaseDoc, None, None]:
        """
        populate the BaseDoc
        :param docs: wapo docs
        :return:
        """
        connections.create_connection(hosts=["localhost"], timeout=100, alias="default")

        # embedders
        sbert_encoder = EmbeddingClient(
            host="localhost", embedding_type="sbert"
        )  # connect to the sbert embedding server
        fasttext_encoder = EmbeddingClient(
            host="localhost", embedding_type="fasttext"
        )  # connect to the fasttext embedding server
        
        # stemmers
        my_analyzer1 = analyzer(
            "my_analyzer1",
            tokenizer=tokenizer("trigram", "ngram", min_gram=3, max_gram=3),
            filter=["lowercase"],
        )
        
        
        response = my_analyzer1.simulate(
            "The big fox jumps over the lazy dog!"
        )  # simulate the analyzer effect on text
        tokens = [t.token for t in response.tokens]

        
        for i, doc in enumerate(docs):
            es_doc = BaseDoc(_id=i)
            es_doc.doc_id = i
            es_doc.title = doc["title"]
            es_doc.review = str(combine_review(doc["reviews"]))
            es_doc.stemmed_review = str([t.token for t in my_analyzer1.simulate(combine_review(doc["reviews"]))])
            es_doc.ft_vector = fasttext_encoder.encode(combine_review(doc["reviews"]))
            es_doc.sbert_vector = sbert_encoder.encode(combine_review(doc["reviews"]))
            yield es_doc

    def load(self, docs: Union[Iterator[Dict], Sequence[Dict]]):
        # bulk insertion
        bulk(
            connections.get_connection(),
            (
                d.to_dict(
                    include_meta=True, skip_empty=False
                )  # serialize the BaseDoc instance (include meta information and not skip empty documents)
                for d in self._populate_doc(docs)
            ),
        )
    
def combine_review(reviews: list(dict())):
    res = set()
    for review in reviews:
        res.add(review['review'])
    return res
