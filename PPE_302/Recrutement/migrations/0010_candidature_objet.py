# Generated by Django 4.2.1 on 2023-06-28 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recrutement', '0009_candidature_age_candidature_email_candidature_nom_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidature',
            name='objet',
            field=models.TextField(null=True),
        ),
    ]
