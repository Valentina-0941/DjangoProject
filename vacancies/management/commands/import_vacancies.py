import os

from django.core.management.base import BaseCommand
from vacancies.utils import import_vacancies_from_csv


class Command(BaseCommand):
    help = 'Import vacancies from CSV file'

    def handle(self, *args, **options):
        file_path = 'vacancies.csv'
        json_output_path = os.path.join('vacancies', 'data', 'vacancies_data.json')
        import_vacancies_from_csv(file_path, json_output_path)
        self.stdout.write(self.style.SUCCESS('Successfully imported vacancies'))
