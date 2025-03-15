import django_filters
from .models import Wallet, Transaction


class WalletFilter(django_filters.FilterSet):
    """
    Filter for Wallet model.
    Allows filtering by label.
    """
    label = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Wallet
        fields = ['label']


class TransactionFilter(django_filters.FilterSet):
    """
    Filter for Transaction model.
    Allows filtering by wallet_id, txid, and amount range.
    """
    txid = django_filters.CharFilter(lookup_expr='icontains')
    min_amount = django_filters.NumberFilter(
        field_name='amount', lookup_expr='gte'
    )
    max_amount = django_filters.NumberFilter(
        field_name='amount', lookup_expr='lte'
    )

    class Meta:
        model = Transaction
        fields = ['wallet', 'txid', 'min_amount', 'max_amount']
