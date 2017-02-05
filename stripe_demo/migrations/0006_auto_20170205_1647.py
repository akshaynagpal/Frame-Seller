# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-05 21:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_demo', '0005_auto_20170203_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
