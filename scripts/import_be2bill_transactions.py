#!/usr/bin/env python

"""
Import transactions exported from the be2bill extranet in database.
"""

import csv
import sys

from emarket.models import Be2billTransaction, Order


def parse(stream):
    lines = [line for line in csv.reader(stream, delimiter=';')]

    for line in lines[:0:-1]:
        (transactionid, orderid, operationtype, description, amount, currency,
         execcode, message, clientip, clientident, clientemail, clientreferrer,
         _3dsecure, date, language, version, refundedby, descriptor, refunded,
         refundtype, chargebackstatus, chargebackdate, alias, aliasmode,
         cardvaliditydate, cardfullname, cardtype, extradata, clientdob,
         clientaddress) = line

        order = Order.objects.get(exposed_id=orderid)

        transaction = Be2billTransaction(
                            order=order,
                            _3dsecure=_3dsecure,
                            alias=alias,
                            amount=amount,
                            cardfullname=cardfullname,
                            cardtype=cardtype,
                            cardvaliditydate=cardvaliditydate,
                            clientemail=clientemail,
                            clientident=clientident,
                            currency=currency,
                            descriptor=descriptor,
                            execcode=execcode,
                            extradata=extradata,
                            language=language,
                            message=message,
                            operationtype=operationtype,
                            transactionid=transactionid,
                            version=version)
        transaction.save()


def main():
    if len(sys.argv) != 2:
        print >> sys.stderr, 'Usage: %s export.csv' % sys.argv[0]
        sys.exit(1)
    parse(open(sys.argv[1]))


if __name__ == '__main__':
    main()
