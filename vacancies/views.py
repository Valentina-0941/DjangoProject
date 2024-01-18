from django.shortcuts import render
from .models import Vacancies


def vacancy_list(request):
    vacancies = Vacancies.objects.all()
    return render(request, 'vacancies/vacancy_list.html', {'vacancies': vacancies})
