from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Wallet, Transaction
from .serializers import WalletSerializer, WalletDetailSerializer, TransactionSerializer
from .filters import WalletFilter, TransactionFilter


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class WalletViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows wallets to be viewed or edited.
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = WalletFilter
    ordering_fields = ['id', 'label']

    def get_serializer_class(self):
        """
        Return the detail serializer for retrieve action
        """
        if self.action == 'retrieve':
            return WalletDetailSerializer
        return self.serializer_class


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transactions to be viewed or edited.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TransactionFilter
    ordering_fields = ['id', 'created_at', 'amount']
