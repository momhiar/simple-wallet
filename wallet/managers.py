from .models import Wallet
from rest_framework.exceptions import ValidationError
class TransactionManager():
    def __init__(self, to_wallet_id,from_wallet_id,amount, reason, serializer):
          self.from_wallet_id = from_wallet_id
          self.to_wallet_id = to_wallet_id
          self.amount = amount
          self.reason = reason
          
    def perform(self):
            source = Wallet.objects.select_for_update().get(id = self.from_wallet_id)
            destination = Wallet.objects.select_for_update().get(id=self.to_wallet_id)
            self.check_balance_is_enough(source)
            self.check_source_is_not_destination(source, destination)
            source.balance -= self.amount
            source.save()
            destination.balance += self.amount
            destination.save()
            
    def check_balance_is_enough(self, source):
        if(source.balance < self.amount):
            raise ValidationError('low balance for this transfer')
    
    def check_source_is_not_destination(self, source, destination):
        if source == destination:
            raise ValidationError('disallowed transaction')