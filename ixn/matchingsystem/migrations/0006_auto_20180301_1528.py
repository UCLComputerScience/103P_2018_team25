# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-01 15:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchingsystem', '0005_project_project_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='student_id',
            new_name='student_code',
        ),
        migrations.AddField(
            model_name='student',
            name='forename',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='surname',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]