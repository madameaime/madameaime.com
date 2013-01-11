from datetime import datetime

from django.views.generic import FormView, TemplateView

from forms import ContactForm
from models import OfferPage


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm


class OfferView(TemplateView):
    template_name = 'offer.html'

    def get_context_data(self, **kwargs):
        ctx = super(OfferView, self).get_context_data(**kwargs)

        offers = OfferPage.objects.filter(date_start__lte=datetime.now()) \
                                  .order_by('-date_start')                \
                                  .all()
        ctx['offers'] = offers[0] if offers else None
        return ctx
