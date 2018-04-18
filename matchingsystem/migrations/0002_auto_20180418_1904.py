# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-18 19:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matchingsystem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Female',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Leader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='leaders',
            fields=[
                ('student_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='matchingsystem.Student')),
                ('assigned', models.IntegerField(choices=[(0, '0'), (1, '1')], default=0)),
            ],
            bases=('matchingsystem.student',),
        ),
        migrations.CreateModel(
            name='members',
            fields=[
                ('student_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='matchingsystem.Student')),
                ('assigned', models.IntegerField(choices=[(0, '0'), (1, '1')], default=0)),
            ],
            bases=('matchingsystem.student',),
        ),
        migrations.CreateModel(
            name='Project_assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_leader', models.IntegerField(choices=[(0, '0'), (1, '1')], default=0)),
                ('module', models.ManyToManyField(help_text='Modules the student is enrolled in', to='matchingsystem.Module')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='matchingsystem.Project')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], help_text='Student Gender', max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='project_assignment',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='matchingsystem.Student'),
        ),
        migrations.AddField(
            model_name='leader',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='matchingsystem.Student'),
        ),
        migrations.AddField(
            model_name='female',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='matchingsystem.Student'),
        ),
    ]
