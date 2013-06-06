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

    #Legacy

    url(r'^offrir/$',
        RedirectView.as_view(url=reverse_lazy('order'),
                             permanent=False),
        name='offer'
    ),


    url(r'^$',
        TemplateView.as_view(template_name='homepage.html'),
        name='homepage'
    ),

    url(r'^mon-compte/$',
        RedirectView.as_view(url=reverse_lazy('account/orders'),
                             permanent=False),
        name='account'
    ),

    url(r'^mon-compte/commandes/$',
        views.AccountOrdersView.as_view(),
        name='account/orders'
    ),

    url(r'^mon-compte/commandes/(?P<pk>\d+)/$',
        views.OrderView.as_view(template_name='account/order.html'),
        name='account/order'
    ),

    url(r'^mon-compte/commandes/(?P<pk>\d+)/facture/$',
        views.OrderInvoicePdfView.as_view(template_name='account/order.html'),
        name='account/order/pdf_invoice'
    ),

    url(r'^google5fa0e92da89aaa27\.html$',
        TemplateView.as_view(template_name='google5fa0e92da89aaa27.html')
    ),

    url(r'^landing/madameaime-phyderma/$',
        TemplateView.as_view(template_name='landing/madameaime-phyderma.html'),
        name='landing/madameaime-phyderma'
    ),

    url(r'^comment-ca-marche/$',
        TemplateView.as_view(template_name='how-does-it-work.html'),
        name='how-does-it-work'
    ),

    url(r'^commander/$',
        views.OfferView.as_view(template_name='order.html'),
        name='order'
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

    url(r'^marques/jeanne-m/soin-pour-les-pieds/$',
        TemplateView.as_view(template_name='brands/jeanne-m/soin-pour-les-pieds.html'),
        name='brands/jeanne-m/soin-pour-les-pieds'
    ),

    url(r'^marques/au-pays-de-la-fleur-d-oranger/$',
        TemplateView.as_view(template_name='brands/au-pays-de-la-fleur-d-oranger.html'),
        name='brands/au-pays-de-la-fleur-d-oranger'
    ),

    url(r'^marques/au-pays-de-la-fleur-d-oranger/savon-d-invites/$',
        TemplateView.as_view(template_name='brands/au-pays-de-la-fleur-d-oranger/savon-d-invites.html'),
        name='brands/au-pays-de-la-fleur-d-oranger/savon-d-invites'
    ),

    url(r'^marques/newtree/$',
        TemplateView.as_view(template_name='brands/newtree.html'),
        name='brands/newtree'
    ),

    url(r'^marques/oliv/lait-corps-ultra-fondant/$',
        TemplateView.as_view(template_name='brands/oliv/lait-corps-ultra-fondant.html'),
        name='brands/oliv/lait-corps-ultra-fondant'
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

    url(r'^marques/teatower/the-a-la-menthe-bio/$',
        TemplateView.as_view(template_name='brands/teatower/the-a-la-menthe-bio.html'),
        name='brands/teatower/the-a-la-menthe-bio'
    ),

    url(r'^marques/phyderma/$',
        TemplateView.as_view(template_name='brands/phyderma.html'),
        name='brands/phyderma'
    ),

    url(r'^marques/phyderma/soin-de-jour-revitalisant/$',
        TemplateView.as_view(template_name='brands/phyderma/soin-de-jour-revitalisant.html'),
        name='brands/phyderma/soin-de-jour-revitalisant'
    ),

    url(r'^marques/phyderma/creme-mains-reparatrice/$',
        TemplateView.as_view(template_name='brands/phyderma/creme-mains-reparatrice.html'),
        name='brands/phyderma/creme-mains-reparatrice'
    ),

    url(r'^marques/dans-le-noir-le-spa/$',
        TemplateView.as_view(template_name='brands/dans-le-noir-le-spa.html'),
        name='brands/dans-le-noir-le-spa'
    ),

    url(r'^marques/le-coin-des-delices/miel-de-citronnier/$',
        TemplateView.as_view(template_name='brands/le-coin-des-delices/miel-de-citronnier.html'),
        name='brands/le-coin-des-delices/miel-de-citronnier'
    ),

    url(r'^marques/le-coin-des-delices/nougat-de-montelimar/$',
        TemplateView.as_view(template_name='brands/le-coin-des-delices/nougat-de-montelimar.html'),
        name='brands/le-coin-des-delices/nougat-de-montelimar'
    ),

    url(r'^marques/sothys/gelee-gommante-visage/$',
        TemplateView.as_view(template_name='brands/sothys/gelee-gommante-visage.html'),
        name='brands/sothys/gelee-gommante-visage'
    ),


    # Boxes:

    url(r'^coffret/$',
        RedirectView.as_view(url=reverse_lazy('boxes/2013-may'),
                             permanent=False),
        name='boxes'
    ),

    url(r'^coffret/mai-2013/$',
        TemplateView.as_view(template_name='boxes/2013-may.html'),
        name='boxes/2013-may'
    ),

    url(r'^coffret/mars-2013/$',
        TemplateView.as_view(template_name='boxes/2013-mar.html'),
        name='boxes/2013-mar'
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

    url(r'^backoffice/',
        include('mmm_backoffice.urls')
    ),

    url(r'deconnexion/$',
        'django.contrib.auth.views.logout', {'next_page': reverse_lazy('homepage')},
        name='logout'
    ),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
