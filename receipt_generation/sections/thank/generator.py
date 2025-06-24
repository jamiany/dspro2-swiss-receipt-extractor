import numpy as np
import numpy.random as rng
from jinja2 import Template


def generate_thank(data):
    shop = data['shop']

    templates = [
        'template_1',
        'template_2',
    ]

    name = templates[rng.randint(len(templates))]

    with open(f'sections/thank/{name}.html', encoding='utf-8') as f:
        template = Template(f.read())

        website = None
        if rng.randint(0, 2) == 1:
            website = shop['website']

        result = template.render({
            'website': website,
        })

        return result
