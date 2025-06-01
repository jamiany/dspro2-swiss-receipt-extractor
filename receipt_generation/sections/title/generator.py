import os

from jinja2 import Template
import numpy.random as rng


def generate_title(data):
    shop = data['shop']

    with open('sections/title/template_title.html') as f:
        template = Template(f.read())

        v = rng.rand()
        if v > 0.9:
            result = template.render({
                'use_image': False,
                'title': shop['chain']
            })
        elif v > 0.8:
            result = template.render({
                'use_image': False,
                'title': shop['chain'].upper()
            })
        else:
            result = template.render({
                'use_image': True,
                'image_src': get_image(shop['chain'])
            })

        return result


def get_image(shop):
    shops = {
        "Aldi": 1,
        "Billa": 2,
        "Coop": 2,
        "Edeka": 2,
        "Globus": 2,
        "Lidl": 3,
        "Migros": 2,
        "Netto": 2,
        "Penny": 4,
        "Real": 2,
        "Rewe": 3,
        "Spar": 2,
    }

    cwd = os.getcwd()
    idx = rng.randint(1, shops[shop] + 1)

    return f'{cwd}/images/logos/{shop.lower()}_{idx}.png'

