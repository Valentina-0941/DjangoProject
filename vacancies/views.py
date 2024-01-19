import base64
import requests
from io import BytesIO
from django.db.models import Avg, Count, Sum
from django.db.models.functions import ExtractYear
from django.shortcuts import render
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse
from .models import Vacancies
from bs4 import BeautifulSoup


def vacancy_list(request):
    vacancies = Vacancies.objects.all()
    return render(request, 'vacancies/vacancy_list.html', {'vacancies': vacancies})


def index(request):
    return render(request, 'vacancies/index.html')


def demand(request):
    # Получаем данные для динамики зарплат
    salary_data = get_salary_dynamics()

    # Генерируем график
    chart = generate_chart(salary_data)

    # Добавляем данные для таблицы в контекст
    table_data = [{'year': year, 'average_salary': data['average']} for year, data in salary_data.items()]

    context = {
        'chart': chart,
        'table_data': table_data,
    }

    return render(request, 'vacancies/demand.html', context)


def get_salary_dynamics():
    # Используем агрегацию для вычисления средней зарплаты для каждого года
    salary_data = (
        Vacancies.objects
        .filter(salary_from__isnull=False)  # Исключаем вакансии без указания зарплаты
        .annotate(year=ExtractYear('published_at'))  # Извлекаем год из даты публикации
        .values('year')
        .annotate(average_salary=Avg('salary_from'), total_count=Count('salary_from'), course=Avg('course'))
        .order_by('year')
    )

    # Преобразуем данные в словарь для удобства использования в графике
    result = {}
    for entry in salary_data:
        year = entry['year']
        average_salary = entry['average_salary']
        course = entry['course']

        # Умножаем среднюю зарплату на курс
        if average_salary is not None and course is not None:
            average_salary_rub = average_salary * course
            result[year] = {'average': round(average_salary_rub, 2), 'total_count': entry['total_count']}

    return result


def generate_chart(salary_data):
    if salary_data:
        years = sorted(list(salary_data.keys()))
        averages = [salary_data[year]['average'] for year in years]

        # Построение графика
        figure = {
            'data': [{
                'x': years,
                'y': averages,
                'type': 'scatter',
                'mode': 'lines+markers',
                'marker': {'color': 'blue'},
                'line': {'shape': 'linear'},
            }],
            'layout': {
                'title': 'Динамика уровня зарплат по годам',
                'xaxis': {'title': 'Год'},
                'yaxis': {'title': 'Средняя зарплата (рубли)'},
            },
        }

        return figure
    else:
        return None



def geography(request):
    return render(request, 'vacancies/geography.html')


def skills(request):
    return render(request, 'vacancies/skills.html')


def latest_vacancies(request):
    return render(request, 'vacancies/latest_vacancies.html')
