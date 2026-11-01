from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, \
    ContactsView

urlpatterns = [
    # Главная страница каталога (список товаров)
    path('', ProductListView.as_view(), name='catalog'),

    # Страница конкретного товара (обрати внимание: <int:pk>)
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

    # Страница контактов
    path('contacts/', ContactsView.as_view(), name='contacts'),

    # CRUD операции (если нужны для админки/разработки)
    path('add/', ProductCreateView.as_view(), name='add_product'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='edit_product'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
]
