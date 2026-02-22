#!/usr/bin/env python3

# https://tutors.dev/lab/setu-hdip-comp-sci-2025-devops/topic-02-Python/unit-1-Python-Intro/book-2-aws-ec2-s3/Metadata

import boto3
import webbrowser
import time
region = 'us-east-1b'
ec2 = boto3.resource('ec2', region_name='us-east-1')

def create_instance(security_group="default"):
    instance = ec2.create_instances(
        ImageId='ami-0f3caa1cf4417e51b',
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.nano',
        KeyName='lab_okorniienko2026',
        UserData="""#!/bin/bash
            yum update -y
            yum install httpd -y
            systemctl enable httpd
            systemctl start httpd
            TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
            echo "This instance is running in availability zone:" > metadata.html
            curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/placement/availability-zone >> metadata.html
            echo "<hr>The instance ID is: " >> metadata.html
            curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id >> metadata.html
            echo "<hr>The instance type is: " >> metadata.html
            curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-type >> metadata.html
            echo "<hr>The public IPv4 is: " >> metadata.html
            curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/public-ipv4 >> metadata.html
            echo "<hr>The ami-id is: " >> metadata.html
            curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/ami-id >> metadata.html
            sudo mv metadata.html /var/www/html""",
        Placement={
            'AvailabilityZone': 'us-east-1b'
        },

        SecurityGroupIds=[
            security_group,
        ],
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'assignment1_okorniienko'
                        }
                    ]
                }
            ]
    )
    
    print("Creating instance...")
    instance[0].wait_until_running()
    instance[0].load()
    print("Instance created and running on IP: http://" + instance[0].public_ip_address)
    print("Waiting for the web server to start in 20 sec...")
    time.sleep(20)
    webbrowser.open("http://" + instance[0].public_ip_address + "/metadata.html")
    return instance[0].public_ip_address
    
if __name__ == "__main__":
    create_instance()