from django.contrib import admin
from .models import Cash, Card, Currency, Income, Outcome
# Register your models here.


admin.site.register(Cash)
admin.site.register(Card)
admin.site.register(Currency)
admin.site.register(Income)
admin.site.register(Outcome)