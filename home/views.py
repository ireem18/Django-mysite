from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from home.models import Setting, ContactForm, ContactFormMessage
from product.models import Product, Category


def index(request):
        setting = Setting.objects.get(pk=2)
        sliderdata = Product.objects.all()[:3]
        category = Category.objects.all()
        dayproducts = Product.objects.all()[:4]
        lastproducts = Product.objects.all().order_by('-id')[:4]
        randomproducts = Product.objects.all().order_by('?')[:4]

        context = {'setting':setting,
                   'category':category,
                   'page':'home',
                   'sliderdata':sliderdata,
                   'dayproducts':dayproducts,
                   'lastproducts':lastproducts,
                   'randomproducts':randomproducts
                   }
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

def category_products(request,id,slug):
        category = Category.objects.all()
        products = Product.objects.filter(category_id=id)
        categoryData = Category.objects.get(pk=id)
        context = {'products': products,
                   'category': category,
                   'categoryData': categoryData,
                   'page': 'products'
                   }
        return render(request, 'products.html', context)

def products(request):
        category = Category.objects.all()
        products = Product.objects.all()
        setting = Setting.objects.get(pk=2)
        context = { 'products': products,
                   'category': category,
                    'page':'products'}
        return render(request, 'products.html',context)