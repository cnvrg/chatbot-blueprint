import boto3
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

    # test connection for s3 resource
    def test_connection(self):
        self.assertTrue(self.s3_connection)
        
    #  test connection with incorrect keys
    def test_conn_with_incorrectkey(self):
        try:
          fun = s3connector.S3( 
            self.test_cfg["incorrect_key"],
            self.test_cfg["incorrect_secret"],
            self.test_cfg["s3_endpoint"],
            self.test_cfg["region_name"]
            ).list_buckets()
          for bucket in fun:
            print(bucket)
        except ClientError as e:
            print("Could not connect to s3 resource, check your parameters:",e.response["Error"]["Code"])
            error = e.response["Error"]["Code"]
        self.assertEqual(error,"InvalidAccessKeyId")

    # test list buckets from s3 resource
    def test_list_bucket(self):
        conn = self.s3_connection.list_buckets()
        for buk in conn:
            self.assertGreater(len(buk.name), 0)
           
  
    # test non_existing list buckets
    def test_list_nonexisting_bucket(self):
        try:
          conn = self.s3_connection.list_objects(self.test_cfg['bucket_name2'])
          for b in conn:
            print(b)
        except ClientError as e:
            error = e.response["Error"]["Code"] 
            print("bucket not found, please check the bucket name")
            self.assertEquals(error,"AccessDenied")  
   
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

    #test metadata non exist object  
    def test_metadata_non_exist_object(self):
        try:
          conn = self.s3_connection.metadata_object(self.test_cfg['bucket_name1'],self.test_cfg['obj_name1'])
        except ClientError as e:
            error = e.response["Error"]["Message"] 
            print("Object",error)
            self.assertEqual(error,"Not Found")    

    #test metadata object
    def test_metadata_object(self):
        conn = self.s3_connection.metadata_object(self.test_cfg['bucket_name1'],self.test_cfg['obj_name2'])
        self.assertEqual(conn['ResponseMetadata']['HTTPStatusCode'],200)

    #delete object for s3
    def test_delete_object(self):
        conn = self.s3_connection.delete_object(self.test_cfg['bucket_name1'],self.test_cfg['obj_name3'])
        self.assertEqual(conn['ResponseMetadata']['HTTPStatusCode'],200)
    
    @classmethod
    def tearDownClass(self):
        del self.s3_connection
        
if __name__ == '__main__':
    unittest.main()