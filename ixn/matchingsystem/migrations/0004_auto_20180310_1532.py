# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-10 15:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matchingsystem', '0003_student_email'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='student',
            unique_together=set([('tag_like_1', 'tag_like_2')]),
        ),
    ]
