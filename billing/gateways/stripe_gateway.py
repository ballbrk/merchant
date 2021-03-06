import stripe
from django.conf import settings

from billing import Gateway, GatewayNotConfigured
from billing.models import Order, State
from billing.models.stripe_models import StripeTransaction
from billing.signals import transaction_was_successful, transaction_was_unsuccessful
from billing.utils.credit_card import InvalidCard, Visa, MasterCard, \
    AmericanExpress, Discover, CreditCard
from cart.cart import Cart


class StripeGateway(Gateway):
    supported_cardtypes = [Visa, MasterCard, AmericanExpress, Discover]
    supported_countries = ['US']
    default_currency = "USD"
    homepage_url = "https://stripe.com/"
    display_name = "Stripe"

    def __init__(self):
        merchant_settings = getattr(settings, "MERCHANT_SETTINGS")
        if not merchant_settings or not merchant_settings.get("stripe"):
            raise GatewayNotConfigured("The '%s' gateway is not correctly "
                                       "configured." % self.display_name)
        stripe_settings = merchant_settings["stripe"]
        self.api_key = stripe_settings['API_KEY']
        self.stripe = stripe

    def purchase(self, amount, credit_card, metadata=None, options=None):
        card = credit_card
        currency = self.default_currency.lower()
        if options and options.get('currency', False):
            currency = options.pop('currency')
        customer = options and options.pop('customer', None)
        if isinstance(credit_card, CreditCard):
            if not self.validate_card(credit_card):
                raise InvalidCard("Invalid Card")
            card = {
                'number': credit_card.number,
                'exp_month': credit_card.month,
                'exp_year': credit_card.year,
                'cvc': credit_card.verification_value
            }
        stripe_transaction = StripeTransaction()
        try:
            print(metadata['invoice'])
            order = Order.objects.get(pk = metadata['invoice'])
            response = self.stripe.Charge.create(
                amount=int(amount * 100),
                currency=currency,
                card=card,
                customer=customer,
                metadata=metadata,
                api_key=self.api_key)
            stripe_transaction.payment_status = State.COMPLETED
            stripe_transaction.txn_id = response['id']
            stripe_transaction.info = response
            stripe_transaction.save()

            order.content_object = stripe_transaction
            order.finish()
            order.save()
            return {'status': 'SUCCESS', 'response': response}
        except self.stripe.CardError as error:
            stripe_transaction.payment_status = State.ERROR
            stripe_transaction.payment_message = error
            stripe_transaction.save()

            order.canceled()
            order.content_object = stripe_transaction
            order.save()
            return {'status': 'FAILURE', 'response': error}



    def store(self, credit_card, options=None):
        card = credit_card
        if isinstance(credit_card, CreditCard):
            if not self.validate_card(credit_card):
                raise InvalidCard("Invalid Card")
            card = {
                'number': credit_card.number,
                'exp_month': credit_card.month,
                'exp_year': credit_card.year,
                'cvc': credit_card.verification_value
            }
        try:
            customer = self.stripe.Customer.create(card=card, api_key=self.api_key)
        except (self.stripe.CardError, self.stripe.InvalidRequestError) as error:
            transaction_was_unsuccessful.send(sender=self,
                                              transaction_type="store",
                                              response=error)
            return {'status': 'FAILURE', 'response': error}
        transaction_was_successful.send(sender=self,
                                        transaction_type="store",
                                        response=customer)
        return {'status': 'SUCCESS', 'response': customer}

    def recurring(self, credit_card, options=None):
        card = credit_card
        if isinstance(credit_card, CreditCard):
            if not self.validate_card(credit_card):
                raise InvalidCard("Invalid Card")
            card = {
                'number': credit_card.number,
                'exp_month': credit_card.month,
                'exp_year': credit_card.year,
                'cvc': credit_card.verification_value
            }
        try:
            plan_id = options['plan_id']
            self.stripe.Plan.retrieve(options['plan_id'], api_key=self.api_key)
            try:
                response = self.stripe.Customer.create(
                    card=card,
                    plan=plan_id,
                    api_key=self.api_key
                )
                transaction_was_successful.send(sender=self,
                                                transaction_type="recurring",
                                                response=response)
                return {"status": "SUCCESS", "response": response}
            except self.stripe.CardError as error:
                transaction_was_unsuccessful.send(sender=self,
                                                  transaction_type="recurring",
                                                  response=error)
                return {"status": "FAILURE", "response": error}
        except self.stripe.InvalidRequestError as error:
            transaction_was_unsuccessful.send(sender=self,
                                              transaction_type="recurring",
                                              response=error)
            return {"status": "FAILURE", "response": error}
        except TypeError as error:
            transaction_was_unsuccessful.send(sender=self,
                                              transaction_type="recurring",
                                              response=error)
            return {"status": "FAILURE", "response": "Missing Plan Id"}

    def unstore(self, identification, options=None):
        try:
            customer = self.stripe.Customer.retrieve(identification, api_key=self.api_key)
            response = customer.delete()
            transaction_was_successful.send(sender=self,
                                            transaction_type="unstore",
                                            response=response)
            return {"status": "SUCCESS", "response": response}
        except self.stripe.InvalidRequestError as error:
            transaction_was_unsuccessful.send(sender=self,
                                              transaction_type="unstore",
                                              response=error)
            return {"status": "FAILURE", "response": error}

    def credit(self, identification, money=None, options=None):
        try:
            charge = self.stripe.Charge.retrieve(identification, api_key=self.api_key)
            if money:
                money = int(money * 100)
            response = charge.refund(amount=money)
            transaction_was_successful.send(sender=self,
                                            transaction_type="credit",
                                            response=response)
            return {"status": "SUCCESS", "response": response}
        except self.stripe.InvalidRequestError as error:
            transaction_was_unsuccessful.send(sender=self,
                                              transaction_type="credit",
                                              response=error)
            return {"status": "FAILURE", "error": error}

    def authorize(self, money, credit_card, options=None):
        card = credit_card
        currency = self.default_currency.lower()
        if options and options.get('currency', False):
            currency = options.pop('currency')
        if isinstance(credit_card, CreditCard):
            if not self.validate_card(credit_card):
                raise InvalidCard("Invalid Card")
            card = {
                'number': credit_card.number,
                'exp_month': credit_card.month,
                'exp_year': credit_card.year,
                'cvc': credit_card.verification_value
            }
        try:
            response = self.stripe.Charge.create(
                amount=int(money * 100),
                currency=currency,
                card=card,
                capture=False,
                api_key=self.api_key)
            transaction_was_successful.send(sender=self,
                                            transaction_type="authorize",
                                            response=response)
            return {'status': "SUCCESS", "response": response}
        except self.stripe.CardError as error:
            transaction_was_unsuccessful.send(sender=self,
                                              transaction_type="purchase",
                                              response=error)
            return {'status': 'FAILURE', 'response': error}

    def capture(self, money, identification, options=None):
        try:
            charge = self.stripe.Charge.retrieve(identification,
                                                 api_key=self.api_key)
            response = charge.capture(amount=int(money * 100))
            transaction_was_successful.send(sender=self,
                                            transaction_type="capture",
                                            response=response)
            return {'status': "SUCCESS", "response": response}
        except self.stripe.InvalidRequestError as error:
            transaction_was_unsuccessful.send(sender=self,
                                              transaction_type="capture",
                                              response=error)
            return {"status": "FAILURE", "response": error}
