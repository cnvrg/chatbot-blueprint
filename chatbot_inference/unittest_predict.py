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


    # test with data
    def test_with_data(self):
     self.assertGreater(get_response(self.test_cfg["data"][0])['confidence'], 0.99 )
     self.assertGreater(get_response(self.test_cfg["data"][1])['confidence'], 0.99 )
     self.assertGreater(get_response(self.test_cfg["data"][0])['confidence'], 0.99 )
     self.assertGreater(get_response(self.test_cfg["data"][1])['confidence'], 0.99 )
     self.assertGreater(get_response(self.test_cfg["data"][2])['confidence'], 0.99 )
     self.assertGreater(get_response(self.test_cfg["data"][3])['confidence'], 0.99 )
     self.assertGreater(get_response(self.test_cfg["data"][4])['confidence'], 0.99 )
     self.assertGreater(get_response(self.test_cfg["data"][6])['confidence'], 0.99 )
     self.assertGreater(get_response(self.test_cfg["data"][7])['confidence'], 0.99 )
    
    def test_str_return_type(self):
        self.assertIsInstance(
            get_response(self.test_cfg["data"][0]), dict
        )

    @classmethod
    def tearDownClass(self):
        del self.test_cfg
        

if __name__ == '__main__':
    unittest.main()