# Generated by Django 4.2.10 on 2024-04-26 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MediGuard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practice',
            name='phone',
            field=models.CharField(default='', max_length=15),
        ),
    ]