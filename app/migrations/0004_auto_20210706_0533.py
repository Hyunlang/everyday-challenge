# Generated by Django 3.2.5 on 2021-07-06 05:33

import app.enums
from django.db import migrations, models
import enumfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_subject_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='content',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='status',
            field=enumfields.fields.EnumField(default='pending', enum=app.enums.ChallengeStatus, max_length=16),
        ),
    ]