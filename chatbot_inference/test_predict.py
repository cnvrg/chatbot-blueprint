import unittest
from predict import get_response
import os
import sys
import pandas
import yaml
from yaml.loader import SafeLoader


class TestPredict(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        cfg_path = os.path.dirname(os.path.abspath(__file__))
        cfg_file = cfg_path + "/" + "test_config.yaml"
        self.test_cfg = {}
        with open(cfg_file) as c_info_file:
             self.test_cfg = yaml.load(c_info_file, Loader=SafeLoader)
        self.test_cfg = self.test_cfg["test_arguments"]
        self.data = self.test_cfg["data"][0]
        self.empty_data = self.test_cfg["empty_data"][0]
        self.list_data = self.test_cfg["list_data"][0]
        self.large_data = self.test_cfg["large_data"][0]
        self.num_data = self.test_cfg["num_data"][0]

    # test with data
    def test_with_data(self):
        data = self.data
        print("----testing with data :", data)
        self.assertTrue(get_response(data))

    def test_without_data(self):
        data = self.empty_data
        # test without data 
        print("----testing without data :", data)
        self.assertTrue(get_response(data))

    def test_with_list(self):
        data = self.list_data
        # test with list data
        print("----testing with list data :", data)
        with self.assertRaises(TypeError):
                get_response(data)

    def test_with_large_data_with_special_chars(self):
        data = self.large_data
        # test with large data
        print("----testing with large data :", data)
        self.assertTrue(get_response(data))

    def test_with_numeric(self):
        data = self.num_data
        # test with numeric 
        print("----testing with numeric data :", data)
        with self.assertRaises(TypeError):
                get_response(data)


if __name__ == '__main__':
    unittest.main()