#!/usr/bin/env python3

# test_hw3.py
# Version 1.0
# 2/23/2022

import unittest

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
        self.assertDictEqual(invidx.appearances_dict, {'bodi': [1], 'titl': [1], 'sampl': [1]}, message)

    def test_load_postings_list(self):
        """The postings list generated by the Inverted Index DS is correct."""
        invidx = InvertedIndex()
        invidx.index_document(self.sample_document)
        invidx.load_index_postings_list()
        message = 'Inverted Index DS does not load appearances dict correctly'
        self.assertCountEqual(invidx.index, [{'token': 'titl', 'doc_ids': [1]},
                                             {'token': 'sampl', 'doc_ids': [1]},
                                             {'token': 'bodi', 'doc_ids': [1]}], message)

    def test_intersection(self):
        """Find the intersection of two lists"""
        posting_lists = [[1, 2, 3, 4], [2, 3, 4], [3, 4, 5, 6, 7]]
        resulting_interstions = intersection(posting_lists)
        message = 'The intersection of multiple lists of ints is incorrect'
        self.assertListEqual(resulting_interstions, [3, 4], message)


class TestTextProcessing(unittest.TestCase):
    """Tests for the text processing done in text_processing.py."""
    def test_normalize_token(self):
        """A token is normalized correctly."""
        tp = TextProcessing()
        sample_token = 'sample'
        normalized_sample_token = tp.normalize(sample_token)
        message = 'The token: \'sample\' was not normalzied correctly'
        self.assertEqual(normalized_sample_token, 'sampl', message)

    def test_normalize_strings(self):
        """Multiple strings simulating a title and content are normalized correctly"""
        tp = TextProcessing()
        normalized_strings = tp.get_normalized_tokens('sample title', 'sample body')
        message = 'Multiple strings were not notmalized correctly'
        self.assertSetEqual(normalized_strings, {'bodi', 'titl', 'sampl'}, message)


class TestCustomTextProcessing(unittest.TestCase):
    """Tests for the text processing done in customized_text_processing.py."""
    def test_normalize_token(self):
        """A token is normalized correctly."""
        tp = CustomizedTextProcessing()
        sample_token = 'sample'
        normalized_sample_token = tp.normalize(sample_token)
        message = 'The token: \'sample\' was not normalzied correctly'
        self.assertEqual(normalized_sample_token, 'sample', message)

    def test_normalize_strings(self):
        """Multiple strings simulating a title and content are normalized correctly"""
        tp = CustomizedTextProcessing()
        normalized_strings = tp.get_normalized_tokens('sample title', 'sample body')
        message = 'Multiple strings were not notmalized correctly'
        self.assertSetEqual(normalized_strings, {'body', 'title', 'sample'}, message)


if __name__ == '__main__':
    unittest.main()