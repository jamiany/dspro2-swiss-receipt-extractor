import numpy as np
import numpy.random as rng
from jinja2 import Template


def generate_address(data):
    shop = data['shop']

    templates = [
        'template_address',
        'template_branch',
    ]

    name = templates[rng.randint(len(templates))]

    with open(f'sections/address/{name}.html') as f:
        template = Template(f.read())

        result = template.render({
            'chain': shop['chain'],
            'branch': shop['branch'],
            'address': shop['address'],
            'postcode': shop['postcode'],
            'city': shop['city'],
            'telephone': shop['telephone'],
            'email': shop['email'],
            'website': shop['website'],
        })

        return result
