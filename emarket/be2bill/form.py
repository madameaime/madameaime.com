from hashlib import sha256

from exceptions import ImproperlyConfigured, ValidationError


class FormMixin(object):

    url = None

    fields = {
        'VERSION': '2.0'
    }

    required_fields = None
    optional_felds = None

    def __init__(self, fields=None, **kwargs):
        """ Update self.fields and, for every <key> of kwargs, set
        self.<key> = kwarg[key]
        """
        if fields:
            self.fields.update(fields)

        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def get_url(self):
        if self.url is None:
            raise ImproperlyConfigured(
                "be2bill FormMixin requires either a definition of "
                "'url' or an implementation of 'get_url'")
        return self.url

    def make_hash(self, b2b_passwd):
        clear = b2b_passwd
        clear += ''.join('%(key)s=%(value)s%(password)s' % {
                            'key': key,
                            'value': self.fields[key],
                            'password': b2b_passwd
                        } for key in sorted(self.fields))
        return sha256(clear).hexdigest()

    def get_fields(self, b2b_passwd):
        if not self.is_valid():
            return None
        hash_field = ('HASH', self.make_hash(b2b_passwd))
        return dict(self.fields.items() + [hash_field])

    def is_valid(self):
        """ Ensure that fields all required fields are present, and there's no
        extra invalid fields.
        """
        missing_required = set(self.required_fields) - set(self.fields)
        if len(missing_required) != 0:
            raise ValidationError("Missing required fields: %s" %
                                  ', '.join(missing_required))

        extra_fields = (set(self.fields)
                      - set(self.required_fields) - set(self.optional_fields))
        if len(extra_fields) != 0:
            raise ValidationError("Extra invalid fields: %s" %
                                  ', '.join(extra_fields))
        return True


class PaymentForm(FormMixin):

    required_fields = (
        'IDENTIFIER', 'OPERATIONTYPE', 'CLIENTIDENT', 'DESCRIPTION', 'ORDERID',
        'VERSION', 'AMOUNT'
    )

    optional_fields = (
        'CARDTYPE', 'CLIENTEMAIL', 'CARDFULLNAME', 'LANGUAGE', 'EXTRADATA',
        'CLIENTDOB', 'CLIENTADDRESS', 'CREATEALIAS', '3DSECURE',
        '3DSECUREDISPLAYMODE', 'USETEMPLATE', 'HIDECLIENTEMAIL',
        'HIDECARDFULLNAME'
    )

    def __init__(self, fields=None, **kwargs):
        """ If OPERATIONTYPE is not in fields, set its default value to PAYMENT
        and call the parent __init__ method.
        """
        if fields is None:
            fields = {}
        fields.setdefault('OPERATIONTYPE', 'PAYMENT')
        super(PaymentForm, self).__init__(fields=fields,
                required_fields=self.required_fields,
                optional_fields=self.optional_fields, **kwargs)


class AuthorizationForm(FormMixin):
    """ Not yet implemented
    """
    pass


if __name__ == '__main__':
    url = 'https://secure-test.be2bill.com/front/form/process.php'
    identifier = '1R2Box'
    b2b_password = 'W%ZIlle@WK$ZO>J9'
    form = PaymentForm(url=url,
            fields={
                "IDENTIFIER": identifier,
                "3DSECURE": "no",
                "CLIENTIDENT": "toto@gmail.com",
                "DESCRIPTION": "Les coffrets de Madame Aime",
                "CLIENTEMAIL": "toto@gmail.com",
                "ORDERID": "3AI72572QS4L3B4R",
                "AMOUNT": "4980",
            })
    print form.get_fields(b2b_password)
