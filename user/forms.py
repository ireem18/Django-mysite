from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput,FileInput, EmailInput
from django import forms
from home.models import UserProfile

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username' : TextInput(attrs={'class':'input','placeholder':'username','style':'color:green'}),
            'email' : EmailInput(attrs={'class':'input','placeholder':'email','style':'color:green'}),
            'first_name' : TextInput(attrs={'class':'input','placeholder':'first_name','style':'color:green'}),
            'last_name' : TextInput(attrs={'class':'input','placeholder':'last_name','style':'color:green'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('masa_no', 'image')
        widgets = {
            'masa_no': TextInput(attrs={'class':'input','placeholder':'placeholder','style':'color:green'}),
            'image': FileInput(attrs={'class':'input','placeholder':'image'}),
        }