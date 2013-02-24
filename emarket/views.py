from datetime import datetime, timedelta
from decimal import Decimal
import json
import random
import string

from be2bill import PaymentForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import IntegrityError
from django.forms.formsets import formset_factory
from django.http import Http404, HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView, TemplateView, RedirectView, View

from models import Be2billTransaction, Order, OrderSale, Sale
import forms
import utils


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
        return redirect(reverse('shopping-cart'), permanent=False)


class ShoppingCartView(TemplateView):
    template_name = 'emarket/shopping-cart.html'

    def get_context_data(self, **kwargs):
        ctx = super(ShoppingCartView, self).get_context_data(**kwargs)
        ctx['objects'] = self.request.session.get('shopping_cart', [])
        ctx['total_price'] = sum(sale.price for sale in ctx['objects'])
        ctx['charges'] = ctx['total_price'] * Decimal('0.196')
        return ctx


class ShoppingCartRemoveView(RedirectView):

    permanent = False
    url = reverse_lazy('shopping-cart')

    def post(self, *args, **kwargs):
        remove_id = int(self.kwargs.get('sale_id'))
        objects = self.request.session.get('shopping_cart', [])
        for idx, sale in enumerate(objects):
            if sale.pk == remove_id:
                del(objects[idx])
                self.request.session.save()
                break
        return super(ShoppingCartRemoveView, self).post(*args, **kwargs)


class DeliveryView(TemplateView):
    template_name = 'emarket/delivery.html'

    class EmptyShoppingCart(Exception):
        pass

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """ This page requires the user to be authenticated
        """
        try:
            return super(DeliveryView, self).dispatch(*args, **kwargs)
        except DeliveryView.EmptyShoppingCart:
            return redirect(reverse('offer'), permanent=False)

    def get_context_data(self, **kwargs):
        """ Generate the three forms displayed (billing info, delivery info and
        accept terms and conditions)
        """
        ctx = super(DeliveryView, self).get_context_data(**kwargs)

        if self.request.method != 'POST':
            post_data = None
        else:
            post_data = self.request.POST

        items = self.request.session.get('shopping_cart', [])
        if len(items) == 0:
            raise DeliveryView.EmptyShoppingCart("Cannot delivery nothing")

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

    def _create_order(self, request, tos_form, billing_form, delivery_formset):
        """ Insert a new Order, and correspondings OrderSale entries. Return
        the order_id. """

        billing_address = billing_form.save()

        # Try to find a unique exposed_id
        # And save the billing info form
        inserted = False
        while not inserted:
            try:
                order_id = self._generate_order_id()
                promo_code = tos_form.cleaned_data['promo_code']
                order = Order(exposed_id=order_id,
                              user=request.user,
                              billing=billing_address,
                              promo_code=promo_code)
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
        return order_id

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
        order_id = self._create_order(request, tos_form, billing_form,
                                      delivery_formset)
        # Redirect to the payment process page
        return redirect(reverse('payment') + '?order=%s' % order_id,
                        permanent=False)


class PaymentView(TemplateView):
    template_name = 'emarket/payment.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """ This page required the user to be authenticated
        """
        return super(PaymentView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(PaymentView, self).get_context_data(**kwargs)
        order_id = self.request.GET.get('order')
        # TODO: ensure that the order has not already been paid or raise a
        # Http404.
        order = get_object_or_404(Order, exposed_id=order_id,
                                  user=self.request.user)
        sales = OrderSale.objects.filter(order=order)
        price = int(sum(sale.sale.price * 100 for sale in sales))
        ctx['form'] = forms.Be2billForm({
                        "CLIENTIDENT": order.billing.email,
                        "DESCRIPTION": "Les coffrets de Madame Aime",
                        "CLIENTEMAIL": order.billing.email,
                        "ORDERID": order.exposed_id,
                        "AMOUNT": price })
        return ctx


class CheckoutOKClient(TemplateView):

    def get_template_names(self):
        PaymentForm.verify_hash(settings.BE2BILL_PASSWORD,
                                self.request.GET)
        if self.request.GET.get('EXECCODE') in ('0000', '0001'):
            # empty shopping card
            self.request.session['shopping_cart'] = []
            return 'emarket/checkout-ok-client.html'
        return 'emarket/checkout-ko-client.html'

    def get_context_data(self, **kwargs):
        ctx = super(CheckoutOKClient, self).get_context_data(**kwargs)
        ctx['GET'] = self.request.GET

        exposed_id = self.request.GET.get('ORDERID')
        order = Order.objects.get(exposed_id=exposed_id)
        ctx['order'] = order
        ctx['order_sales'] = OrderSale.objects.filter(order=order)
        ctx['total_price'] = sum(p.sale.price for p in ctx['order_sales'])
        return ctx


class Be2billNotifTransaction(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(Be2billNotifTransaction, self).dispatch(*args, **kwargs)

    def _save_transaction(self, request, params):
        PaymentForm.verify_hash(settings.BE2BILL_PASSWORD, params)
        log_values = {}
        for field_name in Be2billTransaction._meta.get_all_field_names():
            # Model fields are in lower case and be2bill loves uppercase.
            key = field_name.upper()
            # Python variables can't start with a digit. The key 3DSECURE has a
            # corresponding field named '_3dsecure'. Skip the first undescore.
            if key.startswith('_'):
                key = key[1:]
            value = params.get(key)
            if value:
                log_values[field_name] = value

        log_values['blob'] = json.dumps(params)
        Be2billTransaction(**log_values).save()

        # In case of success, send a mail to inform the transaction is a
        # success
        if params.get('EXECCODE') in ('0000', '0001'):
            exposed_id = params.get('ORDERID')
            order = Order.objects.get(exposed_id=exposed_id)
            mail_to = order.billing.email
            utils.send_mail(settings.TRANSACTION_SUCCESS_MAIL_SUBJECT,
                            [mail_to],
                            settings.TRANSACTION_SUCCESS_MAIL_FROM,
                            'emarket/transaction_confirm.txt',
                            'emarket/transaction_confirm.html',
                            params={'order': order})

        return HttpResponse('OK')

    def get(self, request, *args, **kwargs):
        return self._save_transaction(request, request.GET)

    def post(self, request, *args, **kwargs):
        return self._save_transaction(request, request.POST)
