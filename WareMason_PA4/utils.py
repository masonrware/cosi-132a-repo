from typing import Dict, Union, Generator
import functools
import os
import time
import json
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
    It's same with the load_wapo in HW3
    """
    with open(wapo_jl_path, 'r', encoding='UTF-8') as file:
        id_ = 0
        for line in file:
            if(line):
                conv = json.loads(line)
                contents = conv['contents']
                if conv['title']:
                    res = [item['content'] for item in contents if item and item['type'] == 'sanitized_html']
                    print(conv['id'], '        ...        ', id_)
                    content_str_ = " ".join(res)
                    content_str_ = re.sub("<[^>]*>", "", content_str_)
                    res = {
                        'id': id_,
                        'title': conv['title'],
                        'author': conv['author'],
                        'published_date': datetime.fromtimestamp(int(conv['published_date']/1000)),
                        'content_str': content_str_
                    }
                    id_ += 1
                    yield res


if __name__ == "__main__":
    pass
