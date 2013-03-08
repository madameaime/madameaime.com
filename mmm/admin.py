from django.contrib import admin

from models import *


admin.site.register(ContactMessage)

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'date', 'active')

admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(OfferPage)
admin.site.register(OfferPageSale)
admin.site.register(PasswordRecovery)
