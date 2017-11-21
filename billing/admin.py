from django.contrib import admin
from fsm_admin.mixins import FSMTransitionMixin

import billing.models as billing_models

admin.site.register(billing_models.GCNewOrderNotification)
admin.site.register(billing_models.AuthorizeAIMResponse)
admin.site.register(billing_models.WorldPayResponse)
admin.site.register(billing_models.AmazonFPSResponse)
admin.site.register(billing_models.StripeTransaction)

class OrderAdmin(FSMTransitionMixin, admin.ModelAdmin):
    list_display = ('id', 'amount', 'state', 'created', 'modified')
    list_filter = ('state',)
    readonly_fields = ('state',)

    pass


admin.site.register(billing_models.Order, OrderAdmin)


class PaylaneTransactionAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_email', 'transaction_date', 'amount', 'success', 'error_code')
    list_filter = ('success',)
    ordering = ('-transaction_date',)
    search_fields = ['customer_name', 'customer_email']


admin.site.register(billing_models.PaylaneTransaction, PaylaneTransactionAdmin)
