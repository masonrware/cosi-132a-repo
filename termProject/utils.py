#!usr/bin/python3

# utils.py
# Version 1.0.0
# 4/10/22

# Written By: Mason Ware

import os
import datetime

from pynytimes import NYTAPI        # type: ignore 


nyt = NYTAPI('SMmx72tbIBB8gdZJgVv6gARJxjVd4o2x', parse_dates=True)

reviews = nyt.movie_reviews(
    keyword = "Green Book",
    options = {
        "order": "by-opening-date",
        "reviewer": "A.O. Scott",
        "critics_pick": False
    })

print(reviews)