from datetime import datetime, timedelta

from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, View
from django.views.generic.simple import direct_to_template, redirect_to

from models import Sale, ShoppingCartLog


class ShoppingCartAddView(View):

    def post(self, request):
        # We could use a form to extract the sale_id properly. It'd be a little
        # more complex though, so make the sanitization of sale_id here.
        try:
            sale_id = int(request.POST['sale_id'])
        except ValueError:
            return HttpResponseServerError('invalid sale_id')
        #TODO: replace with get_object_or_404
        sale = Sale.objects.get(pk=sale_id)
        #TODO: replace with get_object_or_404
        session = Session.objects.get(pk=request.session.session_key)
        
        log = ShoppingCartLog(sale=sale, session=session)

        try:
            log.save()
        except ValueError:
            return direct_to_template(request,
                    'emarket/shoppingcart_add_error.html',
                    extra_context={'sale': sale})
        return redirect_to(request, reverse('shoppingcart'), permanent=False)


class ShoppingCartView(TemplateView):
    template_name = 'emarket/shopping_cart.html'

    def get_context_data(self, **kwargs):
        ctx = super(ShoppingCartView, self).get_context_data(**kwargs)
        session = get_object_or_404(Session,
                                    pk=self.request.session.session_key)

        expired = datetime.now() - timedelta(minutes=30)
        ctx['objects'] = ShoppingCartLog.objects.filter(session=session)   \
                                                .filter(date__gte=expired) \
                                                .order_by('date')
        return ctx
