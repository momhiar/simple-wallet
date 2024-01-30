from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from . import models
from . import serializers
from django.db.models import Q
from abc import abstractmethod
from rest_framework.response import Response
from .managers import TransactionManager
from django.db import transaction as db_transaction
# SRP: each view only handles one action
# OCP: different functionalities without modifying BaseWallet


class BaseWalletView():
    serializer_class = serializers.WalletSerializer

    @abstractmethod
    def get_queryset(self):
        pass


class WalletsListAPIView(BaseWalletView, ListAPIView):
    def get_queryset(self):
        # we use url kwargs since we have no Authorization,
        # only simply to define user we use this
        # alternatively we could use query params
        # but decided this way to play with less when creating
        owner = self.kwargs['user']
        return models.Wallet.objects.filter(owner=owner)


class WalletCreateAPIView(BaseWalletView, CreateAPIView):
    def get_queryset(self):
        return models.Wallet.objects.all()


class WalletRetrieveAPIView(BaseWalletView, RetrieveAPIView):
    def get_queryset(self):
        return models.Wallet.objects.all()


class TransactionListAPIView(ListAPIView):
    permission_classes = []
    serializer_class = serializers.TransactionSerializer

    def get_queryset(self):
        wallet = self.request.query_params.get('wallet')
        return models.Transaction.objects.filter(Q(from_wallet_id=wallet) | Q(to_wallet_id=wallet))



class CreateTransactionAPIView(CreateAPIView):
    serializer_class = serializers.CreateTransactionSerializer
    queryset = models.Transaction.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with db_transaction.atomic():
            serializer.save()
            transaction = TransactionManager(**serializer.data, serializer=serializer)
            transaction.perform()
        return Response(serializer.data, status=201)

