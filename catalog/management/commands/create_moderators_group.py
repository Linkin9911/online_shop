from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создаёт группу «Модератор продуктов» и назначает ей права'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        can_unpublish = Permission.objects.get(codename='can_unpublish_product')
        delete_product = Permission.objects.get(codename='delete_product')

        group.permissions.set([can_unpublish, delete_product])

        if created:
            self.stdout.write(self.style.SUCCESS('Группа «Модератор продуктов» создана, права назначены'))
        else:
            self.stdout.write(self.style.SUCCESS('Группа «Модератор продуктов» уже существует, права обновлены'))
