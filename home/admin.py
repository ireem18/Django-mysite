from django.contrib import admin

# Register your models here.
from home.models import Setting, ContactFormMessage, UserProfile


class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject','message','note', 'status']
    list_filter = ['status']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'email','image_tag','masa_no']


admin.site.register(Setting)
admin.site.register(ContactFormMessage,ContactFormMessageAdmin)
admin.site.register(UserProfile,UserProfileAdmin)