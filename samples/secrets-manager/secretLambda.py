"""
secretLambda.py

This lambda is a simple example of decrypting secrets using KMS to reduce exposure
for needed items like database passwords.

Environment Settings:
    --  Secret_Name         Secret name to use

Source Control: https://github.com/Derek-Ashmore/AWSDevOpsUtilities
"""

import sys
import json
import os
import boto3
import base64

def secretHandler(event, context):
    try:
        secretName = os.getenv('Secret_Name')
        if secretName == None:
            raise Exception('Secret_Name environment variable not set')

        print( showSecret(secretName) )
    except Exception as e:
        e.args += (event,vars(context), secretName)
        raise

    return 0;

def showSecret(secretName):
    secretsMgrClient = boto3.client('secretsmanager')
    get_secret_value_response = secretsMgrClient.get_secret_value(
        SecretId=secretName
    )
    return get_secret_value_response['SecretString']
