from django.shortcuts import render, get_object_or_404, reverse
import re
from .models import Passport, Address
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    passport = Passport.objects.get_one_passport(username=username, password=password)

    request.session['username'] = username
    request.session['passport_id'] = passport.id

    return render(request, 'users/register.html')

def register_handle(request):
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')

    if  not all([username, password, email]):
        context = {'errormsg': '参数不能为空! '}
        return render(request, 'users/register.html', context)

    if not re.match(r'^[A-Za-z0-9][\w\.\-]*@[a-z0-9]+(\.[a-z]{2,5}){1,2}$', email):
        context = {'errormsg': '邮箱不合法! '}
        render(request, 'users/register.html', context)

    try:
        Passport.objects.add_one_passport(username=username, password=password, email=email)
    except:
        context = {'errormsg': '用户名已存在! '}
        render(request, 'users/register.html', context)

    return HttpResponseRedirect(reverse('books:index'))

def logout_view(request):
    logout(request)
    request.session.flush()
    return HttpResponseRedirect(reverse('books:index'))

@login_required
def user(request):
    passport_id = request.session.get('passport_id')

    addr =Address.objects.get_default_address(passport_id=passport_id)

    books_list = []
    context = {
        'addr': addr, 'page': 'user', 'books_list': books_list
    }

    return render(request, 'users/info.html', context)

