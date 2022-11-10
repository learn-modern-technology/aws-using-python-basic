import os
import boto3
from botocore.exceptions import ClientError
import json_operations
import json

config_data = json_operations.loadjsondata("./configs/config.json")
region_name = config_data["Region"]
vpc_cidr = config_data["custom_vpc_ip"]
tenancy = config_data["Tenancy"]
maxvpclist = config_data["maxvpclist"]
tagname = config_data["tagname"]
tagvalue = config_data["tagvalue"]
resource_type = config_data["ec2_resource_type"]
key_resource_type = config_data["key_resource_type"]
ec2_resource_type = config_data["ec2_resource_type"]
ami_id = config_data["ec2_ami_id"]
instance_type = config_data["ec2_instance_type"]
key_path = config_data["ec2_key_path"]
key_name = config_data["ec2_key_name"]
user_data = config_data["ec2_user_data"]
ec2_jsondata_path = config_data["ec2data_path"]
ec2data = json_operations.loadjsondata(ec2_jsondata_path)
print(ec2data)

ec2_client = boto3.client("ec2", region_name)


def create_ec2_key_pair():
    try:
        if not os.path.exists("key_path"):
            key_resposne = ec2_client.create_key_pair(
                                                    KeyName=key_name,
                                                    KeyType='rsa',
                                                    KeyFormat='pem',
                                                    TagSpecifications=[
                                                    {
                                                      'ResourceType': key_resource_type,
                                                         'Tags': [
                                                               { 'Key': tagname,
                                                                 'Value': tagvalue
                                                                }
                                                                ]
                                                    }
                                                    ]
                                                  )
        save_private_key = key_resposne['KeyMaterial']
        
        with os.fdopen(os.open(key_path,os.O_WRONLY | os.O_CREAT, 0o400),"w+") as handle:
            handle.write(save_private_key)
        
    except ClientError as e:
        print(e)


def delete_unused_key_pair(del_key_name):
    delete_response = ec2_client.delete_key_pair(KeyName=del_key_name)
    print(delete_response)

### To create ec2 key pair  
## create_ec2_key_pair()

### To delete the unused key_pair
## delete_unused_key_pair("lambda-ec2")    

###----------------------------------------------------------------------------
## To create EC2 instances
def create_ec2_instance(subnet_ec2_id, sg_ec2_ids):
    try:
        ##ni_response = ec2_client.create_network_interface(subnet_id =subnet_ec2_id,
        ##                                                  groups = [sg_ec2_ids],
        ##                                                  associate_public_ip_address = True)
        print("Creating EC2 Instance")
        ec2_instance_response = ec2_client.run_instances(
            ImageId = ami_id,
            InstanceType = instance_type,
            KeyName = key_name,
            SubnetId = subnet_ec2_id,
            UserData= user_data,
            BlockDeviceMappings=[
            {
            'DeviceName': '/dev/xvda',
            ##'VirtualName': 'string',
            'Ebs': {
                'DeleteOnTermination': True,
                ##'Iops': '100/3000',
                'SnapshotId': 'snap-0834d7afbcb68efb7',
                'VolumeSize': 8,
                'VolumeType': 'gp2',
                ##'KmsKeyId': 'string',
                ##'Throughput': 123,
                ##'OutpostArn': 'string',
                'Encrypted': False
                 },
            ##'NoDevice': 'string'
            },
            ],
            MaxCount = 1,
            MinCount = 1,
            Monitoring={
                    'Enabled': False
                },
            SecurityGroupIds=[sg_ec2_ids],
            ##network_interfaces = ni_response,
            EbsOptimized = False,
            IamInstanceProfile={
                'Arn': 'arn:aws:iam::293938022129:instance-profile/ec2-cloudwatchfullrole',
                ##'Name': 'ec2-cloudwatchfullrole'
            },
        )
    except ClientError as e:
        print(e)
    else:
        return ec2_instance_response['Instances'][0]['InstanceId']

def terminate_ec2_instances(ec2_instance_id):
    try:
        terminate_ec2_response = ec2_client.terminate_instances(InstanceIds = ec2_instance_id)
    except ClientError as e:
        print(e)
    else:
        return terminate_ec2_response['TerminatingInstances'][0]['InstanceId']

### To create an ec2 instances
## instance_id=create_ec2_instance(ec2data["subnet_ids"][0], ec2data["sg_ids"][0])
## print(f"Instance_Id - {instance_id}")
## ec2data["instance_ids"].append(instance_id)

### To assing a public ip for the instances

### To terminate an ec2 instances
terminated_instance_id = terminate_ec2_instances(ec2data["instance_ids"])
print(f"terminated ec2-instance response - {terminated_instance_id}")
ec2data["instance_ids"].remove(terminated_instance_id)


savejson_data_status = json_operations.savejsondata(ec2_jsondata_path, ec2data)
if savejson_data_status:
    print("Data saved in ec2data.json")