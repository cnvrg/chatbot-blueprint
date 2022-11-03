import unittest
import global_
#global_.data = "data2.csv"
import train
#import global_
#import unittest
import os
import sys
import pandas
import yaml
from yaml.loader import SafeLoader


class TrainTest(unittest.TestCase):
    def setUp(self):
        #global_.data = "data2.csv"
        cfg_path = os.path.dirname(os.path.abspath(__file__))
        
        cfg_file = cfg_path + "/" + "test_config.yaml"
        #print(cfg_file)
        self.test_cfg = {}
        with open(cfg_file) as c_info_file:
             self.test_cfg = yaml.load(c_info_file, Loader=SafeLoader)
        self.test_cfg = self.test_cfg["test_arguments"]
        #print("#####",self.test_cfg)
        #print()
        #self.data = 'data.csv'

    def test(self):
        global_.data = self.test_cfg["data2"]
        global_.epochs = self.test_cfg["epochs1"]
        self.assertTrue(train)
    
    # def test2(self):
    #     global_.data = self.test_cfg["data3"]
    #     global_.epochs = self.test_cfg["epochs2"]
    #     print("@@",global_.data)
    #     self.assertTrue(train)
    # def test3(self):
    #     global_.data = self.test_cfg["data4"]
    #     print("@",global_.data)
    #     self.assertFalse(train)

if __name__ == '__main__':
    unittest.main()