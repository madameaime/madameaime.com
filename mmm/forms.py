from django import forms


class RegistrationForm(forms.Form):

    username  = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    def clean(self):
        #from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
        # check also if username is valid (ie. if it's a valid email addr)
        # and not already used
        cleaned_data = super(RegistrationForm, self).clean()
        if cleaned_data.get('password1') == cleaned_data.get('password2'):
            return cleaned_data
        raise forms.ValidationError('Les mots de passe doivent correspondre')


class AuthenticationForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField()

    def clean(self):
        # Here, check if username (or email) / password are ok
        return super(AuthenticationForm).clean()

class ContactForm(forms.Form):

    last_name = forms.CharField()
    first_name = forms.CharField()
    email = forms.EmailField()
    order_number = forms.CharField(required = False)
    subject = forms.CharField()
    body = forms.CharField(widget = forms.Textarea({ 'rows': 5 }))
