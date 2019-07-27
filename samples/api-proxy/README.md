# API Proxy lambda function example

## Purpose
This lambda is a simple example of a lambda REST API proxy. This sample was written
to aid development of Slack commands against other enterprise products.

## Installation

* Create a role for the lambda containing the privileges in this [policy](awsPolicy.json).
* Create this lambda from the console.
    * Platform = Python 2.7
    * Copy/paste source code:  [proxyHandler.py](proxyHandler.py)
    * Handler method:  lambda_function.proxyHandler

## Configuration
* None

## Future Plans
* None
