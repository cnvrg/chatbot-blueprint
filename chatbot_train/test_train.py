import unittest
import numpy as np
from train import train_run
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
        

    # def test_default_parms(self):
    #     self.assertEqual(train.train_run(), None)
    # test with default parameters  
    def test_default_parms(self):
            self.assertTrue(train_run())

    def test_with_parms(self):
        #setup data
        data = self.test_cfg["data1"]
        epochs = self.test_cfg["epochs1"]
        #test with data and epochs values
        self.assertTrue(train_run(data,epochs))
    
    def test_negative_epoch(self):
        #setup data
        data = self.test_cfg["data2"]
        epochs = self.test_cfg["epochs2"]
        self.assertFalse(train_run(data,epochs))

    def test_large_epoch(self):
        #setup 
        data = self.test_cfg["data3"]
        epochs = self.test_cfg["epochs3"]
        # test with large epochs value
        self.assertFalse(train_run(data,epochs))

    def test_binary(self):
        data = self.test_cfg["data4"]
        epochs = self.test_cfg["epochs1"]
        # test with binary files
        self.assertFalse(train_run(data,epochs))
        
    def test_empty_file(self):
        #setup 
        data = self.test_cfg["data5"]
        epochs = self.test_cfg["epochs1"]
        # test with empty data
        self.assertFalse(train_run(data,epochs))
        
    # def test_large_data(self):
    #     #setup data 
    #     data = self.test_cfg["data6"]
    #     epochs = self.test_cfg["epochs1"]
    #     # test with large dataset
    #     self.assertFalse(train_run(data,epochs))

    def test_null(self):
        # test with null data
        self.assertFalse(train_run("", 3))
    
    # def tearDown(self):
    #     del self.test_cfg
        


if __name__ == '__main__':
    unittest.main()
