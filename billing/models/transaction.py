# !/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext as _
from django_extensions.db.models import TimeStampedModel
from django_fsm import FSMField, transition
from djmoney.models.fields import MoneyField

from ..signals import *


class State(object):
    '''
    Constants to represent the `state`s of the Order
    '''

    NEW = 'New'
    COMPLETED = 'Completed'
    NO_VALID = 'No Valid'
    CANCELED = 'Canceled'
    RETURNED = 'Returned'
    ERROR = 'Error'


    CHOICES = (
        (NEW, _("New")),
        (COMPLETED, _("Completed")),
        (NO_VALID, _("No Valid")),
        (CANCELED, _("Canceled")),
        (RETURNED, _("Returned")),
        (ERROR, _("Error")),
    )


class Order(TimeStampedModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True,related_name='billing_order')
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    amount = MoneyField(max_digits=10, decimal_places=2, default_currency='EUR')
    state = FSMField(default=State.NEW,
                     verbose_name=_(u'Order State'),
                     choices=State.CHOICES,
                     protected=True,
                     db_index=True)

    class Meta:
        ordering = ('id',)
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return "%s" % self.id

    def save(self, **kwargs):
        if self.pk is None:
            transaction_started.send(sender=self.__class__)
        super(self.__class__, self).save(**kwargs)

    @transition(field=state, source=State.NEW, target=State.COMPLETED)
    def finish(self):
        transaction_was_successful.send(sender=self.__class__, invoice=self.pk)

    @transition(field=state, source=State.NEW, target=State.NO_VALID)
    def no_valid(self):
        transaction_was_unsuccessful.send(sender=self.__class__, invoice=self.pk)

    @transition(field=state, source=State.NEW, target=State.CANCELED)
    def canceled(self):
        transaction_was_unsuccessful.send(sender=self.__class__, invoice=self.pk)

    @transition(field=state, source=State.COMPLETED, target=State.RETURNED)
    def returned(self):
        transaction_was_unsuccessful.send(sender=self.__class__, invoice=self.pk)
