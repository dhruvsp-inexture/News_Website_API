from flask import Blueprint

from public.resources import BuySubscription, PaymentSuccess, PaymentCancel

public = Blueprint("public", __name__)

public.add_url_rule("/buy_subscription", view_func=BuySubscription.as_view("buy_subscription"))
public.add_url_rule("/success", view_func=PaymentSuccess.as_view("payment_success"))
public.add_url_rule("/cancel", view_func=PaymentCancel.as_view("payment_cancel"))
