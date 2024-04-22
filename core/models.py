from django.contrib.auth.models import User
from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=10, primary_key=True)
    price = models.IntegerField(default=9999)


class Order(models.Model):
    STATUS_CHOICES = (
        (0, '等待接单'),
        (1, '服务中'),
        (2, '订单完成'),
    )
    id = models.AutoField(primary_key=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    address = models.TextField()
    services = models.TextField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_orders')
    phone = models.CharField(max_length=11)
    worker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='worker_orders')
    remark = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)


class Review(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key=True)
    attitude_score = models.IntegerField(default=5)
    quality_score = models.IntegerField(default=5)
    overall_score = models.IntegerField(default=5)
    comment = models.TextField(default="系统默认好评")
