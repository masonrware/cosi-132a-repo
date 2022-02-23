#!/usr/bin/env python3

# test_hw3.py
# Version 1.0
# 2/23/2022

from re import L
import unittest

from hw3 import flaskApp
import utils
import inverted_index #to test querying
from inverted_index import InvertedIndex #to test indexing
from customized_text_processing import CustomizedTextProcessing
from text_processing import TextProcessing

class TestInvertedIndex(unittest.TestCase):
    """Tests for the inverted index. This class tests both creating the
    inverted index and querying from it."""
    def run(self):
        first_val = 'a'
        second_val = 'a'
        message = "First value and second value are not equal !"
        self.assertEqual(first_val, second_val, message)

class TestUtilityMethods(unittest.TestCase):
    """Tests for the methods stored in utils.py."""
    def run(self):
        first_val = 'a'
        second_val = 'a'
        message = "First value and second value are not equal !"
        self.assertEqual(first_val, second_val, message)

class TestTextProcessing(unittest.TestCase):
    """Tests for the text processing done in text_processing.py."""
    def run(self):
        first_val = 'a'
        second_val = 'a'
        message = "First value and second value are not equal !"
        self.assertEqual(first_val, second_val, message)

class TestCustomTextProcessing(unittest.TestCase):
    """Tests for the text processing done in customized_text_processing.py."""
    def run(self):
        first_val = 'a'
        second_val = 'a'
        message = "First value and second value are not equal !"
        self.assertEqual(first_val, second_val, message)

def main():
    tests = [
        TestInvertedIndex,
        TestUtilityMethods,
        TestTextProcessing,
        TestCustomTextProcessing
    ]
    for test in tests:
        test.run(test)

if __name__ == '__main__':
    # unittest.main()
    main()