# sendemail/urls.py
from django.contrib import admin
from django.urls import path

from .views import successView, FormView

urlpatterns = [
    path('email/', FormView.as_view(), name='email'),
    path('success/', successView, name='success'),
]