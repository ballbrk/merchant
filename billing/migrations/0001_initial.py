# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-22 21:38
from __future__ import unicode_literals

from decimal import Decimal
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import django_fsm
import djmoney.models.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AmazonFPSResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyerEmail', models.EmailField(max_length=254)),
                ('buyerName', models.CharField(max_length=75)),
                ('callerReference', models.CharField(max_length=100)),
                ('notificationType', models.CharField(max_length=50)),
                ('operation', models.CharField(max_length=20)),
                ('paymentMethod', models.CharField(max_length=5)),
                ('recipientEmail', models.EmailField(max_length=254)),
                ('recipientName', models.CharField(max_length=75)),
                ('statusCode', models.CharField(max_length=50)),
                ('statusMessage', models.TextField()),
                ('transactionAmount', models.CharField(max_length=20)),
                ('transactionDate', models.DateTimeField()),
                ('transactionId', models.CharField(db_index=True, max_length=50)),
                ('transactionStatus', models.CharField(max_length=50)),
                ('customerEmail', models.EmailField(blank=True, max_length=254, null=True)),
                ('customerName', models.CharField(blank=True, max_length=75, null=True)),
                ('addressFullName', models.CharField(blank=True, max_length=100, null=True)),
                ('addressLine1', models.CharField(blank=True, max_length=100, null=True)),
                ('addressLine2', models.CharField(blank=True, max_length=100, null=True)),
                ('addressState', models.CharField(blank=True, max_length=50, null=True)),
                ('addressZip', models.CharField(blank=True, max_length=25, null=True)),
                ('addressCountry', models.CharField(blank=True, max_length=25, null=True)),
                ('addressPhone', models.CharField(blank=True, max_length=25, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AuthorizeAIMResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_code', models.IntegerField(choices=[(1, 'Approved'), (2, 'Declined'), (3, 'Error'), (4, 'Held for Review')])),
                ('response_reason_code', models.IntegerField(blank=True)),
                ('response_reason_text', models.TextField(blank=True)),
                ('authorization_code', models.CharField(max_length=8)),
                ('address_verification_response', models.CharField(choices=[('A', 'Address(Street) matches,ZIP does not'), ('B', 'Address information not provided for AVS check'), ('E', 'AVS error'), ('G', 'Non-U.S. Card Issuing Bank'), ('N', 'No match on Address(Street) or ZIP'), ('P', 'AVS not applicable for this transactions'), ('R', 'Retry-System unavailable or timed out'), ('S', 'Service not supported by issuer'), ('U', 'Address information is unavailable'), ('W', 'Nine digit Zip matches, Address(Street) does not'), ('X', 'Address(Street) and nine digit ZIP match'), ('Y', 'Address(Street) and five digit ZIP match'), ('Z', 'Five digit Zip matches, Address(Street) does not')], max_length=8)),
                ('transaction_id', models.CharField(max_length=64)),
                ('invoice_number', models.CharField(blank=True, max_length=64)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=16)),
                ('method', models.CharField(blank=True, max_length=255)),
                ('transaction_type', models.CharField(blank=True, max_length=255)),
                ('customer_id', models.CharField(blank=True, max_length=64)),
                ('first_name', models.CharField(blank=True, max_length=64)),
                ('last_name', models.CharField(blank=True, max_length=64)),
                ('company', models.CharField(blank=True, max_length=64)),
                ('address', models.CharField(blank=True, max_length=64)),
                ('city', models.CharField(blank=True, max_length=64)),
                ('state', models.CharField(blank=True, max_length=64)),
                ('zip_code', models.CharField(blank=True, max_length=64)),
                ('country', models.CharField(blank=True, max_length=64)),
                ('phone', models.CharField(blank=True, max_length=64)),
                ('fax', models.CharField(blank=True, max_length=64)),
                ('email', models.EmailField(max_length=254)),
                ('shipping_first_name', models.CharField(blank=True, max_length=64)),
                ('shipping_last_name', models.CharField(blank=True, max_length=64)),
                ('shipping_company', models.CharField(blank=True, max_length=64)),
                ('shipping_address', models.CharField(blank=True, max_length=64)),
                ('shipping_city', models.CharField(blank=True, max_length=64)),
                ('shipping_state', models.CharField(blank=True, max_length=64)),
                ('shipping_zip_code', models.CharField(blank=True, max_length=64)),
                ('shipping_country', models.CharField(blank=True, max_length=64)),
                ('card_code_response', models.CharField(choices=[('', ''), ('M', 'Match'), ('N', 'No Match'), ('P', 'Not Processed'), ('S', 'Should have been present'), ('U', 'Issuer unable to process request')], help_text='Card Code Verification response', max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='EwayResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='GCNewOrderNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notify_type', models.CharField(blank=True, max_length=255)),
                ('serial_number', models.CharField(max_length=255)),
                ('google_order_number', models.CharField(max_length=255)),
                ('buyer_id', models.CharField(max_length=255)),
                ('private_data', models.CharField(blank=True, max_length=255)),
                ('shipping_contact_name', models.CharField(blank=True, max_length=255)),
                ('shipping_address1', models.CharField(blank=True, max_length=255)),
                ('shipping_address2', models.CharField(blank=True, max_length=255)),
                ('shipping_city', models.CharField(blank=True, max_length=255)),
                ('shipping_postal_code', models.CharField(blank=True, max_length=255)),
                ('shipping_region', models.CharField(blank=True, max_length=255)),
                ('shipping_country_code', models.CharField(blank=True, max_length=255)),
                ('shipping_email', models.EmailField(max_length=254)),
                ('shipping_company_name', models.CharField(blank=True, max_length=255)),
                ('shipping_fax', models.CharField(blank=True, max_length=255)),
                ('shipping_phone', models.CharField(blank=True, max_length=255)),
                ('billing_contact_name', models.CharField(blank=True, max_length=255)),
                ('billing_address1', models.CharField(blank=True, max_length=255)),
                ('billing_address2', models.CharField(blank=True, max_length=255)),
                ('billing_city', models.CharField(blank=True, max_length=255)),
                ('billing_postal_code', models.CharField(blank=True, max_length=255)),
                ('billing_region', models.CharField(blank=True, max_length=255)),
                ('billing_country_code', models.CharField(blank=True, max_length=255)),
                ('billing_email', models.EmailField(max_length=254)),
                ('billing_company_name', models.CharField(blank=True, max_length=255)),
                ('billing_fax', models.CharField(blank=True, max_length=255)),
                ('billing_phone', models.CharField(blank=True, max_length=255)),
                ('marketing_email_allowed', models.BooleanField(default=False)),
                ('num_cart_items', models.IntegerField()),
                ('cart_items', models.TextField()),
                ('total_tax', models.DecimalField(blank=True, decimal_places=2, max_digits=16, null=True)),
                ('total_tax_currency', models.CharField(blank=True, max_length=255)),
                ('adjustment_total', models.DecimalField(blank=True, decimal_places=2, max_digits=16, null=True)),
                ('adjustment_total_currency', models.CharField(blank=True, max_length=255)),
                ('order_total', models.DecimalField(blank=True, decimal_places=2, max_digits=16, null=True)),
                ('order_total_currency', models.CharField(blank=True, max_length=255)),
                ('financial_order_state', models.CharField(blank=True, max_length=255)),
                ('fulfillment_order_state', models.CharField(blank=True, max_length=255)),
                ('timestamp', models.CharField(blank=True, max_length=64, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('amount_currency', djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €'), ('USD', 'USD $')], default='EUR', editable=False, max_length=3)),
                ('amount', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), default_currency='EUR', max_digits=10)),
                ('state', django_fsm.FSMField(choices=[('New', 'Nuevo'), ('Completed', 'Completed'), ('No Valid', 'No Valid'), ('Canceled', 'Canceled'), ('Returned', 'Returned'), ('Error', 'Error')], db_index=True, default='New', max_length=50, protected=True, verbose_name='Order State')),
            ],
            options={
                'verbose_name': 'Orden',
                'verbose_name_plural': 'Orders',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='PaylaneAuthorization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_authorization_id', models.BigIntegerField(db_index=True)),
                ('first_authorization', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PaylaneTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.FloatField()),
                ('customer_name', models.CharField(max_length=200)),
                ('customer_email', models.CharField(max_length=200)),
                ('product', models.CharField(max_length=200)),
                ('success', models.BooleanField(default=False)),
                ('error_code', models.IntegerField(default=0)),
                ('error_description', models.CharField(blank=True, max_length=300)),
                ('acquirer_error', models.CharField(blank=True, max_length=40)),
                ('acquirer_description', models.CharField(blank=True, max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='PinCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(db_index=True, editable=False, max_length=32)),
                ('display_number', models.CharField(editable=False, max_length=20)),
                ('expiry_month', models.PositiveSmallIntegerField()),
                ('expiry_year', models.PositiveSmallIntegerField()),
                ('scheme', models.CharField(editable=False, max_length=20)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('address_line1', models.CharField(max_length=255)),
                ('address_line2', models.CharField(blank=True, max_length=255)),
                ('address_city', models.CharField(max_length=255)),
                ('address_postcode', models.CharField(max_length=20)),
                ('address_state', models.CharField(max_length=255)),
                ('address_country', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PinCharge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(editable=False, max_length=32, unique=True)),
                ('success', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=16)),
                ('currency', models.CharField(max_length=3)),
                ('description', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('ip_address', models.GenericIPAddressField()),
                ('created_at', models.DateTimeField()),
                ('status_message', models.CharField(max_length=255)),
                ('error_message', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PinCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=32, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='PinRefund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=32, unique=True)),
                ('success', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=16)),
                ('currency', models.CharField(max_length=3)),
                ('created_at', models.DateTimeField()),
                ('status_message', models.CharField(max_length=255)),
                ('error_message', models.CharField(blank=True, max_length=255, null=True)),
                ('charge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refunds', to='billing.PinCharge')),
            ],
        ),
        migrations.CreateModel(
            name='StripeTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txn_id', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('payment_status', models.CharField(choices=[('New', 'Nuevo'), ('Completed', 'Completed'), ('No Valid', 'No Valid'), ('Canceled', 'Canceled'), ('Returned', 'Returned'), ('Error', 'Error')], db_index=True, default='New', max_length=200)),
                ('payment_message', models.CharField(blank=True, max_length=200, null=True)),
                ('info', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorldPayResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installation_id', models.CharField(max_length=64)),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('cart_id', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=16)),
                ('currency', models.CharField(max_length=64)),
                ('amount_string', models.CharField(max_length=64)),
                ('auth_mode', models.CharField(max_length=64)),
                ('test_mode', models.CharField(max_length=64)),
                ('transaction_id', models.CharField(max_length=64)),
                ('transaction_status', models.CharField(max_length=64)),
                ('transaction_time', models.CharField(max_length=64)),
                ('auth_amount', models.DecimalField(decimal_places=2, max_digits=16)),
                ('auth_currency', models.CharField(max_length=64)),
                ('auth_amount_string', models.CharField(max_length=64)),
                ('raw_auth_message', models.CharField(max_length=255)),
                ('raw_auth_code', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('post_code', models.CharField(max_length=64)),
                ('country_code', models.CharField(max_length=64)),
                ('country', models.CharField(max_length=64)),
                ('phone', models.CharField(blank=True, max_length=64, verbose_name='Phone number')),
                ('fax', models.CharField(blank=True, max_length=64, verbose_name='Fax number')),
                ('email', models.EmailField(max_length=254)),
                ('future_pay_id', models.CharField(blank=True, max_length=64)),
                ('card_type', models.CharField(blank=True, max_length=64)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
            ],
        ),
    ]
