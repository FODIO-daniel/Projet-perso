# Generated by Django 4.2.1 on 2023-06-27 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recrutement', '0004_candidature_date_soumission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offre',
            name='demande_document',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='offre',
            name='demande_dossier',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
