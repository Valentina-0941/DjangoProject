from django.db import models


class Vacancies(models.Model):
    name = models.CharField(max_length=255)
    key_skills = models.CharField(max_length=255)
    salary_from = models.FloatField(null=True, blank=True)
    salary_to = models.FloatField(null=True, blank=True)
    salary_currency = models.CharField(max_length=10)
    area_name = models.CharField(max_length=255)
    published_at = models.DateTimeField()

    def __str__(self):
        return self.name
