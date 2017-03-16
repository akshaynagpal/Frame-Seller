"""
Create JWT Token for valid user login
"""

from __future__ import print_function

import datetime
import re
import boto3
from error import error
from botocore.exceptions import ClientError

def validate_user(email, password):
    """
    Fetch only user infor from database
    """

    #Customer table
    customer_table = boto3.resource('dynamodb').Table('Customer')

    try:
        response = customer_table.get_item(
            Key={
                'email': email
            }
        )
    except ClientError as err:
        print(err)
        return error(500, 'Unable to fetch customer information')
    else:
        customer_info = None

        if 'Item' not in response:
            return error(404, 'Customer does not exist')

        _info = response['Item']['info']

        if not _info['verified']:
            return error(400, 'Customer not verified')

        if not _info['active']:
            return error(400, 'Customer de-activated')

        if _info['password'] == password:
            customer_info = {
                'firstname': _info['firstname'],
                'lastname': _info['lastname'],
                'email': response['Item']['email']
            }

        return customer_info


def login_customer(event):
    """
    Import boto3
    """
    if ('email' not in event) or\
        ('password' not in event):
        return error(401, 'Invalid credentials')

    customer_info = validate_user(event['email'], event['password'])

    if not customer_info:
        return error(401, 'Invalid credentials')

    return customer_info
