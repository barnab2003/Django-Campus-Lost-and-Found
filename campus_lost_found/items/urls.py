# items/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('report/', views.report_item, name='report_item'),
    path('register/', views.register, name='register'), # Add this line
    path('dashboard/', views.my_dashboard, name='my_dashboard'),
    path('claim/<int:item_id>/', views.mark_as_claimed, name='mark_as_claimed'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
]