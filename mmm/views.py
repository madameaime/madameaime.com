from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic import TemplateView


class RegistrationView(TemplateView):
    """
    It'd be better to use django.contrib.auth.forms.AuthenticationForm and
    UserCreationForm but there's no way to render something great with
    bootstrap.js easily.
    """

    template_name = 'registration.html'

    def get_context_data(self):
        ctx = super(RegistrationView, self).get_context_data()
        ctx['registration_form'] = UserCreationForm()
        #ctx['authentication_form'] = AuthenticationForm()
        return ctx
