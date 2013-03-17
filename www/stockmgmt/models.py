from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=128)


class Product(models.Model):

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=64, blank=True)
    public_price = models.DecimalField(blank=True, null=True, default=None,
                                       max_digits=6, decimal_places=2)
    supplier = models.ForeignKey(Supplier, blank=True, null=True, default=None)


class Package(Product):
    products = models.ManyToManyField(Product, related_name="products")


class StockMvt(models.Model):

    def __unicode__(self):
        return self.reason

    date     = models.DateTimeField(auto_now_add=True)
    product  = models.ForeignKey(Product)
    quantity = models.IntegerField()
    reason   = models.CharField(max_length=255)
