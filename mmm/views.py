from django.views.generic import TemplateView

from forms import RegistrationForm


class RegistrationView(TemplateView):
    """
    It'd be better to use django.contrib.auth.forms.AuthenticationForm and
    UserCreationForm but there's no way to render something great with
    bootstrap.js easily.
    """
    template_name = 'registration.html'

    def post(self, request):
        if 'register' in request.POST:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                # handle and redirect
                pass
            # error, affect errors and return
            return super(RegistrationView, self).get(
                            request, registration_errors=form.errors)

        elif 'auth' in request.POST:
            pass

        # here, raise an error 400 bad request
