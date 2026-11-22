from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Product(models.Model):
    """Товар магазина: до одобрения модератором находится в статусе 'На модерации'."""

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Опубликован'
        MODERATION = 'moderation', 'На модерации'

    name = models.CharField(
        max_length=100,
        verbose_name='Наименование',
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена',
    )
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name='Изображение',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,      # нужно, чтобы миграция прошла для уже созданных товаров
        blank=True,
        verbose_name='Владелец',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.MODERATION,
        verbose_name='Статус',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения',
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-created_at']
        permissions = [
            ('can_unpublish_product', 'Может отменять публикацию продукта'),
        ]

    def __str__(self):
        return self.name

    # --- Совместимость со старым полем is_published ---

    @property
    def is_published(self):
        """В шаблонах и вьюхах можно по-прежнему читать product.is_published."""
        return self.status == self.Status.ACTIVE

    @is_published.setter
    def is_published(self, value):
        """А присваивание product.is_published = False автоматически
        переводит товар в статус 'На модерации', True — в 'Опубликован'."""
        self.status = self.Status.ACTIVE if value else self.Status.MODERATION
