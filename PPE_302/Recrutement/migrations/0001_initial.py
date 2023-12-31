# Generated by Django 4.2.1 on 2023-06-27 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Inscription', '0002_candidat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('demande_dossier', models.BooleanField(default=False)),
                ('demande_document', models.BooleanField(default=False)),
                ('recruteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inscription.recruteur')),
            ],
        ),
    ]
