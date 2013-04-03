from django.contrib import admin

from models import *


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('date', 'firstname', 'lastname', 'email', 'command', 'subject')
    ordering = ['-date']
    search_fields = ('date', 'email', 'firstname', 'lastname', 'command')


admin.site.register(ContactMessage, ContactMessageAdmin)


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'date', 'active')

admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(OfferPage)
admin.site.register(OfferPageSale)
admin.site.register(PasswordRecovery)
