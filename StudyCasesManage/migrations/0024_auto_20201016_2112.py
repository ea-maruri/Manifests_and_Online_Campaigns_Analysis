# Generated by Django 3.1.1 on 2020-10-17 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudyCasesManage', '0023_auto_20201016_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.BigIntegerField(default=0, primary_key=True, serialize=False),
        ),
    ]