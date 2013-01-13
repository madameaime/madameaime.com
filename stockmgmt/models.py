from django.db import models


class Product(models.Model):

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=255)


class Package(Product):
    products = models.ManyToManyField(Product, related_name="products")


class StockMvt(models.Model):

    def __unicode__(self):
        return self.reason

    date     = models.DateTimeField(auto_now_add=True)
    product  = models.ForeignKey(Product)
    quantity = models.IntegerField()
    reason   = models.CharField(max_length=255)
