#!/usr/bin/env python3
import boto3
import subprocess
import webbrowser
import time
from helpers import id_generator

s3 = boto3.resource("s3")
    
def create_bucket():
    bucket_name = 'okorniienko-' + str(id_generator())
    get_img = subprocess.run(["curl", "-L", "-o", "www/logo.jpg", "http://devops.setudemo.net/logo.jpg"])

    # TODO: check if exist and create another one if true
    bucket = s3.create_bucket(Bucket=bucket_name)
    s3_client = boto3.client('s3')
    s3_client.delete_public_access_block(Bucket=bucket_name)
    try:
        website_configuration = {
            'ErrorDocument': {'Key': 'error.html'},
            'IndexDocument': {'Suffix': 'index.html'},
        }
        
        bucket_policy='''{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": [
                        "s3:GetObject"
                    ],
                    "Resource": [
                        "arn:aws:s3:::%s/*"
                    ]
                }
            ]
        }''' % bucket_name
        s3_client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
        time.sleep(2)
        bucket_website = s3.BucketWebsite(bucket_name)
        time.sleep(2)
        response = bucket_website.put(WebsiteConfiguration=website_configuration)
        time.sleep(2)
        print("Uploading index.html and aws.jpg to the bucket...")
        upload_file = s3.Object(bucket_name, "index.html").put(Body=open("www/index.html", 'rb'), ContentType='text/html')
        upload_file = s3.Object(bucket_name, "error.html").put(Body=open("www/error.html", 'rb'), ContentType='text/html')
        upload_file = s3.Object(bucket_name, "logo.jpg").put(Body=open("www/logo.jpg", 'rb'), ContentType='image/jpeg')
        website_url = "http://%s.s3-website-%s.amazonaws.com" % (bucket_name, boto3.Session().region_name)
        print("Bucket created and configured for website hosting. Access it at: " + website_url)
        webbrowser.open(website_url)
        return website_url

    except Exception as error:
        print(error)
        
if __name__ == "__main__":
    create_bucket()