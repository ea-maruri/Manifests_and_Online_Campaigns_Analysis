# Generated by Django 3.1.1 on 2020-10-17 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudyCasesManage', '0027_auto_20201016_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.BigAutoField(default=0, primary_key=True, serialize=False),
        ),
    ]