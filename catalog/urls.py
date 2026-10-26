from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='catalog'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
]
