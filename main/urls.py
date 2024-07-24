from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_home, name='get-home'),
    path('get-settings/', views.get_settings, name='get-settings'),
    path('get-wallet/', views.get_wallet, name='get-wallet'),

    path('cash-create/', views.cash_create, name='cash-create'),
    path('card-create/', views.card_create, name='card-create'),
    path('currency-create/', views.currency_create, name='currency-create'),

    path('cash-edit/<int:pk>/', views.cash_edit, name='cash-edit'),
    path('card-edit/<int:pk>/', views.card_edit, name='card-edit'),
    path('currency-edit/<int:pk>/', views.currency_edit, name='currency-edit'),

    path('income-outcome/', views.get_income_outcome_list, name='income-outcome'),
    path('income-detail/<int:pk>/', views.get_income_detail, name='income-detail'),

    path('create-income', views.create_income, name='create-income'),
    path('create-outcome', views.create_outcome, name='create-outcome'),
]