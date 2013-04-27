from django.db.models import Q

from emarket.models import Be2billTransaction, DeliveredProduct, OrderSale
from stockmgmt.models import Package, Product


def reformat(value, format_type, format_len=0):
    if format_type == 'A':
        assert(format_len != 0)
        return ('%%-%ss' % format_len) % (value or '',)
    elif format_type == 'N':
        return '%012d' % (value or 0,)
    raise ValueError('Invalid format type %s' % format_type)


def get_metapackages_list():
    """ Return Packages that are metapackages.

    A metapackage is a packages which contains at least one product which is
    itself a Package.
    A non-metapackage is a Package that contains only real Products.
    """
    return set(Package.objects.filter(
            products__in=Package.objects.values_list('pk', flat=True)
    ).values_list('pk', flat=True))


def get_products_file():
    """ return
    CODE                    (A18)
    LIB_LONG                (A50)
    LIB_COURT               (A16)
    TYPE_ART                (A3)
    ART_PHYSIQUE            (A1)
    FAMILLE                 (A30)
    LONGUEUR                (N)
    LARGEUR                 (N)
    HAUTEUR                 (N)
    POIDS                   (N)
    EAN                     (A32)
    VAL_DECLAREE            (A15)
    FLAG_PART_SEUL          (A1)
    CODE_ART_SUBSTITUTION   (A18)

    Do not return products that are packages and that contain packages
    """
    ret = []
    metapackages = get_metapackages_list()
    for product in Product.objects.all().select_related('product_type'):
        # If this product is a metapackage, do not add it to the ret list
        if product.pk in metapackages:
            continue

        product_type = ''
        if product.product_type is not None:
            product_type = product.product_type.shortcode

        ret.append([
            reformat(product.pk, 'A', 18),
            reformat(product.name[:50], 'A', 50),
            reformat('', 'A', 16), # shortname
            reformat(product_type, 'A', 3),
            'O',
            reformat(product.article_family[:30], 'A', 30),
            reformat(product.length, 'N'),
            reformat(product.width, 'N'),
            reformat(product.height, 'N'),
            reformat(product.weight, 'N'),
            reformat(product.ean[:32], 'A', 32),
            reformat(product.public_price, 'A', 15),
            'N',
            reformat('', 'A', 18),
        ])
    return ret

def get_kits_file():
    """
    CODE_KIT    (A18)
    LIB_LONG    (A50)
    LIB_COURT   (A16)
    CODE_ART    (A18)
    QTE         (N)

    Only return kits that contain products which are not packages
    """
    ret = []
    metapackages = get_metapackages_list()
    for package in Package.objects.all().prefetch_related('products'):
        if package.pk in metapackages:
            continue
        for product in package.products.all():
            ret.append([
                reformat(package.pk, 'A', 18),
                reformat(package.name[:50], 'A', 50),
                reformat(package.name[:16], 'A', 16),
                reformat(product.pk, 'A', 18),
                reformat(1, 'N')
            ])
    return ret

def get_non_delivered_ordersales():
    """ Get all non-delivered ordersales corresponding to valid transactions
    (paid or free offers).

    Return a dictionary where keys are OrderSale objects, and values are lists
    of Product to deliver.
    """
    # build a dictionary of latest transactions like :
    # {'order_pk': last_be2bill_transaction, ...}
    all_transactions = Be2billTransaction.objects \
                            .filter(Q(order__be2billtransaction__execcode=0) |
                                    Q(order__be2billtransaction__execcode=1))\
                            .order_by('-date_insert', '-pk') \
                            .prefetch_related('order')
    latest_transactions = {}
    for transaction in all_transactions:
        if transaction.order.pk not in latest_transactions:
            latest_transactions[transaction.order.pk] = transaction
   
    # Generate a list of metapackages
    metapackages = get_metapackages_list()
    # And a dict of packages
    packages = dict((package.pk, package)
                    for package in Package.objects.all())

    # Build a dict of delivered products
    # {order_sale: [product1, product2, product3], ...}
    data = DeliveredProduct.objects.values_list('order_sale', 'product')
    delivered = {}
    for osale_pk, product_pk in data:
        delivered.setdefault(osale_pk, []).append(product_pk)

    product_is_delivered = lambda osale, product: \
                                    product in delivered.get(osale, [])

    # get non delivered ordersales
    valid = {}
    # select related. This will cause problem someday (the query generated is
    # huge and someday MySQL won't like such a big query) but let's try to keep
    # it this way for now.
    for order_sale in OrderSale.objects.all()    \
                               .select_related('order', 'sale',
                                       'order__user', 'order__billing',
                                       'sale__product',
                                       'delivery'):
        # If free transaction or paid transaction
        transaction = latest_transactions.get(order_sale.order.pk)
        if order_sale.order.is_free or (transaction is not None and
                transaction.operationtype == 'payment'
        ):
            products_to_deliver = []
            product = order_sale.sale.product

            # The Product related to the OrderSale is not a metapackage and is
            # deliverable
            if product.pk not in metapackages:
                if (product.deliverable is True and
                    not product_is_delivered(order_sale.pk, product.pk)):
                    products_to_deliver.append(product)
            # If it is a metapackage, iterate over products in it to know which
            # one we need to deliver
            else:
                package = packages[product.pk]
                for product in package.products.all():
                    if (product.deliverable is True and
                        not product_is_delivered(order_sale.pk, product.pk)):
                        products_to_deliver.append(product)

            if products_to_deliver:
                valid[order_sale] = products_to_deliver

    return valid


