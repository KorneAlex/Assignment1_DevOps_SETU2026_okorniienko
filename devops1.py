#!/usr/bin/env python3
import boto3
import subprocess
from create_security_group import create_security_group
from create_instance import create_instance
from create_bucket import create_bucket
from create_ami import create_ami
from monitoring import monitoring
from helpers import bcolors

ERR=f"{bcolors.FAIL}ERR{bcolors.ENDC}"
DONE=f"{bcolors.OKGREEN}DONE{bcolors.ENDC}"

ec2 = boto3.client("ec2")
# looking for the .pem file in the script directory
try:
    pem_key = str(subprocess.run("ls | grep .pem", shell=True, capture_output=True, text=True).stdout[:-1]) 
except:
    pem_key = input("The .pem file is not found or more than 1. Please enter the file name in format file_name.pem: ")

# User variables
monitoring_file = "monitoring.sh"
instance_name="assignment1_okorniienko"
security_group="assignment1_security_group"
security_group_description="The security group for the assignment1"
image_name="assignment1_okorniienko_image"
image_description="Image of the assignment1_okorniienko instance"

#CompletedProcess(args='ls | grep .pem', returncode=0, stdout='lab_okorniienko2026.pem\n', stderr='') // stdout[:-1] gets actual filename
# try:
#     response = ec2.delete_security_group(
#         GroupName=security_group,
#     )
# except Exception as error:
#     print(f"Cannot delete the security group with name {security_group}")

create_security_group(security_group, security_group_description)
instance_response = create_instance(instance_name, security_group)
instance=instance_response['obj']
instance_url="" # needed in case when there is an issue with instance creation
if instance_response['status'] == 1:
    print(f"[ {ERR} ] {bcolors.WARNING}Something went wrong during instance creation. Skipping everything dependant on instance...{bcolors.ENDC}")
else:
    instance_url = instance.public_ip_address
    create_ami(instance.id, image_name, image_description)
    monitoring(instance.id)
bucket_url = create_bucket()

with open('okorniienko-websites.txt', 'w') as file:
    if instance_response['status'] == 0:
        file.write("Instance Public IP:\t" + "http://" + instance_url + "\n")
        file.write("Instance metadata:\t" + "http://" + instance_url + "/metadata.html" + "\n")
    else:
        file.write("Instance Public IP:\t" + "error creating the instance" + "\n")
        file.write("Instance metadata:\t" + "error creating the instance" + "\n")
    file.write("Bucket URL:\t\t\t" + bucket_url)
    
#https://superuser.com/questions/125324/how-can-i-avoid-sshs-host-verification-for-known-hosts
if instance_response['status'] == 0:
    print(f"\n╭ {bcolors.HEADER}Monitoring tool{bcolors.ENDC}")
    try:
        print(f"├── Coping file {monitoring_file} to {bcolors.OKBLUE}{instance_url}{bcolors.ENDC}")
        copy_monitoring_script = subprocess.run(f"scp -i {pem_key}  -o 'StrictHostKeyChecking no' {monitoring_file} ec2-user@{instance_url}:.", shell=True, capture_output=True, text=True)
        print(f"│\t└── [ {DONE} ] ")
    except Exception as error:
        print(f"│\t└── [ {ERR} ] Cannot copy the {monitoring_file} over scp --> ", error)
    
    try:
        print(f"└── Changing permissions for the monitoring file to +x and 700...{bcolors.ENDC}")
        change_permissions = subprocess.run(f"ssh -i {pem_key} -o 'StrictHostKeyChecking no' ec2-user@{bcolors.OKBLUE}{instance_url}{bcolors.ENDC} 'chmod +x {monitoring_file} && chmod 700 {monitoring_file}'", shell=True, capture_output=True, text=True)
        print(f"\t└── [ {DONE} ] ")
    except Exception as error:
        print(f"\t└── [ {ERR} ] Cannot change permissions of {monitoring_file} at {bcolors.OKBLUE}{instance_url}{bcolors.ENDC} --> ", error)
print("")
print(f"{bcolors.HEADER}Finished{bcolors.ENDC}")

if instance_response['status'] == 0:
    try:
        print(f"\n{bcolors.HEADER}Opening ssh as ec2-user@{bcolors.OKBLUE}{instance_url}{bcolors.ENDC}")
        open_ssh = subprocess.run(f"ssh -i {pem_key} -o 'StrictHostKeyChecking no' ec2-user@{instance_url}", shell=True)
    except Exception as error:
        print(f"[ {ERR} ] Cannot connect over ssh to {instance_url} --> ", error)
