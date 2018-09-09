# Lambda execution controller

## Purpose
This AWS Lambda reads a DynamoDB table for configuration information to execute other AWS Lambdas.
This allows you to break up work into chunks small enough to execute in the 5 minute limit.
This is typically used for DevOps Lambdas that to work in remote accounts.

## Installation

* Create a role for the lambda containing the privileges in this [policy](awsPolicy.json).
* Create this lambda from the console.
    * Platform = Python 2.7
    * Copy/paste source code:  [lambdaController.py](lambdaController.py)
    * Handler method:  lambda_function.crossAccountHandler
* Schedule the lambda using a cron expression (e.g. every day, week, etc.)
* Environment variable requirements given by [lambdaController.py](lambdaController.py)

## Configuration
* Requires a DynamoDB table that contains needed arguments/payload for the target lambda

## Future Plans
* None
