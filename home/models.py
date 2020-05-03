from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm, TextInput, Textarea
from django.utils.safestring import mark_safe


class Setting(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=150)
    address = models.CharField(blank=True, max_length=150)
    phone = models.CharField(blank=True, max_length=150)
    fax = models.CharField(blank=True, max_length=150)
    email = models.CharField(blank=True, max_length=150)
    smtpserver = models.CharField(blank=True, max_length=150)
    smtpemail = models.CharField(blank=True, max_length=150)
    smtppassword = models.CharField(blank=True, max_length=150)
    smtpport = models.CharField(blank=True, max_length=150)
    icon = models.ImageField(blank=True, upload_to='images/')
    facebook = models.CharField(blank=True, max_length=50)
    instagram = models.CharField(blank=True, max_length=50)
    twitter = models.CharField(blank=True, max_length=50)
    aboutus = RichTextUploadingField(blank=True, max_length=5000)
    contact = RichTextUploadingField(blank=True, max_length=5000)
    references = RichTextUploadingField(blank=True, max_length=1000)
    status = models.CharField(blank=True, max_length=150, choices=STATUS)
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)

    def __str__(self):
        return self.title


class ContactFormMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    name = models.CharField(blank=True, max_length=20)
    email = models.CharField(blank=True, max_length=50)
    subject = models.CharField(blank=True, max_length=50)
    message = models.CharField(blank=True, max_length=255)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ContactForm(ModelForm):
    class Meta:
        model = ContactFormMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name' : TextInput(attrs={'class':'mb-20', 'placeholder':'Name & Surname'}),
            'subject' : TextInput(attrs={'class':'mb-20', 'placeholder':'Subject'}),
            'email' : TextInput(attrs={'class' : 'mb-20', 'placeholder':'Email Address'}),
            'message' : Textarea(attrs={'class':'h-100x ptb-20 ', 'placeholder':'Your Message','rows':'5'})
        }

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #Modeldeki User ile ilişki kurabiliyoruz
    email = models.CharField(blank=True, max_length=150)
    masa_no = models.IntegerField()
    image = models.ImageField(blank=True, upload_to='images/users/')

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.username

    def image_tag(self):
        return mark_safe('<img src = "{}" height ="50"/>'.format(self.image.url))
    image_tag.short_description = 'Images'

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email', 'image','masa_no']