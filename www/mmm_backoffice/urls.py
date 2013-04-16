from django.conf.urls import patterns, include, url

from . import admin_views, general_views, transaction_views


# General
urlpatterns = patterns('',
    url(r'^$',
        general_views.BackofficeIndex.as_view(),
        name='mmm_backoffice.index'
    ),
)

# Administration
urlpatterns += patterns('',
    url(r'^contact_messages/list/$',
        admin_views.ContactMessageList.as_view(),
        name='mmm_backoffice.contact_messages.list'
    ),
    url(r'^newsletter/list/$',
        admin_views.NewsletterList.as_view(),
        name='mmm_backoffice.newsletter.list'
    ),
)

# Transactions
urlpatterns += patterns('',
    url(r'^transactions/list/$',
        transaction_views.TransactionList.as_view(),
        name='mmm_backoffice.transactions.list'
    ),
)
