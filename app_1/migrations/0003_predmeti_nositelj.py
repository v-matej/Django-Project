# Generated by Django 4.2.1 on 2023-06-06 17:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0002_alter_korisnik_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='predmeti',
            name='nositelj',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]