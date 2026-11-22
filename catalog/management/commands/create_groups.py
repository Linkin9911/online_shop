from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создаёт группу «Модератор продуктов» с нужными правами'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        perm_unpublish = Permission.objects.get(codename='can_unpublish_product')
        perm_delete = Permission.objects.get(codename='delete_product')

        group.permissions.add(perm_unpublish, perm_delete)

        if created:
            self.stdout.write(self.style.SUCCESS('Группа «Модератор продуктов» создана'))
        else:
            self.stdout.write('Группа уже существовала, права обновлены')
