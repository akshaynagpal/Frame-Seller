from django.db import models


class Product(models.Model):
    """
        Model for Products
    """
    price = models.FloatField()
    description = models.CharField(max_length=255)
    url = models.CharField(max_length=200)


class Order(models.Model):
    """
        Model for Orders
    """
    STATUS = (
        (0, 'Not Charged'),
        (1, 'Charged'),
        (2, 'Failed'),
    )

    userid = models.CharField(max_length=20)
    productid = models.ForeignKey(Product)
    orderdate = models.DateTimeField()
    token = models.CharField(max_length=30)
    paymentstatus = models.IntegerField(choices=STATUS)
