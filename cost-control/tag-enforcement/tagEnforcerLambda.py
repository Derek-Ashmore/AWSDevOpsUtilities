"""
tagEnforcer.py

This AWS Lambda enforces a schedule for enforcing items have required tags for AWS cost allocation.

Environment Settings:
    --    

"""

import sys
import json
import os
import boto3

violationList=[]

def tagEnforcementHandler(event, context): 
    try:
        tagEnforcement(os.getenv('Required_Tags', '').split(',')
                         , os.getenv('Tag_Notification_SNS_ARN', ''))
    except Exception as e:
        e.args += (event,vars(context))
        raise
        
    return 0;

def tagEnforcement(tags, snsArn):
    checkEC2Instances(tags)
    checkRDSInstances(tags)
    checkLoadBalancers(tags)
    checkAlbLoadBalancers(tags)
    # Add additional items to check here and return additional code as enhancement -:)
    
    for violation in violationList:
        print (violation)
        
    sendSnsNotification(snsArn)
  
def sendSnsNotification(snsArn):  
    snsClient = boto3.client('sns')
    
    myMessage = ''
    for violation in violationList:
        myMessage += 'missingTag={}, type={}, name={}, id={} \n '.format(
            violation['missingTag'], violation['itemType'], violation['itemName'], violation['itemId'])

    snsClient.publish(TargetArn=snsArn
                      , Subject='Tag Violation List'
                      , Message=myMessage)
    
def checkEC2Instances(tags):
    ec2Client = boto3.client('ec2')
    instanceList = ec2Client.describe_instances();
    
    for instance in instanceList['Reservations']:
        tagDict = tags2dict(instance['Instances'][0]['Tags'])
        checkTags(tagDict, tags, 'instance', safeDictReturn(tagDict, 'Name', 'n/a'), instance['Instances'][0]['InstanceId'])
        
def checkRDSInstances(tags):
    rdsClient = boto3.client('rds')
    instanceList = rdsClient.describe_db_instances()
    
    for instance in instanceList['DBInstances']:
        arn = instance['DBInstanceArn']
        tagList = rdsClient.list_tags_for_resource(ResourceName=arn)
        tagDict = tags2dict(tagList['TagList'])
        checkTags(tagDict, tags, 'RDS instance', safeDictReturn(tagDict, 'Name', 'n/a'), instance['DBInstanceIdentifier'])
        
def checkLoadBalancers(tags):
    elbClient = boto3.client('elb')
    elbList = elbClient.describe_load_balancers()
    
    for balancer in elbList['LoadBalancerDescriptions']:
        tagList = elbClient.describe_tags(LoadBalancerNames=[balancer['LoadBalancerName']])
        tagDict = tags2dict(tagList['TagDescriptions'][0]['Tags'])
        checkTags(tagDict, tags, 'Classic Load balancer', safeDictReturn(tagDict, 'Name', 'n/a'), balancer['LoadBalancerName'])

def checkAlbLoadBalancers(tags):
    elbClient = boto3.client('elbv2')
    elbList = elbClient.describe_load_balancers()
    
    for balancer in elbList['LoadBalancers']:
        print (balancer)
        tagList = elbClient.describe_tags(ResourceArns=[balancer['LoadBalancerArn']])
        tagDict = tags2dict(tagList['TagDescriptions'][0]['Tags'])
        checkTags(tagDict, tags, 'ALB Load balancer', safeDictReturn(tagDict, 'Name', 'n/a'), balancer['LoadBalancerName'])
        
def checkTags(tagDict, tags, itemType, itemName, itemId):
    for ttag in tags:
            if ttag not in tagDict:
                violation={}
                violation['itemType'] = itemType
                violation['itemName'] = itemName
                violation['itemId'] = itemId
                violation['missingTag'] = ttag
                violationList.append(violation)

def safeDictReturn(dict, key, default):
    if key in dict:
        return dict[key]
    return default
        
def tags2dict(tags):
    tagDict = {}
    for tag in tags:
        tagDict[tag['Key']] = tag['Value']
    return tagDict