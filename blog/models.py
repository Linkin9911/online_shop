from django.db import models
from django.utils import timezone

class BlogPost(models.Model):
    title = models.CharField(max_length=200)  # Заголовок
    content = models.TextField()  # Текст статьи
    preview_image = models.ImageField(upload_to='blog_previews/', blank=True, null=True)  # Картинка
    created_at = models.DateTimeField(default=timezone.now)  # Дата создания
    is_published = models.BooleanField(default=False)  # Флаг публикации (True/False)
    views = models.PositiveIntegerField(default=0)  # Счётчик просмотров

    class Meta:
        verbose_name = 'Блоговая запись'
        verbose_name_plural = 'Блоговые записи'
        ordering = ['-created_at']  # Сортировка: новые сверху

    def __str__(self):
        return self.title
