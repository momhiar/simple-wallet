from django.db import models
from django.contrib.auth.models import User


# we skip some legally business needs for this task 
# like masking Wallet ids like (xxxx-****-****-xxx) and ...
class Wallet(models.Model):
    wallet_name = models.CharField(max_length=75,blank=False, null=False)
    owner = models.ForeignKey(User, db_index=True, on_delete=models.PROTECT)
    balance = models.BigIntegerField(default=0)

