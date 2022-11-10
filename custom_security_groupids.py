import os
import boto3
from botocore.exceptions import ClientError
import json_operations
import json

config_data = json_operations.loadjsondata("./configs/config.json")
region_name = config_data["Region"]
sg_resource_type = config_data["sg_resource_type"]
tagname = config_data["tagname"]
tagvalue = config_data["tagvalue"]
ec2_jsondata_path = config_data["ec2data_path"]
ec2data = json_operations.loadjsondata(ec2_jsondata_path)
print(f"ec2data - {ec2data}")

ec2_client = boto3.client("ec2",region_name)

def create_sec_group(sg_name, vpc_id):
    try:
        sg_response = ec2_client.create_security_group(
            Description= 'Create SG for Custom vpc',
            GroupName= sg_name,
            VpcId= vpc_id,
            TagSpecifications=
            [
                {
                    'ResourceType': sg_resource_type,
                    'Tags': [
                        {
                            'Key': tagname,
                            'Value': tagvalue
                        },
                    ]
                }
            ]
        )
        
        
    except ClientError as e:
        print(e)
    else:
        return sg_response['GroupId']


def delete_sec_group(sg_id):
    try:
        sg_del_response = ec2_client.delete_security_group(GroupId = sg_id)
        ec2data["sg_ids"].remove(sg_id)
    except ClientError as e:
        print(e)
    else:
        return sg_del_response

def attach_security_group_ingress(sg_id):
    try:
        sg_ingress_response = ec2_client.authorize_security_group_ingress(
            GroupId = sg_id,
            IpPermissions = [
               {
                   'IpProtocol':'tcp',
                   'FromPort':80,
                   'ToPort':80,
                   'IpRanges':[{'CidrIp':'0.0.0.0/0', 'Description':'My description'}]
               },
               {
                   'IpProtocol':'tcp',
                   'FromPort':22,
                   'ToPort':22,
                   'IpRanges':[{'CidrIp':'0.0.0.0/0', 'Description':'My description'}]
               }
            ]
        )
    except ClientError as e:
        print(e)
    else:
        return sg_ingress_response

### To create Custom Security Group
##sg_name = "VPC- Secutiry Group 01"
##sg_response_id = create_sec_group(sg_name, ec2data['vpc_ids'][0])
##ec2data["sg_ids"].append(sg_response_id)

### To attach inbound security group rules
sg_response = create_sec_group(ec2data['sg_ids'][0])
print(sg_response)

### To delete Custom Security Group
## sg_del_response_meta = delete_sec_group(ec2data['sg_ids'][0])
## print(f"sg_del_response_meta - {sg_del_response_meta}")

savejson_data_status = json_operations.savejsondata(ec2_jsondata_path, ec2data)
if savejson_data_status:
    print("Data saved in ec2data.json")