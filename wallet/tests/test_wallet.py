import pytest
from .factories import UserFactory
from wallet.models import Wallet
@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def test_wallet(user):
    return Wallet.objects.create(wallet_name='test-wallet', owner=user)

@pytest.mark.django_db
def test_wallet_model_creation(test_wallet):
    assert test_wallet.wallet_name == 'test-wallet'
    assert test_wallet.balance == 0
    
@pytest.mark.django_db
def test_wallet_soft_deletion(test_wallet):
    test_wallet.delete()
    assert test_wallet.deleted is True
    assert Wallet.objects.filter(id=test_wallet.id).exists() is False
    
@pytest.mark.skip(reason="no way of currently testing this")     
@pytest.mark.django_db
def test_user_wallet_created(client, user):
    wallet_data = {'wallet_name': 'test_wallet'}
    url = f'/wallets/create-for-user/{user.id}'
    response = client.post(path=url, data=wallet_data)
    assert response.status_code == 201
    assert response.json().get('owner').get('first_name') == user.first_name
    assert response.json().get('balance') == 0

@pytest.mark.skip(reason="no way of currently testing this") 
@pytest.mark.django_db
def test_user_wallet_list(client, user):
    url = f"/wallets/user-wallets/{user.id}"
    Wallet.objects.create(wallet_name='test-wallet', owner=user)
    response = client.get(path=url)
    assert response.status_code == 200
    assert len(response.json()) == 1