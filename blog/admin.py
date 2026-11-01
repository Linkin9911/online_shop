from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'views', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'

    # ✅ Выносим readonly_fields на верхний уровень
    readonly_fields = ('views', 'created_at')

    # Поля, которые будут видны при редактировании
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'content', 'preview_image')
        }),
        ('Настройки публикации', {
            'fields': ('is_published',),
            'classes': ('collapse',)  # Свернутый блок
        }),
        ('Статистика', {
            'fields': ('views', 'created_at'),
            'classes': ('collapse',),
            # ❌ Удаляем 'readonly_fields' отсюда — теперь он сверху
        }),
    )
