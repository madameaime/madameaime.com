from django.views.generic import FormView

from forms import ContactForm


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
