from django.db import models
from django.contrib.auth.models import User
# Create your models here. 


class Student(models.Model):
    name = models.CharField(max_length=60)
    name_id = models.CharField(max_length=15)
    check_code = models.CharField(max_length=15)
    # session_id = models.CharField(max_length=100)


# class store_data(models.Model):
#     table_name = models.CharField(max_length=60)
