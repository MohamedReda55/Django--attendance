from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
class SignupForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2']
class UserForm(forms.ModelForm):
    pass
    # class Meta:
    #     model=User
    #     fields=['username','password1','password2'] 
class ProfileForm(forms.ModelForm):
    pass
    class Meta:
        model=Profile
        fields=['subject_1_name','subject_2_name','subject_3_name'] 