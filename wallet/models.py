from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
        
        
class Transaction(models.Model):
    # we assume that base Currency is IRR 
    # and we do not want to add any other currency
    amount = models.BigIntegerField()
    from_wallet_id = models.ForeignKey(Wallet, db_index=True, related_name='source_wallet', on_delete=models.CASCADE,)
    to_wallet_id = models.ForeignKey(Wallet, db_index=True, related_name='destintaion_wallet', on_delete=models.CASCADE)
    date_issued = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=75, blank=True)
    def clean(self):
        if (self.from_wallet_id == self.to_wallet_id):
            raise ValidationError('destination and source of money can not be the same')