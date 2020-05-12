from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from home.models import UserProfile, Setting
from order.models import Order, OrderProduct
from product.models import Category, Comment
from user.forms import UserUpdateForm, ProfileUpdateForm


def index(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=2)
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category,
               'profile':profile,
               'setting': setting}
    return render(request, 'user_profile.html', context)


@login_required(login_url = '/login') #lgin olması gerekli
def user_update(request):
    setting = Setting.objects.get(pk=2)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance = request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,"Hesabınız guncellendi")
            return redirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance = request.user) #formun user ile iliskisi
        profile_form = ProfileUpdateForm(instance = request.user.userprofile)
        context = {
            'category':category,
            'user_form':user_form,
            'profile_form':profile_form,
            'setting': setting
        }
        return render(request,'user_update.html',context)

@login_required(login_url = '/login') #lgin olması gerekli
def change_password(request):
    setting = Setting.objects.get(pk=2)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request,"Parolanız guncellendi")
            return redirect('change_password')
        else:
            messages.error(request,"Bir şeyler ters gitti" + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user) #Bu form hazır olan bir formdur
        return render(request,'change_password.html', {
            'form':form,
            'category':category,
            'setting': setting
        })

@login_required(login_url = '/login') #lgin olması gerekli
def orders(request):
    setting = Setting.objects.get(pk=2)
    category = Category.objects.all()
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)
    context = {
        'category':category,
        'orders':orders,
        'setting': setting
    }
    return render(request,'user_orders.html',context)

@login_required(login_url = '/login') #lgin olması gerekli
def orderdetail(request,id): #return HttpResponse(str(id)) Id nin gidip gitmedigini test ettik
    setting = Setting.objects.get(pk=2)
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        'category':category,
        'order':order,
        'orderitems':orderitems,
        'setting': setting
    }
    return render(request,'user_order_detail.html',context)


@login_required(login_url = '/login') #login olması gerekli
def comments(request):
    setting = Setting.objects.get(pk=2)
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category':category,
        'comments':comments,
        'setting': setting
    }
    return render(request,'user_comments.html',context)

@login_required(login_url = '/login') #login olması gerekli
def deletecomment(request,id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request,"Yorumunuz silindi!")
    return HttpResponseRedirect('/user/comments')
