"""
purchase order
"""
from __future__ import print_function
import json
from lib.async_promises import Promise
from orders import create_order
from payment import create_charge, Status

def buy_product(event, context):
    """
    Create order entry with unpaid status
    """
    data = create_order(event, Status.UNPAID)

    #if order accepted successfully
    #create payment asynchronously
    #return 202 accepted response to user
    if int(data['statusCode']) == 200:
        order_data = json.loads(data['body'])
        promise = Promise(lambda resolve, reject:
                          reject(Exception('Payment Failed')\
                            if create_charge(order_data) is None else \
                            resolve('Payment Processed')))

        #process payment asynchronously
        promise.then(lambda result: print(result)).\
        catch(lambda error: print(error))

    return data
