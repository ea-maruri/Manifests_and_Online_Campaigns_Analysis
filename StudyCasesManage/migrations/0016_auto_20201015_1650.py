# Generated by Django 3.1.1 on 2020-10-15 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudyCasesManage', '0015_auto_20201015_1623'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialmediaaccount',
            name='description',
        ),
        migrations.AddField(
            model_name='socialmediaaccount',
            name='account',
            field=models.CharField(default='Twitter', max_length=40),
        ),
    ]