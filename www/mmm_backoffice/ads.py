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
    """
    ret = []
    for product in products:
        try:
            Package.objects.get(pk=product.pk)
            continue
        except Package.DoesNotExist:
            pass

        product_type = ''
        if product.product_type is not None:
            product_type = product.product_type.shortcode

        ret.append([
            reformat(product.pk, 'A', 18),
            reformat(product.name[:50], 'A', 50),
            reformat(product.name[:16], 'A', 50),
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
