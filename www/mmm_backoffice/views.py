from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, TemplateView

from braces.views import SuperuserRequiredMixin

from emarket.models import Be2billTransaction
from stockmgmt.models import Product

from .ads import get_product_file


class TransactionsList(SuperuserRequiredMixin, ListView):
    template_name = 'backoffice/be2billtransaction_list.html'

    def get_queryset(self):
        return Be2billTransaction.objects.order_by('-order__date')


class ADSView(SuperuserRequiredMixin, TemplateView):
    template_name = 'backoffice/ads.html'

    def get_context_data(self, **kwargs):
        ctx = super(ADSView, self).get_context_data(**kwargs)
        ctx['products'] = get_product_file(Product.objects.all())
        return ctx
