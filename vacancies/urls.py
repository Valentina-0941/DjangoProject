from django.urls import path
from .views import vacancy_list, index, demand, geography, skills, latest_vacancies

urlpatterns = [
    path('vacancies/', vacancy_list, name='vacancy_list'),
    path('', index, name='index'),
    path('demand/', demand, name='demand'),
    path('geography/', geography, name='geography'),
    path('skills/', skills, name='skills'),
    path('latest_vacancies/', latest_vacancies, name='latest_vacancies'),
]
