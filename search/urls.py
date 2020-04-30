# sendemail/urls.py
from django.contrib import admin
from django.urls import path
from .views import BootstrapFilterView,resultView, SearchPageView, SearchResultsView

urlpatterns = [
    #ค้นหาข้อมูลผู้สูญหาย
    path('searchpost/', SearchPageView.as_view(), name='searchPost'),
    path('resultpost/', SearchResultsView.as_view(), name='resultPost'),
    #ค้นหาข้อมูลจากเบาะแสคนหาย
    path('search3/', BootstrapFilterView, name='searchNew'),
    path('result3/', resultView, name='resultNew'),
]