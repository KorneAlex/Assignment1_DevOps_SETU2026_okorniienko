#!/usr/bin/env python3
import boto3
import subprocess
import webbrowser
import time
from helpers import id_generator, bcolors

s3 = boto3.resource("s3")
files_to_upload = [
    {'name':'index.html','type':'text/html'},
    {'name':'error.html','type':'text/html'}
    ]
files_to_download = [
        {"link":"http://devops.setudemo.net/logo.jpg"}
    ]
    
def create_bucket():
    bucket_name = 'okorniienko-' + str(id_generator())
    
    # checking if exist
    buckets = []
    for bucket in s3.buckets.all():
        buckets.append(bucket.name)
    while bucket_name in buckets:
        # print("This bucket name is already exist, generating a new one...")
        bucket_name = 'okorniienko-' + str(id_generator())
        # print("New bucket name: ", bucket_name)
    
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
    
    print(bcolors.HEADER + f"Creating a bucked with name {bcolors.BOLD}{bcolors.OKGREEN}{bucket_name}" + bcolors.ENDC)
    try:
        bucket = s3.create_bucket(Bucket=bucket_name)
        s3_client = boto3.client('s3')
        
        print("├── Deleting public access block...")
        try:
            s3_client.delete_public_access_block(Bucket=bucket_name)
            print(f"│\t└── [ {bcolors.OKGREEN}OK{bcolors.ENDC} ] Access block deleted")
        except Exception as error:
            print(f"│\t└── [ {bcolors.FAIL}ERR{bcolors.ENDC} ] Access block deletion failed --> {error}")
            
        print("├── Applying policy...")
        try:
            s3_client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
            print(f"│\t└── [ {bcolors.OKGREEN}OK{bcolors.ENDC} ] Policy applied")
        except Exception as error:
            print(f"│\t└── [ {bcolors.FAIL}ERR{bcolors.ENDC} ] Policy application failed --> {error}")
        print("├── Enabling bucket website...")
        try:
            bucket_website = s3.BucketWebsite(bucket_name)
            print(f"│\t└── [ {bcolors.OKGREEN}OK{bcolors.ENDC} ] Bucket website enabled")
        except Exception as error:
            print(f"│\t└── [ {bcolors.FAIL}ERR{bcolors.ENDC} ] Website enable failed --> {error}")
        print("├── Applying website configuration...")
        try:
            response = bucket_website.put(WebsiteConfiguration=website_configuration)
            print(f"│\t└── [ {bcolors.OKGREEN}OK{bcolors.ENDC} ] Website configuration applied")
        except Exception as error:
            print(f"│\t└── [ {bcolors.FAIL}ERR{bcolors.ENDC} ] Website configuration apply failed --> {error}")
 
             
        print("├── Downloading required files...")
        for link in files_to_download:
            link_status = subprocess.run(f'curl --silent --head {link['link']} | grep "200 OK"', shell=True, capture_output=True, text=True)
            if link_status.stdout:
                file_name = link['link'].split('/')[-1] # https://stackoverflow.com/questions/1633932/slice-a-string-after-a-certain-phrase
                file_type = subprocess.run(f'curl --silent --head {link['link']} | grep Content-Type', shell=True, capture_output=True, text=True).stdout.split('Content-Type: ')[-1].strip()
                get_file = subprocess.run(["curl", "--silent", "-L", "-o", f"www/{file_name}", f"{link['link']}"])
                files_to_upload.append({'name':f'{file_name}','type':f'{file_type}'})
                print(f"│\t└── [ {bcolors.OKGREEN}OK{bcolors.ENDC} ] Checking file at {link['link']}")
            else:
                print(f"│\t└── [ {bcolors.FAIL}ERR{bcolors.ENDC} ] Checking file at {link['link']} --> {bcolors.FAIL}Not found{bcolors.ENDC}") 
            
            
        print("├── Uploading files to the bucket...")
        for index, file in enumerate(files_to_upload):
            try:
                result = s3.Object(bucket_name, f'{file['name']}').put(Body=open(f'www/{file['name']}', 'rb'), ContentType=f'{file['type']}')
                if result['ResponseMetadata']['HTTPStatusCode'] == 200:
                    if index == len(files_to_upload)-1:
                        print(f"│\t└── [ {bcolors.OKGREEN}OK{bcolors.ENDC} ] Uploading {file['name']}")
                    else:
                        print(f"│\t├── [ {bcolors.OKGREEN}OK{bcolors.ENDC} ] Uploading {file['name']}")
                else:
                    print(f"│\t└── [ {bcolors.FAIL}ERR{bcolors.ENDC} ] Uploading {file['name']}")
            except Exception as error:
                print(f"[ {bcolors.FAIL}ERR{bcolors.ENDC} ] Uploading {file['name']} --> ", error)
                
        website_url = "http://%s.s3-website-%s.amazonaws.com" % (bucket_name, boto3.Session().region_name)
        print(f"└── [ {bcolors.OKGREEN}DONE{bcolors.ENDC} ] The bucket has been created and configured for the website hosting. \nAccess it at: {bcolors.OKBLUE}" + website_url + f"{bcolors.ENDC}\n")
        webbrowser.open(website_url)
        return website_url
    
    except Exception as error:
        print(f"└── [ {bcolors.FAIL}ERR{bcolors.ENDC} ] Error creating the bucket --> {error}\n" + bcolors.ENDC)
        
if __name__ == "__main__":
    create_bucket()