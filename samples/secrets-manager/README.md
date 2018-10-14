# Using SecretsManager in lambda to obtain secret example

## Purpose
This lambda is a simple example of using SecretsManager to reduce exposure
for needed items like database passwords.

## Installation

* Create a role for the lambda containing the privileges in this [policy](awsPolicy.json).
* Create this lambda from the console.
    * Platform = Python 2.7
    * Copy/paste source code:  [secretLambda.py](secretLambda.py)
    * Handler method:  lambda_function.secretHandler

## Configuration
**This lambda requires environment variable settings.**

| Environment Variable Name | Value Required | Value Syntax |
| --- |:---:| ---:|
| Secret_Name | Y | Secret name to use. |

## Future Plans
* None
