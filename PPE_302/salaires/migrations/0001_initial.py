# Generated by Django 4.2.1 on 2023-06-25 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Salaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=30)),
                ('prenom', models.CharField(max_length=30)),
                ('date_paiement', models.DateField()),
                ('avance_salaire', models.BooleanField(null=True)),
                ('salaire_de_base', models.DecimalField(decimal_places=2, max_digits=10)),
                ('prime', models.DecimalField(decimal_places=2, max_digits=10)),
                ('augmentation', models.DecimalField(decimal_places=2, max_digits=10)),
                ('nom_employeur', models.CharField(default='Inconnu', max_length=30)),
                ('mode_paiement', models.CharField(default='Carte bancaire', max_length=30)),
                ('salaire_net_a_payer', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('temps_de_travail', models.PositiveIntegerField(default=0)),
                ('temps_de_conge', models.PositiveIntegerField(default=0)),
                ('fonction', models.CharField(default=False, max_length=30)),
            ],
        ),
    ]
