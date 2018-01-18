# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-27 16:30
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0005_auto_20171227_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='base_amount',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), default_currency='EUR', max_digits=10),
        ),
        migrations.AddField(
            model_name='order',
            name='base_amount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €'), ('USD', 'USD $')], default='EUR', editable=False, max_length=3),
        ),
        migrations.AddField(
            model_name='order',
            name='tax_amount',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), default_currency='EUR', max_digits=10),
        ),
        migrations.AddField(
            model_name='order',
            name='tax_amount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €'), ('USD', 'USD $')], default='EUR', editable=False, max_length=3),
        ),
    ]
