import unittest
from  train import *
import os
import sys
import pandas
import yaml
from yaml.loader import SafeLoader


class SimplisticTest(unittest.TestCase):
    def setUp(self):
        
        cfg_path = os.path.dirname(os.path.abspath(__file__))
        cfg_file = cfg_path + "/" + "test_config.yaml"
        print(cfg_file)
        self.test_cfg = {}
        with open(cfg_file) as c_info_file:
             self.test_cfg = yaml.load(c_info_file, Loader=SafeLoader)
        self.test_cfg = self.test_cfg["test_arguments"]
        self.data = self.test_cfg["data2"]
        

    def test(self):
        
        self.assertTrue(train.train_run(self.data))
    


if __name__ == '__main__':
    unittest.main()