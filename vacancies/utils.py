import csv
from tqdm import tqdm
from .models import Vacancies
from django.utils.dateparse import parse_datetime


def import_vacancies_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)

        for row in tqdm(csv_reader, desc='Импорт данных', unit=' строк'):
            try:
                if not row[0] or not row[-1]:
                    print(f"Пропущена строка с недостающими данными: {row}")
                    continue

                key_skills = [skill.strip() for skill in row[1].split('\n')] if row[1] else []
                published_at = parse_datetime(row[-1])

                Vacancies.objects.create(
                    name=row[0],
                    key_skills=key_skills,
                    salary_from=float(row[2]) if row[2] else None,
                    salary_to=float(row[3]) if row[3] else None,
                    salary_currency=row[4],
                    area_name=row[5],
                    published_at=published_at
                )
            except Exception as e:
                print(f"Произошла ошибка при обработке строки: {row}. Ошибка: {e}")
