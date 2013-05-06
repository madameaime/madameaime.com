from datetime import datetime
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import (CreateView, FormView, RedirectView,
                                  TemplateView, DetailView, ListView)

from braces.views import LoginRequiredMixin
from django_xhtml2pdf.utils import render_to_pdf_response

import mailhelpers

from emarket.models import Be2billTransaction, Order
from forms import NewsletterForm, RecoverPasswordForm, RegistrationForm, UpdatePasswordForm
from models import ContactMessage, OfferPage, PasswordRecovery, User
import emarket


class AuthenticationView(FormView):
    template_name = 'auth.html'
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    success_url = reverse_lazy('homepage')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(AuthenticationView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AuthenticationView, self).get_context_data(**kwargs)
        context[self.redirect_field_name] = self.request.REQUEST.get(self.redirect_field_name, '')
        context['authentication_form'] = context['form']
        context['registration_form'] = RegistrationForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())

        if form.is_valid():
            redirect_to = request.REQUEST.get(self.redirect_field_name, '')

            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = self.get_success_url();

            login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return redirect(redirect_to)

        return self.form_invalid(form)


class RegistrationView(FormView):
    template_name = 'auth.html'
    redirect_field_name = REDIRECT_FIELD_NAME
    success_url = reverse_lazy('homepage')
    form_class = RegistrationForm

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        context[self.redirect_field_name] = self.request.REQUEST.get(self.redirect_field_name, '')
        context['registration_form'] = context['form']
        context['authentication_form'] = AuthenticationForm()
        return context

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(RegistrationView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())

        if form.is_valid():
            redirect_to = request.REQUEST.get(self.redirect_field_name, '')

            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = self.get_success_url();

            form.save()

            new_user = authenticate(
                username=request.POST.get('email'),
                password=request.POST.get('password')
            )
            login(request, new_user)

            return redirect(redirect_to)
        return self.form_invalid(form)


class ContactView(CreateView):
    template_name = 'contact.html'
    model = ContactMessage

    def get_success_url(self):
        return reverse('contact') + '?status=ok'

    def get_context_data(self, **kwargs):
        ctx = super(ContactView, self).get_context_data(**kwargs)
        if self.request.GET.get('status') == 'ok':
            ctx['success'] = True
        return ctx

    def form_valid(self, form):
        send_mail = mailhelpers.utils.send_mail
        send_mail('Nouveau message de contact sur madameaime.com',
                  ['contact@madameaime.com'],
                  'contact@madameaime.com',
                  'mmm/new_contact_message.txt',
                  'mmm/new_contact_message.html',
                  params={'data': form.cleaned_data})
        return super(ContactView, self).form_valid(form)


class OfferView(TemplateView):
    template_name = 'offer.html'

    def get_context_data(self, **kwargs):
        ctx = super(OfferView, self).get_context_data(**kwargs)

        offers = OfferPage.objects.filter(date_start__lte=datetime.now()) \
                                  .order_by('-date_start')                \
                                  .all()
        ctx['offers'] = offers[0] if offers else None
        return ctx


class NewsletterView(RedirectView):

    permanent = False
    url = reverse_lazy('homepage')

    def post(self, request, *args, **kwargs):
        """ Create the newsletter entry.
        Note that if there a duplicate entry, form.is_valid will return False
        so there's no need to catch an IntegrityError here.
        """
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
        return super(NewsletterView, self).get(request, *args, **kwargs)


class RecoverPasswordView(FormView):

    template_name = 'auth/recover_password_form.html'
    form_class = RecoverPasswordForm

    def get_context_data(self, **kwargs):
        ctx = super(RecoverPasswordView, self).get_context_data(**kwargs)
        if self.request.GET.get('status') == 'ok':
            ctx['status'] = 'ok'
        return ctx

    def get_success_url(self):
        return reverse('password.recover') + '?status=ok'

    def form_valid(self, form):
        mail = form.cleaned_data['email']
        ip = self.request.META['REMOTE_ADDR']

        user = User.objects.get(email=mail)
        model = PasswordRecovery(user=user,
                                 ip_addr=self.request.META['REMOTE_ADDR'])
        model.save()

        args = 'secret=%s&mail=%s' % (model.secret, mail)
        update_uri = reverse('password.update') + '?' + args
        absolute_update_uri = self.request.build_absolute_uri(update_uri)

        emarket.utils.send_mail(settings.FORGOT_PASSWORD_MAIL_SUBJECT,
            [mail], settings.FORGOT_PASSWORD_MAIL_FROM,
            'mmm/password_recovery_mail.txt',
            'mmm/password_recovery_mail.html',
            params={'recovery': model,
                    'update_uri': absolute_update_uri})
        return super(RecoverPasswordView, self).form_valid(form)


class UpdatePasswordView(FormView):

    form_class = UpdatePasswordForm
    template_name = 'auth/update_password_form.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        ctx = super(UpdatePasswordView, self).get_context_data(**kwargs)
        ctx['mail'] = self.request.GET.get('mail')
        ctx['secret'] = self.request.GET.get('secret')
        return ctx

    def get_form(self, form_class):
        post_data = None
        if self.request.method == 'POST':
            post_data = self.request.POST
        return form_class(self.request.GET.get('mail'),
                          self.request.GET.get('secret'),
                          post_data)


class AccountOrdersView(LoginRequiredMixin, ListView):
    template_name = 'account/orders.html'

    def get_queryset(self):
        orders = Order.objects.filter(user=self.request.user)
        return filter(lambda order: order.is_paid(), orders)


class LimitOrderViewMixin(LoginRequiredMixin):
    def dispatch(self, request, pk=None, *args, **kwargs):
        """ The details of an Order can only be seen by a user if he is logged,
        if the Order belongs to him and if it is a paid (or free) order. """
        order = get_object_or_404(Order, pk=pk)
        if order.user != request.user:
            raise Http404
        if not order.is_paid():
            raise Http404
        return super(LimitOrderViewMixin, self).dispatch(request, pk,
                                                         *args, **kwargs)


class OrderView(LimitOrderViewMixin, DetailView):
    template_name = "account/order.hml"
    model = emarket.models.Order


class OrderInvoicePdfView(LimitOrderViewMixin, DetailView):
    model = emarket.models.Order

    def get_context_data(self, **kwargs):
        ctx = super(OrderInvoicePdfView, self).get_context_data(**kwargs)
        order = self.object
        ordersales = order.ordersale_set.all()
        ctx['items'] = [
            {
             'product': ordersale.sale.product,
             'price_ht': (ordersale.sale.price -
                          ordersale.sale.price * Decimal('0.196'))
            }
            for ordersale in ordersales
        ]
        ctx['total_ttc'] = sum(ordersale.sale.price
                                for ordersale in ordersales)
        ctx['total_tva'] = sum(ordersale.sale.price
                                for ordersale in ordersales) * Decimal('0.196')
        ctx['total_ht'] = (ctx['total_ttc'] -
                            ctx['total_ttc'] * Decimal('0.196'))
        return ctx

    def render_to_response(self, context, **response_kwargs):
        response = render_to_pdf_response('account/pdf_invoice.html',
                                          context=context)
        return response
