from django.contrib import admin

from models import *


admin.site.register(Supplier)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'deliverable', 'product_type', 'article_family',
            'supplier', 'public_price', 'length', 'width', 'height', 'weight',
            'ean')
    list_filter = ('product_type', 'deliverable')

admin.site.register(Product, ProductAdmin)


class PackageAdmin(admin.ModelAdmin):

    def get_products(package):
        return ' | '.join([p.name for p in package.products.all()])

    list_display = ('name', get_products, 'product_type')

admin.site.register(Package, PackageAdmin)


class StockMvtAdmin(admin.ModelAdmin):
    list_display = ('date', 'product', 'quantity', 'reason')

admin.site.register(StockMvt, StockMvtAdmin)
