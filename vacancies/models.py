from django.db import models


class CurrencyRate(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(null=True, blank=True)
    currency_code = models.CharField(max_length=10)
    units = models.IntegerField(default=0)
    rate = models.FloatField(default=0)

    def __str__(self):
        return f'{self.currency_code} - {self.rate}'


class Vacancies(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    key_skills = models.CharField(max_length=255)
    salary_from = models.FloatField(null=True, blank=True)
    salary_to = models.FloatField(null=True, blank=True)
    salary_currency = models.CharField(max_length=10)
    area_name = models.CharField(max_length=255)
    published_at = models.DateTimeField()
    course = models.ForeignKey(CurrencyRate, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
