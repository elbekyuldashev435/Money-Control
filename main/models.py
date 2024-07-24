from django.db import models
from users.models import User
from django.db.models import F
from django.core.exceptions import MultipleObjectsReturned
# Create your models here.


class Cash(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'cash'
        unique_together = ('user_id',)

    def __str__(self):
        return f"{self.amount}"


class Card(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    card_number = models.CharField(max_length=16, unique=True)
    phone_number = models.CharField(max_length=13, unique=True)
    validity_period = models.CharField(max_length=4)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'card'
        unique_together = ('user_id',)

    def __str__(self):
        return f"{self.amount}"


class Currency(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'currency'
        unique_together = ('user_id',)

    def __str__(self):
        return f"{self.amount}"


class Income(models.Model):
    INCOME_TYPE = (
        ('salary', 'MAOSH'),
        ('gift', "SOVG'A"),
    )
    PAYMENT_TYPE = (
        ('cash', 'CASH'),
        ('card', 'CARD'),
        ('currency', 'CURRENCY')
    )

    income_type = models.CharField(choices=INCOME_TYPE, max_length=10)
    payment_type = models.CharField(choices=PAYMENT_TYPE, max_length=10)
    receiver_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    created_at = models.DateTimeField()

    comment = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.payment_type == 'cash':
            cash, created = Cash.objects.get_or_create(user_id=self.receiver_id, defaults={'amount': 0.0})
            cash.amount = F('amount') + self.amount
            cash.save()

        elif self.payment_type == 'card':
            card = Card.objects.filter(user_id=self.receiver_id).first()
            if card:
                card.amount = F('amount') + self.amount
                card.save()
            else:
                Card.objects.create(user_id=self.receiver_id, amount=self.amount)

        elif self.payment_type == 'currency':
            currency, created = Currency.objects.get_or_create(user_id=self.receiver_id, defaults={'amount': 0.0})
            currency.amount = F('amount') + self.amount
            currency.save()

        super(Income, self).save(*args, **kwargs)

    class Meta:
        db_table = 'incomes'

    def __str__(self):
        return f"{self.income_type} | {self.payment_type} | {self.amount}"


class Outcome(models.Model):
    OUTCOME_TYPE = (
        ('komunal', 'KOMUNAL'),
        ('shaxsiy', 'SHAXSIY'),
        ('transport', 'TRANSPORT'),
        ('uyali aloqa', 'UYALI ALOQA'),
        ('internet', 'INTERNET'),
        ("ro'zg'or", "RO'ZG'OR")
    )
    PAYMENT_TYPE = (
       ('cash', 'CASH'),
       ('card', 'CARD'),
       ('currency', 'CURRENCY')
    )
    outcome_type = models.CharField(choices=OUTCOME_TYPE, max_length=15)
    payment_type = models.CharField(choices=PAYMENT_TYPE, max_length=10)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    created_at = models.DateTimeField()

    comment = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            if self.payment_type == 'cash':
                cash, _ = Cash.objects.get_or_create(user_id=self.sender_id, defaults={'amount': 0.0})
                percent = self.amount + (self.amount / 100)
                if cash.amount >= self.amount and (cash.amount - percent) > 0:
                    cash.amount -= percent
                    cash.save()
                else:
                    raise ValueError("Hisobingizda mablag' yetarli emas!")

            elif self.payment_type == 'card':
                card, _ = Card.objects.get_or_create(user_id=self.sender_id, defaults={'amount': 0.0})
                percent = self.amount + (self.amount / 100)
                if card.amount > self.amount and (card.amount - percent) > 0:
                    card.amount -= percent
                    card.save()
                else:
                    raise ValueError("Hisobingizda mablag' yetarli emas!")

            elif self.payment_type == 'currency':
                try:
                    currency = Currency.objects.get(user_id=self.sender_id)
                except MultipleObjectsReturned:
                    # Handle the case where multiple Currency objects are found
                    currency = Currency.objects.filter(user_id=self.sender_id).first()  # or handle as needed
                if currency.amount >= self.amount and (currency.amount - self.amount) > 0:
                    currency.amount -= self.amount
                    currency.save()
                else:
                    raise ValueError("Hisobingizda mablag' yetarli emas!")

        except MultipleObjectsReturned:
            pass

        super(Outcome, self).save(*args, **kwargs)

    class Meta:
        db_table = 'outcomes'

    def __str__(self):
        return f"{self.outcome_type} | {self.payment_type} | {self.amount}"