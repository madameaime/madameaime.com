# -*- coding: utf8 -*-
from datetime import datetime

from django import forms
from django.conf import settings
from django.forms.formsets import BaseFormSet

from be2bill import PaymentForm

from .models import Address, Order, PromoCode


class AddressModelForm(forms.ModelForm):
    """ Simple ModelForm for Address which excludes country because we're only
    ship our products to France.
    """
    class Meta:
        model = Address
        exclude = ('country',)

    def clean_zip_code(self):
        code = self.cleaned_data.get('zip_code')
        try:
            int(code)
        except ValueError:
            raise forms.ValidationError('Code invalide')
        if len(code) != 5:
            raise forms.ValidationError('Code invalide')
        return code


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

    sale_id = forms.IntegerField()

    delivery_place = forms.ChoiceField(widget=forms.RadioSelect,
                            choices=DELIVERY_PLACES_CHOICES)

    message = forms.CharField(widget=forms.widgets.Textarea, required=False)

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


class ToSForm(forms.Form):
    """ Checkboxes for terms of service and to subscribe for emails from our
    partners.
    """
    tos = forms.BooleanField()
    partners = forms.BooleanField(required=False)


class Be2billForm(forms.Form, PaymentForm):
    def __init__(self, fields, *args, **kwargs):
        # Default params
        defaults = {
            'IDENTIFIER': settings.BE2BILL_IDENTIFIER,
            '3DSECURE': 'no'
        }
        # be2bill.PaymentForm ctor
        PaymentForm.__init__(self,
                url=settings.BE2BILL_URL,
                fields=dict(list(defaults.items()) + list(fields.items())))
        # Get fields
        fields = self.get_fields(settings.BE2BILL_PASSWORD)
        # django.forms.Form ctor
        forms.Form.__init__(self, initial=fields, *args, **kwargs)
        # Create fields dynamically for this form
        for key in fields:
            self.fields[key] = forms.CharField()


class PromoCodeForm(forms.Form):
    code = forms.CharField(required=False)

    def __init__(self, user, shopping_cart, **kwargs):
        super(PromoCodeForm, self).__init__(**kwargs)
        self.user = user
        self.shopping_cart = shopping_cart
        # the code is not mandatory
        self.fields['code'].required = False

    def clean_code(self):
        """ The promo code is only valid if:
        - the code exists
        - it is valid (not expired)
        - if it is related to a sale, the client ordered this sale 
        - the client has not an order for this code
        """
        data = self.cleaned_data['code']
        if not data:
            return data
        # get the code
        try:
            promo_code = PromoCode.objects.get(code=data)
        except PromoCode.DoesNotExist:
            raise forms.ValidationError("Ce code n'existe pas")
        if Order.objects.filter(user=self.user.pk, promo_code=promo_code) \
                        .count():
            raise forms.ValidationError('Code déjà utilisé')
        if promo_code.expire and datetime.now() >= promo_code.expire:
            raise forms.ValidationError("Ce code est expiré")
        if promo_code.sale and promo_code.sale not in self.shopping_cart:
            raise forms.ValidationError('Code invalide')
        return data
