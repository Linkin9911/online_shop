from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import ContactForm, ProductForm
from .models import Product


def home(request):
    return render(request, 'catalog/home.html')


def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            messages.success(request, f'Спасибо, {name}! Ваше сообщение отправлено.')
    else:
        form = ContactForm()
    return render(request, 'catalog/contacts.html', {'form': form})


# Публичная страница — единственная без декоратора
def product_list(request):
    products = Product.objects.all()
    return render(request, 'catalog/product_list.html', {'products': products})


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар создан.')
            return redirect('catalog:product_list')
    else:
        form = ProductForm()
    return render(request, 'catalog/product_form.html', {'form': form})


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар обновлён.')
            return redirect('catalog:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'catalog/product_form.html', {'form': form})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Товар удалён.')
        return redirect('catalog:product_list')
    return render(request, 'catalog/product_delete.html', {'product': product})
