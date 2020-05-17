import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactForm, ContactFormMessage, FAQ
from order.models import ShopCart
from product.models import Product, Category, Images, Comment


def index(request):
        current_user = request.user
        setting = Setting.objects.get(pk=2)
        sliderdata = Product.objects.all()[:3]
        category = Category.objects.all()
        dayproducts = Product.objects.all()[3:7]
        lastproducts = Product.objects.filter(status='True').order_by('-id')[:4]
        randomproducts = Product.objects.filter(status='True').order_by('?')[:4]
        request.session['cart_items'] = ShopCart.objects.filter( user_id=current_user.id).count()  # sepetteki ürünlerin sayısını alıyoruz

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
        category = Category.objects.all()
        sliderdata = Product.objects.all()[:3]
        context = {'setting':setting,
                   'category': category,
                   'sliderdata': sliderdata,
                   'page':'hakkimizda'}
        return render(request, 'hakkimizda.html',context)

def referanslar(request):
        setting = Setting.objects.get(pk=2)
        category = Category.objects.all()
        sliderdata = Product.objects.all()[:3]
        context = {'setting':setting,
                   'category': category,
                   'sliderdata': sliderdata,
                   'page':'referanslar'}
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
        category = Category.objects.all()
        sliderdata = Product.objects.all()[:3]
        context = {'setting':setting,
                   'category': category,
                   'form': form}
        return render(request, 'iletisim.html',context)

def category_products(request,id,slug):
        category = Category.objects.all()
        products = Product.objects.filter(category_id=id)
        categoryData = Category.objects.get(pk=id)
        setting = Setting.objects.get(pk=2)

        context = {'products': products,
                   'category': category,
                   'categoryData': categoryData,
                   'page': 'products',
                   'setting': setting
                   }
        return render(request, 'products.html', context)

def products(request):
        category = Category.objects.all()
        products = Product.objects.filter(status='True')
        setting = Setting.objects.get(pk=2)
        sliderdata = Product.objects.all()[:3]
        context = { 'products': products,
                   'category': category,
                    'sliderdata': sliderdata,
                    'page':'products',
                    'setting':setting}
        return render(request, 'products.html',context)

def product_detail(request,id,slug):
    mesaj = "Ürün",id,"/",slug
    images = Images.objects.filter(product_id = id)
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    if product.status != 'True':
        messages.warning(request, "Ürün suan bulunamıyor.Lütfen başka bir ürün tercih ediniz....")
        return HttpResponseRedirect('/')
    setting = Setting.objects.get(pk=2)
    comments = Comment.objects.filter(product_id=id,status='True')
    sliderdata = Product.objects.all()[:3]
    context = {'page':'product_detail',
               'category': category,
               'product': product,
               'images': images,
               'comments': comments,
               'setting':setting}
    return render(request,'product_detail.html',context)

def product_search(request):
    setting = Setting.objects.get(pk=2)
    if request.method == 'POST': #Check form post
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query'] #formdan bilgiyi al
            #catid = form.cleaned_data['catid']

            #if catid == 0:
            #  products = Product.objects.filter(title__icontains=query)
            #else:
            products = Product.objects.filter(title__icontains=query)

            context = {'products':products,
                       'category':category,
                       'setting': setting
                       }
            return render(request, 'products_search.html', context)
        return HttpResponseRedirect('/')

def product_search_auto(request):
  if request.is_ajax():
    q = request.GET.get('term', '') #script dosyasından alan foonksiyonu term olarak algılar
    product = Product.objects.filter(title__icontains=q)
    results = []
    for rs in product:
      product_json = {}
      product_json =rs.title
      results.append(product_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    setting = Setting.objects.get(pk=2)
    if request.method == 'POST': #Check form post
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Hatası! Kullanıcı adı ya da Şifre yanlış")
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    context = {'category': category,
               'setting': setting
               }
    return render(request, 'login.html', context)

def signup_view(request):
    setting = Setting.objects.get(pk=2)
    if request.method == 'POST': #Check form post
        form = SignUpForm(request.POST)
        if form.is_valid(): #Formdaki kontrolleri yapar.Tum form elemeanları dolu mu
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request,user)
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form,
               'setting': setting
               }
    return render(request, 'signup.html', context)

def faq(request):
    setting = Setting.objects.get(pk=2)
    category = Category.objects.all()
    faq = FAQ.objects.filter(status ='True').order_by('ordernumber')
    context = {
        'category': category,
        'faq': faq,
        'setting': setting
    }
    return render(request, 'faq.html', context)

