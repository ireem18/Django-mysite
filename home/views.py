from django.http import HttpResponse
from django.shortcuts import render

from home.models import Setting


def index(request):

        setting = Setting.objects.get(pk=2)
        context = {'setting':setting}
        return render(request, 'index.html',context)

