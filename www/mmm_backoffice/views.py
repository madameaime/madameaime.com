import csv

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView

from braces.views import SuperuserRequiredMixin

from emarket.models import Be2billTransaction
from stockmgmt.models import Product

from .ads import get_kits_file, get_product_file


class CSVResponseMixin(object):
    response_class = HttpResponse

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'text/csv'

        response = self.response_class(**response_kwargs)
        writer = csv.writer(response)
        for line in context['objects']:
            writer.writerow([value.encode('utf8') for value in line])
        return response


class TransactionsList(SuperuserRequiredMixin, ListView):
    template_name = 'backoffice/be2billtransaction_list.html'

    def get_queryset(self):
        return Be2billTransaction.objects.order_by('-order__date')


class ADSProductsView(SuperuserRequiredMixin, CSVResponseMixin, TemplateView):
    def get_context_data(self, **kwargs):
        ctx = super(ADSProductsView, self).get_context_data(**kwargs)
        ctx['objects'] = get_product_file(Product.objects.all())
        return ctx


class ADSKitsView(SuperuserRequiredMixin, CSVResponseMixin, TemplateView):
    def get_context_data(self, **kwargs):
        ctx = super(ADSKitsView, self).get_context_data(**kwargs)
        ctx['objects'] = get_kits_file(Product.objects.all())
        return ctx
