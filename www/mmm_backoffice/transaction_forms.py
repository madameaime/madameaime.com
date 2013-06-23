# -*- coding: utf8 -*-

from django import forms

from emarket.models import Address, Sale


class TransactionCreationForm(forms.ModelForm):
    class Meta:
        model = Address

    def __init__(self, *args, **kwargs):
        super(TransactionCreationForm, self).__init__(*args, **kwargs)
        # number of extra fields
        nextra = 2
        # fields order: extra fields THEN model fields
        self.fields.keyOrder = (self.fields.keyOrder[-2:] +
                                self.fields.keyOrder[:-2])

    transaction_type = forms.ChoiceField(choices=[
        (0, 'Transaction gratuite'),
        (1, 'Transaction payée par chèque'),
    ])

    sale = forms.ModelChoiceField(queryset=Sale.objects.all(),
                                  empty_label=None)
