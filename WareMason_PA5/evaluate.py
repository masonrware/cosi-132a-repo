import argparse


# TODO:
# wapo doc index has been built...
# TODO: build out the argument tree for evaluation
# run through each (4/5) retrieval options
# ... get results ...
# ...

class Evaluate:
    ''' A class to represent an individual evaluation run. '''
    def __init__(self, index: str, topic: int, query_type: str, search_type: str,               # vec_name: str
                 eng_ana: bool, top_k: int = 20) -> None:
        self.index = index
        self.topic = topic
        self.query_type = query_type
        self.search_type = search_type
        self.eng_ana = eng_ana
        self.top_k = top_k
        
    def print_content(self) -> None:
        print(f'{self.index}\n{self.topic}\n{self.query_type}\n{self.search_type}\n{self.eng_ana}\n{self.top_k}')


def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--index_name", metavar='{wapo_docs_50k}', required=True,
                        type=str, help="name of the ES index")
    parser.add_argument("--topic_id", required=True, type=int, help="topic id number")
    parser.add_argument("--query_type", metavar='{kw,nl}', required=True, type=str,
                        help="use keyword or natural language query")
    parser.add_argument("--search_type", metavar='{vector,rerank}', required=True,
                        type=str, help="reranking or ranking with vector only")
    parser.add_argument("--use_english_analyzer", required=False,
                        action='store_true', help="use english analyzer for BM25 search")
    # parser.add_argument("--vector_name", metavar='{ft_vector,sbert_vector}',
    #                     required=True, type=str, help="use fasttext or sbert embedding")
    parser.add_argument("--top_k", required=False, type=int,
                        help="evaluate on top K ranked documents")   
    args = parser.parse_args()
    
    if args.use_english_analyzer:
        eval = Evaluate(index=args.index_name, topic=args.topic_id,                                 # vec_name=args.vector_name
                    query_type=args.query_type, search_type=args.search_type,
                    eng_ana=True, top_k=args.top_k)
    else:
        eval = Evaluate(index=args.index_name, topic=args.topic_id,                                 # vec_name=args.vector_name
                    query_type=args.query_type, search_type=args.search_type,
                    eng_ana=False, top_k=args.top_k)
    
    eval.print_content()
    
    

if __name__ == "__main__":
    main()
