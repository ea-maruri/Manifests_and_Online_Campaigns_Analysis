# Generated by Django 3.1.1 on 2020-10-06 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StudyCasesManage', '0003_auto_20201005_1814'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='post',
            new_name='post_as_json',
        ),
        migrations.AddField(
            model_name='manifest',
            name='location',
            field=models.CharField(default='./', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='manifest',
            name='name',
            field=models.CharField(default='Manifest', max_length=45),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='candidate',
            name='campaign_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='StudyCasesManage.campaign', verbose_name='Campaign'),
        ),
        migrations.AlterField(
            model_name='manifest',
            name='candidate_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StudyCasesManage.candidate', verbose_name='Candidate'),
        ),
        migrations.AlterField(
            model_name='manifest',
            name='type',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='socialmediaaccount',
            name='candidate_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='StudyCasesManage.candidate', verbose_name='Candidate'),
        ),
        migrations.AlterField(
            model_name='socialmediaaccount',
            name='created_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='timeline',
            name='social_media_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StudyCasesManage.socialmediaaccount', verbose_name='Timeline'),
        ),
    ]
