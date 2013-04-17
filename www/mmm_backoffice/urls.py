from django.conf.urls import patterns, include, url

from . import admin_views, general_views, transaction_views


# General
urlpatterns = patterns('',
    url(r'^$',
        general_views.BackofficeIndexView.as_view(),
        name='mmm_backoffice.index'
    ),
)

# Administration
urlpatterns += patterns('',
    url(r'^contact_messages/list/$',
        admin_views.ContactMessageListView.as_view(),
        name='mmm_backoffice.contact_messages.list'
    ),
    url(r'^newsletter/list/$',
        admin_views.NewsletterListView.as_view(),
        name='mmm_backoffice.newsletter.list'
    ),
)

# Transactions
urlpatterns += patterns('',
    url(r'^transactions/list/$',
        transaction_views.TransactionListView.as_view(),
        name='mmm_backoffice.transactions.list'
    ),
    ### ADS ###
    url(r'^ads/products/$',
        transaction_views.ADSProductListView.as_view(),
        name='mmm_backoffice.ads.products'
    ),
    url(r'^ads/kits/$',
        transaction_views.ADSKitListView.as_view(),
        name='mmm_backoffice.ads.kits'
    ),
    url(r'^ads/commands/$',
        transaction_views.ADSCommandsListView.as_view(),
        name='mmm_backoffice.ads.commands'
    ),
)
