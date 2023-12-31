# Generated by Django 4.2.1 on 2023-07-05 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Inscription', '0006_personne_valide'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messagerie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objet', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('destinataire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_recus', to='Inscription.personne')),
                ('expediteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_envoyes', to='Inscription.personne')),
            ],
        ),
    ]
