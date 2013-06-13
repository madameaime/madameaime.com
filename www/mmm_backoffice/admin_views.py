from django.contrib.auth import get_user_model
from django.views.generic import ListView

from braces.views import SuperuserRequiredMixin

from emarket.models import PartnersSubscription
from mmm.models import ContactMessage, Newsletter


class RevOrderedListMixin(ListView):
    """ ListView ordered by -pk. """
    def get_queryset(self):
        return self.model.objects.order_by('-pk')


class ContactMessageListView(SuperuserRequiredMixin, RevOrderedListMixin):
    template_name = 'mmm_backoffice/admin/contact_messages_list.html'
    model = ContactMessage


class NewsletterListView(SuperuserRequiredMixin, RevOrderedListMixin):
    template_name = 'mmm_backoffice/admin/newsletter_list.html'
    model = Newsletter


class UserList(SuperuserRequiredMixin, ListView):
    template_name = 'mmm_backoffice/admin/user_list.html'

    def get_queryset(self):
        return get_user_model().objects.order_by('-pk')


class PartnersOK(SuperuserRequiredMixin, ListView):
    template_name = 'mmm_backoffice/admin/partnerssubscription_list.html'

    def get_queryset(self):
        return PartnersSubscription.valid_subscriptions.order_by('-pk')
