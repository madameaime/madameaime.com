from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, simple

from django.contrib import admin
admin.autodiscover()

from emarket import views as emarket_views
import views


urlpatterns = patterns('',
    url(r'^favicon\.ico$', simple.redirect_to,
        {'url': settings.STATIC_URL + 'img/favicon.ico'}),

    url(r'^$',
        TemplateView.as_view(template_name='homepage.html'),
        name='homepage'
    ),

    url(r'^comment-ca-marche$',
        TemplateView.as_view(template_name='how-does-it-work.html'),
        name='how-does-it-work'
    ),

    url(r'^offrir$',
        views.OfferView.as_view(template_name='offer.html'),
        name='offer'
    ),

    url(r'^qui-sommes-nous$',
        TemplateView.as_view(template_name='about.html'),
        name='about'
    ),

    url(r'^notre-histoire$',
        TemplateView.as_view(template_name='story.html'),
        name='story'
    ),

    url(r'^livraison$',
        TemplateView.as_view(template_name='delivery.html'),
        name='delivery'
    ),

    url(r'^cgv$',
        TemplateView.as_view(template_name='sales-conditions.html'),
        name='sales-conditions'
    ),

    url(r'^mentions-legales$',
        TemplateView.as_view(template_name='legal.html'),
        name='legal'
    ),

    url(r'^marques$',
        TemplateView.as_view(template_name='brands.html'),
        name='brands'
    ),

    url(r'^marques/jeanne-m$',
        TemplateView.as_view(template_name='brands/jeanne-m.html'),
        name='brands/jeanne-m'
    ),

    url(r'^marques/au-pays-de-la-fleur-d-oranger$',
        TemplateView.as_view(template_name='brands/au-pays-de-la-fleur-d-oranger.html'),
        name='brands/au-pays-de-la-fleur-d-oranger'
    ),

    url(r'^marques/newtree$',
        TemplateView.as_view(template_name='brands/newtree.html'),
        name='brands/newtree'
    ),

    url(r'^coffret$',
        TemplateView.as_view(template_name='box.html'),
        name='box'
    ),

    url(r'^faq$',
        TemplateView.as_view(template_name='faq.html'),
        name='faq'
    ),

    url(r'^contact$',
        views.ContactView.as_view(),
        name='contact'
    ),

    url(r'^presse$',
        TemplateView.as_view(template_name='press.html'),
        name='press'
    ),

    url(r'^jobs$',
        TemplateView.as_view(template_name='jobs.html'),
        name='jobs'),

    url(r'^terms$',
        'FIXME',
        name='terms'
    ),

    url(r'inscription-sur-newsletter',
        views.NewsletterView.as_view(),
        name='newsletter.add'),

    url(r'^inscription$',
        'django.contrib.auth.views.login',
        {'template_name': 'registration.html'},
        name='registration'
    ),

    url(r'^votre-panier$',
        emarket_views.ShoppingCartView.as_view(),
        name='shoppingcart'),

    url(r'emarket/',
        include('emarket.urls', namespace='emarket')
    ),

    # Ideally, the disconnection page should present a form if accessed on GET
    # to prevent CSRF.
    url(r'deconnexion/$',
        'django.contrib.auth.views.logout',
        {'template_name': 'logout.html'},
        name='logout'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
