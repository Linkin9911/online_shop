from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ContactForm, ProductForm
from .models import Product


def is_moderator(user):
    return user.is_superuser or user.has_perm('catalog.can_unpublish_product')


# ---------- Основные страницы ----------

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


# ---------- CRUD продуктов ----------

def product_list(request):
    products = Product.objects.all()
    return render(request, 'catalog/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user  # привязываем товар к авторизованному пользователю
            product.save()
            messages.success(request, 'Продукт создан и отправлен на модерацию.')
            return redirect('catalog:product_list')
    else:
        form = ProductForm()
    return render(request, 'catalog/product_form.html', {'form': form})


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.owner != request.user and not is_moderator(request.user):
        messages.error(request, 'У вас нет прав на редактирование этого продукта.')
        return redirect('catalog:product_detail', pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Продукт обновлён.')
            return redirect('catalog:product_detail', pk=pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'catalog/product_form.html', {'form': form})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.owner != request.user and not request.user.has_perm('catalog.delete_product'):
        messages.error(request, 'У вас нет прав на удаление этого продукта.')
        return redirect('catalog:product_detail', pk=pk)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Продукт удалён.')
        return redirect('catalog:product_list')
    return render(request, 'catalog/product_delete.html', {'product': product})


# ---------- Модерация ----------

@login_required
@permission_required('catalog.can_unpublish_product', raise_exception=True)
def moderation_list(request):
    products = Product.objects.all().order_by('-pk')
    return render(request, 'catalog/moderation_list.html', {'products': products})


@login_required
@permission_required('catalog.can_unpublish_product', raise_exception=True)
def product_unpublish(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_published = False
    product.save()
    messages.success(request, f'Продукт «{product.name}» снят с публикации.')
    return redirect('catalog:moderation_list')


@login_required
@permission_required('catalog.can_unpublish_product', raise_exception=True)
def product_publish(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_published = True
    product.save()
    messages.success(request, f'Продукт «{product.name}» опубликован.')
    return redirect('catalog:moderation_list')

