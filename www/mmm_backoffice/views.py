from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, TemplateView

from braces.views import SuperuserRequiredMixin

from emarket.models import Be2billTransaction
from stockmgmt.models import Product

from .ads import get_kits_file, get_product_file


class TransactionsList(SuperuserRequiredMixin, ListView):
    template_name = 'backoffice/be2billtransaction_list.html'

    def get_queryset(self):
        return Be2billTransaction.objects.order_by('-order__date')


class ADSProductsView(SuperuserRequiredMixin, TemplateView):
    template_name = 'backoffice/ads_products.html'

    def get_context_data(self, **kwargs):
        ctx = super(ADSProductsView, self).get_context_data(**kwargs)
        ctx['products'] = get_product_file(Product.objects.all())
        return ctx


class ADSKitsView(SuperuserRequiredMixin, TemplateView):
    template_name = 'backoffice/ads_kits.html'

    def get_context_data(self, **kwargs):
        ctx = super(ADSKitsView, self).get_context_data(**kwargs)
        ctx['kits'] = get_kits_file(Product.objects.all())
        return ctx
