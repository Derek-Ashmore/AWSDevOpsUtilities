"""
kmsLambda.py

This lambda is a simple example of decrypting secrets using KMS to reduce exposure
for needed items like database passwords.

Environment Settings:
    --  Key_Id              Id of KMS key to used
    --  Secret_Encrypted    Secret text encrypted and encoded in base 64

Source Control: https://github.com/Derek-Ashmore/AWSDevOpsUtilities
"""

import sys
import json
import os
import boto3
import base64

def secretHandler(event, context):
    try:
        keyId = os.getenv('Key_Id')
        secretEncrypted = os.getenv('Secret_Encrypted')
        if keyId == None:
            raise Exception('Key_Id environment variable not set')
        if secretEncrypted == None:
            raise Exception('Secret_Encrypted environment variable not set')

        print( decryptSecret(keyId, secretEncrypted) )
    except Exception as e:
        e.args += (event,vars(context), keyId, secretEncrypted)
        raise

    return 0;

def decryptSecret(keyId, secretEncrypted):
    binary_secret = base64.b64decode(secretEncrypted)

    kmsClient = boto3.client('kms')
    meta = kmsClient.decrypt(CiphertextBlob=binary_secret)
    plaintext = meta[u'Plaintext']
    return plaintext.decode()
