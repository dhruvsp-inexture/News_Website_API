import os
from datetime import date
import stripe
from flask_api import status
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from app import db
from public.models import PremiumUserMapping
from public.utils import user_required
from users.models import User

stripe_keys = {
    'secret_key': os.environ.get('STRIPE_SECRET_KEY'),
    'publishable_key': os.environ.get('STRIPE_PUBLISHABLE_KEY')
}
stripe.api_key = stripe_keys['secret_key']


class BuySubscription(Resource):
    decorators = [jwt_required(), user_required()]

    def get(self):
        user = User.query.filter_by(id=get_jwt_identity()).first()
        if not user.has_premium:
            invoice = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': 'Subscription',
                        },
                        'unit_amount': int(199 * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                # both url  will be called from frontend side
                success_url=os.environ.get('HOST') + '/success',
                cancel_url=os.environ.get('HOST') + '/cancel',
            )
            card_obj = stripe.PaymentMethod.create(
                type="card",
                card={
                    "number": "4242424242424242",
                    "exp_month": 7,
                    "exp_year": 2023,
                    "cvc": "123",
                },
            )
            customer = stripe.Customer.create(
                email=user.email, payment_method=card_obj.id
            )
            stripe.PaymentIntent.create(
                customer=customer.id,
                payment_method=card_obj.id,
                currency="inr",
                amount=int(199 * 100),
                description='No Nonsense News Subscription Charge'
            )

            return {"data": invoice["url"],
                    "message": "click on following link to complete the payment",
                    "status": "true"
                    }, status.HTTP_200_OK

        else:
            return {"data": [],
                    "message": "Subscription already purchased",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class PaymentSuccess(Resource):
    decorators = [jwt_required(), user_required()]

    def get(self):
        user = User.query.filter_by(id=get_jwt_identity()).first()
        user.has_premium = True
        subscribed_user = PremiumUserMapping(user_id=user.id, purchase_date=date.today())
        db.session.add(subscribed_user)
        db.session.commit()
        return {"data": [],
                'message': 'Congrats, now you are a premium user!!!',
                "status": "true"
                }, status.HTTP_200_OK


class PaymentCancel(Resource):
    decorators = [jwt_required(), user_required()]

    def get(self):
        return {"data": [],
                "message": "Payment Cancelled. Please try again!",
                "status": "true"
                }, status.HTTP_200_OK
