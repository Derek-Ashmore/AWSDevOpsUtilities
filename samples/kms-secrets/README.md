# Using KMS in lambda to decrypt secrets example

## Purpose
This lambda is a simple example of decrypting secrets using KMS to reduce exposure
for needed items like database passwords.

## Installation

* Create a role for the lambda containing the privileges in this [policy](awsPolicy.json).
* Create this lambda from the console.
    * Platform = Python 2.7
    * Copy/paste source code:  [kmsLambda.py](kmsLambda.py)
    * Handler method:  lambda_function.secretHandler
* You can encrypt and base64 encode a secret using script [secretEncrypt.py](secretEncrypt.py)

## Configuration
**This lambda requires environment variable settings.**

| Environment Variable Name | Value Required | Value Syntax |
| --- |:---:| ---:|
| Key_Id | Y | Id of KMS key to used. |
| Secret_Encrypted | Y | Secret text encrypted and encoded in base 64. |

## Future Plans
* None
