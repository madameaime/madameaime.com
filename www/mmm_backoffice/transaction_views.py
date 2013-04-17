from collections import defaultdict

from django.views.generic import ListView, TemplateView

from braces.views import SuperuserRequiredMixin

from . import ads
from emarket.models import Be2billTransaction, Order, OrderSale
from stockmgmt.models import Product


class TransactionListView(SuperuserRequiredMixin, TemplateView):
    template_name = 'mmm_backoffice/transactions/list.html'

    def get_context_data(self, **kwargs):
        """ Return {
            'order_pk': {
                'info': order info
                'success': True or False
                'content': what's in the order
                'be2bill_transactions': be2bill_transactions
            }
        }
        """
        ctx = super(TransactionListView, self).get_context_data(**kwargs)
        orders = {}

        for order in Order.objects.prefetch_related('billing'):
            orders[order.pk] = {
                'info': order,
                'content': [],
                'be2bill_transactions': [],
            }

        # Add content info
        for order_sale in OrderSale.objects.all() \
                                   .prefetch_related('order') \
                                   .prefetch_related('sale__product') \
                                   .prefetch_related('delivery'):
            array = orders[order_sale.order.pk]['content']
            array.append(order_sale)

        # Add Be2billTransaction info
        # order by date insert (last insert is the last action). In case of
        # conflict, take the highest id.
        for transaction in Be2billTransaction.objects \
                                             .order_by('-date_insert',
                                                       '-pk')  \
                                             .prefetch_related('order'):
            array = orders[transaction.order.pk]['be2bill_transactions']
            array.append(transaction)

        # Add success status. Transaction is successfull if the last
        # transaction is a valid payment OR if the order is free.
        for order_pk, order_info in orders.iteritems():
            order_info['success'] = False

            if order_info['info'].is_free is True:
                order_info['success'] = True
            else:
                try:
                    last_transaction = order_info['be2bill_transactions'][0]
                    if (last_transaction.execcode in (0, 1) and
                            last_transaction.operationtype == 'payment'):
                        order_info['success'] = True
                except IndexError:
                    pass

        # Sort orders by pk
        ctx['orders'] = sorted(orders.iteritems())[::-1]
        return ctx


class ADSMixin(SuperuserRequiredMixin):
    template_var_name = None
    get_data = None

    def get_context_data(self, **kwargs):
        ctx = super(ADSMixin, self).get_context_data(**kwargs)
        ctx[self.template_var_name] = self.get_data()
        return ctx


class ADSProductListView(ADSMixin, TemplateView):
    template_name = 'mmm_backoffice/transactions/ads_products.html'
    template_var_name = 'ads_products'
    get_data = lambda self: ads.get_products_file()


class ADSKitListView(ADSMixin, TemplateView):
    template_name = 'mmm_backoffice/transactions/ads_kits.html'
    template_var_name = 'ads_kits'
    get_data = lambda self: ads.get_kits_file()


class ADSCommandsListView(ADSMixin, TemplateView):
    template_name = 'mmm_backoffice/transactions/ads_commands.html'
    template_var_name = 'ads_commands'
    get_data = lambda self: ads.get_commands_file()


class ADSDetailedCommandsListView(ADSMixin, TemplateView):
    template_name = 'mmm_backoffice/transactions/ads_detailedcommands.html'
    template_var_name = 'ads_detailed_commands'
    get_data = lambda self: ads.get_detailed_commands_file()
