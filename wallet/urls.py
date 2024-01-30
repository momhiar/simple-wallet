from django.urls import path
from . import views
urlpatterns = [
    path('create-for-user/<int:user>', views.WalletCreateAPIView.as_view()),
    path('user-wallets/<int:user>', views.WalletsListAPIView.as_view()),
    path('<int:pk>', views.WalletRetrieveAPIView.as_view()),
    path('wallet-transactions', views.TransactionListAPIView.as_view()),
    path('perform-transaction', views.CreateTransactionAPIView.as_view())
]