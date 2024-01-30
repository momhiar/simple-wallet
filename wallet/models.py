from django.db import models
from django.contrib.auth.models import User

class WalletModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

# we skip some legally business needs for this task 
# like masking Wallet ids like (xxxx-****-****-xxx) and ...
class Wallet(models.Model):
    wallet_name = models.CharField(max_length=75,blank=False, null=False)
    owner = models.ForeignKey(User, db_index=True, on_delete=models.PROTECT)
    balance = models.BigIntegerField(default=0)
    # implementation of very basic soft delete for wallets
    # (legally wallets should not be deleted at first)
    deleted = models.BooleanField(default=False)
    objects = WalletModelManager()
    
    def delete(self):
        self.deleted = True
        self.save()