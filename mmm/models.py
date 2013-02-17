from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

import emarket.models

class UserManager(BaseUserManager):
    """
    Custom UserManager to deal with the custom User class
    """

    def create_user(self, email=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = UserManager.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=False,
            is_active=True,
            is_superuser=False,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that uses an email as username
    """
    def __unicode__(self):
        return self.email;

    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class OfferPageSale(models.Model):
    """
    Product exposed on the offer page.
    """
    def __unicode__(self):
        return self.sale.product.name

    sale = models.ForeignKey(emarket.models.Sale)
    title = models.CharField(max_length=64, null=True, blank=True, default=None)
    subtitle = models.CharField(max_length=64, null=True, blank=True, default=None)
    content = models.TextField(null=True, blank=True, default=None)
    price_comment = models.CharField(max_length=64)


class OfferPage(models.Model):
    """
    Configuration of the three products shown on the offer page, displayed
    since date_start.
    """
    def __unicode__(self):
        return self.date_start.strftime('%Y/%m/%d %H:%M:%S')

    date_start = models.DateTimeField(default=timezone.now)

    sale_1 = models.ForeignKey(OfferPageSale, related_name='sale_1')
    sale_2 = models.ForeignKey(OfferPageSale, related_name='sale_2')
    sale_3 = models.ForeignKey(OfferPageSale, related_name='sale_3')

    hurry_text = models.TextField(null=True, blank=True, default=None)


class Newsletter(models.Model):
    date = models.DateTimeField(default=timezone.now)
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=True)
