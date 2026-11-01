from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Product
from django.urls import reverse_lazy

# ListView: отвечает за вывод списка товаров (наш каталог)
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'
    # paginate_by = 10  <-- УБРАЛИ, чтобы не усложнять без необходимости

# DetailView: отвечает за страницу одного товара
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

# CreateView: отвечает за создание товара
class ProductCreateView(CreateView):
    model = Product
    template_name = 'catalog/add_product.html'
    fields = ['name', 'category', 'price', 'description', 'image']
    success_url = reverse_lazy('catalog')

# UpdateView: отвечает за редактирование товара
class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'catalog/edit_product.html'
    fields = ['name', 'category', 'price', 'description', 'image']
    success_url = reverse_lazy('catalog')

# DeleteView: отвечает за удаление товара
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('catalog')

# TemplateView: страница контактов
class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'
