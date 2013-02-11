from datetime import datetime

from django.db import models

import emarket.models


class OfferPageSale(models.Model):
    """
    Product exposed on the offer page.
    """
    def __unicode__(self):
        return self.sale.product.name

    sale = models.ForeignKey(emarket.models.Sale)
    title = models.CharField(max_length=64, null=True, blank=True, default=None)
    subtitle = models.CharField(max_length=64, null=True, blank=True, default=None)
    content = models.TextField(null=True, blank=True, default=None)
    price_comment = models.CharField(max_length=64)


class OfferPage(models.Model):
    """
    Configuration of the three products shown on the offer page, displayed
    since date_start.
    """
    def __unicode__(self):
        return self.date_start.strftime('%Y/%m/%d %H:%M:%S')

    date_start = models.DateTimeField(default=datetime.now)

    sale_1 = models.ForeignKey(OfferPageSale, related_name='sale_1')
    sale_2 = models.ForeignKey(OfferPageSale, related_name='sale_2')
    sale_3 = models.ForeignKey(OfferPageSale, related_name='sale_3')

    hurry_text = models.TextField(null=True, blank=True, default=None)


class Newsletter(models.Model):
    date = models.DateTimeField(default=datetime.now)
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=True)
