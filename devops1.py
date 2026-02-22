#!/usr/bin/env python3
import boto3
import subprocess
from create_security_group import create_security_group
from create_instance import create_instance
from create_bucket import create_bucket

ec2 = boto3.client("ec2")
security_group="assignment1_security_group"
pem_key = subprocess.run("ls | grep .pem", shell=True, capture_output=True, text=True)

create_security_group(security_group)
instance_url = create_instance(security_group)
bucket_url = create_bucket()

with open('okorniienko-websites.txt', 'w') as file:
    file.write("Instance Public IP:\t" + "http://" + instance_url + "\n")
    file.write("Instance metadata:\t" + "http://" + instance_url + "/metadata.html" + "\n")
    file.write("Bucket URL:\t\t\t" + bucket_url)
    
change_permissions = subprocess.run(["chmod", "+x", "monitoring.sh"])
copy_monitoring_script = subprocess.run(["scp", "-i", f"{pem_key.stdout[:-1]}", "monitoring.sh", f"ec2-user@{instance_url}:~/"])
open_ssh = subprocess.run(["ssh", "-i", f"{pem_key.stdout[:-1]}", f"ec2-user@{instance_url}"])

# TODO: Error handlers and checks