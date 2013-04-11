from datetime import datetime

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, FormView, RedirectView, TemplateView, DetailView

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


class OrderView(DetailView):
    template_name = "account/order.hml"
    model = emarket.models.Order
