from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Info(models.Model):
    user_key = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_info', primary_key=True)
    order_count = models.IntegerField(default=0)
    order_success_count = models.IntegerField(default=0)
