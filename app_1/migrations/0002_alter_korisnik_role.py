# Generated by Django 4.2.1 on 2023-06-05 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='korisnik',
            name='role',
            field=models.CharField(choices=[('prof', 'profesor'), ('stu', 'student'), ('admin', 'administrator')], max_length=50),
        ),
    ]