# Generated by Django 3.1.1 on 2020-10-06 22:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudyCasesManage', '0004_auto_20201006_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manifest',
            name='collect_date',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='timeline',
            name='collect_date',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
    ]
