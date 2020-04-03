from django.http import HttpResponse
from django.shortcuts import render

from home.models import Setting


def index(request):
        setting = Setting.objects.get(pk=2)
        context = {'setting':setting,'page':'home'}
        return render(request, 'index.html',context)

def hakkimizda(request):
        setting = Setting.objects.get(pk=2)
        context = {'setting':setting, 'page':'hakkimizda'}
        return render(request, 'hakkimizda.html',context)

def referanslar(request):
        setting = Setting.objects.get(pk=2)
        context = {'setting':setting, 'page':'referanslar'}
        return render(request, 'referanslarimiz.html',context)

def iletisim(request):
        setting = Setting.objects.get(pk=2)
        context = {'setting':setting, 'page':'iletisim'}
        return render(request, 'iletisim.html',context)