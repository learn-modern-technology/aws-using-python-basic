import os
import boto3
from botocore.exceptions import ClientError
import json_operations
import json
import logging

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')

config_data = json_operations.loadjsondata("./configs/config.json")
region_name = config_data["Region"]
vpc_cidr = config_data["custom_vpc_ip"]
tenancy = config_data["Tenancy"]
maxvpclist = config_data["maxvpclist"]
tagname = config_data["tagname"]
tagvalue = config_data["tagvalue"]
resourcetype = config_data["vpc_resource_type"]
ec2_jsondata_path = config_data["ec2data_path"]
ec2data = json_operations.loadjsondata(ec2_jsondata_path)
print(ec2data)

## Create Custome VPC
vpc_resources = boto3.resource("ec2",region_name)

def create_custom_vpc():
    try:
        create_vpc_response = vpc_resources.create_vpc(CidrBlock = vpc_cidr,
                                            InstanceTenancy = tenancy,
                                            TagSpecifications = [{
                                                        'ResourceType': resourcetype, ##'vpc',
                                                        'Tags': [ {
                                                            "Key": tagname, ##"Name",
                                                            "Value": tagvalue, ##"my-vpc-using-python"
                                                    } ]}
                                                ])
        
    except ClientError as ce:
        ##logger.exception('Could not create a custom vpc')
        print(ce)
    else:
        return create_vpc_response.id

## Describe custom vpc based on vpc_list
vpc_describe_resrcs = boto3.client("ec2",region_name)
def describe_custom_vpc(vpcid_list):
    try:
        response_vpcids = vpc_describe_resrcs.describe_vpcs(
            VpcIds = vpcid_list
        )
                     
    except ClientError as e :
        ##logger.exception('Could not describe vpc')
        print (e)
    else:
        return response_vpcids

vpc_delete_rsrcs = boto3.client("ec2", region_name)
def delete_custom_vpc(vpc_ids):
    try:
        response_delete_vpcs = vpc_delete_rsrcs.delete_vpc(VpcId=vpc_ids)
        ec2data["vpc_ids"].remove(vpc_ids)
        
    except ClientError as e :
        print(e)
    else:
        return response_delete_vpcs
    
### To Invoke create_custome_vpc function
vpc_data = create_custom_vpc()
ec2data["vpc_ids"].append(vpc_data)
print(vpc_data)

### To invoke describe_custom_vpc function based on vpcids list
## list_vpc = describe_custom_vpc(ec2data["vpc_ids"])
## print(list_vpc)

### To invoke delete_custom_vpc function based on vpcids list
## vpc_list = delete_custom_vpc(ec2data["vpc_ids"][0])
## print(vpc_list)

savejson_data_status = json_operations.savejsondata(ec2_jsondata_path, ec2data)
if savejson_data_status:
    print("Data saved in ec2data.json")