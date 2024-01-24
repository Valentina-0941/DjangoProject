import base64
import requests
from io import BytesIO
from django.db.models import Avg, Count, Sum
from django.db.models.functions import ExtractYear
from django.shortcuts import render
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse
from .models import Vacancies, CurrencyRate
from bs4 import BeautifulSoup
from .demand import get_salary_dynamics, get_demand_data


def vacancy_list(request):
    vacancies = Vacancies.objects.all()
    return render(request, 'vacancies/vacancy_list.html', {'vacancies': vacancies})


def courses_list(request):
    courses = CurrencyRate.objects.all()
    return render(request, 'vacancies/course_list.html', {'courses': courses})


def index(request):
    return render(request, 'vacancies/index.html')


def demand(request):

    salary_data = get_salary_dynamics()
    salary_level_by_year = generate_chart(salary_data, 'Динамика уровня зарплат по годам')
    table_salary_data = [{'year': year, 'average_salary': data['average']} for year, data in salary_data.items()]

    number_vacancies = get_demand_data()
    number_of_vacancies_by_year = generate_chart(number_vacancies, 'Динамика количества вакансий по годам')
    table_number_vacancies = [{'year': year, 'average_salary': data['average']} for year, data in number_of_vacancies_by_year.items()]

    context = {
        'salary_level_by_year': salary_level_by_year,
        'table_salary_data': table_salary_data,
        'number_of_vacancies_by_year': number_of_vacancies_by_year,
        'table_number_vacancies': table_number_vacancies,
    }

    return render(request, 'vacancies/demand.html', context)


def generate_chart(salary_data, title):
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
                'title': title,
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
