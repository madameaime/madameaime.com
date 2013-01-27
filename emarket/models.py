from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import models

import stockmgmt.models


class Sale(models.Model):

    def __unicode__(self):
        return self.product.name

    begin       = models.DateTimeField(null=True, default=None, blank=True)
    end         = models.DateTimeField(null=True, default=None, blank=True)
    product     = models.ForeignKey(stockmgmt.models.Product)
    price       = models.DecimalField(max_digits=5, decimal_places=2)

    shopping_cart_description = models.TextField(null=True,
        default=None, blank=True,
        help_text='text displayed in the shopping cart')

class Order(models.Model):

    def __unicode__(self):
        return self.exposed_id

    exposed_id = models.CharField(max_length=32)
    date       = models.DateTimeField(auto_now_add=True)
    user       = models.ForeignKey(User)
    billing    = models.ForeignKey('Address')


class OrderSale(models.Model):

    def __unicode__(self):
        return self.order.exposed_id

    order    = models.ForeignKey(Order)
    sale     = models.ForeignKey(Sale)
    delivery = models.ForeignKey('Address', null=True, default=None, blank=True)


class Address(models.Model):

    def __unicode__(self):
        return u'%s %s' % (self.firstname, self.lastname)

    firstname   = models.CharField(max_length=64)
    lastname    = models.CharField(max_length=64)
    email       = models.EmailField()
    address     = models.TextField()
    additionnal = models.TextField(null=True, default=None, blank=True)
    zip_code    = models.CharField(max_length=16)
    city        = models.CharField(max_length=64)
    phone       = models.CharField(max_length=32, null=True, default=None, blank=True)
    country     = models.CharField(max_length=64)


class ShoppingCartLog(models.Model):
    sale    = models.ForeignKey(Sale)
    #FIXME: untimeWarning: DateTimeField received a naive datetime (2013-01-13
    #       22:58:34.205319) while time zone support is active.
    date    = models.DateTimeField(default=datetime.now)
    session = models.ForeignKey(Session, null=True, default=None, blank=True)

    def save(self, *args, **kwargs):
        """A log entry can only be inserted if the product sold is still
        available.

        The lifetime of a shopping cart entry is 30 minutes, after which it is
        considered as deleted. 

        To know if the product is still available:
        - get from stockmgmt.StockMvt the number of available items ;
        - substract to this number the count of ShoppingCartLog entries
          refering to the product ;
        - if the result is greater or equal than 1, it can be added to the
          shopping cart.
        """
        super(ShoppingCartLog, self).save(*args, **kwargs)
