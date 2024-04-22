from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Info(models.Model):
    user_key = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker_info', primary_key=True)
    order_success_count = models.IntegerField(default=0)
    attitude_score = models.FloatField(default=0)
    quality_score = models.FloatField(default=0)
    overall_score = models.FloatField(default=0)

    def change_score(self, attitude_score, quality_score, overall_score,
                     old_attitude_score, old_quality_score, old_overall_score):
        self.attitude_score = (self.attitude_score * self.order_success_count
                               - old_attitude_score + attitude_score) / self.order_success_count
        self.quality_score = (self.quality_score * self.order_success_count
                              - old_quality_score + quality_score) / self.order_success_count
        self.overall_score = (self.overall_score * self.order_success_count
                              - old_overall_score + overall_score) / self.order_success_count
        self.save()

    def finish_order(self):
        self.attitude_score = ((self.attitude_score * self.order_success_count + 5) / (self.order_success_count + 1))
        self.quality_score = ((self.quality_score * self.order_success_count + 5) / (self.order_success_count + 1))
        self.overall_score = ((self.overall_score * self.order_success_count + 5) / (self.order_success_count + 1))
        self.order_success_count += 1
        self.save()
