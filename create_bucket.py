#!/usr/bin/env python3
import boto3
import subprocess
import webbrowser
import time
from helpers import id_generator, bcolors

s3 = boto3.resource("s3")
files_to_upload = [
    {'name':'indsex.html','type':'text/html'},
    {'name':'error.html','type':'text/html'}, 
    {'name':'logo.jpg','type':'image/jpeg'}
    ]
    
def create_bucket():
    bucket_name = 'okorniienko-' + str(id_generator())
    # TODO: check if exist and create another one if true
    print(bcolors.HEADER + f"Creating a bucked with name {bcolors.BOLD}{bcolors.OKGREEN}{bucket_name}" + bcolors.ENDC)
    print("├── Uploading index.html, error.html and aws.jpg to the bucket...")
    try:
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
            get_img = subprocess.run(["curl", "-L", "-o", "www/logo.jpg", "http://devops.setudemo.net/logo.jpg"])
            print("Uploading index.html, error.html and aws.jpg to the bucket...")
            for file in files_to_upload:
                try:
                    result = s3.Object(bucket_name, f'{file['name']}').put(Body=open(f'www/{file['name']}', 'rb'), ContentType=f'{file['type']}')
                    if result['ResponseMetadata']['HTTPStatusCode'] == 200:
                        print(f"[ {bcolors.OKGREEN}OK{bcolors.ENDC} ] Uploading {file['name']}")
                    else:
                        print(f"[ {bcolors.FAIL}ERR{bcolors.ENDC} ] Uploading {file['name']}")
                except Exception as error:
                    print(f"[ {bcolors.FAIL}ERR{bcolors.ENDC} ] Uploading {file['name']} --> ", error)
                    
            website_url = "http://%s.s3-website-%s.amazonaws.com" % (bucket_name, boto3.Session().region_name)
            print("Bucket created and configured for website hosting. Access it at: " + website_url)
            webbrowser.open(website_url)
            return website_url

        except Exception as error:
            print(error)
    except Exception as error:
        print(bcolors.FAIL +bcolors.BOLD + f"\nError creating the bucket\n{error}\n" + bcolors.ENDC)
        
if __name__ == "__main__":
    # create_bucket()
    bucket_name = "okorniienko-vzpvcz"
    # files_to_upload = [{'name':'indsex.html','type':'text/html'}, {'name':'error.html','type':'text/html'}, {'name':'logo.jpg','type':'image/jpeg'}]
    # print(files_to_upload)
    # for file in files_to_upload:
    #     try:
    #         result = s3.Object(bucket_name, f'{file['name']}').put(Body=open(f'www/{file['name']}', 'rb'), ContentType=f'{file['type']}')
    #         if result['ResponseMetadata']['HTTPStatusCode'] == 200:
    #             print(f"[ {bcolors.OKGREEN}OK{bcolors.ENDC} ] Uploading {file['name']}")
    #         else:
    #             print(f"[ {bcolors.FAIL}ERR{bcolors.ENDC} ] Uploading {file['name']}")
    #     except Exception as error:
    #         print(f"[ {bcolors.FAIL}ERR{bcolors.ENDC} ] Uploading {file['name']} --> ", error)
    # files_to_download = [
    #     {
    #         "link":"http://devops.setudemo.net/logo.jpg",
    #     }
    # ]
    
    check_link = subprocess.run('curl --silent --head http://devops.setudemo.net/logo.jpg | grep "200 OK"', shell=True, capture_output=True, text=True)
    print(check_link.stdout)
    if check_link.stdout:
        get_img = subprocess.run(["curl", "--silent", "-L", "-o", "www/logo.jpg", "http://devops.setudemo.net/logo.jpg"])
        print(f"[ {bcolors.OKGREEN}OK{bcolors.ENDC} ] Checking link")
    else:
        print(f"[ {bcolors.FAIL}ERR{bcolors.ENDC} ] Checking link --> {bcolors.FAIL}Invalid link{bcolors.ENDC}") 
    # print(wget_img)