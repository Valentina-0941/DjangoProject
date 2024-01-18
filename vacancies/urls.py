from django.urls import path
from .views import vacancy_list

urlpatterns = [
    path('vacancies/', vacancy_list, name='vacancy_list')
]
