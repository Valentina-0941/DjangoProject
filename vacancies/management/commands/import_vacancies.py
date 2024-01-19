from django.core.management.base import BaseCommand
from vacancies.utils import import_vacancies_from_csv


class Command(BaseCommand):
    help = 'Import vacancies from CSV file'

    def handle(self, *args, **options):
        file_path = 'test.csv'
        # profession_filter = ["разработчик игр", "gamedev", "game", "unity", "игр", "unreal"]
        import_vacancies_from_csv(file_path)
        self.stdout.write(self.style.SUCCESS('Successfully imported vacancies'))
