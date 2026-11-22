from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from config.settings import DEFAULT_FROM_EMAIL
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from users.forms import UserRegisterForm, UserLoginForm, UserProfileForm



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()

                send_mail(
                    subject='Добро пожаловать в наш магазин!',
                    message=(
                        f'Здравствуйте, {user.email}!\n\n'
                        'Ваша учётная запись успешно создана. '
                        'Спасибо за регистрацию!'
                    ),
                    from_email=DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )

                login(request, user)
                return redirect('catalog:home')  # поправь на имя своего роута списка товаров
            except Exception:
                form.add_error(None, 'Не удалось создать аккаунт. Попробуйте ещё раз.')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # USERNAME_FIELD
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('catalog:home')
            form.add_error(None, 'Неверная почта или пароль.')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('catalog:home')

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлён.')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})
