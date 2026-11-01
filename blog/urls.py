from django.urls import path
from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

urlpatterns = [
    # Список статей: явно указываем путь и слэш в конце
    path('blogs/', BlogListView.as_view(), name='blog_list'),

    # Детальная статья: обязательно слэш после <int:pk>
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),

    # Создание статьи
    path('blogs/create/', BlogCreateView.as_view(), name='blog_create'),

    # Редактирование статьи: слэш в конце обязателен
    path('blogs/<int:pk>/edit/', BlogUpdateView.as_view(), name='blog_edit'),

    # Удаление статьи
    path('blogs/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog_delete'),
]
