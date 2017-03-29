"""
Payment processing
"""
import os
import stripe
from order import update

stripe.api_key = os.environ['STRIPE_API_KEY']

class Status:
    """
    Describe payment status
    """
    UNPAID = 0
    PAID = 1
    FAILED = 2

def create_charge(charge_request):
    """
    create charge
    """
    charge = None
    try:

        order_data = charge_request

        metadata = {'link': order_data['orderurl']['href']}

        stripe_token = order_data['stripe_token']

        price = int(order_data['price']) * 100

        charge = stripe.Charge.create(
            amount=price,
            currency="usd",
            metadata=metadata,
            source=stripe_token)

        if charge['paid'] is True:
            #set order status as paid
            order_data['paymentstatus'] = Status.PAID
        else:
            #set order status as failed payment
            order_data['paymentstatus'] = Status.FAILED

    except stripe.error.InvalidRequestError as error:
        print(error)
        order_data['paymentstatus'] = Status.FAILED
    except stripe.error.APIConnectionError as error:
        print(error)
        order_data['paymentstatus'] = Status.FAILED
    except stripe.error.AuthenticationError as error:
        print(error)
        order_data['paymentstatus'] = Status.FAILED
    except stripe.error.RateLimitError as error:
        print(error)
        order_data['paymentstatus'] = Status.FAILED
    except Exception as error:
        print(error)
        order_data['paymentstatus'] = Status.FAILED

    return order_data
