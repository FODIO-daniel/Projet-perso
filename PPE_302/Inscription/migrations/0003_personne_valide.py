# Generated by Django 4.2.1 on 2023-07-04 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inscription', '0002_candidat'),
    ]

    operations = [
        migrations.AddField(
            model_name='personne',
            name='valide',
            field=models.BooleanField(default=None, null=True),
        ),
    ]
