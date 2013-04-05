import csv

from django.core.exceptions import PermissionDenied
from django.db.models import Q, Count
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

        # ADS sucks. They don't know how to parse a CSV (escaping characters seem
        # to be too complicated to handle for them). Separate fields with a pipe
        # (as it won't be used in fields, at least I hope)
        writer = csv.writer(response, delimiter='|')
        for line in context['objects']:
            writer.writerow([value.encode('utf8') for value in line])
        return response


class TransactionsList(SuperuserRequiredMixin, ListView):
    template_name = 'backoffice/be2billtransaction_list.html'

    def get_queryset(self):
        """
        SQL equivalent: SELECT * FROM (SELECT * FROM be2billtransaction ORDER
        BY date_insert DESC, order__date DESC, id DESC) AS subq GROUP BY order

        >> Get every latest be2bill transaction corresponding to every sale

        Of course, doing this with the Django ORM is a pain in the ass
        """
        # get all order sales
        osales = OrderSale.objects \
                          .all() \
                          .prefetch_related('order__be2billtransaction_set')
        trans_ids = []
        # for every osale, get the last transaction
        for osale in osales:
            try:
                # order by pk because if dates conflict, take the last insert
                last_transaction = Be2billTransaction.objects \
                            .filter(order=osale.order) \
                            .order_by('-date_insert', '-order__date', '-pk')[0]
                trans_ids.append(last_transaction.pk)
            except IndexError:
                pass
        # return the last transaction for every osale
        return Be2billTransaction.objects.filter(pk__in=trans_ids) \
                                         .order_by('-date_insert',
                                                   '-order__date') \
                                         .select_related('order')


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
