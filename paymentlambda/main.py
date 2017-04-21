"""
handle payment processing
"""
import json
import boto3
from payment import create_charge
from notify import publish, Topic
from subscribe import Queue

def handler(event, context):
    """
    payment handler invoked by Cloudwatch event
    PaymentSchedule
    """
    client = boto3.client('sqs')

    response = client.receive_message(
        QueueUrl=Queue.PAYMENT_URL,
        AttributeNames=['All'],
        WaitTimeSeconds=Queue.WAIT_TIME_S,
        MaxNumberOfMessages=Queue.MAX_MESSAGES)

    # ignore if no messages returned by queue
    if 'Messages' not in response:
        return

    # process messages
    messages = response['Messages']
    processed_messages = list()

    for message in messages:
        payload = json.loads(message['Body']) #sqs message body
        payment_request = json.loads(payload['Message']) #sns embedded message

        try:
            charge_result = create_charge(payment_request)
            publish(charge_result, Topic.PAYMENT)
            _processed = {
                'Id': message['MessageId'],
                'ReceiptHandle': message['ReceiptHandle']
            }
            processed_messages.append(_processed)

        except Exception as err:
            # this message will be retried upto 3 times and then
            # inserted
            print(err)


    #batch delete successfully processed requests from queue
    del_response = client.delete_message_batch(
        QueueUrl=Queue.PAYMENT_URL,
        Entries=processed_messages)


    #process SNS invoke
    #ignore non sns invokes
    # if 'Records' in event:
    #     sns = event['Records'][0]['Sns']
    #     topic_arn = sns['TopicArn']

    #     #new order arrives, create payment else ignore
    #     if Subscription[topic_arn] == 'order':
    #         payload = json.loads(sns['Message'])
    #         charge_result = create_charge(payload)
    #         publish(charge_result, Topic.PAYMENT)
