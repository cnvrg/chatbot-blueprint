import train 
import unittest
import numpy as np
from bert_model import BERT_Arch
import os
import sys
import pandas
import yaml
from yaml.loader import SafeLoader


class TestTrain(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        cfg_path = os.path.dirname(os.path.abspath(__file__))
        cfg_file = cfg_path + "/" + "test_config.yaml"
        self.test_cfg = {}
        with open(cfg_file) as c_info_file:
             self.test_cfg = yaml.load(c_info_file, Loader=SafeLoader)
        self.test_cfg = self.test_cfg["test_arguments"]

    def test_data(self):
        fun = train.test()
        self.assertLessEqual(fun[0], 2)
        self.assertGreaterEqual(fun[1], 50)
        self.assertGreaterEqual(fun[2], 50)
      

    def test_with_parms(self):
        #setup data
        data = self.test_cfg["data2"]
        epochs = self.test_cfg["epochs1"]
        #test with data and epochs values
        fun = train.test(data,epochs)
        self.assertLessEqual(fun[0], 2)
        self.assertGreaterEqual(fun[1], 50)
        self.assertGreaterEqual(fun[2], 50)

    
    def test_negative_epoch(self):
        #setup data
        data = self.test_cfg["data2"]
        epochs = self.test_cfg["epochs2"]
        fun = train.test(data,epochs)        
        self.assertEqual(fun[1], 0)
        
    def test_binary(self):
        data = self.test_cfg["data5"]
        epochs = self.test_cfg["epochs1"]
        # test with binary files
        fun = train.test(data,epochs) 
        print(fun)       
        self.assertEqual(fun[1], 0)
        
    def test_empty_file(self):
        #setup 
        data = self.test_cfg["data5"]
        epochs = self.test_cfg["epochs1"]
        # test with empty data
        fun = train.test(data,epochs)        
        self.assertEqual(fun[1], 0) 


if __name__ == '__main__':
    unittest.main()