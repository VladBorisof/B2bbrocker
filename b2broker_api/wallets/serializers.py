from rest_framework import serializers
from .models import Wallet, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model"""
    
    class Meta:
        model = Transaction
        fields = ['id', 'wallet', 'txid', 'amount', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate(self, data):
        """
        Validate that the transaction won't make the wallet balance negative.
        """
        wallet = data.get('wallet')
        amount = data.get('amount')
        
        # Skip validation for updates where amount isn't changing
        if self.instance and amount == self.instance.amount:
            return data
            
        # For new transactions or amount changes, validate the balance
        current_balance = wallet.balance
        
        # If updating, subtract the current transaction amount first
        if self.instance:
            current_balance -= self.instance.amount
            
        # Check if this transaction would make the balance negative
        if current_balance + amount < 0:
            raise serializers.ValidationError(
                f"Transaction of {amount} would make wallet balance negative. "
                f"Current balance: {current_balance}"
            )
        
        return data


class WalletSerializer(serializers.ModelSerializer):
    """Serializer for Wallet model with balance as a read-only field"""
    balance = serializers.DecimalField(
        max_digits=38,
        decimal_places=18,
        read_only=True
    )
    
    class Meta:
        model = Wallet
        fields = ['id', 'label', 'balance']
        read_only_fields = ['id', 'balance']


class WalletDetailSerializer(WalletSerializer):
    """Extended Wallet serializer that includes transactions"""
    transactions = TransactionSerializer(many=True, read_only=True)
    
    class Meta(WalletSerializer.Meta):
        fields = WalletSerializer.Meta.fields + ['transactions']
