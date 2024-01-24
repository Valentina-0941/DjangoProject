from bs4 import BeautifulSoup
from django.contrib.sites import requests
from .models import Vacancies, CurrencyRate
from django.db.models import Q
from tqdm import tqdm
import logging
import requests
import csv
from dateutil import parser
from django.db import transaction
from django.utils import timezone


# Настройка журнала
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def import_vacancies_from_csv(file_path):
    vacancies_to_create = []

    with open(file_path, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)

        for row in tqdm(csv_reader, desc="Чтение CSV"):
            try:
                # Парсим дату с учетом временной зоны
                published_at = parser.parse(row['published_at']).astimezone(timezone.get_current_timezone())
            except ValueError:
                print(f"Не удалось распознать дату: {row['published_at']}")
                continue

            vacancy = Vacancies(
                name=row['name'],
                key_skills=row['key_skills'],
                salary_from=float(row['salary_from']) if row['salary_from'] else None,
                salary_to=float(row['salary_to']) if row['salary_to'] else None,
                salary_currency=row['salary_currency'],
                area_name=row['area_name'],
                published_at=published_at,
            )
            vacancies_to_create.append(vacancy)

    # Массово создаем объекты Vacancy внутри транзакции
    with transaction.atomic():
        Vacancies.objects.bulk_create(vacancies_to_create, batch_size=1000)

    print("Импорт вакансий завершен.")




def process_date(date):
    first_day_of_month = date.replace(day=1)
    url = f'https://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To={first_day_of_month.strftime("%d.%m.%Y")}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    currency_rates = []

    for row in soup.find_all('tr')[1:]:
        columns = row.find_all('td')
        currency_code = columns[1].text.strip()
        units = int(columns[2].text.strip())
        rate = columns[4].text.strip()

        try:
            # Преобразование курса в число с плавающей запятой
            rate_float = float(rate.replace(',', '.'))
        except ValueError:
            # Запись ошибки и переход к следующей итерации в случае неудачи
            logging.error(f"Не удалось преобразовать курс '{rate}' в число для валюты '{currency_code}' на {date}")
            continue

        currency_rates.append(
            CurrencyRate(
                date=date,
                currency_code=currency_code,
                units=units,
                rate=rate_float
            )
        )

    # Создаем записи в базе данных
    CurrencyRate.objects.bulk_create(currency_rates)


def get_currency_rate():
    unique_dates = Vacancies.objects.filter(
        ~Q(course__isnull=False) & Q(salary_currency__isnull=False)
    ).dates('published_at', 'month')

    for date in tqdm(unique_dates, desc='Заполнение курса валют', unit=' дат'):
        try:
            process_date(date)
        except Exception as e:
            logging.error(f"Ошибка при обработке даты {date}: {e}")
