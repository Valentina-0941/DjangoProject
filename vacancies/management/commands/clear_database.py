import json
from django.core.management.base import BaseCommand
from envs.MlAgent.Lib import os

from vacancies.models import Vacancies
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = 'Clear database Vacancies'

    def handle(self, *args, **options):
        json_file_path = os.path.join('vacancies', 'data', 'vacancies_data.json')

        try:
            # Очищаем содержимое JSON-файла
            with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
                json.dump([], jsonfile)

            self.stdout.write(self.style.SUCCESS(f'JSON-файл {json_file_path} успешно очищен.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Произошла ошибка при очистке JSON-файла: {e}'))

    # def handle(self, *args, **options):
    #     try:
    #         # Очищаем все записи в модели Vacancies
    #         # Vacancies.objects.all().delete()
    #         self.stdout.write(self.style.SUCCESS('База данных успешно очищена.'))
    #     except OperationalError as e:
    #         self.stderr.write(self.style.ERROR(f'Произошла ошибка при очистке базы данных: {e}'))
