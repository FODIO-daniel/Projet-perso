# Generated by Django 4.2.1 on 2023-06-27 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recrutement', '0005_alter_offre_demande_document_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='offre',
            name='date_offre',
            field=models.DateTimeField(null=True),
        ),
    ]