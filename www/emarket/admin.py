from django.contrib import admin

from models import *


class SaleAdmin(admin.ModelAdmin):
    list_display = ('begin', 'end', 'product', 'price',
                    'shopping_cart_description')

admin.site.register(Sale, SaleAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('exposed_id', 'date', 'user', 'billing', 'promo_code')
    ordering = ['-date']
    search_fields = ('exposed_id', 'date', 'user', 'billing', 'promo_code')
    list_filter = ('promo_code', 'date')

admin.site.register(Order, OrderAdmin)


class OrderSaleAdmin(admin.ModelAdmin):
    list_display = ('order', 'sale', 'delivery')
    ordering = ['-order__date']
    search_fields = ('order', 'sale', 'delivery')
    list_filter = ('sale',)

admin.site.register(OrderSale, OrderSaleAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'email', 'address', 'additional',
                    'zip_code', 'city', 'phone', 'country')
    search_fields = ('firstname', 'lastname', 'email', 'city')
    list_filter = ('country',)


admin.site.register(Address, AddressAdmin)


admin.site.register(Be2billTransaction)
admin.site.register(PartnersSubscription)
