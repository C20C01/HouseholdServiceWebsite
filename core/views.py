from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import render, redirect

from core.models import Service


def index_request(request):
    return render(request, "index.html", {'services': Service.objects.all()})


def login_request(request):
    if request.method == 'POST':
        return _handle_login_post(request)
    else:
        next_url = request.GET.get('next', '')
        return render(request, "core/login.html", {'next': next_url})  # 将 'next' 参数传递到模板


def _handle_login_post(request):
    name = request.POST["name"]
    password = request.POST["password"]
    user = authenticate(request, username=name, password=password)
    if user is not None:
        login(request, user)
        next_url = request.POST.get('next')  # 获取 'next' 参数
        if next_url:
            return redirect(next_url)
        else:
            return redirect("/" + Group.objects.get(user=user).name)
    else:
        return HttpResponse("Invalid login")


def register_request(request):
    if request.method == 'POST':
        return _handle_register_post(request)
    else:
        return render(request, "core/register.html")


def _handle_register_post(request):
    name = request.POST["name"]
    password = request.POST["password"]
    if User.objects.filter(username=name).exists():
        return HttpResponse("User already exists")
    user = User.objects.create_user(username=name, password=password)
    role = str(request.POST["role"])
    if role == "customer":
        from customer.models import Info
        Info.objects.create(user_key=user)
    elif role == "worker":
        from worker.models import Info
        Info.objects.create(user_key=user)
    else:
        return HttpResponse("Invalid role")
    group, _ = Group.objects.get_or_create(name=role)
    user.groups.add(group)
    return redirect("login")
