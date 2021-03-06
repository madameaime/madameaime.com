from datetime import datetime
from decimal import Decimal
import csv
import random
import string

from django.conf import settings
from django.db import IntegrityError
from django.db import models
from django.db.models import Q
from django.utils import timezone

import stockmgmt.models

from .managers import ValidPartnersSubscriptionManager


class TransportType(models.Model):
    """ Specify the type of transport to use to deliver the product to the
    client.
    """
    def __unicode__(self):
        return self.as_string

    ads_field = models.CharField(max_length=16)
    as_string = models.CharField(max_length=64)


class Sale(models.Model):

    def __unicode__(self):
        return '[sale %d] %s' % (self.pk, self.product.name)

    begin          = models.DateTimeField(null=True, default=None, blank=True)
    end            = models.DateTimeField(null=True, default=None, blank=True)
    product        = models.ForeignKey(stockmgmt.models.Product)
    transport_type = models.ForeignKey(TransportType, null=True, blank=True)
    price          = models.DecimalField(max_digits=5, decimal_places=2)

    shopping_cart_description = models.TextField(blank=True,
        help_text='text displayed in the shopping cart (HTML)')


class PromoCode(models.Model):
    """ A promotion code gives a reduction for a given sale (if specified, else
    every sale) and has an expiration date.
    """
    def __unicode__(self):
        return self.code

    code = models.CharField(max_length=64, unique=True)
    sale = models.ForeignKey(Sale, blank=True, null=True)
    expire = models.DateTimeField(blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)


class Order(models.Model):

    def __unicode__(self):
        return self.exposed_id

    exposed_id = models.CharField(max_length=32, unique=True)
    date       = models.DateTimeField(auto_now_add=True)
    user       = models.ForeignKey(settings.AUTH_USER_MODEL)
    billing    = models.ForeignKey('Address')
    promo_code = models.ForeignKey(PromoCode, null=True, blank=True)
    is_free    = models.BooleanField(default=False)

    @staticmethod
    def generate_readable_id():
        """ Generate a human readable order identifier stored in
        Order.exposed_id.
        """
        return ''.join(random.choice(string.ascii_uppercase + string.digits)
                       for x in range(8))

    @staticmethod
    def helper_create_order(user, billing, **kwargs):
        """ Helper to create an Order instance. the exposed_id is generated
        randomly using generate_readable_id. Try forever until there's no id
        conflict.
        The instance created is returned.
        """
        while True:
            try:
                exposed_id = Order.generate_readable_id()
                order = Order(exposed_id=exposed_id, user=user,
                              billing=billing, **kwargs)
                order.save()
                return order
            except IntegrityError:
                pass

    def is_paid(self):
        """ 
        Return True if free or if a valid paid transaction corresponds to
        this order.
        """
        if self.is_free:
            return True
        try:
            last_trans = Be2billTransaction.objects.filter(order=self) \
                            .filter(Q(order__be2billtransaction__execcode=0) |
                                    Q(order__be2billtransaction__execcode=1))\
                            .order_by('-date_insert', '-pk').distinct()[0]
            if last_trans.operationtype == 'payment':
                return True
        except IndexError:
            pass
        return False

    def get_total_price(self):
        """ Return a dict that contains price info for this Order """
        order_price = Decimal(sum(osale.sale.price
                                    for osale in self.ordersale_set.all()))
        promo_code = (self.promo_code.discount
                        if self.promo_code else Decimal('0'))
        total_ttc = order_price - promo_code
        total_ht = total_ttc / Decimal('1.196')
        # cheat with affiliation: remove 5 euros from the transaction
        total_ht_cheated = total_ht - 5
        total_tva = total_ht * Decimal('0.196')
        return {
            'order_price': order_price.quantize(Decimal('0.01')),
            'total_ht': total_ht.quantize(Decimal('0.01')),
            'total_ht_cheated': total_ht_cheated.quantize(Decimal('0.01')),
            'total_tva': total_tva.quantize(Decimal('0.01')),
            'total_ttc': total_ttc.quantize(Decimal('0.01')),
            'promo_code': promo_code.quantize(Decimal('0.01')),
        }


class OrderSale(models.Model):

    def __unicode__(self):
        return self.order.exposed_id

    order     = models.ForeignKey(Order)
    sale      = models.ForeignKey(Sale)
    delivery  = models.ForeignKey('Address', null=True, blank=True)
    message   = models.TextField(blank=True)

    def get_delivery_identifier(self, product=None):
        """ Return the delivery number for this osale.
        For instance, imagine:
        - Order, id=150
        - OrderSale, id=400
        - The related Sale corresponds to a pack of three boxes
        There gonna be three delivery identifiers for the order n. 150:
        - BL400-1, BL400-2 and BL400-3 (in the case products ids are 1, 2 and
          3).

        If product is None, the part that specifies the product id is replaced
        with a star.
        """
        return 'BL%s-%s' % (self.pk, product.pk if product else '*')


class DeliveryTracking(models.Model):
    """ Store tracking information sent from ADS. """
    def __unicode__(self):
        return 'ordersale ' + self.order_sale

    order_sale = models.ForeignKey(OrderSale, unique=True,
                                   related_name='delivery_tracking')
    status = models.CharField(max_length=8)
    transport_type = models.CharField(max_length=32)
    tracking_number = models.CharField(max_length=32)
    sent_date = models.DateField()

    @staticmethod
    def create_entries_from_file(filename):
        for line in csv.reader(open(filename), delimiter=';'):
            order_sale = OrderSale.objects.get(pk=int(line[0]))
            try:
                inst = DeliveryTracking.objects.get(order_sale=order_sale)
            except DeliveryTracking.DoesNotExist:
                inst = DeliveryTracking(order_sale=order_sale)
            inst.status = line[1]
            inst.transport_type = line[2]
            inst.tracking_number = line[3]
            inst.sent_date = datetime.strptime(line[4], '%Y%m%d')
            inst.save()


class DeliveredProduct(models.Model):
    """ Keep track of Products given to ADS.

    A `delivered` flag used to exist in OrderSale but this wasn't working with
    metapackages.

    In the case the OrderSale references a metapackage, for instance three
    boxes, we want to be able to know which box has been delivered or not, and
    not if the whole package (which is a pure commercial product) has been
    delivered.
    """
    order_sale = models.ForeignKey(OrderSale)
    product = models.ForeignKey(stockmgmt.models.Product)


class Address(models.Model):

    def __unicode__(self):
        return u'%s %s' % (self.firstname, self.lastname)

    firstname   = models.CharField(max_length=64)
    lastname    = models.CharField(max_length=64)
    email       = models.EmailField(blank=True)
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

    order = models.ForeignKey(Order)
    date_insert = models.DateTimeField(auto_now_add=True)

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
    blob = models.TextField(blank=True)


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

    objects = models.Manager()
    valid_subscriptions = ValidPartnersSubscriptionManager()
