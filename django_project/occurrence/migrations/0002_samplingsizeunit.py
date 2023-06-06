# Generated by Django 4.1.7 on 2023-06-03 11:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('occurrence', '0001_survey_method_migrations'),
    ]

    operations = [
        migrations.CreateModel(
            name='SamplingSizeUnit',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('unit', models.CharField(max_length=4, unique=True)),
            ],
            options={
                'verbose_name': 'Sampling size unit',
                'verbose_name_plural': 'Sampling size units',
                'db_table': 'sampling_size_unit',
            },
        ),
    ]