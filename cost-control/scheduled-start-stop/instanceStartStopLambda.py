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

def startStopHandler(event, context): 
    try:
        executeStopStart(event, context
                         , datetime.now(os.getenv('Scheduled-TimeZone', 'UTC'))
                         , os.getenv('Scheduled-StartTime', '')
                         , os.getenv('Scheduled-StopTime', '')
                         , os.getenv('Scheduled-StartStop-Days', 'M,T,W,R,F'))
    except Exception as e:
        e.args += (event,vars(context))
        raise
        
    return 0;

def executeStopStart(event, context, currentDateTime, globalStartTimeSpec, globalEndTimeSpec, globalDaySpec):
    print ("to do")
    
def globalStartItUp():
    print ("to do")
    
def globalShutitDown():
    print ("to do")
    
def findAllEc2Instances():
    ec2Client = boto3.client('ec2')
    instanceList = ec2Client.describe_instances();
    return instanceList['Reservations']
    
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