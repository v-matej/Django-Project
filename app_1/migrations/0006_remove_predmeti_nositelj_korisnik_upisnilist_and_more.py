# Generated by Django 4.2.1 on 2023-06-08 18:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0005_alter_predmetiassignment_unique_together_upisnilist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='predmeti',
            name='nositelj',
        ),
        migrations.AddField(
            model_name='korisnik',
            name='UpisniList',
            field=models.ManyToManyField(related_name='korisnici', through='app_1.UpisniList', to='app_1.predmeti'),
        ),
        migrations.AddField(
            model_name='upisnilist',
            name='semester',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='upisnilist',
            name='korisnik',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upisni_list', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='upisnilist',
            unique_together={('predmet', 'korisnik', 'semester')},
        ),
    ]
