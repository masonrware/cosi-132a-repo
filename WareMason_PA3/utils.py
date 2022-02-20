import json
from typing import Dict, Union, Generator
import functools
import os
import time
import re
from datetime import datetime


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_t = time.perf_counter()
        f_value = func(*args, **kwargs)
        elapsed_t = time.perf_counter() - start_t
        mins = elapsed_t // 60
        print(
            f"'{func.__name__}' elapsed time: {mins} minutes, {elapsed_t - mins * 60:0.2f} seconds"
        )
        return f_value
    return wrapper_timer


def load_wapo(wapo_jl_path: Union[str, os.PathLike]) -> Generator[Dict, None, None]:
    """
    Unlike HW2, load_wapo should be an iterator in this assignment. It's more memory-efficient when you need to
    load each document and build the inverted index.
    At each time, load_wapo will yield a dictionary of the following format:

    {
        "id": 1,
        "title": "Many Iowans still don't know who they will caucus for",
        "author": "Jason Horowitz",
        "published_date": 2011-12-31 20:37:52,
        "content_str": "Iran announced a nuclear fuel breakthrough and test-fired ..."
      }
    Compared to HW2, you should also make the following changes:
    - replace the original value of the key "id" with an integer that corresponds to the order of each document
      that has been loaded. For example. the id of the first yielded document is 0 and the second is 1 and so on.
    - remove any HTML elements from the content_str.
    - convert the value of "published_date" to a readable format.
      This one is given as follows, so just sure you apply it in your implementation
            %: from datetime import datetime
            %: doc["published_date"] = datetime.fromtimestamp(doc["published_date"] / 1000.0)

    :param wapo_jl_path:
    :return:
    """
    with open(wapo_jl_path, 'r', encoding='UTF-8') as file:
        id = 0
        for line in file:
            conv = json.loads(line)
            contents = conv['contents']
            if(contents):
                content_str_ = " ".join([item['content'] for item in contents if item['type'] == 'sanitized_html'])
                content_str_ = re.sub("<[^>]*>", "", content_str_)
                #!! This one is given as follows, so just sure you apply it in your implementation
                #!! %: doc["published_date"] = datetime.fromtimestamp(doc["published_date"] / 1000.0)
            
                res = {
                    'id': id,
                    'title': conv['title'],
                    'author': conv['author'],
                    'published_date': conv['published_date'],
                    'content_str': content_str_
                }
            
                id+=1
                yield res


if __name__ == "__main__":
    pass
