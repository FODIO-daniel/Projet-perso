# Generated by Django 4.2.1 on 2023-07-05 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employeur', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagerie',
            name='date_message',
            field=models.DateTimeField(null=True),
        ),
    ]
