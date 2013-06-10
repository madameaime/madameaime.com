from django.db import models
from django.db.models import Count


class ValidPartnersSubscriptionManager(models.Manager):
    def get_query_set(self):
        return super(ValidPartnersSubscriptionManager, self) \
                    .get_query_set() \
                    .filter(register=True) \
                    .annotate(toto=Count('order__user__email')) \
                    .select_related('order', 'order__user')
