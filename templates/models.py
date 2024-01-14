from django.db import models

class Person(models.Model):
    first_name = models.CharField("Имя", max_length=64)
    last_name = models.CharField("Фамилия", max_length=64)
    age = models.IntegerField("Возраст")
    job = models.CharField("Должность", max_length=64)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Человек"
        verbose_name_plural = "Люди"

