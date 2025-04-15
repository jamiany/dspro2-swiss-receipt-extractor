import numpy.random as rng
from jinja2 import Template


def generate_payment(data):
    purchase = data['purchase']
    meta = data['meta']

    with open('sections/payment/template_mastercard.html') as f:
        template = Template(f.read())

        digit4 = rng.randint(0, 10_000)
        digit6 = rng.randint(0, 1_000_000)
        digit8 = rng.randint(0, 100_000_000)
        digit11 = rng.randint(0, 100_000_000_000)

        result = template.render({
            'total_price': purchase['total_price'],
            'payment_method': purchase['payment_method'],
            'date': meta['date'].strftime("%d.%m.%Y"),
            'time': meta['time'].strftime("%H:%M:%S"),
            'digit4': str(digit4).zfill(4),
            'digit6': str(digit6).zfill(6),
            'digit8': str(digit8).zfill(8),
            'digit11': str(digit11).zfill(11),
        })

        return result
