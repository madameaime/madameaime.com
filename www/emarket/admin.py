from django.contrib import admin

from models import *


admin.site.register(Sale)
admin.site.register(Order)

class OrderSaleAdmin(admin.ModelAdmin):

    # order info
    def get_orderid(self, ordersale):
        return ordersale.order.exposed_id

    def get_date(self, ordersale):
        return ordersale.order.date

    def get_promo_code(self, ordersale):
        return ordersale.order.promo_code

    # sale info
    def get_sale_price(self, ordersale):
        return ordersale.sale.price

    def get_product_name(self, ordersale):
        return ordersale.sale.product.name

    # billing info
    def get_billing_firstname(self, ordersale):
        return ordersale.order.billing.firstname 

    def get_billing_lastname(self, ordersale):
        return ordersale.order.billing.lastname

    def get_billing_email(self, ordersale):
        return ordersale.order.billing.email

    def get_billing_address(self, ordersale):
        return ordersale.order.billing.address

    def get_billing_additional(self, ordersale):
        return ordersale.order.billing.additional

    def get_billing_zip_code(self, ordersale):
        return ordersale.order.billing.zip_code

    def get_billing_city(self, ordersale):
        return ordersale.order.billing.city

    def get_billing_phone(self, ordersale):
        return ordersale.order.billing.phone

    def get_billing_country(self, ordersale):
        return ordersale.order.billing.country

    # delivery info
    def get_delivery_firstname(self, ordersale):
        if ordersale.delivery is not None:
            return ordersale.delivery.firstname 
        return ordersale.order.billing.firstname 

    def get_delivery_lastname(self, ordersale):
        if ordersale.delivery is not None:
            return ordersale.delivery.lastname
        return ordersale.order.billing.lastname

    def get_delivery_email(self, ordersale):
        if ordersale.delivery is not None:
            return ordersale.delivery.email
        return ordersale.order.billing.email

    def get_delivery_address(self, ordersale):
        if ordersale.delivery is not None:
            return ordersale.delivery.address
        return ordersale.order.billing.address

    def get_delivery_additional(self, ordersale):
        if ordersale.delivery is not None:
            return ordersale.delivery.additional
        return ordersale.order.billing.additional

    def get_delivery_zip_code(self, ordersale):
        if ordersale.delivery is not None:
            return ordersale.delivery.zip_code
        return ordersale.order.billing.zip_code

    def get_delivery_city(self, ordersale):
        if ordersale.delivery is not None:
            return ordersale.delivery.city
        return ordersale.order.billing.city

    def get_delivery_phone(self, ordersale):
        if ordersale.delivery is not None:
            return ordersale.delivery.phone
        return ordersale.order.billing.phone

    def get_delivery_country(self, ordersale):
        if ordersale.delivery is not None:
            return ordersale.delivery.country
        return ordersale.order.billing.country

    list_display = (
        # order info
        'get_orderid',
        'get_date',
        'get_promo_code',

        # sale info
        'get_sale_price',
        'get_product_name',

        # billing info
        'get_billing_firstname',
        'get_billing_lastname',
        'get_billing_email',
        'get_billing_email',
        'get_billing_address',
        'get_billing_additional',
        'get_billing_zip_code',
        'get_billing_city',
        'get_billing_phone',
        'get_billing_country',

        # delivery info
        'get_delivery_firstname',
        'get_delivery_lastname',
        'get_delivery_email',
        'get_delivery_email',
        'get_delivery_address',
        'get_delivery_additional',
        'get_delivery_zip_code',
        'get_delivery_city',
        'get_delivery_phone',
        'get_delivery_country',
    )

    class Meta:
        odering = ['order__date']


admin.site.register(OrderSale, OrderSaleAdmin)
admin.site.register(Address)
admin.site.register(Be2billTransaction)
admin.site.register(PartnersSubscription)
