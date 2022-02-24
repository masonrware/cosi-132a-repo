#!/usr/bin/env python3

# test_hw3.py
# Version 1.0
# 2/23/2022

import unittest

from hw3 import flaskApp
from utils import load_wapo
from inverted_index import InvertedIndex, intersection
from customized_text_processing import CustomizedTextProcessing
from text_processing import TextProcessing

class TestInvertedIndex(unittest.TestCase):
    """Tests for the inverted index. This class tests the Inverted Indecx data 
    structure as well as the intersection method in inverted_index.py."""
    def setUp(self) -> None:
        self.sample_document = {
            'id': 1,
            'title': 'sample title',
            'author': 'john doe',
            'published_date': '12-34-56',
            'content_str': 'sample body'
        }
        return super().setUp()

    def test_index_document(self):
        """A document is indexed into the appearances dictionary correctly."""
        invidx = InvertedIndex()
        invidx.index_document(self.sample_document)
        message = 'Inverted Index DS does not load appearances dict correctly'
        self.assertDictEqual(invidx.appearances_dict, {'bodi':[1], 'titl':[1], 'sampl':[1]}, message)

    def test_load_postings_list(self):
        """The postings list generated by the Inverted Index DS is correct."""
        invidx = InvertedIndex()
        invidx.index_document(self.sample_document)
        invidx.load_index_postings_list()
        message = 'Inverted Index DS does not load appearances dict correctly'
        self.assertCountEqual(invidx.index, [{'token':'titl', 'doc_ids':[1]},
                                             {'token':'sampl', 'doc_ids':[1]}, 
                                             {'token':'bodi', 'doc_ids':[1]}], message)

    def test_intersection(self):
        """Find the intersection of two lists"""
        posting_lists = [[1,2,3,4], [2,3,4], [3,4,5,6,7]]
        resulting_interstions = intersection(posting_lists)
        message = 'The intersection of multiple lists of ints is incorrect'
        self.assertListEqual(resulting_interstions, [3, 4], message)


class TestUtilityMethods(unittest.TestCase):
    """Tests for the methods stored in utils.py."""
    def test_util_load_wapo(self):
        values = load_wapo('./pa3_data/wapo_pa3.jl')
        v = next(values)
        self.assertIsNone(v)        

class TestTextProcessing(unittest.TestCase):
    """Tests for the text processing done in text_processing.py."""
    def test_txt(self):
        first_val = 'a'
        second_val = 'a'
        message = "First value and second value are not equal !"
        self.assertEqual(first_val, second_val, message)

class TestCustomTextProcessing(unittest.TestCase):
    """Tests for the text processing done in customized_text_processing.py."""
    def test_text_process(self):
        first_val = 1
        second_val = 1
        message = "First value and second value are not equal !"
        self.assertEqual(first_val, second_val, message)

# def main():
#     tests = [
#         TestInvertedIndex,
#         TestUtilityMethods,
#         TestTextProcessing,
#         TestCustomTextProcessing
#     ]
#     for test in tests:
#         test.run(test)

if __name__ == '__main__':
    unittest.main()
