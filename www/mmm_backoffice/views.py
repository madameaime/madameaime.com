from django.core.exceptions import PermissionDenied
from django.views.generic import ListView

from braces.views import SuperuserRequiredMixin

from emarket.models import Be2billTransaction


class TransactionsList(SuperuserRequiredMixin, ListView):
    template_name = 'backoffice/be2billtransaction_list.html'

    def get_queryset(self):
        return Be2billTransaction.objects.order_by('-order__date')
