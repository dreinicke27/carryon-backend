from flask import Blueprint, request, redirect
import stripe

checkoutBP = Blueprint("checkout", __name__, url_prefix="/create-checkout-session")

@checkoutBP.route("", methods=['POST'])
def create_checkout_session():
    data = request.json
    #try to get line items from request rather than here...have to be in the body from the form 
    line_item_data = data['line_items']
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1NYBhpFzSGyLRwvaltRdFK2s',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='https://carryon.onrender.com/',
            cancel_url='https://carryon.onrender.com/cart',
            automatic_tax={'enabled': True},
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)