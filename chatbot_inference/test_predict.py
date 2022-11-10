import unittest
from predict import get_response
import os
import sys
import pandas
import yaml
from yaml.loader import SafeLoader


class TestPredict(unittest.TestCase):

    def test_with_data(self):
        data = {"input_text": "Hello world"}
        self.assertTrue(get_response(data))

    def test_without_data(self):
        data = {"input_text": ""}
        self.assertTrue(get_response(data))

    def test_with_list(self):
        data = {"input_text": []}
        with self.assertRaises(TypeError):
                get_response(data)

    def test_with_large_data_with_special_chars(self):
        data = {"input_text": "we cannot find the *requested (files in $the cached path. ?Please try again or make sure your Internet connection"}
        self.assertTrue(get_response(data))

    def test_with_numeric(self):
        data = {"input_text": 5}
        with self.assertRaises(TypeError):
                get_response(data)



if __name__ == '__main__':
    unittest.main()