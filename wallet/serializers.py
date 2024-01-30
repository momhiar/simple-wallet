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