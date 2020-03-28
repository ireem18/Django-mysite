from django.db import models

# Create your models here.
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
    aboutus = models.TextField(blank=True, max_length=50)
    contact = models.TextField(blank=True, max_length=50)
    references = models.TextField(blank=True, max_length=150)
    status = models.CharField(blank=True, max_length=150, choices=STATUS)
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)

    def __str__(self):
        return self.title