from django.dispatch import Signal

transaction_started = Signal()
transaction_started.__doc__ = """
Sent after order was started (awaiting payment)
"""

transaction_was_successful = Signal(providing_args=['invoice'])
transaction_was_successful.__doc__ = """
Sent after order was completed (product, account,order)
"""


transaction_was_unsuccessful = Signal(providing_args=['invoice'])
transaction_was_unsuccessful.__doc__ = """
Sent after order was returned (product, account,order)
"""

order_canceled = Signal(providing_args=['invoice'])
order_canceled.__doc__ = """
Sent after order was canceled (product, account,order)
"""


order_novalid = Signal(providing_args=['product','user','instance'])
order_novalid.__doc__ = """
Sent after order was canceled (product, account,order)
"""



