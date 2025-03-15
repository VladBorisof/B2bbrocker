from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Wallet, Transaction


class WalletModelTests(TestCase):
    """Test cases for the Wallet model"""

    def test_wallet_balance_calculation(self):
        """Test that wallet balance is calculated correctly"""
        wallet = Wallet.objects.create(label="Test Wallet")

        # Create some transactions
        Transaction.objects.create(
            wallet=wallet, txid="tx1", amount=Decimal("100.5")
        )
        Transaction.objects.create(
            wallet=wallet, txid="tx2", amount=Decimal("50.25")
        )
        Transaction.objects.create(
            wallet=wallet, txid="tx3", amount=Decimal("-30.75")
        )

        # Check balance calculation
        self.assertEqual(wallet.balance, Decimal("120"))


class TransactionModelTests(TestCase):
    """Test cases for the Transaction model"""

    def test_negative_balance_prevention(self):
        """Test that transactions cannot make wallet balance negative"""
        wallet = Wallet.objects.create(label="Test Wallet")

        # Add initial funds
        Transaction.objects.create(
            wallet=wallet, txid="tx1", amount=Decimal("100")
        )

        # Try to withdraw more than the balance
        with self.assertRaises(ValidationError):
            Transaction.objects.create(
                wallet=wallet, txid="tx2", amount=Decimal("-150")
            )

        # Balance should remain unchanged
        self.assertEqual(wallet.balance, Decimal("100"))

        # Valid withdrawal should work
        Transaction.objects.create(
            wallet=wallet, txid="tx3", amount=Decimal("-50")
        )
        self.assertEqual(wallet.balance, Decimal("50"))


class WalletAPITests(APITestCase):
    """Test cases for the Wallet API endpoints"""

    def setUp(self):
        """Set up test data"""
        self.wallet1 = Wallet.objects.create(label="Wallet 1")
        self.wallet2 = Wallet.objects.create(label="Wallet 2")

        # Add transactions to wallet1
        Transaction.objects.create(
            wallet=self.wallet1, txid="tx1", amount=Decimal("100")
        )
        Transaction.objects.create(
            wallet=self.wallet1, txid="tx2", amount=Decimal("50")
        )

    def test_list_wallets(self):
        """Test retrieving a list of wallets"""
        url = reverse('wallet-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

        # Check that balance is included
        self.assertEqual(Decimal(response.data['results'][0]['balance']), Decimal("150"))
        self.assertEqual(Decimal(response.data['results'][1]['balance']), Decimal("0"))

    def test_create_wallet(self):
        """Test creating a new wallet"""
        url = reverse('wallet-list')
        data = {'label': 'New Wallet'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wallet.objects.count(), 3)

        # Get the newly created wallet from the response data
        new_wallet_id = response.data['id']
        new_wallet = Wallet.objects.get(id=new_wallet_id)
        self.assertEqual(new_wallet.label, 'New Wallet')


class TransactionAPITests(APITestCase):
    """Test cases for the Transaction API endpoints"""

    def setUp(self):
        """Set up test data"""
        self.wallet = Wallet.objects.create(label="Test Wallet")
        self.transaction = Transaction.objects.create(
            wallet=self.wallet,
            txid="tx1",
            amount=Decimal("100")
        )

    def test_create_transaction(self):
        """Test creating a new transaction"""
        url = reverse('transaction-list')
        data = {
            'wallet': self.wallet.id,
            'txid': 'tx2',
            'amount': '50.5'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 2)

        # Check wallet balance is updated
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal("150.5"))

    def test_prevent_negative_balance(self):
        """Test that API prevents transactions that would make balance negative"""
        url = reverse('transaction-list')
        data = {
            'wallet': self.wallet.id,
            'txid': 'tx_negative',
            'amount': '-150'  # More than wallet balance
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Transaction.objects.count(), 1)  # No new transaction created

        # Wallet balance should remain unchanged
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal("100"))
