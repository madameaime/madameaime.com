from django import forms

from .models import PasswordRecovery, User
import models


class RegistrationForm(forms.ModelForm):
    password_repeat = forms.CharField(widget = forms.PasswordInput)

    def clean_password_repeat(self):
        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')

        if password and password_repeat and password != password_repeat:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data

    def save(self):
        return models.User.objects.create_user(
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password')
        )

    class Meta:
        model = models.User
        fields = ('email', 'password')

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = models.Newsletter
        exclude = ('date', 'active')


class RecoverPasswordForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        cleaned_data = self.cleaned_data
        if User.objects.filter(email=cleaned_data.get('email')).count() != 1:
            raise forms.ValidationError('unknown email')
        return cleaned_data['email']


class UpdatePasswordForm(forms.Form):

    password = forms.CharField(widget=forms.PasswordInput())
    confirm = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, mail, secret, *args, **kwargs):
        self.mail = mail
        self.secret = secret
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)

    def clean_confirm(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('password') != cleaned_data.get('confirm'):
            raise forms.ValidationError('confirm and password must match')
        return cleaned_data['confirm']

    def clean(self):
        try:
            user = User.objects.get(email=self.mail)
        except User.DoesNotExist:
            raise forms.ValidationError('invalid user')

        # Get the last 10 items from PasswordRecovery (to avoid that someone
        # asks for 1000000 new passwords and tries to bruteforce)
        recover = PasswordRecovery.objects.filter(user=user).order_by('-date')
        for entry in recover:
            if entry.secret == self.secret:
                # update password
                user.set_password(self.cleaned_data['password'])
                user.save()
                # remove
                PasswordRecovery.objects.filter(user=user).delete()
                return self.cleaned_data
        raise forms.ValidationError('invalid mail or secret')
