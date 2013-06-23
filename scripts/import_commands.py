#!/usr/bin/env python

import json
import sys

from django.contrib.auth import get_user_model
from django.forms.formsets import formset_factory

import xlrd

import emarket.forms
import emarket.models
import emarket.views


def get_default_user():
    user, created = get_user_model().objects.get_or_create(
                            email='team@madameaime.com')
    return user


def insert_info(sale_id, firstname, lastname, email, address, additional,
                zip_code, city, phone, country):

    tos_form = emarket.forms.ToSForm({'promo_code': '',
                                      'tos': True,
                                      'partners': False})
    billing_form = emarket.forms.AddressModelForm({
        'firstname': firstname,
        'lastname': lastname,
        'email': email,
        'address': address,
        'additional': additional,
        'zip_code': zip_code,
        'city': city,
        'phone': phone,
        'country': country
    })
    DeliveryFormset = formset_factory(emarket.forms.DeliveryForm)
    delivery_formset = DeliveryFormset({
            'form-TOTAL_FORMS': u'1',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'',
            'form-0-sale_id': sale_id,
            'form-0-delivery_place': '0',
        })

    if not (tos_form.is_valid() and billing_form.is_valid() and
            delivery_formset.is_valid()):
        raise ValueError('ERROR! INVALID FORMS!111!')

    class Request(object):
        """ Simulate a HttpRequest object. Worst hack ever (it's 00.30am here).
        """
        user = get_default_user()

    order_id = emarket.views.DeliveryView()._create_order(Request(),
                                    tos_form, billing_form, delivery_formset)
    order = emarket.models.Order.objects.get(exposed_id=order_id)
    order.is_free = True
    order.save()


def get_cell(worksheet, row, cell):
    return (worksheet.cell_type(row, cell), worksheet.cell_value(row, cell))


def main():
    if len(sys.argv) != 2:
        print >> sys.stderr, 'Usage: %s commands.xlsx' % sys.argv[0]
        sys.exit(1)

    workbook = xlrd.open_workbook(sys.argv[1])
    worksheet = workbook.sheet_by_index(0)
    nrows = worksheet.nrows
    for i in xrange(1, nrows):
        row = worksheet.row(i)
        data = []
        for j in xrange(worksheet.ncols):
            cell_type, cell_value = get_cell(worksheet, i, j)
            data.append(cell_value)
        data[0] = int(data[0]) # fix sale_id type
        # fix zip_code type, always on 5 chars
        zip_code = int(data[6])
        zip_code = ((5 - len(str(zip_code))) * '0') + str(zip_code)
        data[6] = zip_code
        insert_info(*data)

if __name__ == '__main__':
    main()
