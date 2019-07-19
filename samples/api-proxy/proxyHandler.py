"""
proxyHandler.py

This AWS Lambda illustrates a lambda REST API proxy. This sample was written
to aid development of Slack commands against other enterprise products.

Environment Settings:
    --  Target_Server_Url - Required. Target server for which call will be forwarded
    --  Header_List - Optional. Comma delimited list of headers that will be included.
    --  Operation_Type - Optional. Default POST. POST, GET are allowed values.

Required Argument fields:
    --  Rest_Resource - Rest resource to be included in call

Source Control: https://github.com/Derek-Ashmore/AWSDevOpsUtilities
"""

import sys
import json
import os

def proxyHandler(event, context):
    try:
        target_url = os.getenv('Target_Server_Url', None)
        header_array = os.getenv('Header_List', '').split(',')
        operation_type = os.getenv('Operation_Type', 'POST')
        if target_url == None:
            raise Exception('Target_Server_Url not provided as argument')
        return forwardWebCall(target_url, header_array, operation_type)

    except Exception as e:
        e.args += (event,vars(context))
        raise

    return 0;

def forwardWebCall(target_url, header_array, operation_type)
