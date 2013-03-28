from django.conf.urls import patterns, include, url

from .views import *


urlpatterns = patterns('',
    url(r'^transactions/$',
        TransactionsList.as_view(),
        name='transactions.list'
    ),

    url(r'^ads/$',
        ADSView.as_view(),
        name='ads.products'
    ),
)
