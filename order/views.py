from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string

from home.models import UserProfile, Setting
from order.models import ShopCartForm, ShopCart, OrderForm, Order, OrderProduct
from product.models import Category, Product


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
    setting = Setting.objects.get(pk=2)
    category = Category.objects.all()
    current_user = request.user
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()  # sepetteki ürünlerin sayısını alıyoruz

    total = 0
    for rs in schopcart:
        total += rs.product.price * rs.quantity

    context = { 'schopcart': schopcart,
                'category': category,
                'total' : total,
                'setting': setting}
    return render(request, 'Shopcart_products.html', context)


@login_required(login_url = '/login') #lgin olması gerekli
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    current_user = request.user
    request.session['cart_items'] = ShopCart.objects.filter( user_id=current_user.id).count()  # sepetteki ürünlerin sayısını alıyoruz
    messages.success(request,"Ürün basarılı bir sekilde silinmiştir")
    return HttpResponseRedirect("/shopcart")


@login_required(login_url = '/login') #lgin olması gerekli
def orderproduct(request):
    setting = Setting.objects.get(pk=2)
    category = Category.objects.all()
    current_user = request.user
    schopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    for rs in schopcart:
        total += rs.product.price * rs.quantity
    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.masa_no = form.cleaned_data['masa_no']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()
            data.code = ordercode
            data.save()

            schopcart = ShopCart.objects.filter(user_id = current_user.id)
            for rs in schopcart:
                detail = OrderProduct()
                detail.order_id = data.id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity

                product = Product.objects.get(id = rs.product_id)
                product.amount -= rs.quantity
                product.save()

                detail.price = rs.product.price
                detail.amount = rs.amount
                detail.save()

            ShopCart.objects.filter(user_id = current_user.id).delete()
            request.session['cart_items'] = 0
            messages.success(request,"Siparisiniz alındı.Teşekürler")
            return render(request,'Order_Complated.html', {'ordercode':ordercode,'category':category})
        else:
            messages.error(request,form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'schopcart':schopcart,
               'category':category,
               'total':total,
               'form':form,
               'profile':profile,
               'setting': setting
               }
    return render(request,'Order_Form.html',context)