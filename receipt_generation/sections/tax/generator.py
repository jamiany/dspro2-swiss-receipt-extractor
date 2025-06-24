import numpy.random as rng
from jinja2 import Template


def generate_tax(data):
    shop = data['shop']
    purchase = data['purchase']

    templates = [
        'template_1',
        'template_2',
    ]

    name = templates[rng.randint(len(templates))]

    with open(f'sections/tax/{name}.html') as f:
        template = Template(f.read())

        tax_table = {}

        for product in purchase['products']:
            if not product['tax_id'] in tax_table:
                percentage = 2 + rng.rand() * 10
                tax_table[product['tax_id']] = {
                    'percentage': round(percentage, 1),
                    'total': 0,
                    'tax': 0,
                }

            total = float(tax_table[product['tax_id']]['total']) + float(product['total'])
            tax = total * (float(tax_table[product['tax_id']]['percentage']) / 100)

            tax_table[product['tax_id']] = {
                'percentage': tax_table[product['tax_id']]['percentage'],
                'total': '%.2f' % total,
                'tax': '%.2f' % tax,
            }

        tax_list = []
        for key, value in tax_table.items():
            tax_list.append({
                'id': key,
                'percentage': value['percentage'],
                'total': value['total'],
                'tax': value['tax'],
            })

        result = template.render({
            'chain': shop['chain'].upper(),
            'tax_number': shop['tax'],
            'tax_list': tax_list,
        })

        return result
