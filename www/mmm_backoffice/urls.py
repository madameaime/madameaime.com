from django.conf.urls import patterns, include, url

from .views import *


urlpatterns = patterns('',
    url(r'^transactions/$',
        TransactionsList.as_view(),
        name='transactions.list'
    ),

    url(r'^ads/products/$',
        ADSProductsView.as_view(),
        name='ads.products'
    ),

    url(r'^ads/kits/$',
        ADSKitsView.as_view(),
        name='ads.kits'
    ),

    url(r'^ads/commands/$',
        ADSCommandsView.as_view(),
        name='ads.commands'
    ),

    url(r'ads/detailedcommands/$',
        ADSDetailedCommandsView.as_view(),
        name='ads.detailedcommands'
    ),
)
