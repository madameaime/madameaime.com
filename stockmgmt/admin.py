from django.contrib import admin

from models import *


admin.site.register(Product)
admin.site.register(Package)
admin.site.register(ProductPackage)
admin.site.register(StockMvt)
