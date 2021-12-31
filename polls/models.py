from django.db import models
from django.contrib.auth.models import User
# Create your models here. 
from django.db.models import BooleanField, ExpressionWrapper, Q
from django.db.models.functions import Now
from django.utils import timezone
import datetime
import time
# class ExpiredManager(models.Manager):

#     def get_queryset(self):
#         return super().get_queryset().annotate(
#             expired=ExpressionWrapper(
#                 Q(valid_to__lt=Now()), output_field=BooleanField())
#         )
class Student(models.Model):
    name = models.CharField(max_length=60)
    name_id = models.CharField(max_length=15)
    check_code = models.CharField(max_length=15)
    # valid_from = models.DateTimeField(default=timezone.now)
    # valid_to = models.DateTimeField()
    # objects = ExpiredManager()
    # def save(self, *args, **kwargs):
        
    #     time_now = time.time()
    #     time_to=time_now+5400
    #     self.valid_from=time_now
    #     self.valid_to=time_to
        # super().save(*args, **kwargs)
    # session_id = models.CharField(max_length=100)


# class store_data(models.Model):
#     table_name = models.CharField(max_length=60)
