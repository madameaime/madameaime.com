from django.core.exceptions import PermissionDenied
from django.views.generic import ListView

from emarket.models import Be2billTransaction


class TransactionsList(ListView):
    template_name = 'backoffice/be2billtransaction_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return super(TransactionsList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Be2billTransaction.objects.order_by('-order__date')
