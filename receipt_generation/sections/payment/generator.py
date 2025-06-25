import numpy as np
import numpy.random as rng
from jinja2 import Template


def generate_payment(data):
    purchase = data['purchase']
    meta = data['meta']

    templates = [
        'template_mastercard',
        # 'template_mastercard_2',
    ]

    name = templates[rng.randint(len(templates))]

    with open(f'sections/payment/{name}.html') as f:
        template = Template(f.read())

        digit4 = rng.randint(0, 10_000)
        digit6 = rng.randint(0, 1_000_000)
        digit8 = rng.randint(0, 100_000_000)
        digit11 = rng.randint(0, 100_000_000_000, dtype=np.int64)

        date_formats = (
            "%d.%m.%Y",
            "%d.%m.%y",
            "%d-%b-%Y",
            "%d-%b-%y",
        )
        date_format = date_formats[rng.randint(0, len(date_formats))]

        time_formats = (
            "%H:%M",
            "%H:%M:%S",
        )
        time_format = time_formats[rng.randint(0, len(time_formats))]

        result = template.render({
            'total_price': purchase['total_price'],
            'payment_method': purchase['payment_method'],
            'date': meta['date'].strftime(date_format),
            'time': meta['time'].strftime(time_format),
            'digit4': str(digit4).zfill(4),
            'digit6': str(digit6).zfill(6),
            'digit8': str(digit8).zfill(8),
            'digit11': str(digit11).zfill(11),
        })

        return result
