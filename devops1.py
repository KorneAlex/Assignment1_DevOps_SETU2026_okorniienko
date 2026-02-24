#!/usr/bin/env python3
import boto3
import subprocess
from create_security_group import create_security_group
from create_instance import create_instance
from create_bucket import create_bucket
from helpers import bcolors

ec2 = boto3.client("ec2")
instance_name="assignment1_okorniienko"
security_group="assignment1_security_group"
security_group_description="The security group for the assignment1"
pem_key = subprocess.run("ls | grep .pem", shell=True, capture_output=True, text=True)
monitoring_file = "monitoring.sh"

try:
    delete_security_group = ec2.delete_security_group(GroupName=security_group,)
except Exception as error:
    print(f"Cannot delete the security group with name {security_group}")
create_security_group(security_group, security_group_description)
instance_url = create_instance(instance_name, security_group)
bucket_url = create_bucket()

with open('okorniienko-websites.txt', 'w') as file:
    file.write("Instance Public IP:\t" + "http://" + instance_url + "\n")
    file.write("Instance metadata:\t" + "http://" + instance_url + "/metadata.html" + "\n")
    file.write("Bucket URL:\t\t\t" + bucket_url)
    
change_permissions = subprocess.run(["chmod", "+x", f"{monitoring_file}"])
try:
    print(f"{bcolors.HEADER}Coping file {monitoring_file} to {bcolors.OKBLUE}{instance_url}{bcolors.ENDC}")
    copy_monitoring_script = subprocess.run(["scp", "-i", f"{pem_key.stdout[:-1]}", f"{monitoring_file}", f"ec2-user@{instance_url}:~/"])
except Exception as error:
    print(f"[ {bcolors.FAIL}ERR{bcolors.ENDC} ] Cannot copy the {monitoring_file} over scp --> ", error)
try:
    print(f"{bcolors.HEADER}Opening ssh as ec2-user@{bcolors.OKBLUE}{instance_url}{bcolors.ENDC}")
    open_ssh = subprocess.run(["ssh", "-i", f"{pem_key.stdout[:-1]}", f"ec2-user@{instance_url}"])
except Exception as error:
    print(f"[ {bcolors.FAIL}ERR{bcolors.ENDC} ] Cannot connect over ssh to {instance_url} --> ", error)