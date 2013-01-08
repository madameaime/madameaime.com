from django import forms


class ContactForm(forms.Form):

    last_name = forms.CharField()
    first_name = forms.CharField()
    email = forms.EmailField()
    order_number = forms.CharField(required = False)
    subject = forms.CharField()
    body = forms.CharField(widget = forms.Textarea({ 'rows': 5 }))
