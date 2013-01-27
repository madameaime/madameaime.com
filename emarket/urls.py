from django.conf.urls import patterns, include, url

from views import DeliveryView, ShoppingCartAddView, ShoppingCartRemoveView


urlpatterns = patterns('',
    url(r'^sc/add/$',
        ShoppingCartAddView.as_view(),
        name='shoppingcart.add'
    ),

    url(r'^sc/remove/(?P<log_id>\d+)$',
        ShoppingCartRemoveView.as_view(),
        name='shoppingcart.remove'),

    url(r'^vos-adresses-de-livraison/$',
        DeliveryView.as_view(),
        name='delivery'),
)
