from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'card_number', 'expiry_date', 'cvv', 'paid_at')
    search_fields = ('name', 'card_number')
    list_filter = ('paid_at',)

admin.site.register(Payment, PaymentAdmin)

