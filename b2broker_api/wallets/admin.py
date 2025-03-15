from django.contrib import admin
from .models import Wallet, Transaction


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """Admin configuration for Wallet model"""
    list_display = ('id', 'label', 'get_balance')
    search_fields = ('label',)
    
    def get_balance(self, obj):
        return obj.balance
    get_balance.short_description = 'Balance'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin configuration for Transaction model"""
    list_display = ('id', 'wallet', 'txid', 'amount', 'created_at')
    list_filter = ('wallet', 'created_at')
    search_fields = ('txid',)
    readonly_fields = ('created_at',)