def get_commands_file():
    """
    NUM_CMDE                (A30)
    NAT_CMDE                (A30)
    TYPE_CMDE               (A10)
    CODE_CLIENT             (A20)

    DATE_EDITION            (A8)
    NUMIC                   (A20)
    SOCIETE_FAC             (A50)
    CIVILITE_FAC            (A20)
    NOM_CLIENT_FAC          (A40)
    ADR1_FAC                (A38)
    ADR2_FAC                (A38)
    ADR3_FAC                (A38)
    ADR4_FAC                (A38)
    CP_FAC                  (A10)
    VILLE_FAC               (A38)
    ETAT_FAC                (A38)
    PAYS_FAC                (A38)
    CODE_ISO_FAC            (A2)
    SOCIETE_LIV             (A50)
    CIVILITE_LIV            (A20)
    NOM_CLIENT_LIV          (A50)
    ADR1_LIV                (A38)
    ADR2_LIV                (A38)
    ADR3_LIV                (A38)
    ADR4_LIV                (A38)
    CP_LIV                  (A10)
    VILLE_LIV               (A38)
    ETAT_LIV                (A38)
    PAYS_LIV                (A38)
    CODE_ISO_LIV            (A2)
    TELEPHONE_LIV           (A20)
    EMAIL_LIV               (A50)
    TYPE_ENVOI              (A2)
    CODE_TRANSPORTEUR_DEDIE (A30)
    NUMERO_POINT_RELAIS     (A10)
    CODE_ISO_POINT_RELAIS   (A2)
    TAUX_TVA_1              (A10)
    BASE_TVA_1              (A15)
    MONTANT_TVA_1           (A15)
    TAUX_TVA_2              (A10)
    BASE_TVA_2              (A15)
    MONTANT_TVA_2           (A15)
    TAUX_TVA_3              (A10)
    BASE_TVA_3              (A15)
    MONTANT_TVA_3           (A15)
    MONTANT_ESCOMPTE        (A15)
    MONTANT_ACOMPTE         (A15)
    MONTANT_FRAIS_ENVOI_HT  (A15)
    MONTANT_FRAIS_ENVOI_TTC (A15)
    MONTANT_TOTAL_HT        (A15)
    MONTANT_TOTAL_TTC       (A15)
    DATE_ECHEANCE           (A8)
    MODE_PAIEMENT           (A30)
    MONTANT_PAIEMENT        (A15)
    RESTANT_DU              (A15)
    DEVISE                  (A20)
    TYPE_FACTURE            (A1)
    COMMENTAIRE_1_COMMANDE  (A50)
    COMMENTAIRE_2_COMMANDE  (A50)
    COMMENTAIRE_3_COMMANDE  (A50)
    CADEAU                  (A1)
    """
    ret = []

    # iterate over OrderSales that have a valid related Be2BillTransaction
    for osale, products in get_non_delivered_ordersales().iteritems():
        order = osale.order
        if not order.billing.country:
            order.billing.country = 'France'
            order.billing.save()
        assert(order.billing.country.lower() == 'france')
        billing_iso_country = 'FR'

        # if no delivery address, take the billing address
        delivery = osale.delivery or order.billing
        if not delivery.country:
            delivery.country = 'France'
            delivery.save()
        assert(delivery.country.lower() == 'france')
        delivery_iso_country = 'FR'

        ret.append([
            reformat(order.pk, 'A', 30),
            reformat('', 'A', 30),
            reformat('BtoC', 'A', 10),
            reformat(order.user.pk, 'A', 20),
            reformat(osale.pk, 'A', 20),
            reformat(order.date.strftime('%Y%m%d'), 'A', 8),
            reformat('', 'A', 20), # NUMIC
            reformat('', 'A', 50), # SOCIETE FAC
            reformat('', 'A', 20), # CIVILITE FAC

            reformat(order.billing.lastname, 'A', 50),
            reformat(order.billing.firstname, 'A', 40),
            reformat(order.billing.address[:38], 'A', 38),
            reformat(order.billing.address[38:], 'A', 38),
            reformat(order.billing.additional[:38], 'A', 38),
            reformat(order.billing.additional[38:], 'A', 38),
            reformat(order.billing.zip_code, 'A', 10),
            reformat(order.billing.city, 'A', 10),
            reformat('', 'A', 38), # ETAT_FAC
            reformat(order.billing.country, 'A', 38),
            reformat(billing_iso_country, 'A', 2),

            reformat('', 'A', 50), # SOCIETE_LIV
            reformat('', 'A', 20), # CIVILITE_LIV
            reformat(delivery.lastname, 'A', 50),
            reformat(delivery.firstname, 'A', 40),
            reformat(delivery.address[:38], 'A', 38),
            reformat(delivery.address[38:], 'A', 38),
            reformat(delivery.additional[:38], 'A', 38),
            reformat(delivery.additional[38:], 'A', 38),
            reformat(delivery.zip_code, 'A', 10),
            reformat(delivery.city, 'A', 10),
            reformat('', 'A', 38), # ETAT_LIV
            reformat(delivery.country, 'A', 38),
            reformat(delivery_iso_country, 'A', 2),
            reformat(delivery.phone, 'A', 20),
            reformat(delivery.email, 'A', 50),

            reformat('', 'A', 2), # TYPE_ENVOI
            reformat('', 'A', 30), # CODE_TRANSPORTEUR_DEDIE
            reformat('', 'A', 10), # NUMERO_POINT_RELAIS
            reformat('', 'A', 2), # CODE_ISO_POINT_RELAIS

            reformat('', 'A', 10), # TAUX_TVA_1
            reformat('', 'A', 15), # BASE_TVA_1
            reformat('', 'A', 15), # MONTANT_TVA_1
            reformat('', 'A', 10), # TAUX_TVA_2
            reformat('', 'A', 15), # BASE_TVA_2
            reformat('', 'A', 15), # MONTANT_TVA_2
            reformat('', 'A', 10), # TAUX_TVA_3
            reformat('', 'A', 15), # BASE_TVA_3
            reformat('', 'A', 15), # MONTANT_TVA_3
            reformat('', 'A', 15), # MONTANT_ESCOMPTE
            reformat('', 'A', 15), # MONTANT_ACOMPTE
            reformat('', 'A', 15), # MONTANT_FRAIS_ENVOI_HT
            reformat('', 'A', 15), # MONTANT_FRAIS_ENVOI_TTC
            reformat('', 'A', 15), # MONTANT_TOTAL_HT
            reformat(osale.sale.price, 'A', 15), # MONTANT_TOTAL_TTC
            reformat('', 'A', 8), # DATE_ECHEANCE
            reformat('', 'A', 8), # MODE_PAIEMENT
            reformat(order.date.strftime('%Y%m%d'), 'A', 8), # DATE_PAIEMENT
            reformat(osale.sale.price, 'A', 15), # MONTANT_PAIEMENT
            reformat('', 'A', 15), # RESTANT_DU
            reformat('Euros', 'A', 20), # DEVISE
            reformat('B', 'A', 1), # TYPE_FACTURE (Facture (F) ou BL (B))

            reformat('', 'A', 50), # COMMENTAIRE 1
            reformat('', 'A', 50), # COMMENTAIRE 2
            reformat('', 'A', 50), # COMMENTAIRE 3

            reformat(int(order.billing != delivery), 'A', 1), # CADEAU, true if delivery addr != billing addr
        ])

    return ret


def get_detailed_commands_file():
    """
    NUM_FACTURE_BL
    CODE_ART
    LIBELLE_ART
    QTE
    OBLIGATOIRE
    PRIX_UNITAIRE_HT
    TAUX_TVA
    REMISE
    TAUX_REMISE
    MONTANT_TOTAL_LIGNE_HT
    """
    ret = []
    for osale, products in get_non_delivered_ordersales().iteritems():
        for product in products:
            order = osale.order
            ret.append([osale, product,         
                [
                    reformat(osale.pk, 'A', 20),
                    reformat(product.pk, 'A', 18),
                    reformat(product.name, 'A', 50),
                    reformat(1, 'N'), # QTE
                    reformat('O', 'A', 1), # OBLIGATOIRE
                    reformat('0', 'A', 15), # PRIX_UNITAIRE_HT
                    reformat('0', 'A', 10), # TAUX TVA
                    reformat('0', 'A', 15), # REMISE
                    reformat('0', 'A', 10), # TAUX REMISE
                    reformat('0', 'A', 15), # MONTANT_TOTAL_LIGNE_HT
                ]
            ])
    return ret
