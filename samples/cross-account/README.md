# Cross-account lambda function example

## Purpose
This lambda is a simple example of centrally installing a lambda and executing it
across multiple accounts in the enterprise.

## Installation

* Create a role for the lambda containing the privileges in this [policy](awsPolicy.json).
* Create this lambda from the console.
    * Platform = Python 2.7
    * Copy/paste source code:  [crossAccountHandler.py](crossAccountHandler.py)
    * Handler method:  lambda_function.crossAccountHandler

## Configuration
* None

## Future Plans
* None
