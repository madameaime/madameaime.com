from django.conf.urls import patterns, include, url

from views import ShoppingCartAddView


urlpatterns = patterns('',
    url(r'^sc/add/$',
        ShoppingCartAddView.as_view(),
        name='shoppingcart.add'
    ),
)
