from django.core.management.base import BaseCommand
from .command_for_users import clear_role_db


class Command(BaseCommand):
    """
    Класс для инициализации баз данных. Каждая база данных создаётся через запуск конкретной функции.
    Подробное описание какая база создаётся и как описано непосредственно в функциях.
    """
    help = '''
    Initialize db 
    Инициализировать базы данных'''

    def handle(self, *args, **options):
        count = clear_role_db()
        self.stdout.write(self.style.SUCCESS(
            f'{count} records deleted from the database.\nЗаписи Ролей в количестве {count} шт. удалены из базы данных.'))

        self.stdout.write(self.style.SUCCESS(
            'Initialize db command executed successfully.\nКоманда инициализации базы данных выполнена успешно.'))
