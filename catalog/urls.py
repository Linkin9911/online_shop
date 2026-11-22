from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    # Основные страницы
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),

    # Продукты
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/update/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    # Модерация
    path('moderation/', views.moderation_list, name='moderation_list'),
    path('products/<int:pk>/publish/', views.product_publish, name='product_publish'),
    path('products/<int:pk>/unpublish/', views.product_unpublish, name='product_unpublish'),
]
