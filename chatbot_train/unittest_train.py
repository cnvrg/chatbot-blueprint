import unittest
import numpy as np
from train import train_run
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
        
 
    def test_default_parms(self):
            #self.assertTrue(train_run())
            train = train_run()[1]
            self.assertNotAlmostEqual(train,0.0)
            
        

    def test_with_parms(self):
        #setup data
        data = self.test_cfg["data1"]
        epochs = self.test_cfg["epochs1"]
        #test with data and epochs values
        train = train_run(data,epochs)[1]
        self.assertNotAlmostEqual(train,0.0)
    
    def test_negative_epoch(self):
        #setup data
        data = self.test_cfg["data1"]
        epochs = self.test_cfg["epochs2"]
        train = train_run(data,epochs)[1]
        self.assertEqual(train,0.0)

    def test_binary(self):
        data = self.test_cfg["data5"]
        epochs = self.test_cfg["epochs1"]
        # test with binary files
        train = train_run(data,epochs)[1]
        self.assertEqual(train,0.0)
        
    def test_empty_file(self):
        #setup 
        data = self.test_cfg["data6"]
        epochs = self.test_cfg["epochs1"]
        # test with empty data
        train = train_run(data,epochs)[1]
        self.assertEqual(train,0.0)
        
    def test_null(self):
        # test with null data
        data = self.test_cfg["data7"]
        epochs = self.test_cfg["epochs1"]
        train = train_run(data,epochs)[1]
        self.assertEqual(train,0.0)
    
    
if __name__ == '__main__':
    unittest.main()
