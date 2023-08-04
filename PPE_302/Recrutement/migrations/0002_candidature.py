# Generated by Django 4.2.1 on 2023-06-27 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Inscription', '0002_candidat'),
        ('Recrutement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documents', models.FileField(upload_to='documents/')),
                ('candidat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inscription.candidat')),
                ('offre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Recrutement.offre')),
            ],
        ),
    ]