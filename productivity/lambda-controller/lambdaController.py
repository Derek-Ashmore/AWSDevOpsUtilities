"""
lambdaController.py

This AWS Lambda reads a DynamoDB table for configuration information to execute other AWS Lambdas.
This allows you to break up work into chunks small enough to execute in the 5 minute limit.
This is typically used for DevOps Lambdas that to work in remote accounts.

Environment Settings:
    --  Target_Lambda_Function
    --  DynamoDB_Table

Required Argument fields:
    --  None

Git Repo source:    https://github.com/Derek-Ashmore/AWSDevOpsUtilities/blob/master/productivity/lambda-controller/lambdaController.py
"""

import sys
import json
import os
import boto3

def lambdaController(event, context):
    try:
        lambdaFunction = os.getenv('Target_Lambda_Function')
        dynamoDbTable = os.getenv('DynamoDB_Table')
        if lambdaFunction == None:
            raise Exception('Target_Lambda_Function environment variable not set')
        if dynamoDbTable == None:
            raise Exception('DynamoDB_Table environment variable not set')
        localLambdaController(lambdaFunction, dynamoDbTable)

    except Exception as e:
        e.args += (event,vars(context))
        raise

    return 0;

def localLambdaController(lambdaFunction, dynamoDbTable):
    dynamoDbClient = boto3.client('dynamodb')
    dynamopaginator = dynamoDbClient.get_paginator('scan')
    dynamoresponse = dynamopaginator.paginate(
        TableName=dynamoDbTable,
        Select='ALL_ATTRIBUTES',
        ReturnConsumedCapacity='NONE',
        ConsistentRead=True
    )
    for page in dynamoresponse:
        for item in page['Items']:
            execute_lambda(lambdaFunction, flattenArguments(item))

def flattenArguments(dynamoDbRow):
    flattenedRow = {}

    # DynamoDb returns values as dicts; these need to be reformatted for lambda
    for key in dynamoDbRow.keys():
        values = dynamoDbRow[key]
        if isinstance(values, dict):
            keyValue = values.values()[0]
        if type(values) in [list,tuple]:
            keyValue = values[0]
        if isinstance(values, basestring):
            keyValue = values
        flattenedRow[key]=keyValue
    return json.dumps(flattenedRow)

def execute_lambda(lambdaFunction, payload):
    lambdaClient = boto3.client('lambda')
    lambdaClient.invoke(
        FunctionName=lambdaFunction,
        InvocationType='Event',
        Payload=payload
    )
