from django.db.models import Q

from emarket.models import Be2billTransaction, OrderSale
from stockmgmt.models import Package


def reformat(value, format_type, format_len=0):
    if format_type == 'A':
        assert(format_len != 0)
        return ('%%-%ss' % format_len) % (value or '',)
    elif format_type == 'N':
        return '%012d' % (value or 0,)
    raise ValueError('Invalid format type %s' % format_type)


def get_product_file(products):
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
    for product in products:
        try:
            package = Package.objects.get(pk=product.pk)
            is_metapackage = False
            # iterate over package products. If one of them is a package, do
            # not add product to ret
            for package_product in package.products.all():
                if Package.objects.filter(pk=package_product.pk).count():
                    is_metapackage = True
                    break
            if is_metapackage:
                continue

        except Package.DoesNotExist:
            pass

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

def get_kits_file(products):
    """
    CODE_KIT    (A18)
    LIB_LONG    (A50)
    LIB_COURT   (A16)
    CODE_ART    (A18)
    QTE         (N)

    Only return kits that contain products which are not packages
    """
    ret = []
    for product in products:
        # if it is a package
        try:
            package = Package.objects.get(pk=product.pk)
        except Package.DoesNotExist:
            continue

        # this is a true package (no package inside it)
        true_package = True
        for element in package.products.all():
            if Package.objects.filter(pk=element.pk).count() != 0:
                true_package = False
                break
        if true_package is False:
            continue

        # yeah!
        for item in package.products.all():
            ret.append([
                reformat(product.pk, 'N'),
                reformat(product.name[:50], 'A', 50),
                reformat(product.name[:16], 'A', 16),
                reformat(item.pk, 'N'),
                reformat(1, 'N')
            ])
    return ret


def get_commands_file(transactions):
    """
    NUM_CMDE                (A30)
    NAT_CMDE                (A30)
    TYPE_CMDE               (A10)
    CODE_CLIENT             (A20)
    NUM_FACTURE_BL          (A20)
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
    for osale in OrderSale.objects \
                          .filter(Q(order__be2billtransaction__execcode=0) |
                                  Q(order__be2billtransaction__execcode=1)):
        trans = osale.order.be2billtransaction_set.all()[0]
        order = osale.order
        assert(order.billing.country.lower() == 'france')
        billing_iso_country = 'FR'

        # if no delivery address, take the billing address
        delivery = osale.delivery or order.billing
        assert(delivery.country.lower() == 'france')
        delivery_iso_country = 'FR'

        ret.append([
            reformat(order.pk, 'A', 30),
            reformat('', 'A', 30),
            reformat('BtoC', 'A', 10),
            reformat(order.user.pk, 'A', 20),
            reformat(trans.pk, 'A', 20),
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
