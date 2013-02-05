from datetime import datetime, timedelta
from decimal import Decimal
import random
import string

from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.formsets import formset_factory
from django.http import Http404, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, TemplateView, View
from django.views.generic.simple import direct_to_template, redirect_to

from models import Sale, ShoppingCartLog
import forms


class ShoppingCartAddView(View):

    def post(self, request):
        # We could use a form to extract the sale_id properly. It'd be a little
        # more complex though, so make the sanitization of sale_id here.
        try:
            sale_id = int(request.POST['sale_id'])
        except ValueError:
            return HttpResponseServerError('invalid sale_id')
        sale = get_object_or_404(Sale, pk=sale_id)
        session = get_object_or_404(Session, pk=request.session.session_key)
        
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
        """ Delete items from ShoppingCartLog with a date older than 30 minutes
        and update valid items timeouts
        """
        ctx = super(ShoppingCartView, self).get_context_data(**kwargs)
        session = get_object_or_404(Session,
                                    pk=self.request.session.session_key)

        # Delete items for wich timeout is reached
        expired = datetime.now() - timedelta(minutes=30)
        timeout_obj = ShoppingCartLog.objects.filter(session=session)  \
                                             .filter(date__lt=expired)
        timeout_obj.delete()

        # Get valid objects
        ctx['objects'] = ShoppingCartLog.objects.filter(session=session) \
                                                .order_by('date')

        # Update timeouts
        now = datetime.now()
        for obj in ctx['objects']:
            obj.date = now
            obj.save()

        # Add meta info
        ctx['total_price'] = sum(obj.sale.price for obj in ctx['objects'])
        ctx['charges'] = ctx['total_price'] * Decimal('0.196')
        return ctx


class ShoppingCartRemoveView(DeleteView):

    success_url = reverse_lazy('shoppingcart')

    def get_object(self, *args, **kwargs):
        session = get_object_or_404(Session,
                                    pk=self.request.session.session_key)
        log_id = self.kwargs.get('log_id')
        try:
            log = ShoppingCartLog.objects.get(session=session, pk=log_id)
        except ShoppingCartLog.DoesNotExist:
            raise Http404
        return log

    def get(self, *args, **kwargs):
        """By default, DeleteView displays a template to confirm the object
        deletion.

        This view isn't supposed to be called with GET, so let's avoid a
        template creation and raise a 404 if the page is not called with a
        POST.
        """
        raise Http404


class DeliveryView(TemplateView):
    template_name = 'emarket/delivery.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DeliveryView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(DeliveryView, self).get_context_data(**kwargs)

        post_data = None
        if self.request.method == 'POST':
            post_data = self.request.POST

        ctx['billing_form'] = forms.BillingForm(post_data)

        session = get_object_or_404(Session,
                                    pk=self.request.session.session_key)

        # keep the same order than in ShoppingCartView
        items = ShoppingCartLog.objects.filter(session=session) \
                                       .order_by('date')
        ctx['items'] = items

        DeliveryFormset = formset_factory(forms.DeliveryForm,
                                          formset=forms.RequiredFormset,
                                          extra=items.count())

        ctx['delivery_formset'] = DeliveryFormset(post_data)
        ctx['tos_form'] = forms.ToSForm(post_data)

        return ctx

    def _generate_order_id():
        """ Generate a random order id exposed to the user of length 16
        """
        return ''.join(random.choice(string.ascii_uppercase + string.digits)
                       for x in range(16))


    def post(self, request):
        ctx = self.get_context_data()

        tos_form = ctx['tos_form']
        if not tos_form.is_valid():
            return self.render_to_response(ctx)

        billing_form = ctx['billing_form']
        if not billing_form.is_valid():
            return self.render_to_response(ctx)

        delivery_formset = ctx['delivery_formset']
        if not delivery_formset.is_valid():
            return self.render_to_response(ctx)

        # Here, from is valid. Insert in database
#        for form in delivery_formset:
#            pass
#            #print form.cleaned_data['delivery_place']
        return self.render_to_response(ctx)
