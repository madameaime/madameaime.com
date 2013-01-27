from django import forms
from django.forms.formsets import BaseFormSet

from models import Address


class BillingForm(forms.ModelForm):
    class Meta:
        """ This is supposed to be a generic application but on our website,
        we only send products to France. Exclude country from the form.
        """
        model = Address
        exclude = ('country',)

    def __init__(self, *args, **kwargs):
        """ Phone isn't required in the Address model but it is for the Billing
        form.
        """
        super(BillingForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required = True


class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('country',)

    DELIVERY_PLACES_CHOICES = (
        ('0', 'deliver to billing'),
        ('1', 'deliver to custom'),
    )

    delivery_place = forms.ChoiceField(widget=forms.RadioSelect,
                            choices=DELIVERY_PLACES_CHOICES)


class RequiredFormset(BaseFormSet):
    """ By default, every form of a formset is valid if all of its fields are
    empty. This class changes that behaviour.

    Note that this class should probably resides in a more appropriate file
    (ie. excluded from this app) as it is generic.
    """
    def __init__(self, *args, **kwargs):
        super(RequiredFormset, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


class ToSForm(forms.Form):
    """ Checkboxes for terms of service and to subscribe for emails from our
    partners.
    """
    tos = forms.BooleanField()
    partners = forms.BooleanField(required=False)
