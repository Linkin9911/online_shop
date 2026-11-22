from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    """Регистрация: email + пароль + подтверждение пароля."""

    class Meta:
        model = User
        fields = ('email',)

    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с такой почтой уже зарегистрирован.')
        return email


class UserLoginForm(AuthenticationForm):
    """Вход по email и паролю."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Электронная почта'
