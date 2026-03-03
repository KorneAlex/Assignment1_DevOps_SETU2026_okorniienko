#!/usr/bin/env python3

# This file was a part of the assignment example. 
# It was modified to fit the script design and should not to be counted as an additional feature
# Added and tested for curiosity

import boto3
import time
import sys
from datetime import datetime, timezone, timedelta
from helpers import bcolors

OK=f"{bcolors.OKGREEN}OK{bcolors.ENDC}"
ERR=f"{bcolors.FAIL}ERR{bcolors.ENDC}"

cloudwatch = boto3.resource('cloudwatch')
ec2 = boto3.resource('ec2')

def monitoring(instid):
    # instid = input("Please enter instance ID: ")    # Prompt the user to enter an Instance ID
    instance = ec2.Instance(instid)
    instance.monitor()  # Enables detailed monitoring on instance (1-minute intervals)
    print("")
    timer = 0
    counter=60
    while(counter != 0):
        sys.stdout.write(f"\r╭ {bcolors.HEADER}Testing monitoring tool for 60 sec. %i sec left...{bcolors.ENDC}" % counter)
        sys.stdout.flush()
        counter-=1
        time.sleep(1)
    print("")
    metric_iterator = cloudwatch.metrics.filter(Namespace='AWS/EC2',
                                                MetricName='CPUUtilization',
                                                Dimensions=[{'Name':'InstanceId', 'Value': instid}])


    metric = list(metric_iterator)[0]  # extract first (only) element

    try:
        response = metric.get_statistics(StartTime = datetime.now(timezone.utc) - timedelta(minutes=5),   # 5 minutes ago
                                        EndTime=datetime.now(timezone.utc),                              # now
                                        Period=30,                                                      # 5 min intervals
                                        Statistics=['Average'])

        cpu=round(response['Datapoints'][0]['Average'], 2)
        units=response['Datapoints'][0]['Unit']
        print (f"└── [ {OK} ] Average CPU utilisation:", cpu, units)
    except Exception as error:
        print (f"└── [ {ERR} ] Something went wrong: {error}")
        

if __name__ == "__main__":
    monitoring("i-0f355c6d0369569e5")