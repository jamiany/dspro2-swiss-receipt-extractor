import numpy as np
import numpy.random as rng
from jinja2 import Template


def generate_product_table(data):
    purchase = data['purchase']

    templates = [
        'template_napat',
        'template_anpt',
        'template_napati',
    ]

    name = templates[rng.randint(len(templates))]

    with open(f'sections/product_table/{name}.html') as f:
        template = Template(f.read())

        result = template.render({
            'products': purchase['products'],
        })

        return result
