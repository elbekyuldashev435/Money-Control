from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=120)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    password = models.TextField()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username


class Support(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_tickets')
    message = models.TextField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_support_tickets')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'support'

    def __str__(self):
        return f"{self.user.username} | {self.created_at}"