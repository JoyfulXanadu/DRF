import stripe
import requests
from config.settings import STRIPE_API_KEY, APILAYER_API_KEY

stripe.api_key = STRIPE_API_KEY
def convert_rub_to_usd(amount):

    url = "https://api.apilayer.com/exchangerates_data/latest?base=USD"
    response = requests.get(url, headers={'apikey': APILAYER_API_KEY})
    if response.status_code == 200:
        rate = response.json()["rates"]["RUB"]
        return int(amount / rate)
def create_stripe_price(amount):

    return stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        product_data={"name": "payment_name"},
    )
def create_stripe_session(price):

    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
def check_payment(session_id):
    stripe.checkout.Session.retrieve(session_id)