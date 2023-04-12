from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from myapp.models import UserProfile

class SignUpForm(UserCreationForm):

    class Meta:
        model=User
        fields=["email","username","password1","password2"]



class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()



class ProfileEditForm(forms.ModelForm):

    class Meta:
        model=UserProfile
        fields=["profile_pic","bio","address","dob"]