# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-27 12:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0004_order_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-created',), 'verbose_name': 'Orden', 'verbose_name_plural': 'Orders'},
        ),
    ]
