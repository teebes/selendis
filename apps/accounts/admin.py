from django.contrib import admin
from stark.apps.accounts.models import EmailConfirmation

class EmailConfirmationAdmin(admin.ModelAdmin): pass

admin.site.register(EmailConfirmation, EmailConfirmationAdmin)