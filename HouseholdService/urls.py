"""HouseholdService URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from backend.views import backend_request
from core.views import *
from customer.views import customer_request
from worker.views import worker_request

urlpatterns = [
    path("", index_request, name='index'),
    path("accounts/login/", login_request, name='login'),
    path("register/", register_request, name='register'),
    path("backend/", backend_request, name='backend'),
    path("worker/", worker_request, name='worker'),
    path("customer/", customer_request, name='customer'),
]
