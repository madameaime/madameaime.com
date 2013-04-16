from collections import defaultdict

from django.views.generic import ListView, TemplateView

from braces.views import SuperuserRequiredMixin

from emarket.models import Be2billTransaction, Order, OrderSale


class TransactionList(SuperuserRequiredMixin, TemplateView):
    template_name = 'mmm_backoffice/transactions/list.html'

    def get_context_data(self, **kwargs):
        """ Return {
            'order_pk': {
                'info': order info
                'content': what's in the order
                'be2bill_transactions': be2bill_transactions
            }
        }
        """
        ctx = super(TransactionList, self).get_context_data(**kwargs)
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

        # Sort orders by pk
        ctx['orders'] = sorted(orders.iteritems())[::-1]
        return ctx
