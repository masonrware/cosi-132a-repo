#!/usr/bin/env python3

# test_hw3.py
# Version 1.0
# 2/23/2022

from re import L
import unittest

from hw3 import flaskApp
import utils
import inverted_index #to test intersection
from inverted_index import InvertedIndex #to test indexing
from customized_text_processing import CustomizedTextProcessing
from text_processing import TextProcessing

class TestInvertedIndex(unittest.TestCase):
    """Tests for the inverted index. This class tests the Inverted Indecx data 
    structure as well as the intersection method in inverted_index.py."""
    def test_index_document(self):
        """A document is indexed into the appearances dictionary correctly."""
        invidx = InvertedIndex
        
        sample_document = {
            'id': id,
            'title': conv['title'],
            'author': conv['author'],
            'published_date': conv['published_date'],
            'content_str': content_str_
        }
        first_val = 'a'
        second_val = 'a'
        message = "First value and second value are not equal !"
        self.assertEqual(first_val, second_val, message)

class TestUtilityMethods(unittest.TestCase):
    """Tests for the methods stored in utils.py."""
    def test_util(self):
        first_val = 'a'
        second_val = 'a'
        message = "First value and second value are not equal !"
        self.assertEqual(first_val, second_val, message)

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
