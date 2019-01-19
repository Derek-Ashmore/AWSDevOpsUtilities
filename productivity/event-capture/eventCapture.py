"""
eventCapture.py

This AWS Lambda will capture and report trigger event json. This is intended for lambda developers.

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

def eventCaptureHandler(event, context):
    try:
        print(event)
    except Exception as e:
        e.args += (event,vars(context))
        raise

    return event;
