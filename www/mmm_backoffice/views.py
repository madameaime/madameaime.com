import csv

from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView

from braces.views import SuperuserRequiredMixin

from emarket.models import Be2billTransaction, OrderSale
from stockmgmt.models import Package, Product

from .ads import *


class CSVResponseMixin(object):
    response_class = HttpResponse

    def render_to_response(self, context, **response_kwargs):
        response = self.response_class(content_type='text/csv',
                                       **response_kwargs)
        response['Content-Disposition'] = ('attachment; filename="%s"' %
                                            self.filename)
        writer = csv.writer(response)
        for line in context['objects']:
            writer.writerow([value.encode('utf8') for value in line])
        return response


class TransactionsList(SuperuserRequiredMixin, ListView):
    template_name = 'backoffice/be2billtransaction_list.html'

    def get_queryset(self):
        return Be2billTransaction.objects.order_by('-order__date')


class ADSProductsView(SuperuserRequiredMixin, CSVResponseMixin, TemplateView):
    filename = 'products.csv'

    def get_context_data(self, **kwargs):
        ctx = super(ADSProductsView, self).get_context_data(**kwargs)
        ctx['objects'] = get_product_file(Product.objects.all())
        return ctx


class ADSKitsView(SuperuserRequiredMixin, CSVResponseMixin, TemplateView):
    filename = 'kits.csv'

    def get_context_data(self, **kwargs):
        ctx = super(ADSKitsView, self).get_context_data(**kwargs)
        ctx['objects'] = get_kits_file(Product.objects.all())
        return ctx


class ADSCommandsView(SuperuserRequiredMixin, CSVResponseMixin, TemplateView):
    filename = 'commands.csv'

    def get_context_data(self, **kwargs):
        ctx = super(ADSCommandsView, self).get_context_data(**kwargs)
        box_march = Product.objects.get(pk=3)
        ctx['objects'] = get_commands_file(box_march)
        return ctx


class ADSDetailedCommandsView(SuperuserRequiredMixin, CSVResponseMixin,
                              TemplateView):
    filename = 'detailedcommands.csv'

    def get_context_data(self, **kwargs):
        ctx = super(ADSDetailedCommandsView, self).get_context_data(**kwargs)
        box_march = Product.objects.get(pk=3)
        ctx['objects'] = get_detailed_commands_file(box_march)
        return ctx
