# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-10 15:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchingsystem', '0002_auto_20180306_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.CharField(default='', help_text='Student Email', max_length=100),
            preserve_default=False,
        ),
    ]
