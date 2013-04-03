from hashlib import sha256

from .exceptions import (ImproperlyConfigured, HashValidationError,
                         ValidationError)


class FormMixin(object):

    # Be2bill URL where to redirect the user
    url = None

    # current version
    fields = {'VERSION': '2.0'}

    required_fields = None
    optional_felds = None

    def __init__(self, fields=None, **kwargs):
        if fields:
            self.fields.update(fields)

        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def get_url(self):
        """ Instead of directly setting the url, it might be useful to compute
        it dynamically. For instance, if the URI is test.domain.com we could
        redirect to the test extranet, otherwise to the production extranet.
        """
        if self.url is None:
            raise ImproperlyConfigured(
                "be2bill FormMixin requires either a definition of "
                "'url' or an implementation of 'get_url'")
        return self.url

    @staticmethod
    def _compute_fields_hash(b2b_passwd, fields):
        """ Internal function return the Be2bill hash from fields.

        The hash is the sha256 of the clear string
            PASSWD + (KEY + '=' + VALUE) + PASSWD

        where PASSWD is the private password provided by Be2bill, and KEY/VALUE
        are the values to sign (key 'HASH' excluded)
        """
        clear = b2b_passwd
        clear += ''.join('%(key)s=%(value)s%(password)s' % {
                            'key': key,
                            'value': fields[key],
                            'password': b2b_passwd
                        } for key in sorted(fields)
                           if key != 'HASH')
        return sha256(clear.encode('utf8')).hexdigest()

    def make_hash(self, b2b_passwd):
        """ Compute the Be2bill hash from form fields
        """
        return self._compute_fields_hash(b2b_passwd, self.fields)

    @staticmethod
    def verify_hash(b2b_passwd, fields, hash=None):
        """ Compute the Be2bill hash from fields, and ensure that it is equal
        to `hash` or, if None, to `fields['HASH']`.

        If not equal, raise exceptions.HashValidationError
        """
        verified = FormMixin._compute_fields_hash(b2b_passwd, fields)
        if (hash or fields['HASH']) != verified:
            raise HashValidationError('Invalid hash for these fields')

    def ensure_fields_validation(self):
        """ Ensure that fields all required fields are present and there's no
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

    def get_fields(self, b2b_passwd):
        """ Return all fields set in ctor, ensure they are valid (no missing
        required field or no extra field), compute the Be2bill hash and return
        fields to display in a form.

        Raise exceptions.ValidationError if missing/extra fields.
        """
        self.ensure_fields_validation()
        hash_field = ('HASH', self.make_hash(b2b_passwd))
        return dict(self.fields.items() + [hash_field])


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
        """ Set the default value for OPERATIONTYPE to PAYMENT and initialize
        required and optional fields.
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
