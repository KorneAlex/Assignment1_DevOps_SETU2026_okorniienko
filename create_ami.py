#!/usr/bin/env python3

import boto3
import time
from helpers import bcolors
import subprocess

ec2 = boto3.resource('ec2')    
ec2_client = boto3.client('ec2')    
image_name="assignment1_okorniienko_image"
image_description="Image of the assignment1_okorniienko instance"
instance_id="i-0bf36ccf6afdabf85"
timestamp=int(time.time())

def create_ami(instance_id, name, description):
    print(f"\n{bcolors.HEADER}Creating AMI...{bcolors.ENDC}")
    try:
        instance = ec2.Instance(instance_id)
        image = instance.create_image(
            Name=name + "-" + str(timestamp),
            Description=description,
            NoReboot=True
        )
        print(f"└── [ {bcolors.OKGREEN}OK{bcolors.ENDC} ] AMI has been created")
        print(f"\t├── [ {bcolors.OKBLUE}INFO{bcolors.ENDC} ] AMI ID: {bcolors.OKBLUE}{image.id}{bcolors.ENDC}")
        print(f"\t└── [ {bcolors.OKBLUE}INFO{bcolors.ENDC} ] AMI name: {bcolors.OKBLUE}{image.name}{bcolors.ENDC}")
    except Exception as error:
        print(f"└── [ {bcolors.FAIL}FAIL{bcolors.ENDC} ] Error creating the AMI. {error}")

    
if __name__ == "__main__":
    # create_ami(instance_id ,image_name, image_description)
    # print(timestamp)
    # response = ec2_client.describe_images(Owners=['self'])

    # for image in response['Images']:
    #     print(image['ImageId'], image['Name'], image['State'])
    #     ec2_client.delete_image(image['ImageId'])
    # new_instance = ec2.create_instances(
    #     ImageId=image.id,
    #     MinCount=1,
    #     MaxCount=1,
    #     InstanceType='t2.nano',
    #     KeyName='blaa'
    # )

    # print(new_instance[0].id)
    
    script_name="devops1"
    directory=subprocess.run("pwd", shell=True, capture_output=True, text=True).stdout
    checkname=subprocess.run(f"ls{directory} | grep {script_name}", shell=True, capture_output=True, text=True).stdout
    if checkname:
        print(checkname, directory)
    else:
        print(checkname, directory)
        print(f"{bcolors.FAIL}Please run the script being in the script directory{bcolors.ENDC}")
