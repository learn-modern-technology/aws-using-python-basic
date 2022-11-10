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

def delete_single_object(bucket_name, file_name):
    try:
        s3_delete_client = boto3.client('s3')
        delete_objects_response = s3_delete_client.delete_object(
            Bucket= bucket_name, Key= file_name)
    
    except ClientError as e:
        print(e)
        return False
    else:
        return delete_objects_response

file_name_to_delete = "11.+GetSummary.py"
delete_objects_response = delete_single_object(s3_data['bucket_name'][0],file_name_to_delete)
print(delete_objects_response)
