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
#CompletedProcess(args='ls | grep .pem', returncode=0, stdout='lab_okorniienko2026.pem\n', stderr='') // stdout[:-1] gets actual filename
pem_key = str(subprocess.run("ls | grep .pem", shell=True, capture_output=True, text=True).stdout[:-1])
monitoring_file = "monitoring.sh"

# try:
#     response = ec2.delete_security_group(
#         GroupName=security_group,
#     )
# except Exception as error:
#     print(f"Cannot delete the security group with name {security_group}")
create_security_group(security_group, security_group_description)
instance_url = create_instance(instance_name, security_group)
bucket_url = create_bucket()

with open('okorniienko-websites.txt', 'w') as file:
    file.write("Instance Public IP:\t" + "http://" + instance_url + "\n")
    file.write("Instance metadata:\t" + "http://" + instance_url + "/metadata.html" + "\n")
    file.write("Bucket URL:\t\t\t" + bucket_url)
    
#https://superuser.com/questions/125324/how-can-i-avoid-sshs-host-verification-for-known-hosts
print(f"{bcolors.HEADER}Monitoring tool{bcolors.ENDC}")
try:
    print(f"├── Coping file {monitoring_file} to {bcolors.OKBLUE}{instance_url}{bcolors.ENDC}")
    copy_monitoring_script = subprocess.run(f"scp -i {pem_key}  -o 'StrictHostKeyChecking no' {monitoring_file} ec2-user@{instance_url}:.", shell=True, capture_output=True, text=True)
    print(f"│\t└── [ {bcolors.OKGREEN}DONE{bcolors.ENDC} ] ")
except Exception as error:
    print(f"│\t└── [ {bcolors.FAIL}ERR{bcolors.ENDC} ] Cannot copy the {monitoring_file} over scp --> ", error)
    
try:
    print(f"└── Changing permissions for the monitoring file to +x and 700...{bcolors.ENDC}")
    change_permissions = subprocess.run(f"ssh -i {pem_key} -o 'StrictHostKeyChecking no' ec2-user@{bcolors.OKBLUE}{instance_url}{bcolors.ENDC} 'chmod +x {monitoring_file} && chmod 700 {monitoring_file}'", shell=True, capture_output=True, text=True)
    print(f"\t└── [ {bcolors.OKGREEN}DONE{bcolors.ENDC} ] ")
except Exception as error:
    print(f"\t└── [ {bcolors.FAIL}ERR{bcolors.ENDC} ] Cannot change permissions of {monitoring_file} at {bcolors.OKBLUE}{instance_url}{bcolors.ENDC} --> ", error)

try:
    print(f"\n{bcolors.HEADER}Opening ssh as ec2-user@{bcolors.OKBLUE}{instance_url}{bcolors.ENDC}")
    print("")
    print(f"{bcolors.HEADER}Finished{bcolors.ENDC}")
    print("")
    open_ssh = subprocess.run(f"ssh -i {pem_key} -o 'StrictHostKeyChecking no' ec2-user@{instance_url}", shell=True)
except Exception as error:
    print(f"[ {bcolors.FAIL}ERR{bcolors.ENDC} ] Cannot connect over ssh to {instance_url} --> ", error)
