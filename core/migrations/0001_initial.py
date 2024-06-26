# Generated by Django 4.1 on 2024-04-22 05:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "status",
                    models.IntegerField(
                        choices=[(0, "等待接单"), (1, "服务中"), (2, "订单完成")], default=0
                    ),
                ),
                ("address", models.TextField()),
                ("services", models.TextField()),
                ("phone", models.CharField(max_length=11)),
                ("remark", models.TextField()),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField(null=True)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="customer_orders",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "worker",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="worker_orders",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                (
                    "name",
                    models.CharField(max_length=10, primary_key=True, serialize=False),
                ),
                ("price", models.IntegerField(default=9999)),
            ],
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "order",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="core.order",
                    ),
                ),
                ("attitude_score", models.IntegerField(default=5)),
                ("quality_score", models.IntegerField(default=5)),
                ("overall_score", models.IntegerField(default=5)),
                ("comment", models.TextField(default="系统默认好评")),
            ],
        ),
    ]
