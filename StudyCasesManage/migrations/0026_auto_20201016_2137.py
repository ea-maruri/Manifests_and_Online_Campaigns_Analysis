# Generated by Django 3.1.1 on 2020-10-17 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudyCasesManage', '0025_post_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.BigAutoField(default=0, primary_key=True, serialize=False),
        ),
    ]
