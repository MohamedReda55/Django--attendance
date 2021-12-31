from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import qrcode
from io import BytesIO
from PIL import Image,ImageDraw
from django.core.files import File
from django.db.models import BooleanField, ExpressionWrapper, Q
from django.db.models.functions import Now
from django.utils import timezone
import datetime

class Profile(models.Model):
    user=models.OneToOneField(User ,on_delete=models.CASCADE)
    # username = models.CharField(max_length=50)
    # password = models.CharField(max_length=15)
    subject_1_name=models.CharField(max_length=30,null=True,blank=True)
    subject_2_name=models.CharField(max_length=30,null=True,blank=True)
    subject_3_name = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return str(self.user)

# class Students(models.Model):
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=15)


class qrcode_model(models.Model):
    qrcode_id = models.CharField(max_length=30)
    qrcode_hash = models.CharField(max_length=30)
    qrcode_img = models.ImageField(upload_to='qr_codes',blank=True)
    qrcode_url = models.CharField(max_length=70)
    check_code=models.CharField(max_length=15)

    def __str__(self):
        return str(self.qrcode_url)

    def save(self,*args,**kwargs):
       qr_code_img=qrcode.make(self.qrcode_url,version=8,error_correction=qrcode.constants.ERROR_CORRECT_H)
       canvas=Image.new("RGB",(550,550),"white")
       draw=ImageDraw.Draw(canvas)
       canvas.paste(qr_code_img)
       fname=f"qr_code-{self.qrcode_id}.png"
       buffer=BytesIO()
       canvas.save(buffer,"PNG")
       self.qrcode_img.save(fname,File(buffer),save=False)
       canvas.close()
       super().save(*args,**kwargs)     
       
class login_info(models.Model):
    subject_id = models.CharField(max_length=10)
    subject_name=models.CharField(max_length=70) 
    # subject_info = models.CharField(max_length=70)
       
class login_inf(models.Model):
    subject_id = models.CharField(max_length=10)
    subject_name=models.CharField(max_length=70) 
    subject_info = models.CharField(max_length=70)
       

class server_state(models.Model):
    server_id = models.CharField(max_length=10)
    server_state = models.BooleanField(default=False)
       
class restart_state(models.Model):
    restart_id=models.CharField(max_length=20)
    restart_state=models.BooleanField(default=False)




class records(models.Model):
   date=models.CharField(max_length=10)
   attendance = models.CharField(max_length=10)
   absence = models.CharField(max_length=10)
  
   
@receiver(post_save, sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(
            user=instance
        )