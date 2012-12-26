from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
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
        TemplateView.as_view(template_name='about-us.html'),
        name='about-us'
    ),

    url(r'^notre-histoire$',
        TemplateView.as_view(template_name='story'),
        name='story'
    ),

    # Examples:
    # url(r'^$', 'mmm.views.home', name='home'),
    # url(r'^mmm/', include('mmm.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
