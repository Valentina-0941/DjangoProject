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
        .annotate(average=Avg('salary_from'))
        .order_by('year')
    )

    # Преобразуем данные в словарь для удобства использования в графике
    result = {
        entry['year']: {'average': round(entry['average'], 2)} for entry in salary_data
    }

    return result


def get_currency_rates():
    # Получение данных о курсах валют с сайта Центробанка
    url = 'https://www.cbr.ru/currency_base/daily/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Парсинг данных о курсах валют
    currency_rates = {}
    for row in soup.find_all('tr')[1:]:
        columns = row.find_all('td')
        currency_code = columns[1].text.strip()
        rate = columns[4].text.strip()
        currency_rates[currency_code] = float(rate.replace(',', '.'))

    return currency_rates


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


def convert_currency(amount, currency, rates):
    # Перевод суммы в рубли по курсу
    return amount * rates[currency]


def geography(request):
    return render(request, 'vacancies/geography.html')


def skills(request):
    return render(request, 'vacancies/skills.html')


def latest_vacancies(request):
    return render(request, 'vacancies/latest_vacancies.html')
