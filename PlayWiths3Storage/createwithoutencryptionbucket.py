from datetime import date, datetime
import os, sys
import json
import boto3
from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig
prev_dir = 'C:\\Users\\Sudhanshu\\gitrepository\\learncloud\\learn-aws-python'
sys.path.append(prev_dir)
## print(os.path.dirname(sys.executable))
## print(sys.executable)
## print(os.path.dirname(os.path.realpath(__file__)))
## print(sys.path)
import json_operations

config_data = json_operations.loadjsondata("./../configs/config.json")
s3_jsondata_path = config_data["s3_data_path"]
s3_data = json_operations.loadjsondata(s3_jsondata_path)
region_name = config_data["S3Region"]

current_datetime = datetime.now()
year        =current_datetime.year
month       =current_datetime.month
day         =current_datetime.day
hour        =current_datetime.hour
minute      =current_datetime.minute
second      =current_datetime.second
microsecond =current_datetime.microsecond
bucket_name =f"ssingh-bucket-handson-{year}{month}{day}{hour}{minute}{second}{microsecond}"

s3bucket = boto3.client("s3", region_name)

def create_bucket(bucketname, regionname):
    try:
        create_bucket_response = s3bucket.create_bucket(ACL = 'private',
                                                        Bucket =bucketname,
                                                        CreateBucketConfiguration = {
                                                            'LocationConstraint':regionname
                                                        })
        print(bucket_name)

        s3_data["bucket_name"].append(bucket_name)
    
    except ClientError as e:
        print(e)
    else:
        return create_bucket_response

create_bucket(bucket_name, region_name)

savejson_data_status = json_operations.savejsondata(s3_jsondata_path, s3_data)
if savejson_data_status:
    print("Data saved in storagedata.json")