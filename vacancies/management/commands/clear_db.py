from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
from tqdm import tqdm

class Command(BaseCommand):
    help = 'Clear database Vacancies'

    def handle(self, *args, **options):
        try:

            with connections['default'].cursor() as cursor:
                cursor.execute('DELETE FROM vacancies_vacancies')

            self.stdout.write(self.style.SUCCESS('База данных успешно очищена.'))
        except OperationalError as e:
            self.stderr.write(self.style.ERROR(f'Произошла ошибка при очистке базы данных: {e}'))
