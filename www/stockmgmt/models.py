from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=128)


class ProductType(models.Model):
    shortcode = models.CharField(max_length=16, primary_key=True)
    description = models.CharField(max_length=64, blank=True)


class Product(models.Model):

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(ProductType, blank=True,
                                     null=True, default=None)
    # cosmetic, book, ...
    article_family = models.CharField(max_length=64, blank=True)
    supplier = models.ForeignKey(Supplier, blank=True, null=True, default=None)
    public_price = models.DecimalField(blank=True, null=True, default=None,
                                       max_digits=6, decimal_places=2)
    # dimensions info (milimeters)
    length = models.IntegerField(blank=True, null=True, default=None)
    width = models.IntegerField(blank=True, null=True, default=None)
    height = models.IntegerField(blank=True, null=True, default=None)
    # grams
    weight = models.IntegerField(blank=True, null=True, default=None)
    # EAN (ISBN, EAN, GENCOD)
    models.CharField(max_length=64, blank=True)


class Package(Product):
    products = models.ManyToManyField(Product, related_name="products")


class StockMvt(models.Model):

    def __unicode__(self):
        return self.reason

    date     = models.DateTimeField(auto_now_add=True)
    product  = models.ForeignKey(Product)
    quantity = models.IntegerField()
    reason   = models.CharField(max_length=255)
