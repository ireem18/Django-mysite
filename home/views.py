from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from home.models import Setting, ContactForm, ContactFormMessage


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

        if request.method == 'POST': # Form post edildiyse
                form = ContactForm(request.POST)
                if form.is_valid():
                        data = ContactFormMessage() # model ile bağlantı kur
                        data.name = form.cleaned_data['name'] # formdan bilgiyi al
                        data.email = form.cleaned_data['email']
                        data.subject = form.cleaned_data['subject']
                        data.message = form.cleaned_data['message']
                        data.save() # veritabanına kayıt et
                        messages.success(request, "Mesajınız basarı ile gönderildi")
                        return HttpResponseRedirect('/iletisim')

        setting = Setting.objects.get(pk=2)
        form = ContactForm()
        context = {'setting':setting, 'form': form}
        return render(request, 'iletisim.html',context)