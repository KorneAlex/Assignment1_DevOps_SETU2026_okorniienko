# Assignment1 — DevOps Project for SETU 2026

## Overview
DevOps assignment demonstrating core practices: automated build, infrastructure as code and deployment automation.

The overall objective of this assignment is to write a Python 3 program to automate the process of 
creating, launching and monitoring public-facing web servers in the Amazon cloud. A web server will 
run on an EC2 instance and an S3 bucket will also be used to serve some static content. The program 
that does this must be called devops1.py

## Specification

- 1. Launch EC2 instance. Firstly, your Python program should create and launch a new Amazon 
EC2 nano instance. You must use the Boto3 API library to launch from an Amazon Linux 2023 
AMI. Use an up-to-date AMI version. You will need to have your API credentials in a 
configuration file (~/.aws/credentials) and not in the code. There is no need to include 
any credentials or keys in your submission. 
- 2.  Configure appropriate instance settings (at launch). Ensure that your program launches the 
instance into an appropriate security group (you can optionally create one programmatically) 
and that the instance has a Name tag and is accessible using your SSH key. You do not need to 
create a security group or a key pair here (i.e. you can use ones that are already set up on your 
account.) You must launch this instance in Availability Zone us-east-b. 
- 3.  Set up EC2 website. You should provide a “User Data” script when creating the instance. This 
start-up script should apply any required patches to the operating system and then install the 
web server (e.g. Apache). The start-up User Data script should also configure the web server 
index page to display the following instance metadata: instance ID, private IP address, 
instance type, availability zone and some other content e.g. text or image. 
- 4.  Set up S3 website. Another core requirement is that you write Python 3 code to create an S3 
bucket. You should name your bucket using a combination of 6 random characters and your 
name; e.g. jbloggs-1a2b3c replacing jbloggs with your first initial and last name and replacing 
1a2b3c with random characters. This bucket needs to contain at least two items: 
o An image which we will make available at http://devops.setudemo.net/logo.jpg. Your 
Python program should download this image and then upload it to your newly-created 
bucket. The image at this URL will change from time to time, so your code will need to 
handle this in a generic manner. 
o A web page called index.html which displays the image - e.g. using <img> tag. 
Configure the S3 bucket for static website hosting so that the image can be accessed with a URL 
of the form http://bucket-name.s3-website-us-east-1.amazonaws.com (note that index and image 
file names are not in the URL, just the bucket name) 
- 5.  Write both URLs to a file.  Your Python program should write the two URLs to a file called 
jbloggs-websites.txt replacing jbloggs with your first initial and last name. 
- 6.  Monitoring.  We have provided a bash script called monitoring.sh that runs some sample terminal 
commands that carry out monitoring. You should enhance this script to monitor some additional 
items. Then, from your Python script, use scp (secure copy) to copy this script up to your newly-
created instance and then use SSH remote command execution to set the appropriate permissions 
and execute this script on the instance. You will need to use the public IP address or DNS name 
assigned to the instance to connect to it via SSH. 
- 7.  AMI creation.  After your webserver is installed and running successfully, you should create an 
AMI from this instance – you should name this AMI in the format XX-2026-02-14-164498 where 
XX is your initials and 2026-02-14-164498 is the current date and microseconds. 

## To run you will need to have

- your API credentials in a configuration file (~/.aws/credentials)
- .pem file in the project's root directory