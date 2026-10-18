from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product, Category


class Command(BaseCommand):
    help = 'Удаляет все продукты и категории, затем загружает тестовые данные из фикстуры'

    def handle(self, *args, **options):
        self.stdout.write('Удаление существующих данных...')
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write('Загрузка фикстуры initial_data.json...')
        call_command('loaddata', 'initial_data')

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно загружены!'))
