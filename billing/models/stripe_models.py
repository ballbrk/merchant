# -*- coding: utf-8 -*-
# vim:tabstop=4:expandtab:sw=4:softtabstop=4

from django.db import models
from django.contrib.postgres.fields import JSONField
from .transaction import State


class StripeTransaction(models.Model):
    txn_id = models.CharField(max_length=255,blank=True,null=True,db_index=True)
    payment_status = models.CharField(default=State.NEW,choices=State.CHOICES,db_index=True,max_length=200)
    payment_message = models.CharField(max_length=200,null=True,blank=True)
    info = JSONField(null=True,blank=True)

    pass