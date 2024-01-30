from rest_framework.generics import ListAPIView,CreateAPIView, RetrieveAPIView
from . import models
from . import serializers
from abc import abstractmethod
#SRP: each view only handles one action
#OCP: different functionalities without modifying BaseWallet 

class BaseWalletView():
    serializer_class = serializers.WalletSerializer
    @abstractmethod
    def get_queryset(self):
        pass
    
class WalletsListAPIView(BaseWalletView,ListAPIView):
    def get_queryset(self):
        # we use url kwargs since we have no Authorization,
        # only simply to define user we use this
        # alternatively we could use query params
        # but decided this way to play with less when creating
        owner = self.kwargs['user']
        return models.Wallet.objects.filter(owner=owner)

class WalletCreateAPIView(BaseWalletView,CreateAPIView):
    def get_queryset(self):
        return models.Wallet.objects.all()

class WalletRetrieveAPIView( BaseWalletView, RetrieveAPIView):
    def get_queryset(self):
        return models.Wallet.objects.all()
