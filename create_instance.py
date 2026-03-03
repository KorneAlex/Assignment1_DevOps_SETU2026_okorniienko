#!/usr/bin/env python3

# https://tutors.dev/lab/setu-hdip-comp-sci-2025-devops/topic-02-Python/unit-1-Python-Intro/book-2-aws-ec2-s3/Metadata

import boto3
import webbrowser
import time
import subprocess
import requests
import sys
from helpers import bcolors
pem_key = "lab_okorniienko2026.pem"
region = 'us-east-1b' # as requested
ec2 = boto3.resource('ec2', region_name='us-east-1')

def create_instance(instance_name, security_group="default"):
    print(bcolors.HEADER + f"Creating an instance with name {bcolors.BOLD}{bcolors.OKGREEN}{instance_name}" + bcolors.ENDC)
    try:
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
                                'Value': instance_name
                            }
                        ]
                    }
                ]
        )
        print("├── Waiting until running...")
        instance[0].wait_until_running()
        print("├── Loading...")
        instance[0].load()
        print(f"└── [ {bcolors.OKGREEN}DONE{bcolors.ENDC} ] Instance created and running on IP: {bcolors.OKBLUE}http://{instance[0].public_ip_address}{bcolors.ENDC}")
        print(f"\n{bcolors.HEADER}Waiting for the web server to start...{bcolors.ENDC}")
        
        
        # Source - https://stackoverflow.com/a/6169274
        # Posted by 6502, modified by community. See post 'Timeline' for change history
        # Retrieved 2026-03-02, License - CC BY-SA 4.0
        status = ""
        timer = 0
        while(status != 200):
            try:
                r = requests.get(f'http://{instance[0].public_ip_address}/metadata.html')
                status = r.status_code
            except Exception as error:
                pass
            if timer>59:
                sys.stdout.write(f"\r└── [ {bcolors.FAIL}ERR{bcolors.ENDC} ] Cannot connect (waiting time exceeded)\n")
                sys.stdout.flush()
                break
            if status == 200:
                sys.stdout.write(f"\r└── [ {bcolors.OKGREEN}OK{bcolors.ENDC} ] Connected to the webserver\n")
                sys.stdout.flush()
                break
            sys.stdout.write("\r└── [ %i/60 ] Trying to connect..." % timer)
            sys.stdout.flush()
            time.sleep(1)
            timer += 1
            
        
        
        
        webbrowser.open("http://" + instance[0].public_ip_address + "/metadata.html")
        return instance[0]
    except Exception as error:
        print(f"└── [ {bcolors.FAIL}ERR{bcolors.ENDC} ] Error creating the instance --> {error}\n" + bcolors.ENDC)
        
    
if __name__ == "__main__":
    create_instance("testami1", "assignment1_security_group")
    # response = requests.get('http://example.com')
    # print(response.status_code)
    
    # Source - https://stackoverflow.com/a/6169274
# Posted by 6502, modified by community. See post 'Timeline' for change history
# Retrieved 2026-03-02, License - CC BY-SA 4.0
    import sys
    # s="222"
    # for i, ss in enumerate(s):
    #     sys.stdout.write("\rDoing thing %i" % i)
    #     time.sleep(2)
    #     sys.stdout.flush()

    # status = ""
    # timer = 0
    # while(status != 200):
    #     try:
    #         r = requests.get(f'http://sdsds.coccm/sdsd/metadata.html')
    #         status = r.status_code
    #     except Exception as error:
    #         pass
    #     if timer>1:
    #         sys.stdout.write(f"\r\t└── [ {bcolors.FAIL}ERR{bcolors.ENDC} ] Cannot connect (waiting time exceeded)\n")
    #         sys.stdout.flush()
    #         break
    #     if status == 200:
    #         sys.stdout.write(f"\r\t└── [ {bcolors.OKGREEN}OK{bcolors.ENDC} ] Connected\n")
    #         sys.stdout.flush()
    #         break
    #     sys.stdout.write("\r\t└── [ %i/60 ] Trying to connect" % timer)
    #     sys.stdout.flush()
    #     time.sleep(1)
    #     timer += 1