"""
instanceStartStopLambda.py

This AWS Lambda enforces a schedule for starting and stopping instances for AWS cost savings.

Environment Settings:
    --    

"""

import sys
import json
import os
import datetime
import boto3

testMode = False

def startStopHandler(event, context): 
    try:
        executeStopStart(datetime.now(os.getenv('Scheduled-TimeZone', 'UTC'))
                         , os.getenv('Scheduled-StartTime', '')
                         , os.getenv('Scheduled-StopTime', '')
                         , os.getenv('Scheduled-StartStop-Days', 'M,T,W,R,F'))
    except Exception as e:
        e.args += (event,vars(context))
        raise
        
    return 0;

def executeStopStart(currentDateTime, globalStartTimeSpec, globalEndTimeSpec, globalDaySpec):
    instances=findAllEc2Instances()
    
    # Global start
    if datetimeMatches(currentDateTime, globalStartTimeSpec, globalDaySpec):
        for instance in instances:
            if 'Scheduled-StartTime' not in instance['tagDict'] and instance['state'] == 'stopped':
                print ('Starting instance id={} name={} state={}').format(
                    instance['instanceId'], instance['tagDict']['Name'], instance['state'])
                startEc2Instance(instance['instanceId'])
                
    # Global stop
    if datetimeMatches(currentDateTime, globalStartTimeSpec, globalDaySpec):
        for instance in instances:
            if 'Scheduled-StopTime' not in instance['tagDict'] and instance['state'] == 'running':
                print ('Stopping instance id={} name={} state={}').format(
                    instance['instanceId'], instance['tagDict']['Name'], instance['state'])
                stopEc2Instance(instance['instanceId'])
                
    # Instance-level starts/stops
    for instance in instances:
        startStopDays = 'M,T,W,R,F'
        if 'Scheduled-StartTime' in instance['tagDict'] and instance['state'] == 'stopped':            
            if 'Scheduled-StartStop-Days' in instance['tagDict']:
                startStopDays = instance['tagDict']['Scheduled-StartStop-Days']
            if datetimeMatches(currentDateTime, instance['tagDict']['Scheduled-StartTime'] , startStopDays):              
                print ('Starting instance id={} name={} state={}').format(
                    instance['instanceId'], instance['tagDict']['Name'], instance['state'])
                startEc2Instance(instance['instanceId'])
                
        if 'Scheduled-StopTime' not in instance['tagDict'] and instance['state'] == 'running':
            if 'Scheduled-StartStop-Days' in instance['tagDict']:
                startStopDays = instance['tagDict']['Scheduled-StartStop-Days']
            if datetimeMatches(currentDateTime, instance['tagDict']['Scheduled-StopTime'] , startStopDays):              
                print ('Stopping instance id={} name={} state={}').format(
                    instance['instanceId'], instance['tagDict']['Name'], instance['state'])
                stopEc2Instance(instance['instanceId'])
    
def findAllEc2Instances():
    ec2Client = boto3.client('ec2')
    instanceList = ec2Client.describe_instances();
    
    instances=[]
    for item in instanceList['Reservations']:
        instance={}
        instance['instanceId'] = item['Instances'][0]['InstanceId']
        instance['tagDict'] = tags2dict(item['Instances'][0]['Tags'])
        instance['state'] = item['Instances'][0]['State']['Name']
        instances.append(instance)
        
    return instances

def startEc2Instance(instanceId):
    ec2Client = boto3.client('ec2')
    try:
        ec2Client.start_instances(
            InstanceIds=[instanceId],
            DryRun=testMode
            )
    except Exception as e:
        if testMode:
            print ('Instance {} would have started').format(instanceId)

def stopEc2Instance(instanceId):
    ec2Client = boto3.client('ec2')
    try:
        ec2Client.stop_instances(
            InstanceIds=[instanceId],
            DryRun=testMode
            )
    except Exception as e:
        if testMode:
            print ('Instance {} would have stopped').format(instanceId)
            
def tags2dict(tags):
    tagDict = {}
    for tag in tags:
        tagDict[tag['Key']] = tag['Value']
    return tagDict

def datetimeMatches(currentDateTime, timeSpec, daySpec):
    return matchesDaySpec(currentDateTime, daySpec) and matchesTimeSpec(currentDateTime, timeSpec)
  
def matchesTimeSpec(currentDateTime,timeSpec):
    timeSpecSplit = timeSpec.replace(' ','').split(':')
    if currentDateTime.hour == int(timeSpecSplit[0]) and currentDateTime.minute == int(timeSpecSplit[1]):
        return True
    return False
      
def matchesDaySpec(currentDateTime,daySpec):
    currentWeekDay = int2Weekday(currentDateTime.date().weekday())
    daySpecSplit = daySpec.replace(' ','').split(',')
    if currentWeekDay in daySpecSplit:
        return True
    return False

def setTestMode():
    global testMode
    testMode = True
    
def int2Weekday(weekdayInt):
    return weekdayIntStringDict[weekdayInt]

weekdayIntStringDict = {0 : 'M',
           1 : 'T',
           2 : 'W',
           3 : 'R',
           4 : 'F',
           5 : 'S',
           6 : 'U'
           }

