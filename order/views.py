from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from order.models import ShopCartForm, ShopCart
from product.models import Category


def index(request):
    return HttpResponse("Order App")


@login_required(login_url='/login') #lgin olması gerekli
def addtocart(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    checkProduct = ShopCart.objects.filter(product_id=id)
    #****Urun sepette var mı yok mu*******
    if checkProduct:
        control = 1
    else:
        control = 0
    if request.method == 'POST':
        form = ShopCartForm(request.POST)
        if form.is_valid():

            if control == 1: #ürün varsa guncelle
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
                request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count() #sepetteki ürünlerin sayısını alıyoruz
                messages.success(request, "Ürün basarılı bir şekilde eklenmiştir")
                return HttpResponseRedirect(url)
            else: #urun yoksa ekle
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
                request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count() #sepetteki ürünlerin sayısını alıyoruz
                messages.success(request, "Ürün basarılı bir şekilde eklenmiştir")
                return HttpResponseRedirect(url)

    else: #eger post işlemi yoksa sadece id ile gönderim varsa
        if control == 1:
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()  # sepetteki ürünlerin sayısını alıyoruz
        messages.warning(request, "Ürün sepete eklemede hata oluştu.Lütfen tekrar deneyiniz")
        return HttpResponseRedirect(url)

@login_required(login_url = '/login') #login olması gerekli
def shopcart(request):
    category = Category.objects.all()
    current_user = request.user
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()  # sepetteki ürünlerin sayısını alıyoruz

    total = 0
    for rs in schopcart:
        total += rs.product.price * rs.quantity

    context = { 'schopcart': schopcart,
                'category': category,
                'total' : total }
    return render(request, 'Shopcart_products.html', context)


@login_required(login_url = '/login') #lgin olması gerekli
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Ürün basarılı bir şekilde silindi")
    current_user = request.user
    request.session['cart_items'] = ShopCart.objects.filter( user_id=current_user.id).count()  # sepetteki ürünlerin sayısını alıyoruz
    messages.success(request,"Ürün basarılı bir sekilde silinmiştir")
    return HttpResponseRedirect("/shopcart")
