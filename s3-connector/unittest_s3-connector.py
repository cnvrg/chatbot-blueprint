import boto3
import botocore
import unittest
import s3connector
import os
import logging
import yaml
from yaml.loader import SafeLoader
from botocore.exceptions import ClientError

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
        
        self.s3_connection = s3connector.S3(
            self.test_cfg["key"], 
            self.test_cfg["secret"], 
            self.test_cfg["s3_endpoint"], 
            self.test_cfg["region_name"]
            )
        self.main = s3connector.main()
   
    #  test connection with incorrect keys
    def test_instantiate_connector(self):
        print(f"testing with wrong credentials")

        with self.assertRaises(botocore.exceptions.ClientError):
            conn =  s3connector.S3(
            self.test_cfg["incorrect_key"],
            self.test_cfg["incorrect_secret"],
            self.test_cfg["s3_endpoint"],
            self.test_cfg["region_name"]
            ).list_buckets()
            for bucket in conn:
                print(bucket.name)

    # test list buckets from s3 resource
    def test_list_bucket(self):
        conn = self.s3_connection.list_buckets()
        for buk in conn:
            self.assertGreater(len(buk.name), 0)
           
  
    # test non_existing list buckets
    def test_list_nonexisting_bucket(self):
        with self.assertRaises(botocore.exceptions.ClientError):
          conn = self.s3_connection.list_objects(self.test_cfg['bucket_name2'])
          for obj in conn:
             print(obj.key)
          
    # test list objects from s3 bucket
    def test_list_object(self):
         conn = self.s3_connection.list_objects(self.test_cfg['bucket_name1'])
         for obj in conn:
            self.assertGreater(len(obj.key), 0)
   
    # test object without versioning
    def test_check_bucket_without_versioning(self):
        conn = self.s3_connection.check_bucket_versioning(self.test_cfg['bucket_name1'])
        self.assertEqual(conn,None)
        
    # test object with versioning
    def test_check_bucket_with_versioning(self):
        conn = self.s3_connection.check_bucket_versioning(self.test_cfg['bucket_name3'])
        self.assertEqual(conn,"Enabled")

    # test object without versioning
    def test_list_objects_versions(self):
        conn = self.s3_connection.list_objects_versions(self.test_cfg['bucket_name1'])      
        for ver in conn:
            self.assertEqual(ver.id,"null")

    #test metadata object
    def test_metadata_object(self):
        conn = self.s3_connection.metadata_object(self.test_cfg['bucket_name1'],self.test_cfg['obj_name2'])
        self.assertEqual(conn['ResponseMetadata']['HTTPStatusCode'],200)

    #delete object for s3
    def test_delete_object(self):
        conn = self.s3_connection.delete_object(self.test_cfg['bucket_name1'],self.test_cfg['obj_name3'])
        self.assertEqual(conn['ResponseMetadata']['HTTPStatusCode'],200)
    
    # test download object
    def test_download_object(self):
       conn = self.s3_connection.download_object(self.test_cfg['bucket_name1'],self.test_cfg['obj_name2'],dest_name=self.test_cfg['obj_name4'])
       self.assertEqual(conn,None)
    
    #test upload object   
    def test_upload_file(self):
       conn = self.s3_connection.upload_file(self.test_cfg['bucket_name1'],self.test_cfg['obj_name2'])
       self.assertEqual(conn,None)
    
    
    @classmethod
    def tearDownClass(self):
        del self.s3_connection
        
if __name__ == '__main__':
    unittest.main()