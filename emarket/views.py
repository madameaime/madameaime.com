from datetime import datetime, timedelta
from decimal import Decimal
import random
import string

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import IntegrityError
from django.forms.formsets import formset_factory
from django.http import Http404, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, TemplateView, RedirectView, View
from django.views.generic.simple import direct_to_template, redirect_to

from models import Order, OrderSale, Sale
import forms


class ShoppingCartAddView(View):

    def post(self, request):
        """
        Add an item to a session.

        For now, there's no check ton ensure that the corresponding sale is
        valid.
        We should also check that we don't run out of stocks.
        """
        # We could use a form to extract the sale_id properly. It'd be a little
        # more complex though, so make the sanitization of sale_id here.
        try:
            sale_id = int(request.POST['sale_id'])
        except ValueError:
            return HttpResponseServerError('invalid sale_id')

        sale = get_object_or_404(Sale, pk=sale_id)

        request.session.setdefault('shopping_cart', []).append(sale)
        request.session.modified = True
        return redirect_to(request, reverse('shoppingcart'), permanent=False)


class ShoppingCartView(TemplateView):
    template_name = 'emarket/shopping_cart.html'

    def get_context_data(self, **kwargs):
        ctx = super(ShoppingCartView, self).get_context_data(**kwargs)
        ctx['objects'] = self.request.session['shopping_cart']
        ctx['total_price'] = sum(sale.price for sale in ctx['objects'])
        ctx['charges'] = ctx['total_price'] * Decimal('0.196')
        return ctx


class ShoppingCartRemoveView(RedirectView):

    permanent = False
    url = reverse_lazy('shoppingcart')

    def post(self, *args, **kwargs):
        remove_id = int(self.kwargs.get('sale_id'))
        for idx, sale in enumerate(self.request.session['shopping_cart']):
            if sale.pk == remove_id:
                del(self.request.session['shopping_cart'][idx])
                self.request.session.save()
                break
        return super(ShoppingCartRemoveView, self).post(*args, **kwargs)


class DeliveryView(TemplateView):
    template_name = 'emarket/delivery.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """ This page requires the user to be authenticated
        """
        return super(DeliveryView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """ Generate the three forms displayed (billing info, delivery info and
        accept terms and conditions)
        """
        ctx = super(DeliveryView, self).get_context_data(**kwargs)

        if self.request.method != 'POST':
            post_data = None
        else:
            post_data = self.request.POST

        items = self.request.session['shopping_cart']

        DeliveryFormset = formset_factory(forms.DeliveryForm, extra=0)
        # Billing form
        ctx['billing_form'] = forms.BillingForm(post_data)
        # Delivery form
        initial = list({'sale_id': sale.pk} for sale in items)
        ctx['delivery_formset'] = DeliveryFormset(post_data, initial=initial)
        # Terms of Service form
        ctx['tos_form'] = forms.ToSForm(post_data)
        return ctx

    @staticmethod
    def _generate_order_id():
        """ Generate a random order id exposed to the user of length 16
        """
        return ''.join(random.choice(string.ascii_uppercase + string.digits)
                       for x in range(8))

    def _create_order(self, request, billing_form, delivery_formset):
        """ Insert a new Order, and correspondings OrderSale entries """

        billing_address = billing_form.save()

        # Try to find a unique exposed_id
        # And save the billing info form
        inserted = False
        while not inserted:
            try:
                order_id = self._generate_order_id()
                order = Order(exposed_id=order_id,
                              user=request.user,
                              billing=billing_address)
                order.save()
                inserted = True
            except IntegrityError:
                pass

        # Save delivery forms
        for form in delivery_formset:
            cdata = form.cleaned_data
            #TODO: ensure that the sale_id corresponds to a valid sale. This
            # could be done in the clean_<fieldname> of the form
            sale = Sale.objects.get(pk=cdata['sale_id'])
            if cdata['delivery_place'] == '0':
                delivery = billing_address
            else:
                delivery = form.save()
            # Create the order sale
            osale = OrderSale(order=order, sale=sale, delivery=delivery)
            osale.save()

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

        # Forms are valid, create the order
        self._create_order(request, billing_form, delivery_formset)
        # Redirect to the payment process page
        return self.render_to_response(ctx)
