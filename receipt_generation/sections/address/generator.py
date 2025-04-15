from jinja2 import Template


def generate_address(data):
    shop = data['shop']

    with open('sections/address/template_address.html') as f:
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
