#!/usr/bin/env python3

# https://docs.aws.amazon.com/boto3/latest/guide/ec2-example-security-group.html

import boto3
from helpers import bcolors

ec2 = boto3.client("ec2")

def create_security_group(name, description):
    print(bcolors.HEADER + f"Creating a security group with name {bcolors.BOLD}{bcolors.OKGREEN}{name}" + bcolors.ENDC)
    try:
        response = ec2.create_security_group(
            Description=description,
            GroupName=name,
        )
        
        try:
            security_group_id = response['GroupId']
            print(f"│\t└── [ {bcolors.OKBLUE}INFO{bcolors.ENDC} ] Group ID: {bcolors.BOLD}{bcolors.OKGREEN}{security_group_id}{bcolors.ENDC}")
        except Exception as error:
            print(f"│\t└── [ {bcolors.FAIL}ERR{bcolors.ENDC} ] Cannot get Group ID --> {error})")
        print(f"│\t└── [ {bcolors.OKBLUE}INFO{bcolors.ENDC} ] Group description: {bcolors.BOLD}{bcolors.OKGREEN}{description}{bcolors.ENDC}")

        data = ec2.authorize_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=[
                    {'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                ])
        print(f"└── [ {bcolors.OKGREEN}DONE{bcolors.ENDC} ] Security group {bcolors.BOLD}{bcolors.OKGREEN}{name}{bcolors.ENDC} has been created\n")
    except Exception as error:
        print(f"└── [ {bcolors.FAIL}FAIL{bcolors.ENDC} ] Failed to create security group --> {error}\n")

if __name__ == "__main__":
    create_security_group("test","test_group")
    response = ec2.delete_security_group(
        GroupName='test',
    )