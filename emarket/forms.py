from django import forms
from django.forms.formsets import BaseFormSet

from models import Address


class AddressModelForm(forms.ModelForm):
    """ Simple ModelForm for Address which excludes country because we're only
    ship our products to France.
    """
    class Meta:
        model = Address
        exclude = ('country',)


class BillingForm(AddressModelForm):
    def __init__(self, *args, **kwargs):
        """ Phone isn't required in the Address model but it is for the Billing
        form.
        """
        super(BillingForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required = True


class DeliveryForm(AddressModelForm):

    DELIVERY_PLACES_CHOICES = (
        ('0', 'deliver to billing'),
        ('1', 'deliver to custom'),
    )

    delivery_place = forms.ChoiceField(widget=forms.RadioSelect,
                            choices=DELIVERY_PLACES_CHOICES)

    def clean(self):
        """ UGLY HACK

        If the address where to deliver the object is the same than the billing
        one, fields are not required. Every field is overriden with a dummy
        value (x@x.xxx).

        Better way to achieve the same result could be:
        - mark all fields from DeliveryForm non-required
        - in every clean() method, raise forms.ValidationError if the field is
          empty and delivery_place is different than the billing address
        """
        cleaned_data = super(DeliveryForm, self).clean()
        delivery_place = cleaned_data.get('delivery_place')
        if delivery_place == '0':
            # Iterate over fields of AddressModelForm, and remove errors
            base = AddressModelForm()
            for field in base.fields:
                if field in self.errors:
                    # remove the error and replace the field value with dummy
                    del self.errors[field]
                    cleaned_data[field] = 'x@x.xxx'
        return cleaned_data


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
