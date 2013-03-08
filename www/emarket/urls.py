from django.conf.urls import patterns, include, url

from views import *


urlpatterns = patterns('',
    url(r'^emarket/sc/add/$',
        ShoppingCartAddView.as_view(),
        name='shopping-cart.add'
    ),

    url(r'^emarket/sc/remove/(?P<sale_id>\d+)$',
        ShoppingCartRemoveView.as_view(),
        name='shopping-cart.remove'),

    url(r'^vos-adresses-de-livraison/$',
        DeliveryView.as_view(),
        name='delivery'),

    # Confirm the client everything went fine
    url(r'^checkout-ok/$',
        CheckoutOKClient.as_view(),
        name='checkout_ok.client'),

    url(r'be2bill/notifications/transaction/',
        Be2billNotifTransaction.as_view(),
        name='be2bill.notifications.transaction'),
)
