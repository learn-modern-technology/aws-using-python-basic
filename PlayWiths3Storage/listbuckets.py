from datetime import date, datetime
import os, sys
import json
import boto3
from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig
prev_dir = 'C:\\Users\\Sudhanshu\\gitrepository\\learncloud\\learn-aws-python'
sys.path.append(prev_dir)
import json_operations

## print(os.path.dirname(sys.executable))
## print(sys.executable)
## print(os.path.dirname(os.path.realpath(__file__)))
## print(sys.path)

config_data = json_operations.loadjsondata("./../configs/config.json")
s3_jsondata_path = config_data["s3_data_path"]
region_name = config_data["S3Region"]
s3_data = json_operations.loadjsondata(s3_jsondata_path)

def list_regional_bucket(bucket_name):
    try:
        s3_client = boto3.client('s3',region_name)
        
        buckets_response = s3_client.list_buckets()
           
    except ClientError as e:
        print(e)
        return False
    else:
        return buckets_response['Buckets']
    

list_of_buckets = list_regional_bucket(s3_data['bucket_name'][0])
print(list_of_buckets[0]['Name'])
