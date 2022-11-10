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

def delete_all_object(bucket_name):
    try:
        s3_client = boto3.client('s3')
        
        list_response = s3_client.list_objects_v2(Bucket = bucket_name)
        
        files_in_s3 = list_response["Contents"]
        file_to_delete =[]

        for file in files_in_s3:
            file_to_delete.append({"Key": file["Key"]})
        print (file_to_delete)

        delete_objects_response = s3_client.delete_objects(
            Bucket= bucket_name, Delete = {"Objects": file_to_delete})
    
    except ClientError as e:
        print(e)
        return False
    else:
        print (file_to_delete)
        return delete_objects_response

delete_objects_response = delete_all_object(s3_data['bucket_name'][0])
print(delete_objects_response)
