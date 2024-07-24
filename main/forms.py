from django.forms import ModelForm
from .models import Cash, Card, Currency, Income, Outcome


class CashForm(ModelForm):
    class Meta:
        model = Cash
        fields = ['amount', 'created_at']


class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = ['name', 'card_number', 'phone_number', 'validity_period', 'amount', 'created_at']


class CardEditForm(ModelForm):
    class Meta:
        model = Card
        fields = ['card_number', 'phone_number', 'amount', 'created_at']


class CurrencyForm(ModelForm):
    class Meta:
        model = Currency
        fields = ['amount', 'created_at']


class IncomeForm(ModelForm):
    class Meta:
        model = Income
        fields = ['income_type', 'payment_type', 'amount', 'created_at', 'comment']


class OutcomeForm(ModelForm):
    class Meta:
        model = Outcome
        fields = ['outcome_type', 'payment_type', 'amount', 'created_at', 'comment']