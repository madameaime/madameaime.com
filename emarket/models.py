from datetime import datetime

from django.conf import settings
from django.contrib.sessions.models import Session
from django.db import models
from django.utils import timezone

import stockmgmt.models


class Sale(models.Model):

    def __unicode__(self):
        return self.product.name

    begin       = models.DateTimeField(null=True, default=None, blank=True)
    end         = models.DateTimeField(null=True, default=None, blank=True)
    product     = models.ForeignKey(stockmgmt.models.Product)
    price       = models.DecimalField(max_digits=5, decimal_places=2)

    shopping_cart_description = models.TextField(blank=True,
        help_text='text displayed in the shopping cart')


class Order(models.Model):

    def __unicode__(self):
        return self.exposed_id

    exposed_id = models.CharField(max_length=32)
    date       = models.DateTimeField(auto_now_add=True)
    user       = models.ForeignKey(settings.AUTH_USER_MODEL)
    billing    = models.ForeignKey('Address')
    promo_code = models.CharField(max_length=32, blank=True)


class OrderSale(models.Model):

    def __unicode__(self):
        return self.order.exposed_id

    order    = models.ForeignKey(Order)
    sale     = models.ForeignKey(Sale)
    delivery = models.ForeignKey('Address', null=True, blank=True)


class Address(models.Model):

    def __unicode__(self):
        return u'%s %s' % (self.firstname, self.lastname)

    firstname   = models.CharField(max_length=64)
    lastname    = models.CharField(max_length=64)
    email       = models.EmailField()
    address     = models.TextField()
    additional  = models.TextField(blank=True)
    zip_code    = models.CharField(max_length=16)
    city        = models.CharField(max_length=64)
    phone       = models.CharField(max_length=32, blank=True)
    country     = models.CharField(max_length=64)


class Be2billTransaction(models.Model):
    """ When a transaction is completed, be2bill requests a page and gives info
    about the transaction. Log it.
    """
    def __unicode__(self):
        return self.transactionid

    _3dsecure = models.CharField(max_length=3, blank=True)
    alias = models.CharField(max_length=32, blank=True)
    amount = models.IntegerField(blank=True, null=True)
    cardcode = models.CharField(max_length=16, blank=True)
    cardcountry = models.CharField(max_length=128, blank=True)
    cardfullname = models.CharField(max_length=255, blank=True)
    cardtype = models.CharField(max_length=64, blank=True)
    cardvaliditydate = models.CharField(max_length=10, blank=True)
    clientemail = models.CharField(max_length=255, blank=True)
    clientident = models.CharField(max_length=255, blank=True)
    currency = models.CharField(max_length=32, blank=True)
    descriptor = models.CharField(max_length=32, blank=True)
    execcode = models.IntegerField(blank=True, null=True)
    extradata = models.CharField(max_length=255, blank=True)
    identifier = models.CharField(max_length=32, blank=True)
    language = models.CharField(max_length=16, blank=True)
    message = models.CharField(max_length=510, blank=True)
    operationtype = models.CharField(max_length=64, blank=True)
    transactionid = models.CharField(max_length=32, blank=True)
    version = models.CharField(max_length=16, blank=True)

    # Store all parameters in a blob field in case a new field is added
    blob = models.TextField()


class PartnersSubscription(models.Model):
    """ When a user makes an order, he can choose to be contacted by partners
    or not.
    Whatever is his decision, store it.
    """
    def __unicode__(self):
        return self.order.user.email

    date = models.DateTimeField(default=timezone.now)
    order = models.ForeignKey(Order, primary_key=True)
    register = models.BooleanField()
