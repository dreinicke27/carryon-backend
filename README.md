# carryon-backend

This project is the website for Carry On, a small business who creates one of a kind clothing and wares from upcycled and vintage textiles.  The site features a jacket customizer for custom orders, and links to a Shopify site for pre-made items.\

The frontend uses React, Bootstrap, and Email.js. The backend uses Postgres, Flask, and the Stripe API.

# Accept a Payment with Stripe Checkout

Stripe Checkout is the fastest way to get started with payments. Included are some basic build and run scripts you can use to start up the application.

## Running the sample

1. Build the server

~~~
pip3 install -r requirements.txt
~~~

2. Run the server

~~~
export FLASK_APP=server.py
python3 -m flask run --port=4242
~~~