from django.db import models
from django.core.validators import FileExtensionValidator


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="наименование")
    description = models.TextField(verbose_name="описание")
    image = models.ImageField(
        upload_to="products/",
        verbose_name="изображение",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="цена")
    is_published = models.BooleanField(default=False, verbose_name="опубликован")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
