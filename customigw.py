import os
import boto3
from botocore.exceptions import ClientError
import json_operations
import json
import logging

config_data = json_operations.loadjsondata("./configs/config.json")
region_name = config_data["Region"]
availability_zones = config_data["region_AZ"]
tagname = config_data["tagname"]
tagvalue = config_data["tagvalue"]
resourcetype = config_data["igw_resource_type"]
ec2_jsondata_path = config_data["ec2data_path"]
ec2data = json_operations.loadjsondata(ec2_jsondata_path)

client_igw = boto3.client("ec2", region_name)

def create_igw():
    try:
        igw_response = client_igw.create_internet_gateway(
                                                    TagSpecifications=[
                                                    {
                                                        'ResourceType': resourcetype,
                                                        'Tags': [
                                                            {
                                                                'Key': tagname,
                                                                'Value': tagvalue
                                                            },
                                                        ]
                                                    }]
                                                    )
    except ClientError as e:
        print(e)
    else:
        return igw_response['InternetGateway']['InternetGatewayId']
    
def attach_igw(attach_igw_id, attach_vpc_id):
    try:
        attach_igw_response = client_igw.attach_internet_gateway(
                                                             InternetGatewayId=attach_igw_id,
                                                             VpcId=attach_vpc_id
                                                             )
    except ClientError as e:
        print(e)
    else:
        return attach_igw_response


def detach_igw(detach_igw_id, detach_vpc_id):
    try:
        detach_igw_response = client_igw.detach_internet_gateway(
                                                             InternetGatewayId=detach_igw_id,
                                                             VpcId=detach_vpc_id
                                                             )
    except ClientError as e:
        print(e)
    else:
        return detach_igw_response

def delete_igw(del_igw_id):
    try:
        delete_igw_response = client_igw.delete_internet_gateway(
                                                                InternetGatewayId= del_igw_id)
        ec2data["igw_ids"].remove(del_igw_id)
        json_operations.savejsondata(ec2_jsondata_path, ec2data)
        print(f"Deleted Internet Gateway ")
        
    except ClientError as e:
        print(e)
    else:
        return delete_igw_response

### To invoke create_igw function 
igw_id = create_igw()
print(f"igw_id - {igw_id}")
ec2data["igw_ids"].append(igw_id)

### To attach internet gateway
## attach_igw_result = attach_igw(ec2data['igw_ids'][0], ec2data['vpc_ids'][0])
## if len(attach_igw_result) != 0:
##     print(f"Attach Internet Gateway - {ec2data['igw_ids'][0]} to VPC - {ec2data['vpc_ids'][0]}")
## else:
##     print(f"Internet Gateway didn't attach to the vpc")

### To detach internet gateway
## detach_igw_result = detach_igw(ec2data['igw_ids'][0], ec2data['vpc_ids'][0])
## if len(detach_igw_result) != 0:
##     print(f"Detached Internet Gateway - {ec2data['igw_ids'][0]} from VPC - {ec2data['vpc_ids'][0]}")
## else:
##     print(f"Internet Gateway didn't detach to the vpc")
 
## ### To delete internet gateway
## delete_igw_result = delete_igw(ec2data['igw_ids'][0])
## print(delete_igw_result)

savejson_data_status = json_operations.savejsondata(ec2_jsondata_path, ec2data)
if savejson_data_status:
    print("Data saved in ec2data.json")