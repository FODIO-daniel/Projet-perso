# Generated by Django 4.2.1 on 2023-07-04 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inscription', '0005_remove_personne_valide'),
    ]

    operations = [
        migrations.AddField(
            model_name='personne',
            name='valide',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
