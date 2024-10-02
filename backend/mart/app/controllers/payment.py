

import json
from ..db.schemas.payment import PaymentRequest, PaymentResponse
from fastapi import APIRouter
import stripe
from fastapi import APIRouter, Request, Depends
from ..config.mt_config import MtConfig as mt_config
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..db.conn import get_db

class PaymentController:
    def __init__(self):
        self.router = APIRouter(tags=["payments"])
        self.router.add_api_route("/payment/process", self.process_payment, methods=["POST"], response_model=PaymentResponse)
        self.router.add_api_route("/payment/create-checkout-session", self.create_checkout_session, methods=["POST"])
        self.router.add_api_route("/payment/get/{payment_id}", self.get_payment_status, methods=["GET"], response_model=PaymentResponse)
        self.router.add_api_route("/payment/create-payment-intent", self.create_payment_intent, methods=["POST"], response_model=PaymentResponse)
    
    @staticmethod
    async def process_payment(payment_request: PaymentRequest):
        # Process payment logic
        return PaymentResponse(status="success", message="Payment processed successfully")
    
    @staticmethod
    async def create_checkout_session(request: Request):
        try:
            # Example data, you'll likely get this from your request body
            data = await request.json()
            price_id = data.get("priceId")
            stripe.api_key = mt_config.STRIPE_SECRET_KEY
            price_id = stripe.price.create(
                currency="usd",
                unit_amount=1000,
                product_data=[{"name": "Gold Plan", "product_id":"prod_1234567890"}],
            )
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': '{{price_id}}',
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url='http://localhost:3000/success',
                cancel_url='http://localhost:3000/cancel',
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return str(e)

    @staticmethod
    async def get_payment_status(payment_id: int, db: Session=Depends(get_db)):
        # Retrieve payment status logic
        payment = PaymentService(db).get_by_id(payment_id)

        return PaymentResponse(status="success", data=payment)

    @staticmethod
    async def create_payment_intent(self, request: Request):
        try:
            data = json.loads(request.data)
            # Create a PaymentIntent with the order amount and currency
            intent = stripe.PaymentIntent.create(
                amount=self.calculate_order_amount(data['items']),
                currency='usd',
                # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            return JSONResponse({
                'clientSecret': intent['client_secret'],
            # [DEV]: For demo purposes only, you should avoid exposing the PaymentIntent ID in the client-side code.
            'dpmCheckerLink': 'https://dashboard.stripe.com/settings/payment_methods/review?transaction_id={}'.format(intent['id']),
                 })
        except Exception as e:
            return JSONResponse(error=str(e)), 403    
    @staticmethod
    async def get_payment_status(payment_id: int, db: Session=Depends(get_db)):
        # Retrieve payment status logic
        payment = PaymentService(db).get_by_id(payment_id)

        return PaymentResponse(status="success", data=payment)