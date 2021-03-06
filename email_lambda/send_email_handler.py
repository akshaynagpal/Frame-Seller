"""
send email activity for state machine
"""

from __future__ import print_function
import json
import boto3
import os
from botocore.exceptions import ClientError
import json
import urllib

EMAIL_ACTIVITY = \
    'arn:aws:states:us-east-1:908762746590:activity:sendEmailActivity'

def send_email_handler(event, context):
    # TODO implement
    print(event)
    
    client = boto3.client('stepfunctions')
    """
    poll sendEmailActivity for task
    Generally returns {"taskToken":""} after 60 seconds
    """
    response = client.get_activity_task(
        activityArn=EMAIL_ACTIVITY,
        workerName='sendemaillambdaworker')
    
    if response is None:
        return
    
    # task token is the token that would be be used to set
    # output of the corresponding state machine activity

    taskToken = response["taskToken"]
    input_json = json.loads(response["input"])
    
    if taskToken == "":
        return
    
    """
    send verification email
    """
    if 'jwt' not in input_json or 'verify_page' not in input_json or "email" not in input_json :
        print('400:Bad Request')
        return
    try:
        """
        Sending email using someone else AWS SES using credentials
        """
        aws_access_key_id = os.environ['LOCAL_AWS_ACCESS_KEY']
        aws_secret_access_key = os.environ['LOCAL_AWS_SECRET_KEY']
        email_client = boto3.client('ses', aws_access_key_id=aws_access_key_id,
                                    aws_secret_access_key=aws_secret_access_key
                                   )
        s3url = input_json['verify_page'].strip().strip('/')
        
        params = {
            "vToken" : input_json['jwt']['token'],
            "taskToken" : taskToken
        }
        
        """
        Encoding parameters using urlencode to escape special characters
        """
        succeed_verification_url = (s3url + '?' + urllib.urlencode(params))
                          
        # Send Email Code 
        response = email_client.send_email(
            Source='akshay2626@gmail.com',
            Destination={
                'ToAddresses': [
                    input_json['email'],
                ],
                'BccAddresses': [
                ],
                'CcAddresses': [
                ],
            },
            Message={
                'Subject': {
                    'Data': 'Frameseller Email Verification',
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': 'Use this url to verify:'+succeed_verification_url,
                        'Charset': 'UTF-8'
                    },
                    'Html': {
                        'Data': 'Use <a href="'+succeed_verification_url+'">this url</a> to verify.<br/><br/> Copy paste this url:'+succeed_verification_url,
                        'Charset': 'UTF-8'
                    }
                }
            },
            ReplyToAddresses=[
                'akshay2626@gmail.com',
            ],
        )
        print('Email inserted to send queue')
        return {
            'success': True,
            'message': 'Email inserted to send queue'
        }
    except ClientError as email_err:
        print('500:Error sending email')
