import json
import os
from typing import Dict, Union


def title_match(query: str, title: str) -> bool:
    if query in title:
        return True
    else:
        return False


def load_wapo(wapo_jl_path: Union[str, os.PathLike]) -> Dict[str, Dict]:
    """
    output dictionary should be of the following format:
    {
      "2ee2b1ca-33d9-11e1-a274-61fcdeecc5f5": {
        "id": "2ee2b1ca-33d9-11e1-a274-61fcdeecc5f5",
        "title": "Many Iowans still don't know who they will caucus for",
        "author": "Jason Horowitz",
        "published_date": 1325380672000,
        "content_str": "Iran announced a nuclear fuel breakthrough and test-fired ..."
      },
      "another id": {...}
    }

    "content_str" is a new field that you need to generate. The value of "content_str" is the concatenation of
    content values that are typed as "sanitized_html" from "contents" field.

    """
    output_dict = dict()
    with open(wapo_jl_path) as file:
        for line in file:
            conv = json.loads(line)
            contents = conv['contents']
            content_str_ = " ".join([item['content'] for item in contents if item['type'] == 'sanitized_html'])
            value_dict = {
                'id': conv['id'],
                'title': conv['title'],
                'author': conv['author'],
                'published_date': conv['published_date'],
                'content_str': content_str_
            }
            output_dict[conv['id']] = value_dict
    return output_dict
