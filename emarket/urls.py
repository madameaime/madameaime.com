from django.conf.urls import patterns, include, url

from views import DeliveryView, ShoppingCartAddView, ShoppingCartRemoveView


urlpatterns = patterns('',
    url(r'^sc/add/$',
        ShoppingCartAddView.as_view(),
        name='shopping-cart.add'
    ),

    url(r'^sc/remove/(?P<sale_id>\d+)$',
        ShoppingCartRemoveView.as_view(),
        name='shopping-cart.remove'),

    url(r'^vos-adresses-de-livraison/$',
        DeliveryView.as_view(),
        name='delivery'),
)
