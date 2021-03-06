# -*- coding: utf8 -*-

from datetime import datetime, timedelta
from decimal import Decimal
import json

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
from django.views.generic import (DeleteView, TemplateView, RedirectView, View,
                                  FormView)

from mailhelpers import utils

from .models import (Be2billTransaction, Order, OrderSale,
                     PartnersSubscription, PromoCode, Sale)
from . import forms


class PromoCodeMixin(object):

    def dispatch(self, request, *args, **kwargs):
        """ If the product for which the promo code applies has been removed
        from the shopping cart, cancel the promo code.
        I prefer not to check if the promo code has expired (if someone added
        the code before it was expired, I don't see a reason why I should
        cancel it. Maybe should I).
        """
        # no code duplication (return super(...) + don't call super method now
        view = lambda: super(PromoCodeMixin, self).dispatch(request, *args,
                                                            **kwargs)
        promo_code = self.get_from_session()
        if promo_code is None:
            return view()
        objects = self.request.session.get('shopping_cart', [])
        if promo_code.sale and promo_code.sale.pk not in objects:
            self.remove_from_session()
        return view()

    def remove_from_session(self):
        # AttributeError is raised because there's no request in "self" when
        # the class is used with import_commands.py.
        try:
            if 'promo_code' in self.request.session:
                del(self.request.session['promo_code'])
        except AttributeError:
            pass

    def set_in_session(self, promo_code):
        """ Set promo_code in session. No check is done to ensure that it is
        valid.
        """
        self.request.session['promo_code'] = promo_code

    def get_from_session(self):
        try:
            promo_code = self.request.session['promo_code']
        except KeyError:
            return None
        # no session set yet
        except AttributeError:
            return None
        if promo_code:
            obj = get_object_or_404(PromoCode, code=promo_code)
            return obj
        return None


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

        if not sale.end or sale.end > datetime.now():
            request.session.setdefault('shopping_cart', []).append(sale.pk)
            request.session.modified = True
        else:
            raise Http404('Cette vente est terminée')
        return redirect(reverse('shopping-cart'), permanent=False)


class ShoppingCartView(PromoCodeMixin, FormView):
    template_name = 'emarket/shopping-cart.html'
    form_class = forms.PromoCodeForm

    def get_initial(self):
        initial = super(ShoppingCartView, self).get_initial()
        promo_code = self.get_from_session()
        if promo_code is not None:
            initial['code'] = promo_code.code
        return initial

    def get_form_kwargs(self):
        kwargs = super(ShoppingCartView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        objects = self.request.session.get('shopping_cart', [])
        kwargs['shopping_cart'] = [get_object_or_404(Sale, pk=pk)
                                    for pk in objects]
        return kwargs

    def form_valid(self, form):
        http_response = super(ShoppingCartView, self).form_valid(form)
        # set the promo code in session
        promo_code = form.cleaned_data['code']
        self.set_in_session(promo_code)
        return http_response

    def get_success_url(self):
        return reverse('shopping-cart')

    def get_context_data(self, **kwargs):
        ctx = super(ShoppingCartView, self).get_context_data(**kwargs)
        objects = self.request.session.get('shopping_cart', [])
        ctx['objects'] = [get_object_or_404(Sale, pk=pk) for pk in objects]
        ctx['total_price'] = sum(sale.price for sale in ctx['objects'])
        promo_code = self.get_from_session()
        if promo_code:
            ctx['total_price'] -= promo_code.discount
        ctx['charges'] = ctx['total_price'] * Decimal('0.196')
        return ctx


class ShoppingCartRemoveView(RedirectView):
    permanent = False
    url = reverse_lazy('shopping-cart')

    def post(self, *args, **kwargs):
        remove_id = int(self.kwargs.get('sale_id'))
        objects = self.request.session.get('shopping_cart', [])
        for idx, sale_pk in enumerate(objects):
            if sale_pk == remove_id:
                del(objects[idx])
                self.request.session.save()
                break
        return super(ShoppingCartRemoveView, self).post(*args, **kwargs)


class DeliveryView(PromoCodeMixin, TemplateView):
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

        objects = self.request.session.get('shopping_cart', [])
        items = [get_object_or_404(Sale, pk=pk) for pk in objects]
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

    def _create_order(self, request, tos_form, billing_form, delivery_formset):
        """ Insert a new Order, and correspondings OrderSale entries. Return
        the order_id. """

        billing_address = billing_form.save()
        order = Order.helper_create_order(request.user, billing_address,
                                          promo_code=self.get_from_session())
        # Save partnership info
        PartnersSubscription(
            order=order,
            register=tos_form.cleaned_data.get('partners', False)).save()

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
            osale = OrderSale(order=order, sale=sale, delivery=delivery,
                              message=form.cleaned_data['message'])
            osale.save()
        return order.exposed_id

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


class PaymentView(PromoCodeMixin, TemplateView):
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
        promo_code = self.get_from_session()
        if promo_code:
            price -= promo_code.discount * 100
        ctx['form'] = forms.Be2billForm({
                        "CLIENTIDENT": order.billing.email,
                        "DESCRIPTION": "Les coffrets de Madame Aime",
                        "CLIENTEMAIL": order.billing.email,
                        "ORDERID": order.exposed_id,
                        "AMOUNT": int(price) })
        return ctx


class CheckoutOKClient(PromoCodeMixin, TemplateView):
    def dispatch(self, *args, **kwargs):
        ret = super(CheckoutOKClient, self).dispatch(*args, **kwargs)
        # Remove the promo code from session
        self.remove_from_session()
        return ret

    def get_template_names(self):
        try:
            PaymentForm.verify_hash(settings.BE2BILL_PASSWORD,
                                    self.request.GET)
        except:
            pass
        if self.request.GET.get('EXECCODE') in ('0000', '0001'):
            # empty shopping card
            self.request.session['shopping_cart'] = []
            return 'emarket/checkout-ok-client.html'
        return 'emarket/checkout-ko-client.html'

    def get_context_data(self, **kwargs):
        ctx = super(CheckoutOKClient, self).get_context_data(**kwargs)
        ctx['GET'] = self.request.GET

        exposed_id = self.request.GET.get('ORDERID')
        order = get_object_or_404(Order, exposed_id=exposed_id)
        ctx['order'] = order
        ctx['order_sales'] = OrderSale.objects.filter(order=order)
        ctx['total_price'] = order.get_total_price()
        return ctx


class Be2billNotifTransaction(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(Be2billNotifTransaction, self).dispatch(*args, **kwargs)

    def _save_transaction(self, request, params):
        try:
            PaymentForm.verify_hash(settings.BE2BILL_PASSWORD, params)
        except:
            return HttpResponse('bad hash')
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
        try:
            log_values['order'] = \
                    Order.objects.get(exposed_id=params.get('ORDERID'))
        except Order.DoesNotExist:
            return HttpResponse('no such order')
        try:
            Be2billTransaction(**log_values).save()
        except IntegrityError:
            return HttpResponse('order already processed')
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
