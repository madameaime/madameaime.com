from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView

from django.contrib import admin
admin.autodiscover()

from emarket import views as emarket_views
import views


urlpatterns = patterns('',
    url(r'^favicon\.ico$',
        RedirectView.as_view(url=settings.STATIC_URL + 'img/favicon.ico')
    ),

    url(r'^$',
        TemplateView.as_view(template_name='homepage.html'),
        name='homepage'
    ),

    url(r'^comment-ca-marche/$',
        TemplateView.as_view(template_name='how-does-it-work.html'),
        name='how-does-it-work'
    ),

    url(r'^offrir/$',
        views.OfferView.as_view(template_name='offer.html'),
        name='offer'
    ),

    url(r'^qui-sommes-nous/$',
        TemplateView.as_view(template_name='about.html'),
        name='about'
    ),

    url(r'^notre-histoire/$',
        TemplateView.as_view(template_name='story.html'),
        name='story'
    ),

    url(r'^livraison/$',
        TemplateView.as_view(template_name='delivery.html'),
        name='delivery'
    ),

    url(r'^cgv/$',
        TemplateView.as_view(template_name='sales-conditions.html'),
        name='sales-conditions'
    ),

    url(r'^mentions-legales/$',
        TemplateView.as_view(template_name='legal.html'),
        name='legal'
    ),

    # Brands:

    url(r'^marques/$',
        TemplateView.as_view(template_name='brands.html'),
        name='brands'
    ),

    url(r'^marques/jeanne-m/$',
        TemplateView.as_view(template_name='brands/jeanne-m.html'),
        name='brands/jeanne-m'
    ),

    url(r'^marques/au-pays-de-la-fleur-d-oranger/$',
        TemplateView.as_view(template_name='brands/au-pays-de-la-fleur-d-oranger.html'),
        name='brands/au-pays-de-la-fleur-d-oranger'
    ),

    url(r'^marques/newtree/$',
        TemplateView.as_view(template_name='brands/newtree.html'),
        name='brands/newtree'
    ),

    url(r'^marques/secrets-de-miel/$',
        TemplateView.as_view(template_name='brands/secrets-de-miel.html'),
        name='brands/secrets-de-miel'
    ),

    url(r'^marques/sous-l-oranger/$',
        TemplateView.as_view(template_name='brands/sous-l-oranger.html'),
        name='brands/sous-l-oranger'
    ),

    url(r'^marques/comptoir-colonial/$',
        TemplateView.as_view(template_name='brands/comptoir-colonial.html'),
        name='brands/comptoir-colonial'
    ),

    # Boxes:

    url(r'^coffret/$',
        RedirectView.as_view(url=reverse_lazy('boxes/2013-feb'),
                             permanent=False),
        name='boxes'
    ),

    url(r'^coffret/fevrier-2013/$',
        TemplateView.as_view(template_name='boxes/2013-feb.html'),
        name='boxes/2013-feb'
    ),

    url(r'^coffret/decembre-2012/$',
        TemplateView.as_view(template_name='boxes/2012-dec.html'),
        name='boxes/2012-dec'
    ),


    url(r'^faq/$',
        TemplateView.as_view(template_name='faq.html'),
        name='faq'
    ),

    url(r'^contact/$',
        views.ContactView.as_view(),
        name='contact'
    ),

    url(r'^presse/$',
        TemplateView.as_view(template_name='press.html'),
        name='press'
    ),

    url(r'^jobs/$',
        TemplateView.as_view(template_name='jobs.html'),
        name='jobs'),

    url(r'inscription-sur-newsletter',
        views.NewsletterView.as_view(),
        name='newsletter.add'
    ),

    url(r'^inscription/$',
        views.RegistrationView.as_view(),
        name='register'
    ),

    url(r'^se-connecter/$',
        views.AuthenticationView.as_view(),
        name='login'
    ),

    url(r'mot-de-passe-oublie/$',
        views.RecoverPasswordView.as_view(),
        name='password.recover'
    ),

    url(r'nouveau-mot-de-passe/$',
        views.UpdatePasswordView.as_view(),
        name='password.update'
    ),

    url(r'^votre-panier/$',
        emarket_views.ShoppingCartView.as_view(),
        name='shopping-cart'
    ),

    url(r'^paiement/$',
        emarket_views.PaymentView.as_view(),
        name='payment'
    ),

    url(r'',
        include('emarket.urls', namespace='emarket')
    ),

    url(r'deconnexion/$',
        'django.contrib.auth.views.logout', {'next_page': reverse_lazy('homepage')},
        name='logout'
    ),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
