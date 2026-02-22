#!/usr/bin/env python3

# https://docs.aws.amazon.com/boto3/latest/guide/ec2-example-security-group.html

import boto3

ec2 = boto3.client("ec2")

def create_security_group(name):
    try:
        response = ec2.create_security_group(
            Description='The security group for the assignment1',
            GroupName=name,
        )
        security_group_id = response['GroupId']
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
        print(f"Security group {name} has been created")
    except Exception as error:
        print (error)
