"""
crossAccount.py

This AWS Lambda illustrates how one Lambda installation can service accounts across the organization.

Required Argument fields:
    --  Assumed_Role - ARN of role to assume

Environment Settings:
    --  None

"""

import sys
import json
import os
import boto3

def crossAccountHandler(event, context):
    try:
        if 'Assumed_Role' in event:
            listRolesInDifferentAccount(event['Assumed_Role'])
        else:
            raise Exception('Assumed_Role not provided as argument')
    except Exception as e:
        e.args += (event,vars(context))
        raise

    return 0;

def listRolesInDifferentAccount(assumedRole):
    stsClient = boto3.client('sts')
    response = stsClient.assume_role(RoleArn=assumedRole, RoleSessionName='mySession')

    # Fields are AccessKeyId, SecretAccessKey, SessionToken
    tempCredentials = response['Credentials']

    crossAccountSession = boto3.session.Session(
        aws_access_key_id=tempCredentials['AccessKeyId']
        , aws_secret_access_key=tempCredentials['SecretAccessKey']
        , aws_session_token=tempCredentials['SessionToken'])
    iamClient = crossAccountSession.client('iam')

    response = iamClient.list_roles()
    print('Role names:')
    for role in response['Roles']:
        print(role['RoleName'])
