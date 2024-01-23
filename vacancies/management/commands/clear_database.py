from django.core.management.base import BaseCommand
from vacancies.models import Vacancies
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = 'Clear database Vacancies'

    def handle(self, *args, **options):
        try:
            # Очищаем все записи в модели Vacancies
            Vacancies.objects.all().delete()

            self.stdout.write(self.style.SUCCESS('База данных успешно очищена.'))
        except OperationalError as e:
            self.stderr.write(self.style.ERROR(f'Произошла ошибка при очистке базы данных: {e}'))
