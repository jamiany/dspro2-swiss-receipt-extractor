import numpy.random as rng
from jinja2 import Template


def generate_total(data):
    purchase = data['purchase']

    with open('sections/total/template_2.html') as f:
        template = Template(f.read())

        # TODO move in receipt gen?
        exchange_rate = 0.75 + (rng.rand() / 2)

        result = template.render({
            'payment_method': purchase['payment_method'],
            'total_price': purchase['total_price'],
            'total_price_currency': '%.2f' % (float(purchase['total_price']) * exchange_rate),
        })

        return result
