# Generated by Django 5.0.1 on 2024-01-23 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0006_currencyrate_alter_vacancies_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='currencyrate',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='currencyrate',
            name='units',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='currencyrate',
            name='currency_code',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='currencyrate',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='currencyrate',
            name='rate',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='vacancies',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
