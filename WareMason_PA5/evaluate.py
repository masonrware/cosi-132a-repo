import argparse


# TODO:
# wapo doc index has been built...
# TODO: build out the argument tree for evaluation
# run through each (4/5) retrieval options
# ... get results ...
# ...



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
       "--index_name",
        metavar='{wapo_docs_50k}',
        required=True,
        type=str,
        help="name of the ES index"
    )
    parser.add_argument(
       "--topic_id",
        required=True,
        type=str,
        help="topic id number"
    )
    parser.add_argument(
       "--query_type",
        metavar='{kw,nl}',
        required=True,
        type=str,
        help="use keyword or natural language query"
    )
    parser.add_argument(
       "--search_type",
        metavar='{vector,rerank}',
        required=True,
        type=str,
        help="reranking or ranking with vector only"
    )
    parser.add_argument(
       "--use_english_analyzer",
        metavar='',
        required=True,
        type=str,
        help="use english analyzer for BM25 search"
    )
    # parser.add_argument(
    #    "--vector_name",   #? issue with vector in name?
    #     metavar='{ft_vector,sbert_vector}',
    #     required=True,
    #     type=str,
    #     help="use fasttext or sbert embedding"
    # )
    parser.add_argument(
       "--top_k",
        required=True,
        type=str,
        help="evaluate on top K ranked documents"
    )
    

    args = parser.parse_args()
    #TODO:
    #stuff
    


if __name__ == "__main__":
    main()
