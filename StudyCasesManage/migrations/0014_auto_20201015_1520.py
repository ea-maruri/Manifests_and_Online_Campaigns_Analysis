# Generated by Django 3.1.1 on 2020-10-15 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudyCasesManage', '0013_auto_20201007_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]