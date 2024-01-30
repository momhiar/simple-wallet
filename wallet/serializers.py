from rest_framework import serializers
from django.contrib.auth.models import User
from . import models as wallet_models
from django.core.exceptions import ObjectDoesNotExist


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class WalletSerializer(serializers.ModelSerializer):
    owner = BasicUserSerializer(read_only=True)

    class Meta:
        model = wallet_models.Wallet
        exclude = ['deleted']
        read_only_fields = ['balance']

    def create(self, validated_data):
        owner = self.get_owner_object()
        wallet = wallet_models.Wallet.objects.create(
            owner=owner, **validated_data)
        return wallet

    def get_owner_object(self):
        owner_id = self.context['view'].kwargs['user']
        try:
            owner = User.objects.get(id=owner_id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('user does not exists')
        return owner


class WalletBasicSerializer(WalletSerializer):
    class Meta:
        model = wallet_models.Wallet
        exclude = ['deleted', 'balance', 'wallet_name']

    def save(self):
        return

class TransactionSerializer(serializers.ModelSerializer):
    from_wallet_id = WalletBasicSerializer()
    to_wallet_id = WalletBasicSerializer()
    transaction_type = serializers.SerializerMethodField()

    class Meta:
        model = wallet_models.Transaction
        fields = '__all__'

    def get_transaction_type(self, obj):
        
        wallet_object = self.get_wallet_object()
        if (obj == wallet_object):
            return 'outbound'
        return 'inbound'
    
    def get_wallet_object(self):
        wallet_id = self.context['request'].query_params.get('wallet')
        try:
            wallet_obj = wallet_models.Wallet.objects.get(id=wallet_id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Invalid Wallet id')
        return wallet_obj

class CreateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = wallet_models.Transaction
        fields = ["from_wallet_id", "to_wallet_id", "amount", "reason"]
