import csv
import requests
from django.db import transaction
from django.utils.dateparse import parse_datetime
from .models import Vacancies
from tqdm import tqdm
from bs4 import BeautifulSoup


def import_vacancies_from_csv(file_path):
    def get_currency_rate_for_date(date_str, currency):

        url = f'https://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To={date_str.strftime("01.%m.%Y")}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for row in soup.find_all('tr')[1:]:
            columns = row.find_all('td')
            currency_code = columns[1].text.strip()
            rate = columns[4].text.strip()

            if currency_code == currency:
                return float(rate.replace(',', '.'))

        return None

    with open(file_path, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Пропускаем заголовок

        batch_size = 1000  # Экспериментируйте с этим значением
        vacancies_to_create = []

        for row in tqdm(csv_reader, desc='Импорт данных', unit=' строк'):
            try:
                name = row[0]
                key_skills = row[1]
                salary_from = float(row[2]) if row[2] else None
                salary_to = float(row[3]) if row[3] else None
                salary_currency = row[4]
                area_name = row[5]
                published_at = parse_datetime(row[6])

                if salary_currency is not None:
                    course = get_currency_rate_for_date(published_at, salary_currency)
                else:
                    course = 1

                vacancy = Vacancies(
                    name=name,
                    key_skills=key_skills,
                    salary_from=salary_from,
                    salary_to=salary_to,
                    salary_currency=salary_currency,
                    course=course,
                    area_name=area_name,
                    published_at=published_at
                )

                vacancies_to_create.append(vacancy)

                if len(vacancies_to_create) >= batch_size:
                    # Создаем пакет объектов Vacancies в базе данных
                    with transaction.atomic():
                        Vacancies.objects.bulk_create(vacancies_to_create)
                    vacancies_to_create = []

            except Exception as e:
                print(f"Произошла ошибка при обработке строки: {row}. Ошибка: {e}")

        if vacancies_to_create:
            with transaction.atomic():
                Vacancies.objects.bulk_create(vacancies_to_create)
