import boto3
import unittest
import s3connector
import os
import logging
import yaml
from yaml.loader import SafeLoader


class Tests3Bucket(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        cfg_path = os.path.dirname(os.path.abspath(__file__))
        cfg_file = cfg_path + "/" + "test_config.yaml"
        self.test_cfg = {}
        with open(cfg_file) as c_info_file:
             self.test_cfg = yaml.load(c_info_file, Loader=SafeLoader)
        self.test_cfg = self.test_cfg["test_arguments"]
        self.key = self.test_cfg['key']
        self.secret= self.test_cfg['secret']
        self.s3_endpoint=self.test_cfg['s3_endpoint']
        self.region_name=self.test_cfg['region_name']
        # Intialize connection for S3
        self.s3_connection = s3connector.S3(
            self.test_cfg["key"], 
            self.test_cfg["secret"], 
            self.test_cfg["s3_endpoint"], 
            self.test_cfg["region_name"]
            )

    # Test connection for S3
    def test_connection(self):
        self.assertTrue(self.s3_connection)

    # Test list buckets from s3 
    def test_list_bucket(self):
        conn = self.s3_connection.list_buckets()
        for bucket in conn:
            print(bucket.name)
        self.assertTrue(conn)
        
    # Test list objects from s3 Bucket
    def test_list_object(self):
        conn = self.s3_connection.list_objects(self.test_cfg['bucket_name'])
        for obj in conn: 
            print(obj.key)
        self.assertTrue(conn)

    # Test bucket versioning
    def test_check_bucket_versioning(self):
        conn = self.s3_connection.check_bucket_versioning(self.test_cfg['bucket_name'])
        self.assertEqual(conn,None)
        
    # Test object versioning from s3 bucket
    def test_list_objects_versions(self):
        conn = self.s3_connection.list_objects_versions(self.test_cfg['bucket_name'])
        for obj_version in conn:
            print(obj_version)
        self.assertTrue(conn)
        
    # Test object metadata    
    def test_metadata_object(self):
        conn = self.s3_connection.metadata_object(self.test_cfg['bucket_name'],self.test_cfg['file_name2'])
        for obj_metadata in conn:
            print(obj_metadata)
        self.assertTrue(conn)

    # Test deleting object from s3 buckets
    def test_delete_object(self):
        conn = self.s3_connection.delete_object(self.test_cfg['bucket_name'],self.test_cfg['file_name1'])
        for obj_delete in conn:
            print(obj_delete)
        self.assertTrue(conn)

    @classmethod
    def tearDownClass(self):
        del self.s3_connection
        
        
if __name__ == '__main__':
    unittest.main() 