import csv
from django.db import transaction
from django.utils.dateparse import parse_datetime
from .models import Vacancies
from tqdm import tqdm


def import_vacancies_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Пропускаем заголовок

        batch_size = 10000  # Экспериментируйте с этим значением
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

                vacancy = Vacancies(
                    name=name,
                    key_skills=key_skills,
                    salary_from=salary_from,
                    salary_to=salary_to,
                    salary_currency=salary_currency,
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
