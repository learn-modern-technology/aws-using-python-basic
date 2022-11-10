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
s3_data = json_operations.loadjsondata(s3_jsondata_path)

def upload_files(bucket_name, dir_path):
    session = boto3.Session()
    
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket_name)
    
    for root, subdirs, files in os.walk(dir_path):
        for file in files:
            full_path = os.path.join(root, file)
            ## print(full_path)
            with open (full_path, 'rb') as data:
                bucket.put_object(Key=full_path[len(root)+1:], Body = data)
                ## print(full_path[len(dir_path)+1:])

def upload_files_v2(bucket_name, dir_path):
    try:
        s3_client = boto3.client('s3')
        for root, subdir,files in os.walk(dir_path, topdown=True):
            print(f"root - {root}")
            print(f"subdir - {subdir}")
            print(f"files - {files}")
            for file in files:
                full_path = os.path.join(root, file)
                ## print(full_path)
                with open (full_path, 'rb') as data:
                    s3_client.put_object(Bucket = bucket_name, Key = full_path[len(root)+1:], Body = data)
                
    except ClientError as e:
        print(e)
        

## local_path = 'C:\\Users\\Sudhanshu\\gitrepository\\Python-AWS-SDK-Boto3\\S3Storage'
## bucket_name = s3_data['bucket_name'][0]
## upload_files(bucket_name,local_path)
## print(local_path)

local_path = 'C:\\Users\\Sudhanshu\\gitrepository\\Python-AWS-SDK-Boto3'
bucket_name = s3_data['bucket_name'][0]
upload_files_v2(bucket_name,local_path)
print(local_path)

## aws s3 sync . s3://ssingh-bucket-handson-202292705540680686/python_scripts/
