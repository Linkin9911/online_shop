from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ['email']
    list_display = ('email', 'phone_number', 'country')

    # Форма редактирования существующего пользователя
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Дополнительно', {'fields': ('avatar', 'phone_number', 'country')}),
        ('Разрешения', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    # Форма создания пользователя (та страница, на которой падала ошибка)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
