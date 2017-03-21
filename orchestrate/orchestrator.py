"""
Lamdba Orchestrator
"""

from __future__ import print_function
import json
import orders
import purchase
from respond import respond, error

def handler(event, context):
    """
    delegate work
    """
    print(event)
    if event['resource'].startswith('/orders'):
        try:
            response = orders.order(event)
            data = json.loads(response["Payload"].read())
            body = json.loads(data['body'])
            return respond(data['statusCode'], body)
        except (KeyError, Exception) as err:
            #in case of unhandled exception
            print(err)
            return error(500, 'Error processing order request')

    elif event['resource'].startswith('/purchase'):
        status = None
        data = purchase.buy_product(event)
        body = json.loads(data['body'])

        if int(data['statusCode']) == 200:
            status = 202
        else:
            status = data['statusCode']
        return respond(status, body)

    else:
        return error(500, "Unknown operation")
