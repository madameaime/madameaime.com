from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, simple

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^favicon\.ico$', simple.redirect_to, { 'url': '/static/img/favicon.ico' }),

    url(r'^$',
        TemplateView.as_view(template_name='homepage.html'),
        name='homepage'
    ),

    url(r'^comment-ca-marche$',
        TemplateView.as_view(template_name='how-does-it-work.html'),
        name='how-does-it-work'
    ),

    url(r'^offrir$',
        TemplateView.as_view(template_name='offer.html'),
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

    # Examples:
    # url(r'^$', 'mmm.views.home', name='home'),
    # url(r'^mmm/', include('mmm.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
