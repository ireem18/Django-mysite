from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from order import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addtocart/<int:id>', views.addtocart, name='addtocart'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),

]