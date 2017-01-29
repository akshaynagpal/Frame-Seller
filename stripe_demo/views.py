"""
@authors: Siddharth Shah, Kunal Baweja

Stripe Demo Business Logic
"""

import os
import json
from stripe_demo.models import Product
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET, require_POST
import stripe

def load_key(keyfile):
    """
    A more secure way to load API keys is to set them in
    os environement variable and read that using os.environ

    Load authentication key from json formatted keyfile

    Expected keyfile content:
    { "stripe_api_key": "YOUR_STRIPE_API_KEY" }
    """
    try:
        if not (os.path.exists(keyfile) or os.path.isfile(keyfile)):
            raise OSError('file does not exist')

        with open(keyfile, 'r') as handle:
            keydata = json.load(handle)
            keydata = keydata['stripe_api_key']

    except:
        keydata = None

    return keydata

#set api key for stripe requests
stripe.api_key = load_key("key.json")

@require_GET
def get_products(request):
    """
    function to get all products and send them as json
    @param request:
    :return:
    """

    #TODO: Check for JWT from request

    products = Product.objects.values()
    product_list = [p for p in products]  # ValuesQuerySet to Python list
    return JsonResponse(product_list, safe=False)
