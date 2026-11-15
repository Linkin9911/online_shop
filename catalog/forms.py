from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from catalog.models import Product

# Список запрещённых слов вынесен в константу,
# используется для проверки name и description (регистр игнорируется)
FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


def check_forbidden_words(value: str) -> None:
    """Проверяет, что в тексте нет запрещённых слов в любом регистре."""
    lowered = value.lower()
    for word in FORBIDDEN_WORDS:
        if word in lowered:
            raise ValidationError(
                f'Слово «{word}» запрещено в названии и описании продукта.'
            )


def validate_image_size(image):
    """Изображение не должно превышать 5 МБ."""
    max_size = 5 * 1024 * 1024  # 5 МБ
    if image.size > max_size:
        raise ValidationError("Размер файла не должен превышать 5 МБ.")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "image", "price", "is_published"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Задание 3: стилизация всех полей через __init__,
        # чтобы формы выглядели единообразно на всей платформе
        for field_name, field in self.fields.items():
            if field_name != "is_published":
                field.widget.attrs.setdefault("class", "form-control")
            # чекбокс оставляем элементом формы, но задаём класс
            else:
                field.widget.attrs.setdefault("class", "form-check-input")

    def clean_name(self):
        name = self.cleaned_data["name"]
        check_forbidden_words(name)
        return name

    def clean_description(self):
        description = self.cleaned_data["description"]
        check_forbidden_words(description)
        return description

    def clean_price(self):
        # Задание 2: цена не может быть отрицательной
        price = self.cleaned_data["price"]
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_image(self):
        # Дополнительное задание: формат и размер
        image = self.cleaned_data.get("image")
        if image:
            validate_image_size(image)
        return image
