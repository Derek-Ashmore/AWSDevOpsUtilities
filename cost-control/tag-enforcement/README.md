# Automated Tag Notifications

## Purpose
This lambda notifies an SNS arn for items that don't have required tag names. This helps enforce that 
tags used for cost allocation are properly set.

## Installation

* Create a role for the lambda containing the privileges in this [policy](awsPolicy.json). 
* Create this lambda from the console.
    * Platform = Python 2.7
    * Copy/paste source code:  [tagEnforcer.py](tagEnforcer.py)
    * Handler method:  lambda_function.tagEnforcementHandler
* If you plan to use a global schedule (recommended), set environment variables listed in the configuration section
* Schedule the lambda using a cron expression (e.g. every day, week, etc.)

## Configuration
**Tags must be present with non-blank values.** 

| Environment Variable Name | Value Required | Value Syntax |
| --- |:---:| ---:|
| Required_Tags | Y | Comma delimited list of tags. |
| Tag_Notification_SNS_ARN | Y | Arn which to notify enforcement violations |

## Future Plans
* Add ability to check for allowed values per tag.
* Add ability for a notification even if no violations are found.

