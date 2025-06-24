import numpy.random as rng
from jinja2 import Template


def generate_total(data):
    purchase = data['purchase']

    templates = [
        'template_1',
    ]

    name = templates[rng.randint(len(templates))]

    with open(f'sections/total/{name}.html') as f:
        template = Template(f.read())

        # TODO move in receipt gen?
        exchange_rate = 0.75 + (rng.rand() / 2)

        style = rng.randint(0, 2)
        bold = rng.randint(0, 2)

        border_top = True
        small_border = rng.randint(0, 2)

        result = template.render({
            'payment_method': purchase['payment_method'],
            'total_price': purchase['total_price'],
            'total_price_currency': '%.2f' % (float(purchase['total_price']) * exchange_rate),
            'style': style,
            'bold': 'bold' if bold == 0 else '',
            'small_border': small_border,
        })

        return result
