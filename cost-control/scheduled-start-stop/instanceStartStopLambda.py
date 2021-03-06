"""
instanceStartStopLambda.py

This AWS Lambda enforces a schedule for starting and stopping instances for AWS cost savings.

Environment Settings:
    --

Source Control: https://github.com/Derek-Ashmore/AWSDevOpsUtilities

"""

import sys
import json
import os
import datetime
import boto3

testMode = False

def startStopHandler(event, context):
    try:
        executeStopStart(datetime.datetime.now()
                         , os.getenv('Scheduled_StartTime', '')
                         , os.getenv('Scheduled_StopTime', '')
                         , os.getenv('Scheduled_StartStop_Days', 'M,T,W,R,F'))
    except Exception as e:
        e.args += (event,vars(context))
        raise

    return 0;

def executeStopStart(currentDateTime, globalStartTimeSpec, globalEndTimeSpec, globalDaySpec):
    instances=findAllEc2Instances()

    # Global start
    if datetimeMatches(currentDateTime, globalStartTimeSpec, globalEndTimeSpec, globalDaySpec):
        for instance in instances:
            if 'Scheduled_StartTime' not in instance['tagDict'] and instance['state'] == 'stopped':
                print ('Starting instance id={} name={} state={}').format(
                    instance['instanceId'], instance['tagDict']['Name'], instance['state'])
                startEc2Instance(instance['instanceId'])
            else:
                print ('Instance not eligible for global start: id={} name={} state={}').format(
                    instance['instanceId'], instance['tagDict']['Name'], instance['state'])
    else:
        for instance in instances:
            if 'Scheduled_StopTime' not in instance['tagDict'] and instance['state'] == 'running':
                print ('Stopping instance id={} name={} state={}').format(
                    instance['instanceId'], instance['tagDict']['Name'], instance['state'])
                stopEc2Instance(instance['instanceId'])
            else:
                print ('Instance not eligible for global stop: id={} name={} state={}').format(
                    instance['instanceId'], instance['tagDict']['Name'], instance['state'])

    # Instance-level starts/stops
    for instance in instances:
        startStopDays = 'M,T,W,R,F'
        if 'Scheduled_StartTime' in instance['tagDict'] and instance['state'] == 'stopped':
            if 'Scheduled_StartStop_Days' in instance['tagDict']:
                startStopDays = instance['tagDict']['Scheduled_StartStop_Days']
            if datetimeMatches(currentDateTime, instance['tagDict']['Scheduled_StartTime'] , instance['tagDict']['Scheduled_StopTime'], startStopDays):
                print ('Starting instance id={} name={} state={}').format(
                    instance['instanceId'], instance['tagDict']['Name'], instance['state'])
                startEc2Instance(instance['instanceId'])
            else:
                print ('Instance not eligible for start: id={} name={} state={}').format(
                    instance['instanceId'], instance['tagDict']['Name'], instance['state'])

        if 'Scheduled_StopTime' in instance['tagDict'] and instance['state'] == 'running':
            if 'Scheduled_StartStop_Days' in instance['tagDict']:
                startStopDays = instance['tagDict']['Scheduled_StartStop_Days']
            if not datetimeMatches(currentDateTime, instance['tagDict']['Scheduled_StartTime'], instance['tagDict']['Scheduled_StopTime'] , startStopDays):
                print ('Stopping instance id={} name={} state={}').format(
                    instance['instanceId'], instance['tagDict']['Name'], instance['state'])
                stopEc2Instance(instance['instanceId'])
            else:
                print ('Instance not eligible for stop: id={} name={} state={}').format(
                    instance['instanceId'], instance['tagDict']['Name'], instance['state'])

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

def datetimeMatches(currentDateTime, startTimeSpec, endTimeSpec, daySpec):
    return matchesDaySpec(currentDateTime, daySpec) and isRunningTime(currentDateTime, startTimeSpec, endTimeSpec)

def matchesDaySpec(currentDateTime,daySpec):
    currentWeekDay = int2Weekday(currentDateTime.date().weekday())
    daySpecSplit = daySpec.replace(' ','').split(',')
    if currentWeekDay in daySpecSplit:
        return True
    return False

def getMinute(timeSpec):
    timeSpecSplit = timeSpec.replace(' ','').split(':')
    return int(timeSpecSplit[1])

def getHour(timeSpec):
    timeSpecSplit = timeSpec.replace(' ','').split(':')
    return int(timeSpecSplit[0])

def isRunningTime(currentDateTime, startTimeSpec, endTimeSpec):
    startHour = getHour(startTimeSpec)
    endHour = getHour(endTimeSpec)
    startMinute = getMinute(startTimeSpec)
    endMinute = getMinute(endTimeSpec)
    if currentDateTime.hour > startHour and currentDateTime.hour < endHour:
        return True
    if currentDateTime.hour == startHour and currentDateTime.minute >= startMinute:
        return True
    if currentDateTime.hour == endHour and currentDateTime.minute <= endMinute:
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
