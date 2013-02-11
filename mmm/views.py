from datetime import datetime

from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, RedirectView, TemplateView

from forms import ContactForm, NewsletterForm
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


class NewsletterView(RedirectView):

    permanent = False
    url = reverse_lazy('homepage')

    def post(self, request, *args, **kwargs):
        """ Create the newsletter entry.
        Note that if there a duplicate entry, form.is_valid will return False
        so there's no need to catch an IntegrityError here.
        """
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
        return super(NewsletterView, self).get(request, *args, **kwargs)
