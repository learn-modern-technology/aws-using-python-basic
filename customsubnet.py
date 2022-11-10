import os
import boto3
from botocore.exceptions import ClientError
import json_operations
import json

config_data = json_operations.loadjsondata("./configs/config.json")
region_name = config_data["Region"]
availability_zones = config_data["region_AZ"]
tagname = config_data["tagname"]
tagvalue = config_data["tagvalue"]
resourcetype = config_data["subnet_resource_type"]
ec2_jsondata_path = config_data["ec2data_path"]
ec2data = json_operations.loadjsondata(ec2_jsondata_path)
vpcid = ec2data["vpc_ids"][0]
cidr_sunet_A = config_data["subnet_cidr_A"]
cidr_sunet_B = config_data["subnet_cidr_B"]
cidr_sunet_C = config_data["subnet_cidr_C"]
cidr_sunet_D = config_data["subnet_cidr_D"]

subnet_client = boto3.client("ec2", region_name)

def create_pub_subnet():
    try:
        response = subnet_client.create_subnet(
                                            TagSpecifications=[
                                                {
                                                    'ResourceType': resourcetype,
                                                    'Tags': [
                                                        {
                                                            'Key': tagname,
                                                            'Value': tagvalue
                                                        },
                                                    ]
                                                },
                                            ],
                                            AvailabilityZone=availability_zones[0],
                                            ##AvailabilityZoneId='string',
                                            CidrBlock=cidr_sunet_A,
                                            ##Ipv6CidrBlock='string',
                                            ##OutpostArn='string',
                                            VpcId=vpcid,
                                            ## DryRun=True|False,
                                            Ipv6Native=False
                                            )
    except ClientError as e:
        print(e)
    else:
        return response['Subnet']['SubnetId']
    
def del_pub_subnet(del_subnet_id):
    try:
        del_response = subnet_client.delete_subnet(
                                SubnetId = del_subnet_id
                                )
        ec2data["subnet_ids"].remove(del_subnet_id)
    except ClientError as e:
        print(e)
    else:
        return del_response

### To invoke create_pub_subnet
subnet_id = create_pub_subnet()
print(subnet_id)
ec2data["subnet_ids"].append(subnet_id)


### To delete and remove subnetid
## response_del = del_pub_subnet(ec2data["subnet_ids"][0])
## print(response_del)

savejson_data_status = json_operations.savejsondata(ec2_jsondata_path, ec2data)
if savejson_data_status:
    print("Data saved in ec2data.json")