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

    url(r'^users/list/$',
        admin_views.UserList.as_view(),
        name='mmm_backoffice.user.list'),

    # people who accepted to get info about our partners
    url(r'^partners/$',
        admin_views.PartnersOK.as_view(),
        name='mmm_backoffice.partners_ok'),
)

# Transactions
urlpatterns += patterns('',
    url(r'^transactions/list/$',
        transaction_views.TransactionListView.as_view(),
        name='mmm_backoffice.transactions.list'
    ),
    url(r'^transactions/detailedlist/$',
        transaction_views.TransactionDetailedListView.as_view(),
        name='mmm_backoffice.transactions.detailedlist'
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
    url(r'^ads/detailedcommands/$',
        transaction_views.ADSDetailedCommandsListView.as_view(),
        name='mmm_backoffice.ads.detailedcommands'
    ),

    # set a command status as delivered
    url(r'^ads/detailedcommands/set_delivered/$',
        transaction_views.ADSDetailedCommandSetDeliveredView.as_view(),
        name='mmm_backoffice.ads.detailedcommands.set_delivered'),
)
