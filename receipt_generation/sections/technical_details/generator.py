import numpy as np
from jinja2 import Template
import numpy.random as rng


def generate_technical_details(data):
    meta = data['meta']

    templates = [
        'template_1',
        'template_2',
    ]

    name = templates[rng.randint(len(templates))]

    with open(f'sections/technical_details/{name}.html') as f:
        template = Template(f.read())

        digit2 = rng.randint(0, 100)
        digit3 = rng.randint(0, 1_000)
        digit4 = rng.randint(0, 10_00)
        digit5 = rng.randint(0, 100_000)
        digit7 = rng.randint(0, 10_000_000)
        digit8 = rng.randint(0, 100_000_000)

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
            'date': meta['date'].strftime(date_format),
            'time': meta['time'].strftime(time_format),
            'digit2': str(digit2).zfill(2),
            'digit3': str(digit3).zfill(3),
            'digit4': str(digit4).zfill(4),
            'digit5': str(digit5).zfill(5),
            'digit7': str(digit7).zfill(7),
            'digit8': str(digit8).zfill(8),
        })

        return result
