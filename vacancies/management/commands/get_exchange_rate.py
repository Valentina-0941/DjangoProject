from django.core.management.base import BaseCommand
from vacancies.utils import get_currency_rate


class Command(BaseCommand):
    help = 'Get the exchange rate and write it to the database'

    def handle(self, *args, **options):
        get_currency_rate()
        self.stdout.write(self.style.SUCCESS('Successfully imported vacancies'))
