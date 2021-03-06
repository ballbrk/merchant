# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-22 21:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('billing', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='pinrefund',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pin_refunds', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pincustomer',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customers', to='billing.PinCard'),
        ),
        migrations.AddField(
            model_name='pincustomer',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pin_customer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pincharge',
            name='card',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='charges', to='billing.PinCard'),
        ),
        migrations.AddField(
            model_name='pincharge',
            name='customer',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customers', to='billing.PinCustomer'),
        ),
        migrations.AddField(
            model_name='pincharge',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pin_charges', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pincard',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pin_cards', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paylaneauthorization',
            name='transaction',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='billing.PaylaneTransaction'),
        ),
        migrations.AddField(
            model_name='order',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='billing_order', to='contenttypes.ContentType'),
        ),
    ]
