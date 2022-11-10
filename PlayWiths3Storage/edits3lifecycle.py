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
import logging

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')

config_data = json_operations.loadjsondata("./../configs/config.json")
s3_jsondata_path = config_data["s3_data_path"]
s3_data = json_operations.loadjsondata(s3_jsondata_path)
region_name = config_data["S3Region"]
s3_policy = {
    "Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "id-1",
			"Effect": "Allow",
			"Principal": {
				"AWS": "arn:aws:iam::293938022129:*"
			},
			"Action": "*",
			"Resource": [
				"arn:aws:s3:::*"
			]
		}
	]
}

s3bucket = boto3.client("s3", region_name)
print(s3_data['bucket_name'][0])

def edit_s3_lifecycle(bucktname):
    try:
      policy_response = s3bucket.put_bucket_policy(Bucket=bucktname,
                                                   ChecksumAlgorithm = 'SHA256',
                                                   ConfirmRemoveSelfBucketAccess = False,
                                                   Policy= '{"Statement": [{"Sid": "id-1","Effect": "Allow","Principal": "*","Action": "*","Resource": ["arn:aws:s3:::ssingh-bucket-handson-202292705540680686/*"]}]}',
                                                   ExpectedBucketOwner = '293938022129'
                                                   )
    except ClientError as e:
        print(e)
    else:
      return policy_response

s3_policy_response = edit_s3_lifecycle(s3_data['bucket_name'][0])
print(s3_policy_response)
