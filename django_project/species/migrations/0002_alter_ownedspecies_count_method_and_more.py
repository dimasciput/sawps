# Generated by Django 4.1.7 on 2023-06-11 10:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("population_data", "0001_initial"),
        ("property", "0002_alter_parcel_parcel_type_alter_parcel_property"),
        ("species", "0001_species_models"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ownedspecies",
            name="count_method",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="population_data.countmethod",
            ),
        ),
        migrations.AlterField(
            model_name="ownedspecies",
            name="management_status",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="species.managementstatus",
            ),
        ),
        migrations.AlterField(
            model_name="ownedspecies",
            name="nature_of_population",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="population_data.natureofpopulation",
            ),
        ),
        migrations.AlterField(
            model_name="ownedspecies",
            name="property",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="property.property"
            ),
        ),
        migrations.AlterField(
            model_name="ownedspecies",
            name="taxon",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="species.taxon"
            ),
        ),
        migrations.AlterField(
            model_name="ownedspecies",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
