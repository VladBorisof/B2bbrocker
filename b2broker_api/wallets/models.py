from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum
from decimal import Decimal
from django.utils import timezone


class Wallet(models.Model):
    """
    Wallet model to store wallet information and calculate balance
    """
    label = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def balance(self):
        """Calculate the wallet balance from all related transactions"""
        result = self.transactions.aggregate(
            balance=Sum('amount', default=Decimal('0'))
        )
        return result['balance']

    def __str__(self):
        return f"{self.label} (Balance: {self.balance})"


class Transaction(models.Model):
    """
    Transaction model to store wallet transactions
    """
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    txid = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=38, decimal_places=18)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """
        Validate that the transaction won't make the wallet balance negative
        """
        if self.amount < 0:
            # Get current wallet balance excluding this transaction
            current_balance = self.wallet.balance
            
            # If this is an update, add back the original amount
            if self.id:
                original = Transaction.objects.get(id=self.id)
                current_balance -= original.amount
                
            # Check if this transaction would make the balance negative
            if current_balance + self.amount < 0:
                raise ValidationError(
                    f"Transaction would make wallet balance negative. "
                    f"Current balance: {current_balance}, "
                    f"Transaction amount: {self.amount}"
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.txid}: {self.amount}"
