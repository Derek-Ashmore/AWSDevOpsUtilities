"""
secretEncrypt.py

Will encrypt a secret using KMS and byte64 encode it.

Usage:  python secretEncrypt.py --r ec2 --s instances

Options:    --s         Secret to be encrypted.

"""

import sys
import os
import click
import boto3

@click.command()
@click.option("--s", help="Secret to be encrypted.")
@click.option("--k", help="Key Id.")
def execute(s, k):
    secretText = s
    keyId = k

    kmsClient = boto3.client('kms')
    stuff = kmsClient.encrypt(KeyId=keyId, Plaintext=secretText)
    binary_encrypted = stuff[u'CiphertextBlob']
    encrypted_password_base64 = base64.b64encode(binary_encrypted)

    print ("Base64 encrypted secret is: %s") % encrypted_password_base64

if __name__ == "__main__":
    execute()
